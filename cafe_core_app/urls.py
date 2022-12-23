from django.urls import path
from . import views

app_name = 'cafe_core_app_1'
urlpatterns = [
    path('', views.menu, name='menu'),
    path('menu', views.menu, name='menu'),
    path('meal_statistics', views.meals_statistics, name='meals_statistics'),
    path('<int:meal_id>/statistics', views.meal_statistic, name='statistic_for_meal'),
    path('<meal_category>', views.meal_category, name='meal_category'),
    path('<int:meal_id>/meal', views.meal, name='meal'),

    path('user/statistic/', views.user_statistics, name='user_statistic'),
    path('user/statistic/clicked/', views.user_statistic, name='user_clicked_statistic'),
    path('user/statistic/meals_category/', views.user_statistics_for_category, name='user_statistic_for_category'),
]
