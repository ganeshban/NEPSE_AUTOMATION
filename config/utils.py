from dotenv import load_dotenv
import os
import base64

load_dotenv()
def get_user_name():
    return os.getenv("USER_NAME")

def get_password():
    return os.getenv("PASSWORD")

def get_tms_id():
    return os.getenv("TMS_ID")

def auto_runner():
    return bool(os.getenv("AUTO_START_ORDER"))

def get_symbol():
    return os.getenv("SYMBOL")

def encode_base64(param:str):
    return base64.b64encode(param.encode()).decode()

def decode_base64(param:str):
    return base64.b64decode(param).decode()

def get_headers_before_login():
    return {
            # 'Origin': f'https://tms{get_tms_id()}.nepsetms.com.np',
            'Host' : f'tms{get_tms_id()}.nepsetms.com.np',
            'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            'Accept' : 'application/json, text/plain, */*',
            'Content-Type' : 'application/json',
            }

def get_headers_after_login(cookie, session, token, owner):
    return {
            'Cookie' : cookie,
            'X-XSRF-TOKEN' : token,
            'host-session-id' : session,
            'request-owner' : owner
            } | get_headers_before_login()
