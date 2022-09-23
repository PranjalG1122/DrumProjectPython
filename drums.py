import pygame
from pygame import mixer
pygame.init()

WIDTH = 1400
HEIGHT = 800

# Defining colors for later use

black = (0, 0, 0)
white = (255, 255, 255)
gray = (128, 128, 128)
dark_gray = (64, 64, 64)
green = (0, 255, 0)
red = (255, 0, 0)
gold = (212, 715, 55)
blue = (0, 255, 255)

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Beats Maker")
label_font = pygame.font.Font("Roboto-Bold.ttf", 32)
medium_font = pygame.font.Font('Roboto-Bold.ttf', 24)

# This is an area for defining variables that will be used later in the program
# -----Start-----

fps = 60
timer = pygame.time.Clock()
instruments = 6
beats = 8
boxes = []
# This creates a positional array with all values as -1
clicked = [[-1 for _ in range(beats)] for _ in range(instruments)]
# in order to change the state, we multiply by -1
bpm = 240
playing = True
active_length = 0  # Tells us how many beats we've played so far
active_beat = 0
beat_changed = True  # Tells us if our beats have changed

# -----End-----

# Loading in the sounds
hi_hat = mixer.Sound("sounds\hi_hat.wav")
snare = mixer.Sound("sounds\snare.wav")
kick = mixer.Sound("sounds\kick.wav")
crash = mixer.Sound("sounds\crash.wav")
clap = mixer.Sound("sounds\clap.wav")
floor_tom = mixer.Sound("sounds\\tom.wav")
pygame.mixer.set_num_channels(instruments * 3)


def draw_grid(clicks, beat):
    left_menu = pygame.draw.rect(screen, gray, [0, 0, 200, HEIGHT - 200], 5)
    bottom_menu = pygame.draw.rect(
        screen, dark_gray, [0, HEIGHT-200, WIDTH, 200], 5)
    boxes = []
    colors = [gray, white, gray]
    # This is to render the left box menu
    hi_hat_text = label_font.render("Hi-Hat", True, white)
    screen.blit(hi_hat_text, (30, 30))
    snare_text = label_font.render("Snare", True, white)
    screen.blit(snare_text, (30, 130))
    kick_text = label_font.render("Kick", True, white)
    screen.blit(kick_text, (30, 230))
    crash_text = label_font.render("Crash", True, white)
    screen.blit(crash_text, (30, 330))
    clap_text = label_font.render("Clap", True, white)
    screen.blit(clap_text, (30, 430))
    floor_tom_text = label_font.render("Floor Tom", True, white)
    screen.blit(floor_tom_text, (30, 530))

    for i in range(instruments):
        pygame.draw.line(screen, gray, (0, (i * 100 + 100)),
                         (200, (i * 100 + 100)), 5)

    for i in range(beats):
        for j in range(instruments):
            if clicks[j][i] == -1:  # This is to check current position state
                color = gray
            else:
                color = green
            # This rectangle is for the gray box
            rectangle = pygame.draw.rect(
                screen, color, [(i * ((WIDTH - 200) // beats) + 205), (j * 100) + 5, ((WIDTH - 200) // beats) - 10, ((HEIGHT - 200) // instruments) - 10], 0, 3)
            # This rectange is for the black outline of each box
            pygame.draw.rect(
                screen, black, [(i * ((WIDTH - 200) // beats) + 200), (j * 100), ((WIDTH - 200) // beats), ((HEIGHT - 200) // instruments)], 5, 5)
            boxes.append(((rectangle), (i, j)))

    # This displays the current beat as a aqua color
    beat_active = pygame.draw.rect(
        screen, blue, [beat * ((WIDTH - 200) // beats) + 200, 0, ((WIDTH - 200) // beats), instruments * 100], 5, 3)

    return boxes


def play_notes():
    for i in range(len(clicked)):
        if clicked[i][active_beat] == 1:  # If the beat is active, we will play the sound
            if i == 0:
                hi_hat.play()
            if i == 1:
                crash.play()
            if i == 2:
                snare.play()
            if i == 3:
                clap.play()
            if i == 4:
                kick.play()
            if i == 5:
                floor_tom.play()


run = True
while run:
    timer.tick(fps)
    screen.fill(black)
    boxes = draw_grid(clicked, active_beat)
    # This is for the lower menu
    play_pause_button = pygame.draw.rect(
        screen, gray, [50, HEIGHT - 150, 200, 100], 0, 5)  # This is to create the play/pause button
    play_text = label_font.render("Play/Pause", True, white)
    screen.blit(play_text, (70, HEIGHT-130))
    if playing:
        play_text_2 = label_font.render(
            "Playing", True, green)  # Renders if playing
    else:
        play_text_2 = label_font.render(
            "Paused", True, red)   # Renders if paused
    screen.blit(play_text_2, (70, HEIGHT-100))

    # Beats Per Minute Display
    bpm_rectangle = pygame.draw.rect(
        screen, gray, [300, HEIGHT - 150, 200, 100], 5, 5)
    bpm_text = medium_font.render("Beats Per Minute", True, white)
    screen.blit(bpm_text, (308, HEIGHT-130))
    bpm_text2 = label_font.render(f'{bpm}', True, white)
    screen.blit(bpm_text2, (370, HEIGHT-100))

    # BPM increment and decrement buttons
    bpm_up = pygame.draw.rect(screen, green, [510, HEIGHT - 150, 48, 48], 0, 5)
    bpm_down = pygame.draw.rect(screen, red, [510, HEIGHT - 100, 48, 48], 0, 5)
    increment_text = medium_font.render("+", True, white)
    screen.blit(increment_text, (528, HEIGHT-140))
    decrement_text = medium_font.render("-", True, white)
    screen.blit(decrement_text, (528, HEIGHT-90))

    if beat_changed:
        play_notes()
        beat_changed = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(boxes)):
                # This if statement is to check if the mouse pointer is colliding with the current box
                if boxes[i][0].collidepoint(event.pos):
                    coords = boxes[i][1]
                    # This is to change the box from gray to green by changing initial clicked array by multiplying by -1
                    clicked[coords[1]][coords[0]] *= -1
        if event.type == pygame.MOUSEBUTTONUP:
            # This is to check if the play/pause button is clicked
            if play_pause_button.collidepoint(event.pos):
                if playing:
                    playing = False
                elif not playing:
                    playing = True
            elif bpm_up.collidepoint(event.pos):
                bpm += 5
            elif bpm_down.collidepoint(event.pos):
                bpm -= 5

    beat_length = 3600 // bpm
    if playing:
        if active_length < beat_length:  # This is to check if the beat has finished
            active_length += 1           # Adds a beat
        else:
            active_length = 0
            if active_beat < beats - 1:
                active_beat += 1
                beat_changed = True
            else:
                active_beat = 0
                beat_changed = True

    pygame.display.flip()

pygame.quit()
