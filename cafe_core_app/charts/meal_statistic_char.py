import time

import plotly.express as px

from datetime import date

from cafe_core_app.models import Meal

today = date.today()


def get_char_for_meal(meal: Meal, period: str = "day") -> str:
    """Возвращает график для блюда"""
    #  в зависимости от периода отображения достаём с базы данных данные и фильтруем их по периоду и по
    #  y передаём количество кликов в этот период
    meals = meal.mealclick_set.all()

    list_of_dates, list_of_clicks = select_period(period)
    for meal in meals:
        number, count = filter_date(meal, period)
        list_of_clicks[number - 1] = count

    if period == "year":
        range_x = [list_of_dates[0], list_of_dates[-1]]
    else:
        range_x = [0, len(list_of_dates)]

    # строим график с помощью plotly
    df = px.bar(
        x=list_of_dates,
        y=list_of_clicks,
        range_x=range_x,
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
        case "month":
            number = meal.click_date.month
            count = meal.meal.mealclick_set.filter(click_date__month=number, click_date__year=today.year).count()

        case "year":
            number = meal.click_date.year
            count = meal.meal.mealclick_set.filter(click_date__year=number).count()
            number = number - today.year + 11
        case _:
            number = meal.click_date.day
            count = meal.meal.mealclick_set.filter(click_date__day=number, click_date__month=today.month).count()

    return number, count


def select_period(period: str):
    match period:
        case "hour":
            list_of_dates = [i for i in range(0, 24)]
            list_of_clicks = [0 for i in range(0, 24)]
            return list_of_dates, list_of_clicks
        case "month":
            list_of_dates = [i for i in range(1, 13)]
            list_of_clicks = [0 for i in range(1, 13)]
            return list_of_dates, list_of_clicks
        case "year":
            list_of_dates = [i for i in range(today.year - 10, today.year + 1)]
            list_of_clicks = [0 for i in range(today.year - 10, today.year + 1)]
            return list_of_dates, list_of_clicks
        case _:
            list_of_dates = [i for i in range(1, 32)]
            list_of_clicks = [0 for i in range(1, 32)]
            return list_of_dates, list_of_clicks
