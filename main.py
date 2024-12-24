import requests
import json

url = "https://www.swiggy.com/dapi/order/all?order_id="

cookiesValue = ""
with open('cookies', 'r') as cookiesFile:
  cookiesValue = cookiesFile.read()

if (cookiesValue == ""):
  print('missing some cookies')
  exit(1)
  
payload={}
headers = {
  '__fetch_req__': 'true',
  'accept': '*/*',
  'accept-language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
  'content-type': 'application/json',
  'cookie': cookiesValue,
  'if-none-match': 'W/"235cb-dIjl6JiUo+ZiNS3Ve213//T/peY"',
  'priority': 'u=1, i',
  'referer': 'https://www.swiggy.com/my-account',
  'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"macOS"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-origin',
  'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
}

response = requests.request("GET", url, headers=headers, data=payload).json()

print(response['data']['total_orders'])
