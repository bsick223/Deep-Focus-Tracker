# To-do 
# add a long break sound for timer
# Done, highlight the state we are in
# do the 4 rounds of pomodoro then a long break
# be able to save progress

import pygame
import sys
from button import Button
import json

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

POMODORO_LENGTH = 5  # 1500 secs / 25 mins
SHORT_BREAK_LENGTH = 3  # 300 secs / 5 mins
LONG_BREAK_LENGTH = 9  # 900 secs / 15 mins

def save_progress(total_time):
    with open("focus_data.json", "w") as file:
        json.dump({"total_focus_time": total_time}, file)

def load_progress():
    try:
        with open("focus_data.json", "r") as file:
            data = file.read().strip()  # Read the file content
            if not data:  # Check if the file is empty
                return 0
            return json.loads(data).get("total_focus_time", 0)
    except (FileNotFoundError, json.JSONDecodeError):  # Handle missing or invalid JSON files
        return 0

total_focus_time = load_progress()

current_seconds = POMODORO_LENGTH
state = "POMODORO"  # Can be "POMODORO", "SHORT_BREAK", "LONG_BREAK"
pomodoro_count = 0  # Track completed Pomodoros

pygame.time.set_timer(pygame.USEREVENT, 1000)  # 1000 milliseconds will return True
started = False

def draw_pomodoro_indicators(screen, count):
    for i in range(4):
        color = "#FFD700" if i < count else "#666666"  # Filled or empty indicator
        pygame.draw.circle(screen, color, (WIDTH//2 + i*40 - 60, HEIGHT//2 + 160), 15)

def format_time(seconds):
    mins, secs = divmod(seconds, 60)
    hrs, mins = divmod(mins, 60)
    return f"{hrs}h {mins}m {secs}s"

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_progress(total_focus_time)
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if START_STOP_BUTTON.check_for_input(pygame.mouse.get_pos()):
                started = not started  # Toggle the started state
            if POMODORO_BUTTON.check_for_input(pygame.mouse.get_pos()):
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
            else:
                if state == "POMODORO":
                    total_focus_time += POMODORO_LENGTH
                    pomodoro_count += 1
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

    START_STOP_BUTTON.update(SCREEN)
    START_STOP_BUTTON.change_color(pygame.mouse.get_pos())
    POMODORO_BUTTON.update(SCREEN)
    POMODORO_BUTTON.change_color(pygame.mouse.get_pos())
    SHORT_BREAK_BUTTON.update(SCREEN)
    SHORT_BREAK_BUTTON.change_color(pygame.mouse.get_pos())
    LONG_BREAK_BUTTON.update(SCREEN)
    LONG_BREAK_BUTTON.change_color(pygame.mouse.get_pos())

    if current_seconds >= 0:
        display_seconds = current_seconds % 60
        display_minutes = int(current_seconds // 60)
        timer_text = FONT.render(f"{display_minutes:02}:{display_seconds:02}", True, "white")
    else:
        timer_text = FONT.render("00:00", True, "white")
    
    SCREEN.blit(timer_text, timer_text_rect)

    pygame.display.update()
    CLOCK.tick(60)