import requests
from settings import PUSHOVER_API_TOKEN, PUSHOVER_USER_KEY

def send_pushover_notification(weekly_focus_time):
    message = f"Your total focus time this week is {weekly_focus_time:.2f} hours."
    
    response = requests.post("https://api.pushover.net/1/messages.json", data={
        "token": PUSHOVER_API_TOKEN,
        "user": PUSHOVER_USER_KEY,
        "message": message,
        "title": "Weekly Focus Report",
        "sound": "climb",  # Optional: Customize the notification sound
    })
    
    if response.status_code == 200:
        print("Notification sent successfully!")
    else:
        print("Failed to send notification:", response.status_code, response.text)