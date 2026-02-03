import requests
import random
import http.client
import json
import time
import os
from concurrent.futures import ThreadPoolExecutor

BOLD = '[1m'
R = '[91m'
G = '[92m'
Y = '[93m'
D = '[0m'
C = '[96m'

def logo():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f'{BOLD}{C}\n       _____ __      ___                \n      / __(_) /__   / _ \\__ ____ _  ___ \n     / _// / / -_) / // / // /  \' \\/ _ \\\n    /_/ /_/_/\\__/ /____/\\_,_/_/_/_/ .__/\n                                 /_/    \n\n            FB File Maker V-2.0\n {D}')

def username_gen(names, start, end):
    usernames = []
    for name in names.split(','):
        for num in range(start, end + 1):
            username = f'{name.strip().lower()}{num} | {name.capitalize()}'
            usernames.append(username)
    return usernames

def checker(uname):
    try:
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:79.0) Gecko/20100101 Firefox/79.0',
            'Mozilla/5.0 (X11; Linux i686; rv:79.0) Gecko/20100101 Firefox/79.0',
            'Mozilla/5.0 (Linux x86_64; rv:79.0) Gecko/20100101 Firefox/79.0',
            'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:79.0) Gecko/20100101 Firefox/79.0',
            'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:79.0) Gecko/20100101 Firefox/79.0',
            'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:79.0) Gecko/20100101 Firefox/79.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36 OPR/70.0.3728.95',
            'Mozilla/5.0 (Windows NT 10.0; WOW64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36 OPR/70.0.3728.95',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36 OPR/70.0.3728.95',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36 OPR/70.0.3728.95',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0',
            'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
            'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
            'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; rv:11.0) like Gecko',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
        ]
        
        headers = {
            'sec-ch-ua': '\"Chromium\";v=\"139\", \"Not;A=Brand\";v=\"99\"',
            'sec-ch-ua-mobile': '?1',
            'User-Agent': random.choice(user_agents),
            'sec-ch-ua-arch': '\"\"',
            'Content-Type': 'application/json',
            'sec-ch-ua-full-version': '\"139.0.7339.0\"',
            'Accept': 'application/json, text/plain, */*',
            'sec-ch-ua-platform-version': '\"14.0.0\"',
            'Referer': 'https://baji999.net/bd/en/register',
            'sec-ch-ua-full-version-list': '\"Chromium\";v=\"139.0.7339.0\", \"Not;A=Brand\";v=\"99.0.0.0\"',
            'sec-ch-ua-bitness': '\"\"',
            'sec-ch-ua-model': '\"LE2101\"',
            'sec-ch-ua-platform': '\"Android\"'
        }
        
        url = 'https://baji999.net/api/wv/v1/user/registerPreCheck'
        json_data = {
            'languageTypeId': 1,
            'currencyTypeId': 8,
            'userId': uname,
            'phone': '1347054625',
            'friendReferrerCode': '',
            'captcha': '',
            'callingCode': '880',
            'registerTypeId': 0,
            'random': str(random.randint(1000, 9999))
        }
        
        conn = http.client.HTTPSConnection('baji999.net')
        conn.request('POST', '/api/wv/v1/user/registerPreCheck', json.dumps(json_data), headers)
        response = conn.getresponse()
        data = json.loads(response.read())
        
        if data['status'] == 'F0003':
            return True
        if data['status'] == 'S0001':
            print(f'{R} [RATE LIMIT] PLEASE TURN OFF DATA FOR 10 SEC...!{D}')
            time.sleep(30)
            return False
            
    except Exception as e:
        time.sleep(10)
        print(f'{R} ERROR >> {e}{D}')
        return False
        
    return False

def check_username(username):
    uname = username.replace(' ', '').split('|')[0]
    if checker(uname):
        print(f'{BOLD}{G} [FB] {uname}{D}')
        with open('.uids.txt', 'a') as file:
            file.write(username + '\n')

def main():
    logo()
    print(f'{BOLD}{Y} ENTER NAMES BY USING COMMA (,) Eg : (Sadek,Tanvir, Sagor) Etc{D}\n')
    names = input(f'{BOLD}{G} ENTER NAMES : {D}')
    print('')
    start = int(input(f'{BOLD}{Y} START (Eg : 1 ) : '))
    end = int(input(f'{BOLD}{Y} END (Eg : 10000 ) : '))
    print('')
    print(f'{G} [1] LOW SPEED')
    print(f'{Y} [2] MEDIUM SPEED')
    print(f'{R} [3] HIGH SPEED{D}\n')
    print('')
    speed = int(input(f'{C} CHOOSE : {D}'))
    if speed == 1:
        spd = 3
    elif speed == 2:
        spd = 6
    elif speed == 3:
        spd = 12
    else:
        spd = 3
    clear_file()
    usernames = username_gen(names, start, end)
    random.shuffle(usernames)
    print('')
    print(f'{BOLD}{G} TOTAL USERNAMES : {len(usernames)} {D}')
    print(f'{BOLD}{G} ----------------------------------------{D}')
    with ThreadPoolExecutor(max_workers=spd) as executor:
        executor.map(check_username, usernames)
    print(f'{BOLD}{G} ---------------------------------------{D}')
    total = sum((1 for _ in open('.uids.txt')))
    print(f'\n{BOLD}{G} TOTAL{Y}{total}{G} VALID FB IDS FOUND{D}\n\n')

def clear_file():
    with open('.uids.txt', 'w') as file:
        pass

def switch():
    s = requests.get('https://raw.githubusercontent.com/havecode17/dg/refs/heads/main/switch').text
    if 'ON' in s:
        return
    print(f'\n{BOLD}{R} THIS TOOL HAS DISABLED BY ADMIN!{D}')
    exit(0)

def setup_username():
    try:
        with open('.name.txt') as f:
            if f.read().strip():
                return
    except FileNotFoundError:
        username = input(f'{Y} ENTER TELEGRAM USERNAME: {D}').strip()
        if not username.startswith('@'):
            username = '@' + username
        with open('.name.txt', 'w') as f:
            f.write(username)

if __name__ == '__main__':
    setup_username()
    switch()
    main()
