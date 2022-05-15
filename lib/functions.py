from urllib import parse
from datetime import datetime
from bs4 import BeautifulSoup
from .shorteners import *
from .brands import *
from .string_match import *
import re
import ipaddress
import requests
import geoip2.database
import tldextract
import math
from fuzzywuzzy import fuzz, process

PATH = 'lib/files/'


def start_url(url):
    """Split URL into: protocol, host, path, params, query and fragment."""
    if not parse.urlparse(url.strip()).scheme:
        url = 'http://' + url
    protocol, host, path, params, query, fragment = parse.urlparse(url.strip())
    
    subd = re.sub(r'\bwww.\b','',host)
    tldex = tldextract.extract(subd.lower())
    
    result = {
        'url': host + path + params + query + fragment,
        'url2': subd + path + params + query + fragment,
        'subdomain': tldex.subdomain,
        'domain': tldex.domain,
        'protocol': protocol+'://',
        'host': host,
        'path': path,
        'params': params,
        'query': query,
        'fragment': fragment,
        'fullpath': path + params + query + fragment
    }
    return result


def count(text, character):
    """Return the amount of certain character in the text."""
    return text.lower().count(character)


def count_delims(text):
    """Return the number of characters."""
    charact = ['~', '`', '!', '^', '*', '(', ')', '[', ']', '{', '}', '"', "'", ';', ',', '>', '<', '|']
    count = 0
    for i in charact:
        count += text.lower().count(i)
    
    if count > 0:
        return 1
    else:
        return 0
        
        
def other_delims(text):
    """Return the number of characters."""
    charact = ['+', '$', '=', '&', ':', '#', '%']
    count = 0
    for i in charact:
        count += text.lower().count(i)
    
    return count
    
    
def other_delims2(text):
    """Return the number of characters."""
    charact = ['+', '$', '=', '&', ':', '#']
    count = 0
    for i in charact:
        count += text.lower().count(i)
    
    return count
    
    
def count_degits(text):
    """Return the number of digits."""
    count = sum(c.isdigit() for c in text.lower())
    return count
    
    
def count_params(text):
    """Return number of parameters."""
    return len(parse.parse_qs(text))
    
    
def check_tld(text):
    """Check for presence of Top-Level Domains (TLD)."""
    file = open(PATH + 'tlds.txt', 'r')
    pattern = re.compile("[a-zA-Z0-9.]")
    for line in file:
        i = (text.lower().strip()).find(line.strip())
        while i > -1:
            if ((i + len(line) - 1) >= len(text)) or not pattern.match(text[i + len(line) - 1]):
                file.close()
                return 1
            i = text.find(line.strip(), i + 1)
    file.close()
    return 0
    
    
def count_tld(text):
    """Return amount of Top-Level Domains (TLD) present in the URL."""
    file = open(PATH + 'tlds.txt', 'r')
    count = 0
    pattern = re.compile("[a-zA-Z0-9.]")
    for line in file:
        i = (text.lower().strip()).find(line.strip())
        while i > -1:
            if ((i + len(line) - 1) >= len(text)) or not pattern.match(text[i + len(line) - 1]):
                count += 1
            i = text.find(line.strip(), i + 1)
    file.close()
    
    if count > 1:
        return 1
    else:
        return 0


def length(text):
    """Return the length of a string."""
    return len(text)
    
    
def avg_large_count(string):
    avg = 0.0
    largest = 0
    string = string.strip()
    tokens = re.split('\W+', string)
    if string == "":
        return [0,0,0]
    else:
        if "" in tokens:
            count = len(tokens)-1
        else:
            count = len(tokens)
        for token1 in tokens:
            avg += len(token1)
            if largest < len(token1):
                largest = len(token1)
        avg /= count
    return int(round(count)), int(round(avg)), int(round(largest)) #average_len, count and length_of_largest token
    
    
def valid_ip(host):
    """Return if the domain has a valid IP format (IPv4 or IPv6)."""
    try:
        ipaddress.ip_address(host)
        return 1
    except Exception:
        return 0


