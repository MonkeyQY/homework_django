from django.urls import path
from . import views

app_name = 'menu'
urlpatterns = [
    path('', views.menu, name='menu'),
    path('menu', views.menu, name='menu'),
    path('meal_statistics', views.meals_statistics, name='meals_statistics'),
    path('<int:meal_id>/statistics', views.meal_statistic, name='statistic_for_meal'),
    path('<meal_category>', views.meal_category, name='meal_category'),
    path('<int:meal_id>/meal', views.meal, name='meal'),

]
