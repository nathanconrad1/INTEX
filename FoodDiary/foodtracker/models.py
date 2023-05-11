from django.db import models
from datetime import datetime

# Create your models here.
class Food(models.Model):
    food_name = models.CharField(max_length = 30, primary_key=True)
    food_K = models.DecimalField(default = 0.0, decimal_places = 2, max_digits = 6)
    food_na = models.DecimalField(default = 0.0, decimal_places = 2, max_digits = 6)
    food_phos = models.DecimalField(default = 0.0, decimal_places = 2, max_digits = 6)
    food_protein = models.DecimalField(default = 0.0, decimal_places = 2, max_digits = 6)
    food_water = models.DecimalField(default = 0.0, decimal_places = 2, max_digits = 6)
    
    def __str__(self) :
        return str(self.food_name)
    
    class Meta:
        db_table = 'food'

class Target_Diet(models.Model):

    DIETS = (
        ('3/4 Men', '3/4 Men'),
        ('3/4 Women', '3/4 Women'),
        ('Dialysis', 'Dialysis')
    )

    diet_name = models.CharField(max_length = 15, choices = DIETS, primary_key = True)
    protein_limit = models.DecimalField(default = 0.0, decimal_places = 2, max_digits = 8)
    k_limit = models.DecimalField(default = 0.0, decimal_places = 2, max_digits = 8)
    phos_limit = models.DecimalField(default = 0.0, decimal_places = 2, max_digits = 8)
    water_limit = models.DecimalField(default = 0.0, decimal_places = 2, max_digits = 8)
    na_limit = models.DecimalField(default = 0.0, decimal_places = 2, max_digits = 8)
    
    def __str__(self):
        return str(self.diet_name)
    
    class Meta: 
        db_table = 'target_diet'

    def __unicode__(self):
        return self.diet_name
        
class Person(models.Model):

    CONDITIONS = (
        ('Diabetes', 'Diabetes'),
        ('High Blood Pressure', 'High Blood Pressure'),
    )

    GENDERS = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )

    email = models.EmailField(max_length = 254, primary_key = True)
    firstName = models.CharField(max_length = 20)
    lastName = models.CharField(max_length = 30)
    gender = models.CharField(max_length = 7, choices = GENDERS, null = False, blank = False)
    age = models.IntegerField(default = 0)
    weight = models.IntegerField(default = 0)
    height = models.IntegerField(default = 0)
    diet_name = models.ForeignKey(Target_Diet, on_delete = models.CASCADE)
    comorbidity = models.CharField(max_length = 20, choices = CONDITIONS, null = False, blank = False)

    def __str__(self) :
        return (str(self.email))
    
    class Meta:
        db_table = 'person'

class DailyConsumed(models.Model):

    HEALTH = (
        ('Very Poor', 'Very Poor'),
        ('Poor', 'Poor'),
        ('Fair', 'Fair'),
        ('Good', 'Good'),
        ('Very Good', 'Very Good'),
    )
    
    dcid = models.AutoField(primary_key = True)
    date = models.DateField(default = datetime.today)
    email = models.ForeignKey(Person, on_delete = models.CASCADE)
    total_k = models.DecimalField(default = 0.0, decimal_places = 2, max_digits = 6)
    total_na = models.DecimalField(default = 0.0, decimal_places = 2, max_digits = 6)
    total_phos = models.DecimalField(default = 0.0, decimal_places = 2, max_digits = 6)
    total_water = models.DecimalField(default = 0.0, decimal_places = 2, max_digits = 6)
    total_protein = models.DecimalField(default = 0.0, decimal_places = 2, max_digits = 6)
    systolic_bp = models.IntegerField(default = 0, blank = True)
    diastolic_bp = models.IntegerField(default = 0, blank = True)
    blood_glucose = models.IntegerField(default = 0, blank = True)
    mentalHealthRating = models.CharField(max_length = 9, choices = HEALTH, null = True)
    goal_obtained = models.BooleanField()

    #Add this line
    consumedFood = models.ManyToManyField('Food', through='FoodConsumed')

    def __str__(self):
        return (str(self.dcid))
    
    class Meta:
        db_table = 'daily_consumed'

class FoodConsumed(models.Model):
    dcid = models.ForeignKey(DailyConsumed, on_delete = models.CASCADE)
    food_name = models.ForeignKey(Food, on_delete = models.CASCADE)
    quantity = models.IntegerField(default = 0)
    
    def __str__(self) :
        return (str(self.food_name))
    
    class Meta:
        db_table = 'food_consumed'