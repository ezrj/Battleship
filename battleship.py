import pygame
import socket
import threading
import pickle
import sys
import os

# Constants
WAVE_STYLE = 2     #Choose Between 1 or 2 for comparison
GRID_SIZE = 10
CELL_SIZE = 40
MARGIN = 20
INFO_PANEL_WIDTH = 200
WINDOW_WIDTH = MARGIN * 3 + CELL_SIZE * GRID_SIZE * 2 + INFO_PANEL_WIDTH
WINDOW_HEIGHT = MARGIN * 2 + CELL_SIZE * GRID_SIZE
FPS = 30

# Asset placeholders
ASSETS_DIR = 'assets'
HIT_IMAGE = os.path.join(ASSETS_DIR, 'Hit.png')       # red X for hits
MISS_IMAGE = os.path.join(ASSETS_DIR, 'Miss.png')     # black X for misses
SEA_IMAGE = [os.path.join(ASSETS_DIR, 'Waves1', '0001.png'), os.path.join(ASSETS_DIR, 'Waves1', '0002.png'),
os.path.join(ASSETS_DIR, 'Waves1', '0003.png'), os.path.join(ASSETS_DIR, 'Waves1', '0004.png'), os.path.join(ASSETS_DIR, 'Waves1', '0005.png'),
os.path.join(ASSETS_DIR, 'Waves1', '0006.png'), os.path.join(ASSETS_DIR, 'Waves1', '0007.png'), os.path.join(ASSETS_DIR, 'Waves1', '0008.png'),
os.path.join(ASSETS_DIR, 'Waves1', '0009.png'), os.path.join(ASSETS_DIR, 'Waves1', '0010.png'), os.path.join(ASSETS_DIR, 'Waves1', '0011.png'),
os.path.join(ASSETS_DIR, 'Waves1', '0012.png'), os.path.join(ASSETS_DIR, 'Waves1', '0013.png'), os.path.join(ASSETS_DIR, 'Waves1', '0014.png'),
os.path.join(ASSETS_DIR, 'Waves1', '0015.png'), os.path.join(ASSETS_DIR, 'Waves1', '0016.png'), os.path.join(ASSETS_DIR, 'Waves1', '0017.png'),
os.path.join(ASSETS_DIR, 'Waves1', '0018.png'), os.path.join(ASSETS_DIR, 'Waves1', '0019.png'), os.path.join(ASSETS_DIR, 'Waves1', '0020.png'),
os.path.join(ASSETS_DIR, 'Waves1', '0021.png'), os.path.join(ASSETS_DIR, 'Waves1', '0022.png'), os.path.join(ASSETS_DIR, 'Waves1', '0023.png'),
os.path.join(ASSETS_DIR, 'Waves1', '0024.png'), os.path.join(ASSETS_DIR, 'Waves1', '0025.png'), os.path.join(ASSETS_DIR, 'Waves1', '0026.png'),
os.path.join(ASSETS_DIR, 'Waves1', '0027.png'), os.path.join(ASSETS_DIR, 'Waves1', '0028.png'), os.path.join(ASSETS_DIR, 'Waves1', '0029.png'),
os.path.join(ASSETS_DIR, 'Waves1', '0030.png'), os.path.join(ASSETS_DIR, 'Waves1', '0031.png'), os.path.join(ASSETS_DIR, 'Waves1', '0032.png'),
os.path.join(ASSETS_DIR, 'Waves1', '0033.png'), os.path.join(ASSETS_DIR, 'Waves1', '0034.png'), os.path.join(ASSETS_DIR, 'Waves1', '0035.png'),
os.path.join(ASSETS_DIR, 'Waves1', '0036.png'), os.path.join(ASSETS_DIR, 'Waves1', '0037.png'), os.path.join(ASSETS_DIR, 'Waves1', '0038.png'),
os.path.join(ASSETS_DIR, 'Waves1', '0039.png'), os.path.join(ASSETS_DIR, 'Waves1', '0040.png'), os.path.join(ASSETS_DIR, 'Waves1', '0041.png'),
os.path.join(ASSETS_DIR, 'Waves1', '0042.png'), os.path.join(ASSETS_DIR, 'Waves1', '0043.png'), os.path.join(ASSETS_DIR, 'Waves1', '0044.png'),
os.path.join(ASSETS_DIR, 'Waves1', '0045.png'), os.path.join(ASSETS_DIR, 'Waves1', '0046.png'), os.path.join(ASSETS_DIR, 'Waves1', '0047.png'),
os.path.join(ASSETS_DIR, 'Waves1', '0048.png'), os.path.join(ASSETS_DIR, 'Waves1', '0049.png'), os.path.join(ASSETS_DIR, 'Waves1', '0050.png'),
os.path.join(ASSETS_DIR, 'Waves1', '0051.png'), os.path.join(ASSETS_DIR, 'Waves1', '0052.png'), os.path.join(ASSETS_DIR, 'Waves1', '0053.png'),
os.path.join(ASSETS_DIR, 'Waves1', '0054.png'), os.path.join(ASSETS_DIR, 'Waves1', '0055.png'), os.path.join(ASSETS_DIR, 'Waves1', '0056.png'),
os.path.join(ASSETS_DIR, 'Waves1', '0057.png'), os.path.join(ASSETS_DIR, 'Waves1', '0058.png'), os.path.join(ASSETS_DIR, 'Waves1', '0059.png'),
os.path.join(ASSETS_DIR, 'Waves1', '0060.png'), os.path.join(ASSETS_DIR, 'Waves1', '0061.png'), os.path.join(ASSETS_DIR, 'Waves1', '0062.png'),
os.path.join(ASSETS_DIR, 'Waves1', '0063.png'), os.path.join(ASSETS_DIR, 'Waves1', '0064.png'), os.path.join(ASSETS_DIR, 'Waves1', '0065.png'),
os.path.join(ASSETS_DIR, 'Waves1', '0066.png'), os.path.join(ASSETS_DIR, 'Waves1', '0067.png'), os.path.join(ASSETS_DIR, 'Waves1', '0068.png'),
os.path.join(ASSETS_DIR, 'Waves1', '0069.png'), os.path.join(ASSETS_DIR, 'Waves1', '0070.png'), os.path.join(ASSETS_DIR, 'Waves1', '0071.png'),
os.path.join(ASSETS_DIR, 'Waves1', '0072.png'), os.path.join(ASSETS_DIR, 'Waves1', '0073.png'), os.path.join(ASSETS_DIR, 'Waves1', '0074.png'),
os.path.join(ASSETS_DIR, 'Waves1', '0075.png'), os.path.join(ASSETS_DIR, 'Waves1', '0076.png'), os.path.join(ASSETS_DIR, 'Waves1', '0077.png'),
os.path.join(ASSETS_DIR, 'Waves1', '0078.png'), os.path.join(ASSETS_DIR, 'Waves1', '0079.png'), os.path.join(ASSETS_DIR, 'Waves1', '0080.png'),
os.path.join(ASSETS_DIR, 'Waves1', '0081.png'), os.path.join(ASSETS_DIR, 'Waves1', '0082.png'), os.path.join(ASSETS_DIR, 'Waves1', '0083.png'),
os.path.join(ASSETS_DIR, 'Waves1', '0084.png'), os.path.join(ASSETS_DIR, 'Waves1', '0085.png'), os.path.join(ASSETS_DIR, 'Waves1', '0086.png'),
os.path.join(ASSETS_DIR, 'Waves1', '0087.png'), os.path.join(ASSETS_DIR, 'Waves1', '0088.png'), os.path.join(ASSETS_DIR, 'Waves1', '0089.png'),
os.path.join(ASSETS_DIR, 'Waves1', '0090.png'), os.path.join(ASSETS_DIR, 'Waves1', '0091.png'), os.path.join(ASSETS_DIR, 'Waves1', '0092.png'),
os.path.join(ASSETS_DIR, 'Waves1', '0093.png'), os.path.join(ASSETS_DIR, 'Waves1', '0094.png'), os.path.join(ASSETS_DIR, 'Waves1', '0095.png'),
os.path.join(ASSETS_DIR, 'Waves1', '0096.png'), os.path.join(ASSETS_DIR, 'Waves1', '0097.png'), os.path.join(ASSETS_DIR, 'Waves1', '0098.png'),
os.path.join(ASSETS_DIR, 'Waves1', '0099.png'), os.path.join(ASSETS_DIR, 'Waves1', '0100.png')]    # water background tile

