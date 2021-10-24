# Upwork RSS Parser
> This Python3 script will monitor Upwork RSS feed and then email you the results. 
> 

## Table of Contents
* [General Info](#general-information)
* [Technologies Used](#technologies-used)
* [Features](#features)
* [Screenshots](#screenshots)
* [Setup](#setup)
* [Project Status](#project-status)
* [Acknowledgements](#acknowledgements)
* [Contact](#contact)

## General Information
This Python3 script will monitor Upwork RSS feed, filter out listings based on client budget/keywords, and then email you the results. 

## Technologies Used
- Python3
- requests
- bs4 (BeautifulSoup)
- lxml
- ssl
- smtplib
- email.message

## Features
- Parses Upwork RSS feed every N seconds
- Filters out listings that don't meet the desired minimum budget
- Filters out listings that don't contain at least one specific keyword
- Emails you the results (if there are any)

## Screenshots
![screenshot](https://user-images.githubusercontent.com/86444599/138576620-52be4111-3817-41c9-9ab6-ef947f60bfcc.png)


## Setup
download/clone repo

Login to Upwork, navigate to the job search page within the category of your choice. In my case it was "Web, Mobile, & Software Development". Make sure the results are sorted by "newest". Then click on the icon that looks like a green wifi logo. Right click on RSS, then copy the URL. 

![upwork](https://user-images.githubusercontent.com/86444599/138576891-249e1d2f-66bb-4e10-aa22-e4450bc38f34.png)

If you want email sending capabilities, first create a new Gmail account. Then go into the account settings and enable "less secure apps". 

After creating your email account for sending emails, open upwork-rss-parser.py and edit the following values:

KEYWORDS = ["website", "wordpress", "react", "javascript", "landing", "elementor"] #keywords to look for in title/description

MINIMUM_BUDGET = 250 #Minimum budget to search for in dollars

RSS_URL = "https://www.upwork.com" #Upwork RSS URL that you gathered earlier

TO_EMAIL = "email@email.com" #Email address that you want to receive the notifications on 

FROM_EMAIL = "email@gmail.com" #Email address that you created on Gmail with less secure apps enabled

SLEEP_TIME = 250 #Time to sleep between Upwork RSS HTTP GET requests


run `pip3 install -r requirements.txt` in project root directory

run `python3 upwork-rss-parser.py` in project root directory

## Project Status
_in progress_

## TODO
- Resend email on failure
- More RSS feeds?
- ...

## Acknowledgements
- Many thanks to Sergii, Chris, Swapna, Aras, Brock, Ibrahim, Ali, Sandra, Abhishek, my cat, Mozart, Monster Energy

## Contact
Created by Chris☕ [@chrmc](https://mc-chris.me) - feel free to contact me!
