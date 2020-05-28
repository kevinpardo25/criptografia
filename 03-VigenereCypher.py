# --------------------------- Vigenère Cypher ----------------------------- #
# This Python code is for encrypting purposes. The algorithm executes a     #
# Vigènere encryption, considering a key entered by console.                #
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

key = input('Enter the key (text only): ')
key = normalize_text(key)
len_key = len(key)

plain_text = input('Enter the text to be encrypted: ')
plain_text = normalize_text(plain_text)
len_text = len(plain_text)
replaced_text = plain_text

for i in range(0,len_text):
    b = ord(key[i%len_key])-65
    replaced_text = replaced_text[:i] + chr(((ord(replaced_text[i])-65) + b)%26 + 65) + replaced_text[i+1:]

print('Vigenère encryption result: ' + replaced_text)
