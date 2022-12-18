from django.shortcuts import render
from .models import Meal
from django.utils import timezone


def menu(request):
    meal_categories = list(filter(lambda el: 'NO_TYPE' not in el[0], Meal.MealType.choices))
    return render(request, 'cafe_core_app/menu.html', {'meal_categories': meal_categories})


def meal_category(request, meal_category):
    meals_by_category = Meal.objects.filter(meal_type=meal_category)
    return render(request, 'cafe_core_app/meals.html', {'meals': meals_by_category, 'meal_category': meal_category})


def meal(request, meal_id):
    meal = Meal.objects.get(id=meal_id)
    meal.mealclick_set.create(click_date=timezone.now())
    return render(request, 'cafe_core_app/meal.html', {'meal': meal})


def meal_statistics(request):
    pass
