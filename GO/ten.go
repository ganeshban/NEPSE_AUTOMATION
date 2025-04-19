package main

import (
	"bytes"
	"fmt"
	"net/http"
	"os"
	"strconv"
	"sync"
	"time"

	"github.com/joho/godotenv"
)

func main() {
	err := godotenv.Load()
	if err != nil {
		fmt.Println("Error loading .env file")
		return
	}

	domain := os.Getenv("TMS")

	price := os.Getenv("PER10")
	qty := "500"
	max_order := 5
	security_id := os.Getenv("ID")
	security_exchange_id := os.Getenv("SECURITY_ID")
	symbol := os.Getenv("SYMBOL")
	client_id := os.Getenv("CLIENT_ID")
	member_code := os.Getenv("MEMBER_CODE")
	client_code := os.Getenv("CLIENT_CODE")

	data := `{
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
            "id": ` + client_id + `,
            "accountType": "CLI",
            "allowedToTrade": "Y",
            "clientMemberCode": ` + member_code + `,
            "clientOrDealer": "C",
            "contactNumber": "PHONE",
            "emailId": null,
            "notsUniqueClientCode": ` + client_code + `,
            "clientDealerType": null,
            "clientGroup": {
                "activeStatus": "A",
                "id": null,
                "clientGroupCode": null,
                "clientGroupName": null
            },
            "memberBranch": {
                "activeStatus": "A",
                "id": 4
            },
            "displayName": "NAME",
            "shortSellMode": 0,
            "onlineOrOffline": 1,
            "collateralCalculationMode": 1
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
    "exchangeOrderId": null}
`

	if domain == "" {
		fmt.Println("Missing required environment variables (DOMAIN).")
		return
	}
	headers := getHeaders()
	url := "https://tms" + domain + ".nepsetms.com.np/tmsapi/orderApi/order/"

	fmt.Println("Placing order for " + symbol + " at " + qty + " @ " + price)

	var wg sync.WaitGroup
	var mu sync.Mutex
	successCount := 0
	interval := 1 * time.Millisecond
	ticker := time.NewTicker(interval)

	for successCount < max_order {
		wg.Add(1)
		go sendRequest(&wg, url, data, headers, &successCount, &mu, max_order)
		<-ticker.C
	}
	ticker.Stop()
	wg.Wait()

}

func getHeaders() map[string]string {

	cookie := os.Getenv("COOKIE")
	token := os.Getenv("TOKEN")
	session := os.Getenv("SESSION")
	request_owner := os.Getenv("REQUEST_OWNER")
	domain := os.Getenv("TMS")

	headers := make(map[string]string)
	headers["Content-Type"] = "application/json"
	headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"

	headers["host"] = "tms" + domain + ".nepsetms.com.np"
	headers["accept"] = "application/json, text/plain, */*"
	headers["cookie"] = cookie
	headers["x-xsrf-token"] = token
	headers["host-session-id"] = session
	headers["request-owner"] = request_owner

	return headers
}

func sendRequest(wg *sync.WaitGroup, url string, data string, headers map[string]string, successCount *int, mu *sync.Mutex, order int) {
	defer wg.Done()

	req, err := http.NewRequest("POST", url, bytes.NewBuffer([]byte(data)))
	if err != nil {
		fmt.Println("Error creating request:", err)
		return
	}

	for key, value := range headers {
		req.Header.Add(key, value)
	}
	req.Header.Add("Content-Length", strconv.Itoa(len(data)))
	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		fmt.Println("Error : ", err)
		return
	}
	defer resp.Body.Close()
	if resp.StatusCode >= 200 && resp.StatusCode < 300 {
		mu.Lock()
		*successCount++
		mu.Unlock()
		fmt.Println(strconv.Itoa(*successCount) + "/" + strconv.Itoa(order) + "ORDER Placed!!!")
	}

}
