from abc import ABC, abstractmethod
from gtts import gTTS

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
    

