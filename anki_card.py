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
    
    def create_card(self):
        card_df =self.card_file.copy()
        
        card_df["Back"] = '<div style="text-align: center;"><b>'+ card_df["English Word"]   + "</b></div> " + '<div style="text-align: center;"><b>' +card_df["Arabic Translation"] + "</b></div> "+ """<div style="text-align: center;"><b><br></b></div><div style="text-align: center;"><span style="text-align: start;">
                """ + card_df["Example Sentence"] + '</span><b><br></b></div>'
        card_df["English Word"]  = '<div style="text-align: center;"><b>'+ card_df["English Word"]   + "</b></div> "
        columns_drop = [column  for column in card_df if (column in  ["English Word","Back"] ) ]
        card_df.drop(columns_drop,axis= 1,inplace = True)

        return card_df