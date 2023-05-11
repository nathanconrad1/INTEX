# Create your views here.
from django.shortcuts import  render, redirect
from .forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .models import Target_Diet
from .forms import Target_Diet_Form
from .models import Person, DailyConsumed, FoodConsumed
from .models import Food, Target_Diet
import requests
import json
from decimal import Decimal
from datetime import date
from django.http import HttpResponse
#initializing id variable
current_dc = 0

#login function checks email and renders index page
def login_request(request):

	tryEmail = request.POST.get('email')
	global current_person

	listEmails = []
	for person in Person.objects.all() :
		listEmails.append(person.email)

	if tryEmail in listEmails :

		login_person = Person.objects.get(email=tryEmail)
	
		current_person = login_person
		
		global current_dc
		current_dc = storeDailyConsumed(current_person)
		# print(current_dc.dcid)
		context = {
			"current_person": current_person,
			"current_dc": current_dc,
		}
		
		# context = storeDailyConsumed(request, tryEmail)
		return render(request, "foodtracker/index.html", context)
	
	else: 
		
		diet_names = Target_Diet.objects.all()
		people = Person.objects.all()
	
		form = UserCreationForm()
		
		context = {
			"diet_names" : diet_names,
			"new_form" : form,
			"people" : people,
			}

		return render(request, "foodtracker/new.html", context)


# create a new user
def register_request(request):
	diet_names = Target_Diet.objects.all()
	people = Person.objects.all()
	
	if request.method == "POST":
		form = UserCreationForm(request.POST)
	
	form = UserCreationForm()
	
	context = {
		"diet_names" : diet_names,
		"new_form" : form,
		"people" : people,
  		}

	return render(request, "foodtracker/new.html", context)

#stores a new person
def AccountPageView(request):
	
	current_person = Person.objects.get(email=request.POST.get('email'))
	
	
	current_dc = DailyConsumed.objects.get(dcid=request.POST.get('dcid'))
	context = {
		'current_dc' : current_dc,
		'current_person' : current_person
	}

	return render(request, "foodtracker/storePerson.html", context)

def successPageView(request):
    return render(request, 'foodtracker/success.html')

#logs user out
def logOutPageView(request):
    return render(request, 'foodtracker/new.html')

#creates the radial visualization
def radialPageView(request):
	current_person = Person.objects.get(email = request.POST.get('email'))
	current_dc = DailyConsumed.objects.get(dcid = request.POST.get('dcid'))
	target_diet = Target_Diet.objects.get(diet_name = current_person.diet_name_id)
	protein_limit = ((current_person.weight * target_diet.protein_limit))
	
	k = (current_dc.total_k / target_diet.k_limit) * 100
	protein = (current_dc.total_protein / protein_limit) * 100
	water = (current_dc.total_water / target_diet.water_limit) * 100
	phos = (current_dc.total_phos / target_diet.phos_limit) * 100
	na = (current_dc.total_na / target_diet.na_limit) * 100
    
	if (k >= 100) and (protein >= 100) and (water >= 100) and (phos >= 100) and (na >= 100) :
		current_dc.goal_obtained = True
	else :
		current_dc.goal_obtained = False
	current_dc.save()

	exceeded = []
	recommended = []

	if (k > 100) :
		exceeded.append("Potassium: You are at " + str(round(k,2)) + "% of your daily limit")
	else :
		recommended.append('Potassium')
	if (protein > 100) :
		exceeded.append("Protein: You are at " + str(round(protein,2)) + "% of your daily limit")
	else :
		recommended.append('Protein')
	if (phos > 100) :
		exceeded.append("Phosphorus: You are at " + str(round(phos,2)) + "% of your daily limit")
	else :
		recommended.append('Phosphorus')
	if (na > 100):
		exceeded.append("Sodium: You are at " + str(round(na,2)) + "% of your daily limit")
	else :
		recommended.append('Sodium')
	if (water > 100):
		exceeded.append("Water: You are at " + str(round(water,2)) + "% of your daily limit")
	else :
		recommended.append('Water')

	if (len(recommended) == 5):
		context = {
			"k" : k,
			"protein" : protein,
			"water" : water,
			"phos" : phos,
			"na" : na,
			"current_person" : Person.objects.get(email=request.POST.get('email')),
			"current_dc" : DailyConsumed.objects.get(dcid=request.POST.get('dcid')),
			"exceeded" : exceeded,
			"length_e" : False,
			"recommended" : recommended,
			"length_r" : True
		}
		return render(request, 'foodtracker/index.html', context)

	elif (len(exceeded) == 5) :
		context = {
			"k" : k,
			"protein" : protein,
			"water" : water,
			"phos" : phos,
			"na" : na,
			"current_person" : Person.objects.get(email=request.POST.get('email')),
			"current_dc" : DailyConsumed.objects.get(dcid=request.POST.get('dcid')),
			"exceeded" : exceeded,
			"length_e" : True,
			"recommended" : recommended,
			"length_r" : False
		}
		return render(request, 'foodtracker/index.html', context)
	
	else :
		context = {
			"k" : k,
			"protein" : protein,
			"water" : water,
			"phos" : phos,
			"na" : na,
			"current_person" : Person.objects.get(email=request.POST.get('email')),
			"current_dc" : DailyConsumed.objects.get(dcid=request.POST.get('dcid')),
			"exceeded" : exceeded,
			"length_e" : True,
			"recommended" : recommended,
			"length_r" : True
		}
		return render(request, 'foodtracker/index.html', context)
