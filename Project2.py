import sys
import re
import requests
from bs4 import BeautifulSoup

# get both the urls from command line
if len(sys.argv) < 3:
    print("give proper input:  python project.py url1 url2")
    sys.exit()

url1 = sys.argv[1]
url2 = sys.argv[2]

# get text from webpage
def load_data(url):
    try:
        body_data = requests.get(url)
        soup = BeautifulSoup(body_data.content, "html.parser")
        
        # remove script and style
        for tag in soup(["script", "style"]):
            tag.extract()
        
        data = soup.get_text()
        return data
    except:
        return ""

# split into words: 
def split_words(body_data):
    body_data = body_data.lower()
    words = re.findall(r'[a-z0-9]+', body_data)
    return words

# count each word
def count_occur(words):
    frq= {}
    for w in words:
        if w in frq:
            frq[w] = frq[w] + 1
        else:
            frq[w] = 1
    return frq

# hash function
def hash_func(word):
    p = 53
    m = 2**64
    ans = 0
    pow = 1
    
    for c in word:
        ans = (ans + ord(c) * pow) % m
        pow = (pow * p) % m
    
    return ans

# create fingerprints:
def create_fingerprint(freq):
    lst = [0] * 64
    
    for word, count in freq.items():
        h = hash_func(word)
        
        for i in range(64):
            bit = (h >> i) & 1
            if bit == 1:
                lst[i] = lst[i] + count
            else:
                lst[i] = lst[i] - count
    
    fing_print = 0
    for i in range(64):
        if lst[i] > 0:
            fing_print= fing_print | (1 << i)
    
    return fing_print

# compare fingerprints of two web pages : 
def compare_fingerprints(fing1, fing2):
    different_bits = fing1 ^ fing2
    same = 64 - bin(different_bits).count('1')
    return same

# main

data1 = load_data(url1)
data2 = load_data(url2)
word_lst1 = split_words(data1)
word_lst2= split_words(data2)
freq1 = count_occur(word_lst1)
freq2 = count_occur(word_lst2)
fingerprint1 = create_fingerprint(freq1)
fingerprint2 = create_fingerprint(freq2)
ans = compare_fingerprints(fingerprint1, fingerprint2)
print("Common bits:", ans)


