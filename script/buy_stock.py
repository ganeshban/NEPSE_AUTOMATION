from concurrent.futures import as_completed, ThreadPoolExecutor
import requests_futures.sessions
import requests_futures
from dotenv import load_dotenv
import os

load_dotenv()

url = os.getenv("API_URL")
cookie = os.getenv('COOKIE')
host_session_id = os.getenv('HOST_SESSION_ID')
xsrf_token=os.getenv('X-XSRF-TOKEN')
buy_sale = os.getenv('BUY_SALE')
qty = os.getenv('QTY')
price = os.getenv('RATE')
security_id = os.getenv('SECURITY_ID')
security_exchange_id = os.getenv('SECURITY_EXCHANGE_ID')
number_of_request = os.getenv('NUMBER_OF_REQUEST')

# url = 'http://localhost:8080/data'
headers = {
    'Cookie': cookie,
    'X-XSRF-TOKEN': xsrf_token,
    'host-session-id':host_session_id,
    'request-owner': '48920',
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
                "orderPrice": price,
                "orderQuantity": qty,
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
            "id": 2155370,
            "accountType": "CLI",
            "allowedToTrade": "Y",
            "clientMemberCode": "20210304277",
            "clientOrDealer": "C",
            "contactNumber": "9857087455",
            "emailId": None,
            "notsUniqueClientCode": "202101181812704",
            "clientDealerType": None,
            "clientGroup": {
                "activeStatus": "A",
                "id": 101,
                "clientGroupCode": None,
                "clientGroupName": None
            },
            "memberBranch": {
                "activeStatus": "A",
                "id": 2,
                "branchLocation": None,
                "branchName": None,
                "hidden": None,
                "branchProvince": None,
                "branchDistrict": None,
                "branchMunicipality": None,
                "branchHead": None,
                "branchPhoneNumber": None
            },
            "clientDealerAddressDetails": None,
            "clientDealerBankDetail": None,
            "clientDealerIndividual": None,
            "clientDealerPerTradeLimits": None,
            "clientDealerProductMappings": None,
            "clientDealerOrderTypeMappings": None,
            "clientDealerTradingLimits": None,
            "clientDepositoryDetail": None,
            "corporateDetail": None,
            "corporateOwnershipDetails": None,
            "displayName": "Rupesh Babu Giri",
            "blockedDate": None,
            "remarks": None,
            "parentId": None,
            "recordType": None,
            "collateralByEntities": None,
            "shortSellMode": 0,
            "onlineOrOffline": 1,
            "panNumber": "113728389",
            "onlineFundTransfer": None,
            "collateralCalculationMode": 1,
            "isMarginLendingClient": None,
            "clientRiskType": None,
            "userAgreementChecked": None,
            "referredBy": None,
            "responseStatus": None,
            "kycUpload": False,
            "marginLendingClient": None
        },
        "security": {
            "id": security_id,
            "exchangeSecurityId": security_exchange_id,
            "marketProtectionPercentage": 0,
            "divisor": 100,
            "boardLotQuantity": 1,
            "tickSize": 0.1
        },
        "accountType": 1,
        "cpMemberId": 0,
        "buyOrSell": buy_sale
    },
    "orderPlacedBy": 2,
    "exchangeOrderId": None
}

with requests_futures.sessions.FuturesSession(executor=ThreadPoolExecutor(max_workers=8)) as session:
    futures = [session.post(url, headers=headers, data=pload) for _ in range(int(number_of_request))]
    for future in as_completed(futures):
        try:
            response = future.result()
            if response.status_code == 200:
                print(f"Request succeeded")
            else:
                print(f"error: {response.text}")
        except Exception as e:
            print(f"~ - {e}")

