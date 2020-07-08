# Import the Gtts module for text  
# to speech conversion 
from gtts import gTTS 
from pygame import mixer




# Language we want to use 
def text_to_speech (text) :
    language = 'fr'
    output = gTTS(text=text, lang=language, slow=False)
    output.save("../resources/audio/output.mp3")

    mixer.init()
    mixer.music.load('../resources/audio/output.mp3')
    mixer.music.play()

# Play the converted file 
