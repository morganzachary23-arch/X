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

# Session object for connection pooling
session = requests.Session()

def logo():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f'{BOLD}{C}\n       _____ __      ___                \n      / __(_) /__   / _ \\__ ____ _  ___ \n     / _// / / -_) / // / // /  \' \\/ _ \\\n    /_/ /_/_/\\__/ /____/\\_,_/_/_/_/ .__/\n                                 /_/    \n\n            FB File Maker V-2.0 (Optimized)\n {D}')

def username_gen(names, start, end):
    usernames = []
    for name in names.split(','):
        for num in range(start, end + 1):
            username = f'{name.strip().lower()}{num} | {name.capitalize()}'
            usernames.append(username)
    return usernames

def checker(uname):
    url = 'https://baji999.net/api/wv/v1/user/registerPreCheck'
    
    # Random User-Agents to avoid footprinting
    user_agents = [
        'Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.91 Mobile Safari/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (Linux; Android 10; SM-A205U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36'
    ]

    headers = {
        'sec-ch-ua-mobile': '?1',
        'User-Agent': random.choice(user_agents),
        'Content-Type': 'application/json',
        'Accept': 'application/json, text/plain, */*',
        'Referer': 'https://baji999.net/bd/en/register',
        'Origin': 'https://baji999.net'
    }

    json_data = {
        'languageTypeId': 1,
        'currencyTypeId': 8,
        'userId': uname,
        'phone': str(random.randint(1600000000, 1999999999)), # Random phone simulation
        'friendReferrerCode': '',
        'captcha': '',
        'callingCode': '880',
        'registerTypeId': 0,
        'random': str(random.randint(1000, 9999))
    }

    try:
        # Adding a small micro-delay to prevent burst triggers
        time.sleep(random.uniform(0.5, 1.5))
        
        response = session.post(url, json=json_data, headers=headers, timeout=10)
        data = response.json()

        if data.get('status') == 'F0003': # Account available/Valid
            return True
        elif data.get('status') == 'S0001' or response.status_code == 429:
            print(f'{R} [!] API LIMIT REACHED. SLEEPING 20s...{D}')
            time.sleep(20)
            return False
    except Exception as e:
        time.sleep(5)
        return False
    return False

def check_username(username):
    uname = username.replace(' ', '').split('|')[0]
    if checker(uname):
        print(f'{BOLD}{G} [SUCCESS] {uname}{D}')
        with open('.uids.txt', 'a') as file:
            file.write(username + '\n')

def main():
    logo()
    print(f'{BOLD}{Y} ENTER NAMES (e.g., Sadek, Tanvir): {D}')
    names = input(f'{BOLD}{G} >> {D}')
    start = int(input(f'{BOLD}{Y} START NUMBER: {D}'))
    end = int(input(f'{BOLD}{Y} END NUMBER: {D}'))
    
    print(f'\n{G}[1] SAFE (Slow){Y}\n[2] NORMAL (Medium){R}\n[3] RISKY (High){D}')
    speed = input(f'\n{C} CHOOSE SPEED: {D}')
    
    # Adjusting workers based on safety
    if speed == '1': spd = 2
    elif speed == '2': spd = 5
    else: spd = 8

    clear_file()
    usernames = username_gen(names, start, end)
    random.shuffle(usernames)

    print(f'\n{BOLD}{G} TOTAL USERNAMES: {len(usernames)} {D}')
    print(f'{BOLD}{G} ----------------------------------------{D}')

    with ThreadPoolExecutor(max_workers=spd) as executor:
        executor.map(check_username, usernames)

    print(f'{BOLD}{G} ----------------------------------------{D}')
    try:
        total = sum(1 for _ in open('.uids.txt'))
        print(f'\n{BOLD}{G} TOTAL {Y}{total}{G} VALID IDS FOUND{D}\n')
    except:
        print(f"\n{R} NO IDS FOUND.{D}\n")

def clear_file():
    open('.uids.txt', 'w').close()

def switch():
    try:
        s = requests.get('https://raw.githubusercontent.com/havecode17/dg/refs/heads/main/switch', timeout=5).text
        if 'ON' not in s:
            print(f'\n{BOLD}{R} TOOL DISABLED BY ADMIN!{D}')
            exit()
    except:
        pass # Skip if github is down

def setup_username():
    if not os.path.exists('.name.txt') or os.stat('.name.txt').st_size == 0:
        username = input(f'{Y} ENTER TELEGRAM USERNAME: {D}').strip()
        if not username.startswith('@'): username = '@' + username
        with open('.name.txt', 'w') as f: f.write(username)

if __name__ == '__main__':
    setup_username()
    switch()
    main()
