#import dependencies
import openai
import pyttsx3
import speech_recognition as spr
import sys
import API_Keys


conversation = ''
user_name = 'Ahmad'
bot_name = 'G-one'
openai.api_key = API_Keys.api_key

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id) #0 for male and 1 for female voice

# for voice in voices:
#     print(voice.id)
#     engine.setProperty('voice', voice.id)
#     engine.say("Hello")
# engine.runAndWait()

r = spr.Recognizer()
mic = spr.Microphone(device_index=1)
# print(spr.Microphone.list_microphone_names())
while True:
    with mic as source:

        print('\n' + bot_name +' listening..')

        r.adjust_for_ambient_noise(source, duration=0.2)
        audio = r.listen(source)
    print(bot_name +' not listening..\n')
    
    try:
        user_input = r.recognize_google(audio)
    except:
        continue
    
    prompt = user_name + ":" + user_input + "\n"+ bot_name + ":"
    conversation += prompt
    
    #fetch response from open AI api
    response = openai.Completion.create(engine='text-davinci-003', prompt=conversation, max_tokens=100)
    response_string = response["choices"][0]["text"].replace("\n", "")
    response_string = response_string.split(user_name + ": ", 1)[0].split(bot_name + ": ", 1)[0]
    conversation += response_string + "\n"
    print(response_string)
    #Convert response to Audio
    engine.say(response_string)
    engine.runAndWait()
    #Exit the loop when exit word appear in user input
    if 'exit' in user_input:
        sys.exit()
    

