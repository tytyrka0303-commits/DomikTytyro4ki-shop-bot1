import os
import requests
requests.get(
    f"https://api.telegram.org/bot{TOKEN}/sendPhoto",
    params={
        "chat_id": CHAT_ID,
        "photo": "https://fortnite-api.com/images/cosmetics/br/cid_001_athena_commando_f_default/icon.png",
        "caption": "Тест фото"
    }
)
