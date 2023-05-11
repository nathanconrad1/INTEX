from django.urls import path
from .views import storePersonPageView, updatePersonPageView, AccountPageView, logOutPageView
from .views import deletePersonPageView,  register_request, successPageView, login_request, radialPageView, updateFoodConsumed, saveConsumedFood, deleteFoodConsumed, newFoodConsumed
from .views import FDC_API_Name, FDC_API_Nutrients, index, storeFoodPageView, namesPageView, accountPageView, storeDailyConsumed, userPageView, historyPageView, updateMood, updateMeasurement

app_name = "foodtracker"   


urlpatterns = [
    path("login/", logOutPageView, name="logOut"),
    path("storePerson/", storePersonPageView, name="storePerson"),
    path("account/", AccountPageView, name="account"),
    path("updatePerson/", updatePersonPageView, name="updatePerson"),
    path("deletePerson/", deletePersonPageView, name="deletePerson"),
    # path("registerPerson/", registerPersonPageView, name="registerPerson"),
    path("", register_request, name="login_register"),
    path("login_request/", login_request, name="login_request"),
    path("index/", index, name="index"),
    path('success/', successPageView, name = 'success'),
    path('api_names/', FDC_API_Name, name='fdc_api_name'),
    path('api_result/', FDC_API_Nutrients, name= 'fdc_api_nutrients'),
    path('user/', userPageView, name= 'user'),
    path('storeDailyConsumed/', storeDailyConsumed, name = 'storeDailyConsumed'),
    path("name_foods/", namesPageView, name="nameFood"),
    path("storeFood/", storeFoodPageView, name="storeFood"),
    path("saveConsumed/", saveConsumedFood, name="saveConsumed"),
    path('account/', accountPageView, name = 'account'),
    path('radialtracker/', radialPageView, name = 'radialtracker'),
    path('history/', historyPageView, name = 'history'),
    path('delete/', deleteFoodConsumed , name = 'delete'),
    path('update/', updateFoodConsumed , name = 'update'),
    path('newConsumed/', newFoodConsumed , name = 'newConsumed'),
    path('updateMood/', updateMood, name = 'update_mood'),
    path('updateMeasurement/', updateMeasurement, name = 'updateMeasurement'),
    path('updateMeasurement/', updateMeasurement, name = 'updateMeasurement'),
]