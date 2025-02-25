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


def get_captcha():
    captcha_id:str=get_captcha_uuid()
    get_captcha_image(captcha_id)
    captcha_text=input("Please enter captcha text : ")

    return captcha_text, captcha_id
