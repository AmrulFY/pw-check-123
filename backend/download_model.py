import os
import gdown

model_path = "models/password_strength_model_v2.joblib"
url = "https://drive.google.com/uc?id=12XXMQ-bG7XPlEuURzs7gcn_43rceoMYL"

if not os.path.exists(model_path):
    os.makedirs("models", exist_ok=True)
    gdown.download(url, model_path, quiet=False)