#  
def index(request):
# 	data = Food.objects.all()
# 	if request.method == 'POST':
# 		form = Food_Form(request.POST)
# 		if form.is_valid():
# 			form.save()
# 			return redirect('/')
# 	else:
# 		form = Food_Form()
	# context = {
    #     'data': data,
    #     'form': form,
    # 	}
	context = {
		"current_person" : Person.objects.get(email=request.POST.get('email')),
		"current_dc" : DailyConsumed.objects.get(dcid=request.POST.get('dcid')),
	}
	return render(request, 'foodtracker/index.html', context)

#saves the information for a new person
def storePersonPageView(request) :

	new_person = Person()

	new_person.firstName = request.POST.get('firstName')
	new_person.lastName = request.POST.get('lastName')
	new_person.email = request.POST.get('email')
	new_person.gender = request.POST.get('gender')
	new_person.age = request.POST.get('age')
	new_person.height = request.POST.get('height')
	new_person.weight = request.POST.get('weight')
	new_person.comorbidity = request.POST.get('comorbidity')
	new_person.diet_name_id = request.POST.get('diet_name')
	
	new_person.save()
	global current_person
	current_person = new_person

	global current_dc
	new_consumed = userPageView(new_person)
	current_dc = new_consumed

	context = {
		"current_person" : current_person,
		"current_dc" : current_dc
	}
	return render(request, "foodtracker/index.html", context)

#Intializes daily consumed table
def userPageView(person) :
	people = Person.objects.get(email=person.email)

	new_daily_consumed = DailyConsumed()

	new_daily_consumed.email_id = people.email
	new_daily_consumed.date = date.today()
	new_daily_consumed.total_k= 0
	new_daily_consumed.total_na = 0
	new_daily_consumed.total_water = 0
	new_daily_consumed.total_phos = 0
	new_daily_consumed.total_protein = 0
	new_daily_consumed.systolic_bp= 0
	new_daily_consumed.diastolic_bp = 0
	new_daily_consumed.blood_glucose= 0
# Change to None
	new_daily_consumed.mentalHealthRating = 'Okay'
	new_daily_consumed.goal_obtained = False

	new_daily_consumed.save()

	return (new_daily_consumed)
	# return render(request, "foodtracker/account.html", context)

	
#daily consumed stored
def storeDailyConsumed(person) :
	
	daily_consumed = DailyConsumed.objects.get(email_id=person.email, date=date.today())
	if daily_consumed :
		return (daily_consumed)
	else:
		new_daily_consumed = DailyConsumed()

		new_daily_consumed.email_id =  person.email
		new_daily_consumed.date = date.today()
		new_daily_consumed.total_k= 0
		new_daily_consumed.total_na = 0
		new_daily_consumed.total_water = 0
		new_daily_consumed.total_phos = 0
		new_daily_consumed.total_protein = 0
		new_daily_consumed.systolic_bp= 0
		new_daily_consumed.diastolic_bp = 0
		new_daily_consumed.blood_glucose= 0
# Change to None
		new_daily_consumed.mentalHealthRating = 'Okay'
		new_daily_consumed.goal_obtained = False
		new_daily_consumed.save()
		return(new_daily_consumed)


