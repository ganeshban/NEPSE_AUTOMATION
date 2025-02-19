from dotenv import load_dotenv
import os

load_dotenv()
def get_user_name():
    return os.getenv("USER_NAME")

def get_password():
    return os.getenv("PASSWORD")
def get_tms_id():
    return os.getenv("TMS_ID")