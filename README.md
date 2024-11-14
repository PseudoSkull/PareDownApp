# Pared Down app for Flask Login debugging
This app is a minimal reproduction of bugs encountered while trying to use [Flask-Login](https://pypi.org/project/Flask-Login/). It uses a React.js frontend built with Vite, which pairs with a Flask backend.

## Setup
Prerequisites:
- Python 3.11.3+
- Node.js v20.11.1+

### Backend
#### Install dependencies
```shell
pip install -r backend/requirements.txt
```

#### Setup environment
Add a file `backend/.env` that contains something like this:
```bash
########## ADMIN AUTH ##########

PAREDOWN_APP_USERNAME = 'admin'
PAREDOWN_APP_PASSWORD = 'mygreatpassword'

######### SERVER #########

WEB_HOST_OF_PAREDOWN_APP = "localhost"
PAREDOWN_APP_FRONTEND_PORT = "5173"
```

Adjust the values to fit your environment.

### Frontend
#### Install dependencies
```shell
npm install frontend/
```

## Start local dev env

### React frontend
```shell
cd frontend
npm run dev
```

### Flask backend
```shell
cd backend
python app.py
```