#takes them to account page
def accountPageView(request):
	email = request.POST.get('email')
	
	person = Person.objects.filter(email=email)
	context = {
		"current_person": person,
		"email" : request.POST.get('email'),
	}
	
	return render(request, 'foodtracker/account.html', context)

# Update person
def changePersonPageView(request) :

	return render(request, "foodtracker/editPerson.html")


def updatePersonPageView(request) :
	if request.method == 'POST':

	#Create a new employee object from the Employee model
		person = Person.objects.GET['email']

	#grab the data from the form and store it to the new object
		newFirst = request.POST.get('firstName')
		newLast = request.POST.get('lastName')
		newAge = request.POST.get('age')
		newHeight = request.POST.get('height')
		newWeight = request.POST.get('weight')

		person.firstName = newFirst
		person.lastName = newLast
		person.age = newAge
		person.height = newHeight
		person.weight = newWeight

		person.save()

	return render(request, "foodtracker/index.html")

def deletePersonPageView(request) :
	if request.method == 'POST':

	#Create a new employee object from the Employee model
		person = Person.objects.filter(email=request.GET['email'])
		person.delete()

# Navigation and Basic Function of Food Add Page
def namesPageView(request) :
	
	# searchDcid = request.POST.get('dcid')
	# findDailyCons = DailyConsumed.objects.get(dcid=searchDcid)
	
	global current_dc
	this_dc = DailyConsumed.objects.get(email=request.POST.get('email'))
	current_dc = this_dc
	print(str(current_dc.dcid) + "test")

	global current_person
	thisPerson = Person.objects.get(email=request.POST.get('email'))
	current_person = thisPerson
	foods = FoodConsumed.objects.filter(dcid=current_dc)
	context = {
		'foods' : foods,
		'current_dc': this_dc,
		'current_person': current_person
	}
	return render(request, "foodtracker/names.html", context)


# def new(request):
#     return render(request = request, template_name = 'foodtracker/new.html')




# def login_request(request):
# 	if request.method == "POST":
# 		form = AuthenticationForm(request, data=request.POST)
# 		if form.is_valid():
# 			username = form.cleaned_data.get('username')
# 			password = form.cleaned_data.get('password')
# 			user = authenticate(username=username, password=password)
# 			if user is not None:
# 				login(request, user)
# 				messages.info(request, f"You are now logged in as {username}.")
# 				return redirect("foodtracker:index")
# 			else:
# 				messages.error(request,"Invalid username or password.")
# 		else:
# 			messages.error(request,"Invalid username or password.")
# 	form = AuthenticationForm()
# 	return render(request=request, template_name="foodtracker/new.html", context={"new_form":form})

# Create New Food
def storeFoodPageView(request) :

	if request.method == 'POST':

	#Create a new employee object from the Employee model
		new_food = Food()

	#grab the data from the form and store it to the new object
		food_name = request.POST.get('food_name')
		new_food.food_K = request.POST.get('food_K')
		new_food.food_phos = request.POST.get('food_phos')
		new_food.food_protein = request.POST.get('food_protein')
		new_food.food_water = request.POST.get('food_water')
		new_food.food_na = request.POST.get('food_na')
		new_food.food_name = food_name

		quantity = request.POST.get('quantity')
		#daily_consumed = DailyConsumed.objects.get(email_id=person.email, date=date.today())

		global current_person
		current_person = Person.objects.get(email=request.POST.get('4email'))
		
		global current_dc
		current_dc = DailyConsumed.objects.get(dcid=request.POST.get('4dcid'))
		# tryDcid = current_dc.dcid

		foods = FoodConsumed.objects.filter(dcid=current_dc)

		if (len(food_name) > 30) :
			new_food.food_name = food_name[0:29]
		new_food.save()

	foods = FoodConsumed.objects.filter(dcid=request.POST.get('4dcid'))
		
	context = {
		'foods': foods,
		"new_food" : new_food,
		"current_dc" : current_dc,
		'foods': foods,
		"current_person": current_person,
		"quantity": quantity,
	}

	if 'more' in request.POST:
		return render(request, "foodtracker/names.html", context)
	else:
		return render(request, "foodtracker/addedFood.html", context)

