import pygame

# Initialize Pygame
pygame.init()

# Define constants for screen dimensions and colors
SCREEN_WIDTH, SCREEN_HEIGHT = 300, 300
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 40
BALL_SIZE = 10
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FRAMERATE = 60
WINNING_SCORE = 50  # Score needed to win the game

# Class representing a paddle
class Paddle:
    def __init__(self, x, y, is_player=True):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)  # Paddle's position and size
        self.is_player = is_player  # Determines if it's the player or computer paddle

    def move(self, direction, speed):
        if self.is_player:
            # Move player paddle based on input direction
            self.rect.y += direction * speed
            # Ensure paddle stays within the screen bounds
            self.rect.y = max(min(self.rect.y, SCREEN_HEIGHT - PADDLE_HEIGHT), 0)

    def update(self, ball):
        if not self.is_player:
            # Simple AI to follow the ball
            if self.rect.centery < ball.rect.centery:
                self.rect.y += 2
            elif self.rect.centery > ball.rect.centery:
                self.rect.y -= 2
            # Ensure AI paddle stays within bounds
            self.rect.y = max(min(self.rect.y, SCREEN_HEIGHT - PADDLE_HEIGHT), 0)

# Class representing the ball
class Ball:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, BALL_SIZE, BALL_SIZE)  # Ball's position and size
        self.x_direction = 1  # Initial horizontal direction of the ball
        self.y_direction = 1  # Initial vertical direction of the ball
        self.speed = 2  # Speed of the ball

    def move(self):
        # Update ball position based on its direction and speed
        self.rect.x += self.x_direction * self.speed
        self.rect.y += self.y_direction * self.speed

        # Check for collision with top and bottom walls
        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.y_direction *= -1
        # Check for collision with left and right walls
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.x_direction *= -1

    def check_collision(self, paddle):
        # Check if ball collides with a paddle
        if self.rect.colliderect(paddle.rect):
            self.x_direction *= -1  # Reverse horizontal direction
            # Move ball out of paddle to prevent sticking
            if self.x_direction > 0:
                self.rect.left = paddle.rect.right
            else:
                self.rect.right = paddle.rect.left

# Main class to manage the game
class PongGame:
    def __init__(self):
        # Set up the game window and initialize paddles and ball
        self.screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        pygame.display.set_caption('PONG')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('freesansbold.ttf', 36)  # Larger font size for scores
        self.player_paddle = Paddle(5, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2)  # Player paddle
        self.computer_paddle = Paddle(SCREEN_WIDTH - PADDLE_WIDTH - 5, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, is_player=False)  # Computer paddle
        self.ball = Ball(SCREEN_WIDTH // 2 - BALL_SIZE // 2, SCREEN_HEIGHT // 2 - BALL_SIZE // 2)
        self.player_score = 0  # Player's score
        self.computer_score = 0  # Computer's score
        self.game_over = False  # Game over state
        self.game_paused = False  # Game paused state
        self.restart_button = pygame.Rect(70, 150, 100, 20)  # Button to restart the game
        self.player_direction = 0  # Direction of player movement

    def run(self):
        # Main game loop
        running = True
        while running:
            self.clock.tick(FRAMERATE)  # Limit the frame rate
            self.handle_events()  # Handle user input and events
            if not self.game_over and not self.game_paused:
                self.update()  # Update game state
            self.render()  # Draw everything on the screen
            pygame.display.flip()  # Update the display

        pygame.quit()  # Clean up and close the game

    def handle_events(self):
        # Process events such as key presses and mouse clicks
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.player_direction = -1  # Move player up
                if event.key == pygame.K_s:
                    self.player_direction = 1  # Move player down
                if event.key == pygame.K_p:
                    self.game_paused = not self.game_paused  # Toggle pause state
            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_w, pygame.K_s]:
                    self.player_direction = 0  # Stop player movement
            if event.type == pygame.MOUSEBUTTONDOWN and self.game_over:
                if self.restart_button.collidepoint(event.pos):
                    self.reset_game()  # Restart the game

    def update(self):
        # Update game elements
        self.player_paddle.move(self.player_direction, 5)
        self.computer_paddle.update(self.ball)
        self.ball.move()
        self.ball.check_collision(self.player_paddle)
        self.ball.check_collision(self.computer_paddle)
        self.check_score()  # Check and update scores

    def render(self):
        # Draw everything on the screen
        self.screen.fill(BLACK)  # Clear screen with black color
        pygame.draw.rect(self.screen, WHITE, self.player_paddle.rect)  # Draw player paddle
        pygame.draw.rect(self.screen, WHITE, self.computer_paddle.rect)  # Draw computer paddle
        pygame.draw.rect(self.screen, WHITE, self.ball.rect)  # Draw ball

        # Draw scores
        player_score_text = self.font.render(f'{self.player_score}', True, WHITE)
        computer_score_text = self.font.render(f'{self.computer_score}', True, WHITE)
        self.screen.blit(player_score_text, (SCREEN_WIDTH // 4 - player_score_text.get_width() // 2, 10))  # Player score at top left
        self.screen.blit(computer_score_text, (3 * SCREEN_WIDTH // 4 - computer_score_text.get_width() // 2, 10))  # Computer score at top right

        if self.game_over:
            # Draw game over text and restart button
            game_over_text = self.font.render(f'GAME OVER! Player: {self.player_score} Computer: {self.computer_score}', True, WHITE, BLACK)
            self.screen.blit(game_over_text, [SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 20])
            pygame.draw.rect(self.screen, BLACK, self.restart_button)  # Draw restart button
            restart_text = self.font.render('Press to restart', True, WHITE, BLACK)
            self.screen.blit(restart_text, [self.restart_button.x + self.restart_button.width // 2 - restart_text.get_width() // 2, self.restart_button.y + 5])

        elif self.game_paused:
            # Draw paused text
            paused_text = self.font.render('PAUSED', True, WHITE, BLACK)
            self.screen.blit(paused_text, [SCREEN_WIDTH // 2 - paused_text.get_width() // 2, SCREEN_HEIGHT // 2 - 10])

    def check_score(self):
        # Update scores based on ball position
        if self.ball.rect.left <= 0:
            self.computer_score += 1
            self.reset_ball()
        elif self.ball.rect.right >= SCREEN_WIDTH:
            self.player_score += 1
            self.reset_ball()

        # Check for game over condition
        if self.player_score >= WINNING_SCORE or self.computer_score >= WINNING_SCORE:
            self.game_over = True

    def reset_ball(self):
        # Reset ball to the center and reverse direction
        self.ball.rect.x = SCREEN_WIDTH // 2 - BALL_SIZE // 2
        self.ball.rect.y = SCREEN_HEIGHT // 2 - BALL_SIZE // 2
        self.ball.x_direction = 1 if self.ball.x_direction > 0 else -1
        self.ball.y_direction = 1 if self.ball.y_direction > 0 else -1

    def reset_game(self):
        # Reset all game variables for a new game
        self.game_over = False
        self.game_paused = False
        self.player_paddle.rect.y = SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2
        self.computer_paddle.rect.y = SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2
        self.reset_ball()
        self.player_score = 0
        self.computer_score = 0

# Start the game
if __name__ == '__main__':
    PongGame().run()
