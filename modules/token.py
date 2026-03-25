import requests
from core.utils import print_info, print_success, print_error, save_to_file

class TokenTools:
    @staticmethod
    def check_token(token):
        headers = {"Authorization": token, "User-Agent": "Mozilla/5.0"}
        try:
            r = requests.get("https://discord.com/api/v9/users/@me", headers=headers, timeout=10)
            if r.status_code == 200:
                return True, "Valid"
            elif r.status_code == 401:
                return False, "Invalid"
            else:
                return False, f"Error {r.status_code}"
        except Exception as e:
            return False, str(e)

    @staticmethod
    def get_token_info(token):
        headers = {"Authorization": token, "User-Agent": "Mozilla/5.0"}
        try:
            r = requests.get("https://discord.com/api/v9/users/@me", headers=headers, timeout=10)
            if r.status_code != 200:
                return None, f"Failed: {r.status_code}"
            data = r.json()
            info = {
                "id": data.get("id"),
                "username": data.get("username"),
                "discriminator": data.get("discriminator"),
                "email": data.get("email"),
                "phone": data.get("phone"),
                "verified": data.get("verified"),
                "mfa_enabled": data.get("mfa_enabled"),
                "premium_type": data.get("premium_type", 0)
            }
            return info, None
        except Exception as e:
            return None, str(e)

    @staticmethod
    def get_token_type(token):
        headers = {"Authorization": token, "User-Agent": "Mozilla/5.0"}
        try:
            r = requests.get("https://discord.com/api/v9/users/@me", headers=headers, timeout=10)
            if r.status_code == 200:
                data = r.json()
                return "Bot Token" if "bot" in data else "User Token"
            return "Invalid Token"
        except:
            return "Error"

    @staticmethod
    def format_info(info):
        nitro_map = {0: "None", 1: "Nitro Classic", 2: "Nitro"}
        return f"""
[+] Discord Account Info
    ID: {info['id']}
    Username: {info['username']}#{info['discriminator']}
    Email: {info['email'] or 'Not visible'}
    Phone: {info['phone'] or 'Not visible'}
    Verified: {info['verified']}
    2FA Enabled: {info['mfa_enabled']}
    Nitro: {nitro_map.get(info['premium_type'], 'Unknown')}
"""

    @staticmethod
    def check_tokens_from_file(filepath):
        """قراءة توكنات من ملف (كل سطر توكن) وفحصها"""
        try:
            with open(filepath, 'r') as f:
                tokens = [line.strip() for line in f if line.strip()]
        except Exception as e:
            return None, f"Error reading file: {e}"

        results = []
        for token in tokens:
            valid, msg = TokenTools.check_token(token)
            results.append((token, msg))
        return results, None