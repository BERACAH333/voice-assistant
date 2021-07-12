import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
# from geopy.geocoders import Nominatim
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os    
from IPython.display import Audio
from deepspeech import Model
from IPython.display import clear_output
import webbrowser
import pyautogui    
import psutil
import pyjokes
import fnmatch
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.actions.interaction import KEY
from selenium.webdriver.common import keys
from PIL import Image,ImageGrab
import urllib.request
from bs4 import BeautifulSoup
# import yagmail
import time
import gtts
import shutil
from PyDictionary import PyDictionary as Diction
import pywhatkit
import keyboard
import webbrowser
import pyaudio
import wave
import pandas
import os
import pickle
import warnings
import numpy as np
from sklearn import preprocessing
from scipy.io.wavfile import read
import python_speech_features as mfcc
# import speaker_verification_toolkit.tools as svt
from sklearn.mixture import GaussianMixture 
import random
warnings.filterwarnings("ignore")
################################################################################################
# geoLoc = Nominatim(user_agent="GetLoc")
# locname = geoLoc.reverse("26.7674446, 81.109758")
model_file_path = 'deepspeech-0.9.3-models.pbmm'
lm_file_path = 'deepspeech-0.9.3-models.scorer'
beam_width = 100
lm_alpha = 0.93
lm_beta = 1.18
volume=0
model = Model(model_file_path)
model.enableExternalScorer(lm_file_path)


model.setScorerAlphaBeta(lm_alpha, lm_beta)
model.setBeamWidth(beam_width)

stream = model.createStream()
def read_wav_file(filename):
    with wave.open(filename, 'rb') as w:
        rate = w.getframerate()
        frames = w.getnframes()
        buffer = w.readframes(frames)
        print("Rate:", rate)
        print("Frames:", frames)
        print("Buffer Len:", len(buffer))

    return buffer, rate

def transcribe_batch(audio_file):
    buffer, rate = read_wav_file(audio_file)
    data16 = np.frombuffer(buffer, dtype=np.int16)
    return model.stt(data16)


def transcribe_streaming(audio_file):
    buffer, rate = read_wav_file(audio_file)
    offset=0
    batch_size=8196
    text=""
    while offset < len(buffer):
        end_offset=offset+batch_size
        chunk=buffer[offset:end_offset]
        data16 = np.frombuffer(chunk, dtype=np.int16)
        stream.feedAudioContent(data16)
        text=stream.intermediateDecode()
        clear_output(wait=True)
        print(text)
        offset=end_offset
    return text

speaker=pyttsx3.init()
voices = speaker.getProperty('voices')
voiceses=0
speaker.setProperty('voice', voices[0].id)
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
path=r'G:\SOFTWARES\chromedriver_win32\chromedriver.exe'
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

on=0


################################################################################################ WORKING
def speak(message):
    speaker.say(message)
    speaker.runAndWait()
################################################################################################ WORKING
def times():
    Time=datetime.datetime.now().strftime("%I:%M:%S")
    speak(Time)
    print(Time)
################################################################################################ WORKING
def date():
    year=int(datetime.datetime.now().year)
    month = int(datetime.datetime.now().month)
    date = int(datetime.datetime.now().day)
    speak(date)
    speak(month)
    speak(year)
################################################################################################ WORKING
def wishme():
    hour=datetime.datetime.now().hour
    if hour>=6 and hour<12:
        speak("Good Morning Sir")
    elif hour>=12 and hour<16:
        speak("Good Afternoon Sir")
    elif hour>=16 and hour<20:
        speak("Good Evening Sir")
    else:
        speak("Good Night Sir")
    speak("The current time is ")
    times()
    speak("The current date is")
    date()
    speak("Jarvis at your service,tell me how can i help you")
################################################################################################ WORKING
def wishme1():
    speak("Welcome back sir")
    hour=datetime.datetime.now().hour
    if hour>=6 and hour<12:
        speak("Good Morning Sir")
    elif hour>=12 and hour<16:
        speak("Good Afternoon Sir")
    elif hour>=16 and hour<20:
        speak("Good Evening Sir")
    else:
        speak("Good Night Sir")
    speak("The current time is ")
    times()
    speak("The current date is")
    date()
    speak("Jarvis at your service,tell me how can i help you")
