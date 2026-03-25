import requests
import random
from core.utils import print_info, print_success, print_error, save_to_file

class UserTools:
    @staticmethod
    def get_user_info(user_id, token=None):
        headers = {"User-Agent": "Mozilla/5.0"}
        if token:
            headers["Authorization"] = token
        try:
            url = f"https://discord.com/api/v9/users/{user_id}"
            r = requests.get(url, headers=headers, timeout=10)
            if r.status_code == 200:
                data = r.json()
                info = {
                    "id": data.get("id"),
                    "username": data.get("username"),
                    "discriminator": data.get("discriminator"),
                    "avatar": data.get("avatar"),
                    "bot": data.get("bot", False)
                }
                return info, None
            else:
                return None, f"Error {r.status_code}"
        except Exception as e:
            return None, str(e)

    @staticmethod
    def format_user_info(info):
        avatar_url = f"https://cdn.discordapp.com/avatars/{info['id']}/{info['avatar']}.png" if info['avatar'] else "No avatar"
        return f"""
[+] User Info
    ID: {info['id']}
    Username: {info['username']}#{info['discriminator']}
    Bot: {info['bot']}
    Avatar URL: {avatar_url}
"""

    @staticmethod
    def check_username_availability(username, discriminator):
        """التحقق إذا كان اسم المستخدم#المعرف متاحاً (غير مستخدم)"""
        url = f"https://discord.com/api/v9/users?username={username}&discriminator={discriminator}"
        headers = {"User-Agent": "Mozilla/5.0"}
        try:
            r = requests.get(url, headers=headers, timeout=10)
            if r.status_code == 404:
                return True, "Available"
            elif r.status_code == 200:
                return False, "Taken"
            else:
                return False, f"Error {r.status_code}"
        except Exception as e:
            return False, str(e)

    @staticmethod
    def find_available_discriminators(username, digits=4, limit=10):
        """
        البحث عن معرفات (مثلاً 0001-9999) غير مستخدمة لاسم مستخدم معين.
        digits: عدد الأرقام (3 أو 4 أو 5)
        limit: عدد النتائج المطلوبة
        """
        if digits == 3:
            disc_range = range(1, 1000)
            fmt = "{:03d}"
        elif digits == 4:
            disc_range = range(1, 10000)
            fmt = "{:04d}"
        elif digits == 5:
            disc_range = range(1, 100000)
            fmt = "{:05d}"
        else:
            return []

        available = []
        for num in disc_range:
            if len(available) >= limit:
                break
            disc = fmt.format(num)
            avail, _ = UserTools.check_username_availability(username, disc)
            if avail:
                available.append(disc)
                print_success(f"Found available: {username}#{disc}")
        return available

    @staticmethod
    def generate_random_usernames(count=10):
        """توليد أسماء مستخدمين عشوائية (للاختبار)"""
        prefixes = ["cool", "pro", "xd", "noob", "elite", "dark", "light", "shadow", "fire", "ice"]
        suffixes = ["gamer", "hacker", "user", "bot", "dev", "xd", "123", "zz", "qt"]
        names = []
        for _ in range(count):
            name = random.choice(prefixes) + random.choice(suffixes) + str(random.randint(0, 999))
            names.append(name)
        return names