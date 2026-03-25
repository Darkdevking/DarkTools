#!/usr/bin/env python3
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.colors import Colors
from core.banner import show_banner
from core.utils import clear_screen, press_enter, print_error, print_success, print_info, print_warning, save_to_file
from modules.token import TokenTools
from modules.nitro import NitroTools
from modules.user import UserTools
from modules.webhook import WebhookTools

def main_menu():
    clear_screen()
    show_banner()
    print(Colors.CYAN + """
    ╔══════════════════════════════════════╗
    ║            MAIN MENU                 ║
    ╠══════════════════════════════════════╣
    ║  [1] Token Tools                     ║
    ║  [2] Nitro Tools                     ║
    ║  [3] User Tools                      ║
    ║  [4] Webhook Tools                   ║
    ║  [5] Outputs (View Saved Files)      ║
    ║  [6] About / Info                    ║
    ║  [0] Exit                            ║
    ╚══════════════════════════════════════╝
    """ + Colors.RESET)
    return input(Colors.YELLOW + "[?] Select an option: " + Colors.RESET)

def token_menu():
    clear_screen()
    print(Colors.CYAN + """
    ╔══════════════════════════════════════╗
    ║         TOKEN TOOLS                  ║
    ╠══════════════════════════════════════╣
    ║  [1] Token Checker                   ║
    ║  [2] Token Info                      ║
    ║  [3] Token Type                      ║
    ║  [4] Check tokens from file          ║
    ║  [0] Back to Main Menu               ║
    ╚══════════════════════════════════════╝
    """ + Colors.RESET)
    return input(Colors.YELLOW + "[?] Select an option: " + Colors.RESET)

def nitro_menu():
    clear_screen()
    print(Colors.CYAN + """
    ╔══════════════════════════════════════╗
    ║         NITRO TOOLS                  ║
    ╠══════════════════════════════════════╣
    ║  [1] Generate Nitro Codes            ║
    ║  [2] Check single link               ║
    ║  [3] Bulk check from file            ║
    ║  [0] Back to Main Menu               ║
    ╚══════════════════════════════════════╝
    """ + Colors.RESET)
    return input(Colors.YELLOW + "[?] Select an option: " + Colors.RESET)

def user_menu():
    clear_screen()
    print(Colors.CYAN + """
    ╔══════════════════════════════════════╗
    ║         USER TOOLS                   ║
    ╠══════════════════════════════════════╣
    ║  [1] Get User Info by ID             ║
    ║  [2] Find available discriminators   ║
    ║  [3] Generate random usernames       ║
    ║  [0] Back to Main Menu               ║
    ╚══════════════════════════════════════╝
    """ + Colors.RESET)
    return input(Colors.YELLOW + "[?] Select an option: " + Colors.RESET)

def webhook_menu():
    clear_screen()
    print(Colors.CYAN + """
    ╔══════════════════════════════════════╗
    ║         WEBHOOK TOOLS                ║
    ╠══════════════════════════════════════╣
    ║  [1] Send Message                    ║
    ║  [2] Send Embed                      ║
    ║  [3] Delete Webhook                  ║
    ║  [4] Get Webhook Info                ║
    ║  [5] Modify Webhook (name/avatar)    ║
    ║  [6] Spam Webhook                    ║
    ║  [0] Back to Main Menu               ║
    ╚══════════════════════════════════════╝
    """ + Colors.RESET)
    return input(Colors.YELLOW + "[?] Select an option: " + Colors.RESET)

def view_outputs():
    outputs_dir = os.path.join(os.path.dirname(__file__), "outputs")
    if not os.path.exists(outputs_dir):
        print_warning("Outputs directory does not exist.")
        press_enter()
        return
    files = os.listdir(outputs_dir)
    if not files:
        print_warning("No saved files found.")
        press_enter()
        return
    clear_screen()
    print(Colors.CYAN + "\n[ Saved Files ]\n" + Colors.RESET)
    for i, f in enumerate(files, 1):
        print(f"  {i}. {f}")
    print(Colors.YELLOW + "\n[0] Back" + Colors.RESET)
    choice = input(Colors.YELLOW + "[?] View file number (or 0): " + Colors.RESET)
    if choice == "0":
        return
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(files):
            filepath = os.path.join(outputs_dir, files[idx])
            print(Colors.CYAN + f"\n--- Content of {files[idx]} ---\n" + Colors.RESET)
            with open(filepath, 'r', encoding='utf-8') as f:
                print(f.read())
            press_enter()
        else:
            print_error("Invalid number.")
            press_enter()
    except ValueError:
        print_error("Invalid input.")
        press_enter()

