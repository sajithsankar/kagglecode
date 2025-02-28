import pandas as pd

# Load the dataset
file_path = 'Ecommerce-Transactions.csv'
data = pd.read_csv(file_path)

# Data sanity check
def data_sanity_check(df):
    print("Data Sanity Check:")
    print("1. Checking for duplicates...")
    duplicates = df.duplicated().sum()
    print(f"  - Number of duplicate rows: {duplicates}")
    
    print("2. Checking for missing values...")
    missing_values = df.isnull().sum()
    print(f"  - Missing values per column:\n{missing_values}")
    
    print("3. Checking for outliers in transaction amount...")
    print(f"  - Transaction amount statistics:\n{df['transaction_amount'].describe()}")

data_sanity_check(data)

# Calculate RFM metrics
def calculate_rfm(df, current_date):
    # Convert purchase_date to datetime
    df['purchase_date'] = pd.to_datetime(df['purchase_date'])
    
    # Calculate Recency, Frequency, and Monetary
    rfm = df.groupby('customer_id').agg({
        'purchase_date': lambda x: (current_date - x.max()).days,
        'customer_id': 'count',
        'transaction_amount': 'sum'
    }).rename(columns={
        'purchase_date': 'recency',
        'customer_id': 'frequency',
        'transaction_amount': 'monetary'
    })
    
    return rfm

current_date = pd.Timestamp('2025-02-28')
rfm = calculate_rfm(data, current_date)

# Assign RFM scores
def assign_rfm_scores(rfm):
    rfm['recency_score'] = pd.qcut(rfm['recency'], 4, labels=[4, 3, 2, 1])
    rfm['frequency_score'] = pd.qcut(rfm['frequency'].rank(method='first'), 4, labels=[1, 2, 3, 4])
    rfm['monetary_score'] = pd.qcut(rfm['monetary'], 4, labels=[1, 2, 3, 4])
    
    return rfm

rfm_scores = assign_rfm_scores(rfm)

# Combine RFM scores into a single score
rfm_scores['RFM_Score'] = rfm_scores['recency_score'].astype(str) + rfm_scores['frequency_score'].astype(str) + rfm_scores['monetary_score'].astype(str)

# Save the results to a new CSV file
rfm_scores.to_csv('RFM_Scores.csv', index=True)

print("RFM analysis completed. RFM scores have been saved to 'RFM_Scores.csv'.")