def saveConsumedFood(request) :
	newFoodConsumed = FoodConsumed()

	global current_dc
	current_dc = DailyConsumed.objects.get(dcid=request.POST.get('dcid'))
	newFoodConsumed.dcid_id = current_dc.dcid
	
	global current_person
	current_person = Person.objects.get(email=request.POST.get('email'))

	current_food = Food.objects.get(food_name=request.POST.get('food_name'))
	newFoodConsumed.food_name_id = current_food.food_name

	quantity = request.POST.get('quantity')
	newFoodConsumed.quantity = quantity
	newFoodConsumed.save()
	quantity = Decimal(quantity)

	# Update Current DC with added foods and their quantites
	k = (current_food.food_K * quantity) + (current_dc.total_k)
	if k > 9999.99 :
		k = 9999.99
	na = (current_food.food_na * quantity) + (current_dc.total_na)
	if na > 9999.99 :
		na = 9999.99
	phos = (current_food.food_phos * quantity) + (current_dc.total_phos)
	if phos > 9999.99 :
		phos = 9999.99
	protein = (current_food.food_protein * quantity) + (current_dc.total_protein)
	if protein > 9999.99 :
		protein = 9999.99
	water = (current_food.food_water * quantity) + (current_dc.total_water)
	if water > 9999.99 :
		water = 9999.99

	current_dc.total_k = k
	current_dc.total_na = na
	current_dc.total_phos = phos
	current_dc.total_protein = protein
	current_dc.total_water = water
	current_dc.save()
	foods = FoodConsumed.objects.filter(dcid=request.POST.get('dcid'))
	
	# food_name = request.POST.get('food_name')
	context = {
		'foods' : foods,
		"foodConsumed": newFoodConsumed,
		"current_dc": current_dc, 
		"current_person": current_person
	}
	if 'more' in request.POST:
		return render(request, "foodtracker/names.html", context)
	else:
		return render(request, "foodtracker/index.html", context)
# THIS IS NOT BEING USED, ATTEMPTING TO DO IT IN THE SAVE FOOD FUNCTION
def createFoodConsumed(new_food, quantity):
	newFoodConsumed = FoodConsumed()
	
	newFoodConsumed.dcid = current_dc.dcid
	newFoodConsumed.food_name = new_food.food_name
	newFoodConsumed.quantity = quantity
	
	return(newFoodConsumed)

# Create new FoodConsumed Object and associations
def newFoodConsumed(request):
	consumed = FoodConsumed.objects.get(food_name=request.POST.get('foodName'), dcid=request.POST.get('dcid'))
	
	dcid = request.POST.get('dcid')
	foodName = request.POST.get('foodName')
	quantity = request.POST.get('quantity')
	
	consumed.quantity = quantity

	consumed.save()
	foods = FoodConsumed.objects.filter(dcid=request.POST.get('dcid'))
	global current_person
	current_person = Person.objects.get(email=request.POST.get('email'))
	current_dc = DailyConsumed.objects.get(dcid=request.POST.get('dcid'))
	context= { 
		'foods': foods,
		'current_dc' : current_dc,
		'foodName' : foodName,
		'quantity' : quantity,
		"current_person" : current_person
	}

	current_dc = DailyConsumed.objects.get(dcid=request.POST.get('dcid'))
	calcDCValues(current_dc)
	
	return render(request, "foodtracker/names.html", context)

# Update quantity of foods
def updateFoodConsumed(request):

	
	tryName = Food.objects.get(food_name=request.POST.get('2fname'))
	current_dc = DailyConsumed.objects.get(dcid=request.POST.get('2dcid'))

	global current_person
	current_person = Person.objects.get(email=request.POST.get('2email'))
	
	#dcid = request.POST.get('dcid')
	#foodName = request.POST.get('food')
	quantity = request.POST.get('quantity')

	context= {
		'dcid' : current_dc,
		'foodName' : tryName,
		'quantity' : quantity,
		"current_person" : current_person,
		"current_dc": current_dc
	}
	
	return render(request, "foodtracker/updateFood.html", context)

# Delete the selected Food
def deleteFoodConsumed(request):

	tryDcid = request.POST.get('dcid')
	tryName = request.POST.get('fName')
	tryEmail = request.POST.get('email')
	
	foodConsumed = FoodConsumed.objects.get(food_name=tryName, dcid= tryDcid)
	foods = FoodConsumed.objects.filter(dcid= tryDcid)

	foodConsumed.delete()
	# food.delete()

	
	
	current_dc = DailyConsumed.objects.get(dcid=tryDcid)
	current_person = Person.objects.get(email=tryEmail)
	
	context = {
		'foods' : foods,
		"current_person" : current_person,
		"current_dc": current_dc
	}

	calcDCValues(current_dc)

	return render(request, "foodtracker/names.html", context)
	
