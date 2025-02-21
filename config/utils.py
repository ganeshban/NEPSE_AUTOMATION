from dotenv import load_dotenv
import os

load_dotenv()
def get_user_name():
    return os.getenv("USER_NAME")

def get_password():
    return os.getenv("PASSWORD")

def get_tms_id():
    return os.getenv("TMS_ID")

def auto_runner():
    return os.getenv("AUTO_START_ORDER")

def get_headers_before_login():
    return {
            # 'Origin': f'https://tms{get_tms_id()}.nepsetms.com.np',
            'Host' : f'tms{get_tms_id()}.nepsetms.com.np',
            'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            'Accept' : 'application/json, text/plain, */*',
            'Content-Type' : 'application/json',
            }

def get_headers_after_login():
    return {
            'Cookie' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            'X-XSRF-TOKEN' : 'application/json, text/plain, */*',
            'host-session-id' : f'https://tms{get_tms_id()}.nepsetms.com.np/login',
            'request-owner' : f'https://tms{get_tms_id()}.nepsetms.com.np/login'
            } | get_headers_before_login()
