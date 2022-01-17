import email.message
import smtplib
import ssl
import time

import requests
from bs4 import BeautifulSoup

# Keywords to search for (EDIT THIS, SEE README)
KEYWORDS = ["website", "wordpress", "react", "javascript", "landing", "elementor"]

# Minimum client budget to search for in dollars (EDIT THIS, SEE README)
MINIMUM_BUDGET = 0

MINIMUM_FIXED_PRICE = 250

MINIMUM_HOURLY_RATE = 10

# RSS URL for Upwork (EDIT THIS, SEE README)
RSS_URL = "https://www.upwork.com"

# Email address to send results to (EDIT THIS, SEE README)
TO_EMAIL = "email@test.com"

# Gmail address to send emails with (EDIT THIS, SEE README)
FROM_EMAIL = "email@test.com"

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
    msg['To'] = TO_EMAIL
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
    is_there_any_budget = (budget_string.find("</b>: $") > 0) #

    # extract fixed price/hourly rate from string
    budget_string = budget_string[budget_string.find("</b>: $") + 6::]
    budget_string = budget_string[0:budget_string.find("<br")].strip()
    budget_string = budget_string.replace(',', '')
    budget_string = budget_string.replace('$', '').split("-")

    # if there is a budget, convert value from string representation of a number to integer, otherwise, set to 0
    final_value = int(float(budget_string[len(budget_string)-1])) if is_there_any_budget else 0
    # set MINIMUM_BUDGET to MINIMUM HOURLY RATE if it is an hourly contract, otherwise set to MINIMUM_FIXED_PRICE
    MINIMUM_BUDGET = MINIMUM_HOURLY_RATE if (len(budget_string) > 1) else MINIMUM_FIXED_PRICE

    # check against min budget and min hourly rate depending on each case
    return [final_value > MINIMUM_BUDGET, budget_string[0]]


def title_or_description_contains_keywords(title, description):
    global KEYWORDS
    results = []
    for keyword in KEYWORDS:
        if keyword in title.lower() or keyword in description.lower():
            results.append(keyword)
    return results


def request_upwork_rss():
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
                if keyword_results:
                    if not (str(res.find("title").text) + str(res.find("pubDate").text)) in previous_results:
                        previous_results.append(str(res.find("title").text) + str(res.find("pubDate").text))
                        email_data = [" Title: " + str(res.find("title").text),
                                      " Keywords Detected: " + ",".join(str(x) for x in keyword_results),
                                      " Client budget: " + min_budget[1], " URI: " + str(res.find("link").text),
                                      " Date published: " + str(res.find("pubDate").text), "\r\n"]
                        email_output.append(email_data)
        if email_output:
            email_results(email_output)


while True:
    request_upwork_rss()
    time.sleep(SLEEP_TIME)
