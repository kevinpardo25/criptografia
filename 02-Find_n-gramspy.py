# --------------------------- Kasiski Method ------------------------------ #
# This Python code is for cryptanalysis purposes. The algorithm executes a  #
# Kasiski method for cryptoanalysis                                         #
# Author: Julián Darío Miranda                                              #
# Institution: Pontifical Bolivarian University, Bucaramanga, Colombia      #
# Subject: Information Security Specialization                              #
# ------------------------------------------------------------------------- #

from operator import itemgetter
import re
import itertools

# ---------------------------------- Methods ------------------------------ #

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

def letters_count(cryptogram):
    word_dict = {}
    for char in cryptogram:
        if char in word_dict:
            word_dict[char] = word_dict[char] + 1;
        else:
            word_dict[char] = 1;

    word_dict.pop(' ', None)
    word_dict.pop('\n', None)

    return sorted(word_dict.items(), key=itemgetter(1), reverse=True)

def dictionary_toString(dictionary_diff, MAXLEN):
    print('n-gram' + ' '*(MAXLEN-len('n-gram')+1)+'\t' + 'Distance')
    for key in dictionary_diff:
        print(key, end=' '*(MAXLEN-len(key)+1)+'\t')
        print(dictionary_diff[key])

def get_IF(freq_dict):      
    first_five_letters = ['E', 'A', 'O' , 'S' , 'N' , 'R']
    last_five_letters = ['F', 'J', 'Z' , 'X' , 'K' , 'W']
    IF = 0
    for i in range(0, 5):
        if freq_dict[i][0] in first_five_letters:
            IF += 1
    for i in range(-1, -6):
        if freq_dict[i][0] in last_five_letters:
            IF += 1
    return IF

# ---------------------------------- Program ------------------------------ #

# Cryptogram input
cryptogram = normalize_text(input('Enter the cryptogram: '))

# Letters count
word_lst = letters_count(cryptogram)
word_dict = dict(word_lst)

# n-grams occurrences count
dictionary_diff={}
number_lst = []
divisors = {}
MINLEN=3
MAXLEN = 10
MINCNT = 2
for sublen in range(MINLEN,MAXLEN):
    for i in range(0,len(cryptogram)-sublen):
        sub = cryptogram[i:i+sublen]
        cnt = [m.start() for m in re.finditer(sub, cryptogram)]
        cnt = [x - cnt[i - 1] for i, x in enumerate(cnt)][1:]
        if len(cnt) >= MINCNT-1 and sub not in dictionary_diff:
            dictionary_diff[sub] = cnt
            for number in cnt:
                if number not in number_lst:
                    number_lst.append(number)

for number in number_lst:
    for i in range(2,int(number/2)+1):
        if number%i==0 and i not in divisors:
            divisors[i] = 1
        elif number%i==0:
            divisors[i] += 1

print('\n-------- n-grams ocurrences and distances --------')
dictionary_toString(dictionary_diff,MAXLEN)
divisors = dict(sorted(divisors.items(), key=itemgetter(1), reverse=True))
