package main

import (
	"bytes"
	"context"
	"fmt"
	"io"
	"math"
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

	if domain == "" {
		fmt.Println("Missing required environment variables (DOMAIN).")
		return
	}
	headers := getHeaders()
	url := "https://tms" + domain + ".nepsetms.com.np/tmsapi/orderApi/order/"

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

			// Parse input
			startVal, _ := strconv.ParseFloat(os.Getenv("PER10"), 64)

			// Compute ceiling and lower bound
			ceil := math.Ceil(startVal)
			start := ceil
			end := ceil - 2.0

			// Loop from ceiling down to ceiling - 2.0
			isSuccess := false
			priceFound := false
			exactPrice := ""
			mu.Lock()
			if !priceFound {
				for val := start; val >= end-1e-9; val -= 0.1 {
					price := fmt.Sprintf("%.1f", math.Round(val*10)/10)
					isSuccess = sendRequest(url, price, headers)
					if isSuccess {
						priceFound = true
						exactPrice = price
						break
					}
				}
			} else {
				isSuccess = sendRequest(url, exactPrice, headers)
			}

			mu.Unlock()

			if isSuccess {
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
func getBody(price string) string {
	qty := "500"
	fmt.Println("Placing order for " + os.Getenv("SYMBOL") + " at " + qty + " @ " + price)
	return `{
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
            "id": ` + os.Getenv("CLIENT_ID") + `,
            "accountType": "CLI",
            "allowedToTrade": "Y",
            "clientMemberCode": ` + os.Getenv("CLIENT_ID") + `,
            "clientOrDealer": "C",
            "contactNumber": "PHONE",
            "emailId": null,
            "notsUniqueClientCode": ` + os.Getenv("CLIENT_CODE") + `,
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
            "id": ` + os.Getenv("ID") + `,
            "exchangeSecurityId": ` + os.Getenv("SECURITY_ID") + `,
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

func sendRequest(url string, price string, headers map[string]string) bool {
	data := getBody(price)

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

	// Read the response body
	responseBody, err := io.ReadAll(resp.Body)
	if err != nil {
		fmt.Println("Error reading response body:", err)
		return false
	}
	fmt.Println("Status Code : ", resp.StatusCode)
	fmt.Println("Resp : ", string(responseBody))

	defer resp.Body.Close()

	return resp.StatusCode == http.StatusOK

}
