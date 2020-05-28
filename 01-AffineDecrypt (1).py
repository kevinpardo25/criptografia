# --------------------------- Affine Decryption --------------------------- #
# This Python code is for decryption purposes. The algorithm executes a     #
# substitution decryption according to the equation:                        #
# C = (inv(a)*(M + b)) mod (n)                                              #
# Author: Julián Darío Miranda                                              #
# Institution: Pontifical Bolivarian University, Bucaramanga, Colombia      #
# Subject: Information Security Specialization                              #
# ------------------------------------------------------------------------- #

import re, os
from operator import itemgetter
import pickle

dictionary = {0:1, 3:9, 5:21, 7:15, 9:3, 11:19, 15:7, 17:23, 19:11, 21:5, 23:17, 25:25}

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

a = input("Enter the 'a' value: ")
while not a.isdigit(): a = input("Enter a correct 'a' value: ")
a = int(a)
    
b = input("Enter the 'b' value: ")
while not b.isdigit(): b = input("Enter a correct 'b' value: ")
b = int(b)

plain_text = input('Enter the text to be decrypted: ')

replaced_text = normalize_text(plain_text)
len_text = len(replaced_text)

for i in range(0,len_text):
    if replaced_text[i] is not " ":
        #replaced_text = replaced_text[:i] + chr(((a**(-1))*(ord(replaced_text[i])-65) - b)%26 + 65) + replaced_text[i+1:]
        replaced_text = replaced_text[:i] + chr(int((dictionary[a%26])*((ord(replaced_text[i])-65) - b)%26 + 65)) + replaced_text[i+1:]

        
print('Affine decryption result: ' + replaced_text)
