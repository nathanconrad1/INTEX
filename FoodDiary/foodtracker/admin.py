from django.contrib import admin
from . models import Food, Target_Diet, Person, DailyConsumed, FoodConsumed


# Register your models here.
admin.site.register(Food)
admin.site.register(Target_Diet)
admin.site.register(Person)
admin.site.register(DailyConsumed)
admin.site.register(FoodConsumed)