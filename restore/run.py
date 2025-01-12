import re
import time
import argparse
import pyperclip
import pyautogui


from colorama import Fore, Style, init

init()

parser = argparse.ArgumentParser(description="Process user IDs and generate restore commands.")
parser.add_argument('--auto', action='store_true',
                    help="Automatically write commands.")
parser.add_argument('--perc', action='store_true',
                    help="Display progress percentage.")
args = parser.parse_args()

def countdown(seconds, message):
    print(f"{Fore.GREEN}{message}{Style.RESET_ALL}")
    for i in range(seconds, 0, -1):
        print(f"{Fore.CYAN}{i}{Style.RESET_ALL}", end=" ", flush=True)
        time.sleep(1)
    print("\n")

def parse_ids(file_path):
    with open(file_path, 'r') as file:
        data = file.read()
    return re.findall(r'\((\d+)\)', data)

def type_command(command):
    pyperclip.copy(command)
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press('enter')

file_path = 'list.txt'
print(f"{Fore.BLUE}Reading IDs from file: {file_path}{Style.RESET_ALL}")

try:
    ids = parse_ids(file_path)
except FileNotFoundError:
    print(f"{Fore.RED}Error: File not found: {file_path}{Style.RESET_ALL}")
    exit(1)

id_count = len(ids)
print(f"{Fore.GREEN}Found {id_count} IDs.{Style.RESET_ALL}\n")

if args.auto:
    countdown(5, "Auto mode enabled. Prepare to focus.")

completed = 0
percentage_checkpoint = 10

for idx, user_id in enumerate(ids, 1):
    command = f"$restoreuser {user_id} 1"
    print(f"{Fore.CYAN}{command}{Style.RESET_ALL}")

    if args.auto:
        type_command(command)
        time.sleep(1)

    if args.perc:
        progress = (idx / id_count) * 100
        if progress >= percentage_checkpoint:
            percentage_checkpoint += 10
            print(f"{Fore.YELLOW}Progress: {progress:.2f}% ({id_count - idx} IDs left){Style.RESET_ALL}")

print(f"{Fore.GREEN}All commands executed. Total IDs processed: {id_count}.{Style.RESET_ALL}")
