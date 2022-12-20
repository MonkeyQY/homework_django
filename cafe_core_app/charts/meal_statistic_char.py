import plotly.express as px

from datetime import date

from cafe_core_app.models import Meal

today = date.today()


def get_char_for_meal(meal: Meal, period: str = "day") -> str:
    """Возвращает график для блюда"""
    #  в зависимости от периода отображения достаём с базы данных данные и фильтруем их по периоду и по
    #  y передаём количество кликов в этот период
    meals = meal.mealclick_set.all()

    list_of_dates = []
    list_of_clicks = []
    for meal in meals:
        number, count = filter_date(meal, period)

        if number not in list_of_dates:
            list_of_dates.append(number)
            list_of_clicks.append(count)

    # строим график с помощью plotly
    df = px.bar(
        x=list_of_dates,
        y=list_of_clicks,
        range_x=[0, 24],
        title='График кликов по блюду',
        labels={'x': f'Время, {period}', 'y': 'Количество кликов, единиц'}
    )
    char = df.to_html()

    return char


def filter_date(meal, period: str) -> tuple[int, int]:
    """Фильтрует дату по периоду"""
    match period:
        case "hour":
            number = meal.click_date.hour
            count = meal.meal.mealclick_set.filter(click_date__hour=number, click_date__day=today.day).count()
            number = meal.click_date.time().replace(microsecond=False, second=False, minute=False)
        case "month":
            number = meal.click_date.month
            count = meal.meal.mealclick_set.filter(click_date__month=number, click_date__year=today.year).count()

        case "year":
            number = meal.click_date.year
            count = meal.meal.mealclick_set.filter(click_date__year=number).count()
        case _:
            number = meal.click_date.day
            count = meal.meal.mealclick_set.filter(click_date__day=number, click_date__month=today.month).count()

    return number, count
