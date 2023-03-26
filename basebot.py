import pyttsx3
import time
# import openai_secret_manager
import testchatgpt
import speech_recognition as sr
import json
import requests
from statistics import mean




def sendmedicationreminder():


    url = "https://us-central1-aiot-fit-xlab.cloudfunctions.net/sendsms"

    payload = json.dumps({
    "receiver": "18137516099",
    "message": "Hello!  This is a friendly reminder from FitBOT to take your medication on time.",
    "token": "get ur own token"
    })
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)




def getreadings():


    url = "https://us-central1-aiot-fit-xlab.cloudfunctions.net/fitbot"

    payload = json.dumps({
    "action": "getreadings"
    })
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
    
    rj = response.json()
    
    temps, hums, hr, o2, co2, bps = ([] for i in range(6))
    
    for r in rj['readings']:
        if r['name'] == "temperature":
            temps.append(float(r['value']))
            continue
        if r['name'] == "Humidity":
            hums.append(float(r['value']))
            continue
        if r['name'] == "CO2":
            co2.append(float(r['value']))
            continue
        if r['name'] == "Heart Rate":
            hr.append(float(r['value']))
            continue
        if r['name'] == "SPO2":
            o2.append(float(r['value']))
            continue
        if r['name'] == "Blood Pressure":
            bps.append(float(r['value']))
            continue
    
    return temps, hums, hr, o2, co2, bps
    





def getsnores():

    url = "https://us-central1-aiot-fit-xlab.cloudfunctions.net/fitbot"

    payload = json.dumps({
    "action": "getsnores",
    "dayid": "0"
    })
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
    
    rj = response.json()
    
    return rj['count']


def getrooms():


    url = "https://us-central1-aiot-fit-xlab.cloudfunctions.net/fitbot"

    payload = json.dumps({
    "action": "getrooms"
    })
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
    
    rj = response.json()
    
    return rj['rooms']




# obtain audio from the microphone
r = sr.Recognizer()

def getspeech():
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)


    # recognize speech using Google Speech Recognition
    sp = "unknown"
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        sp = r.recognize_google(audio)
        print("Google Speech Recognition thinks you said " + sp)
        return sp
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        return sp
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return sp



# initialize Text-to-speech engine
engine = pyttsx3.init()
engine.setProperty("rate", 150)


def saysomething (text):
    

    # convert this text to speech
    # text = "Hello! welcome to Fit Bot!"
    engine.say(text)
    # play the speech
    engine.runAndWait()
    



##init


saysomething("Hello! welcome to Fit Bot")
time.sleep(3)

sp = "unknown"

temps, hums, hr, o2, co2, bps = getreadings()


while True:
    print("start main interface")
    
    while sp == "unknown":
        sp = getspeech()
    
    if "ask" in sp and "GPT" in sp:
        prompt = sp.split("GPT")[1]
        print (prompt)
        prompt = prompt + " in 50 words or less"
        
        print (prompt)
        ##call chatgpt
        
        res = testchatgpt.getchatgpt(prompt)
        
        saysomething(res)
        
        
        sp = "unknown"
        continue
    
    
    if "i snore" in sp.lower():
        
        res = getsnores()
        
        saysomething("last night you snored "+ str(res) + " times")
        if res > 15:
            print ("pre emptive sleep apnea warning")
            prompt = "tell me about snoring and sleep apnea in 70 words or less"
            res = testchatgpt.getchatgpt(prompt)
        
            saysomething(res)        
        
        
        sp = "unknown"
        continue   
    
    
    
    if "how many" in sp.lower() and "room" in sp.lower():
        
        rooms = getrooms()
        saysomething("here is the latest count of all the rooms in the house ...")
        
        i = 1
        for r in rooms:
            word =  "people"
            if r == 1:
                word = "person"
            saysomething("room number " + str(i) +" has " + str(r) + " "+ word)
            i +=1
        
        sp = "unknown"
        continue   


    if "what" in sp.lower() and "temperature" in sp.lower():
        
        avtemp = mean(temps)
        
        saysomething("the average temperature for the last few hours is " +str(avtemp) + " degrees")
        
        
        sp = "unknown"
        continue     


    if "what" in sp.lower() and "humidity" in sp.lower():
        
        avhum = mean(hums)
        
        saysomething("the average humidity for the last few hours is " +str(avhum) + " percent")
        
        
        sp = "unknown"
        continue  


    if "what" in sp.lower() and "carbon dioxide" in sp.lower():
        
        avco2 = mean(co2)
        
        saysomething("the average carbon dioxide level for the last few hours is " +str(avco2) + " parts per million")
        
        
        sp = "unknown"
        continue 





    if "what" in sp.lower() and "my" in sp.lower() and "blood oxygen" in sp.lower():
        
        avo2 = mean(o2)
        
        saysomething("your average blood oxygen saturation for the last few hours is " +str(avo2) + " percent")
        
        
        sp = "unknown"
        continue  


    if "what" in sp.lower() and "my" in sp.lower() and "heart rate" in sp.lower():
        
        avhr = mean(hr)
        
        saysomething("your average heart rate for the last few hours is " +str(avhr) + " beats per minute")
        
        
        sp = "unknown"
        continue 

    if "what" in sp.lower() and "my" in sp.lower() and "pulse" in sp.lower():
        
        avhr = mean(hr)
        
        saysomething("your average pulse for the last few hours is " +str(avhr) + " beats per minute")
        
        
        sp = "unknown"
        continue 


    if "what" in sp.lower() and "my" in sp.lower() and "blood pressure" in sp.lower():
        
        avbp = mean(bps)
        
        saysomething("your average blood pressure for the last few hours is " +str(avbp) + " millimeters mercury")
        
        
        sp = "unknown"
        continue 


    if "send" in sp.lower() and "notification" in sp.lower() and "medication" in sp.lower():
        
        
        sendmedicationreminder()
        
        saysomething("Reminder has been sent")
        
        sp = "unknown"
        continue 
    
    
    
    if "quit" in sp.lower() or "goodbye" in sp.lower():
        sp = "unknown"
        break 
    
    time.sleep(2)
    



saysomething("Goodbye!!")
