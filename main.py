import os
import zipfile

import pygame
import json
import easygui
import math


class GalaxyForge:
    def __init__(self):

        # Initialize Pygame
        pygame.init()

        # list of planets to be displayed. [[id,[x,y],planet-type, id of parent node]]
        self.galaxy_chart = "MapFiles\\galaxy_chart.json"
        self.phaselanes = self.readPhaseLanes()
        self.planetlist = self.readGalaxyChart()

        # load Icons
        self.icons = self.loadIcons()
        self.ICON_SIZE = 64

        # setting up screen
        self.WIDTH = 1280
        self.HEIGHT = 720
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption('Alpha Forge')

        # Zoom and Drag numbers
        self.scale = 1
        self.offset = [0, 0]
        size = int(20 * self.scale)
        self.font = pygame.font.SysFont(None, size * 2)
        self.MousePositionOnGrid = ""
        self.running = True
        self.last_click_pos = None
        self.last_click_time = 0
        self.control_click = [0, 0]
        self.highestID = 0

        # Selected Entities
        self.selectedPlanet = ""

        # Run the Game
        self.getHighestID()
        self.gameLoop()

    def getHighestID(self):
        # Load JSON data from file
        with open(self.galaxy_chart) as file:
            galaxyChart = json.load(file)
        element_0 = next(node for node in galaxyChart['root_nodes'] if node['id'] == 0)
        for node in element_0['child_nodes']:
            if node['id'] > self.highestID:
                self.highestID = node['id']
            if 'child_nodes' in node:
                for childNode in node["child_nodes"]:
                    if childNode['id'] > self.highestID:
                        self.highestID = childNode['id']
        for node in galaxyChart['phase_lanes']:
            if node['id'] > self.highestID:
                self.highestID = node['id']

    def readPhaseLanes(self):
        # Load JSON data from file
        phaselanes = []
        with open(self.galaxy_chart) as file:
            galaxyChart = json.load(file)
        for node in galaxyChart['phase_lanes']:
            phaselanes.append([node['node_a'], node['node_b']])
        return phaselanes

    def readGalaxyChart(self):
        # Load JSON data from file
        with open(self.galaxy_chart) as file:
            galaxyChart = json.load(file)

        # Find the element with id 0
        element_0 = next(node for node in galaxyChart['root_nodes'] if node['id'] == 0)
        sunPosition = element_0['position']
        sunType = element_0['filling_name']

        # Create planet list
        planetlisttemp = [[0, sunPosition, sunType, 0]]
        for lane in self.phaselanes:
            if lane[0] == 0:
                lane[0] = sunPosition
            if lane[1] == 0:
                lane[1] = sunPosition
        # Get the id and position of every child node of element 0
        for child_node in element_0['child_nodes']:
            child_node_id = child_node['id']
            child_node_position = child_node['position']
            child_node_filling_name = child_node['filling_name']

            for lane in self.phaselanes:
                if lane[0] == child_node_id:
                    lane[0] = child_node_position
                if lane[1] == child_node_id:
                    lane[1] = child_node_position

            planetlisttemp.append([child_node_id, child_node_position, child_node_filling_name, 0])

            if 'child_nodes' in child_node:
                for grandchild_node in child_node['child_nodes']:
                    grandchild_node_id = grandchild_node['id']
                    grandchild_node_position = grandchild_node['position']
                    grandchild_node_filling_name = grandchild_node['filling_name']

                    planetlisttemp.append(
                        [grandchild_node_id, grandchild_node_position, grandchild_node_filling_name, child_node_id])
                    for lane in self.phaselanes:
                        if lane[0] == grandchild_node_id:
                            lane[0] = grandchild_node_position
                        if lane[1] == grandchild_node_id:
                            lane[1] = grandchild_node_position
        return planetlisttemp

    @staticmethod
    def loadIcons():
        # Load icons
        ICON_SIZE = 64
        icons = {}
        for filename in os.listdir('icons'):
            if filename.endswith('.png'):
                name = os.path.splitext(filename)[0]
                icons[name] = pygame.transform.scale(pygame.image.load(os.path.join('icons', filename)),
                                                     (ICON_SIZE, ICON_SIZE))
        return icons

    # finds the closest planet to where you clicked
    def find_closest_planet(self, coords):
        a, b = coords
        min_distance = float('inf')
        closest_planet = ""

        for planet in self.planetlist:
            x, y = planet[1]
            distance = math.sqrt((x - a) ** 2 + (y - b) ** 2)
            if distance < min_distance:
                min_distance = distance
                closest_planet = planet[0]

        return closest_planet, min_distance

    def addPhaseLane(self, pos1, pos2):
        gridPos1 = self.screen_to_grid(pos1)
        gridPos2 = self.screen_to_grid(pos2)
        node_a = self.find_closest_planet(gridPos1)[0]
        node_b = self.find_closest_planet(gridPos2)[0]
        newID = self.highestID + 1
        new_node = {"id": newID, "node_a": node_a, "node_b": node_b}
        appender = JSONAppender(self.galaxy_chart)
        appender.appendPhaselane(new_node)
        self.control_click = [0, 0]
        self.getHighestID()
        self.phaselanes = self.readPhaseLanes()
        self.planetlist = self.readGalaxyChart()

    def show_context_menu(self, mouse_pos):

        # Define the menu options
        menu_options = ['Add spaced out sattelites', 'Fuck ya life', 'bing bong']

        # Show the context menu
        choice = easygui.buttonbox('Choose an option:', choices=menu_options, title='Context Menu', default_choice=None,
                                   cancel_choice='Cancel', image=None)

        # Handle the user's choice
        if choice == 'Add spaced out sattelites':
            # Do something for option 1
            pass
        elif choice == 'Option 2':
            # Do something for option 2
            pass
        elif choice == 'Option 3':
            # Do something for option 3
            pass

    def eventhandler(self, events):
        handlers = {
            pygame.QUIT: self.quit,
            pygame.VIDEORESIZE: self.resize_window,
            pygame.MOUSEBUTTONDOWN: self.handle_mouse_button_down,
            pygame.MOUSEMOTION: self.handle_mouse_motion,
            pygame.KEYDOWN: self.handle_key_down
        }

        for event in events:
            handler = handlers.get(event.type)
            if handler:
                handler(event)

    def quit(self, event):
        self.running = False

    def resize_window(self, event):
        self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

    def handle_mouse_button_down(self, event):
        # Handle lmb events
        if event.button == 1:
            self.handle_left_button_down(event)
        # Handle rmb events
        elif event.button == 3:
            self.handle_right_button_down(event)
        # Zoom in
        elif event.button == 4:
            self.scale *= 1.1
        # Zoom out
        elif event.button == 5:
            self.scale /= 1.1

    def handle_left_button_down(self, event):
        # Wenn gleichzeitig links strg und lmb gedrückt sind
        if self.isCtrlClick():
            # wenn schon ein strg click gemacht wurde erstelle eine phaselane zwischen dem letzten und aktuellen klick
            if self.control_click != [0, 0]:
                self.addPhaseLane(self.control_click, event.pos)
            # wenn noch kein strg click gemacht wurde wird der aktuelle gespeichert
            else:
                self.control_click = event.pos

        # wenn ein doppelclick gemacht wurde
        elif self.isDoubleClick(event.pos):
            x, y = self.screen_to_grid(self.last_click_pos)
            self.PlanetPopup(x, y)
        else:
            planet_id, disance = self.find_closest_planet(self.screen_to_grid(event.pos))
            if disance <= self.ICON_SIZE * self.scale * 0.5:
                self.selectedPlanet = str(planet_id)
            else:
                self.selectedPlanet = ""
            self.last_click_pos = event.pos
            self.last_click_time = pygame.time.get_ticks()

    def handle_right_button_down(self, event):
        if pygame.mouse.get_pressed()[2]:
            mouse_pos = pygame.mouse.get_pos()
            self.show_context_menu(mouse_pos)

    def handle_key_down(self, event):
        if event.key == pygame.K_DELETE:
            self.delete_selected_planet()

    def isDoubleClick(self, pos):
        return pygame.time.get_ticks() - self.last_click_time < 500 and self.last_click_pos == pos

    def isCtrlClick(self):
        return pygame.key.get_pressed()[pygame.K_LCTRL] and pygame.mouse.get_pressed()[0]

    def handle_mouse_motion(self, event):
        if event.buttons[1]:
            dx, dy = event.rel
            self.offset[0] += dx / self.scale
            self.offset[1] += dy / self.scale

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

    def screen_to_grid(self, screen_pos):
        x, y = screen_pos

        x00offset = (self.screen.get_width() // 2)
        y00offset = (self.screen.get_height() // 2)

        y = int((y - y00offset - self.offset[1]) / self.scale)
        x = int((x - x00offset - self.offset[0]) / self.scale)

        return x, y

    def gridToScreen(self, grid_pos):
        x, y = grid_pos

        x00offset = (self.screen.get_width() // 2)
        y00offset = (self.screen.get_height() // 2)

        x = int(x * self.scale + x00offset + self.offset[0])
        y = int(y * self.scale + y00offset + self.offset[1])

        return x, y

    def draw_planetlist(self):

        # Define some colors
        GRAY = (128, 128, 128)
        DARK_GRAY = (64, 64, 64)
        BLACK = (0, 0, 0)
        OFFWHITE = (155, 155, 155)

        x00offset = (self.screen.get_width() // 2)
        y00offset = (self.screen.get_height() // 2)

        self.screen.fill(BLACK)

        # Draw phase lanes
        for lane in self.phaselanes:
            start = lane[0]
            end = lane[1]

            startX = int(start[0] * self.scale + x00offset + self.offset[0])
            endX = int(end[0] * self.scale + x00offset + self.offset[0])
            startY = int(start[1] * self.scale + y00offset + self.offset[1])
            endY = int(end[1] * self.scale + y00offset + self.offset[1])

            pygame.draw.line(self.screen, OFFWHITE, (startX, startY), (endX, endY), 1)

        for planet in self.planetlist:
            # get the ID
            planet_id = planet[0]
            # calculate planet position on sceen
            x, y = self.gridToScreen(planet[1])
            # get the name by which to find the icon
            icon_name = planet[2]
            # get icon
            icon = self.icons.get(icon_name, None)
            if icon is not None:
                # scale icon if zoomed
                icon = self.scaleIcons(icon)
                # if planet is selected draw circle around it
                if str(planet_id) == self.selectedPlanet:
                    pygame.draw.circle(self.screen, (90, 90, 90), (x, y), 0.4 * (self.ICON_SIZE * self.scale),
                                       int(3 * self.scale))
                # get a rectangle centered on the spot the planet should be at
                rect = icon.get_rect(center=(x, y))
                # stick the icon on the rectangle
                self.screen.blit(icon, rect)

                # define the font
                font = pygame.font.SysFont('Arial', 16)
                # prepare to render planet_id string in white
                text = font.render(str(planet_id), True, (255, 255, 255))
                # get a rectangle the size of the text and put it above the planet
                text_rect = text.get_rect(center=(x, y - self.ICON_SIZE * self.scale * 0.6))
                # Stick the text to the rectangle
                self.screen.blit(text, text_rect)


            else:
                size = int(20 * self.scale)
                pygame.draw.circle(self.screen, GRAY,
                                   (int((x + self.offset[0]) * self.scale), int((y + self.offset[1]) * self.scale)),
                                   size)
                text = self.font.render('?', True, DARK_GRAY)
                rect = text.get_rect(
                    center=(int((x + self.offset[0]) * self.scale), int((y + self.offset[1]) * self.scale)))
                self.screen.blit(text, rect)

        pygame.display.flip()

    def scaleIcons(self, icon):
        size = int(self.ICON_SIZE * self.scale)
        return pygame.transform.scale(icon, (size, size))

    def PlanetPopup(self, x, y):
        planet_types = ['gas_giant_planet', 'random_home_ice_volcanic_planet', 'random_moon_planet',
                        'random_fair_planet', 'random_poor_planet', 'random_rich_planet',
                        'random_asteroid_line_cluster', 'player_home_planet', 'random_asteroid',
                        'lagrange_point_planet', 'random_star']
        title = 'Choose a planet type to add:'
        planet_type = easygui.choicebox(msg=title, title='Planet Type', choices=planet_types, preselect=0)

        if planet_type:
            if planet_type == 'cancel':
                return
            else:
                # Show input box for user to enter a parent id
                number_str = easygui.enterbox(msg=f'Enter a valid id (0-{self.highestID}):',
                                              title='Enter Parent Gravity Well id', default='0')
                if not number_str:
                    return
                try:
                    number = int(number_str)
                    if not 0 <= number <= self.highestID:
                        raise ValueError
                except ValueError:
                    easygui.msgbox(msg=f'Invalid id. Please enter a planet id between 0 and {self.highestID}.',
                                   title='Error')
                    return
                self.addPlanet(x, y, planet_type, number)

    def addPlanet(self, x, y, planettype, parentid):
        newID = self.highestID + 1
        planet = [newID, [x, y], planettype, parentid]
        appender = JSONAppender(self.galaxy_chart)
        appender.prepareAppend(planet)
        self.getHighestID()
        self.phaselanes = self.readPhaseLanes()
        self.planetlist = self.readGalaxyChart()

    def delete_selected_planet(self):
        appender = JSONAppender(self.galaxy_chart)
        appender.deleteNode(self.selectedPlanet)
        self.selectedPlanet = ""
        self.getHighestID()
        self.phaselanes = self.readPhaseLanes()
        self.planetlist = self.readGalaxyChart()



class JSONAppender:
    def __init__(self, galaxy_chart):
        with open(galaxy_chart, 'r') as f:
            self.data = json.load(f)
        self.galaxy_chart = galaxy_chart

    def isParentRoot(self, parent_id):
        for node in self.data["root_nodes"]:
            if node["id"] == parent_id:
                return True

    def findParent(self, parent_id):
        for node in self.data["root_nodes"]:
            for child_node in node['child_nodes']:
                if child_node["id"] == parent_id:
                    return child_node

    def append(self, new_node, parent_id):
        pid = int(parent_id)
        if self.isParentRoot(parent_id):
            parent_element = next(node for node in self.data['root_nodes'] if node['id'] == pid)
        else:
            parent_element = self.findParent(parent_id)
        if 'child_nodes' not in parent_element:
            parent_element['child_nodes'] = []
        parent_element['child_nodes'].append(new_node)
        with open(self.galaxy_chart, 'w') as f:
            json.dump(self.data, f, indent=4)

    def appendPhaselane(self, new_node):
        self.data['phase_lanes'].append(new_node)
        with open(self.galaxy_chart, 'w') as f:
            json.dump(self.data, f, indent=4)

    def prepareAppend(self, planet):
        planetId = planet[0]
        position = planet[1]
        filling_name = planet[2]
        parent_node = planet[3]

        # Create a new child node
        new_node = {"id": planetId, "filling_name": filling_name, "position": position}
        print(f"Adding new node: {new_node}")
        self.append(new_node, parent_node)

    def deleteNode(self, planet_id):
        self.deletePhaseLanes(planet_id)
        parent_element = next(node for node in self.data['root_nodes'] if node['id'] == 0)
        if 'child_nodes' in parent_element:
            for child_node in parent_element['child_nodes']:
                if str(child_node['id']) == str(planet_id):
                    # Remove the child node from the parent node
                    parent_element['child_nodes'].remove(child_node)
                if 'child_nodes' in child_node:
                    for grandchild_node in child_node['child_nodes']:
                        if str(grandchild_node['id']) == str(planet_id):
                            # Remove the child node from the parent node
                            child_node['child_nodes'].remove(grandchild_node)
        # Dump the modified object back into JSON format
        with open(self.galaxy_chart, 'w') as f:
            json.dump(self.data, f, indent=4)

    def deletePhaseLanes(self, planet_id):
        for phaselane in self.data['phase_lanes']:
            if str(phaselane['node_a']) == str(planet_id) or str(phaselane['node_b']) == str(planet_id):
                self.data['phase_lanes'].remove(phaselane)


class ScenarioArchive:
    def __init__(self, archive_file):
        self.archive_file = archive_file

    def extract_files(self, dest_dir):
        with zipfile.ZipFile(self.archive_file, 'r') as zipf:
            for member in zipf.infolist():
                if member.filename.startswith('maps/') and not member.is_dir():
                    # extract only files from maps directory
                    member.filename = os.path.basename(member.filename)
                    zipf.extract(member, dest_dir)

    @staticmethod
    def create_archive(source_dir, dest_file):
        with zipfile.ZipFile(dest_file, 'w') as zipf:
            for root, dirs, files in os.walk(source_dir):
                for file in files:
                    zipf.write(os.path.join(root, file), arcname=os.path.relpath(os.path.join(root, file), source_dir))


gf = GalaxyForge()

ScenarioArchive.create_archive("MapFiles", "maps/3erTest.scenario")
