import requests
import os
import sys
import uuid
from config.utils import encode_base64, get_tms_id,get_password,get_user_name, get_headers_before_login, auto_runner, get_symbol,get_headers_after_login
from captcha import get_captcha

tms_id = get_tms_id()
user_name = get_user_name()
password = get_password()


def do_login():
    text,uuid = get_captcha()

    payload = {
            "userName": user_name,
            "password": encode_base64(password),
            "jwt": "",
            "otp": "",
            "captchaIdentifier": uuid,
            "userCaptcha": text
    }
    hdrs = {
        'Content-Length':str(len(str(payload))),
        'referer':f'https://tms{tms_id}.nepsetms.com.np/login'
        } | get_headers_before_login()
    
    url = f'https://tms{tms_id}.nepsetms.com.np/tmsapi/authApi/authenticate'
    print('sending request ..........')
    res = requests.post(url,json=payload,headers=hdrs)
    print(f'Request compleated with the status code {res.status_code}')
    
    if res.status_code!=200:
        print("Couldn't log into your account, re-trying again......")
        do_login()
    else:
        return res

def get_stock_info(headers)->dict:
    securities = requests.get(f"https://tms{tms_id}.nepsetms.com.np/tmsapi/stock/securities",headers=headers).json()
    symbol = get_symbol()
    security = [item for item in securities if item['symbol'].lower()==symbol.lower()]
    return security[0]
    


def update_req_metadata(metadata):
    data:dict = metadata.headers
    all_raw_cookies = str(data['set-cookie'])
    all_raw_cookies = all_raw_cookies.split(', ')
    all_cookies = [a.split(';')[0] for a in all_raw_cookies ]
    token = ''
    cookie = ''

    for c in all_cookies:
        cookie = f'{cookie}; {c}'
        if c.startswith('XSRF'):
            token = c.split("=")[1]
    cookie = cookie.removeprefix('; ')
    body = metadata.json()
    body = body['data']
    session = str(body['sessionId'])
    session = encode_base64(session)
    host_session = f'{session}-{uuid.uuid4()}'
    host_session = encode_base64(host_session)
    owner = f"{body['user']['id']}"
    headers = get_headers_after_login(cookie,host_session,token,owner)
    stock_info = get_stock_info(headers)
    lines = []
    baseAmt=round((stock_info['preOpenDprHigh']+stock_info['preOpenDprLow'])/2,1)
    amt=baseAmt
    lines.append(f"ID='{stock_info['id']}'\n")
    lines.append(f"SECURITY_ID='{stock_info['exchangeSecurityId']}'\n")
    lines.append(f"OPEN='{amt}'\n")
    amt=round(amt+(amt*0.02),1)
    lines.append(f"PER2='{amt}'\n")
    amt=round(amt+(amt*0.02),1)
    lines.append(f"PER4='{amt}'\n")
    amt=round(amt+(amt*0.02),1)
    lines.append(f"PER6='{amt}'\n")
    amt=round(amt+(amt*0.02),1)
    lines.append(f"PER8='{amt}'\n")
    lines.append(f"PER10='{round(baseAmt+(baseAmt*0.1),1)}'\n")
    lines.append(f"COOKIE='{cookie}'\n")
    lines.append(f"TOKEN='{token}'\n")
    lines.append(f"SESSION='{host_session}'\n")
    lines.append(f"REQUEST_OWNER='{owner}'\n")
    lines.append(f"TMS='{tms_id}'\n")
    lines.append(f"SYMBOL='{get_symbol()}'\n")
    lines.append(f"CLIENT_ID='{body['clientDealerMember']['client']['id']}'\n")
    lines.append(f"MEMBER_CODE='{body['clientDealerMember']['client']['clientMemberCode']}'\n")
    lines.append(f"CLIENT_CODE='{body['clientDealerMember']['client']['notsUniqueClientCode']}'\n")

    file_name = './GO/.env'

    with open(file_name, "w") as f:
        f.writelines(lines)

def run_bash_script():
    platform=sys.platform
    os.chdir("./GO")
    if platform =="win32":
        os.system("runner.sh")
        
    if platform =="darwin":
        os.system("bash ./runner.sh")

metadata = do_login()
update_req_metadata(metadata)
auto=auto_runner()
if auto:
    os.chmod("./Go/runner.sh",0o755)
    run_bash_script()