################################################################################################ WORKING
def takecommand():
    on=0
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 512
    RECORD_SECONDS = 5
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS,rate=RATE, input=True,frames_per_buffer=CHUNK)
    print ("recording started")
    Recordframes = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        Recordframes.append(data)
    print ("recording stopped")
    stream.stop_stream()
    stream.close()
    audio.terminate()
    OUTPUT_FILENAME="sample1.wav"
    WAVE_OUTPUT_FILENAME=os.path.join("testing_set",OUTPUT_FILENAME)
    waveFile = wave.open(OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(Recordframes))
    waveFile.close()
    r = sr.Recognizer()
    with sr.AudioFile("sample1.wav") as source:
        print("Ready")
        r.pause_threshold = 0.5
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.record(source)
    try:
        #query= r.recognize_sphinx(audio,language='en-US')  
        query = r.recognize_google(audio,language='en-in')
        if 'offline' in query or 'half line' in query:
            while(1):
                with sr.Microphone() as source:
                    r.pause_threshold = 1
                    r.adjust_for_ambient_noise(source, duration=1)
                    audio=r.listen(source)
                try:
                    query=r.recognize_google(audio,language='en-in')
                    if "online" in  query:
                        try:
                            os.remove("sample1.wav")
                            on=1
                        except:
                            pass
                        break
                    return query
                except sr.UnknownValueError:  
                    pass
                except:
                    pass
        print("Text: "+query)
    except sr.UnknownValueError:  
        return "none"
    except:
        pass
    if on==1:
        on=0
        return "online"
    again=test_model1(OUTPUT_FILENAME)
    print("again is",again)
    got=0
    global volume
    with open('start.txt') as f:
        lines = f.readlines()
        if again=='None':
            speak("Not Authorized Speaker")
            return 'none1'
        print("lines are as follows",lines)
        for i in lines:
            print("i value is",i)
            if '\n' in i:
                i=i.replace('\n','')
            if i in again and i!='\n': 
                k="Voice authorized as "+str(i)
                if volume==0:
                    speak(k)
                    volume+=1
                got=1
                break
    if got==1:
        r = sr.Recognizer()
        with sr.AudioFile("sample1.wav") as source:
            print("Ready")
            r.pause_threshold = 0.5
            r.adjust_for_ambient_noise(source, duration=1)
            audio = r.record(source)
        try:
            #query= r.recognize_sphinx(audio,language='en-US')  
            query = r.recognize_google(audio,language='en-in')
            print("Text: "+query)
            return query
        except sr.UnknownValueError:  
            return "none"
        
        except:
            query= r.recognize_sphinx(audio,language='en-US')  
            return query
            pass
    else:
        speak("Your voice is not recognized yet try again")
        return 'none'
    # interview = sr.AudioFile('sample.wav')
    # with interview as source:
    #     print('Ready...')
    #     r.pause_threshold = 2
    #     audio = r.record(source,duration=5)
    # query=r.recognize_google(audio,language='en-in')
    # print(query)
    # return query
    # with sr.Microphone() as source:
    #     print('Lisetning')
    #     r.pause_threshold = 1
    #     r.adjust_for_ambient_noise(source, duration=1)
    #     audio=r.listen(source)
    #     print(type(audio))
    # try:
    #     print('Recognizing')
    #     try:
    #         query=r.recognize_google(audio,language='en-in')
    #         print(query)
    #         return query
    #     except:
    #         return 
    # except Exception as e:
    #     print(e)
    #     return "None"    
################################################################################################
def sendemail(to, content):
    speak("Single mail or multiple mail")
    mail_type=takecommand().lower()
    if "single email" in mail_type:
        print("single mail")
        speak("What is the subject")
        subject=takecommand().lower()
        speak("What is the body of the mail")
        body1=takecommand().lower()
        speak("Is there any attachment included")
        reply=takecommand().lower()
        if "yes" in reply:
            print("Attachemnt")
            speak("tell me the name of the attachment")
            attach=takecommand().lower()
            mess="Tell the content of the "+attach
            speak(mess)
            mess=takecommand().lower()
            attach+=".txt"
            files=open(attach,"w")
            files.write(mess)
            files.close()
            fromadd="panam.beracah@gmail.com"
            to = "panam.beracah@gmail.com"
            msg = MIMEMultipart()
            msg['From'] = fromadd
            msg['To'] = to
            msg['Subject'] = subject
            msg.attach(MIMEText(body1, 'plain'))
            filename = "data.txt"
            filename=attach
            THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
            attachment = open(THIS_FOLDER+"\\"+filename, "rb")
            p = MIMEBase('application', 'octet-stream')
            p.set_payload((attachment).read())
            encoders.encode_base64(p)
            p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
            msg.attach(p)
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            s.login(fromadd, "Jbsas@333")
            text = msg.as_string()
            s.sendmail(fromadd, to, text)
            s.quit()   
            speak("Mail sent")
        else:
            print("No Attachemnt")
            to =['panam.beracah@gmail.com']#,'panam.amariah@gmail.com','panam.berach@gmail.com']
            gmail_user = 'panam.beracah@gmail.com'
            gmail_pwd = 'Jbsas@333'
            smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
            smtpserver.ehlo()
            smtpserver.starttls()
            smtpserver.ehlo
            smtpserver.login(gmail_user, gmail_pwd)
            header = 'To:' + ", ".join(to) + '\n' + 'From: ' + gmail_user + '\n' + 'Subject: ' +subject + '\n'
            msg = header + '\n' + body1+ '\n\n no attchement single email'
            smtpserver.sendmail(gmail_user, to, msg)
            smtpserver.close()
    elif "multiple email" in mail_type:
        speak("Is there any attachment included")
        reply=takecommand().lower()
        speak("What is the subject")
        subject=takecommand().lower()
        speak("What is the body of the mail")
        body1=takecommand().lower()
        if "yes" in reply:
            print("Attachemnt")
            speak("tell me the name of the attachment")
            attach=takecommand().lower()
            mess="Tell the content of the "+attach
            speak(mess)
            mess=takecommand().lower()
            attach+=".txt"
            files=open(attach,"w")
            files.write(mess)
            files.close()
            
            fromadd="panam.beracah@gmail.com"
            to = ["panam.beracah@gmail.com","panam.amariah@gmail.com","panam.berach@gmail.com","panam.beracah@aliet.ac.in","meesalagauti@gmail.com"] 
            for i in to:
                msg = MIMEMultipart()
                msg['From'] = fromadd
                msg['To'] = i
                msg['Subject'] = subject
                msg.attach(MIMEText(body1, 'plain'))
                filename = "data.txt"
                filename=attach
                THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
                attachment = open(THIS_FOLDER+"\\"+filename, "rb")
                p = MIMEBase('application', 'octet-stream')
                p.set_payload((attachment).read())
                encoders.encode_base64(p)
                p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
                msg.attach(p)
                s = smtplib.SMTP('smtp.gmail.com', 587)
                s.starttls()
                s.login(fromadd, "Jbsas@333")
                text = msg.as_string()
                s.sendmail(fromadd, to, text)
                s.quit()     
                break
            speak("Mail sent")        
        else:
            print("No attachement")
            to =['panam.beracah@gmail.com','panam.amariah@gmail.com','panam.berach@gmail.com','meesalagauti@gmail.com']
            gmail_user = 'panam.beracah@gmail.com'
            gmail_pwd = 'Jbsas@333'
            smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
            smtpserver.ehlo()
            smtpserver.starttls()
            smtpserver.ehlo
            smtpserver.login(gmail_user, gmail_pwd)
            header = 'To:' + ", ".join(to) + '\n' + 'From: ' + gmail_user + '\n' + 'Subject: ' +subject + '\n'
            msg = header + '\n' + body1 + '\n\n no attacment multiple email'
            smtpserver.sendmail(gmail_user, to, msg)
            smtpserver.close()
