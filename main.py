import pygame
import math
import random

# setup display
pygame.init()
WIDTH, HEIGHT = 800, 500
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman game by Megatrons")

FPS = 60

font_name = pygame.font.match_font("arial")

# button variables
RADIUS = 20
GAP = 15
letters = []  # [x,y,letter]
startx = round((WIDTH - (RADIUS * 2 + GAP) * 13) / 2)
starty = 400
A = 65
for i in range(26):
    x = startx + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
    y = starty + ((i // 13) * (GAP + RADIUS * 2))
    letters.append([x, y, chr(A + i), True])

# fonts
LETTER_FONT = pygame.font.SysFont('comicsans', 40)
WORD_FONT = pygame.font.SysFont('comicsans', 60)
TITLE_FONT = pygame.font.SysFont('comicsans', 70)
# load images
images = []
for i in range(7):
    image = pygame.image.load("hangman" + str(i) + ".png")
    images.append(image)

# game variables
hangman_status = 0
words = ["JAVA", "RUBY", "HTML", "C", "PYGAME", "CSS", "JAVASCRIPT", "PYTHON", "SPRITES", "HANGMAN"]
# words = ["C"]

word = random.choice(words)
guessed = []

# colors
WHITE = (255, 100, 10)
BLACK = (0, 0, 0)

bg = pygame.image.load("ppu.jpg")


def reset():
    global letters, word, guessed
    letters = []
    for i in range(26):
        x = startx + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
        y = starty + ((i // 13) * (GAP + RADIUS * 2))
        letters.append([x, y, chr(A + i), True])

    word = random.choice(words)
    guessed = []



def draw_text(surf, text, size, x, y, color = WHITE):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def wait():
    while True:

        keystate = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        if keystate[pygame.K_r]:
            return 1
        if keystate[pygame.K_ESCAPE]:
            pygame.quit()



def draw():
    win.blit(bg, (0, 0))

    # draw title
    text = TITLE_FONT.render("Hangman", 1, BLACK)
    win.blit(text, (WIDTH / 2 - text.get_width() / 2, 20))

    # draw word
    display_word = ""
    for letter in word:
        if letter in guessed:
            display_word += letter + " "
        else:
            display_word += "_ "
    text = WORD_FONT.render(display_word, 1, BLACK)
    win.blit(text, (400, 200))

    # draw buttons
    for letter in letters:
        x, y, ltr, visible = letter
        if visible:
            pygame.draw.circle(win, BLACK, (x, y), RADIUS, 3)
            text = LETTER_FONT.render(ltr, 1, BLACK)
            win.blit(text, (x - text.get_width() / 2, y - text.get_width() / 2))

    win.blit(images[hangman_status], (150, 100))
    pygame.display.update()


def display_message(message):
    pygame.time.delay(1000)
    win.fill(WHITE)
    text = WORD_FONT.render(message, 1, BLACK)
    win.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
    draw_text(win, "Press 'R' to Play Again", 15, WIDTH // 2, HEIGHT // 2 + 30, BLACK)
    pygame.display.update()
    # pygame.time.delay(5000)

def main():
    global hangman_status, word, guessed
    # setup game loop
    clock = pygame.time.Clock()
    run = True
    won = False

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = pygame.mouse.get_pos()
                for letter in letters:
                    x, y, ltr, visible = letter
                    if visible:
                        dis = math.sqrt((x - m_x) ** 2 + (y - m_y) ** 2)
                        if dis < RADIUS:
                            letter[3] = False
                            guessed.append(ltr)
                            if ltr not in word:
                                hangman_status += 1

        if not won:
            draw()

        for letter in word:
            if letter not in guessed:
                won = False
                break
        else:
            won = True

        if won:
            display_message("You Won!!")
            wait()
            reset()
            won = False
            hangman_status = 0


        if hangman_status == 6:
            display_message("Lost!! The word was " + word)
            wait()
            reset()
            won = False
            hangman_status = 0


main()
pygame.quit()