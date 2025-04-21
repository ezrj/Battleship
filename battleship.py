# Directory Structure
# 
# ├── assets/
# │   ├── water.png            # Placeholder: image for water cell
# │   ├── ship_horizontal.png  # Placeholder: horizontal ship segment
# │   ├── ship_vertical.png    # Placeholder: vertical ship segment
# │   ├── hit.png              # Placeholder: image for hit marker
# │   └── miss.png             # Placeholder: image for miss marker
# └── battleship.py            # Main script

"""
battleship.py

Usage:
    python battleship.py server [port]
    python battleship.py client <server_ip> [port]

This script runs a networked Battleship game using pygame. One instance runs as the server,
binds to a port and waits for a connection. The other runs as the client and connects to the server.
Each side places ships randomly, then players take turns clicking the opponent's grid to fire.
"""

import sys
import socket
import pickle
import random
import pygame

# Grid and window settings
CELL_SIZE = 40
GRID_SIZE = 10
MARGIN = 20
SCREEN_WIDTH = CELL_SIZE * GRID_SIZE * 2 + MARGIN * 3
SCREEN_HEIGHT = CELL_SIZE * GRID_SIZE + MARGIN * 2
FPS = 30


ASSETS_DIR = 'assets'
WATER_IMG = f"{ASSETS_DIR}/water.png"
SHIP_H_IMG = f"{ASSETS_DIR}/ship_horizontal.png"
SHIP_V_IMG = f"{ASSETS_DIR}/ship_vertical.png"
HIT_IMG = f"{ASSETS_DIR}/hit.png"
MISS_IMG = f"{ASSETS_DIR}/miss.png"

# Helper to load images with fallback to colored square
def load_image(path, fallback_color):
    try:
        img = pygame.image.load(path)
        return pygame.transform.scale(img, (CELL_SIZE, CELL_SIZE))
    except Exception:
        surface = pygame.Surface((CELL_SIZE, CELL_SIZE))
        surface.fill(fallback_color)
        return surface

class Board:
    def __init__(self):
        # 0 = empty, 1 = ship
        self.grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.ships = []
        self.hits = set()
        self.misses = set()
        self.place_ships_randomly()

    def place_ships_randomly(self):
        # Standard battleship lengths
        lengths = [5, 4, 3, 3, 2]
        for length in lengths:
            placed = False
            while not placed:
                orient = random.choice(['H', 'V'])
                if orient == 'H':
                    x = random.randint(0, GRID_SIZE - length)
                    y = random.randint(0, GRID_SIZE - 1)
                    coords = [(x + i, y) for i in range(length)]
                else:
                    x = random.randint(0, GRID_SIZE - 1)
                    y = random.randint(0, GRID_SIZE - length)
                    coords = [(x, y + i) for i in range(length)]
                # Check overlap
                if all(self.grid[cy][cx] == 0 for cx, cy in coords):
                    for cx, cy in coords:
                        self.grid[cy][cx] = 1
                    self.ships.append(coords)
                    placed = True

    def receive_attack(self, x, y):
        if (x, y) in self.hits or (x, y) in self.misses:
            return 'already'
        if self.grid[y][x] == 1:
            self.hits.add((x, y))
            return 'hit'
        else:
            self.misses.add((x, y))
            return 'miss'

    def all_sunk(self):
        # Check if every ship's cells are in hits
        return all(all((cx, cy) in self.hits for cx, cy in ship) for ship in self.ships)

# Draw a board at horizontal offset offset_x
def draw_board(screen, board, offset_x, show_ships):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x = offset_x + col * CELL_SIZE
            y = MARGIN + row * CELL_SIZE
            # Draw water background
            screen.blit(water_img, (x, y))
            # Optionally draw ships
            if show_ships and board.grid[row][col] == 1:
                screen.blit(ship_h_img, (x, y))  # Using horizontal image for all segments
            # Draw misses
            if (col, row) in board.misses:
                screen.blit(miss_img, (x, y))
            # Draw hits
            if (col, row) in board.hits:
                screen.blit(hit_img, (x, y))


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ('server', 'client'):
        print(__doc__)
        sys.exit(1)
    role = sys.argv[1]
    # Default port
    port = int(sys.argv[2]) if len(sys.argv) >= 3 and role == 'server' else 50007
    if role == 'server':
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('', port))
        sock.listen(1)
        print(f"Waiting for connection on port {port}...")
        conn, addr = sock.accept()
        print(f"Connected by {addr}")
    else:
        if len(sys.argv) < 3:
            print("Usage: python battleship.py client <server_ip> [port]")
            sys.exit(1)
        host = sys.argv[2]
        port = int(sys.argv[3]) if len(sys.argv) >= 4 else 50007
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(f"Connecting to {host}:{port}...")
        conn.connect((host, port))
        print("Connected to server")

    # Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Battleship")
    clock = pygame.time.Clock()

    # Load images
    global water_img, ship_h_img, ship_v_img, hit_img, miss_img
    water_img = load_image(WATER_IMG, (0, 0, 128))
    ship_h_img = load_image(SHIP_H_IMG, (192, 192, 192))
    ship_v_img = load_image(SHIP_V_IMG, (192, 192, 192))
    hit_img = load_image(HIT_IMG, (255, 0, 0))
    miss_img = load_image(MISS_IMG, (255, 255, 255))

    # Create boards
    my_board = Board()
    opp_board = Board()
    my_turn = (role == 'server')
    running = True

    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            # Handle click on opponent's grid when it's our turn
            if event.type == pygame.MOUSEBUTTONDOWN and my_turn:
                mx, my = pygame.mouse.get_pos()
                opp_offset = MARGIN * 2 + GRID_SIZE * CELL_SIZE
                if opp_offset <= mx < opp_offset + GRID_SIZE * CELL_SIZE and MARGIN <= my < MARGIN + GRID_SIZE * CELL_SIZE:
                    col = (mx - opp_offset) // CELL_SIZE
                    row = (my - MARGIN) // CELL_SIZE
                    # Send attack
                    conn.sendall(pickle.dumps({'type': 'attack', 'x': col, 'y': row}))
                    # Receive result
                    data = conn.recv(4096)
                    msg = pickle.loads(data)
                    if msg['type'] == 'result':
                        if msg['result'] == 'hit':
                            opp_board.hits.add((col, row))
                        elif msg['result'] == 'miss':
                            opp_board.misses.add((col, row))
                    elif msg['type'] == 'game_over':
                        print("You win!")
                        running = False
                    my_turn = False

        # If it's opponent's turn, wait for their attack
        if not my_turn and running:
            data = conn.recv(4096)
            msg = pickle.loads(data)
            if msg['type'] == 'attack':
                x, y = msg['x'], msg['y']
                result = my_board.receive_attack(x, y)
                conn.sendall(pickle.dumps({'type': 'result', 'result': result}))
                if my_board.all_sunk():
                    conn.sendall(pickle.dumps({'type': 'game_over'}))
                    print("You lose!")
                    running = False
                my_turn = True

        # Draw boards
        screen.fill((0, 0, 0))
        # Draw our board on the left (show ships)
        draw_board(screen, my_board, MARGIN, show_ships=True)
        # Draw opponent board on the right (hide ships)
        draw_board(screen, opp_board, MARGIN * 2 + GRID_SIZE * CELL_SIZE, show_ships=False)

        pygame.display.flip()
        clock.tick(FPS)

    conn.close()
    pygame.quit()

if __name__ == "__main__":
    main()

