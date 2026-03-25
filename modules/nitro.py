import re
import random
import string
import requests
from core.utils import print_info, print_success, print_error, save_to_file

class NitroTools:
    @staticmethod
    def generate_nitro_codes(count=10, length=16):
        codes = []
        for _ in range(count):
            code = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
            codes.append(f"https://discord.gift/{code}")
        return codes

    @staticmethod
    def check_nitro_link(link):
        """فحص رابط النيترو فعلياً"""
        if "discord.gift/" in link:
            code = link.split("discord.gift/")[-1].strip("/")
        else:
            code = link.strip("/")
        url = f"https://discord.gift/{code}"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        try:
            r = requests.get(url, headers=headers, allow_redirects=False, timeout=10)
            if r.status_code == 302:
                location = r.headers.get("Location", "")
                if "accept" in location or "claim" in location:
                    return True, "Valid (redirect to claim)"
                else:
                    return False, "Invalid (unexpected redirect)"
            elif r.status_code == 200:
                if "This gift has already been redeemed" in r.text:
                    return False, "Already redeemed"
                elif "expired" in r.text.lower():
                    return False, "Expired"
                else:
                    return True, "Valid (possibly claimable)"
            else:
                return False, f"HTTP {r.status_code}"
        except Exception as e:
            return False, str(e)

    @staticmethod
    def bulk_check(codes_list, save_valid_only=False):
        """فحص مجموعة روابط وإرجاع الصالح فقط"""
        valid_links = []
        for link in codes_list:
            valid, msg = NitroTools.check_nitro_link(link)
            if valid:
                valid_links.append((link, msg))
                print_success(f"{link} -> {msg}")
            else:
                print_error(f"{link} -> {msg}")
        return valid_links

    @staticmethod
    def check_from_file(filepath, save_valid_only=True):
        """قراءة روابط من ملف (كل سطر رابط) وفحصها، حفظ الصالح فقط"""
        try:
            with open(filepath, 'r') as f:
                links = [line.strip() for line in f if line.strip()]
        except Exception as e:
            return None, f"Error reading file: {e}"
        valid = NitroTools.bulk_check(links, save_valid_only)
        if valid:
            output = "\n".join([f"{link} - {msg}" for link, msg in valid])
            save_to_file(output, "valid_nitro_links")
        return valid, None