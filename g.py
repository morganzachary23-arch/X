import requests
import random
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
    print(f'{BOLD}{C}\n       _____ __      ___                \n      / __(_) /__   / _ \\__ ____ _  ___ \n     / _// / / -_) / // / // /  \' \\/ _ \\\n    /_/ /_/_/\\__/ /____/\\_,_/_/_/_/ .__/\n                                 /_/    \n\n            FB File Maker V-2.0 (Fixed)\n {D}')

def username_gen(names, start, end):
    usernames = []
    for name in names.split(','):
        for num in range(start, end + 1):
            username = f'{name.strip().lower()}{num} | {name.capitalize()}'
            usernames.append(username)
    return usernames

def get_headers():
    # প্রতিবার আলাদা ইউজার এজেন্ট ব্যবহার করলে ব্লক হওয়ার ঝুঁকি কমে
    ua_list = [
        'Mozilla/5.0 (Linux; Android 10; SM-G960F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1'
    ]
    return {
        'User-Agent': random.choice(ua_list),
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json',
        'Origin': 'https://baji999.net',
        'Referer': 'https://baji999.net/bd/en/register'
    }

def checker(uname):
    url = 'https://baji999.net/api/wv/v1/user/registerPreCheck'
    json_data = {
        'languageTypeId': 1, 
        'currencyTypeId': 8, 
        'userId': uname, 
        'phone': str(random.randint(1600000000, 1999999999)), 
        'friendReferrerCode': '', 
        'captcha': '', 
        'callingCode': '880', 
        'registerTypeId': 0, 
        'random': str(random.randint(1000, 9999))
    }
    
    try:
        # requests ব্যবহার করা হয়েছে এবং timeout দেওয়া হয়েছে যাতে stuck না হয়
        response = requests.post(url, json=json_data, headers=get_headers(), timeout=10)
        
        # রেসপন্স খালি কিনা চেক করা
        if not response.text:
            return False
            
        data = response.json()
        
        if data.get('status') == 'F0003':
            return True
        if data.get('status') == 'S0001':
            print(f'{R} [RATE LIMIT] SLEEPING 15 SEC...{D}')
            time.sleep(15)
            return False
            
    except json.JSONDecodeError:
        # যদি সার্ভার JSON না পাঠিয়ে HTML এরর পাঠায়
        return False
    except Exception:
        return False
    return False

def check_username(username):
    uname = username.replace(' ', '').split('|')[0]
    if checker(uname):
        print(f'{BOLD}{G} [FB-OK] {uname}{D}')
        with open('.uids.txt', 'a') as file:
            file.write(username + '\n')

def main():
    logo()
    print(f'{BOLD}{Y} ENTER NAMES BY USING COMMA (,) Eg : (Sadek,Tanvir){D}\n')
    names = input(f'{BOLD}{G} ENTER NAMES : {D}')
    start = int(input(f'{BOLD}{Y} START : {D}'))
    end = int(input(f'{BOLD}{Y} END : {D}'))
    
    print(f'\n{G} [1] LOW SPEED\n{Y} [2] MEDIUM SPEED\n{R} [3] HIGH SPEED{D}\n')
    speed = int(input(f'{C} CHOOSE : {D}'))
    
    spd = 2 if speed == 1 else 5 if speed == 2 else 10
    
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
        print(f'\n{BOLD}{G} TOTAL {Y}{total}{G} VALID IDS FOUND{D}\n')
    except:
        print(f'\n{R} NO VALID IDS FOUND{D}\n')

def clear_file():
    open('.uids.txt', 'w').close()

def switch():
    try:
        s = requests.get('https://raw.githubusercontent.com/havecode17/dg/refs/heads/main/switch').text
        if 'ON' in s: return
    except: pass
    print(f'\n{BOLD}{R} THIS TOOL HAS DISABLED BY ADMIN!{D}')
    exit(0)

def setup_username():
    if not os.path.exists('.name.txt'):
        username = input(f'{Y} ENTER TELEGRAM USERNAME: {D}').strip()
        with open('.name.txt', 'w') as f: f.write(username)

if __name__ == '__main__':
    setup_username()
    switch()
    main()
