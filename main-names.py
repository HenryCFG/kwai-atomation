import os
import random
import string
import re

folder_path = r'c:\Users\henrycfg\Desktop\Automacao\videos'

def extract_number(filename):
    match = re.match(r'(\d+)', filename)
    return int(match.group(1)) if match else float('inf')

def generate_unique_code(existing_codes, length=12):
    while True:
        code = ''.join(random.choices(string.ascii_letters, k=length))
        if code not in existing_codes:
            existing_codes.add(code)
            return code

files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
files.sort(key=extract_number)

used_codes = set()

for filename in files:
    name, ext = os.path.splitext(filename)
    number_match = re.match(r'(\d+)', filename)
    if not number_match:
        continue 
    number = number_match.group(1)
    random_code = generate_unique_code(used_codes)
    new_name = f"{number} {random_code}{ext}"
    src = os.path.join(folder_path, filename)
    dst = os.path.join(folder_path, new_name)
    os.rename(src, dst)
    print(f'Renamed: {filename} -> {new_name}')
