import requests
import random
import http.client
import json
import time
import os
from concurrent.futures import ThreadPoolExecutor

# Colors
BOLD = '\033[1m'
R = '\033[91m'
G = '\033[92m'
Y = '\033[93m'
D = '\033[0m'
C = '\033[96m'

def logo():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f'{BOLD}{C}\n       _____ __      ___                \n      / __(_) /__   / _ \\__ ____ _  ___ \n     / _// / / -_) / // / // /  \' \\/ _ \\\n    /_/ /_/_/\\__/ /____/\\_,_/_/_/_/ .__/\n                                 /_/    \n\n            FB File Maker V-2.1 (Anti-Block)\n {D}')

def get_random_ua():
    # বিভিন্ন ডিভাইসের ব্রাউজার লিস্ট যাতে সার্ভার বট ধরতে না পারে
    ua_list = [
        'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Version/17.0 Safari/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/119.0.6045.163 Mobile/15E148 Safari/604.1'
    ]
    return random.choice(ua_list)

def username_gen(names, start, end):
    usernames = []
    for name in names.split(','):
        for num in range(start, end + 1):
            username = f'{name.strip().lower()}{num} | {name.capitalize()}'
            usernames.append(username)
    return usernames

def checker(uname):
    while True:
        try:
            # রিকোয়েস্টের মাঝে বিরতি দেওয়া যাতে এপিআই ব্লক না হয়
            time.sleep(random.uniform(1.0, 2.5)) 
            
            headers = {
                'User-Agent': get_random_ua(),
                'Content-Type': 'application/json',
                'Accept': 'application/json, text/plain, */*',
                'Referer': 'https://bj88.live/bd/en/register',
                'Origin': 'https://bj88.live'
            }
            
            # ডেটা কিছুটা র‍্যান্ডমাইজ করা হচ্ছে
            json_data = {
                'languageTypeId': 1,
                'currencyTypeId': 8,
                'userId': uname,
                'phone': f'1347{random.randint(100000, 999999)}', 
                'friendReferrerCode': '',
                'captcha': '',
                'callingCode': '880',
                'registerTypeId': 0,
                'random': str(random.randint(1000, 9999))
            }
            
            # সরাসরি লাইভ এপিআই এন্ডপয়েন্ট ব্যবহার করা
            response = requests.post(
                'https://bj88.live/api/wv/v1/user/registerPreCheck', 
                json=json_data, 
                headers=headers, 
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'F0003': # ইউজার এভেইলএবল বা নির্দিষ্ট স্ট্যাটাস
                    return True
                elif data.get('status') == 'S0001': # রেট লিমিট বা ব্লক মেসেজ
                    print(f'{R} [!] RATE LIMIT! WAITING 40 SEC...{D}')
                    time.sleep(40)
                    continue
                else:
                    return False
            else:
                time.sleep(10)
                continue

        except Exception:
            time.sleep(5)
            continue

def check_username(username):
    uname = username.replace(' ', '').split('|')[0]
    if checker(uname):
        print(f'{BOLD}{G} [VALID] {uname}{D}')
        with open('.uids.txt', 'a') as file:
            file.write(username + '\n')

def main():
    logo()
    print(f'{BOLD}{Y} ENTER NAMES BY USING COMMA (,) Eg: Sadek,Tanvir{D}\n')
    names = input(f'{BOLD}{G} ENTER NAMES : {D}')
    start = int(input(f'{BOLD}{Y} START NUMBER : '))
    end = int(input(f'{BOLD}{Y} END NUMBER : '))
    
    print(f'\n{G} [1] LOW (Safe)\n{Y} [2] MEDIUM\n{R} [3] HIGH (Risk){D}\n')
    speed = int(input(f'{C} CHOOSE SPEED : {D}'))
    
    # স্পিড অনুযায়ী থ্রেড সংখ্যা নিয়ন্ত্রণ
    if speed == 1: spd = 2
    elif speed == 2: spd = 5
    else: spd = 8

    clear_file()
    usernames = username_gen(names, start, end)
    random.shuffle(usernames)
    
    print(f'\n{BOLD}{G} TOTAL USERNAMES : {len(usernames)} {D}')
    print(f'{BOLD}{G} ----------------------------------------{D}')
    
    with ThreadPoolExecutor(max_workers=spd) as executor:
        executor.map(check_username, usernames)
        
    print(f'{BOLD}{G} ---------------------------------------{D}')
    try:
        total = sum(1 for _ in open('.uids.txt'))
    except FileNotFoundError:
        total = 0
    print(f'\n{BOLD}{G} PROCESS FINISHED. TOTAL FOUND: {Y}{total}{D}\n')

def clear_file():
    open('.uids.txt', 'w').close()

def setup_username():
    if not os.path.exists('.name.txt'):
        uname = input(f'{Y} ENTER TELEGRAM USERNAME: {D}').strip()
        with open('.name.txt', 'w') as f:
            f.write(uname if uname.startswith('@') else '@' + uname)

if __name__ == '__main__':
    setup_username()
    main()
