# leads_scraper_main/urls.py


from django.urls import path
from . import views

urlpatterns = [
    # route path
    path('', views.home, name='home'),

    # signup
    path('signup/', views.SignUp.as_view(), name='signup'),

    # set custom requirements
    path('custom', views.custom, name='custom')
]
