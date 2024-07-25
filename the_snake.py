from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE


# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject():
    """Общий класс игровых объектов."""

    # Метод __init__ с атрибутами экземпляров.
    def __init__(self):
        # Позиция объекта, изначально по центру.
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        # Цвет объекта, изначально не определен.
        self.body_color = None
    # Пустой метод draw, используемый в наследуемых классах.
    def draw():
        pass


# Класс яблока, наследуемый от общего класса.
class Apple(GameObject):
    # Метод для перемещения яблока на рандомную позицию.
    def randomize_position(self):
        rand_position = (self.random_numbers_for_position(SCREEN_WIDTH - 20), self.random_numbers_for_position(SCREEN_HEIGHT - 20))
        return rand_position
    
    # Метод __init__ с атрибутами яблока.
    def __init__(self):
        # Наследование атрибутов из родительского класса.
        super().__init__()
        # Цвет яблока - красный.
        self.body_color = APPLE_COLOR
    
    # Метод draw, теперь отрисовывающий яблоко.
    def draw(self):
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    # Метод для генерирования рандомной позиция яблока.
    def random_numbers_for_position(self, number):
        r = randint(0, number)
        if r % 20 == 0:
            return r
        else:
            return self.random_numbers_for_position(number)

# Класс змейки, наследуемый от общего класса.
class Snake(GameObject):
    # Метод __init__ с атрибутами змейки.
    def __init__(self):
        # Наследование атрибутов из родительского класса.
        super().__init__()
        # Максимальная длина змейки.
        self.length = 1
        # Cписок позиций змейки.
        self.positions = [self.position]
        # Направление движения змейки.
        self.direction = RIGHT
        # Следующее направление движения змейки.
        self.next_direction = None
        # Цвет змейки - зеленый.
        self.body_color = SNAKE_COLOR
        # Последний элемент змейки.
        self.last = None
        # Атрибут-переключатель, отвечающий за удаление последнего элемента.
        self.last_position_delete = True


    # Метод draw класса Snake.
    def draw(self):
        # Последний элемент змейки.
        self.last = self.positions[-1]
        # Отрисовка всех элементов змейки, кроме головы.
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки.
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last_position_delete == True:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


    # Метод обновления направления после нажатия на кнопку.
    def update_direction(self):
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None


    # Метод обновления положения змейки.
    def move(self):
        # Позиция головы змейки.
        current_head_position = self.get_head_position() 
        # Разложение позиции на координаты x и y.
        x, y = current_head_position
        # Если направление движения - вверх, то двигаемся по оси у на один сегмент выше.
        if self.direction == UP:
            # Проверка достижения верхней границы.
            y += GRID_SIZE 
            if y > SCREEN_HEIGHT:
                # Перемещение на противоположный край.
                y = y - SCREEN_HEIGHT
            # Проверка столкновения с яблоком (если произошло столкновение, то последний элемент не затирается).
            if len(self.positions) > self.length:
                self.positions.pop(-1)
            
        # Если направление движения - вниз, то двигаемся по оси у на один сегмент ниже.
        elif self.direction == DOWN:
            y -= GRID_SIZE 
            # Проверка достижения нижней границы.
            if y < 0:
                # Перемещение на противоположный край.
                y = SCREEN_HEIGHT - y
            # Проверка столкновения с яблоком (если произошло столкновение, то последний элемент не затирается).
            if len(self.positions) > self.length:
                self.positions.pop(-1)
            
        # Если направление движения - влево, то двигаемся по оси х на один сегмент левее.
        elif self.direction == LEFT:
            x -= GRID_SIZE 
            # Проверка достижения левой границы.
            if x < 0:
                # Перемещение на противоположный край.
                x = SCREEN_WIDTH - x
            # Проверка столкновения с яблоком (если произошло столкновение, то последний элемент не затирается).
            if len(self.positions) > self.length:
                self.positions.pop(-1)
            
        # Если направление движения - вправо, то двигаемся по оси х на один сегмент правее.  
        elif self.direction == RIGHT:
            x += GRID_SIZE 
            # Проверка достижения правой границы.
            if x > SCREEN_WIDTH:
                # Перемещение на противоположный край.
                x = x - SCREEN_WIDTH
            # Проверка столкновения с яблоком (если произошло столкновение, то последний элемент не затирается).
            if len(self.positions) > self.length:
                self.positions.pop(-1)

        # Составление позиции головы из координат х и у.
        current_head_position = x, y
        # Проверка столкновения змейки с самой собой.
        for position in self.positions:
            if current_head_position == position:
                self.reset()
        # Добавление головы в начало списка сегментов.
        self.positions.insert(0, current_head_position)


    # Метод получения позиции головы.
    def get_head_position(self):
        return self.positions[0]
    

    # Метод сброса.
    def reset(self):
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        screen.fill(BOARD_BACKGROUND_COLOR)


# Функция обработки действий пользователя.
def handle_keys(game_object):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_UP and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT

  
# Основной цикл игры.
def main():
    # Инициализация PyGame:
    pygame.init()
    # Экземпляры классов.
    apple = Apple()
    snake =  Snake()
    while True:
        # Основная логика игры.
        snake.last_position_delete = True
        clock.tick(SPEED)
        handle_keys(snake)

        # Отрисовка экземпляров классов.
        apple.draw()
        snake.draw()
        # Обновление направления змейки.
        snake.update_direction()
        # Движение змейки.
        snake.move()
            
        # Проверка столкновения с яблоком.
        if snake.get_head_position() == apple.position:
            snake.length += 1
            # Если произошло столкновение, то длина змейки не уменьшается.
            snake.last_position_delete = False
            apple.position = apple.randomize_position()
        # Отображение на экране.
        pygame.display.update()
        

if __name__ == '__main__':
    main()
