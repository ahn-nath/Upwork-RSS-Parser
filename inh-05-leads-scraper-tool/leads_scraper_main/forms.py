from django import forms

from leads_scraper_main.models import CustomRequirements


class CustomRequirementsForm(forms.ModelForm):
    # create meta class
    class Meta:
        # specify model to be used
        model = CustomRequirements

        # specify fields to be used
        fields = "__all__"  
