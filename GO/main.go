package main

import (
	"bytes"
	"fmt"
	"io"
	"net/http"
	"os"
	"sync"

	"github.com/joho/godotenv"
)

func main() {
	err := godotenv.Load()
	if err != nil {
		fmt.Println("Error loading .env file")
		return
	}

	domain := os.Getenv("TMS")

	price := "416.7"
	qty := "10"
	security_id := "3059"
	security_exchange_id := "9246"

	data := `
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
                "orderPrice":` + price + ` ,
                "orderQuantity": ` + qty + `,
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
            "id": 2234482,
            "accountType": "CLI",
            "allowedToTrade": "Y",
            "clientMemberCode": "20231252966",
            "clientOrDealer": "C",
            "contactNumber": "9847240018",
            "emailId": null,
            "notsUniqueClientCode": "202312293604532",
            "clientDealerType": null,
            "clientGroup": {
                "activeStatus": "A",
                "id": null,
                "clientGroupCode": null,
                "clientGroupName": null
            },
            "memberBranch": {
                "activeStatus": "A",
                "id": 4,
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
            "displayName": "KISHOR KUMAR GIRI",
            "blockedDate": null,
            "remarks": null,
            "parentId": null,
            "recordType": null,
            "collateralByEntities": null,
            "shortSellMode": 0,
            "onlineOrOffline": 1,
            "panNumber": null,
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
            "id": ` + security_id + `,
            "exchangeSecurityId": ` + security_exchange_id + `,
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
`

	if domain == "" {
		fmt.Println("Missing required environment variables (DOMAIN).")
		return
	}
	headers := getHeaders()
	url := "https://tms" + domain + ".nepsetms.com.np/tmsapi/orderApi/order/"

	fmt.Println("Placing ORDER !!!")

	var wg sync.WaitGroup

	for i := 0; i < 3; i++ {
		wg.Add(1) // Add one to the WaitGroup counter
		go sendRequest(&wg, url, data, headers)
	}

	wg.Wait()
}

func getHeaders() map[string]string {

	cookie := os.Getenv("COOKIE")
	token := os.Getenv("TOKEN")
	session := os.Getenv("SESSION")
	request_owner := os.Getenv("REQUEST_OWNER")

	headers := make(map[string]string)
	headers["Content-Type"] = "application/json"
	headers["accept"] = "application/json, text/plain, */*"
	headers["cookie"] = cookie
	headers["x-xsrf-token"] = token
	headers["host-session-id"] = session
	headers["request-owner"] = request_owner

	return headers
}

func sendRequest(wg *sync.WaitGroup, url string, data string, headers map[string]string) {
	defer wg.Done()

	// Create a new POST request with the provided URL, headers, and payload
	req, err := http.NewRequest("POST", url, bytes.NewBuffer([]byte(data)))
	if err != nil {
		fmt.Println("Error creating request:", err)
		return
	}

	// Add headers to the request
	for key, value := range headers {
		req.Header.Add(key, value)
	}
	fmt.Println("Request url is :", req.URL)
	fmt.Println("Request body is :", req.Body)
	fmt.Println("Request Header is :", req.Header)
	// Sending HTTP POST request
	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		fmt.Println("Error sending POST request:", err)
		return
	}
	defer resp.Body.Close()

	// Read the response body
	responseBody, err := io.ReadAll(resp.Body)
	if err != nil {
		fmt.Println("Error reading response body:", err)
		return
	}

	// Print out the status code of the response
	fmt.Printf("Received response with status code: %d\n", resp.StatusCode)

	// Print the response body (or you could log it or process it as needed)
	fmt.Println("Response Body:", string(responseBody))

}
