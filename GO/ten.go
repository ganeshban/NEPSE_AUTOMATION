package main

import (
	"bytes"
	"context"
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

	const (
		maxOrder        = 5
		maxConcurrent   = 100
		requestInterval = 1 * time.Millisecond
	)

	var (
		successCount int
		mu           sync.Mutex
		wg           sync.WaitGroup
	)

	sem := make(chan struct{}, maxConcurrent)
	ticker := time.NewTicker(requestInterval)
	defer ticker.Stop()

	for {
		mu.Lock()
		if successCount >= maxOrder {
			mu.Unlock()
			break
		}
		mu.Unlock()

		<-ticker.C
		sem <- struct{}{}

		wg.Add(1)
		go func() {
			defer wg.Done()
			defer func() { <-sem }()

			if sendRequest(url, data, headers) {
				mu.Lock()
				if successCount < maxOrder {
					successCount++
				}
				mu.Unlock()
				fmt.Println(strconv.Itoa(successCount) + " / " + strconv.Itoa(maxOrder) + " order placed! ")
			}
		}()
	}

	wg.Wait()

	// for successCount < max_order {
	// 	wg.Add(1)
	// 	go sendRequest(url, data, headers)
	// 	<-ticker.C
	// }
	// ticker.Stop()
	// wg.Wait()

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

func sendRequest(url string, data string, headers map[string]string) bool {
	_, cancel := context.WithTimeout(context.Background(), 2*time.Second)
	defer cancel()

	req, err := http.NewRequest("POST", url, bytes.NewBuffer([]byte(data)))
	if err != nil {
		return false
	}

	for key, value := range headers {
		req.Header.Add(key, value)
	}
	req.Header.Add("Content-Length", strconv.Itoa(len(data)))

	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		fmt.Println("Error : ", err)
		return false
	}
	defer resp.Body.Close()

	return resp.StatusCode == http.StatusOK

}
