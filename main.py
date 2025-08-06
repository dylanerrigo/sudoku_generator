import pygame
from cell import Cell
from sudoku_generator import generate_sudoku

pygame.init()

# Constants
WIDTH, HEIGHT = 540, 540
ROWS, COLS = 9, 9
CELL_WIDTH = WIDTH // COLS
CELL_HEIGHT = HEIGHT // ROWS

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku")

# Generate board
REMOVED_CELLS = 40  # You can adjust this
board = generate_sudoku(9, REMOVED_CELLS)

# Create cells
cells = [[Cell(board[row][col], row, col, screen) for col in range(COLS)] for row in range(ROWS)]

def draw_grid():
    for i in range(ROWS + 1):
        line_width = 3 if i % 3 == 0 else 1
        pygame.draw.line(screen, (0, 0, 0), (0, i * CELL_HEIGHT), (WIDTH, i * CELL_HEIGHT), line_width)
        pygame.draw.line(screen, (0, 0, 0), (i * CELL_WIDTH, 0), (i * CELL_WIDTH, HEIGHT), line_width)

def redraw_window():
    screen.fill((255, 255, 255))
    for row in cells:
        for cell in row:
            cell.draw(CELL_WIDTH, CELL_HEIGHT)
    draw_grid()
    pygame.display.update()

# Main loop
def main():
    running = True
    selected_row, selected_col = None, None

    while running:
        redraw_window()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                selected_col = x // CELL_WIDTH
                selected_row = y // CELL_HEIGHT

                # Reset all selected flags
                for row in cells:
                    for cell in row:
                        cell.selected = False

                cells[selected_row][selected_col].selected = True

            elif event.type == pygame.KEYDOWN:
                if selected_row is not None and selected_col is not None:
                    if event.key == pygame.K_1:
                        cells[selected_row][selected_col].set_sketched_value(1)
                    elif event.key == pygame.K_2:
                        cells[selected_row][selected_col].set_sketched_value(2)
                    elif event.key == pygame.K_3:
                        cells[selected_row][selected_col].set_sketched_value(3)
                    elif event.key == pygame.K_4:
                        cells[selected_row][selected_col].set_sketched_value(4)
                    elif event.key == pygame.K_5:
                        cells[selected_row][selected_col].set_sketched_value(5)
                    elif event.key == pygame.K_6:
                        cells[selected_row][selected_col].set_sketched_value(6)
                    elif event.key == pygame.K_7:
                        cells[selected_row][selected_col].set_sketched_value(7)
                    elif event.key == pygame.K_8:
                        cells[selected_row][selected_col].set_sketched_value(8)
                    elif event.key == pygame.K_9:
                        cells[selected_row][selected_col].set_sketched_value(9)
                    elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                        cells[selected_row][selected_col].set_sketched_value(0)

    pygame.quit()

if __name__ == "__main__":
    main()
