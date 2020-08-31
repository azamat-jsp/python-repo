from libs.wav import setLogFileFromVoice
from libs.database import db_connect
import os

phoneInput = input("Номер телефона? ")
fileInput = input("Название файла?")
dbInput = input("Запись в базу? (Y or N) ")
setLogFileFromVoice(phoneInput, fileInput, dbInput)