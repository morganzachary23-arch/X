import requests
import random
import json
import time
import os
from concurrent.futures import ThreadPoolExecutor

# Color Codes
BOLD = '\033[1m'
R = '\033[91m' # Red
G = '\033[92m' # Green
Y = '\033[93m' # Yellow
D = '\033[0m'  # Default
C = '\033[96m' # Cyan

# Global Request Session
session = requests.Session()

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

# Random User Agent Generator
def get_headers():
    android_versions = ['10', '11', '12', '13', '14']
    models = ['SM-A205U', 'Pixel 6', 'Redmi Note 10', 'Samsung Galaxy S21', 'OnePlus 9']
    
    ua = f'Mozilla/5.0 (Linux; Android {random.choice(android_versions)}; {random.choice(models)}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(110, 139)}.0.0.0 Mobile Safari/537.36'
    
    return {
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120"', 
        'sec-ch-ua-mobile': '?1', 
        'User-Agent': ua, 
        'Content-Type': 'application/json', 
        'Accept': 'application/json, text/plain, */*',
        'Referer': 'https://baji999.net/bd/en/register',
        'Origin': 'https://baji999.net'
    }

def checker(uname):
    try:
        url = 'https://baji999.net/api/wv/v1/user/registerPreCheck'
        
        # Payload with randomization
        json_data = {
            'languageTypeId': 1, 
            'currencyTypeId': 8, 
            'userId': uname, 
            'phone': str(random.randint(1300000000, 1999999999)), # Random phone logic
            'friendReferrerCode': '', 
            'captcha': '', 
            'callingCode': '880', 
            'registerTypeId': 0, 
            'random': str(random.randint(1000, 9999))
        }

        # Timeout added to prevent "Stuck" issue (5 seconds max wait)
        response = session.post(url, json=json_data, headers=get_headers(), timeout=5)
        
        # Check if response is empty
        if not response.text:
            return False

        data = response.json()

        if data.get('status') == 'F0003': # ID Available
            return True
        elif data.get('status') == 'S0001': # Rate Limit
            print(f'{R} [BLOCK] Waiting 10s...{D}')
            time.sleep(10) # Cool down logic
            return False
            
    except requests.exceptions.ConnectionError:
        time.sleep(2) # Network issue
    except requests.exceptions.Timeout:
        pass # Just skip if stuck
    except Exception as e:
        pass
        
    return False

def check_username(username):
    # Split safely
    try:
        uname = username.replace(' ', '').split('|')[0]
        if checker(uname):
            print(f'{BOLD}{G} [OK] {uname}{D}')
            with open('.uids.txt', 'a') as file:
                file.write(username + '\n')
        else:
            # Optional: Print failing to see speed (Comment out if not needed)
            # print(f'{R} [XX] {uname}{D}', end='\r')
            pass
    except:
        pass

def main():
    logo()
    print(f'{BOLD}{Y} ENTER NAMES BY USING COMMA (,) Eg : (Sadek,Tanvir){D}\n')
    names = input(f'{BOLD}{G} ENTER NAMES : {D}')
    print('')
    start = int(input(f'{BOLD}{Y} START (Eg : 1 ) : '))
    end = int(input(f'{BOLD}{Y} END (Eg : 1000 ) : '))
    print('')
    
    # Speed selection logic changed for safety
    print(f'{G} [1] SAFE SPEED (Recommended)')
    print(f'{Y} [2] MEDIUM SPEED')
    print(f'{R} [3] CRASH SPEED (Will Block){D}\n')
    
    speed = input(f'{C} CHOOSE : {D}')
    
    if speed == '1':
        spd = 1  # Very slow but safe
    elif speed == '2':
        spd = 4  # Balanced
    elif speed == '3':
        spd = 10 # High risk
    else:
        spd = 2

    clear_file()
    usernames = username_gen(names, start, end)
    random.shuffle(usernames)
    
    print('')
    print(f'{BOLD}{G} TOTAL USERNAMES : {len(usernames)} {D}')
    print(f'{BOLD}{G} ----------------------------------------{D}')
    
    with ThreadPoolExecutor(max_workers=spd) as executor:
        executor.map(check_username, usernames)
        
    print(f'{BOLD}{G} ---------------------------------------{D}')
    try:
        total = sum((1 for _ in open('.uids.txt')))
        print(f'\n{BOLD}{G} TOTAL{Y} {total} {G}VALID FB IDS FOUND{D}\n\n')
    except:
        print(f'\n{BOLD}{R} NO IDS FOUND {D}\n')

def clear_file():
    with open('.uids.txt', 'w') as file:
        pass

def switch():
    try:
        s = requests.get('https://raw.githubusercontent.com/havecode17/dg/refs/heads/main/switch', timeout=5).text
        if 'ON' in s:
            return
    except:
        pass # If check fails, continue script
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