# Ship rendering color (simple grey square per cell)
SHIP_TILE_COLOR = (150, 150, 150)

GRID_COLOR = (0, 0, 0)
FLASH_COLOR = [(238, 75, 43), (238, 75, 43)] #(238, 75, 43) is red

# Network message types
MSG_SHOT = 'shot'
MSG_RESULT = 'result'
MSG_READY = 'ready'
MSG_GAME_OVER = 'game_over'

class Ship:
    def __init__(self, length):
        self.length = length
        self.orientation = 'H'  # 'H' or 'V'
        self.positions = []
        self.hits = set()

    def place(self, x, y, orientation):
        self.orientation = orientation
        self.positions = []
        for i in range(self.length):
            dx, dy = (i, 0) if orientation == 'H' else (0, i)
            self.positions.append((x + dx, y + dy))

    def is_sunk(self):
        return set(self.positions) == self.hits

    def register_hit(self, pos):
        if pos in self.positions:
            self.hits.add(pos)
            return True
        return False

class Board:
    def __init__(self):
        self.grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.ships = []
        self.hits = set()
        self.misses = set()

    def add_ship(self, ship):
        for x, y in ship.positions:
            self.grid[y][x] = ship
        self.ships.append(ship)

    def receive_shot(self, x, y):
        if (x, y) in self.hits or (x, y) in self.misses:
            return False, False
        target = self.grid[y][x]
        if target:
            hit = target.register_hit((x, y))
            self.hits.add((x, y))
            sunk = target.is_sunk()
            if sunk == True:
                print("Your battleship has been sunk.")
            return True, sunk
        else:
            self.misses.add((x, y))
            return False, False

    def all_sunk(self):
        return all(ship.is_sunk() for ship in self.ships)

