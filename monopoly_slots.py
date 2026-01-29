import pygame
import random

pygame.init()

# ---------- ЭКРАН ----------
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption("Монополия со слотами — 4 игрока")
clock = pygame.time.Clock()

FONT = pygame.font.SysFont("arial", 18)
BIG_FONT = pygame.font.SysFont("arial", 42)
SLOT_FONT = pygame.font.SysFont("arial", 36)

# ---------- ИГРОКИ ----------
PLAYERS = 4
player_pos = [0, 0, 0, 0]
player_colors = [(0, 200, 0), (200, 0, 0), (0, 0, 200), (200, 200, 0)]
current_player = 0
skip_turn = [False, False, False, False]

# ---------- ПОЛЕ ----------
BOARD_SIZE = 50  # количество клеток
CELL_SIZE = 60   # размер одной клетки
BOARD_MARGIN = 80
BOARD_SIDE = min(WIDTH - 400, HEIGHT - 2 * BOARD_MARGIN)  # квадратная доска, оставляем место под слоты
CELLS_PER_SIDE = BOARD_SIDE // CELL_SIZE  # количество клеток по стороне

# ---------- СЛОТЫ ----------
slot_values = [
    "+1 ход", "+1 ход", "+1 ход",
    "+2 хода", "+2 хода",
    "-1 ход",
    "-2 хода",
    "Пропуск"
]
current_slot = ["SPIN"] * PLAYERS
slot_rects = [pygame.Rect(WIDTH - 380, 60 + i * 180, 320, 160) for i in range(PLAYERS)]
spin_button = pygame.Rect(WIDTH - 360, HEIGHT - 120, 280, 80)

# ---------- ФУНКЦИИ ----------

def draw_board():
    positions = []

    # Нижняя сторона
    for i in range(CELLS_PER_SIDE):
        x = BOARD_MARGIN + i * CELL_SIZE
        y = HEIGHT - BOARD_MARGIN - CELL_SIZE
        positions.append((x, y))

    # Левая сторона
    for i in range(1, CELLS_PER_SIDE - 1):
        x = BOARD_MARGIN
        y = HEIGHT - BOARD_MARGIN - CELL_SIZE - i * CELL_SIZE
        positions.append((x, y))

    # Верхняя сторона
    for i in range(CELLS_PER_SIDE):
        x = BOARD_MARGIN + i * CELL_SIZE
        y = HEIGHT - BOARD_MARGIN - CELL_SIZE - (CELLS_PER_SIDE - 1) * CELL_SIZE
        positions.append((x, y))

    # Правая сторона
    for i in range(1, CELLS_PER_SIDE - 1):
        x = BOARD_MARGIN + (CELLS_PER_SIDE - 1) * CELL_SIZE
        y = HEIGHT - BOARD_MARGIN - CELL_SIZE - (CELLS_PER_SIDE - 1 - i) * CELL_SIZE
        positions.append((x, y))

    for idx, (x, y) in enumerate(positions):
        rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, (220, 220, 220), rect)
        pygame.draw.rect(screen, (0, 0, 0), rect, 2)

        # Номер клетки
        num_text = FONT.render(str(idx), True, (0, 0, 0))
        screen.blit(num_text, (rect.right - num_text.get_width() - 2, rect.bottom - num_text.get_height() - 2))

        # Игроки
        for p_idx, p in enumerate(range(PLAYERS)):
            if player_pos[p] == idx:
                offset_x = (p_idx % 2) * 20 + 10
                offset_y = (p_idx // 2) * 20 + 10
                pygame.draw.circle(screen, player_colors[p], (rect.left + offset_x, rect.top + offset_y), 10)

def draw_slots():
    for i in range(PLAYERS):
        rect = slot_rects[i]
        pygame.draw.rect(screen, (245, 245, 245), rect, border_radius=10)
        pygame.draw.rect(screen, (0, 0, 0), rect, 3, border_radius=10)

        label = BIG_FONT.render(f"Игрок {i + 1}", True, (0, 0, 0))
        screen.blit(label, (rect.x, rect.y - 40))

        text = SLOT_FONT.render(current_slot[i], True, (0, 0, 0))
        screen.blit(text, text.get_rect(center=rect.center))

        if i == current_player:
            pygame.draw.rect(screen, (0, 150, 255), rect, 4, border_radius=10)

def draw_button():
    pygame.draw.rect(screen, (0, 140, 255), spin_button, border_radius=14)
    text = BIG_FONT.render("SPIN", True, (255, 255, 255))
    screen.blit(text, text.get_rect(center=spin_button.center))

def show_winner(player):
    screen.fill((255, 255, 255))
    msg = BIG_FONT.render(f"Игрок {player + 1} победил!", True, (0, 0, 0))
    screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2 - msg.get_height() // 2))
    pygame.display.flip()
    pygame.time.delay(5000)
    pygame.quit()
    exit()

def animate_slot(player):
    global current_player

    rect = slot_rects[player]
    y = rect.top - 50
    result = random.choice(slot_values)

    start = pygame.time.get_ticks()
    while pygame.time.get_ticks() - start < 1000:
        screen.fill((255, 255, 255))
        draw_board()
        draw_slots()
        draw_button()

        temp = random.choice(slot_values)
        txt = SLOT_FONT.render(temp, True, (0, 0, 0))
        screen.blit(txt, (rect.centerx - txt.get_width() // 2, y))

        y += 30
        if y > rect.bottom:
            y = rect.top - 50

        pygame.display.flip()
        clock.tick(60)

    current_slot[player] = result

    # --- эффект слота ---
    if result == "+1 ход":
        player_pos[player] += 1
    elif result == "+2 хода":
        player_pos[player] += 2
    elif result == "-1 ход":
        player_pos[player] -= 1
    elif result == "-2 хода":
        player_pos[player] -= 2
    elif result == "Пропуск":
        skip_turn[player] = True

    if player_pos[player] < 0:
        player_pos[player] = 0

    if player_pos[player] >= BOARD_SIZE - 1:
        player_pos[player] = BOARD_SIZE - 1
        show_winner(player)
        return

    current_player = (current_player + 1) % PLAYERS

# ---------- ЦИКЛ ----------
running = True
while running:
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and spin_button.collidepoint(event.pos):
            if not skip_turn[current_player]:
                animate_slot(current_player)
            else:
                skip_turn[current_player] = False
                current_player = (current_player + 1) % PLAYERS

    draw_board()
    draw_slots()
    draw_button()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
