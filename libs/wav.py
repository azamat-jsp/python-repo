import os
from shutil import copyfile
from tinkoff_voicekit_client import ClientSTT
from libs.validation import checkEmpty
from libs.database import db_connect
from settings import envInit
import datetime
import uuid
import logging
import wave
import contextlib
import re

envInit()
logging.basicConfig(filename='./logs/voice.log',level=logging.DEBUG)

API_KEY = os.getenv("API_KEY", '')
SECRET_KEY = os.getenv("SECRET_KEY", '')
client = ClientSTT(API_KEY, SECRET_KEY)

audio_config = {
    "encoding": "LINEAR16",
    "sample_rate_hertz": 8000,
    "num_channels": 1
}

def checkNegAndPosWord(response):
    txt = response[0]["transcript"]
    if re.findall("нет", txt) or re.findall("неудобно", txt):
        return 0.2
    else: 
        return 1

def recognitionAO(response):
    txt = response[0]["transcript"]
    res = re.findall("автоответчик", txt)
    if(res):
      return 0.2
    else:
        return 1

def checkDbSet(inputVal):
    if(inputVal.upper() == "Y"):
        return True
    else : return False

def getDuration(file):
    try:
        with contextlib.closing(wave.open(file,'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            duration = frames / float(rate)
            return duration
    except:
        return False

def checkWavFileExist(file):
    fileExists = os.path.exists("voices/" + file)
    return fileExists


def setLogFileFromVoice(phoneInput, fileInput, dbInput):
    checkEmpty(phoneInput, 'phoneInput')
    checkEmpty(fileInput, 'fileInput')
    try:
        if(checkWavFileExist(fileInput)):
            fileName = "copy_" + fileInput
            path = "voices/temp/"
            copyfile("voices/" + fileInput, path + fileName)
            duration = getDuration(path + fileName)
            response = client.recognize(path + fileName, audio_config)
            ao = recognitionAO(response[0]["alternatives"])
            checkWord = checkNegAndPosWord(response[0]["alternatives"])
            alternatives = response[0]["alternatives"]
            start_time = response[0]["start_time"]
            end_time = response[0]["end_time"]
            date = datetime.datetime.now().strftime("%x")
            time = datetime.datetime.now().strftime("%X")
            dbSet = checkDbSet(dbInput)
            result = {
                "date" : date,
                "time" : time,
                "uuid" :  uuid.uuid1().hex,
                "duration" :  duration,
                "dbSet" : dbSet,
                "ckeckAO" : ao,
                "checkWord" : checkWord,
                "phone" : phoneInput,
            }
            logging.info(result)
            print('Запись сохранена в логах')
            if(dbSet):
                db_connect(result)
        else: print('файл не найден')
    except Exception as error :
        logging.error(error)
        print(error)
    finally:
        os.remove(path + fileName)
        print("Файл удален")

