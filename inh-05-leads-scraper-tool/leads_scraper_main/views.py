from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView

# base route
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
        hourly = request.POST['hourly']
        budget = request.POST['budget']
        email = request.POST['email']

        # debug
        print(keywords + email + hourly + budget)

        # update database
        id = 1
        # custom_requirements = CustomRequirements.objects.update(request.POST, instance = requirements)
        requirements = CustomRequirements.objects.get(id=id)
        custom_requirements = CustomRequirements.objects.update(hourly_rate=hourly, budget=budget,
                                                                to_email=email, instance=requirements)
        custom_requirements.save()
        print('requirements created')

        # run main script again to update status
        return redirect('leads_scraper_main/home.html')
    #
    return render(request, 'leads_scraper_main/custom.html')
