import os
import pandas as pd
from dotenv import load_dotenv
import genanki
from TTS import TTSNormal



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
    def __init__(self,path_word_file,fields , templates,css,  name ="CSV to Anki Model"):
        self.card_file = self.__read_file(path_word_file)
            
        self.audio_folder = "audio_files"
        os.makedirs(self.audio_folder, exist_ok=True)


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
        if (css == None ):     
          css="""
                .card {
                    font-family: Arial, sans-serif;
                    text-align: center;
                  
                    padding: 20px;
                    border-radius: 10px;
                }
                h2 {
                    color: #007bff;
                }
                p {
                    font-size: 18px;
                }
             """

        self.__model = genanki.Model(
            1607392319,  
            name ,
            fields=fields, 
            templates= templates ,
            css= css
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
    
    def create(self,name_of_apkg = "CSV_to_Anki.apkg"):
        media_files = []

        for index, row in self.card_file.iterrows():
            question = row["English Word"]
            answer = row["Example Sentence"]
            audio_filename = ""

            audio_filename = f"audio_{index}.mp3"
            audio_path = os.path.join(self.audio_folder, audio_filename)

            tts =TTSNormal()
            tts.speck(answer)
            tts.save(audio_path)
            media_files.append(audio_path)
            audio_tag = f"[sound:{audio_filename}]"
  

            note = genanki.Note(
                model=self.__model,
                fields=[question, answer, audio_tag],
            )
            self.__deck.add_note(note)

        package = genanki.Package( self.__deck)
        package.media_files = media_files  
        package.write_to_file("CSV_to_Anki.apkg")


    




