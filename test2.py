import pygame

class InfiniteGrid:
    def __init__(self, cell_size=10, bg_color=(255, 255, 255)):
        self.cell_size = cell_size
        self.bg_color = bg_color
        self.screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
        self.cells = {}
        self.camera_x = 0
        self.camera_y = 0

        # Initialize the red center cell at (0, 0)
        self.cells[(0, 0)] = pygame.Rect(0, 0, self.cell_size, self.cell_size)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.VIDEORESIZE:
                    self.screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)

            self.screen.fill(self.bg_color)

            # Calculate the cell position of the camera
            cell_x = self.camera_x // self.cell_size
            cell_y = self.camera_y // self.cell_size

            # Center the camera on the (0, 0) cell
            screen_width, screen_height = self.screen.get_size()
            self.camera_x = screen_width // 2 - self.cell_size // 2 - cell_x * self.cell_size
            self.camera_y = screen_height // 2 - self.cell_size // 2 - cell_y * self.cell_size

            # Draw the cells in the camera's view
            for x in range(cell_x - 20, cell_x + 20):
                for y in range(cell_y - 15, cell_y + 15):
                    if (x, y) not in self.cells:
                        self.cells[(x, y)] = pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
                    color = (255, 0, 0) if x == 0 and y == 0 else (0, 0, 0)
                    pygame.draw.rect(self.screen, color, self.cells[(x, y)], 1)

            pygame.display.update()

if __name__ == '__main__':
    pygame.init()
    grid = InfiniteGrid()
    grid.run()
    pygame.quit()

