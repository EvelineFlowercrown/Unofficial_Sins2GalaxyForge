import os
import pygame
from pygame.locals import QUIT
import json

# Initialize Pygame
pygame.init()

# Set up the window
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption('Galaxy Chart')

# Define some colors
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)

# Create a font object for displaying the position coordinates
font = pygame.font.SysFont(None, 20)

# Create a new surface for displaying the position coordinates
coordinates_surface = pygame.Surface((200, 20))
coordinates_surface.fill((255, 255, 255))

# Load icons
ICON_SIZE = 40
icons = {}
for filename in os.listdir('icons'):
    if filename.endswith('.png'):
        name = os.path.splitext(filename)[0]
        icons[name] = pygame.transform.scale(pygame.image.load(os.path.join('icons', filename)), (ICON_SIZE, ICON_SIZE))


def readGalaxyChart():
    # Load JSON data from file
    with open('galaxy_chart.json') as file:
        galaxyChart = json.load(file)

    # Find the element with id 0
    element_0 = next(node for node in galaxyChart['root_nodes'] if node['id'] == 0)
    sunPosition = element_0['position']
    sunType = element_0['filling_name']

    # Create planet list
    planetlisttemp = [[0, sunPosition, sunType, 0]]

    # Get the id and position of every child node of element 0
    for child_node in element_0['child_nodes']:
        child_node_id = child_node['id']
        child_node_position = child_node['position']
        child_node_filling_name = child_node['filling_name']

        planetlisttemp.append([child_node_id, child_node_position, child_node_filling_name, 0])

        if 'child_nodes' in child_node:
            for grandchild_node in child_node['child_nodes']:
                grandchild_node_id = grandchild_node['id']
                grandchild_node_position = grandchild_node['position']
                grandchild_node_filling_name = grandchild_node['filling_name']

                planetlisttemp.append(
                    [grandchild_node_id, grandchild_node_position, grandchild_node_filling_name, child_node_id])
    return planetlisttemp


def getStarPosition():
    global planetlist
    


# Initialize scale and offset
scale = 1.0
offset = list(getStarPosition())


def screen_to_grid(screen_pos):
    global offset, scale
    x, y = screen_pos
    x = (x - screen.get_width() // 2) / scale - offset[0]
    y = (y - screen.get_height() // 2) / scale - offset[1]
    return x, y


# Function to draw the planet list
def draw_planetlist(planetlist):
    global screen, scale, offset
    screen.fill(WHITE)
    for planet in planetlist:
        x, y = planet[1]
        icon_name = planet[2]
        parent_node = planet[3]
        icon = icons.get(icon_name, None)
        if icon is not None:
            size = int(ICON_SIZE * scale)
            icon = pygame.transform.scale(icon, (size, size))
            rect = icon.get_rect(center=(int((x + offset[0]) * scale), int((y + offset[1]) * scale)))
            screen.blit(icon, rect)
        else:
            size = int(20 * scale)
            pygame.draw.circle(screen, GRAY, (int((x + offset[0]) * scale), int((y + offset[1]) * scale)), size)
            font = pygame.font.SysFont(None, size * 2)
            text = font.render('?', True, DARK_GRAY)
            rect = text.get_rect(center=(int((x + offset[0]) * scale), int((y + offset[1]) * scale)))
            screen.blit(text, rect)
    pygame.display.flip()


planetlist = readGalaxyChart()

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            screen_width, screen_height = event.w, event.h
            screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
            # Redraw planets after resizing window
            draw_planetlist(planetlist)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 2:
                start_pos = pygame.mouse.get_pos()
            elif event.button == 5:
                scale /= 1.1
            elif event.button == 4:
                scale *= 1.1
        elif event.type == pygame.MOUSEMOTION and event.buttons[1]:
            dx, dy = event.rel
            offset[0] += dx / scale
            offset[1] += dy / scale
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 2:
                end_pos = pygame.mouse.get_pos()
                offset[0] += end_pos[0] - start_pos[0]
                offset[1] += end_pos[1] - start_pos[1]
        # Update the display after each event
        draw_planetlist(planetlist)
        pygame.display.update()

# Clean up
pygame.quit()
