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
    def save_to_audio(self,path,format):
        if isinstance(self.clint , type):
            raise NotImplementedError("clint not defend")
        raise NotImplementedError("Redefined method  ,")




    
