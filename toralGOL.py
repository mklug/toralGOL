import time
import pygame
import numpy as np

COLOR_BG = (10, 10, 10,)
COLOR_GRID = (40, 40, 40)
COLOR_DIE_NEXT = (170, 170, 170)
COLOR_ALIVE_NEXT = (255, 255, 255)

pygame.init()
pygame.display.set_caption("Conway's game of life but on a torus")

SIZE = 10
WIDTH = 10
HEIGHT = 10

# Number of vertical and horizontal cells.
CH = SIZE * WIDTH
CV = SIZE * HEIGHT

# Rules for GOL:
# If a cell is alive:
#    - If the cell has 0 or 1 neighbors, it dies.
#    - If the cell has 4 or more neightbors it dies.
#    - Otherwise, it lives.
# If the cell is dead:
#    - If the cells has 3 neighbors it comes alive.
#    - Otherwise, it remains dead.

def update(screen, cells, size, with_progress=False):
    updated_cells = np.zeros((cells.shape[0], cells.shape[1]))

    for row, col in np.ndindex(cells.shape):
        # Just modified the slicing to get a torus.
        alive = cells[(row - 1) % CV, (col - 1) % CH] + cells[(row - 1) % CV, col] + cells[(row - 1) % CV, (col + 1) % CH] \
         + cells[(row + 1) % CV, (col - 1) % CH] + cells[(row + 1) % CV, col] + cells[(row + 1) % CV, (col + 1) % CH] \
         + cells[row, (col - 1) % CV] + cells[row, (col + 1) % CH]

        #Swap in this for the classic planar game of life. 
        #alive = np.sum(cells[row-1:row+2, col-1:col+2]) - cells[row, col]
        color = COLOR_BG if cells[row, col] == 0 else COLOR_ALIVE_NEXT

        if cells[row, col] == 1:
            if alive < 2 or alive > 3:
                if with_progress:
                    color = COLOR_DIE_NEXT
            elif 2 <= alive <= 3:
                updated_cells[row, col] = 1
                if with_progress:
                    color = COLOR_ALIVE_NEXT
        else:
            if alive == 3:
                updated_cells[row, col] = 1
                if with_progress:
                    color = COLOR_ALIVE_NEXT

        pygame.draw.rect(screen, color, (col * size, row * size, size - 1, size - 1))

    return updated_cells


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH * SIZE * 10, HEIGHT * SIZE * 10))

    cells = np.zeros((HEIGHT* SIZE, WIDTH * SIZE))
    screen.fill(COLOR_GRID)
    update(screen, cells, SIZE)

    pygame.display.flip()
    pygame.display.update()

    running = False

    while True:
        for Q in pygame.event.get():
            if Q.type == pygame.QUIT:
                pygame.quit()
                return
            elif Q.type == pygame.KEYDOWN:
                if Q.key == pygame.K_SPACE:
                    running = not running
                    update(screen, cells, SIZE)
                    pygame.display.update()
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                cells[pos[1] // SIZE, pos[0] // SIZE] = 1
                update(screen, cells, SIZE)
                pygame.display.update()

        screen.fill(COLOR_GRID)

        if running:
            cells = update(screen, cells, SIZE, with_progress=True)
            pygame.display.update()

        time.sleep(0.001)


if __name__ == '__main__':
    main()
