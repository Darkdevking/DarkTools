import requests
import time
from core.utils import print_info, print_success, print_error, save_to_file

class WebhookTools:
    @staticmethod
    def send_webhook_message(webhook_url, content, embeds=None):
        data = {"content": content}
        if embeds:
            data["embeds"] = embeds
        try:
            r = requests.post(webhook_url, json=data, timeout=10)
            if r.status_code == 204:
                return True, "Message sent"
            else:
                return False, f"Error {r.status_code}"
        except Exception as e:
            return False, str(e)

    @staticmethod
    def send_embed(webhook_url, title, description, color=0x00ff00, fields=None):
        embed = {
            "title": title,
            "description": description,
            "color": color
        }
        if fields:
            embed["fields"] = fields
        return WebhookTools.send_webhook_message(webhook_url, "", embeds=[embed])

    @staticmethod
    def delete_webhook(webhook_url):
        try:
            r = requests.delete(webhook_url, timeout=10)
            if r.status_code == 204:
                return True, "Webhook deleted"
            else:
                return False, f"Error {r.status_code}"
        except Exception as e:
            return False, str(e)

    @staticmethod
    def get_webhook_info(webhook_url):
        try:
            r = requests.get(webhook_url, timeout=10)
            if r.status_code == 200:
                data = r.json()
                info = {
                    "id": data.get("id"),
                    "name": data.get("name"),
                    "channel_id": data.get("channel_id"),
                    "guild_id": data.get("guild_id"),
                    "avatar": data.get("avatar"),
                }
                return info, None
            else:
                return None, f"Error {r.status_code}"
        except Exception as e:
            return None, str(e)

    @staticmethod
    def modify_webhook(webhook_url, name=None, avatar_url=None):
        """تعديل اسم أو صورة الويب هوك (avatar_url يجب أن يكون base64)"""
        payload = {}
        if name:
            payload["name"] = name
        if avatar_url:
            payload["avatar"] = avatar_url
        try:
            r = requests.patch(webhook_url, json=payload, timeout=10)
            if r.status_code == 200:
                return True, "Webhook updated"
            else:
                return False, f"Error {r.status_code}"
        except Exception as e:
            return False, str(e)

    @staticmethod
    def spam_webhook(webhook_url, message, count=10, delay=1):
        """إرسال رسائل متعددة مع تأخير"""
        for i in range(count):
            success, msg = WebhookTools.send_webhook_message(webhook_url, f"{message} [{i+1}/{count}]")
            if not success:
                return False, msg
            time.sleep(delay)
        return True, f"Sent {count} messages"

    @staticmethod
    def format_webhook_info(info):
        avatar_url = f"https://cdn.discordapp.com/avatars/{info['id']}/{info['avatar']}.png" if info['avatar'] else "No avatar"
        return f"""
[+] Webhook Info
    ID: {info['id']}
    Name: {info['name']}
    Channel ID: {info['channel_id']}
    Guild ID: {info['guild_id']}
    Avatar: {avatar_url}
"""