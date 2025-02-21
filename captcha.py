import requests
import pickle
import os
from PIL import Image
from io import BytesIO
from config.utils import get_tms_id,get_headers_before_login

tms_id = get_tms_id()

def get_captcha_uuid():
    captcha_id_url = f'https://tms{tms_id}.nepsetms.com.np/tmsapi/authApi/captcha/id'
    res = requests.get(captcha_id_url,headers=get_headers_before_login()).json()       
    return res["id"]

def get_captcha_image(img_path:str):
    image_url = f"https://tms{tms_id}.nepsetms.com.np/tmsapi/authApi/captcha/image/{img_path}"
    response = requests.get(image_url,headers=get_headers_before_login())
    image = Image.open(BytesIO(response.content))
    image.show()


count = int(input("how many session you want ? "))
if count>0:
    for i in range(count):
        captcha_id=get_captcha_uuid()
        get_captcha_image(captcha_id)
        captcha_text=input("Please enter captcha text : ")

        dump_data=list(tuple())
        dump_data.append((captcha_id,captcha_text))

        print(dump_data)
        file_name=f"{tms_id}.pkl"
        if os.path.exists(file_name):
            with open(file_name, "rb") as f:
                old_data= pickle.load(f)
                dump_data.extend(old_data)

        with open(file_name, "wb") as file:
            pickle.dump(dump_data, file)
