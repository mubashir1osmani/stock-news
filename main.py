from dotenv import load_dotenv
import os
import requests
from twilio.rest import Client

load_dotenv()

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API = os.getenv("STOCK_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")


#Get yesterday's closing stock price
stock_params = {
    "function":"TIME_SERIES_DAILY",
    "symbol" : STOCK_NAME,
    "apikey" : STOCK_API,
}

response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]
print(yesterday_closing_price)

# Get the day before yesterday's closing stock price
day_before = data_list[1]
day_before_closeprice = day_before["4. close"]
print("Day before yesterday closing price: ", day_before_closeprice)

#Find the positive difference between 1 and 2
diff = float(yesterday_closing_price) - float(day_before_closeprice)
print("Whats the difference? ", diff)


#Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.
percent = (diff/float(yesterday_closing_price)) * 100


#if the difference is greater than 0.3 prints news, just for testing
up_down = None
if diff > 0:
    up_down="🔺"
else: 
    up_down="🔻"

if abs(round(percent)) > 0.3:
    news_params = {
        "apiKey" : NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,
    }
    news_resp = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = (news_resp.json()["articles"])

#get three articles
three = articles[:3]
print(three)

formatted_three = [f"{STOCK_NAME}: {up_down}{percent}%\nHeadline: {articles['title']}. \nBrief: {articles['description']}" for articles in three]

#getting twilio
client = Client(account_sid, auth_token)

for article in formatted_three:
    message = client.messages.create(
        body=article,
        from_="+13369396773",
        to="+14379834240"
    )


"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

