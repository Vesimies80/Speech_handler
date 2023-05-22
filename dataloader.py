import torch
from transformers import AutoTokenizer, AutoModel
import pandas as pd

from csv import DictReader

class Dataloader:
    #funny enough the longest single utterance in training is 69 words long
    #TODO consider is there a better max_length and why
    def __init__(self, mode, max_length=69, tokenizer=None, nmfcc=13) -> None:
    
        if tokenizer is not None:
            self.tokenizer = tokenizer
            
        else:
            self.tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
        self.nmfcc = nmfcc
        self.max_length = max_length
        self.mode = mode
        self.audio_data = {}
        # Load csv files for feature extraction
        if self.mode == "dev":
            with open("MELD_MP3/dev_sent_emo.csv") as f:
                
                dict_read = DictReader(f)
                self.text_data = list(dict_read)
            with open('MELD_MP3/MELD_MFCC_features_dev.csv') as file:
                for line in file:
                    line = line.replace("[", "")
                    line = line.replace("]", "")
                    cleaned_line = line.strip().split('::')
                    key = cleaned_line[0]
                    strvalues = cleaned_line[1:]
                    values = []
                    for value in strvalues:
                        str_value = value.split(",")
                        int_value =[]
                        for element in str_value:
                            int_value.append(float(element))
                        values.append(int_value)
                    self.audio_data[key] = values

        if self.mode == "test":
            with open("MELD_MP3/test_sent_emo.csv") as f:
                
                dict_read = DictReader(f)
                self.text_data = list(dict_read)
            with open('MELD_MP3/MELD_MFCC_features_test.csv') as file:
                for line in file:
                    line = line.replace("[", "")
                    line = line.replace("]", "")
                    cleaned_line = line.strip().split('::')
                    key = cleaned_line[0]
                    strvalues = cleaned_line[1:]
                    values = []
                    for value in strvalues:
                        str_value = value.split(",")
                        int_value =[]
                        for element in str_value:
                            int_value.append(float(element))
                        values.append(int_value)
                    self.audio_data[key] = values
            
        if self.mode == "train":    
            with open("MELD_MP3/train_sent_emo.csv") as f:
                
                dict_read = DictReader(f)
                self.text_data = list(dict_read)
            with open('MELD_MP3/MELD_MFCC_features_train.csv') as file:
                for line in file:
                    line = line.replace("[", "")
                    line = line.replace("]", "")
                    cleaned_line = line.strip().split('::')
                    key = cleaned_line[0]
                    strvalues = cleaned_line[1:]
                    values = []
                    for value in strvalues:
                        str_value = value.split(",")
                        int_value =[]
                        for element in str_value:
                            int_value.append(float(element))
                        values.append(int_value)
                    self.audio_data[key] = values
            
        

        
        self.data = {}
        self.text_only = {}
        #This is probably faster then using a ordered dict
        self.indexed_keys =[]
        self.pair_audio_and_text()
        self.n_data = len(self.data)
        
        print(self.n_data)
        print(self.text_data[0:2])
        print(self.audio_data["dia0_utt0"][0][0])
        #self.pair_audio_text_and_prepare_data()
        
    #Obsolete
    def parse_csv(self, file_text):
        dict_read = DictReader(file_text)
        for row in dict_read:
            yield row
    #Obsolete
    def max_lenght_text(self):
        max_len = 0
        for text in self.text_data:
            lenght = len(text['Utterance'].split(' '))
            if  lenght > max_len:
                max_len = lenght
        return max_len
    
    
    def prepare_text_data(self):
        for text in self.text_data:
            dia = text["Dialogue_ID"]
            ut = text["Utterance_ID"]
            idx = 'dia'+str(dia) + '_' + 'utt' +str(ut)

            label = text['Emotion']
            only_text = text['Utterance']
            
            tokenized_text = self.tokenizer(only_text, add_special_tokens=True, return_tensors='pt', padding='max_length', truncation=True, max_length=self.max_length)
            
            self.text_only[idx] = [label, tokenized_text]
            
            
    def pair_audio_and_text(self):
        self.prepare_text_data()
        #This key is the dia(nro) utt(nro) string
        for key,value in self.audio_data.items():
            label = self.text_only[key][0]
            text = self.text_only[key][1]
            audio_features = value
            self.indexed_keys.append[key]
            self.data[key] = [text, audio_features, label, key]
            
    #Obsolete
    def pair_audio_text_and_prepare_data(self):
        
        for text in self.text_data:
            dia = text["Dialogue_ID"]
            ut = text["Utterance_ID"]
            idx = str(dia) + '_' + str(ut)

            label = text['Emotion']
            Sr_no = text['Sr No.']
            only_text = text['Utterance']
            
            tokenized_text = self.tokenizer(only_text, add_special_tokens=True, return_tensors='pt', padding='max_length', truncation=True, max_length=self.max_length)
            
            sample = {
                "tokenized_text": tokenized_text,
                "audio_features": self.audio_data[idx],
                "label": label,
                "Sr_no": Sr_no
            }
            self.data.append(sample)
            
        return
    
    def __len__(self):
        return self.n_data
    
    def __getitem__(self,idx):
        
        key = self.indexed_keys[idx]
        return self.data[key]