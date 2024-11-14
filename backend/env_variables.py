import os

from dotenv import load_dotenv

load_dotenv()

########## ADMIN AUTH ##########

PAREDOWN_APP_USERNAME = os.getenv('PAREDOWN_APP_USERNAME')
PAREDOWN_APP_PASSWORD = os.getenv('PAREDOWN_APP_PASSWORD')

######### SERVER #########

WEB_HOST_OF_PAREDOWN_APP = os.getenv('WEB_HOST_OF_PAREDOWN_APP')
PAREDOWN_APP_FRONTEND_PORT = os.getenv('PAREDOWN_APP_FRONTEND_PORT')
