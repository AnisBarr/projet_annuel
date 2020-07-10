# Import the Gtts module for text  
# to speech conversion 
from gtts import gTTS 
from pygame import mixer
import configparser
import logging
from logging.handlers import RotatingFileHandler

config = configparser.ConfigParser()
config.read('../config/config.ini')

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s-%(levelname)s-[%(message)s]')
file_handler = RotatingFileHandler(config['GLOBAL_LOG_MONITORING']['log'] , 'a', 1000000000, 1)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)



# Language we want to use 
def text_to_speech (text) :
    try :
        language = 'fr'
        output = gTTS(text=text, lang=language, slow=False)
        output.save("../resources/audio/output.mp3")

        mixer.init()
        mixer.music.load('../resources/audio/output.mp3')
        mixer.music.play()
        logger.info("text_to_speech  ... OK ")

    except Exception as e:
        logger.error("text_to_speech ... KO ")
        logger.error(f"The error '{e}' occurred")
# Play the converted file 
