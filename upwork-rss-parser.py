import requests
from bs4 import BeautifulSoup
import lxml 
import time
import ssl
import smtplib
import email.message


#Keywords to search for (EDIT ME)
KEYWORDS = ["website", "wordpress", "react", "javascript", "landing", "elementor"]

#Minimum client budget to search for in dollars (EDIT ME)
MINIMUM_BUDGET = 250

#RSS URL for Upwork (EDIT ME)
RSS_URL = "https://www.upwork.com"

#Email address to send results to (EDIT ME)
TO_EMAIL = "email@email.com"

#Gmail address to send emails with (EDIT ME)
FROM_EMAIL = "email@gmail.com" 

#Time to sleep between RSS HTTP GET requests. (EDIT ME)
SLEEP_TIME = 250 

#Script will prompt you for your Gmail password
FROM_EMAIL_PASSWORD = input("Please input your Gmail password:")

#Array to keep track of previously emailed results
previous_results = []



def send_email(sender, password, to, message):
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP("smtp.gmail.com", "587") as server:
            server.ehlo() 
            server.starttls(context=context)
            server.ehlo()  
            server.login(sender, password)
            server.sendmail(sender, to, message)
    except Exception as e:
        print("[!] Error sending email!")
        print(str(e))


def email_results(emailArray):
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
    for result in emailArray:
        message_payload = message_payload + "\r\n".join(result) + "\r\n"
    msg.set_payload(message_payload)
    print(msg)
    send_email(
        sender = FROM_EMAIL,
        password = FROM_EMAIL_PASSWORD,
        to=TO_EMAIL,
        message=msg.as_string())


def is_above_minimum_budget(budgetString):
    global MINIMUM_BUDGET
    budgetString = budgetString[budgetString.find("</b>: $")+6::]
    budgetString = budgetString[0:budgetString.find("<br")].strip()
    budgetString = budgetString.replace(',', '')
    budgetString = budgetString.replace('$', '')
    return [int(budgetString) > MINIMUM_BUDGET,budgetString]


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
    emailOutput = []
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
            minBudget = is_above_minimum_budget(str(res.find("description").text))
            if minBudget[0]:
                keywordResults = title_or_description_contains_keywords(str(res.find("title").text), str(res.find("description").text))
                if keywordResults:
                    if not (str(res.find("title").text) + str(res.find("pubDate").text)) in previous_results:
                        previous_results.append(str(res.find("title").text) + str(res.find("pubDate").text))
                        emailData = []
                        emailData.append(" Title: " + str(res.find("title").text))
                        emailData.append(" Keywords Detected: " + ",".join(str(x) for x in keywordResults))
                        emailData.append(" Client budget: " + minBudget[1])
                        emailData.append(" URI: " + str(res.find("link").text))
                        emailData.append(" Date published: " + str(res.find("pubDate").text))
                        emailData.append("\r\n")
                        emailOutput.append(emailData)
        if emailOutput:
            email_results(emailOutput)


while True:
    request_upwork_rss()
    time.sleep(SLEEP_TIME)

