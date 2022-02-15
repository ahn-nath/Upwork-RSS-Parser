from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView

# base route
from leads_scraper_main.forms import CustomRequirementsForm
from leads_scraper_main.models import CustomRequirements


def home(request):
    return render(request, "leads_scraper_main/home.html")


# route for registering a new user
class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


# route for registering new requirements
def custom(request):
    if request.method == 'POST':
        keywords = request.POST['keywords']
        hourly = request.POST['hourly_rate']
        budget = request.POST['budget']
        email = request.POST['to_email']

        request_val = {
            "keywords": "",
            "hourly_rate": 5,
            "budget": 196,
            "to_email": "nathaly12toledo@gmail.com"
        }

        # debug
        print(keywords + email + hourly + budget)
        print(request.POST)

        # update database
        id = 1
        # custom_requirements = CustomRequirements.objects.update(request.POST, instance = requirements)
        requirements = CustomRequirements.objects.get(id=id)
        custom_requirements = CustomRequirementsForm(request.POST, instance=requirements)

        if custom_requirements.is_valid():
            custom_requirements.save()
            print('requirements created')

        # run main script again to update status
        return redirect('/home')
    #
    return render(request, 'leads_scraper_main/custom.html')