################################################################################################ WORKING
def screenshot():    
    speak("Want to show the screen shot or save the screen shot silently to the folder,Reply with yes or no")
    query=takecommand().lower()
    if query=="yes" or query=="s" or query=="yeah":
        image=ImageGrab.grab()
        speak("screen shot taken showing to you...")
        image.show()
    else:
        img=pyautogui.screenshot()
        speak("Tell me the name of your screenshot")
        while(1):
            query=takecommand().lower()
            if (query)!='none':
                break
            else:
                speak("Tell me again name of your screenshot")
        # list_dir = []
        # list_dir = os.listdir(r'G:\B.TECH\msp-web-scraping-master\msp-web-scraping-master\screenshot\ ')
        # c = 0
        # for file in list_dir:
        #     if file.endswith('.png'):
        #         c+=1
        #gt=len(fnmatch.filter(os.listdir("G:\B.TECH\msp-web-scraping-master\msp-web-scraping-master\screenshot\*.png"),"*.png"))+1
        img.save(r'G:\B.TECH\msp-web-scraping-master\msp-web-scraping-master\screenshot\ '+str(query)+'.png')
        print(query)
################################################################################################ WORKING
def cpu():
    usage = str(psutil.cpu_percent())
    speak('CPU is at ' + usage)
    battery = (psutil.sensors_battery())
    speak('Battery is at ')
    speak(battery.percent)
    if int(battery[0])<30:
        speak("Please plug in the charger")
    ram=psutil.virtual_memory()[2]
    ram1='RAM memory'+str(psutil.virtual_memory()[2])+'percentage used'
    speak(ram1)
def cpu1():
    battery = (psutil.sensors_battery())
    print(type(battery))
    print(battery[0])
    if int(battery[0])<30:
        speak("Please charge your laptop your battery is at "+str(battery[0])+" percentage")
################################################################################################ WORKING
def jokes():
    speak(pyjokes.get_joke())
    
def calculate_delta(array):
    rows,cols = array.shape
    deltas = np.zeros((rows,20))
    N = 2
    for i in range(rows):
        index = []
        j = 1
        while j <= N:
            if i-j < 0:
                first = 0
            else:
                first = i-j
            if i+j > rows -1:
                second = rows -1
            else:
                second = i+j
            index.append((second,first))
            j+=1
        deltas[i] = ( array[index[0][0]]-array[index[0][1]] + (2 * (array[index[1][0]]-array[index[1][1]])) ) / 10
    return deltas
def extract_features(audio,rate):
    mfcc_feature = mfcc.mfcc(audio,rate, 0.025, 0.01,20,nfft = 1200, appendEnergy = True)    
    mfcc_feature = preprocessing.scale(mfcc_feature)
    # print(mfcc_feature)
    delta = calculate_delta(mfcc_feature)
    combined = np.hstack((mfcc_feature,delta)) 
    return combined
