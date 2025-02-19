import pandas as pd
from dotenv import load_dotenv
import genanki
from elevenlabs.client import ElevenLabs
from elevenlabs import  save

import re





class TextStyle:
    @staticmethod
    def b(text):

        return f"<b> {text} </b>"
    
    @staticmethod
    def center(text):

        return f'<div style="text-align: center;">{text}</div>'
     
    @staticmethod
    def span(text, color = "blue" , font_weight = "bold"):   


        return   f"""<span style="color:{color};font-weight:{font_weight}">{text}</span> """
class AnkiCard:
    def __init__(self,path_word_file,fields , templates,  name ="CSV to Anki Model"):
        self.card_file = self.__read_file(path_word_file)

        if (fields == None  ):
            fields = [
                {"name": "Word"},
                {"name": "Answer"},
                {"name": "Example"},
                {"name": "Audio"},
            ],
        if (templates == None  ):
            templates = [{
                "name": "Card 1",
                "qfmt": """
                          <div class="card">
                            <h2>{{Word}}</h2>
                          </div>
                        """ ,
                "afmt": """
                          <div class="card"> 
                            <h2>{{Word}}</h2>
                            <hr>
                            <p> {{Answer}}  <br>  <br>  </p>
                            <p> {{Example}}<br> </p>
                            {{Audio}} 
                          </div>
                        """ ,
                        },
            ]

        self.__model = genanki.Model(
            1607392319,  # معرف فريد عشوائي
            name ,
            fields=fields, 
            templates= templates 
        )
        self.__deck  = genanki.Deck(2059400110, name)
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
        
        card_df["Back"] = '<div style="text-align: center;"><b>'+ card_df["English Word"]   + "</b></div> " + '<div style="text-align: center;"><b>' +card_df["Arabic Translation"] + "</b></div> "+ """<div style="text-align: center;">  <b><br></b></div><div style="text-align: center;"><span style="text-align: start;">
                """ + card_df["Example Sentence"] + '</span><b><br></b></div>'
        card_df["English Word"]  = '<div style="text-align: center;"><b>'+ card_df["English Word"]   + "</b></div> "
        columns_drop = [column  for column in card_df if (column in  ["English Word","Back"] ) ]
        card_df.drop(columns_drop,axis= 1,inplace = True)

        return card_df

    

class TextToSpeech:

    def __init__(self):
        
        load_dotenv()
        
        self.__client = ElevenLabs()


    def text_to_speech(self, text, output_file="output.mp3"):

        audio =  self.__client.text_to_speech.convert(
            text= text,voice_id="21m00Tcm4TlvDq8ikWAM",

                model_id="eleven_multilingual_v2",

        )

 
        save(audio,output_file)
 
