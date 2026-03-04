import cloudscraper
import random
import json
import time
import os
import requests
from concurrent.futures import ThreadPoolExecutor

BOLD = '\033[1m'
R = '\033[91m'
G = '\033[92m'
Y = '\033[93m'
D = '\033[0m'
C = '\033[96m'

# Cloudflare bypass করার জন্য scraper তৈরি করা
scraper = cloudscraper.create_scraper(
    browser={
        'browser': 'chrome',
        'platform': 'android',
        'desktop': False
    }
)

def logo():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f'{BOLD}{C}\n       _____ __      ___                \n      / __(_) /__   / _ \\__ ____ _  ___ \n     / _// / / -_) / // / // /  \' \\/ _ \\\n    /_/ /_/_/\\__/ /____/\\_,_/_/_/_/ .__/\n                                 /_/    \n\n            FB File Maker V-2.0 (Anti-Block)\n {D}')

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
            url = 'https://baji999.net/api/wv/v1/user/registerPreCheck'
            
            headers = {
                'Accept': 'application/json, text/plain, */*',
                'Content-Type': 'application/json',
                'Origin': 'https://baji999.net',
                'Referer': 'https://baji999.net/bd/en/register',
                'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36'
            }

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

            # Cloudscraper ব্যবহার করে রিকোয়েস্ট পাঠানো
            response = scraper.post(url, json=json_data, headers=headers, timeout=15)
            
            if response.status_code == 403:
                print(f'{R} [403] Cloudflare Blocked! Sleeping 20s...{D}')
                time.sleep(20)
                return False

            data = response.json()
            
            if data.get('status') == 'F0003':
                return True
            elif data.get('status') == 'S0001':
                print(f'{R} [RATE LIMIT] Wait 30 seconds...{D}')
                time.sleep(30)
                continue
            else:
                return False

        except Exception as e:
            # যদি JSON না পেয়ে HTML (Cloudflare page) পায়, তবে এখানে এরর হ্যান্ডেল হবে
            time.sleep(5)
            return False

def check_username(username):
    uname = username.replace(' ', '').split('|')[0]
    if checker(uname):
        print(f'{BOLD}{G} [VALID] {uname}{D}')
        with open('.uids.txt', 'a') as file:
            file.write(username + '\n')
    else:
        # অপশনাল: ইনভ্যালিড গুলো দেখতে চাইলে এখানে প্রিন্ট দিতে পারেন
        pass

def main():
    logo()
    print(f'{BOLD}{Y} ENTER NAMES BY USING COMMA (,) Eg : (Sadek,Tanvir, Sagor) Etc{D}\n')
    names = input(f'{BOLD}{G} ENTER NAMES : {D}')
    start = int(input(f'{BOLD}{Y} START : '))
    end = int(input(f'{BOLD}{Y} END : '))
    
    print(f'\n{G} [1] LOW SPEED (Safe)\n{Y} [2] MEDIUM SPEED\n{R} [3] HIGH SPEED (Risky){D}\n')
    speed = int(input(f'{C} CHOOSE : {D}'))
    
    spd_map = {1: 2, 2: 5, 3: 10}
    spd = spd_map.get(speed, 2)

    clear_file()
    usernames = username_gen(names, start, end)
    random.shuffle(usernames)

    print(f'\n{BOLD}{G} TOTAL USERNAMES : {len(usernames)} {D}')
    print(f'{BOLD}{G} ----------------------------------------{D}')
    
    with ThreadPoolExecutor(max_workers=spd) as executor:
        executor.map(check_username, usernames)
        
    print(f'{BOLD}{G} ---------------------------------------{D}')
    if os.path.exists('.uids.txt'):
        total = sum(1 for _ in open('.uids.txt'))
    else:
        total = 0
    print(f'\n{BOLD}{G} TOTAL {Y}{total}{G} VALID IDS FOUND{D}\n')

def clear_file():
    open('.uids.txt', 'w').close()

def setup_username():
    if not os.path.exists('.name.txt'):
        uname = input(f'{Y} ENTER TELEGRAM USERNAME: {D}').strip()
        with open('.name.txt', 'w') as f:
            f.write(uname)

if __name__ == '__main__':
    setup_username()
    main()
