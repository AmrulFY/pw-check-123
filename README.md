# Password Strength Checker
A simple web app to evaluate password strength using a pre-trained machine learning model.

## Live Front End (Hosted on Vercel)
Open web via https://pw-check-123.vercel.app/

Note: This site only handles the user interface. All backend logic (including model predictions) runs locally.

## Backend (Run Locally)
The backend server is a Python Flask application that serves the ML model to evaluate password strength.

### How to run locally
1. Clone this repository:
   ```
   git clone https://github.com/AmrulFY/pw-check-123.git
   cd pw-check-123
   ```
2. (Optional) Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

   or if you set up your Python environment using Anaconda, follow these steps:
   ```
   # 1. Create a new environment named 'myenv' with Python 3.9 (or your version)
   conda create -n myenv python=3.9

   # 2. Activate the environment
   conda activate myenv

   # 3. Install required packages from requirements.txt
   pip install -r requirements.txt
   ```
   
3. Install dependencies:
   ```pip install -r requirements.txt```
5. Run the backend server:
   ```python backend/app.py```
7. The backend will be accessible at:
   ```http://localhost:5000```
 
