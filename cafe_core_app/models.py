from django.db import models


class Meal(models.Model):
    name = models.CharField('Название блюда', max_length=100)
    description = models.TextField('Описание блюда')
    price = models.IntegerField('Стоимость блюда')
    size = models.IntegerField('Вес блюда')

    class MealType(models.TextChoices):
        HOT_MEALS = 'Hot meals'
        DRINK = 'Drinks'
        DESSERT = 'Dessert'
        NO_TYPE = 'NO_TYPE'

    meal_type = models.CharField(
        max_length=30,
        choices=MealType.choices,
        default=MealType.NO_TYPE
    )


class MealClick(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.DO_NOTHING)
    click_date = models.DateTimeField('Дата клика')
