# --------------------------- Vernam Decrypt ------------------------------ #
# This Python code is for decryption purposes. The algorithm executes a     #
# Vernam decryption, considering a key entered by console.                  #
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

flag = True
get_bin = lambda x, n: format(x, 'b').zfill(n)

cryptogram = input('Enter the text to be dercrypted (base hexadecimal): ')

while flag:
    try:
        int(cryptogram,16)
        flag = False
    except:
        cryptogram = input('Enter a valid hexadecimal text to be dercrypted: ')
        flag = True
        
len_text = len(cryptogram)
if len_text%2 == 1:
    cryptogram = '0' + cryptogram
    len_text += 1

key = input('Enter the key (text only): ')
key = normalize_text(key)
key = key*((len_text//2)//len(key))
key += key[0:(len_text//2)-len(key)]
len_key = len(key)

result = ''

for i in range(0,len_key):
    result += chr(int(cryptogram[2*i]+cryptogram[2*i+1],16)^ord(key[i]))

print('Vernam encryption result: ' + result.upper())