def record_audio_train():
    Name =(input("Please Enter Your Name:"))
    speak("a different paras are shown for 5 times for each recording")
    speak("read the para when shown for recording")
    a=open('start.txt','a')
    lists=["text recognition","speech","audition","darknet","surface web","human","beracah","earth"]
    for count in range(5):
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100
        CHUNK = 256
        RECORD_SECONDS = 10
        audio = pyaudio.PyAudio()
        stream = audio.open(format=FORMAT, channels=CHANNELS,rate=RATE, input=True,frames_per_buffer=CHUNK)
        android=random.choice(lists)
        speak("recording will start in 2 seconds read the shown para")
        try:
            print("=========================================================================================================================================================")
            print(android)
            result=wikipedia.summary(android, sentences=4)
            print(result)
            print("=========================================================================================================================================================")
        except:
            print(wikipedia.summary("text recognition", sentences=4))
            pass
        Recordframes = []
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            Recordframes.append(data)
        speak("recording stopped")
        stream.stop_stream()
        stream.close()
        audio.terminate()
        OUTPUT_FILENAME=Name+"-sample"+str(count)+".wav"
        WAVE_OUTPUT_FILENAME=os.path.join("training_set",OUTPUT_FILENAME)
        trainedfilelist = open("training_set_addition.txt", 'a')
        trainedfilelist.write(OUTPUT_FILENAME+"\n")
        waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        waveFile.setnchannels(CHANNELS)
        waveFile.setsampwidth(audio.get_sample_size(FORMAT))
        waveFile.setframerate(RATE)
        waveFile.writeframes(b''.join(Recordframes))
        waveFile.close()
    a.write(Name)
    a.close()
def record_audio_test():
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 512
    RECORD_SECONDS = 10
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS,rate=RATE, input=True,frames_per_buffer=CHUNK)
    speak("recording starts in 2 seconds")
    Recordframes = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        Recordframes.append(data)
    speak("recording stopped")
    stream.stop_stream()
    stream.close()
    audio.terminate()
    OUTPUT_FILENAME="sample.wav"
    WAVE_OUTPUT_FILENAME=os.path.join("testing_set",OUTPUT_FILENAME)
    trainedfilelist = open("testing_set_addition.txt", 'w')
    trainedfilelist.write(OUTPUT_FILENAME+"\n")
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(Recordframes))
    waveFile.close()
def train_model():
    source   = "./training_set/"   
    dest = "./trained_models/"
    train_file = "./training_set_addition.txt"
    gmm_models="./gmm_models.txt"
    gmm_list=[]
    file_paths = open(train_file,'r')
    count = 1
    features = np.asarray(())
    for path in file_paths:    
        path = path.strip()   
        print(path)
        sr,audio = read(source + path)
        print(sr)
        vector   = extract_features(audio,sr)
        if features.size == 0:
            features = vector
        else:
            features = np.vstack((features, vector))
        if count == 5:    
            gmm = GaussianMixture(n_components = 6, max_iter = 200, covariance_type='diag',n_init = 3)
            gmm.fit(features)
            # dumping the trained gaussian model
            picklefile = path.split("-")[0]+".gmm"
            gmm_list.append(picklefile)
            pickle.dump(gmm,open(dest + picklefile,'wb'))
            print('+ modeling completed for speaker:',picklefile," with data point = ",features.shape)   
            features = np.asarray(())
            count = 0
        count = count + 1
    files=open(gmm_models,"w")
    for i in gmm_list:
        k=str(i)+"\n"
        files.write(k)
    files.close()

def test_model():
    source   = "./testing_set/"  
    modelpath = "./trained_models/"
    test_file = "./testing_set_addition.txt"       
    file_paths = open(test_file,'r')
    
    gmm_files = [os.path.join(modelpath,fname) for fname in os.listdir(modelpath) if fname.endswith('.gmm')]
    # print(gmm_files)
    #Load the Gaussian gender Models
    models    = [pickle.load(open(fname,'rb')) for fname in gmm_files]
    speakers   = [fname.split("/")[-1].split(".gmm")[0] for fname in gmm_files]
    # Read the test directory and get the list of test audio files 
    for path in file_paths:   
        path = path.strip()   
        print(path)
        sr,audio = read(source + path)
        vector   = extract_features(audio,sr)
        log_likelihood = np.zeros(len(models)) 
        print(log_likelihood)
        for i in range(len(models)):
            gmm    = models[i]  #checking with each model one by one
            # print('gmm',gmm)
            # print(speakers[i])
            scores = np.array(gmm.score(vector))
            # print('scores',scores)
            log_likelihood[i] = scores.sum()
            # print('logs',log_likelihood[i])
        # print('logggin\n\n\n\n\n\n\nn\n\n\n\n\n\n',log_likelihood)
        winner = np.argmax(log_likelihood)
        # print("\tdetected as - ", speakers[winner])
        time.sleep(1.0)  
