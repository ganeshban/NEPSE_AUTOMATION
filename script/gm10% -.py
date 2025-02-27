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
qty =1000
price =442.1
security_id=3060
security_exchange_id=9246


headers = {
    'Cookie': cookie,
    'X-XSRF-TOKEN': xsrf_token,
    'host-session-id':host_session_id,
    'request-owner': '48920',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'Content-Type': 'application/json',
    'Accept': 'application/json, text/plain, */*',
}

pload = '''
{
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
            "id": 2155370,
            "accountType": "CLI",
            "allowedToTrade": "Y",
            "clientMemberCode": "20210304277",
            "clientOrDealer": "C",
            "contactNumber": "9857087455",
            "emailId": null,
            "notsUniqueClientCode": "202101181812704",
            "clientDealerType": null,
            "clientGroup": {
                "activeStatus": "A",
                "id": 101,
                "clientGroupCode": null,
                "clientGroupName": null
            },
            "memberBranch": {
                "activeStatus": "A",
                "id": 2,
                "branchLocation": null,
                "branchName": null,
                "hidden": null,
                "branchProvince": null,
                "branchDistrict": null,
                "branchMunicipality": null,
                "branchHead": null,
                "branchPhoneNumber": null
            },
            "clientDealerAddressDetails": null,
            "clientDealerBankDetail": null,
            "clientDealerIndividual": null,
            "clientDealerPerTradeLimits": null,
            "clientDealerProductMappings": null,
            "clientDealerOrderTypeMappings": null,
            "clientDealerTradingLimits": null,
            "clientDepositoryDetail": null,
            "corporateDetail": null,
            "corporateOwnershipDetails": null,
            "displayName": "Rupesh Babu Giri",
            "blockedDate": null,
            "remarks": null,
            "parentId": null,
            "recordType": null,
            "collateralByEntities": null,
            "shortSellMode": 0,
            "onlineOrOffline": 1,
            "panNumber": "113728389",
            "onlineFundTransfer": null,
            "collateralCalculationMode": 1,
            "isMarginLendingClient": null,
            "clientRiskType": null,
            "userAgreementChecked": null,
            "referredBy": null,
            "responseStatus": null,
            "kycUpload": false,
            "marginLendingClient": null
        },
        "security": {
            "id": {security_id},
            "exchangeSecurityId": {security_exchange_id},
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
    "exchangeOrderId": null
}
'''.replace("{price}",str(price)).replace("{qty}",str(qty)).replace("{security_exchange_id}",str(security_exchange_id)).replace("{security_id}",str(security_id))

with requests_futures.sessions.FuturesSession(executor=ThreadPoolExecutor(max_workers=8)) as session:
    while True:
        futures = [session.post(url, headers=headers, data=pload) for _ in range(int(50))]
        for future in as_completed(futures):
            try:
                response = future.result()
                if response.status_code == 200:
                    print(f"Request succeeded")
                elif response.status_code == 502:
                    pass
                else:
                    print(f"error: {response.text}")
            except Exception as e:
                pass

