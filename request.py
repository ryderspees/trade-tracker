import requests
import json
from datetime import datetime, timedelta

# This function will grab the data from house/senate stockwatcher and return an array
# of dictonary items that represent transactions

def fetch_data():
  response = requests.get("https://senate-stock-watcher-data.s3-us-west-2.amazonaws.com/aggregate/all_transactions.json")
  
  if response.status_code != 200:
    print("request failed.")
    return False

  data = response.json()
  data.sort(key = lambda x: datetime.strptime(x['disclosure_date'], '%m/%d/%Y'), reverse=False)
  return data


# good formatting for the data if a print is needed
"""for trade in data:
  disclosed_date = datetime.strptime(trade['disclosure_date'], "%m/%d/%Y")
  if disclosed_date > past:
    if (trade['ticker'] != '--'):
      print('Disclosure Date: ' + trade['disclosure_date'])
      print('Transaction Date: ' + trade['transaction_date'])
      print('Name: ' + trade['senator'])
      print('Stock Ticker: ' + trade['ticker'])
      print('Transaction Type: ' + trade['type'])
      print('Amount: ' + trade['amount'])
      print()"""



