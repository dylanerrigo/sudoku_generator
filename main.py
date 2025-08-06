
import pygame
import sys
from sudoku_generator import SudokuGenerator
from cell import Cell
import os

def is_board_full(cells):
    for row in cells:
        for cell in row:
            if cell.value == 0:
                return False
    return True

def show_end_screen(message, button_text):
    screen.fill(WHITE)
    draw_text(message, 60, BLACK, (WINDOW_WIDTH // 2, WINDOW_WIDTH // 2 - 50))

    button_rect = pygame.Rect(WINDOW_WIDTH // 2 - 60, WINDOW_WIDTH // 2 + 20, 120, 50)
    pygame.draw.rect(screen, (255, 128, 0), button_rect)
    draw_text(button_text, 28, WHITE, button_rect.center)

    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    waiting = False

WINDOW_WIDTH, WINDOW_HEIGHT = 540, 600
GRID_SIZE = 9
CELL_SIZE = WINDOW_WIDTH // GRID_SIZE
MENU_HEIGHT = 60
FPS = 60

EASY_CELLS = 30
MEDIUM_CELLS = 40
HARD_CELLS = 50

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
LIGHT_BLUE = (173, 216, 230)
RED = (255, 0, 0)

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

class Button:
    def __init__(self, rect, text, bg_color=LIGHT_BLUE, text_color=BLACK):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.bg_color = bg_color
        self.text_color = text_color

    def draw(self, surface):
        pygame.draw.rect(surface, self.bg_color, self.rect)
        draw_text(self.text, 24, self.text_color, self.rect.center)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

def main():
    game_state = "MENU"
    difficulty_cells = 0
    original_board = None
    solution_board = None
    cells = None

    easy_btn, medium_btn, hard_btn = None, None, None

    reset_button = Button((50, WINDOW_WIDTH + 20, 120, 40), "Reset")
    restart_button = Button((210, WINDOW_WIDTH + 20, 120, 40), "Restart")
    exit_button = Button((370, WINDOW_WIDTH + 20, 120, 40), "Exit")

    selected_cell = None

    running = True
    while running:
        clock.tick(FPS)

        if game_state == "MENU":
            easy_btn, medium_btn, hard_btn = draw_menu()
        elif game_state == "PLAYING":
            draw_board(cells)
            reset_button.draw(screen)
            restart_button.draw(screen)
            exit_button.draw(screen)
            pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if game_state == "MENU":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if easy_btn and easy_btn.collidepoint(event.pos):
                        difficulty_cells = EASY_CELLS
                    elif medium_btn and medium_btn.collidepoint(event.pos):
                        difficulty_cells = MEDIUM_CELLS
                    elif hard_btn and hard_btn.collidepoint(event.pos):
                        difficulty_cells = HARD_CELLS
                    else:
                        continue

                    generator = SudokuGenerator(difficulty_cells)
                    generator.fill_values()
                    solution_board = [row[:] for row in generator.get_board()]
                    generator.remove_cells()
                    original_board = generator.get_board()
                    cells = create_cells(original_board)
                    game_state = "PLAYING"

            elif game_state == "PLAYING":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos

                    if reset_button.is_clicked(pos):
                        for r in range(GRID_SIZE):
                            for c in range(GRID_SIZE):
                                cells[r][c].value = original_board[r][c]
                                cells[r][c].sketched_value = 0
                        selected_cell = None

                    elif restart_button.is_clicked(pos):
                        generator = SudokuGenerator(difficulty_cells)
                        generator.fill_values()
                        solution_board = [row[:] for row in generator.get_board()]
                        generator.remove_cells()
                        original_board = generator.get_board()
                        cells = create_cells(original_board)
                        selected_cell = None

                    elif exit_button.is_clicked(pos):
                        game_state = "MENU"
                        selected_cell = None

                    else:
                        x, y = pos
                        if x < WINDOW_WIDTH and y < WINDOW_WIDTH:
                            col = x // CELL_SIZE
                            row = y // CELL_SIZE
                            selected_cell = (row, col)
                            for r in range(GRID_SIZE):
                                for c in range(GRID_SIZE):
                                    cells[r][c].selected = False
                            cells[row][col].selected = True

                elif event.type == pygame.KEYDOWN and selected_cell:
                    row, col = selected_cell
                    cell = cells[row][col]

                    if event.key in [pygame.K_1, pygame.K_2, pygame.K_3,
                                     pygame.K_4, pygame.K_5, pygame.K_6,
                                     pygame.K_7, pygame.K_8, pygame.K_9]:
                        number = int(event.unicode)
                        if original_board[row][col] == 0:
                            cell.set_cell_value(number)
                        pygame.display.update()

                    elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                        if original_board[row][col] == 0:
                            cell.clear()
                        pygame.display.update()

                    if is_board_full(cells):
                        player_board = [[cells[r][c].value for c in range(GRID_SIZE)] for r in range(GRID_SIZE)]
                        if player_board == solution_board:
                            show_end_screen("Game Won!", "EXIT")
                            pygame.quit()
                            sys.exit()
                        else:
                            show_end_screen("Game Over :(", "RESTART")
                            game_state = "MENU"

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
