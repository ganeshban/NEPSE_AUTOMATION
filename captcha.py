import requests
import pickle
import os
from PIL import Image
from io import BytesIO
from config.get_env import get_tms_id

tms_id = get_tms_id()
def get_header_not_login():
    return {"host":f"tms{tms_id}.nepsetms.com.np",
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            'accept':'application/json, text/plain, */*',
            'referer':f'https://tms{tms_id}.nepsetms.com.np/login'
            }

count = int(input("how many session you want ? "))
if count>0:
    for i in range(count):
        captcha_id_url = f'https://tms{tms_id}.nepsetms.com.np/tmsapi/authApi/captcha/id'
        res = requests.get(captcha_id_url,headers=get_header_not_login()).json()       
        captcha_id=res["id"]

        image_url = f"https://tms{tms_id}.nepsetms.com.np/tmsapi/authApi/captcha/image/{captcha_id}"

        response = requests.get(image_url,headers=get_header_not_login())
        image = Image.open(BytesIO(response.content))

        image.show()
        captcha_text=input("Please enter captcha text : ")
        dump_data=list(dict())
        dump_data.append({captcha_id,captcha_text})
        image.close()
        print(dump_data)
        file_name=f"{tms_id}.pkl"
        if os.path.exists(file_name):
            with open(file_name, "rb") as f:
                old_data= pickle.load(f)
                dump_data.extend(old_data)

        with open(file_name, "wb") as file:
            pickle.dump(dump_data, file)
