from django.apps import AppConfig


class LeadsScraperMainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'leads_scraper_main'
    verbose_name = "Upwork Leads Scraper Application"

    # startup code here
    def ready(self):
        #pass
        print('## TESTING PROJECT ##')

