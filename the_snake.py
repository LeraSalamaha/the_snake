from random import randint
import pygame

"""Инициализация PyGame:"""
pygame.init()

"""Константы для размеров поля и сетки:"""
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

"""Направления движения:"""
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

"""Цвет фона - черный:"""
BOARD_BACKGROUND_COLOR = (0, 0, 0)

"""Цвет границы ячейки"""
BORDER_COLOR = (93, 216, 228)

"""Цвет яблока"""
APPLE_COLOR = (255, 0, 0)

"""Цвет змейки"""
SNAKE_COLOR = (0, 255, 0)

"""Скорость движения змейки
уменьшила так как удобнее было тестировать"""
SPEED = 10

"""Настройка игрового окна:"""
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

"""Заголовок окна игрового поля:"""
pygame.display.set_caption('Змейка')

"""Настройка времени:"""
clock = pygame.time.Clock()


class GameObject:
    """Экран"""

    def __init__(self, body_color=APPLE_COLOR) -> None:

        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = body_color

    """заглушка"""
    def draw(self):
        """заглушка"""
        pass


class Apple(GameObject):
    """Яблоко"""

    def __init__(self, body_color=APPLE_COLOR) -> None:
        super().__init__(body_color)
        self.position = self.randomize_position([])

    """Рандомная позиция появления яблока"""
    def randomize_position(self, snake_positions):
        """Рандомная позиция появления яблока"""
        apple_new_position = (
            randint(0, GRID_WIDTH) * GRID_SIZE - GRID_SIZE,
            randint(0, GRID_HEIGHT) * GRID_SIZE - GRID_SIZE,
        )
        """проверка на появлении на змее"""
        if apple_new_position in snake_positions:
            return self.randomize_position(snake_positions)
        return apple_new_position

    def draw(self):
        """Отрисовывает объект на экране."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Змея"""

    def __init__(self, body_color=SNAKE_COLOR) -> None:
        super().__init__(body_color)
        self.length = 1
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None
        self.reset()

    def get_head_position(self):
        """первый элемент змеи(голова)"""
        return self.positions[0]

    """Метод обновления направления после нажатия на кнопку"""
    def update_direction(self):
        """Метод обновления направления после нажатия на кнопку"""
        if self.next_direction:
            self.direction = self.next_direction

    def reset(self):
        """обновление змейки"""
        self.length = 1
        self.positions = [self.position]
        self.next_direction = None

    def draw(self):
        """отрисовка"""
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        """ Отрисовка головы змейки"""
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        """Затирание последнего сегмента"""
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def move(self):
        """Обновляет змеи"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

        cur_head = self.get_head_position()
        x, y = self.direction
        new_head = ((cur_head[0] + (x * GRID_SIZE)) % SCREEN_WIDTH,
                    (cur_head[1] + (y * GRID_SIZE)) % SCREEN_HEIGHT)

        if len(self.positions) > 2 and new_head in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new_head)
            if len(self.positions) > self.length:
                self.positions.pop()


def handle_keys(game_object):
    """Обработка нажитий на клавиши"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main() -> None:
    """основная функция"""
    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)

        handle_keys(snake)
        snake.move()

        if snake.get_head_position() == apple.position:
            """змея съела яблоко"""
            snake.length += 1
            apple.position = apple.randomize_position(snake.positions)

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()

        pygame.display.update()


if __name__ == '__main__':
    main()
