from django.apps import AppConfig
from leads_scraper_main.utils.parser import main_scrape_results


class LeadsScraperMainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'leads_scraper_main'
    verbose_name = "Upwork Leads Scraper Application"

    # startup code here
    def ready(self):
        print('## STARTING PROJECT ##')
        main_scrape_results()
