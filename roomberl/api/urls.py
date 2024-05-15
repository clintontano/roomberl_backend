from django.urls import path, include

app_name = 'api'

urlpatterns = [
    path('literals/', include('literals.urls')),
    path("accounts/", include("account.urls")),

]
