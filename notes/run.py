import re
from collections import defaultdict
import argparse
from colorama import Fore, Style, init
import time
import pyautogui
import pyperclip

init()

parser = argparse.ArgumentParser(description="Process and group notes with additional flags for automation and progress.")
parser.add_argument('--auto', action='store_true', help="Automate the process and type commands automatically.")
parser.add_argument('--perc', action='store_true', help="Print progress as percentage during execution.")
parser.add_argument('--file', type=str, default='input.txt', help="Input file containing notes.")
args = parser.parse_args()

def chunk_list(lst, max_size):
    for i in range(0, len(lst), max_size):
        yield lst[i:i + max_size]

def countdown(seconds):
    for i in range(seconds, 0, -1):
        print(f"{Fore.CYAN}{i}{Style.RESET_ALL}", end=" ", flush=True)
        time.sleep(1)
    print()

def type_command(command):
    pyperclip.copy(command)
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press('enter')

def process_notes(file_path):
    print(f"{Fore.BLUE}Reading input file: {file_path}{Style.RESET_ALL}")
    with open(file_path, "r") as file:
        text = file.read()

    pattern = r"(.+?)\s*\|\s*(.+)"
    matches = re.findall(pattern, text)

    grouped_data = defaultdict(list)
    all_notes = []
    seen_notes = set()

    for name, note in matches:
        note = note.strip()
        grouped_data[note].append(name.strip())
        if note not in seen_notes:
            all_notes.append(note)
            seen_notes.add(note)

    total_notes = len(grouped_data)
    counter = 0
    progress_step = 10

    for note, names in grouped_data.items():
        for chunk in chunk_list(names, 50):
            counter += 1
            command = f"$n {'$'.join(chunk)}${note}"
            print(f"{Fore.CYAN}{command}{Style.RESET_ALL}")

            if args.auto:
                type_command(command)
                time.sleep(1)

            if args.perc:
                percentage = round(counter / total_notes * 100, 2)
                if percentage >= progress_step:
                    progress_step += 10
                    phraseT = f"{Fore.YELLOW}{percentage}% complete ({total_notes - counter} remaining).{Style.RESET_ALL}" 
                    phrase  = f"*{percentage}% complete ({total_notes - counter} remaining).*"
                    print(phraseT)
                    type_command(phrase)
                    time.sleep(1)

    print(f"{Fore.GREEN}Processing complete.{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}$sm$mmr{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}$smn {'$'.join(all_notes)}{Style.RESET_ALL}")

    if args.auto:
        final_message = f"Processed {total_notes} notes."
        type_command(final_message)

if __name__ == "__main__":
    if args.auto:
        print(f"{Fore.GREEN}Auto mode enabled. Starting in 5 seconds...{Style.RESET_ALL}")
        countdown(5)

    process_notes(args.file)
