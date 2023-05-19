import os
import librosa
import numpy as np
import csv
from tensorflow.keras.utils import pad_sequences

#A bit manual but good enough for this
folder_path = 'MELD_MP3/test'

output_file = 'MELD_MP3/MELD_MFCC_features_test.csv'

# Parameters for MFCC extraction
n_mfcc = 13
hop_length = 512
n_fft = 1024

# Max length based on longest training dataset audio and max 16 seconds
max_length = 687

# Initialize an empty list to store features
all_features = []

# Loop through each file in the folder
with open(output_file, 'w', newline='') as csvfile:
    counter = 0
    #writer = csv.writer(csvfile)
    #Header row
    #writer.writerow(['Audiofile', 'MFCC1','MFCC2','MFCC3','MFCC4','MFCC5','MFCC6', 'MFCC7', 'MFCC8', 'MFCC9', 'MFCC10', 'MFCC11', 'MFCC12', 'MFCC13'])
    for file_name in os.listdir(folder_path):
        counter += 1
        if file_name.endswith('.mp3'):
            # Load the audio
            audio_file = folder_path + '/' + file_name
            
            data, sample_rate = librosa.load(audio_file)

            # Extract MFCC features
            mfcc_features = librosa.feature.mfcc(y=data, sr=sample_rate, n_mfcc=n_mfcc, hop_length=hop_length, n_fft=n_fft)
            
            mfcc_features_normalized = librosa.util.normalize(mfcc_features)
            
            mfcc_features_normalized = pad_sequences(mfcc_features_normalized, maxlen = max_length, padding='post', truncating='post', dtype='float32')
            audio_name = file_name.replace(".mp3", "")
            csvfile.write(audio_name + '::')
            for i in range(13):
                if i < 12:
                    csvfile.write(np.array2string(mfcc_features_normalized[i], separator=',', max_line_width=10000000000000000) + '::')
                else:
                    csvfile.write(np.array2string(mfcc_features_normalized[i], separator=',', max_line_width=10000000000000000) + '\n')
            
            #writer.writerow([file_name, mfcc_features_normalized[0], mfcc_features_normalized[1], mfcc_features_normalized[2], mfcc_features_normalized[3], 
            #                 mfcc_features_normalized[4], mfcc_features_normalized[5], mfcc_features_normalized[6], mfcc_features_normalized[7], mfcc_features_normalized[8],
            #                 mfcc_features_normalized[9], mfcc_features_normalized[10], mfcc_features_normalized[11], mfcc_features_normalized[12]])
            # Append the features to the list
            all_features.append(mfcc_features_normalized)
            if counter % 100 == 0:
                print(counter, 'Files handled')


# Save the features to the output file
print("DONE!")