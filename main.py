import pygame
import sys
from sudoku_generator import generate_sudoku
from cell import Cell

# Constants
WINDOW_WIDTH, WINDOW_HEIGHT = 540, 600
GRID_SIZE = 9
CELL_SIZE = WINDOW_WIDTH // GRID_SIZE
MENU_HEIGHT = 60
FPS = 60

EASY_CELLS = 30
MEDIUM_CELLS = 40
HARD_CELLS = 50

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
LIGHT_BLUE = (173, 216, 230)

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Sudoku")
clock = pygame.time.Clock()


def draw_text(text, font_size, color, center):
    font = pygame.font.SysFont(None, font_size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=center)
    screen.blit(text_surface, text_rect)


def draw_menu():
    screen.fill(WHITE)
    draw_text("Select Difficulty", 50, BLUE, (WINDOW_WIDTH // 2, 100))

    easy_btn = pygame.Rect(WINDOW_WIDTH // 2 - 100, 180, 200, 50)
    medium_btn = pygame.Rect(WINDOW_WIDTH // 2 - 100, 260, 200, 50)
    hard_btn = pygame.Rect(WINDOW_WIDTH // 2 - 100, 340, 200, 50)

    pygame.draw.rect(screen, LIGHT_BLUE, easy_btn)
    pygame.draw.rect(screen, LIGHT_BLUE, medium_btn)
    pygame.draw.rect(screen, LIGHT_BLUE, hard_btn)

    draw_text("Easy", 36, BLACK, easy_btn.center)
    draw_text("Medium", 36, BLACK, medium_btn.center)
    draw_text("Hard", 36, BLACK, hard_btn.center)

    pygame.display.update()
    return easy_btn, medium_btn, hard_btn


def select_difficulty():
    while True:
        easy_btn, medium_btn, hard_btn = draw_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if easy_btn.collidepoint(event.pos):
                    return EASY_CELLS
                elif medium_btn.collidepoint(event.pos):
                    return MEDIUM_CELLS
                elif hard_btn.collidepoint(event.pos):
                    return HARD_CELLS
        clock.tick(FPS)


def draw_grid():
    for i in range(GRID_SIZE + 1):
        line_width = 3 if i % 3 == 0 else 1
        pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE), (WINDOW_WIDTH, i * CELL_SIZE), line_width)
        pygame.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, WINDOW_WIDTH), line_width)


def create_cells(board):
    return [[Cell(board[row][col], row, col, screen) for col in range(GRID_SIZE)] for row in range(GRID_SIZE)]


def draw_board(cells):
    screen.fill(WHITE)
    draw_grid()
    for row in cells:
        for cell in row:
            cell.draw(CELL_SIZE, CELL_SIZE)
    pygame.display.update()


def main():
    removed_cells = select_difficulty()
    board = generate_sudoku(9, removed_cells)
    cells = create_cells(board)

    running = True
    while running:
        draw_board(cells)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
