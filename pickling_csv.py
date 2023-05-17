import pandas as pd
import gzip
import pickle


# Read the CSV file into a pandas DataFrame
df = pd.read_csv('MELD_MP3/MELD_MFCC_features_train.csv')

# Compress the DataFrame using gzip
compressed_data = gzip.compress(df.to_csv().encode())

# Save the compressed data using pickle
with open('MELD_MP3/MELD_MFCC_features_train.pkl', 'wb') as file:
    pickle.dump(compressed_data, file)