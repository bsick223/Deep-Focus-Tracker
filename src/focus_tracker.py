# To-Do
# Fix the crash report / create the auto save
# when goal achieved play a video of self dancing

import pygame
import sys
from button import Button
import json
from datetime import datetime
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import os

# Set the working directory to the directory of the script
os.chdir(os.path.dirname(os.path.abspath(__file__)))

pygame.init()

# Load sound files
break_sound = pygame.mixer.Sound("assets/Calm Alarm.wav")
pomodoro_sound = pygame.mixer.Sound("assets/Finish Alarm.wav")
# long_break = 

# Set the opacity (0 is fully transparent, 255 is fully opaque)
opacity = 40


WIDTH, HEIGHT = 900, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pomodoro Timer")

CLOCK = pygame.time.Clock()

BACKDROP = pygame.image.load("assets/backdrop.png")
WHITE_BUTTON = pygame.image.load("assets/button.png")

FONT = pygame.font.Font("assets/ArialRoundedMTBold.ttf", 120)
timer_text = FONT.render("25:00", True, "white")
timer_text_rect = timer_text.get_rect(center=(WIDTH/2, HEIGHT/2-25))


# initialize the buttons
START_STOP_BUTTON = Button(WHITE_BUTTON, (WIDTH/2, HEIGHT/2+100), 170, 60, "START", 
                           pygame.font.Font("assets/ArialRoundedMTBold.ttf", 20), "#c97676", "#9ab034")
POMODORO_BUTTON = Button(None, (WIDTH/2-150, HEIGHT/2-140), 120, 30, "Pomodoro", 
                         pygame.font.Font("assets/ArialRoundedMTBold.ttf", 20), "#FFFFFF", "#9ab034")
SHORT_BREAK_BUTTON = Button(None, (WIDTH/2, HEIGHT/2-140), 120, 30, "Short Break", 
                            pygame.font.Font("assets/ArialRoundedMTBold.ttf", 20), "#FFFFFF", "#9ab034")
LONG_BREAK_BUTTON = Button(None, (WIDTH/2+150, HEIGHT/2-140), 120, 30, "Long Break", 
                           pygame.font.Font("assets/ArialRoundedMTBold.ttf", 20), "#FFFFFF", "#9ab034")
RESET_BUTTON = Button(WHITE_BUTTON, (WIDTH/2, HEIGHT/2+180), 170, 60, "RESET", 
                      pygame.font.Font("assets/ArialRoundedMTBold.ttf", 20), "#c97676", "#9ab034")
STATS_BUTTON = Button(WHITE_BUTTON, (WIDTH/2, HEIGHT/2+260), 170, 60, "STATS", 
                      pygame.font.Font("assets/ArialRoundedMTBold.ttf", 20), "#c97676", "#9ab034")

POMODORO_LENGTH = 1500  # 1500 secs / 25 mins
SHORT_BREAK_LENGTH = 300  # 300 secs / 5 mins
LONG_BREAK_LENGTH = 1200  # 1200 secs / 20 mins

# Track time in the current Pomodoro session
accumulated_seconds = 0  

def save_progress(daily_focus_time, total_focus_time):
    with open("focus_data.json", "w") as file:
        json.dump({
            "total_focus_time": total_focus_time,
            "daily_focus_time": daily_focus_time  # Save the daily focus time correctly
        }, file)

def load_progress():
    try:
        with open("focus_data.json", "r") as file:
            data = file.read().strip()
            if not data:
                return {}, 0  # Return empty dictionary and 0 total time if no data
            loaded_data = json.loads(data)
            daily_time = loaded_data.get("daily_focus_time", {})
            total_time = loaded_data.get("total_focus_time", 0)
            return daily_time, total_time
    except (FileNotFoundError, json.JSONDecodeError):
        return {}, 0
    
def show_stats():
    dates = list(daily_focus_time.keys())
    focus_times = [time / 60 for time in daily_focus_time.values()]  # Convert seconds to minutes
    
    plt.bar(dates, focus_times)
    plt.xlabel('Date')
    plt.ylabel('Focus Time (minutes)')
    plt.title('Daily Focus Time')
    plt.show()
    