class Network:
    def __init__(self, role, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if role == 'server':
            self.sock.bind((host, port))
            self.sock.listen(1)
            print('Waiting for connection...')
            self.conn, _ = self.sock.accept()
            print('Client connected.')
        else:
            self.sock.connect((host, port))
            self.conn = self.sock
            print('Connected to server.')
        self.inbox = []
        self.recv_thread = threading.Thread(target=self._receive_loop, daemon=True)
        self.recv_thread.start()

    def send(self, msg):
        data = pickle.dumps(msg)
        self.conn.sendall(data)

    def _receive_loop(self):
        while True:
            try:
                data = self.conn.recv(4096)
                if not data:
                    break
                msg = pickle.loads(data)
                self.inbox.append(msg)
            except Exception:
                break

    def get_message(self):
        return self.inbox.pop(0) if self.inbox else None

class Game:
    
    def __init__(self, role, host, port):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Networked Battleship')
        self.clock = pygame.time.Clock()
        self.network = Network(role, host, port)

        # Boards and ships
        self.own_board = Board()
        self.enemy_board = Board()
        self.ships_to_place = [Ship(l) for l in [5,4,3,2,1]]
        self.selected_ship = None
        self.preview_orientation = 'H'
        self.mouse_grid = (0, 0)

        # State flags
        self.placing = True  # still positioning ships
        self.ready = False   # placement done
        self.opponent_ready = False
        self.turn = (role == 'server')
        self.running = True
        self.sunk_opponent_ship = False
        self.sunk_player_ship = False

        # Load graphics
        self.sea_frame = 0 # water background tile current frame
        self.flash_frame = 0 # variable for alternating colors for border flashes
        self.hit_img = pygame.transform.scale(pygame.image.load(HIT_IMAGE), (CELL_SIZE, CELL_SIZE))
        self.small_hit_img = pygame.transform.scale(pygame.image.load(HIT_IMAGE), (CELL_SIZE/2, CELL_SIZE/2))
        self.miss_img = pygame.transform.scale(pygame.image.load(MISS_IMAGE), (CELL_SIZE, CELL_SIZE))

        if(WAVE_STYLE == 1):
            self.sea_img  = pygame.transform.scale(pygame.image.load(SEA_IMAGE[self.sea_frame]),  (CELL_SIZE, CELL_SIZE))
        elif(WAVE_STYLE == 2):
            self.sea_img  = pygame.transform.scale(pygame.image.load(SEA_IMAGE[self.sea_frame]),  (CELL_SIZE*2, CELL_SIZE*2))


    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.handle_network()
            self.handle_events()

            # Start game when both players ready
            if self.placing and self.ready and self.opponent_ready:
                self.placing = False
                print('Both ready—game starting!')

            if self.sea_frame >= (len(SEA_IMAGE) - 1):
                self.sea_frame = 0
            else:
                self.sea_frame += 1
            
            if(WAVE_STYLE == 1):
                self.sea_img  = pygame.transform.scale(pygame.image.load(SEA_IMAGE[self.sea_frame]),  (CELL_SIZE, CELL_SIZE))
            elif(WAVE_STYLE == 2):
                self.sea_img  = pygame.transform.scale(pygame.image.load(SEA_IMAGE[self.sea_frame]),  (CELL_SIZE*2, CELL_SIZE*2))

            self.draw()
        pygame.quit()

    def handle_network(self):
        msg = self.network.get_message()
        if not msg: return
        t = msg['type']
        if t == MSG_READY:
            self.opponent_ready = True

        elif t == MSG_SHOT:
            x, y = msg['pos']
            hit, sunk = self.own_board.receive_shot(x, y)
            if sunk:
                self.sunk_player_ship = True
            else:
                self.sunk_player_ship = False
            # Only give defender the turn on a miss
            if not hit:
                self.turn = True
            self.network.send({'type': MSG_RESULT, 'hit': hit, 'pos': (x, y), 'sunk': sunk})
            if self.own_board.all_sunk():
                self.network.send({'type': MSG_GAME_OVER})
                self.game_over(False)

        elif t == MSG_RESULT:
            hit = msg['hit']
            x, y = msg['pos']
            sunk = msg['sunk']
            if hit:
                self.enemy_board.hits.add((x, y))
                if sunk:
                    self.sunk_opponent_ship = True
                # attacker keeps turn on hit
                self.turn = True
            else:
                self.enemy_board.misses.add((x, y))
                # attacker loses turn on miss
                self.turn = False

        elif t == MSG_GAME_OVER:
            self.game_over(True)

    def handle_events(self):
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                self.running = False
            elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_r and self.placing and self.selected_ship:
                self.preview_orientation = 'V' if self.preview_orientation == 'H' else 'H'
            elif self.placing:
                self.handle_placement(ev)
            elif self.turn and ev.type == pygame.MOUSEBUTTONDOWN:
                self.fire(ev)

        if self.placing:
            mx, my = pygame.mouse.get_pos()
            self.mouse_grid = ((mx - MARGIN) // CELL_SIZE, (my - MARGIN) // CELL_SIZE)

    def handle_placement(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            gx, gy = self.mouse_grid
            if not self.selected_ship and self.ships_to_place:
                self.selected_ship = self.ships_to_place.pop(0)
                self.preview_orientation = 'H'
            elif self.selected_ship:
                coords = [
                    (gx + (i if self.preview_orientation == 'H' else 0),
                     gy + (i if self.preview_orientation == 'V' else 0))
                    for i in range(self.selected_ship.length)
                ]
                if all(0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE and not self.own_board.grid[y][x] for x, y in coords):
                    self.selected_ship.place(gx, gy, self.preview_orientation)
                    self.own_board.add_ship(self.selected_ship)
                    self.selected_ship = None
                    if not self.ships_to_place:
                        self.ready = True
                        self.network.send({'type': MSG_READY})

    def fire(self, event):
        mx, my = event.pos
        off = MARGIN * 2 + CELL_SIZE * GRID_SIZE
        if mx > off:
            gx, gy = (mx - off) // CELL_SIZE, (my - MARGIN) // CELL_SIZE
            if 0 <= gx < GRID_SIZE and 0 <= gy < GRID_SIZE:
                # attacker relinquishes turn until result
                if ((gx, gy) in self.enemy_board.hits) or ((gx, gy) in self.enemy_board.misses):
                    return
                else:
                    self.sunk_opponent_ship = False
                    self.sunk_player_ship = False
                    self.turn = False
                    self.network.send({'type': MSG_SHOT, 'pos': (gx, gy)})

    def draw(self):
        self.screen.fill((50, 150, 200))

        # Draw own board
        own_border_rect = pygame.Rect(MARGIN - 3, MARGIN - 3, (CELL_SIZE * 10 + 6), (CELL_SIZE * 10 + 6))
        if(self.placing and not self.ready):
            pygame.draw.rect(self.screen, FLASH_COLOR[self.flash_frame], own_border_rect)
            if(self.flash_frame >= len(FLASH_COLOR) - 1):
                self.flash_frame = 0
            else:
                self.flash_frame += 1
        else:
            pygame.draw.rect(self.screen, GRID_COLOR, own_border_rect)

        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                rect = pygame.Rect(MARGIN + x * CELL_SIZE, MARGIN + y * CELL_SIZE, CELL_SIZE, CELL_SIZE)

                grid = [pygame.Rect(MARGIN + x * CELL_SIZE, MARGIN + y * CELL_SIZE, CELL_SIZE, 1),
                pygame.Rect(MARGIN + x * CELL_SIZE, MARGIN + y * CELL_SIZE, 1, CELL_SIZE),
                pygame.Rect(MARGIN + x * CELL_SIZE, MARGIN + (y + 1) * CELL_SIZE - 1, CELL_SIZE, 1),
                pygame.Rect(MARGIN + (x + 1) * CELL_SIZE - 1, MARGIN + y * CELL_SIZE, 1, CELL_SIZE)]

                if(WAVE_STYLE == 1):
                    self.screen.blit(self.sea_img, rect.topleft)
                elif(WAVE_STYLE == 2):
                    if(y % 2 == 0 and x % 2 == 0):
                        self.screen.blit(self.sea_img, rect.topleft)

                if self.own_board.grid[y][x]:
                    pygame.draw.rect(self.screen, SHIP_TILE_COLOR, rect)

                pygame.draw.rect(self.screen, GRID_COLOR, grid[0])
                pygame.draw.rect(self.screen, GRID_COLOR, grid[1])
                pygame.draw.rect(self.screen, GRID_COLOR, grid[2])
                pygame.draw.rect(self.screen, GRID_COLOR, grid[3])
                
                
                if (x, y) in self.own_board.hits:
                    self.screen.blit(self.hit_img, rect.topleft)
                elif (x, y) in self.own_board.misses:
                    self.screen.blit(self.miss_img, rect.topleft)

        # Draw enemy board
        offx = MARGIN * 2 + CELL_SIZE * GRID_SIZE

        enemy_border_rect = pygame.Rect(offx - 3, MARGIN - 3, (CELL_SIZE * 10 + 6), (CELL_SIZE * 10 + 6))
        if(self.turn == True and not self.placing):
            pygame.draw.rect(self.screen, FLASH_COLOR[self.flash_frame], enemy_border_rect)
            if(self.flash_frame >= len(FLASH_COLOR) - 1):
                self.flash_frame = 0
            else:
                self.flash_frame += 1
        else:
            pygame.draw.rect(self.screen, GRID_COLOR, enemy_border_rect)
        
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                rect = pygame.Rect(offx + x * CELL_SIZE, MARGIN + y * CELL_SIZE, CELL_SIZE, CELL_SIZE)

                grid = [pygame.Rect(offx + x * CELL_SIZE, MARGIN + y * CELL_SIZE, CELL_SIZE, 1),
                pygame.Rect(offx + x * CELL_SIZE, MARGIN + y * CELL_SIZE, 1, CELL_SIZE),
                pygame.Rect(offx + x * CELL_SIZE, MARGIN + (y + 1) * CELL_SIZE - 1, CELL_SIZE, 1),
                pygame.Rect(offx + (x + 1) * CELL_SIZE - 1, MARGIN + y * CELL_SIZE, 1, CELL_SIZE)]

                if(WAVE_STYLE == 1):
                    self.screen.blit(self.sea_img, rect.topleft)
                elif(WAVE_STYLE == 2):
                    if(y % 2 == 0 and x % 2 == 0):
                        self.screen.blit(self.sea_img, rect.topleft)

                pygame.draw.rect(self.screen, GRID_COLOR, grid[0])
                pygame.draw.rect(self.screen, GRID_COLOR, grid[1])
                pygame.draw.rect(self.screen, GRID_COLOR, grid[2])
                pygame.draw.rect(self.screen, GRID_COLOR, grid[3])
                
                if (x, y) in self.enemy_board.hits:
                    self.screen.blit(self.hit_img, rect.topleft)
                elif (x, y) in self.enemy_board.misses:
                    self.screen.blit(self.miss_img, rect.topleft)

        # Placement preview
        if self.placing and self.selected_ship:
            gx, gy = self.mouse_grid
            for i in range(self.selected_ship.length):
                dx, dy = (i, 0) if self.preview_orientation == 'H' else (0, i)
                px, py = gx + dx, gy + dy
                if 0 <= px < GRID_SIZE and 0 <= py < GRID_SIZE:
                    rect = pygame.Rect(MARGIN + px * CELL_SIZE, MARGIN + py * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    pygame.draw.rect(self.screen, (255, 255, 255), rect, 2)

        ### Info Panel ###
        # Status:
        infoFont = pygame.font.SysFont(None, 26)
        if (self.placing and not self.ready):
            statusMessage = infoFont.render('Place Your Ships.', True, (255, 255, 255))
            additionalMessage = infoFont.render('Press \'R\' to rotate.', True, (255, 255, 255))
            self.screen.blit(additionalMessage, (offx + (CELL_SIZE * 10 + 6), MARGIN + 26))
        elif (self.placing):
            statusMessage = infoFont.render('Waiting For Opponent...', True, (255, 255, 255))
        elif (self.turn == True):
            statusMessage = infoFont.render('Your Turn', True, (238, 75, 43))
        else:
            statusMessage = infoFont.render('Opponent\'s Turn', True, (255, 255, 255))
        self.screen.blit(statusMessage, (offx + (CELL_SIZE * 10 + 6), MARGIN))
        #Player Ships
        if (not self.placing):
            playerShips = infoFont.render('Your Remaining Ships:', True, (255, 255, 255))
            self.screen.blit(playerShips, (offx + (CELL_SIZE * 10 + 6), MARGIN + 26))
            playerShipIndex = 0
            for ship in self.own_board.ships:
                if not ship.is_sunk():
                    for i in range (0, ship.length):
                        rect = pygame.Rect(offx + (CELL_SIZE * 10 + 6) + (CELL_SIZE/2 * i), MARGIN + (26*2) + (CELL_SIZE/2 * playerShipIndex) + 3 * (playerShipIndex), CELL_SIZE/2, CELL_SIZE/2)

                        grid = [pygame.Rect(offx + (CELL_SIZE * 10 + 6) + (CELL_SIZE/2 * i), MARGIN + (26*2) + (CELL_SIZE/2 * playerShipIndex) + 3 * (playerShipIndex), CELL_SIZE/2, 1),
                        pygame.Rect(offx + (CELL_SIZE * 10 + 6) + (CELL_SIZE/2 * i), MARGIN + (26*2) + (CELL_SIZE/2 * playerShipIndex) + 3 * (playerShipIndex), 1, CELL_SIZE/2),
                        pygame.Rect(offx + (CELL_SIZE * 10 + 6) + (CELL_SIZE/2 * i), MARGIN + (26*2) + (CELL_SIZE/2 * (playerShipIndex + 1)) - 1 + 3 * (playerShipIndex), CELL_SIZE/2, 1),
                        pygame.Rect(offx + (CELL_SIZE * 10 + 6) + (CELL_SIZE/2 * (i + 1)) - 1, MARGIN + (26*2) + (CELL_SIZE/2 * playerShipIndex) + 3 * (playerShipIndex), 1, CELL_SIZE/2)]

                        pygame.draw.rect(self.screen, SHIP_TILE_COLOR, rect)

                        if(ship.orientation == 'H'):
                            base_pos = ship.positions[0]
                            check_pos = (base_pos[0] + i, base_pos[1])
                            if(check_pos in ship.hits):
                                self.screen.blit(self.small_hit_img, rect.topleft)
                        else:
                            base_pos = ship.positions[0]
                            check_pos = (base_pos[0], base_pos[1] + i)
                            if(check_pos in ship.hits):
                                self.screen.blit(self.small_hit_img, rect.topleft)
                        
                        pygame.draw.rect(self.screen, GRID_COLOR, grid[0])
                        pygame.draw.rect(self.screen, GRID_COLOR, grid[1])
                        pygame.draw.rect(self.screen, GRID_COLOR, grid[2])
                        pygame.draw.rect(self.screen, GRID_COLOR, grid[3])
                    playerShipIndex += 1

        #Enemy Ships
        #if (False):
        #    enemyShips = infoFont.render('Remaining Enemy Ships:', True, (255, 255, 255))
        #    self.screen.blit(enemyShips, (offx + (CELL_SIZE * 10 + 6), MARGIN + 200))
        #    playerShipIndex = 0
        #    for ship in self.enemy_board.ships:
        #        if not ship.is_sunk():
        #            for i in range (0, ship.length):
        #                rect = pygame.Rect(offx + (CELL_SIZE * 10 + 6) + (CELL_SIZE/2 * i), MARGIN + (26) + (CELL_SIZE/2 * playerShipIndex) + 3 * (playerShipIndex) + 200, CELL_SIZE/2, CELL_SIZE/2)
#
        #                grid = [pygame.Rect(offx + (CELL_SIZE * 10 + 6) + (CELL_SIZE/2 * i), MARGIN + (26) + (CELL_SIZE/2 * playerShipIndex) + 3 * (playerShipIndex) + 200, CELL_SIZE/2, 1),
        #                pygame.Rect(offx + (CELL_SIZE * 10 + 6) + (CELL_SIZE/2 * i), MARGIN + (26) + (CELL_SIZE/2 * playerShipIndex) + 3 * (playerShipIndex) + 200, 1, CELL_SIZE/2),
        #                pygame.Rect(offx + (CELL_SIZE * 10 + 6) + (CELL_SIZE/2 * i), MARGIN + (26) + (CELL_SIZE/2 * (playerShipIndex + 1)) - 1 + 3 * (playerShipIndex) + 200, CELL_SIZE/2, 1),
        #                pygame.Rect(offx + (CELL_SIZE * 10 + 6) + (CELL_SIZE/2 * (i + 1)) - 1, MARGIN + (26) + (CELL_SIZE/2 * playerShipIndex) + 3 * (playerShipIndex) + 200, 1, CELL_SIZE/2)]
#
        #                pygame.draw.rect(self.screen, SHIP_TILE_COLOR, rect)
        #                pygame.draw.rect(self.screen, GRID_COLOR, grid[0])
        #                pygame.draw.rect(self.screen, GRID_COLOR, grid[1])
        #                pygame.draw.rect(self.screen, GRID_COLOR, grid[2])
        #                pygame.draw.rect(self.screen, GRID_COLOR, grid[3])
        #            playerShipIndex += 1
        if(self.sunk_opponent_ship):
            enemyShips = infoFont.render('You\'ve Sunk A Ship!', True, (255, 255, 255))
            self.screen.blit(enemyShips, (offx + (CELL_SIZE * 10 + 6), MARGIN + 385))
        if(self.sunk_player_ship):
            enemyShips = infoFont.render('A Ship Has Sunk!', True, (255, 255, 255))
            self.screen.blit(enemyShips, (offx + (CELL_SIZE * 10 + 6), MARGIN + 385))
                

        pygame.display.flip()

    def game_over(self, won):
        font = pygame.font.SysFont(None, 48)
        text = 'You won!' if won else 'You lost!'
        img = font.render(text, True, (0, 0, 0))
        back_rect = pygame.Rect(WINDOW_WIDTH // 2 - img.get_width() // 2 - 5, WINDOW_HEIGHT // 2 - img.get_height() // 2 - 5, img.get_width() + 10, img.get_height() + 10)
        border_back_rect = pygame.Rect(WINDOW_WIDTH // 2 - img.get_width() // 2 - 8, WINDOW_HEIGHT // 2 - img.get_height() // 2 - 8, img.get_width() + 16, img.get_height() + 16)
        pygame.draw.rect(self.screen, (0, 0, 0), border_back_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), back_rect)
        self.screen.blit(img, (WINDOW_WIDTH // 2 - img.get_width() // 2, WINDOW_HEIGHT // 2 - img.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(10000)
        self.running = False

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python battleship.py server|client host [port]')
        sys.exit(1)
    role = sys.argv[1]
    host = sys.argv[2] if len(sys.argv) > 2 else 'localhost'
    port = int(sys.argv[3]) if len(sys.argv) > 3 else 5000
    Game(role, host, port).run()