# Update Foods
def UpdateFoodView(request) :

	if request.method == 'POST':

	#Create a new employee object from the Employee model
		food = Food.objects.GET['food_name']

	#grab the data from the form and store it to the new object
		food_name = request.POST.get('food_name')
		newK = request.POST.get('food_K')
		newPhos = request.POST.get('food_phos')
		newProtein = request.POST.get('food_protein')
		newWater = request.POST.get('food_water')
		newNa = request.POST.get('food_na')
		foods = FoodConsumed.objects.filter(dcid=current_dc)
		tryDcid = request.POST.get('dcid')
		# DailyConsumed = DailyConsumed.objects.get(dcid=tryDcid)  -- This should be executed in a separate function to ensure the new food is
		# created before you create the foodConsumed object that contains the daily consumeddiet and the food item

		if (len(food_name) > 30) :
			food_name = food_name[0:29]
			
		food.food_name = food_name
		food.food_K = newK
		food.food_newPhos = newPhos
		food.food_protein = newProtein
		food.food_water = newWater
		food.food_na = newNa

	food.save()
	context =  {
		'foods' : foods
	}
	return render(request, "foodtracker/names.html", context)

# Navigation to History page
def historyPageView(request) :
	context = {
		"current_person" : Person.objects.get(email=request.POST.get('email')),
		"current_dc" : DailyConsumed.objects.get(dcid=request.POST.get('dcid')),
	}
	return render(request, 'foodtracker/history.html', context)

# API Call to get all foods associated with an entered value
def FDC_API_Name(request):
	foodName = request.POST.get('foodName')
	url = f'https://api.nal.usda.gov/fdc/v1/foods/search?query={foodName}&dataType=Foundation&sortBy=dataType.keyword&api_key=hau66Auej9ComnzHEm2xLrHvyelPig3ORzx3jqry'
	j = requests.get(url).json()
	l = []
	ids = []
	class Item :	
		def __init__(self, name, id):
			self.name = name
			self.id = id	
	
	listItem = []

	for food in j['foods']:
		# if j['foods'] not in listItem:
		x = Item(food['description'], food['fdcId'])
		listItem.append(x)

			#l.append(food['description'])
			#ids.append(food['fdcId'])
	if len(listItem) == 0:
		url = f'https://api.nal.usda.gov/fdc/v1/foods/search?query={foodName}&dataType=Survey%20%28FNDDS%29&sortBy=dataType.keyword&api_key=hau66Auej9ComnzHEm2xLrHvyelPig3ORzx3jqry'
		j = requests.get(url).json()
		for food in j['foods']:
			#if j['foods'] not in l:
			x = Item(food['description'], food['fdcId'])
			listItem.append(x)				
				# l.append(food['description'])
				# ids.append(food['fdcId'])
		if len(listItem) == 0:
			url = f'https://api.nal.usda.gov/fdc/v1/foods/search?query={foodName}&dataType=Branded&sortBy=dataType.keyword&api_key=hau66Auej9ComnzHEm2xLrHvyelPig3ORzx3jqry'
			j = requests.get(url).json()
			for food in j['foods']:
				x = Item(food['description'], food['fdcId'])
				listItem.append(x)
				# l.append(food['description'])
				# ids.append(food['fdcId'])	

	global current_dc
	current_dc = DailyConsumed.objects.get(dcid=request.POST.get('3dcid'))
	global current_person
	current_person = Person.objects.get(email=request.POST.get('3email'))
	
	foods = FoodConsumed.objects.filter(dcid=current_dc)	

	if len(listItem) == 0 :
		context = {
		'listItem' : listItem,
		'send': True,
		'message': 'Food not found, enter info manually below',
		'current_person': current_person,
		'foods' : foods,
		'current_dc': current_dc
		}
		
	else :
		context = {
		'send': False,
		'listItem' : listItem,
		'current_person': current_person,
		'foods' : foods,
		'current_dc': current_dc
		}
	#listItem = []

	# for i in l :
	# 	food = Item(l[i], ids[i])
	# 	listItem.append(food)

	
		# make each id a dummy object, then have an attribute of food name
	return render(request, "foodtracker/names.html", context)

