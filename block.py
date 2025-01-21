import pygame
import sys
import random

# 初期化
pygame.init()

# 画面サイズと設定
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLOCK_WIDTH = 75
BLOCK_HEIGHT = 30
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 15
BALL_SIZE = 15

# 色の定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# 画面の設定
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Block Breaker")

# フレームレート
clock = pygame.time.Clock()
FPS = 60

# パドルのクラス
class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PADDLE_WIDTH, PADDLE_HEIGHT))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = (SCREEN_WIDTH - PADDLE_WIDTH) // 2
        self.rect.y = SCREEN_HEIGHT - 40
        self.speed = 10

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed

# ボールのクラス
class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((BALL_SIZE, BALL_SIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH // 2
        self.rect.y = SCREEN_HEIGHT // 2
        self.speed_x = random.choice([-5, 5])
        self.speed_y = -5

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # 壁との衝突
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.speed_x *= -1
        if self.rect.top <= 0:
            self.speed_y *= -1

        # 下に落ちた場合
        if self.rect.bottom >= SCREEN_HEIGHT:
            return True
        return False

# ブロックのクラス
class Block(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((BLOCK_WIDTH, BLOCK_HEIGHT))
        self.image.fill(random.choice([GREEN, BLUE, WHITE]))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# グループの作成
all_sprites = pygame.sprite.Group()
blocks = pygame.sprite.Group()
paddle = Paddle()
ball = Ball()
all_sprites.add(paddle, ball)

# ブロックを作成
for row in range(5):
    for col in range(SCREEN_WIDTH // BLOCK_WIDTH):
        block = Block(col * BLOCK_WIDTH, row * BLOCK_HEIGHT)
        blocks.add(block)
        all_sprites.add(block)

# ゲームループ
running = True
misses = 0  # ミスのカウント
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 更新
    paddle.update()
    game_over = ball.update()

    # ボールとパドルの衝突
    if ball.rect.colliderect(paddle.rect):
        ball.speed_y *= -1

    # ボールとブロックの衝突
    block_hit_list = pygame.sprite.spritecollide(ball, blocks, True)
    if block_hit_list:
        ball.speed_y *= -1

    # ボールが下に落ちた場合
    if game_over:
        misses += 1
        if misses >= 3:
            print("Game Over")
            running = False
        else:
            # ボールをリセット
            ball.rect.x = SCREEN_WIDTH // 2
            ball.rect.y = SCREEN_HEIGHT // 2
            ball.speed_x = random.choice([-5, 5])
            ball.speed_y = -5

    # 描画
    screen.fill(BLACK)
    all_sprites.draw(screen)

    # ミスの表示
    font = pygame.font.SysFont(None, 36)
    text = font.render(f"Misses: {misses}/3", True, WHITE)
    screen.blit(text, (10, 10))

    # 画面更新
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
