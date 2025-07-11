import requests
from telegram import Bot

TELEGRAM_TOKEN = "7482502436:AAFsDURMgBZgBjpiy4Xd_4W60xL4iiz1RMk"
TELEGRAM_CHAT_ID = "7094440452"

def fetch_latest_pelosi_trade():
    url = "https://api.capitoltrades.com/graphql"
    headers = {
        "Content-Type": "application/json",
        "Origin": "https://www.capitoltrades.com",
        "Referer": "https://www.capitoltrades.com/",
        "User-Agent": "Mozilla/5.0"
    }

    query = {
        "operationName": "tradesSearch",
        "variables": {
            "limit": 1,
            "offset": 0,
            "filters": {
                "politicianSlugs": ["nancy-pelosi"]
            }
        },
        "query": """query tradesSearch($limit: Int!, $offset: Int!, $filters: TradeFilters) {
              trades(limit: $limit, offset: $offset, filters: $filters) {
                id
                transactionDate
                disclosureDate
                amount
                assetName
                type
                ticker
                party
                politician {
                  firstName
                  lastName
                }
              }
            }"""
    }

    try:
        response = requests.post(url, headers=headers, json=query, timeout=10)
        response.raise_for_status()
        trade = response.json()["data"]["trades"][0]

        summary = (
            f"👤 {trade['politician']['firstName']} {trade['politician']['lastName']}\n"
            f"🏛️ Party: {trade['party']}\n"
            f"💼 {trade['type'].capitalize()} {trade['ticker']} ({trade['assetName']})\n"
            f"💰 Amount: {trade['amount']}\n"
            f"📅 Traded: {trade['transactionDate']} | Filed: {trade['disclosureDate']}"
        )
        return summary

    except Exception as e:
        return f"❌ Error fetching trade: {e}"

def send_telegram_alert(message):
    bot = Bot(token=TELEGRAM_TOKEN)
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)

def main():
    trade_info = fetch_latest_pelosi_trade()
    send_telegram_alert(trade_info)

if __name__ == "__main__":
    main()
