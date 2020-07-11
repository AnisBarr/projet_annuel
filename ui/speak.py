from espeakng import ESpeakNG
import speech_recognition as sr

def text_to_speech (text):
    esng = ESpeakNG()
    esng.voice = "fr" 
    esng.say(text)




# r = sr.Recognizer()
# mic = sr.Microphone()

# for index, name in enumerate(sr.Microphone.list_microphone_names()):
#     print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))

# mic = sr.Microphone(device_index=8)

# with mic as source:
#     r.adjust_for_ambient_noise(source)
#     audio = r.listen(source)

# print(r.recognize_google(audio))
