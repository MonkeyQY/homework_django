from django.contrib.auth.models import User, AnonymousUser
from django.db.models import QuerySet
from django.shortcuts import render, redirect

from .charts.meal_statistic_char import get_char_for_meal
from .models import Meal
from django.utils import timezone
from django.http import HttpRequest


def menu(request: HttpRequest):
    meal_categories = list(filter(lambda el: 'NO_TYPE' not in el[0], Meal.MealType.choices))
    return render(request,
                  'cafe_core_app/menu.html',
                  {'meal_categories': meal_categories})


def meal_category(request: HttpRequest, meal_category: str):
    meals_by_category = Meal.objects.filter(meal_type=meal_category)
    return render(request,
                  'cafe_core_app/meals.html',
                  {'meals': meals_by_category,
                   'meal_category': meal_category})


def meal(request: HttpRequest, meal_id: int):
    meal = Meal.objects.get(id=meal_id)
    user = request.user

    if isinstance(user, AnonymousUser):
        return redirect('login')

    meal.mealclick_set.create(clicked_user=user, click_date=timezone.now())
    return render(request,
                  'cafe_core_app/meal.html',
                  {'meal': meal})


def meals_statistics(request: HttpRequest):
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
        if len(dict_meals) == 3:
            break
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
    return render(request,
                  'cafe_core_app/meal_statistic.html',
                  {'meal': meal,
                   'meal_clicks': meal_clicks,
                   "fig": fig})


def user_statistic(request: HttpRequest):
    users = User.objects.all()

    list_users = filter_user(users, 10)

    # сортировка по количеству кликов
    meals = sorted(list_users, key=lambda user: user['clicks'], reverse=True)
    enumerate_users = index(meals)

    return render(request,
                  'cafe_core_app/statistics_for_user/user_statistic_total.html',
                  {"users": enumerate_users})


def user_statistics_for_category(request: HttpRequest):
    list_users = []
    meals_category = None
    if request.method == 'POST':
        count_user = request.POST.get("count_user")
        meals_category = request.POST.get("meals_category")

        users = User.objects.all()
    # TODO переписать это в нормальный вид, без дублирования кода
        for user in users:
            if len(list_users) == count_user:
                break
            meal = Meal.objects.filter(mealclick__clicked_user=user, meal_type=meals_category)
            clicks = meal.count()
            list_users.append({'user': user.first_name, "clicks": clicks})

    sorted_list_users = sorted(list_users, key=lambda user: user['clicks'], reverse=True)
    statistics = index(sorted_list_users)

    meals = Meal.MealType.values
    meals = list(filter(lambda el: 'NO_TYPE' not in el, meals))

    return render(request,
                  'cafe_core_app/statistics_for_user/user_statistic_for_meals_category.html',
                  {'category': meals_category, "statistics": statistics, "meals": meals})


def user_statistics(request):
    return render(request, 'cafe_core_app/statistics_for_user/user_statistic_home.html')


def filter_user(users: QuerySet[User], count: int):
    list_users = []
    for user in users:
        if len(list_users) == count:
            break
        meal = Meal.objects.filter(mealclick__clicked_user=user)
        clicks = meal.count()
        list_users.append({'user': user.first_name, "clicks": clicks})
    return list_users

