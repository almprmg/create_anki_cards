from abc import ABC, abstractmethod
from gtts import gTTS
from pydub import AudioSegment
import os
class TTS(ABC):
    def __init__(self, clint,lang ):
        self.clint: gTTS = clint
        self._lang = lang
    @abstractmethod
    def speck(self, text):
        raise NotImplementedError("Redefined method")
    
    @abstractmethod
    def save(self,path,format):
        if isinstance(self.clint , type):
            raise TypeError("First redefined speck method ")
        raise NotImplementedError("Redefined method  ,")




class TTSNormal(TTS):
    def __init__(self,lang = 'en'  ):
        super().__init__(gTTS , lang) 

    def speck(self, text):
        self.__tts = self.clint(text,lang = self._lang)

    def save(self, path):

        type_format = [".mp3",".wav"]
        list_path = os.path.splitext(path)
        mp3_path = os.path.join(*list_path[:-1],type_format[0]) 
        wav_path = os.path.join(*list_path[:-1],type_format[1]) 


        ext = list_path[-1].lower()


        if ext in type_format :
            
            self.__tts.save(mp3_path)

            if ext == type_format[1]:
                audio_segment = AudioSegment.from_mp3(mp3_path)
                audio_segment.export(wav_path, format="wav")
             
            if os.path.exists(mp3_path):
                os.remove(mp3_path)
            return 1 
       
        else:
            raise FileExistsError(f"{ext} type not defined  , type defined are {type_format} ") 
