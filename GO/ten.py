from concurrent.futures import as_completed, ThreadPoolExecutor
import requests_futures.sessions
import requests_futures
from dotenv import load_dotenv
import os

load_dotenv()
id = os.getenv("ID")
security_id = os.getenv("SECURITY_ID")
price = os.getenv("PER10")
cookie = os.getenv("COOKIE")
token=os.getenv("TOKEN")
session_id = os.getenv("SESSION")
request_owner = os.getenv("REQUEST_OWNER")
tms = os.getenv("TMS")
symbol=os.getenv("SYMBOL")
client_id=os.getenv("CLIENT_ID")
member_code=os.getenv("MEMBER_CODE")
client_code=os.getenv("CLIENT_CODE")
url="https://tms" + tms + ".nepsetms.com.np/tmsapi/orderApi/order/"
qty = 500


headers = {
    'Cookie': cookie,
    'X-XSRF-TOKEN': token,
    'host-session-id':security_id,
    'request-owner': request_owner,
    'host':"tms" + tms + ".nepsetms.com.np",
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'Content-Type': 'application/json',
    'Accept': 'application/json, text/plain, */*',
}


pload = {
    "orderBook": {
        "orderBookExtensions": [
            {
                "orderTypes": {
                    "id": 1,
                    "orderTypeCode": "LMT"
                },
                "disclosedQuantity": 0,
                "orderValidity": {
                    "id": 1,
                    "orderValidityCode": "DAY"
                },
                "triggerPrice": 0,
                "orderPrice": {price},
                "orderQuantity": {qty},
                "remainingOrderQuantity": 10,
                "marketType": {
                    "id": 2,
                    "marketType": "Continuous"
                }
            }
        ],
        "exchange": {
            "id": 1
        },
        "dnaConnection": {},
        "dealer": {},
        "member": {},
        "productType": {
            "id": 1,
            "productCode": "CNC"
        },
        "instrumentType": {
            "id": 1,
            "code": "EQ"
        },
        "client": {
            "activeStatus": "A",
            "id": {client_id},
            "accountType": "CLI",
            "allowedToTrade": "Y",
            "clientMemberCode": {member_code},
            "clientOrDealer": "C",
            "notsUniqueClientCode": {client_code},
            "clientGroup": {
                "activeStatus": "A",
                "id": 101
            },
            "memberBranch": {
                "activeStatus": "A",
                "id": 2
            },

            "shortSellMode": 0,
            "onlineOrOffline": 1,
            "panNumber": "Pan",
            "collateralCalculationMode": 1,
        },
        "security": {
            "id": {id},
            "exchangeSecurityId": {security_id},
            "marketProtectionPercentage": 0,
            "divisor": 100,
            "boardLotQuantity": 1,
            "tickSize": 0.1
        },
        "accountType": 1,
        "cpMemberId": 0,
        "buyOrSell": 1
    },
    "orderPlacedBy": 2,
    "exchangeOrderId": None
}

# .replace("{price}",str(price)).replace("{qty}",str(qty)).replace("{security_id}",str(security_id)).replace("{id}",str(id))
max_order=5
success_count=0
with requests_futures.sessions.FuturesSession(executor=ThreadPoolExecutor(max_workers=8)) as session:
    print(f"Placing order for {symbol} at {qty} @ {price}")
    while max_order> success_count:
        futures = [session.post(url, headers=headers, json=pload) for _ in range(int(5))]
        for future in as_completed(futures):
            try:
                response = future.result()
                if response.status_code == 200 and response.status_code==201:
                    success_count=success_count+1
                    print(f"{success_count}/{max_order} order placed!")
            except Exception as e:
                pass
    print("done!")