import os
import pygame
from pygame.locals import QUIT
import json
import easygui

class GalaxyForge:
    def __init__(self):

        # Initialize Pygame
        pygame.init()

        #list of planets to be displayed. [[id,[x,y],planettype, id of parent node]]
        self.planetlist = self.readGalaxyChart()

        #load Icons
        self.icons = self.loadIcons()
        self.ICON_SIZE = 64

        #setting up screen
        self.WIDTH = 1280
        self.HEIGHT = 720
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption('Alpha Forge')

        #Zoom and Drag numbers
        self.scale = 1
        self.offset = [0,0]
        size = int(20 * self.scale)
        self.font = pygame.font.SysFont(None, size * 2)
        self.MousePositionOnGrid = ""
        self.running = True
        self.last_click_pos = None
        self.last_click_time = 0

        #Run the Game
        self.gameLoop()


    def readGalaxyChart(self):
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

    def loadIcons(self):
        # Load icons
        ICON_SIZE = 64
        icons = {}
        for filename in os.listdir('icons'):
            if filename.endswith('.png'):
                name = os.path.splitext(filename)[0]
                icons[name] = pygame.transform.scale(pygame.image.load(os.path.join('icons', filename)),(ICON_SIZE, ICON_SIZE))
        return icons

    def eventhandler(self, events):
        for event in events:
            # Quit Game
            if event.type == pygame.QUIT:
                self.running = False

            # Window Resize
            elif event.type == pygame.VIDEORESIZE:
                self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

            # Mouse inputs
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Middleclick Pressed
                if event.button == 2:
                    start_pos = pygame.mouse.get_pos()
                elif event.button == 4:
                    self.scale *= 1.1
                elif event.button == 5:
                    self.scale /= 1.1
                elif event.button == 1 and pygame.mouse.get_pressed()[0]:
                    # Check for double-click
                    if pygame.time.get_ticks() - self.last_click_time < 500 and self.last_click_pos == event.pos:
                        # Open popup dialogue
                        x,y = self.last_click_pos
                        self.PlanetPopup(x,y)

                    else:
                        # Store the last click position and time
                        self.last_click_pos = event.pos
                        self.last_click_time = pygame.time.get_ticks()

            elif event.type == pygame.MOUSEMOTION and event.buttons[1]:
                dx, dy = event.rel
                self.offset[0] += dx / self.scale
                self.offset[1] += dy / self.scale

            # MouseMovement
            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = self.screen_to_grid(pygame.mouse.get_pos())
                self.MousePositionOnGrid = f"Grid: ({mouse_pos[0]:.2f}, {mouse_pos[1]:.2f}) Screen: {pygame.mouse.get_pos()}"

    def gameLoop(self):
        while self.running:
            # Handle events

            self.eventhandler(pygame.event.get())
            # Clear screen
            self.screen.fill((0, 0, 0))

            # Draw planets
            self.draw_planetlist()

            # Draw MousePositionOnGrid text
            status_surface = self.font.render(self.MousePositionOnGrid, True, (255, 255, 255))
            status_rect = status_surface.get_rect()
            status_rect.topleft = (10, self.screen.get_height() - status_rect.height - 10)
            self.screen.blit(status_surface, status_rect)

            # Update display
            pygame.display.update()

        # Clean up
        pygame.quit()

    def screen_to_grid(self,screen_pos):
        x, y = screen_pos

        x00offset = (self.screen.get_width() // 2)
        y00offset = (self.screen.get_height() // 2)

        y = int((y - y00offset - self.offset[1]) / self.scale)
        x = int((x - x00offset - self.offset[0]) / self.scale)
        return x, y

    def draw_planetlist(self):

        # Define some colors
        WHITE = (255, 255, 255)
        GRAY = (128, 128, 128)
        DARK_GRAY = (64, 64, 64)
        BLACK = (0, 0, 0)

        self.screen.fill(BLACK)
        for planet in self.planetlist:
            x, y = planet[1]
            icon_name = planet[2]
            parent_node = planet[3]
            icon = self.icons.get(icon_name, None)
            if icon is not None:
                #Icon Scaling
                size = int(self.ICON_SIZE * self.scale)
                icon = pygame.transform.scale(icon, (size, size))

                #calculate planet position on sceen
                center = [0,0]

                x00offset = (self.screen.get_width() // 2)
                y00offset = (self.screen.get_height() // 2)

                center[0] = int(x * self.scale + x00offset + self.offset[0])
                center[1] = int(y * self.scale + y00offset + self.offset[1])

                #get a rectangle centered on the spot the planet should be at
                rect = icon.get_rect(center=((center[0]), (center[1])))

                #stick the icon on the rectangle
                self.screen.blit(icon, rect)
            else:
                size = int(20 * self.scale)
                pygame.draw.circle(self.screen, GRAY, (int((x + self.offset[0]) * self.scale), int((y + self.offset[1]) * self.scale)), size)
                text = self.font.render('?', True, DARK_GRAY)
                rect = text.get_rect(center=(int((x + self.offset[0]) * self.scale), int((y + self.offset[1]) * self.scale)))
                self.screen.blit(text, rect)
        pygame.display.flip()

    def PlanetPopup(self,x, y):
        planet_types = ['gas_giant_planet', 'random_home_ice_volcanic_planet', 'random_moon_planet',
                        'random_fair_planet', 'random_poor_planet', 'random_rich_planet',
                        'random_asteroid_line_cluster', 'player_home_planet', 'random_asteroid']
        title = 'Choose a planet type to add:'
        choice = easygui.choicebox(msg=title, title='Planet Type', choices=planet_types, preselect=0)

        if choice:
            if choice == 'cancel':
                return
            else:
                print(f"Chosen planet type: {choice}")
                print(f"Position of double click: ({x}, {y})")



gf = GalaxyForge()