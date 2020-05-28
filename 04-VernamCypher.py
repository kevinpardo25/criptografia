# --------------------------- Vernam Cypher ------------------------------- #
# This Python code is for encrypting purposes. The algorithm executes a     #
# Vernam encryption, considering a key entered by console.                  #
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
    plain_text = re.sub('(?![A-Z])(?![0-9]).', '', plain_text)
    plain_text = re.sub(' +', '', plain_text)
    return plain_text

get_bin = lambda x, n: format(x, 'b').zfill(n)

plain_text = input('Enter the text to be encrypted: ')
plain_text = normalize_text(plain_text)
len_text = len(plain_text)

key = input('Enter the key (text only): ')
key = normalize_text(key)
key = key*(len_text//len(key))
key += key[0:len_text-len(key)]

result = ''

for i in range(0,len_text):
    result += get_bin(ord(plain_text[i])^ord(key[i]),8)

print('Vernam encryption result: ' + hex(int(result, 2))[2:].upper())
