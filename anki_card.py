import pandas as pd
import re



class AnkiCard:
    def __init__(self,path_word_file):
        self.card_file = self.__read_file(path_word_file)
    
    def __read_file(self,path_word_file):
        return pd.read_csv(path_word_file,index_col=0)
    def camper_different(self,path_file):
        column_1 = self.card_file.columns[0]
        df_text = self.__read_file(path_file)
        column_2 = df_text.columns[0]
        
        missing_words = [word for word in  df_text[column_2] if word not in  self.card_file[column_1].values]
        return missing_words