def valid_email(text):
    """Return if there is an email in the text."""
    if re.findall(r'[\w\.-]+@[\w\.-]+', text):
        return 1
    else:
        return 0
      

def is_https(host):
    if "https" in host:
        return 0 # 'https' present in domain, legitimate
    else:
        return 1 # 'https' not present in domain, phishing
    
    
def having_protocol(text):
    """Return the number of http and https text in url."""
    htp = ['http', 'www', 'h_t_t_p']
    count = 0
    for i in htp:
        count += text.lower().count(i)
     
    if count > 0:
        return 1
    else:
        return 0
    
    
def check_suspwords(text):
    
    url = text.lower()
    tokens_words=re.split('\W+',url)       #Extract bag of words 
    
    sec_sen_words=['server', 'client', 'confirm', 'account', 'banking', 'secure', 'ebayisapi', 'webscr', 'login', 'signin', 'update', 'click', 'password', 'verify', 'lucky', 'bonus', 'suspend', 'paypal', 'wordpress', 'includes', 'admin', 'alibaba', 'myaccount', 'dropbox', 'themes', 'plugins', 'logout', 'signout', 'submit', 'limited', 'securewebsession', 'redirectme', 'recovery', 'secured', 'refund', 'webservis', 'giveaway', 'webspace', 'servico', 'webnode', 'dispute', 'review', 'browser', 'billing', 'temporary', 'restore', 'verification', 'required', 'resolution', '000webhostapp', 'webhostapp', 'wp', 'content', 'site', 'images', 'js', 'css', 'view' ]
    
    cnt=0
    for ele in sec_sen_words:
        if(ele in tokens_words):
            cnt+=1;
            
    if cnt > 0:
        return 1
    else:
        return 0
    

def get_top(dom):
    dom = dom.split('.')
    dom = re.split('\W+|_', dom[-1])
    if dom[0].isdigit():
        return ""
    else:
        #return len(dom[0])
        return dom[0]
        
        
def slash_pos(webpage):
    pos = webpage.rfind('//')
    #return pos+1
    '''if pos+1 > 6:
        return 1 #redirection present
    else:
        return 0 #redirection not present'''
    if pos > 7:
        return 1 #redirection present
    else:
        return 0 #redirection not present
        

# 8. Checking for Shortening Services in URL (Tiny_URL)
def tinyURL(url):
    match=re.search(shortening_services,url.lower())
    if match:
        return 1
    else:
        return 0
        
        
def extract_extension(text):
    """Return file extension name."""
    file = open(PATH + 'extensions.txt', 'r')
    pattern = re.compile("[a-zA-Z0-9.]")
    for extension in file:
        i = (text.lower().strip()).find(extension.strip())
        while i > -1:
            if ((i + len(extension) - 1) >= len(text)) or not pattern.match(text[i + len(extension) - 1]):
                file.close()
                return 0
            i = text.find(extension.strip(), i + 1)
    file.close()
    return 1
        

def check_brand(url):
    """Check if the domain has a brand name."""
    url = url.lower()
    m = tfidf_match5([url], brands)
    m1 = process.extractOne(url,brands, scorer=fuzz.token_set_ratio)
    if m < 11 or m1[1] > 89:
        return 1
    elif m < 30 and m1[1] > 70:
        return 1
    else:
        return 0
  
  
#Shannon’s entropy
def entropy(url):
    string = url.lower()
    prob = [float(string.count(c)) / len(string) for c in dict.fromkeys(list(string))]
    entropy = - sum([(p * math.log(p) / math.log(2.0)) for p in prob])
    cnt = int(round(entropy*10))
    return cnt
    
    
#Checking for Prefix or Suffix Separated by (-) in the Domain (Prefix/Suffix)
def prefixSuffix(url):
    if '-' in parse.urlparse(url).netloc:
        return 1            # phishing
    else:
        return 0            # legitimate


def read_file(archive):
    """Read the file with the URLs."""
    with open(archive, 'r') as f:
        urls = ([line.rstrip() for line in f])
        return urls
