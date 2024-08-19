# Focus Tracker

Focus Tracker is a Pomodoro timer application built with Python and Pygame that helps you manage your time effectively. It tracks your focus sessions and provides weekly mobile reports via Pushover notifications.

# Features

	•	Pomodoro Timer: A classic 25-minute work timer followed by short breaks, with a long break after every four sessions.
	•	Time Tracking: Records your focus time and saves it for later analysis.
	•	Weekly Reports: Sends a weekly notification to your phone using Pushover, summarizing your total focus time.
	•	Visual Stats: View daily focus time stats with a simple and clean bar chart.
	•	Customization: Easily change timer durations, sounds, and notification preferences.

Installation

	1.	Clone the repository:
    git clone https://github.com/yourusername/focus-tracker.git
    cd focus-tracker

	2.	Install required dependencies:
    pip install -r requirements.txt
    
    3.	Set up Pushover:
	•	Create a settings.py file in the root directory.
	•	Add your Pushover API token and user key:
    PUSHOVER_API_TOKEN = 'your_api_token'
    PUSHOVER_USER_KEY = 'your_user_key'
    
    4. Run the application:
    python focus_tracker.py

# Usage

	•	Starting the Timer: Press the “START” button to begin a Pomodoro session.
	•	Resetting: Press the “RESET” button to reset the current timer.
	•	View Stats: Press the “STATS” button to view your daily focus time in a bar chart.
	•	Weekly Reports: The app will automatically send a weekly focus time summary every Sunday at 10 AM.

# File Structure

	•	focus_tracker.py: Main Pomodoro timer application.
	•	pushover_notify.py: Handles sending notifications via Pushover.
	•	settings.py: Contains your Pushover API credentials (not included in the repository).
	•	focus_data.json: Stores your focus time data (automatically generated).

# Contributing

Contributions are welcome! If you have suggestions, please fork the repository and create a pull request. For major changes, please open an issue to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

Acknowledgments

	•	Pygame: For the game development framework.
	•	Pushover: For the notification service.
	•	Matplotlib: For creating visual stats.