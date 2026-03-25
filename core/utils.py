import os
import sys
from datetime import datetime
from .colors import Colors

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def press_enter():
    input(Colors.YELLOW + "\n[!] Press Enter to continue..." + Colors.RESET)

def print_error(msg):
    print(Colors.RED + f"[-] {msg}" + Colors.RESET)

def print_success(msg):
    print(Colors.GREEN + f"[+] {msg}" + Colors.RESET)

def print_info(msg):
    print(Colors.CYAN + f"[*] {msg}" + Colors.RESET)

def print_warning(msg):
    print(Colors.YELLOW + f"[!] {msg}" + Colors.RESET)

def save_to_file(data, filename_prefix, extension="txt"):
    outputs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "outputs")
    if not os.path.exists(outputs_dir):
        os.makedirs(outputs_dir)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{filename_prefix}_{timestamp}.{extension}"
    filepath = os.path.join(outputs_dir, filename)
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(data)
        print_success(f"Saved to: {filepath}")
        return filepath
    except Exception as e:
        print_error(f"Failed to save: {e}")
        return None