import pandas as pd
import json

def preprocess_pmc_patients(input_path, output_path):
    # Read the CSV file
    df = pd.read_csv(input_path)
    
    # Select important features
    important_features = ['patient_uid', 'PMID', 'title', 'patient', 'age', 'gender', 'relevant_articles', 'similar_patients']
    df = df[important_features]
    
    # Clean and transform data
    df['age'] = df['age'].apply(lambda x: json.loads(x) if pd.notna(x) else [])
    df['age_years'] = df['age'].apply(lambda x: sum(value if unit == 'year' else value/12 if unit == 'month' else value/52 if unit == 'week' else value/365 if unit == 'day' else value/8760 for value, unit in x))
    
    df['relevant_articles'] = df['relevant_articles'].apply(lambda x: json.loads(x) if pd.notna(x) else {})
    df['similar_patients'] = df['similar_patients'].apply(lambda x: json.loads(x) if pd.notna(x) else {})
    
    # Convert gender to binary
    df['gender'] = df['gender'].map({'M': 1, 'F': 0})
    
    # Save the preprocessed data
    df.to_csv(output_path, index=False)
    print(f"Preprocessed data saved to {output_path}")

if __name__ == "__main__":
    input_path = "data/raw/PMC-Patients.csv"
    output_path = "data/processed/PMC-Patients_preprocessed.csv"
    preprocess_pmc_patients(input_path, output_path)