def get_weekly_focus_time(daily_focus_time):
    # Get the current date
    today = datetime.now().date()

    # Calculate the start of the week (assuming week starts on Monday)
    start_of_week = today - timedelta(days=today.weekday())

    # Sum the focus time for each day of the current week
    weekly_focus_time = 0.0
    for date_str, focus_time in daily_focus_time.items():
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
        if start_of_week <= date <= today:
            weekly_focus_time += focus_time

    # Convert to floating-point hours
    return weekly_focus_time / 3600.0  # Convert from seconds to hours

daily_focus_time, total_focus_time = load_progress()

current_date = datetime.now().strftime("%Y-%m-%d")
if current_date not in daily_focus_time:
    daily_focus_time[current_date] = 0

current_seconds = POMODORO_LENGTH
state = "POMODORO"  # Can be "POMODORO", "SHORT_BREAK", "LONG_BREAK"
pomodoro_count = 0

pygame.time.set_timer(pygame.USEREVENT, 1000)  # 1000 milliseconds will return True
started = False

def draw_pomodoro_indicators(screen, count):
    for i in range(4):
        color = "#FFD700" if i < count else "#666666"  # Filled or empty indicator
        pygame.draw.circle(screen, color, (WIDTH//2 + i*40 - 60, HEIGHT//2 + 160), 15)



# def format_time(seconds):
#     mins, secs = divmod(seconds, 60)
#     hrs, mins = divmod(mins, 60)
#     return f"{hrs}h {mins}m {secs}s"

def main():
    global started, accumulated_seconds, pomodoro_count, current_seconds, state, total_focus_time

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if started and state == "POMODORO":  # Check if the timer is running and in Pomodoro state
                    elapsed_time = last_seconds - current_seconds
                    accumulated_seconds += elapsed_time
                    total_focus_time += accumulated_seconds
                    daily_focus_time[current_date] += accumulated_seconds
                save_progress(daily_focus_time, total_focus_time)
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if START_STOP_BUTTON.check_for_input(pygame.mouse.get_pos()):
                    if started:
                        # Timer is being stopped, add accumulated time to total
                        if state == "POMODORO":
                            total_focus_time += accumulated_seconds
                            daily_focus_time[current_date] += accumulated_seconds
                    started = not started  # Toggle the started state
                    last_seconds = current_seconds  # Reset last_seconds when starting or stopping
                    accumulated_seconds = 0  # Reset accumulated time on stop/start
                    
                if RESET_BUTTON.check_for_input(pygame.mouse.get_pos()):
                    if state == 'POMODORO':
                        accumulated_seconds = 0 
                        current_seconds = POMODORO_LENGTH # Reset the timer to the initial Pomodoro length
                    elif state == 'SHORT_BREAK':
                        current_seconds = SHORT_BREAK_LENGTH
                    elif state == 'LONG_BREAK':
                        current_seconds = LONG_BREAK_LENGTH
                    started = False  # Stop the timer
                if STATS_BUTTON.check_for_input(pygame.mouse.get_pos()):
                    show_stats()
                if POMODORO_BUTTON.check_for_input(pygame.mouse.get_pos()):
                    accumulated_seconds = 0
                    current_seconds = POMODORO_LENGTH
                    started = False
                    state = "POMODORO"
                if SHORT_BREAK_BUTTON.check_for_input(pygame.mouse.get_pos()):
                    current_seconds = SHORT_BREAK_LENGTH
                    started = False
                    state = "SHORT_BREAK"
                if LONG_BREAK_BUTTON.check_for_input(pygame.mouse.get_pos()):
                    current_seconds = LONG_BREAK_LENGTH
                    started = False
                    state = "LONG_BREAK"

                if started:
                    START_STOP_BUTTON.text_input = "STOP"
                else:
                    START_STOP_BUTTON.text_input = "START"
                
                START_STOP_BUTTON.text = pygame.font.Font("assets/ArialRoundedMTBold.ttf", 20).render(
                    START_STOP_BUTTON.text_input, True, START_STOP_BUTTON.base_color)
                    
            if event.type == pygame.USEREVENT and started:
                if current_seconds > 0:
                    current_seconds -= 1
                    if state == "POMODORO":
                        elapsed_time = last_seconds - current_seconds
                        accumulated_seconds += elapsed_time  # Add to accumulated time
                        last_seconds = current_seconds
                else:
                    if state == "POMODORO":
                        total_focus_time += accumulated_seconds
                        daily_focus_time[current_date] += accumulated_seconds
                        pomodoro_count += 1
                        accumulated_seconds = 0
                        if pomodoro_count < 4:
                            state = "SHORT_BREAK"
                            current_seconds = SHORT_BREAK_LENGTH
                            break_sound.play()
                        else:
                            state = "LONG_BREAK"
                            current_seconds = LONG_BREAK_LENGTH
                            break_sound.play()
                            pomodoro_count = 0  # Reset after the long break
                    elif state == "SHORT_BREAK":
                        state = "POMODORO"
                        current_seconds = POMODORO_LENGTH
                        pomodoro_sound.play()
                    elif state == "LONG_BREAK":
                        state = "POMODORO"
                        current_seconds = POMODORO_LENGTH
                        pomodoro_sound.play()
            

        SCREEN.fill("#ba4949")
        SCREEN.blit(BACKDROP, BACKDROP.get_rect(center=(WIDTH/2, HEIGHT/2)))
        
        draw_pomodoro_indicators(SCREEN, pomodoro_count)
        
        # Draw the highlight around the active button
        if state == "POMODORO":
            # pygame.draw.rect(SCREEN, "#FFD700", POMODORO_BUTTON.rect.inflate(10, 10), border_radius=12)
            highlight_surface = pygame.Surface(POMODORO_BUTTON.rect.inflate(10, 10).size, pygame.SRCALPHA)
            highlight_surface.set_alpha(opacity)  # Set the opacity (0 is fully transparent, 255 is fully opaque)
            pygame.draw.rect(highlight_surface, (255, 215, 0), highlight_surface.get_rect(), border_radius=12)
            SCREEN.blit(highlight_surface, POMODORO_BUTTON.rect.inflate(10, 10).topleft)
        elif state == "SHORT_BREAK":
            # pygame.draw.rect(SCREEN, "#FFD700", SHORT_BREAK_BUTTON.rect.inflate(10, 10), border_radius=12)
            highlight_surface = pygame.Surface(SHORT_BREAK_BUTTON.rect.inflate(10, 10).size, pygame.SRCALPHA)
            highlight_surface.set_alpha(opacity)
            pygame.draw.rect(highlight_surface, (255, 215, 0), highlight_surface.get_rect(), border_radius=12)
            SCREEN.blit(highlight_surface, SHORT_BREAK_BUTTON.rect.inflate(10, 10).topleft)
        elif state == "LONG_BREAK":
            # pygame.draw.rect(SCREEN, "#FFD700", LONG_BREAK_BUTTON.rect.inflate(10, 10), border_radius=12)
            highlight_surface = pygame.Surface(LONG_BREAK_BUTTON.rect.inflate(10, 10).size, pygame.SRCALPHA)
            highlight_surface.set_alpha(opacity)
            pygame.draw.rect(highlight_surface, (255, 215, 0), highlight_surface.get_rect(), border_radius=12)
            SCREEN.blit(highlight_surface, LONG_BREAK_BUTTON.rect.inflate(10, 10).topleft)

        RESET_BUTTON.update(SCREEN)
        RESET_BUTTON.change_color(pygame.mouse.get_pos())
        START_STOP_BUTTON.update(SCREEN)
        START_STOP_BUTTON.change_color(pygame.mouse.get_pos())
        POMODORO_BUTTON.update(SCREEN)
        POMODORO_BUTTON.change_color(pygame.mouse.get_pos())
        SHORT_BREAK_BUTTON.update(SCREEN)
        SHORT_BREAK_BUTTON.change_color(pygame.mouse.get_pos())
        LONG_BREAK_BUTTON.update(SCREEN)
        LONG_BREAK_BUTTON.change_color(pygame.mouse.get_pos())
        STATS_BUTTON.update(SCREEN)  
        STATS_BUTTON.change_color(pygame.mouse.get_pos())

        if current_seconds >= 0:
            display_seconds = current_seconds % 60
            display_minutes = int(current_seconds // 60)
            timer_text = FONT.render(f"{display_minutes:02}:{display_seconds:02}", True, "white")
        else:
            timer_text = FONT.render("00:00", True, "white")
        
        SCREEN.blit(timer_text, timer_text_rect)

        pygame.display.update()
        CLOCK.tick(60)

if __name__ == "__main__":
    main()