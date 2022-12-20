from django.db.models import QuerySet
from django.shortcuts import render

from .charts.meal_statistic_char import get_char_for_meal
from .models import Meal
from django.utils import timezone
from django.http import HttpRequest


def menu(request: HttpRequest):
    meal_categories = list(filter(lambda el: 'NO_TYPE' not in el[0], Meal.MealType.choices))
    return render(request, 'cafe_core_app/menu.html', {'meal_categories': meal_categories})


def meal_category(request: HttpRequest, meal_category: str):
    meals_by_category = Meal.objects.filter(meal_type=meal_category)
    return render(request, 'cafe_core_app/meals.html', {'meals': meals_by_category, 'meal_category': meal_category})


def meal(request: HttpRequest, meal_id: int):
    meal = Meal.objects.get(id=meal_id)
    meal.mealclick_set.create(click_date=timezone.now())
    return render(request, 'cafe_core_app/meal.html', {'meal': meal})


def meals_statistics(request: HttpRequest):
    """ Не делал ограничение по кол-ву выводимых блюд, т.к. в задании не было указано """
    meals = Meal.objects.all()

    # сортировка по количеству кликов
    meals = sorted(meals, key=lambda meal: meal.mealclick_set.count(), reverse=True)

    enumerate_meals = index(meals)

    return render(request, 'cafe_core_app/meals_statistics.html',
                  {'meals': enumerate_meals})


# TODO  Переделать этот костыль. Чтобы это работало на фронте.
def index(meals: list) -> dict:
    dict_meals = {}
    i = 1

    for meal in meals:
        dict_meals.update({i: meal})
        i += 1

    return dict_meals


def meal_statistic(request: HttpRequest, meal_id: int, period: str = 'hour'):
    """Выведем всю статистику по данному блюду"""
    if request.method == 'POST':
        period = request.POST.get("format")

    meal: Meal = Meal.objects.get(id=meal_id)

    meal_clicks = meal.mealclick_set.count()

    fig = get_char_for_meal(meal, period)
    return render(request, 'cafe_core_app/meal_statistic.html', {'meal': meal, 'meal_clicks': meal_clicks, "fig": fig})