# API Call with foodID to get nutrients
def FDC_API_Nutrients(request):
	foodID = request.POST.get('food')
	url = f'https://api.nal.usda.gov/fdc/v1/foods/search?query={foodID}&dataType=&sortBy=dataType.keyword&sortOrder=asc&api_key=hau66Auej9ComnzHEm2xLrHvyelPig3ORzx3jqry'
	j = requests.get(url).json()
	
	food_name = j['foods'][0]['description']
	phos = 0
	k = 0
	water = 0
	protein = 0
	na = 0
	for nutrient in j['foods'][0]['foodNutrients']:
		
		if nutrient['nutrientName'] == 'Phosphorus, P':
			phos = round(nutrient['value'],2 )
				
		elif nutrient['nutrientName'] == 'Potassium, K':
			k = round(nutrient['value'], 2)

		elif nutrient['nutrientName'] == 'Water':
			water = round(nutrient['value'], 2)

		elif nutrient['nutrientName'] == 'Protein':
			protein = round(nutrient['value'],2 )
	
		elif nutrient['nutrientName'] == 'Sodium, Na':
			na = round(nutrient['value'],2 )

	# foods = FoodConsumed.objects.get(dcid=current_dc)
	# food_name = food['description']

	current_person = Person.objects.get(email=request.POST.get('email'))
	current_dc = DailyConsumed.objects.get(email=request.POST.get('email'))
	foods = FoodConsumed.objects.filter(dcid=current_dc)
	
	context = {
		'phos' : phos,
		'k' : k,
		'water' : water,
		'protein' : protein,
		'na' : na,
		'food_name' :  food_name,
		'foods': foods,
		'current_person': current_person,
		'current_dc': current_dc
	}
	return render(request, "foodtracker/names.html", context)

# Update Selected Mood from Index Page
def updateMood(request) :
	current_dc = DailyConsumed.objects.get(dcid = request.POST.get('dcid'))
	faces = request.POST.get('faces')
	current_dc.mentalHealthRating = faces
	current_dc.save()
	newPerson = Person.objects.get(email=request.POST.get('email'))
	#DailyConsumed.objects.get(dcid=request.POST.get('dcid')),
	
	context = {
		"current_person" : newPerson,
		"current_dc" : current_dc
	}
	return render(request, "foodtracker/index.html", context)

# Update BG, SDP, and DBP from Index Page
def updateMeasurement(request):
	current_dc = DailyConsumed.objects.get(dcid = request.POST.get('m-dcid'))
	bg = request.POST.get('blood_glucose')
	sbp = request.POST.get('d-systolic')
	dbp = request.POST.get('d-diastolic')
	current_dc.blood_glucose = bg
	current_dc.systolic_bp = sbp
	current_dc.diastolic_bp = dbp
	current_dc.save()
	context = {
		"current_person" : Person.objects.get(email=request.POST.get('email')),
		"current_dc" : DailyConsumed.objects.get(dcid=request.POST.get('dcid')),
	}
	return render(request, "foodtracker/index.html", context)

# Update Values of DailyConsumed Object to match the current foods connect
def calcDCValues(current_dc) :
	FoodConsumeds = FoodConsumed.objects.filter(dcid_id = current_dc.dcid)
	total_k = 0
	total_na = 0
	total_phos = 0
	total_protein = 0
	total_water = 0


	for fc in FoodConsumeds :
		food = Food.objects.get(food_name = fc.food_name)
		quantity = fc.quantity
		total_k = (food.food_K * quantity) + (total_k)
		if total_k > 9999.99 :
			total_k = 9999.99
		total_na = (food.food_na * quantity) + (total_na)
		if total_na > 9999.99 :
			total_na = 9999.99
		total_phos = (food.food_phos * quantity) + (total_phos)
		if total_phos > 9999.99 :
			total_phos = 9999.99
		total_protein = (food.food_protein * quantity) + (total_protein)
		if total_protein > 9999.99 :
			total_protein = 9999.99
		total_water = (food.food_water * quantity) + (total_water)
		if total_water > 9999.99 :
			total_water = 9999.99
	
	current_dc.total_k = total_k
	current_dc.total_na = total_na
	current_dc.total_phos = total_phos
	current_dc.total_protein = total_protein
	current_dc.total_water = total_water
	current_dc.save()