
import pygame
import sys
from button import Button

pygame.init()

WIDTH, HEIGHT = 900, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pomodoro Timer")

CLOCK = pygame.time.Clock()

BACKDROP = pygame.image.load("assets/backdrop.png")
WHITE_BUTTON = pygame.image.load("assets/button.png")

FONT = pygame.font.Font("assets/ArialRoundedMTBold.ttf", 120)
timer_text = FONT.render("25:00", True, "white")
timer_text_rect = timer_text.get_rect(center=(WIDTH/2, HEIGHT/2-25))

START_STOP_BUTTON = Button(WHITE_BUTTON, (WIDTH/2, HEIGHT/2+100), 170, 60, "START", 
                    pygame.font.Font("assets/ArialRoundedMTBold.ttf", 20), "#c97676", "#9ab034")
POMODORO_BUTTON = Button(None, (WIDTH/2-150, HEIGHT/2-140), 120, 30, "Pomodoro", 
                    pygame.font.Font("assets/ArialRoundedMTBold.ttf", 20), "#FFFFFF", "#9ab034")
SHORT_BREAK_BUTTON = Button(None, (WIDTH/2, HEIGHT/2-140), 120, 30, "Short Break", 
                    pygame.font.Font("assets/ArialRoundedMTBold.ttf", 20), "#FFFFFF", "#9ab034")
LONG_BREAK_BUTTON = Button(None, (WIDTH/2+150, HEIGHT/2-140), 120, 30, "Long Break", 
                    pygame.font.Font("assets/ArialRoundedMTBold.ttf", 20), "#FFFFFF", "#9ab034")

POMODORO_LENGTH = 15  # 1500 secs / 25 mins
SHORT_BREAK_LENGTH = 3  # 300 secs / 5 mins
LONG_BREAK_LENGTH = 9  # 900 secs / 15 mins

current_seconds = POMODORO_LENGTH
started = False

# Introduce state management
state = "POMODORO"  # Can be "POMODORO", "SHORT_BREAK", "LONG_BREAK"

pygame.time.set_timer(pygame.USEREVENT, 1000)  # 1000 milliseconds will return True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if START_STOP_BUTTON.check_for_input(pygame.mouse.get_pos()):
                started = not started  # Toggle the started state
            if POMODORO_BUTTON.check_for_input(pygame.mouse.get_pos()):
                state = "POMODORO"
                current_seconds = POMODORO_LENGTH
            if SHORT_BREAK_BUTTON.check_for_input(pygame.mouse.get_pos()):
                state = "SHORT_BREAK"
                current_seconds = SHORT_BREAK_LENGTH
            if LONG_BREAK_BUTTON.check_for_input(pygame.mouse.get_pos()):
                state = "LONG_BREAK"
                current_seconds = LONG_BREAK_LENGTH

        if event.type == pygame.USEREVENT and started:
            if current_seconds > 0:
                current_seconds -= 1
            else:
                if state == "POMODORO":
                    state = "SHORT_BREAK"
                    current_seconds = SHORT_BREAK_LENGTH
                elif state == "SHORT_BREAK":
                    state = "POMODORO"
                    current_seconds = POMODORO_LENGTH
                elif state == "LONG_BREAK":
                    state = "POMODORO"
                    current_seconds = POMODORO_LENGTH

    minutes = current_seconds // 60
    seconds = current_seconds % 60
    timer_text = FONT.render(f"{minutes:02}:{seconds:02}", True, "white")

    SCREEN.blit(BACKDROP, (0, 0))
    SCREEN.blit(timer_text, timer_text_rect)
    START_STOP_BUTTON.update(SCREEN)
    POMODORO_BUTTON.update(SCREEN)
    SHORT_BREAK_BUTTON.update(SCREEN)
    LONG_BREAK_BUTTON.update(SCREEN)

    pygame.display.update()
    CLOCK.tick(60)