def test_model1(audios):
    print("test models jersefnklsdflsvoasnvnafslv\n\n\n\nn\n")
    source   = "./testing_set/"  
    modelpath = "./trained_models/"
    test_file = "./testing_set_addition.txt"       
    file_paths = open(test_file,'r')
    gmm_files = [os.path.join(modelpath,fname) for fname in os.listdir(modelpath) if fname.endswith('.gmm')]
    #print(gmm_files)
    #Load the Gaussian gender Models
    models    = [pickle.load(open(fname,'rb')) for fname in gmm_files]
    speakers   = [fname.split("/")[-1].split(".gmm")[0] for fname in gmm_files]
    # Read the test directory and get the list of test audio files 
    for path in file_paths:   
        path = path.strip()   
        print(path)
        sr,audio = read("sample1.wav")
        vector   = extract_features(audio,sr)
        log_likelihood = np.zeros(len(models)) 
        #print(log_likelihood)
        for i in range(len(models)):
            gmm    = models[i]  #checking with each model one by one
            # print('gmm',gmm)
            # print(speakers[i])
            scores = np.array(gmm.score(vector))
            # print('scores',scores)
            log_likelihood[i] = scores.sum()
            # if int(log_likelihood[i]<=-23) and int(log_likelihood[i]>=-31):
            #     pass
            # else:
            #     print('logs',log_likelihood[i])    
            #     return 'None'
            print('logs',log_likelihood[i])
        # print('logggin\n\n\n\n\n\n\nn\n\n\n\n\n\n',log_likelihood)
        winner = np.argmax(log_likelihood)
        # print("\tdetected as - ", speakers[winner])
        # if max(log_likelihood)<0:
        #     return "No voice recognized"
        # time.sleep(1.0) 
        # try:
        #     os.remove('sample1.wav')
        # except:
        #     pass
        return speakers[winner]

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
if __name__=="__main__":
    # animal="this is an animal text"
    # speak(animal)
    #wishme()
    filesize = os.path.getsize("start.txt")
    if filesize == 0:
        speak("No User Detected.Give your name to recognize speakers.")
        record_audio_train()
        train_model()
    while(1):
        #cpu1()
        query=takecommand().lower()
        print('main',query)
        if "online" in query:
            speak("Jarvis at online sir, How can i help you")
        elif 'time' in query:      ################################################################## DONE
            times()
        elif 'none1' in query:
            continue
        elif 'lock screen' in query:
            print('lockscfreen')
            pyautogui.hotkey('win', 'l')
        elif 'hello jarvis' in query or 'hi jarvis' in query:
            speak("Hi Sir what can i do for you please give the commands")
#------------------------------------------------------------------------------------------------------------------------------------
        elif 'date' in query or 'gate' in query:   ################################################################## DONE
            date()
#------------------------------------------------------------------------------------------------------------------------------------
        elif 'quit' in query or 'exit' in query:   ################################################################## DONE
            print('exit')
            speak('Ok sir,Visit again.Have a Good Day')
            exit()
#------------------------------------------------------------------------------------------------------------------------------------
        elif 'offline' in query:    ################################################################## DONE
            speak("Ok Sir,Going to Sleep")
            time.sleep(1)
            speak("Call me when you need me")
            g=0
            while(1):
                query=takecommand().lower()
                if 'come to online' in query:
                    g=1
                    break
            if g==1:
                wishme1()
            else:
                speak("Sorry can't access at this point of time")
#------------------------------------------------------------------------------------------------------------------------------------
        elif 'wikipedia' in query:
            speak("What should i search sir")
            query=takecommand().lower()  #home
            speak("Shall i read out sir")
            query1=takecommand().lower() #yes /no
            query=query.replace("jarvis"," ")
            query=query.replace("search"," ")
            query=query.replace("for"," ")
            query=query.replace("hey"," ")
            query=query.replace("ok"," ")
            if query1=='yes' or query1=='yeah' or query1=='sure' or query1=='s':
                query=query.replace("jarvis"," ")
                query=query.replace("search"," ")
                query=query.replace("for"," ")
                query=query.replace("hey"," ")
                query=query.replace("ok"," ")
                result=wikipedia.summary(query, sentences=1)
                print(result)
                speak(result)
            else:
                speak("Please wait for a moment sir,i am opening your wiki search on website and website will close automatically in 30 seconds, so please read it out for yourself in given time")
                path=r'G:\SOFTWARES\chromedriver_win32\chromedriver.exe'
                driver = webdriver.Chrome(path)
                buttons = ActionChains(driver)
                driver.get('https://en.wikipedia.org/wiki/Main_Page')
                driver.implicitly_wait(20)
                time.sleep(5)
                driver.find_element_by_xpath('/html/body/div[5]/div[1]/div[2]/div/form/div/input[1]').send_keys(query)
                buttons.send_keys(Keys.ENTER).perform()
                driver.implicitly_wait(30)
                time.sleep(15)
                driver.close()
#------------------------------------------------------------------------------------------------------------------------------------                
        elif 'send email' in query:
            try:
                content="hai"
                to='sharonprabhu2@gmail.com'
                sendemail(to,content)
            except Exception as e:
                print(e)
                speak('Unable to send email')
#------------------------------------------------------------------------------------------------------------------------------------                
        elif 'search in chrome' in query:
            speak('What should i search')    
            path = 'C:/Program Files/Google/Chrome/Application/chrome.exe'    
            search=takecommand().lower()
            webbrowser.get(path).open_new_tab('youtube.com')    
#------------------------------------------------------------------------------------------------------------------------------------            
        elif 'logout' in query:     ################################################################## DONE
            os.system('shutdown -l')        
#------------------------------------------------------------------------------------------------------------------------------------
        elif 'shutdown' in query:    ################################################################## DONE    
            os.system('shutdown /s')    
#------------------------------------------------------------------------------------------------------------------------------------
        elif 'restart' in query:        ################################################################## DONE
            os.system('shutdown /r')    
