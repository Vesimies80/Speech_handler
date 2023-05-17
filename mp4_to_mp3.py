import moviepy.editor as mp
import os

folder_path = 'MELD_Raw/dev/dev_splits_complete'

output_path = 'MELD_MP3/dev'

for file_name in os.listdir(folder_path):
    if file_name.endswith('.mp4'):
        
        audio_file = folder_path + '/' + file_name
        mp3 = file_name.split(".")[0] + '.mp3'
        output_file = output_path + '/' + mp3
        my_clip = mp.VideoFileClip(audio_file)
        file = open(output_file, 'w')
        file.close()
        my_clip.audio.write_audiofile(output_file)