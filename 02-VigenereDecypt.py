# ------------------------ Viegenère Decryption --------------------------- #
# This Python code is for decryption purposes. The algorithm executes a     #
# Vigènere decryption, considering a key entered by console.                #
# Author: Julián Darío Miranda                                              #
# Institution: Pontifical Bolivarian University, Bucaramanga, Colombia      #
# Subject: Information Security Specialization                              #
# ------------------------------------------------------------------------- #

import re, os
from operator import itemgetter
import pickle

def normalize_text(plain_text):
    plain_text = plain_text.upper()
    plain_text = plain_text.replace('Á', 'A')
    plain_text = plain_text.replace('É', 'E')
    plain_text = plain_text.replace('Í', 'I')
    plain_text = plain_text.replace('Ó', 'O')
    plain_text = plain_text.replace('Ú', 'U')
    plain_text = re.sub('(?![A-Z]).', '', plain_text)
    plain_text = re.sub(' +', '', plain_text)
    return plain_text

def decrypt(cryptogram, key):
    text = cryptogram
    len_cryptogram = len(text)
    len_key = len(key)
    for i in range(0,len_cryptogram):
        if cryptogram[i] is not " ":
            b = ord(key[i%len_key])-65
            text = text[:i] + chr(((ord(text[i])-65) - b)%26 + 65) + text[i+1:]
    return text

key = input('Enter the key (text only): ')
cryptogram = input('Enter the text to be decrypted: ')

print('Vigenère decryption result: ' + decrypt(normalize_text(cryptogram),normalize_text(key)))