def about():
    clear_screen()
    print(Colors.CYAN + """
    ╔══════════════════════════════════════╗
    ║           ABOUT DarkTools            ║
    ╠══════════════════════════════════════╣
    ║  Version: 1.1                        ║
    ║  Author: DarK                        ║
    ║  Purpose: Discord Tool Suite         ║
    ║  Features:                           ║
    ║    - Token tools (check, info, file) ║
    ║    - Nitro checker & generator       ║
    ║    - User lookup & availability      ║
    ║    - Webhook manager (spam, embed)   ║
    ║  Outputs saved in 'outputs' folder   ║
    ║  Usage: Educational Purposes Only    ║
    ╚══════════════════════════════════════╝
    """ + Colors.RESET)
    press_enter()

# ---------- Token UI ----------
def token_checker_ui():
    clear_screen()
    print(Colors.CYAN + "\n[ Token Checker ]\n" + Colors.RESET)
    token = input(Colors.YELLOW + "[?] Enter Discord token: " + Colors.RESET).strip()
    if not token:
        print_error("Token cannot be empty.")
        press_enter()
        return
    print_info("Checking token...")
    valid, msg = TokenTools.check_token(token)
    if valid:
        print_success(f"Token is {msg}")
    else:
        print_error(f"Token is {msg}")
    save_to_file(f"Token: {token}\nStatus: {msg}", "token_check")
    press_enter()

def token_info_ui():
    clear_screen()
    print(Colors.CYAN + "\n[ Token Info ]\n" + Colors.RESET)
    token = input(Colors.YELLOW + "[?] Enter Discord token: " + Colors.RESET).strip()
    if not token:
        print_error("Token cannot be empty.")
        press_enter()
        return
    print_info("Fetching token info...")
    info, err = TokenTools.get_token_info(token)
    if info:
        formatted = TokenTools.format_info(info)
        print(Colors.GREEN + formatted)
        save_to_file(formatted, "token_info")
    else:
        print_error(f"Failed: {err}")
    press_enter()

def token_type_ui():
    clear_screen()
    print(Colors.CYAN + "\n[ Token Type ]\n" + Colors.RESET)
    token = input(Colors.YELLOW + "[?] Enter Discord token: " + Colors.RESET).strip()
    if not token:
        print_error("Token cannot be empty.")
        press_enter()
        return
    print_info("Identifying token type...")
    ttype = TokenTools.get_token_type(token)
    print_success(f"Token type: {ttype}")
    save_to_file(f"Token: {token}\nType: {ttype}", "token_type")
    press_enter()

def token_file_check_ui():
    clear_screen()
    print(Colors.CYAN + "\n[ Check tokens from file ]\n" + Colors.RESET)
    filepath = input(Colors.YELLOW + "[?] Path to token file (one per line): " + Colors.RESET).strip()
    if not filepath:
        print_error("No file provided.")
        press_enter()
        return
    results, err = TokenTools.check_tokens_from_file(filepath)
    if err:
        print_error(err)
        press_enter()
        return
    if not results:
        print_warning("No tokens in file.")
        press_enter()
        return
    output = ""
    for token, status in results:
        output += f"{token} -> {status}\n"
        if "Valid" in status:
            print_success(f"{token} -> {status}")
        else:
            print_error(f"{token} -> {status}")
    save_to_file(output, "bulk_token_check")
    press_enter()

# ---------- Nitro UI ----------
def nitro_generate_ui():
    clear_screen()
    print(Colors.CYAN + "\n[ Generate Nitro Codes ]\n" + Colors.RESET)
    try:
        count = int(input(Colors.YELLOW + "[?] Number of codes to generate: " + Colors.RESET).strip())
    except:
        count = 10
    codes = NitroTools.generate_nitro_codes(count)
    print_success(f"Generated {len(codes)} codes:")
    for c in codes:
        print(Colors.CYAN + c)
    save_to_file("\n".join(codes), "nitro_codes")
    press_enter()

def nitro_check_single_ui():
    clear_screen()
    print(Colors.CYAN + "\n[ Check Nitro Link ]\n" + Colors.RESET)
    link = input(Colors.YELLOW + "[?] Enter nitro link or code: " + Colors.RESET).strip()
    if not link:
        print_error("No input.")
        press_enter()
        return
    valid, msg = NitroTools.check_nitro_link(link)
    if valid:
        print_success(f"Valid: {msg}")
    else:
        print_error(f"Invalid: {msg}")
    save_to_file(f"Link: {link}\nStatus: {msg}", "nitro_check")
    press_enter()

