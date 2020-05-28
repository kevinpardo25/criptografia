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

def vigenere_decrypt(cryptogram, key):
    text = cryptogram
    len_cryptogram = len(text)
    len_key = len(key)
    for i in range(0,len_cryptogram):
        if cryptogram[i] is not " ":
            b = ord(key[i%len_key])-65
            text = text[:i] + chr(((ord(text[i])-65) - b)%26 + 65) + text[i+1:]
    return text

def caesar_decrypt(cryptogram, b):
    len_cryptogram = len(cryptogram)
    for i in range(0,len_cryptogram):
        cryptogram = cryptogram[:i] + chr(((ord(cryptogram[i])-65) - b)%26 + 65) + cryptogram[i+1:]
    return cryptogram

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

# IC calculation
N = sum(word_dict.values())
IC = 0

for character in word_dict:
    IC += word_dict[character]*(word_dict[character]-1)
IC /= (N*(N-1))
IC -= 0.0032

# Subcryptograms calculation
subcryptograms = {}
top_divisors = []

print('\n----------- Top divisors and ocurrences ----------')
print('Divisor\tOcurrences')
for i in divisors:
    if int(divisors[i]) >= float(len(number_lst)/2):
        top_divisors.append(i)
        print(str(i) + '\t' + str(divisors[i]))
        subcryptograms[i] = []
        for ii in range(0,i):
            subcryptograms[i].append(cryptogram[ii::i])
print('\n--------- Chars ocurrences in cryptogram ---------')
print('Char\tOcurrences')
for i in word_dict:
    print(i + '\t' + str(word_dict[i]))

# Get length of final key
maxim = -1
top_divisors = []
for key in divisors:
    if divisors[key] > maxim:
        top_divisors = []
        maxim = divisors[key]
        top_divisors.append(key)
    elif divisors[key] == maxim:
        top_divisors.append(key)
maxim = max(top_divisors)

print('\n-------------------- IC value --------------------')
print('IC value: ' + str(IC) + ' - Most probable length key: ' + str(maxim))

# Vigenère decryption and IF value calculation per subcryptogram
IFs_subcryptograms = []
print('\n----- Subcryptograms decryption using one-lenght key per Subcryptogram ------')
print('char',end='\t')
for i in range(0,len(subcryptograms[maxim])):
    print('s'+str(i+1),end='\t')
    IFs_subcryptograms.append([])
for char in range(0,26):
    print()
    print(chr(char+65),end='\t')
    for s in range(0,len(subcryptograms[maxim])):
        IF_value = get_IF(letters_count(caesar_decrypt(subcryptograms[maxim][s], char)))
        print(str(IF_value),end='\t')
        IFs_subcryptograms[s].append(IF_value)

# Get max IF values for each subcryptogram to find the total key
subc = []
all_posible_keys = []
for IFs in IFs_subcryptograms:
    subc.append([chr(i+65) for i,val in enumerate(IFs) if val==max(IFs)])

# Get all combinations of posible keys
combinations = list(itertools.product(*subc))
for combination in combinations:
    all_posible_keys.append(''.join(combination))

# Print cryptogram decryption with all combinations of key
print('\n----- Possible mesagges according to key variations ------')
for key in all_posible_keys:
    text = vigenere_decrypt(cryptogram, key)
    print(key + ': ' + text[0:30])
