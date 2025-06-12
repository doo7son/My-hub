import pygame
import math
import random
import sys

# 게임 초기화
pygame.init()

# 화면 설정
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
HALF_WIDTH = SCREEN_WIDTH // 2
HALF_HEIGHT = SCREEN_HEIGHT // 2

# 색상
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
LIGHT_GRAY = (192, 192, 192)

# 게임 설정
TILE_SIZE = 64
MAP_WIDTH = 16
MAP_HEIGHT = 12
FOV = math.pi / 3  # 60도 시야각
HALF_FOV = FOV / 2
NUM_RAYS = SCREEN_WIDTH // 2
DELTA_ANGLE = FOV / NUM_RAYS
MAX_DEPTH = int(MAP_WIDTH * TILE_SIZE)

# 미니맵 설정
MINIMAP_SCALE = 0.2
MINIMAP_SIZE = 150

# 맵 데이터 (1: 벽, 0: 빈 공간)
WORLD_MAP = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,1,1,1,0,0,0,0,1,1,1,0,0,1],
    [1,0,0,1,0,0,0,0,0,0,0,0,1,0,0,1],
    [1,0,0,1,0,0,0,1,1,0,0,0,1,0,0,1],
    [1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,1,0,0,0,0,0,0,0,0,1,0,0,1],
    [1,0,0,1,1,1,0,0,0,0,1,1,1,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0
        self.speed = 2
        self.rot_speed = 0.05
        
    def move(self, keys, world_map):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        
        dx = dy = 0
        
        if keys[pygame.K_w]:  # 앞으로
            dx += cos_a * self.speed
            dy += sin_a * self.speed
        if keys[pygame.K_s]:  # 뒤로
            dx -= cos_a * self.speed
            dy -= sin_a * self.speed
        if keys[pygame.K_a]:  # 왼쪽으로
            dx += sin_a * self.speed
            dy -= cos_a * self.speed
        if keys[pygame.K_d]:  # 오른쪽으로
            dx -= sin_a * self.speed
            dy += cos_a * self.speed
        
        # 벽 충돌 체크
        new_x = self.x + dx
        new_y = self.y + dy
        
        if self.check_wall_collision(new_x, self.y, world_map):
            new_x = self.x
        if self.check_wall_collision(self.x, new_y, world_map):
            new_y = self.y
            
        self.x = new_x
        self.y = new_y
        
        # 회전
        if keys[pygame.K_LEFT]:
            self.angle -= self.rot_speed
        if keys[pygame.K_RIGHT]:
            self.angle += self.rot_speed
    
    def check_wall_collision(self, x, y, world_map):
        map_x = int(x // TILE_SIZE)
        map_y = int(y // TILE_SIZE)
        
        if (0 <= map_x < MAP_WIDTH and 0 <= map_y < MAP_HEIGHT):
            return world_map[map_y][map_x] == 1
        return True

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.alive = True
        self.size = 32
        self.color = RED
    
    def get_distance(self, player):
        return math.sqrt((self.x - player.x)**2 + (self.y - player.y)**2)
    
    def draw_on_minimap(self, screen, offset_x, offset_y):
        if self.alive:
            mini_x = int(self.x * MINIMAP_SCALE) + offset_x
            mini_y = int(self.y * MINIMAP_SCALE) + offset_y
            pygame.draw.circle(screen, self.color, (mini_x, mini_y), 3)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("1인칭 FPS 게임")
        self.clock = pygame.time.Clock()
        
        # 플레이어 시작 위치
        self.player = Player(TILE_SIZE * 1.5, TILE_SIZE * 1.5)
        
        # 적들 생성
        self.enemies = [
            Enemy(TILE_SIZE * 3, TILE_SIZE * 3),
            Enemy(TILE_SIZE * 8, TILE_SIZE * 5),
            Enemy(TILE_SIZE * 12, TILE_SIZE * 8),
            Enemy(TILE_SIZE * 6, TILE_SIZE * 9)
        ]
        
        self.font = pygame.font.Font(None, 36)
        self.score = 0
        
        # 크로스헤어 설정
        self.crosshair_size = 10
        
    def cast_ray(self, start_angle):
        sin_a = math.sin(start_angle)
        cos_a = math.cos(start_angle)
        
        # 수직선 체크
        x_map, y_map = int(self.player.x // TILE_SIZE), int(self.player.y // TILE_SIZE)
        
        if cos_a > 0:
            x_vert = (x_map + 1) * TILE_SIZE
            dx = TILE_SIZE
        else:
            x_vert = x_map * TILE_SIZE - 1e-6
            dx = -TILE_SIZE
            
        depth_vert = (x_vert - self.player.x) / cos_a
        y_vert = self.player.y + depth_vert * sin_a
        
        delta_depth = dx / cos_a
        dy = delta_depth * sin_a
        
        for i in range(MAX_DEPTH // TILE_SIZE):
            tile_vert = int(x_vert // TILE_SIZE), int(y_vert // TILE_SIZE)
            if tile_vert[0] < 0 or tile_vert[0] >= MAP_WIDTH or tile_vert[1] < 0 or tile_vert[1] >= MAP_HEIGHT:
                break
            if WORLD_MAP[tile_vert[1]][tile_vert[0]]:
                break
            x_vert += dx
            y_vert += dy
            depth_vert += delta_depth
            
        # 수평선 체크
        if sin_a > 0:
            y_hor = (y_map + 1) * TILE_SIZE
            dy = TILE_SIZE
        else:
            y_hor = y_map * TILE_SIZE - 1e-6
            dy = -TILE_SIZE
            
        depth_hor = (y_hor - self.player.y) / sin_a
        x_hor = self.player.x + depth_hor * cos_a
        
        delta_depth = dy / sin_a
        dx = delta_depth * cos_a
        
        for i in range(MAX_DEPTH // TILE_SIZE):
            tile_hor = int(x_hor // TILE_SIZE), int(y_hor // TILE_SIZE)
            if tile_hor[0] < 0 or tile_hor[0] >= MAP_WIDTH or tile_hor[1] < 0 or tile_hor[1] >= MAP_HEIGHT:
                break
            if WORLD_MAP[tile_hor[1]][tile_hor[0]]:
                break
            x_hor += dx
            y_hor += dy
            depth_hor += delta_depth
            
        # 더 가까운 거리 선택
        if depth_vert < depth_hor:
            depth = depth_vert
        else:
            depth = depth_hor
            
        return depth
    
    def draw_3d_walls(self):
        ray_angle = self.player.angle - HALF_FOV
        
        for ray in range(NUM_RAYS):
            depth = self.cast_ray(ray_angle)
            
            # 어안 렌즈 효과 보정
            depth *= math.cos(self.player.angle - ray_angle)
            
            # 벽 높이 계산
            proj_height = SCREEN_HEIGHT / (depth + 0.0001)
            
            # 벽 색상 (거리에 따라 어두워짐)
            color_intensity = max(0, min(255, 255 - int(depth * 0.5)))
            wall_color = (color_intensity // 3, color_intensity // 3, color_intensity)
            
            # 벽 그리기
            wall_top = (SCREEN_HEIGHT - proj_height) // 2
            wall_bottom = wall_top + proj_height
            
            pygame.draw.line(self.screen, wall_color, 
                           (ray * 2, wall_top), (ray * 2, wall_bottom), 2)
            
            ray_angle += DELTA_ANGLE
    
    def draw_enemies_3d(self):
        # 적들을 거리순으로 정렬 (멀리 있는 것부터)
        enemies_with_distance = []
        for enemy in self.enemies:
            if enemy.alive:
                distance = enemy.get_distance(self.player)
                enemies_with_distance.append((enemy, distance))
        
        enemies_with_distance.sort(key=lambda x: x[1], reverse=True)
        
        for enemy, distance in enemies_with_distance:
            # 적의 각도 계산
            enemy_angle = math.atan2(enemy.y - self.player.y, enemy.x - self.player.x)
            angle_diff = enemy_angle - self.player.angle
            
            # 각도 정규화
            while angle_diff > math.pi:
                angle_diff -= 2 * math.pi
            while angle_diff < -math.pi:
                angle_diff += 2 * math.pi
            
            # 시야각 내에 있는지 확인
            if abs(angle_diff) < HALF_FOV:
                # 화면 위치 계산
                screen_x = HALF_WIDTH + int(angle_diff / HALF_FOV * HALF_WIDTH)
                enemy_size = max(10, int(SCREEN_HEIGHT / (distance + 0.0001) * 30))
                
                # 적 그리기
                enemy_rect = pygame.Rect(screen_x - enemy_size//2, 
                                       HALF_HEIGHT - enemy_size//2,
                                       enemy_size, enemy_size)
                pygame.draw.ellipse(self.screen, enemy.color, enemy_rect)
                pygame.draw.ellipse(self.screen, BLACK, enemy_rect, 2)
    
    def draw_minimap(self):
        # 미니맵 배경
        minimap_surface = pygame.Surface((MINIMAP_SIZE, MINIMAP_SIZE))
        minimap_surface.fill(BLACK)
        
        # 맵 그리기
        for y in range(MAP_HEIGHT):
            for x in range(MAP_WIDTH):
                if WORLD_MAP[y][x]:
                    rect = pygame.Rect(x * TILE_SIZE * MINIMAP_SCALE,
                                     y * TILE_SIZE * MINIMAP_SCALE,
                                     TILE_SIZE * MINIMAP_SCALE,
                                     TILE_SIZE * MINIMAP_SCALE)
                    pygame.draw.rect(minimap_surface, WHITE, rect)
        
        # 플레이어 그리기
        player_x = int(self.player.x * MINIMAP_SCALE)
        player_y = int(self.player.y * MINIMAP_SCALE)
        pygame.draw.circle(minimap_surface, GREEN, (player_x, player_y), 3)
        
        # 시선 방향 표시
        end_x = player_x + int(math.cos(self.player.angle) * 15)
        end_y = player_y + int(math.sin(self.player.angle) * 15)
        pygame.draw.line(minimap_surface, GREEN, (player_x, player_y), (end_x, end_y), 2)
        
        # 적들 그리기
        for enemy in self.enemies:
            if enemy.alive:
                enemy_x = int(enemy.x * MINIMAP_SCALE)
                enemy_y = int(enemy.y * MINIMAP_SCALE)
                pygame.draw.circle(minimap_surface, RED, (enemy_x, enemy_y), 2)
        
        # 미니맵을 메인 화면에 그리기
        self.screen.blit(minimap_surface, (SCREEN_WIDTH - MINIMAP_SIZE - 10, 10))
        pygame.draw.rect(self.screen, WHITE, 
                        (SCREEN_WIDTH - MINIMAP_SIZE - 10, 10, MINIMAP_SIZE, MINIMAP_SIZE), 2)
    
    def draw_crosshair(self):
        # 크로스헤어 그리기
        pygame.draw.line(self.screen, WHITE,
                        (HALF_WIDTH - self.crosshair_size, HALF_HEIGHT),
                        (HALF_WIDTH + self.crosshair_size, HALF_HEIGHT), 2)
        pygame.draw.line(self.screen, WHITE,
                        (HALF_WIDTH, HALF_HEIGHT - self.crosshair_size),
                        (HALF_WIDTH, HALF_HEIGHT + self.crosshair_size), 2)
    
    def draw_ui(self):
        # 점수 표시
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # 조작법 표시
        controls = [
            "WASD: Move",
            "Arrow Keys: Look",
            "Mouse: Shoot",
            "ESC: Quit"
        ]
        
        for i, control in enumerate(controls):
            text = pygame.font.Font(None, 24).render(control, True, WHITE)
            self.screen.blit(text, (10, SCREEN_HEIGHT - 100 + i * 20))
    
    def check_enemy_hit(self, mouse_pos):
        # 마우스 클릭으로 적 제거
        for enemy in self.enemies:
            if enemy.alive:
                distance = enemy.get_distance(self.player)
                if distance < 200:  # 사정거리 내에 있을 때만
                    enemy_angle = math.atan2(enemy.y - self.player.y, enemy.x - self.player.x)
                    angle_diff = enemy_angle - self.player.angle
                    
                    # 각도 정규화
                    while angle_diff > math.pi:
                        angle_diff -= 2 * math.pi
                    while angle_diff < -math.pi:
                        angle_diff += 2 * math.pi
                    
                    # 조준선 근처에서 클릭했는지 확인
                    if abs(angle_diff) < 0.2:  # 약 11도 정도의 여유
                        enemy.alive = False
                        self.score += 100
                        break
    
    def run(self):
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # 왼쪽 마우스 버튼
                        self.check_enemy_hit(event.pos)
            
            # 키 입력 처리
            keys = pygame.key.get_pressed()
            self.player.move(keys, WORLD_MAP)
            
            # 화면 그리기
            self.screen.fill(BLACK)
            
            # 하늘과 바닥
            pygame.draw.rect(self.screen, DARK_GRAY, (0, 0, SCREEN_WIDTH, HALF_HEIGHT))  # 하늘
            pygame.draw.rect(self.screen, GRAY, (0, HALF_HEIGHT, SCREEN_WIDTH, HALF_HEIGHT))  # 바닥
            
            # 3D 렌더링
            self.draw_3d_walls()
            self.draw_enemies_3d()
            
            # UI 그리기
            self.draw_crosshair()
            self.draw_minimap()
            self.draw_ui()
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

# 게임 실행
if __name__ == "__main__":
    game = Game()
    game.run()