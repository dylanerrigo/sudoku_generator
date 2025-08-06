import pygame
import math
from cell import Cell
from sudoku_generator import generate_sudoku, SudokuGenerator

pygame.init()

def create_new_game(difficulty):
    global board, cells, sudoku_validator, selected_row, selected_col, ROWS, COLS, CELL_WIDTH, CELL_HEIGHT

    size = DIFFICULTY_SETTINGS[difficulty]["size"]
    removed = DIFFICULTY_SETTINGS[difficulty]["removed"]

    ROWS, COLS = size, size
    CELL_WIDTH = WIDTH // COLS
    CELL_HEIGHT = (HEIGHT - 60) // ROWS

    board = generate_sudoku(size, removed)
    cells = [[Cell(board[r][c], r, c, screen) for c in range(COLS)] for r in range(ROWS)]

    sudoku_validator = SudokuGenerator(removed, size)
    sudoku_validator.fill_values()
    selected_row, selected_col = None, None

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku")

FONT = pygame.font.SysFont(None, 36)
SMALL_FONT = pygame.font.SysFont(None, 24)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (50, 50, 50)
RED = (255, 0, 0)
GREEN = (0, 180, 0)
BLUE = (0, 0, 255)

DIFFICULTY_SETTINGS = {
    "easy": {"size": 6, "removed": 10},
    "medium": {"size": 9, "removed": 40},
    "hard": {"size": 12, "removed": 70}
}

class Button:
    def __init__(self, x, y, w, h, text, color=LIGHT_GRAY, hover_color=DARK_GRAY, text_color=BLACK):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(surface, self.hover_color, self.rect)
        else:
            pygame.draw.rect(surface, self.color, self.rect)

        text_surf = FONT.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)

button_width, button_height = 140, 50
spacing = 20
start_y = HEIGHT // 2 - button_height // 2

total_width = button_width * 3 + spacing * 2
start_x = (WIDTH - total_width) // 2

easy_button = Button(start_x, start_y, button_width, button_height, "Easy", color=GREEN)
medium_button = Button(start_x + button_width + spacing, start_y, button_width, button_height, "Medium", color=BLUE)
hard_button = Button(start_x + 2 * (button_width + spacing), start_y, button_width, button_height, "Hard", color=RED)

reset_button = Button(10, HEIGHT - 50, 100, 40, "Reset")
restart_button = Button(WIDTH // 2 - 50, HEIGHT - 50, 100, 40, "Restart")
exit_button = Button(WIDTH - 110, HEIGHT - 50, 100, 40, "Exit")

gameover_restart_button = Button(WIDTH // 2 - 50, HEIGHT // 2 + 50, 100, 40, "Restart")
gamewon_exit_button = Button(WIDTH // 2 - 50, HEIGHT // 2 + 50, 100, 40, "Exit")

game_state = "MENU"
selected_row, selected_col = None, None
cells = []
board = []
sudoku_validator = None
removed_cells = 40

def create_new_game(difficulty_removed):
    global board, cells, sudoku_validator, selected_row, selected_col, removed_cells
    removed_cells = difficulty_removed
    board = generate_sudoku(9, removed_cells)
    cells = [[Cell(board[r][c], r, c, screen) for c in range(COLS)] for r in range(ROWS)]

    sudoku_validator = SudokuGenerator(removed_cells, 9)
    sudoku_validator.fill_values()
    selected_row, selected_col = None, None

def draw_grid():
    box_length = int(math.sqrt(ROWS))
    for i in range(ROWS + 1):
        lw = 3 if i % box_length == 0 else 1
        pygame.draw.line(screen, BLACK, (0, i * CELL_HEIGHT), (WIDTH, i * CELL_HEIGHT), lw)
        pygame.draw.line(screen, BLACK, (i * CELL_WIDTH, 0), (i * CELL_WIDTH, ROWS * CELL_HEIGHT), lw)

def redraw_window():
    screen.fill(WHITE)
    box_length = int(math.sqrt(ROWS))
    lw = 3 if i % box_length == 0 else
    if game_state == "MENU":
        title = FONT.render("Select Difficulty", True, BLACK)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))
        easy_button.draw(screen)
        medium_button.draw(screen)
        hard_button.draw(screen)

    elif game_state == "PLAYING":
        for row in cells:
            for cell in row:
                cell.draw(CELL_WIDTH, CELL_HEIGHT)
        draw_grid()

        reset_button.draw(screen)
        restart_button.draw(screen)
        exit_button.draw(screen)

    elif game_state == "GAME_OVER":
        msg = FONT.render("Game Over!", True, RED)
        screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2 - 50))
        gameover_restart_button.draw(screen)

    elif game_state == "GAME_WON":
        msg = FONT.render("You Won!", True, GREEN)
        screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2 - 50))
        gamewon_exit_button.draw(screen)

    pygame.display.update()

def is_move_valid(row, col, num):
    if board[row][col] != 0:
        return False
    return sudoku_validator.is_valid(row, col, num)

def check_win():
    for r in range(ROWS):
        for c in range(COLS):
            cell = cells[r][c]
            if cell.value == 0:
                return False
            if not is_move_valid(r, c, cell.value):
                return False
    return True

def main():
    global game_state, selected_row, selected_col

    clock = pygame.time.Clock()

    running = True
    while running:
        clock.tick(30)
        redraw_window()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if game_state == "MENU":
                if easy_button.is_clicked(event):
                    create_new_game(DIFFICULTY_LEVELS["easy"])
                    game_state = "PLAYING"
                elif medium_button.is_clicked(event):
                    create_new_game(DIFFICULTY_LEVELS["medium"])
                    game_state = "PLAYING"
                elif hard_button.is_clicked(event):
                    create_new_game(DIFFICULTY_LEVELS["hard"])
                    game_state = "PLAYING"

            elif game_state == "PLAYING":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if 0 <= x < WIDTH and 0 <= y < ROWS * CELL_HEIGHT:
                        col = x // CELL_WIDTH
                        row = y // CELL_HEIGHT
                        if 0 <= row < ROWS and 0 <= col < COLS:
                            for row_cells in cells:
                                for cell in row_cells:
                                    cell.selected = False
                            selected_row, selected_col = row, col
                            cells[row][col].selected = True
                    else:
                        if reset_button.is_clicked(event):
                            create_new_game(removed_cells)
                        elif restart_button.is_clicked(event):
                            game_state = "MENU"
                            selected_row, selected_col = None, None
                        elif exit_button.is_clicked(event):
                            running = False

                elif event.type == pygame.KEYDOWN:
                    if selected_row is not None and selected_col is not None:
                        cell = cells[selected_row][selected_col]

                        if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4,
                                         pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]:
                            number = int(event.unicode)
                            cell.set_sketched_value(number)

                        elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                            if cell.sketched_value != 0:
                                if is_move_valid(selected_row, selected_col, cell.sketched_value):
                                    cell.set_cell_value(cell.sketched_value)
                                    cell.set_sketched_value(0)
                                    if check_win():
                                        game_state = "GAME_WON"
                                else:
                                    game_state = "GAME_OVER"

                        elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                            if board[selected_row][selected_col] == 0:
                                cell.clear()

            elif game_state == "GAME_OVER":
                if gameover_restart_button.is_clicked(event):
                    create_new_game(removed_cells)
                    game_state = "PLAYING"
                    selected_row, selected_col = None, None

            elif game_state == "GAME_WON":
                if gamewon_exit_button.is_clicked(event):
                    game_state = "MENU"
                    selected_row, selected_col = None, None

    pygame.quit()

if __name__ == "__main__":
    main()