def nitro_bulk_check_ui():
    clear_screen()
    print(Colors.CYAN + "\n[ Bulk Check Nitro Links ]\n" + Colors.RESET)
    filepath = input(Colors.YELLOW + "[?] Path to file with links (one per line): " + Colors.RESET).strip()
    if not filepath:
        print_error("No file provided.")
        press_enter()
        return
    valid, err = NitroTools.check_from_file(filepath, save_valid_only=True)
    if err:
        print_error(err)
    elif not valid:
        print_warning("No valid links found.")
    press_enter()

# ---------- User UI ----------
def user_info_ui():
    clear_screen()
    print(Colors.CYAN + "\n[ Get User Info by ID ]\n" + Colors.RESET)
    user_id = input(Colors.YELLOW + "[?] Enter user ID: " + Colors.RESET).strip()
    token = input(Colors.YELLOW + "[?] Optional token (press Enter to skip): " + Colors.RESET).strip() or None
    if not user_id:
        print_error("User ID cannot be empty.")
        press_enter()
        return
    print_info("Fetching user info...")
    info, err = UserTools.get_user_info(user_id, token)
    if info:
        formatted = UserTools.format_user_info(info)
        print(Colors.GREEN + formatted)
        save_to_file(formatted, f"user_{user_id}")
    else:
        print_error(f"Failed: {err}")
    press_enter()

def user_find_discriminators_ui():
    clear_screen()
    print(Colors.CYAN + "\n[ Find Available Discriminators ]\n" + Colors.RESET)
    username = input(Colors.YELLOW + "[?] Username (without #): " + Colors.RESET).strip()
    if not username:
        print_error("Username required.")
        press_enter()
        return
    digits = input(Colors.YELLOW + "[?] Number of digits (3,4,5): " + Colors.RESET).strip()
    try:
        digits = int(digits)
        if digits not in (3,4,5):
            digits = 4
    except:
        digits = 4
    limit = input(Colors.YELLOW + "[?] How many to find (default 10): " + Colors.RESET).strip()
    try:
        limit = int(limit)
    except:
        limit = 10
    print_info(f"Searching for available {digits}-digit discriminators...")
    available = UserTools.find_available_discriminators(username, digits, limit)
    if available:
        output = f"Available discriminators for {username}:\n" + "\n".join(available)
        print_success(output)
        save_to_file(output, f"available_disc_{username}")
    else:
        print_warning("No available discriminators found.")
    press_enter()

def user_generate_usernames_ui():
    clear_screen()
    print(Colors.CYAN + "\n[ Generate Random Usernames ]\n" + Colors.RESET)
    try:
        count = int(input(Colors.YELLOW + "[?] How many usernames to generate: " + Colors.RESET).strip())
    except:
        count = 10
    names = UserTools.generate_random_usernames(count)
    output = "\n".join(names)
    print_success(f"Generated {len(names)} usernames:")
    print(Colors.CYAN + output)
    save_to_file(output, "random_usernames")
    press_enter()

# ---------- Webhook UI ----------
def webhook_send_ui():
    clear_screen()
    print(Colors.CYAN + "\n[ Send Webhook Message ]\n" + Colors.RESET)
    url = input(Colors.YELLOW + "[?] Webhook URL: " + Colors.RESET).strip()
    msg = input(Colors.YELLOW + "[?] Message: " + Colors.RESET).strip()
    if not url or not msg:
        print_error("URL and message are required.")
        press_enter()
        return
    success, result = WebhookTools.send_webhook_message(url, msg)
    if success:
        print_success(result)
    else:
        print_error(result)
    save_to_file(f"URL: {url}\nMessage: {msg}\nStatus: {result}", "webhook_send")
    press_enter()

def webhook_send_embed_ui():
    clear_screen()
    print(Colors.CYAN + "\n[ Send Embed ]\n" + Colors.RESET)
    url = input(Colors.YELLOW + "[?] Webhook URL: " + Colors.RESET).strip()
    title = input(Colors.YELLOW + "[?] Title: " + Colors.RESET).strip()
    desc = input(Colors.YELLOW + "[?] Description: " + Colors.RESET).strip()
    if not url:
        print_error("URL required.")
        press_enter()
        return
    success, result = WebhookTools.send_embed(url, title, desc)
    if success:
        print_success(result)
    else:
        print_error(result)
    save_to_file(f"URL: {url}\nEmbed sent: {title}", "webhook_embed")
    press_enter()

def webhook_delete_ui():
    clear_screen()
    print(Colors.CYAN + "\n[ Delete Webhook ]\n" + Colors.RESET)
    url = input(Colors.YELLOW + "[?] Webhook URL: " + Colors.RESET).strip()
    if not url:
        print_error("URL required.")
        press_enter()
        return
    confirm = input(Colors.RED + "[!] Are you sure? (y/n): " + Colors.RESET).strip().lower()
    if confirm != 'y':
        return
    success, result = WebhookTools.delete_webhook(url)
    if success:
        print_success(result)
    else:
        print_error(result)
    save_to_file(f"URL: {url}\nStatus: {result}", "webhook_delete")
    press_enter()

