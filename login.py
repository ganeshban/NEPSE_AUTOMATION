import requests
import pickle
import os
import base64
import sys
import time
from config.utils import get_tms_id,get_password,get_user_name, get_headers_before_login
from PIL import Image
from io import BytesIO

tms_id = get_tms_id()
user_name = get_user_name()
password = get_password()

def exit_app():
    print('exiting application ......................')
    time.sleep(6)
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
    
    payload = {
            "userName": user_name,
            "password": base64.b64encode(password.encode()).decode(),
            "jwt": "",
            "otp": "",
            "captchaIdentifier": uuid,
            "userCaptcha": text
    }
    hdrs = get_headers_before_login() | {'Content-Length':str(len(str(payload)))}
    url = f'https://tms{tms_id}.nepsetms.com.np/tmsapi/authApi/authenticate'
    res = requests.post(url,data=payload,headers=hdrs)
    return res
    
def update_req_metadata(metadata):
    data:dict=metadata.headers
    cookie=data['date']
    token=data['date']
    host_session=''

    lines=[]

    lines.append(f"COOKIE='{cookie}'\n")
    lines.append(f"TOKEN='{token}'\n")
    lines.append(f"SESSION='{host_session}'\n")
    lines.append(f"REQUEST_OWNER='{cookie}'\n")
    lines.append(f"TMS='{tms_id}'")

    file_name = './GO/.env'

    with open(file_name, "w") as f:
        f.writelines(lines)


while True:
    metadata = do_login()
    update_req_metadata(metadata)
    time.sleep(60*25)


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
