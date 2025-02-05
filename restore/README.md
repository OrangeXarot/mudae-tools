# Mudae Notes
The script will generate commands to restore users after a reset.

## Usage

1. Use the command `$tsv id`
2. Copy and paste the output into the `input.txt` file.
3. Run `run.py` with your preferred flags.

## Flags

- `--auto`: Automatically writes the commands. You have 5 seconds to manually focus on Discord.
- `--perc`: Prints the percentage you're at.

## Requirements

To use this tool, ensure you have the following dependencies:

- `colorama`
- `pyautogui`
- `pyperclip`

You can install them with `pip install -r requirements.txt`