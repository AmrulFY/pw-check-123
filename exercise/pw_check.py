import re
import numpy as np
import pandas as pd
from joblib import dump
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder, FunctionTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, accuracy_score
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier

def has_special_chars(password):
    pattern = r'[~`!@#$%^&*()\-_+={}\[\]|\\;:\'",.<>/?]'
    return bool(re.search(pattern, password))

def has_digits(password):
    pattern = r'\d'
    return bool(re.search(pattern, password))

def has_upper_and_lower(password):
    pattern_upper = r'[A-Z]'
    pattern_lower = r'[a-z]'
    return bool(re.search(pattern_upper, password)) and bool(re.search(pattern_lower, password))

def is_length_valid(password, min_length=10):
    pattern = fr'.{{{min_length},}}'
    return bool(re.fullmatch(pattern, password))

def has_common_patterns(password):
    common_patterns = [
        r'password',
        r'qwerty',
        r'abcdef',
    ]
    for pattern in common_patterns:
        if re.search(pattern, password, re.IGNORECASE):
            return True
    return False

def has_sequential_numbers(password):
    number_sequences = re.findall(r'\d+', password)

    for sequence in number_sequences:
        if len(sequence) >= 3:  # Memeriksa urutan dengan panjang minimal 3 angka
            # Memeriksa urutan menaik
            is_increasing = True
            for i in range(len(sequence) - 1):
                if int(sequence[i+1]) != int(sequence[i]) + 1:
                    is_increasing = False
                    break
            if is_increasing:
                return True

            # Memeriksa urutan menurun
            is_decreasing = True
            for i in range(len(sequence) - 1):
                if int(sequence[i+1]) != int(sequence[i]) - 1:
                    is_decreasing = False
                    break
            if is_decreasing:
                return True
    return False

def check_password_strength(password):
    if is_length_valid(password, 6) == False or has_common_patterns(password) == True or has_special_chars(password) == False or has_digits(password) == False or has_upper_and_lower(password) == False:
      return "Weak"
    elif is_length_valid(password, 10) == True and has_sequential_numbers(password) == False and has_special_chars(password) == True and has_digits(password) == True and has_upper_and_lower(password) == True and has_common_patterns(password) == False:
      return "Strong"
    else:
      return "Medium"
    
with open('rockyou.txt', 'r', encoding='latin-1') as file:
    data = file.read()

word = data.split('\n')
df_word = pd.DataFrame(word, columns=['pw'])
df_word['label'] = df_word['pw'].apply(check_password_strength)

def extract_features(password_series):
    features = []
    for password in password_series:
        feature = {
            'length': len(password),
            'num_upper': len(re.findall(r'[A-Z]', password)),
            'num_lower': len(re.findall(r'[a-z]', password)),
            'num_digit': len(re.findall(r'\d', password)),
            'num_special': len(re.findall(r'[~`!@#$%^&*()\-_+={}\[\]|\\;:\'",.<>/?]', password)),
            'has_upper': int(bool(re.search(r'[A-Z]', password))),
            'has_lower': int(bool(re.search(r'[a-z]', password))),
            'has_digit': int(bool(re.search(r'\d', password))),
            'has_special': int(bool(re.search(r'[~`!@#$%^&*()\-_+={}\[\]|\\;:\'",.<>/?]', password))),
        }
        features.append(feature)
    return pd.DataFrame(features)

def extract_sequential_feature(password_series):
    sequential_feature = password_series.apply(lambda x: int(not has_sequential_numbers(x)))
    return sequential_feature.to_frame()

# Fungsi untuk mengekstrak fitur dari password
def extract_features_transformer(password_series):
    return extract_features(password_series)

# Fungsi untuk mengekstrak fitur urutan angka
def extract_sequential_feature_transformer(password_series):
    return extract_sequential_feature(password_series)
        
def create_password_strength_pipeline(extract_features_transformer, extract_sequential_feature_transformer):
    # Membuat transformer untuk mengekstrak fitur
    feature_transformer = FunctionTransformer(extract_features_transformer)
    sequential_transformer = FunctionTransformer(extract_sequential_feature_transformer)

    # Membuat pipeline untuk fitur teks
    text_pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(analyzer='char', ngram_range=(1, 2), max_features=5000)),
    ])

    # Membuat column transformer untuk menggabungkan fitur
    preprocessor = ColumnTransformer(
        transformers=[
            ('text', text_pipeline, 'pw'),
            ('features', feature_transformer, 'pw'),
            ('sequential', sequential_transformer, 'pw')
        ]
    )

    # Membuat pipeline utama
    pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
    ])

    return pipeline

df_sample = df_word.sample(frac=0.5, random_state=42) 
X = df_sample[['pw']]
y = df_sample['label']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

pipeline = create_password_strength_pipeline(extract_features_transformer, extract_sequential_feature_transformer)
pipeline.fit(X_train, y_train)

y_pred = pipeline.predict(X_test)

dump(pipeline, 'password_strength_model_v2.joblib')

# Evaluasi model
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)

print(f"Accuracy: {accuracy}")
print("Classification Report:")
print(report)