#------------------------------------------------------------------------------------------------------------------------------------            
        elif 'play songs' in query:    
            songs_dir=r"E:\Songs"    
            songs=os.listdir(songs_dir)    
            os.startfile("E:\\jingle_bells.mp4")
#------------------------------------------------------------------------------------------------------------------------------------
        elif 'remember that' in query:
            speak("What should i remember")    
            data=takecommand()    
            speak("You said me to remember "+data)    
            remember=open('data.txt','w')    
            remember.write(data)    
            remember.close()    
#------------------------------------------------------------------------------------------------------------------------------------
        elif  'did i tell you anything' in query:    
            remember=open('data.txt','r')    
            speak('you said to remember that '+remember.read())
#------------------------------------------------------------------------------------------------------------------------------------            
        elif 'screenshot' in query:
            screenshot()    
            speak('done')
#------------------------------------------------------------------------------------------------------------------------------------            
        elif 'cpu usage' in query:
            cpu()
#------------------------------------------------------------------------------------------------------------------------------------            
        elif 'joke' in query or 'jokes' in query:
            jokes()
#------------------------------------------------------------------------------------------------------------------------------------
        elif 'open notepad' in query:
            os.startfile(r"C:\\WINDOWS\\system32\\notepad.exe")
        elif "microsoft word" in query:
            print(query)
            speak("opening ms word")
            os.startfile("C:\\Program Files (x86)\\Microsoft Office\\root\\Office16\\WINWORD")
            time.sleep(3)
            keyboard.send("enter")
#------------------------------------------------------------------------------------------------------------------------------------            
        elif "microsoft excel"in query:
            speak("opening ms excel")
            os.startfile("C:\\Program Files (x86)\\Microsoft Office\\root\\Office16\\EXCEL")
            time.sleep(3)
            keyboard.send("enter")
#------------------------------------------------------------------------------------------------------------------------------------            
        elif "microsoft powerpoint" in query or 'microsoft power point' in query:
            speak("opening ms Power Point")
            os.startfile("C:\\Program Files (x86)\\Microsoft Office\\root\\Office16\\POWERPNT")
            time.sleep(3)
            keyboard.send("enter")
#------------------------------------------------------------------------------------------------------------------------------------            
        elif "microsoft onenote" in query:
            speak("opening ms one note")
            os.startfile("C:\\Program Files (x86)\\Microsoft Office\\root\\Office16\\ONENOTE.EXE")
            time.sleep(3)
            keyboard.send("enter")
#------------------------------------------------------------------------------------------------------------------------------------            
        elif "write notes" in query:
            speak("What should i note,sir")
            notes=takecommand()
            file=open('notes.txt','w')
            speak("Sir should i include date and time also?")
            ans=takecommand()
            if "yes" in ans or "sure" in ans or "ok" in ans:
                strtime=datetime.datetime.now().strftime("%H:%M:%S")
                file.write(notes)
                file.write(" ")
                file.write("noted down on "+strtime)
                speak("Done taking notes")
            else:
                file.write(notes)
                speak("Done taking notes")
#------------------------------------------------------------------------------------------------------------------------------------                
        elif "show notes" in query:
            speak("showing notes")
            file=open('notes.txt','r')
            print(file.read())
            speak(file.read())
#------------------------------------------------------------------------------------------------------------------------------------            
        elif "jarvis come to online" in query:
            wishme1()
            speak("Good to see you again sir")
