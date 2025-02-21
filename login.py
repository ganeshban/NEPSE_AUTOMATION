import requests
import pickle
import os
import base64
import sys
import time
import uuid
from config.utils import get_tms_id,get_password,get_user_name, get_headers_before_login, auto_runner

tms_id = get_tms_id()
user_name = get_user_name()
password = get_password()

def exit_app():
    print('exiting application ......................')
    time.sleep(60)
    sys.exit()

def file_error():
    print("no more session avaiable, please load the session first.")
    exit_app()

def get_captcha_info():
    file_name = f"{tms_id}.pkl"
    captcha_info:tuple = None
    if os.path.exists(file_name):
        if os.path.getsize(file_name)>0:
            data = None
            with open(file_name, "rb") as f:
                data = list(pickle.load(f))
                if len(data)>0:
                    captcha_info = data.pop()
                else:
                    file_error()
            
            with open(file_name, "wb") as f:
                pickle.dump(data, f)

        else:
            file_error()
    else:
        file_error()

    return captcha_info

def do_login():
    uuid,text = get_captcha_info()

    if len(text)>len(uuid):
        text,uuid = uuid,text
    
    payload = {
            "userName": user_name,
            "password": base64.b64encode(password.encode()).decode(),
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
    session = base64.b64encode(session.encode()).decode()
    host_session = f'{session}-{uuid.uuid4()}'
    host_session =base64.b64encode(host_session.encode()).decode()

    lines = []

    lines.append(f"COOKIE='{cookie}'\n")
    lines.append(f"TOKEN='{token}'\n")
    lines.append(f"SESSION='{host_session}'\n")
    lines.append(f"REQUEST_OWNER='{body['user']['id']}'\n")
    lines.append(f"TMS='{tms_id}'")

    file_name = './GO/.env'

    with open(file_name, "w") as f:
        f.writelines(lines)

sleep_time=60*25
while True:
    metadata = do_login()
    update_req_metadata(metadata)
    print(f'System will wake up again in {sleep_time//60} mins.')

    if auto_runner()==True:
        os.system("chmod +x ./Go/runner.sh")
        os.system("bash ./Go/runner.sh")
    
    time.sleep(sleep_time)


# count = int(input("how many session you want ? "))
# if count>0:
#     for i in range(count):
#         captcha_id=get_captcha_uuid()
#         get_captcha_image()
#         captcha_text=input("Please enter captcha text : ")
        
#         dump_data=list(dict())
#         dump_data.append({captcha_id,captcha_text})

#         print(dump_data)
#         file_name=f"{tms_id}.pkl"
#         if os.path.exists(file_name):
#             with open(file_name, "rb") as f:
#                 old_data= pickle.load(f)
#                 dump_data.extend(old_data)

#         with open(file_name, "wb") as file:
#             pickle.dump(dump_data, file)
