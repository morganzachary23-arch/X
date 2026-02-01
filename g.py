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
        headers = {
            'sec-ch-ua': '"Chromium";v="139", "Not;A=Brand";v="99"',
            'sec-ch-ua-mobile': '?1',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',
            'sec-ch-ua-arch': '""',
            'Content-Type': 'application/json',
            'sec-ch-ua-full-version': '"139.0.7339.0"',
            'Accept': 'application/json, text/plain, */*',
            'sec-ch-ua-platform-version': '"14.0.0"',
            'Referer': 'https://baji999.net/bd/en/register',
            'sec-ch-ua-full-version-list': '"Chromium";v="139.0.7339.0", "Not;A=Brand";v="99.0.0.0"',
            'sec-ch-ua-bitness': '""',
            'sec-ch-ua-model': '"LE2101"',
            'sec-ch-ua-platform': '"Android"'
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
        
        conn = http.client.HTTPSConnection('baji999.net', timeout=10)
        conn.request('POST', '/api/wv/v1/user/registerPreCheck', 
                    json.dumps(json_data), headers)
        
        response = conn.getresponse()
        response_data = response.read().decode('utf-8')
        
        # Debug: দেখুন রেসপন্স কী আসছে
        print(f"{Y}[DEBUG] Response: {response_data[:100]}...{D}")
        
        if not response_data:
            print(f"{R}[ERROR] Empty response{D}")
            return False
            
        data = json.loads(response_data)
        
        if data.get('status') == 'F0003':
            return True
        elif data.get('status') == 'S0001':
            print(f'{R} [RATE LIMIT] PLEASE TURN OFF DATA FOR 10 SEC...!{D}')
            time.sleep(30)
            return False
        else:
            print(f"{Y}[INFO] Status: {data.get('status', 'UNKNOWN')}{D}")
            return False
            
    except json.JSONDecodeError as e:
        print(f'{R} [JSON ERROR] Invalid JSON response: {e}{D}')
        print(f'{R} [RESPONSE] {response_data if "response_data" in locals() else "No data"}{D}')
        time.sleep(5)
        return False
    except Exception as e:
        print(f'{R} [ERROR] {type(e).__name__}: {e}{D}')
        time.sleep(5)
        return False
    
    return False

def check_username(username):
    try:
        uname = username.split('|')[0].strip()
        if checker(uname):
            print(f'{BOLD}{G} [FB] {uname}{D}')
            with open('.uids.txt', 'a', encoding='utf-8') as file:
                file.write(username + '\n')
    except Exception as e:
        print(f'{R}[CHECK ERROR] {e}{D}')

def main():
    logo()
    print(f'{BOLD}{Y} ENTER NAMES BY USING COMMA (,) Eg : (Sadek,Tanvir, Sagor) Etc{D}\n')
    
    names = input(f'{BOLD}{G} ENTER NAMES : {D}').strip()
    if not names:
        print(f"{R}[ERROR] No names entered{D}")
        return
        
    print('')
    
    try:
        start = int(input(f'{BOLD}{Y} START (Eg : 1 ) : {D}').strip())
        end = int(input(f'{BOLD}{Y} END (Eg : 10000 ) : {D}').strip())
        
        if start > end:
            print(f"{R}[ERROR] Start cannot be greater than end{D}")
            return
            
        if end - start > 100000:
            print(f"{R}[WARNING] Large range may cause performance issues{D}")
            
    except ValueError:
        print(f"{R}[ERROR] Invalid number{D}")
        return
    
    print('')
    print(f'{G} [1] LOW SPEED')
    print(f'{Y} [2] MEDIUM SPEED')
    print(f'{R} [3] HIGH SPEED{D}\n')
    
    try:
        speed = int(input(f'{C} CHOOSE : {D}').strip())
    except ValueError:
        speed = 1
        print(f"{Y}[INFO] Defaulting to LOW SPEED{D}")
    
    if speed == 1:
        spd = 3
    elif speed == 2:
        spd = 6
    elif speed == 3:
        spd = 12
    else:
        spd = 3
    
    clear_file()
    
    # Generate usernames
    print(f"{Y}[INFO] Generating usernames...{D}")
    usernames = username_gen(names, start, end)
    random.shuffle(usernames)
    
    print('')
    print(f'{BOLD}{G} TOTAL USERNAMES : {len(usernames)} {D}')
    print(f'{BOLD}{G} ----------------------------------------{D}')
    
    # Progress counter
    total_checked = 0
    valid_count = 0
    
    # Use ThreadPoolExecutor with error handling
    with ThreadPoolExecutor(max_workers=spd) as executor:
        futures = []
        for username in usernames:
            future = executor.submit(check_username, username)
            futures.append(future)
            total_checked += 1
            
            # Show progress every 100 checks
            if total_checked % 100 == 0:
                print(f"{Y}[PROGRESS] Checked: {total_checked}/{len(usernames)}{D}")
                # Count current valid IDs
                try:
                    with open('.uids.txt', 'r', encoding='utf-8') as f:
                        valid_count = len(f.readlines())
                    print(f"{G}[VALID] Found: {valid_count}{D}")
                except:
                    pass
        
        # Wait for all threads to complete
        for future in futures:
            try:
                future.result(timeout=30)
            except Exception as e:
                print(f"{R}[THREAD ERROR] {e}{D}")
    
    print(f'{BOLD}{G} ---------------------------------------{D}')
    
    # Show final results
    try:
        with open('.uids.txt', 'r', encoding='utf-8') as f:
            valid_ids = f.readlines()
            total_valid = len(valid_ids)
            
        print(f'\n{BOLD}{G} TOTAL {Y}{total_valid}{G} VALID FB IDS FOUND{D}\n')
        
        if total_valid > 0:
            print(f'{C} Saved in: .uids.txt{D}')
            print(f'{C} First few results:{D}')
            for i, id_line in enumerate(valid_ids[:5]):
                print(f'{G}  {i+1}. {id_line.strip()}{D}')
                
    except FileNotFoundError:
        print(f'\n{R} No valid IDs found{D}\n')
    
    print(f'\n{Y} Press Enter to exit...{D}')
    input()

def clear_file():
    try:
        with open('.uids.txt', 'w', encoding='utf-8') as file:
            pass
    except:
        pass

def switch():
    try:
        s = requests.get('https://raw.githubusercontent.com/havecode17/dg/refs/heads/main/switch', 
                        timeout=10).text
        if 'ON' in s:
            return
        print(f'\n{BOLD}{R} THIS TOOL HAS BEEN DISABLED BY ADMIN!{D}')
        exit(0)
    except Exception as e:
        print(f'{Y}[SWITCH CHECK ERROR] {e}{D}')
        print(f'{Y}[INFO] Continuing anyway...{D}')

def setup_username():
    try:
        with open('.name.txt', 'r', encoding='utf-8') as f:
            if f.read().strip():
                return
    except FileNotFoundError:
        username = input(f'{Y} ENTER TELEGRAM USERNAME: {D}').strip()
        if not username.startswith('@'):
            username = '@' + username
        with open('.name.txt', 'w', encoding='utf-8') as f:
            f.write(username)

if __name__ == '__main__':
    try:
        setup_username()
        switch()
        main()
    except KeyboardInterrupt:
        print(f'\n{R}[INFO] Process interrupted by user{D}')
    except Exception as e:
        print(f'\n{R}[FATAL ERROR] {type(e).__name__}: {e}{D}')
        print(f'{Y}Press Enter to exit...{D}')
        input()
