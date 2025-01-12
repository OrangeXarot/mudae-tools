import requests
import re
from io import BytesIO
from colorthief import ColorThief
import pyautogui
import time
import argparse
from colorama import Fore, Style, init
import pyperclip

init()

parser = argparse.ArgumentParser()
parser.add_argument('--auto', action='store_true',
                    help="Writes the commands automatically, (you have 5 seconds to manually focus on discord).")
parser.add_argument('--perc', action='store_true', help="Prints the percentage you're at.")

args = parser.parse_args()


def get_most_dominant_color(image_url):
    response = requests.get(image_url)
    response.raise_for_status()

    image_bytes = BytesIO(response.content)
    color_thief = ColorThief(image_bytes)

    dominant_color = color_thief.get_color(quality=1)
    hex_color = '{:02x}{:02x}{:02x}'.format(*dominant_color)

    return hex_color


def parse_file(file_path):
    name_link_dict = {}
    pattern = re.compile(r"(.+?)\s*\u00b7.*?-\s*(https?://\S+)")

    with open(file_path, 'r') as file:
        for line in file:
            match = pattern.search(line)
            if match:
                name = match.group(1).strip()
                link = match.group(2).strip()

                if "imgur.com" in link:
                    print(f"{Fore.YELLOW}[SKIP]{Style.RESET_ALL} Found imgur link for \"{name}\". Skipping...")
                    continue
                name_link_dict[name] = link
    return name_link_dict

def type_command(command):
    pyperclip.copy(command)
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press('enter')


def countdown(seconds):
    for i in range(seconds, 0, -1):
        print(f"{Fore.CYAN}{i}{Style.RESET_ALL}", end=" ", flush=True)
        time.sleep(1)
    print()


def countdown_spam(seconds):
    for i in range(seconds, 0, -1):
        string = str(i) + "."
        type_command(string)
        time.sleep(1)


file_path = 'input.txt'
print(f"{Fore.BLUE}Parsing input...{Style.RESET_ALL}")
data = parse_file(file_path)

data_length = len(data)

print(f"{Fore.GREEN}Done.{Style.RESET_ALL}")
print(f"{Fore.MAGENTA}The total is: {data_length}.{Style.RESET_ALL}\n")

if args.perc:
    print(f"{Fore.GREEN}The --perc argument was provided.{Style.RESET_ALL}")
else:
    print(f"{Fore.RED}The --perc argument was not provided.{Style.RESET_ALL}")

if args.auto:
    print(f"{Fore.GREEN}The --auto argument was provided. You have 5 seconds to switch to Discord.{Style.RESET_ALL}")
    countdown(5)
    print()
    string = f"**This user is going to edit {data_length} characters' embedded color.** Prepare in 3."
    type_command(string)
    countdown_spam(2)
else:
    print(f"{Fore.RED}The --auto argument was not provided.{Style.RESET_ALL}")

counter = 0
percbump = 0
print(f"\n{Fore.BLUE}Extracting colors and printing commands...{Style.RESET_ALL}")

for name, link in data.items():
    counter += 1
    most_dominant_color = get_most_dominant_color(link)
    command = f"$ec {name}${most_dominant_color}"

    print(f"{Fore.CYAN}{command}{Style.RESET_ALL}")

    if args.auto:
        type_command(command)
        time.sleep(1)

    if args.perc:
        percentage = round(counter / data_length * 100, 2)
        if percentage >= percbump:
            percbump += 10
            strp = f"{percentage}% ({data_length - counter} left)"
            print(f"{Fore.YELLOW}{strp}{Style.RESET_ALL}")
            if args.auto:
                string = f"*{strp}*"
                type_command(string)
                time.sleep(1)

print(f"{Fore.GREEN}Done.{Style.RESET_ALL}")
if args.auto:
    string = f"Done {data_length} characters."
    type_command(string)
