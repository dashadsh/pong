import pygame
import sys

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 600, 300
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 60  # classic Pong paddle height
BALL_SIZE = 10
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
PINK = (255, 105, 180)

FRAMERATE = 60
WINNING_SCORE = 5 # Reduced for testing
BALL_SPEED = 4

class Paddle:
    def __init__(self, x, y, is_player=True):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)  # paddle's position and size
        self.is_player = is_player  # determine if it's the player or computer paddle

    def move(self, direction, speed):
        if self.is_player:
            # move player's paddle based on input direction
            self.rect.y += direction * speed
            # make paddle stay within the screen bounds
            self.rect.y = max(min(self.rect.y, SCREEN_HEIGHT - PADDLE_HEIGHT), 0)

    def update(self, ball):
        if not self.is_player:
            # simple AI to follow the ball
            if self.rect.centery < ball.rect.centery:
                self.rect.y += 3  # increase speed for AI
            elif self.rect.centery > ball.rect.centery:
                self.rect.y -= 3
            # make AI paddle stay within the screen bounds
            self.rect.y = max(min(self.rect.y, SCREEN_HEIGHT - PADDLE_HEIGHT), 0)

class Ball:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, BALL_SIZE, BALL_SIZE)  # ball's position & size
        self.x_direction = 1  # init. horizontal direction of the ball
        self.y_direction = 1  # init. vertical direction of the ball
        self.speed = BALL_SPEED  # ibcreased ball speed for better gameplay

    def move(self):
        # upd. ball position based on its direction and speed
        self.rect.x += self.x_direction * self.speed
        self.rect.y += self.y_direction * self.speed

        # check for collision with top and bottom walls
        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.y_direction *= -1
        # check for collision with left and right walls
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.x_direction *= -1

    def check_collision(self, paddle):
        # check if ball collides with a paddle
        if self.rect.colliderect(paddle.rect):
            self.x_direction *= -1  # reverse horizontal direction
            # move ball out of paddle to prevent sticking
            if self.x_direction > 0:
                self.rect.left = paddle.rect.right
            else:
                self.rect.right = paddle.rect.left

class PongGame:
    def __init__(self):
        # game window setup. paddles and ball init.
        self.screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        pygame.display.set_caption('PONG')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('freesansbold.ttf', 16)  # Font size for scores
        self.player_paddle = Paddle(5, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2)  # Player paddle
        self.computer_paddle = Paddle(SCREEN_WIDTH - PADDLE_WIDTH - 5, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, is_player=False)  # computer paddle
        self.ball = Ball(SCREEN_WIDTH // 2 - BALL_SIZE // 2, SCREEN_HEIGHT // 2 - BALL_SIZE // 2)
        self.player_score = 0  # player's score
        self.computer_score = 0  # computer's score
        self.game_over = False  # game over state
        self.game_paused = False  # game paused state
        self.restart_button = pygame.Rect(70, 150, 160, 30)  # button to restart the game
        self.player_direction = 0  # direction of player movement

    def run(self):
        while True:
            self.clock.tick(FRAMERATE)  # limit frame rate
            self.handle_events()  # handle user input and events
            if not self.game_over and not self.game_paused:
                self.update()  # upd game state
            self.render()  # draw everything on the screen
            pygame.display.flip()  # upd the display

    def handle_events(self):
        # handle events such as key presses and mouse clicks
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.player_direction = -1  # move player up
                if event.key == pygame.K_s:
                    self.player_direction = 1  # move player down
                if event.key == pygame.K_p:
                    self.game_paused = not self.game_paused  # toggle pause state
            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_w, pygame.K_s]:
                    self.player_direction = 0  # stop player movement
            if event.type == pygame.MOUSEBUTTONDOWN and self.game_over:
                if self.restart_button.collidepoint(event.pos):
                    self.reset_game()  # restart the game

    def update(self):
        # upd game elements
        self.player_paddle.move(self.player_direction, 5)
        self.computer_paddle.update(self.ball)
        self.ball.move()
        self.ball.check_collision(self.player_paddle)
        self.ball.check_collision(self.computer_paddle)
        self.check_score()  # check and update scores

    def render(self):
        # draw everything on the screen
        self.screen.fill(BLACK)  # clear screen with black color

        # draw paddles and ball
        pygame.draw.rect(self.screen, WHITE, self.player_paddle.rect)  # draw player paddle
        pygame.draw.rect(self.screen, WHITE, self.computer_paddle.rect)  # draw computer paddle
        pygame.draw.rect(self.screen, WHITE, self.ball.rect)  # draw ball

        # draw center line
        pygame.draw.aaline(self.screen, WHITE, (SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT))

        # draw scores
        player_score_text = self.font.render(f'{self.player_score}', True, WHITE)
        computer_score_text = self.font.render(f'{self.computer_score}', True, WHITE)
        self.screen.blit(player_score_text, (SCREEN_WIDTH // 4 - player_score_text.get_width() // 2, 10))  # Player score at top left
        self.screen.blit(computer_score_text, (3 * SCREEN_WIDTH // 4 - computer_score_text.get_width() // 2, 10))  # Computer score at top right

        if self.game_over:
            # draw game over text and restart button
            game_over_text = self.font.render(f'GAME OVER! Player: {self.player_score} Computer: {self.computer_score}', True, WHITE)
            self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 40))
            pygame.draw.rect(self.screen, PINK, self.restart_button)  # Draw restart button
            restart_text = self.font.render('Press to restart', True, BLACK)
            self.screen.blit(restart_text, [self.restart_button.x + self.restart_button.width // 2 - restart_text.get_width() // 2, self.restart_button.y + 5])

        elif self.game_paused:
            # draw paused text
            paused_text = self.font.render('PAUSED', True, WHITE, BLACK)
            self.screen.blit(paused_text, [SCREEN_WIDTH // 2 - paused_text.get_width() // 2, SCREEN_HEIGHT // 2 - 10])

    def check_score(self):
        # upd. scores based on ball position
        if self.ball.rect.left <= 0:
            self.computer_score += 1
            self.reset_ball()
        elif self.ball.rect.right >= SCREEN_WIDTH:
            self.player_score += 1
            self.reset_ball()

        # check for game over condition
        if self.player_score >= WINNING_SCORE or self.computer_score >= WINNING_SCORE:
            self.game_over = True

    def reset_ball(self):
        # reset ball to the center and reverse direction
        self.ball.rect.x = SCREEN_WIDTH // 2 - BALL_SIZE // 2
        self.ball.rect.y = SCREEN_HEIGHT // 2 - BALL_SIZE // 2
        self.ball.x_direction = 1 if self.ball.x_direction > 0 else -1
        self.ball.y_direction = 1 if self.ball.y_direction > 0 else -1

    def reset_game(self):
        # reset the game state
        self.player_paddle.rect.y = SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2
        self.computer_paddle.rect.y = SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2
        self.reset_ball()
        self.player_score = 0
        self.computer_score = 0
        self.game_over = False

if __name__ == '__main__':
    PongGame().run()
