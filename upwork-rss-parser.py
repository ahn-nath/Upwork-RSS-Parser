import email.message
import smtplib
import ssl
import time

import requests
from bs4 import BeautifulSoup

'''
TODOS:

#1 comment/document methods

'''

# Keywords to search for (EDIT THIS, SEE README)
KEYWORDS = ["cms development", "wordpress", "webflow", "wix", "shopify", "squarespace", "weebly"]

# Keywords to avoid (EDIT THIS, SEE README)
KEYWORDS_TO_AVOID = ['javascript, php, c#, c, c++, java, scala, coldfusion, ruby, perl, python, javascript, erlang, '
                     'sql', 'golang', 'excel vba', 'kotlin', 'vb.net', 'swift']

TOOLS_LANGUAGES_TO_AVOID = ['asp.net', 'node.js', 'ruby on rails', 'django', 'laravel', 'cakephp', 'jquery', 'angular',
                            'angular 2', 'aurelia', 'backbone.js', 'ember', 'knockout.js', 'mercury.js', 'meteor.js',
                            'polymer', 'react', 'underscore', 'vue', 'react']

# The minimum budget variable for hourly contract and fixed prices
MINIMUM_BUDGET = 0

# Minimum client budget to search for in dollars (EDIT THIS, SEE README)
MINIMUM_FIXED_PRICE = 250

# Minimum client hourly rate to search for in dollars (EDIT THIS, SEE README)
MINIMUM_HOURLY_RATE = 10

# Desired project length/range  [-1: 'None', 0: 'Less than a month', 1: '1 to 3 months', 2: '3 to 6 months', 3: 'More than 6 months'](EDIT THIS, SEE README)
PROJECT_LENGTH = 1

# RSS URL for Upwork (EDIT THIS, SEE README)
RSS_URL = "https://www.upwork.com/ab/feed/jobs/rss?budget=250-&category2_uid=531770282580668418&duration_v3=month&hourly_rate=10-&sort=recency&job_type=hourly%2Cfixed&paging=0%3B10&api_params=1&q=&securityToken=be7695356ca18fd6ff8e879cbcbb27c9affa21fe3943861361f2c951400dbcecf97f8eeaaac7773024eca5f73194cb8d626b32818641d2eaa457d068c1c1e613&userUid=1216002150314332160&orgUid=1216002150331109377"

# Email address to send results to (EDIT THIS, SEE README)
TO_EMAIL = ["nathaly@karpidesign.com", "pavel@karpidesign.com"]

# Gmail address to send emails with (EDIT THIS, SEE README)
FROM_EMAIL = "nathaly.toledo.dev@gmail.com"

# Time to sleep between RSS HTTP GET requests. (EDIT THIS, SEE README)
SLEEP_TIME = 250

# Script will prompt you for your Gmail password
FROM_EMAIL_PASSWORD = input("Please input your Gmail password:")

# Array to keep track of previously emailed results
previous_results = []


def send_email(sender, password, to, message):
    try:
        context = ssl.create_default_context()

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(sender, password)
            server.sendmail(sender, to, message)

    except Exception as e:
        print("[!] Error sending email!")
        print(str(e))


def email_results(email_array):
    global TO_EMAIL
    global FROM_EMAIL
    global FROM_EMAIL_PASSWORD

    msg = email.message.Message()
    msg['From'] = FROM_EMAIL
    msg['To'] = str(TO_EMAIL)
    msg['Subject'] = "New Upwork Projects"
    msg.add_header('Content-Type', 'text')
    msg.set_payload("This is your message.")
    message_payload = ""
    for result in email_array:
        message_payload = message_payload + "\r\n".join(result) + "\r\n"
    msg.set_payload(message_payload)
    print(msg)
    send_email(
        sender=FROM_EMAIL,
        password=FROM_EMAIL_PASSWORD,
        to=TO_EMAIL,
        message=msg.as_string())


def is_above_minimum_budget(budget_string):
    global MINIMUM_BUDGET

    # check if there's any budget/hourly rate available
    is_there_any_budget = (budget_string.find("</b>: $") > 0)  #

    # extract fixed price/hourly rate from string
    budget_string = budget_string[budget_string.find("</b>: $") + 6::]
    budget_string = budget_string[0:budget_string.find("<br")].strip()
    budget_string = budget_string.replace(',', '')
    budget_string = budget_string.replace('$', '').split("-")

    # if there is a budget, convert value from string representation of a number to integer, otherwise, set to 0
    final_value = int(float(budget_string[len(budget_string) - 1])) if is_there_any_budget else 0
    # set MINIMUM_BUDGET to MINIMUM HOURLY RATE if it is an hourly contract, otherwise set to MINIMUM_FIXED_PRICE
    MINIMUM_BUDGET = MINIMUM_HOURLY_RATE if (len(budget_string) > 1) else MINIMUM_FIXED_PRICE
    string_concatenate = "${fvalue} {sign}".format(fvalue=budget_string[0],
                                                   sign='/h' if (len(budget_string) > 1) else '')

    # check against min budget and min hourly rate depending on each case
    return [final_value > MINIMUM_BUDGET, string_concatenate]


def title_or_description_contains_keywords(title, description):
    global KEYWORDS
    results = []
    for keyword in KEYWORDS:
        if keyword in title.lower() or keyword in description.lower():
            results.append(keyword)
    return results


def keywords_and_tools_not_present_title_or_description(title, description):
    global KEYWORDS_TO_AVOID
    global TOOLS_LANGUAGES_TO_AVOID

    words_to_avoid = list(KEYWORDS_TO_AVOID)
    words_to_avoid.extend(TOOLS_LANGUAGES_TO_AVOID)
    result = False

    for keyword in words_to_avoid:
        if keyword not in title.lower() or keyword in description.lower():
            result = True
    return result


def is_within_project_length(url):
    print("url to parse: ", url)
    pass


def request_upwork_rss():
    print('running a new request')

    global KEYWORDS
    global previous_results
    global RSS_URL
    email_output = []
    try:
        x = requests.get(RSS_URL)
    except Exception as e:
        print("[!] Connection error")
        print(str(e))
        return
    if str(x.status_code) == "200":
        soup = BeautifulSoup(x.content, features='xml')
        result = soup.find_all("item")

        for res in result:
            min_budget = is_above_minimum_budget(str(res.find("description").text))
            if min_budget[0]:
                keyword_results = title_or_description_contains_keywords(str(res.find("title").text),
                                                                         str(res.find("description").text))
                if keyword_results:  # or skills
                    are_keywords_in_post = keywords_and_tools_not_present_title_or_description(
                        str(res.find("title").text), str(res.find("description").text))
                    if are_keywords_in_post:
                        # is_within_project_length(str(res.find("link").text)) # testing only
                        if not (str(res.find("title").text) + str(res.find("pubDate").text)) in previous_results:
                            previous_results.append(str(res.find("title").text) + str(res.find("pubDate").text))
                            email_data = [" Title: " + str(res.find("title").text),
                                          " Keywords/Skills Detected: " + ",".join(str(x) for x in keyword_results),
                                          " Client budget: " + min_budget[1], " URI: " + str(res.find("link").text),
                                          " Date published: " + str(res.find("pubDate").text), "\r\n"]
                            email_output.append(email_data)
        if email_output:
            email_results(email_output)


while True:
    request_upwork_rss()
    time.sleep(SLEEP_TIME)