#------------------------------------------------------------------------------------------------------------------------------------            
        elif "download bulk images" in query or "download images" in query:
            speak("Tell the name of the image you want to download")
            search=takecommand().lower()
            driver = webdriver.Chrome(path)
            driver.get('https://images.google.com/')
            driver.implicitly_wait(2)
            driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys(search)
            buttons = ActionChains(driver)
            buttons.send_keys(Keys.ENTER).perform()
            i = 0
            while i<7:  
                driver.execute_script("window.scrollBy(0,document.body.scrollHeight)")
                try:
                    driver.find_element_by_xpath("/html/body/div[2]/c-wiz/div[3]/div[1]/div/div/div/div/div[5]/input").click()
                except Exception as e:
                    pass
                time.sleep(2)
                i+=1
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            driver.close()
            img_tags = soup.find_all("img", class_="rg_i")
            count = 0
            THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
            directory=THIS_FOLDER+'\\'+str(search)
            try:
                os.mkdir(directory)
            except:
                pass
            for i in img_tags:
                try:
                    urllib.request.urlretrieve(i['src'], str(count)+".jpg")
                    count+=1
                    source=THIS_FOLDER+'\\'+str(count-1)+'.jpg'
                    new_path = shutil.move(source, directory)
                    print("Number of images downloaded = "+str(count),end='\r')
                    if i==50:
                        break
                except Exception as e:
                    pass
        elif "send whatsapp messages" in query or "send whatsapp" in query:
            speak("Single contact or Multiple contact or delayed contact")
            choice=takecommand().lower()
            while(1):
                if "delayed message" in choice:
                    speak("Tell the contact")
                    contact=takecommand().lower()
                    speak("Tell the Message")
                    msg=takecommand().lower()
                    hour=datetime.datetime.now().hour
                    Time=datetime.datetime.now().strftime("%I:%M:%S")
                    times=str(Time)
                    a=times.split(':')
                    a[0]=hour
                    print(type(a))
                    for i in range(len(a)):
                        a[i]=int(a[i])
                    print(a)
                    if(int(a[-1])>30):
                        a[1]+=2
                    else:
                        a[1]+=1
                    if(a[1]>=60):
                        a[0]+=1
                        a[1]=abs(60-a[1])
                    pywhatkit.sendwhatmsg("+919347393970",msg,a[0],a[1],5)
                    speak("OK Sir , Sending Whatsapp Message !")
                    keyboard.press_and_release("enter")
                    break
                elif "single contact" in choice:
                    while(1):
                        speak("give the contact to send message")
                        contact=takecommand().lower()
                        print(contact)
                        contact=contact.replace(" ",'')
                        print(contact)
                        speak("is the shown number is correct?")
                        os.startfile(r"C:\\WINDOWS\\system32\\notepad.exe")
                        time.sleep(3)
                        keyboard.write(contact)
                        keyboard.send("ctrl+a")
                        speakers=takecommand().lower()
                        if speakers=="yes":
                            keyboard.send("backspace")
                            keyboard.send("alt+F4")
                            break
                        else:
                            keyboard.send("backspace")
                            keyboard.send("alt+F4")
                            time.sleep
                            speak("tell the contact again")
                    speak("tell the message")
                    message=takecommand().lower()
                    speak("Sending message.Please scan the Qr code int 5 Seconds")
                    path = 'G:\SOFTWARES\chromedriver_win32\chromedriver.exe'
                    driver = webdriver.Chrome(path)
                    buttons = ActionChains(driver)
                    driver.get('https://web.whatsapp.com/')
                    driver.implicitly_wait(20)
                    try:
                        driver.find_element_by_xpath('/html/body/div/div[1]/div[1]/div[3]/div/div[1]/div/label/div/div[2]').send_keys(contact) 
                        time.sleep(3)
                        buttons.send_keys(Keys.ENTER).perform()
                        driver.implicitly_wait(5)
                        driver.find_element_by_xpath('/html/body/div/div[1]/div[1]/div[4]/div[1]/footer/div[1]/div[2]/div/div[2]').send_keys(message)
                        time.sleep(3)
                        buttons.send_keys(Keys.ENTER).perform()
                        driver.implicitly_wait(5)
                    except:
                        pass
                    print('Done')
                    speak("Message Sent")
                    driver.close()
                    break
                elif "multiple contact" in choice:
                    speak("Tell the message to send")
                    message=takecommand().lower()
                    #contacts = pandas.read_excel(THIS_FOLDER+"\\phone.xslx")
                    df=pandas.read_excel("contacts.xlsx") #this file contains the contacts or phone numbers
                    print(df)
                    ka=df['Phone_Number']
                    print(ka[0])
                    path = 'G:\SOFTWARES\chromedriver_win32\chromedriver.exe'
                    driver = webdriver.Chrome(path)
                    buttons = ActionChains(driver)
                    driver.get('https://web.whatsapp.com/')
                    driver.implicitly_wait(20)
                    time.sleep(5)
                    try:
                        for i in range(len(ka)):                    
                            print("i",i)
                            driver.find_element_by_xpath('/html/body/div/div[1]/div[1]/div[3]/div/div[1]/div/label/div/div[2]').send_keys('') 
                            time.sleep(0.4);
                            keyboard.send('ctrl+a')
                            keyboard.send('backspace')
                            keyboard.write(ka[i])
                            keyboard.send('enter');time.sleep(3)
                            keyboard.send('ctrl+a')
                            keyboard.send('backspace')
                            buttons.send_keys(Keys.ENTER).perform()
                            driver.implicitly_wait(5)
                            try:
                                driver.find_element_by_xpath('/html/body/div/div[1]/div[1]/div[4]/div[1]/footer/div[1]/div[2]/div/div[2]').send_keys("");
                                keyboard.write('Hi,Guys')
                                keyboard.send('shift+enter')
                                keyboard.write(message)
                                keyboard.send('shift+enter')
                                keyboard.write('so please ignore this message')
                                keyboard.send('enter');
                                time.sleep(0.4)
                            except:
                                time.sleep(0.4)
                                print("in except inner")
                                driver.implicitly_wait(5)
                    except:
                        pass
                    driver.close()
                    break
                else:
                    speak("Try Again")
                    speak("Single contact or Multiple contact or delayed contact")
                    choice=takecommand().lower()    
        elif "send attach" in query:
            fromadd="panam.beracah@gmail.com"
            to = "panam.beracah@gmail.com"
            msg = MIMEMultipart()
            msg['From'] = fromadd
            msg['To'] = ["panam.beracah@gmail.com","panam.amariah@gmail.com","panam.berach@gmail.com"] 
            msg['Subject'] = "Demo for attachment"
            body = "Demo Body"
            msg.attach(MIMEText(body, 'plain'))
            filename = "data.txt"
            THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
            filename=THIS_FOLDER+"\\"+filename
            attachment = open(filename, "rb")
            p = MIMEBase('application', 'octet-stream')
            p.set_payload((attachment).read())
            encoders.encode_base64(p)
            p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
            msg.attach(p)
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            s.login(fromadd, "Jbsas@333")
            text = msg.as_string()
            s.sendmail(fromadd, to, text)
            s.quit()     
        elif "wish me" in query:
            wishme()
        elif "change voice" in query:
            if voiceses==0:
                speaker.setProperty('voice', voices[1].id)
                voiceses=1
                speak("Changed voice from Male to Female voice")
            else:
                speaker.setProperty('voice', voices[0].id)
                voiceses=0
                speak("Changed voice from Female to Male voice")
        elif "play in youtube" in query:  
            try:                
                speak("what is it you want to search")
                seaa=takecommand().lower()
                sss="https://youtube.com/results?search_query="+seaa
                pywhatkit.playonyt(sss)
                print("Playing...")
            except:
                print("Network Error Occured")

        elif "select all" in query:
            # keyboard.press(key)
            # keyboard.release(key)
            speak("selecting all")
            keyboard.send("ctrl+a")
            #pyautogui.hotkey('ctrlright','A')
        elif "copy" in query:
            speak("Copying")
            keyboard.send("ctrl+c")
            #pyautogui.hotkey('ctrlright','C')
        elif "paste" in query:
            speak("PASTING")
            keyboard.press_and_release('ctrl + v')
            #pyautogui.hotkey('ctrlright','V')
        elif "cut" in query:
            speak("CUTING")
            keyboard.send("ctrl+x")
            #pyautogui.hotkey('ctrlright','X')
        elif "pass" in query:
            speak("PAUSING")       
            keyboard.press_and_release("space")
        elif "play" in query:
            speak("PLAYING")
            keyboard.press_and_release("space")
        elif "meaning to word" in query:
            speak("What is the word")
            probl=takecommand().lower()
            print(probl)
            probl = probl.replace("what is the","")
            probl = probl.replace("jarvis","")
            probl = probl.replace("of","")
            probl = probl.replace("meaning of","")
            result = Diction.meaning(probl)
            speak(f"The Meaning For {probl} is {result}")
        elif "opposite to word" in query:
            speak("What is the word")
            probl=takecommand().lower()
            print(probl)
            probl = probl.replace("what is the","")
            probl = probl.replace("jarvis","")
            probl = probl.replace("of","")
            probl = probl.replace("antonym of","")
            result = Diction.antonym(probl)
            speak(f"The Antonym For {probl} is {result}")   
        elif "full screen" in query:
            keyboard.press_and_release("f")
        elif 'close the tab' in query:
            keyboard.press_and_release('ctrl + w')
        elif 'open new tab' in query:
            keyboard.press_and_release('ctrl + t')
        elif 'open new window' in query:
            keyboard.press_and_release('ctrl + n')
        elif 'history' in query:
            keyboard.press_and_release('ctrl + h')
        elif "escape" in query:
            keyboard.press_and_release('esc')
        elif "alt tab" in query:
            keyboard.press_and_release('alt + tab')
        elif "register speaker" in query:
            record_audio_train()
            train_model()
        elif "change speaker" in query:
            record_audio_test()
            test_model()
        elif "remove all users" in query:
            file = open("start.txt","w")
            file.close()
        elif "play in youtube" in query:  
            try:                
                # it plays a random YouTube
                speak("what is it you want to search")
                seaa=takecommand().lower()
                # video of GeeksforGeeks
                sss="https://youtube.com/results?search_query="+str(seaa)
                pywhatkit.playonyt(sss)
                print("Playing...")
                
            except:
                    
                # printing the error message
                print("Network Error Occured")
        elif "train" in query:
            train_model()
        elif 'type in word' in query:
            speak("what should i write")
            words=takecommand().lower()
            if words !='None' or words!='none':
                keyboard.write(words)
        elif 'type in notepad' in query:
            speak("what should i type")
            words=takecommand().lower()
            if words !='None' or words!='none':
                keyboard.write(words)
        elif "close the word" in query:
            speak("want to save or not")
            words=takecommand().lower()
            if 'yes' in words or 'save' in words:
                speak("give the name of the file")
                saved=takecommand().lower()
                keyboard.press_and_release('ctrl+s')
                keyboard.write(saved)
                keyboard.press_and_release('enter')
                keyboard.press_and_release('alt+F4')
            else:
                keyboard.press_and_release('alt+F4')
                for i in range(5):
                    keyboard.press_and_release('tab')
                keyboard.press_and_release('enter')
        elif 'close the notepad' in query:
            speak("want to save or not")
            words=takecommand().lower()
            if 'yes' in words or 'save' in words:
                speak("give the name of the file")
                saved=takecommand().lower()
                keyboard.press_and_release('ctrl+s')
                keyboard.write(saved)
                keyboard.press_and_release('enter')
                time.sleep(5)
                keyboard.press_and_release('alt+F4')
            else:
                keyboard.press_and_release('alt+F4')
                keyboard.press_and_release('tab')
                keyboard.press_and_release('enter')
        elif 'none' in query or 'None' in query:
            pass
        elif 'open file explorer' in query:
            print("asdsad")
            pyautogui.hotkey('win', 'e')
        elif 'lock the screen' in query:
            print("sdgdl")
            pyautogui.hotkey('win', 'l')
        else:
            speak("The command is not present")
            
