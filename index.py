import pygame
import random

# 游戏常量
BLOCK_SIZE = 40
GRID_WIDTH = 10
GRID_HEIGHT = 20
WIDTH = BLOCK_SIZE * GRID_WIDTH
HEIGHT = BLOCK_SIZE * GRID_HEIGHT
FPS = 30

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = {
    'I': (0, 255, 255),    # 青色
    'O': (255, 255, 0),    # 黄色
    'J': (0, 0, 255),      # 蓝色
    'L': (255, 165, 0),    # 橙色
    'Z': (255, 0, 0),      # 红色
    'S': (0, 255, 0),      # 绿色
    'T': (128, 0, 128)     # 紫色
}

# 方块文本
TEXTS = {
    'I': '王者荣耀',
    'O': '王明霞',
    'J': '雷东燕',
    'L': '樊亚春',
    'Z': '雷东莺',
    'S': '王绣朝',
    'T': '侯大宇'
}

# 方块形状
SHAPES = {
    'I': [[(0, 0), (0, 1), (0, 2), (0, 3)],
          [(0, 0), (1, 0), (2, 0), (3, 0)]],
    'O': [[(0, 0), (0, 1), (1, 0), (1, 1)]],
    'J': [[(0, 0), (1, 0), (1, 1), (1, 2)],
          [(0, 1), (0, 0), (1, 0), (2, 0)],
          [(0, 0), (0, 1), (0, 2), (1, 2)],
          [(0, 1), (1, 1), (2, 1), (2, 0)]],
    'L': [[(0, 2), (1, 0), (1, 1), (1, 2)],
          [(0, 0), (0, 1), (1, 1), (2, 1)],
          [(0, 0), (0, 1), (0, 2), (1, 0)],
          [(0, 0), (1, 0), (2, 0), (2, 1)]],
    'Z': [[(0, 0), (0, 1), (1, 1), (1, 2)],
          [(0, 1), (1, 0), (1, 1), (2, 0)]],
    'S': [[(0, 1), (0, 2), (1, 0), (1, 1)],
          [(0, 0), (1, 0), (1, 1), (2, 1)]],
    'T': [[(0, 1), (1, 0), (1, 1), (1, 2)],
          [(0, 1), (1, 0), (1, 1), (2, 1)],
          [(1, 0), (1, 1), (1, 2), (2, 1)],
          [(0, 1), (1, 1), (1, 2), (2, 1)]]
}

class Tetris:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("俄罗斯方块")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('simhei', 20)
        self.grid = [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = self.new_piece()
        self.game_over = False

    def new_piece(self):
        shape_type = random.choice(list(SHAPES.keys()))
        return {
            'type': shape_type,
            'shape': SHAPES[shape_type][0],
            'x': GRID_WIDTH // 2 - 2,
            'y': 0,
            'rotation': 0
        }

    def check_collision(self, piece, dx, dy, rotation):
        new_shape = SHAPES[piece['type']][rotation]
        for (x, y) in new_shape:
            px = piece['x'] + x + dx
            py = piece['y'] + y + dy
            if px < 0 or px >= GRID_WIDTH or py >= GRID_HEIGHT:
                return True
            if py >=0 and self.grid[py][px]:
                return True
        return False

    def lock_piece(self, piece):
        for (x, y) in piece['shape']:
            px = piece['x'] + x
            py = piece['y'] + y
            if py >= 0:
                self.grid[py][px] = piece['type']
        self.clear_lines()

    def clear_lines(self):
        lines_to_clear = [i for i, row in enumerate(self.grid) if all(row)]
        for i in lines_to_clear:
            del self.grid[i]
            self.grid.insert(0, [None for _ in range(GRID_WIDTH)])

    def draw_block(self, x, y, block_type):
        color = COLORS[block_type]
        pygame.draw.rect(self.screen, color, (x*BLOCK_SIZE, y*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
        text = self.font.render(TEXTS[block_type], True, WHITE)
        text_rect = text.get_rect(center=(x*BLOCK_SIZE + BLOCK_SIZE//2, y*BLOCK_SIZE + BLOCK_SIZE//2))
        self.screen.blit(text, text_rect)

    def draw_grid(self):
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.grid[y][x]:
                    self.draw_block(x, y, self.grid[y][x])

    def draw_piece(self, piece):
        for (x, y) in piece['shape']:
            px = piece['x'] + x
            py = piece['y'] + y
            if py >= 0:
                self.draw_block(px, py, piece['type'])

    def run(self):
        fall_time = 0
        fall_speed = 500

        while not self.game_over:
            self.screen.fill(BLACK)
            delta_time = self.clock.get_rawtime()
            fall_time += delta_time

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        if not self.check_collision(self.current_piece, -1, 0, self.current_piece['rotation']):
                            self.current_piece['x'] -= 1
                    if event.key == pygame.K_RIGHT:
                        if not self.check_collision(self.current_piece, 1, 0, self.current_piece['rotation']):
                            self.current_piece['x'] += 1
                    if event.key == pygame.K_DOWN:
                        if not self.check_collision(self.current_piece, 0, 1, self.current_piece['rotation']):
                            self.current_piece['y'] += 1
                    if event.key == pygame.K_UP:
                        new_rotation = (self.current_piece['rotation'] + 1) %