from focus_tracker import load_progress, get_weekly_focus_time
from pushover_notify import send_pushover_notification

def send_weekly_report():
    daily_focus_time, _ = load_progress()
    
    # Debugging: Print out the daily_focus_time dictionary
    print("Daily Focus Time Data:", daily_focus_time)
    
    weekly_focus_time = get_weekly_focus_time(daily_focus_time)
    
    # Debugging: Print out the calculated weekly focus time
    print(f"Calculated Weekly Focus Time: {weekly_focus_time:.2f} hours")
    
    send_pushover_notification(weekly_focus_time)

if __name__ == "__main__":
    send_weekly_report()