def webhook_info_ui():
    clear_screen()
    print(Colors.CYAN + "\n[ Get Webhook Info ]\n" + Colors.RESET)
    url = input(Colors.YELLOW + "[?] Webhook URL: " + Colors.RESET).strip()
    if not url:
        print_error("URL required.")
        press_enter()
        return
    info, err = WebhookTools.get_webhook_info(url)
    if info:
        formatted = WebhookTools.format_webhook_info(info)
        print(Colors.GREEN + formatted)
        save_to_file(formatted, "webhook_info")
    else:
        print_error(f"Failed: {err}")
    press_enter()

def webhook_modify_ui():
    clear_screen()
    print(Colors.CYAN + "\n[ Modify Webhook ]\n" + Colors.RESET)
    url = input(Colors.YELLOW + "[?] Webhook URL: " + Colors.RESET).strip()
    if not url:
        print_error("URL required.")
        press_enter()
        return
    name = input(Colors.YELLOW + "[?] New name (leave empty to skip): " + Colors.RESET).strip() or None
    avatar = input(Colors.YELLOW + "[?] New avatar URL (base64 or image URL? API expects base64): " + Colors.RESET).strip() or None
    if not name and not avatar:
        print_warning("No changes provided.")
        press_enter()
        return
    success, result = WebhookTools.modify_webhook(url, name, avatar)
    if success:
        print_success(result)
    else:
        print_error(result)
    save_to_file(f"URL: {url}\nChanges: name={name}, avatar set\nStatus: {result}", "webhook_modify")
    press_enter()

def webhook_spam_ui():
    clear_screen()
    print(Colors.CYAN + "\n[ Spam Webhook ]\n" + Colors.RESET)
    url = input(Colors.YELLOW + "[?] Webhook URL: " + Colors.RESET).strip()
    msg = input(Colors.YELLOW + "[?] Message: " + Colors.RESET).strip()
    if not url or not msg:
        print_error("URL and message are required.")
        press_enter()
        return
    try:
        count = int(input(Colors.YELLOW + "[?] Number of messages: " + Colors.RESET).strip())
    except:
        count = 10
    try:
        delay = float(input(Colors.YELLOW + "[?] Delay between messages (seconds): " + Colors.RESET).strip())
    except:
        delay = 1
    print_warning("Spamming... press Ctrl+C to stop.")
    success, result = WebhookTools.spam_webhook(url, msg, count, delay)
    if success:
        print_success(result)
    else:
        print_error(result)
    save_to_file(f"URL: {url}\nSpam count: {count}\nStatus: {result}", "webhook_spam")
    press_enter()

# ---------- Main Loop ----------
def main():
    while True:
        choice = main_menu()
        if choice == "1":
            while True:
                sub = token_menu()
                if sub == "0":
                    break
                elif sub == "1":
                    token_checker_ui()
                elif sub == "2":
                    token_info_ui()
                elif sub == "3":
                    token_type_ui()
                elif sub == "4":
                    token_file_check_ui()
                else:
                    print_error("Invalid option!")
                    press_enter()
        elif choice == "2":
            while True:
                sub = nitro_menu()
                if sub == "0":
                    break
                elif sub == "1":
                    nitro_generate_ui()
                elif sub == "2":
                    nitro_check_single_ui()
                elif sub == "3":
                    nitro_bulk_check_ui()
                else:
                    print_error("Invalid option!")
                    press_enter()
        elif choice == "3":
            while True:
                sub = user_menu()
                if sub == "0":
                    break
                elif sub == "1":
                    user_info_ui()
                elif sub == "2":
                    user_find_discriminators_ui()
                elif sub == "3":
                    user_generate_usernames_ui()
                else:
                    print_error("Invalid option!")
                    press_enter()
        elif choice == "4":
            while True:
                sub = webhook_menu()
                if sub == "0":
                    break
                elif sub == "1":
                    webhook_send_ui()
                elif sub == "2":
                    webhook_send_embed_ui()
                elif sub == "3":
                    webhook_delete_ui()
                elif sub == "4":
                    webhook_info_ui()
                elif sub == "5":
                    webhook_modify_ui()
                elif sub == "6":
                    webhook_spam_ui()
                else:
                    print_error("Invalid option!")
                    press_enter()
        elif choice == "5":
            view_outputs()
        elif choice == "6":
            about()
        elif choice == "0":
            clear_screen()
            print_success("Goodbye!")
            sys.exit(0)
        else:
            print_error("Invalid option!")
            press_enter()

if __name__ == "__main__":
    main()