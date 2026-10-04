import pygame
import random
from pygame import *
from time import sleep


# КОНСТАНТЫ (все настройки в одном месте, чтобы легко менять)
WIN_WIDTH = 1024  # Ширина игрового окна
WIN_HEIGHT = 720  # Высота игрового окна
GAME_FPS = 60  # Количество кадров в секунду
DELAY_MS = 1000 // GAME_FPS  # Задержка между кадрами в миллисекундах

# Параметры врагов
ENEMY_SHOOT_MIN = 30  # Минимальная задержка между выстрелами врага (в кадрах)
ENEMY_SHOOT_MAX = 100  # Максимальная задержка между выстрелами врага (в кадрах)
ENEMY_SPEED = 4  # Скорость движения врагов
ENEMY_BULLET_SPEED = 6  # Скорость пуль врагов
ENEMIES_NUMBER = 5  # Количество врагов

# Параметры игрока
PLAYER_SPEED = 10  # Скорость движения игрока
BULLET_SPEED = 10  # Скорость пуль игрока

# СОЗДАНИЕ ОКНА
pygame.init()  # Запускаем все системы Pygame (графика, звук, события)
pygame.mixer.init()  # Запускаем звуковую подсистему отдельно (для надёжности)
display.set_caption('Space Wars')  # Устанавливаем заголовок окна
window = display.set_mode((WIN_WIDTH, WIN_HEIGHT))  # Создаём игровое окно нужного размера

# ФОНОВАЯ КАРТИНКА
background = transform.scale(  # Загружаем и масштабируем фон под размер окна
    pygame.image.load('all_sprites/mback3.jpg'),  # Путь к файлу
    (WIN_WIDTH, WIN_HEIGHT)  # Новый размер
)


# КЛАССЫ СПРАЙТОВ (все игровые объекты)
class GameSprite(sprite.Sprite):
    """Родительский класс для всех игровых объектов (игрок, враги, пули)"""
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)  # Обязательный вызов конструктора родителя
        self.image = transform.scale(  # Загружаем картинку и меняем её размер
            image.load(player_image),  # Загружаем изображение
            (size_x, size_y)  # Новый размер
        )
        self.rect = self.image.get_rect()  # Получаем прямоугольник-хитбокс (границы объекта)
        self.rect.x = player_x  # Устанавливаем начальную координату X
        self.rect.y = player_y  # Устанавливаем начальную координату Y
        self.speed = player_speed  # Запоминаем скорость объекта

    def reset(self):
        """Отрисовывает объект в текущей позиции"""
        window.blit(self.image, (self.rect.x, self.rect.y))


class Explosion(sprite.Sprite):
    """Эффект взрыва (появляется при столкновении и исчезает через несколько кадров)"""
    def __init__(self, x, y, image_path):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(
            image.load(image_path),  # Загружаем картинку взрыва
            (260, 260)  # Делаем её большой, чтобы было заметно
        )
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)  # Центрируем взрыв в точке столкновения
        self.lifetime = 15  # Сколько кадров взрыв будет виден

    def update(self):
        """Обновление состояния взрыва (уменьшаем время жизни)"""
        self.lifetime -= 1  # Уменьшаем счётчик на 1 кадр
        if self.lifetime <= 0:  # Если время вышло
            self.kill()  # Удаляем спрайт из всех групп


class Bullet(GameSprite):
    """Пуля (летит вверх или вниз, зависит от direction)"""
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed, direction=-1):
        super().__init__(player_image, player_x, player_y, size_x, size_y, player_speed)  # Вызываем конструктор родителя
        self.direction = direction  # -1 = вверх, 1 = вниз

    def update(self):
        """Движение пули"""
        self.rect.y += self.speed * self.direction  # Смещаем пулю по Y в заданном направлении
        if self.rect.y < 0 or self.rect.y > WIN_HEIGHT:  # Если вылетела за экран
            self.kill()  # Удаляем пулю


class Player(GameSprite):
    """Игрок (управляется клавишами WASD)"""
    def move(self):
        """Обработка движения игрока"""
        keys = key.get_pressed()  # Получаем состояние всех клавиш (нажата/не нажата)
        if keys[K_a]:  # Если нажата A
            self.rect.x -= self.speed  # Движение влево
        if keys[K_d]:  # Если нажата D
            self.rect.x += self.speed  # Движение вправо
        if keys[K_w]:  # Если нажата W
            self.rect.y -= self.speed  # Движение вверх
        if keys[K_s]:  # Если нажата S
            self.rect.y += self.speed  # Движение вниз

        # Границы (чтобы игрок не вылетел за экран)
        if self.rect.right > WIN_WIDTH:  # Если правая граница вышла за экран
            self.rect.right = WIN_WIDTH  # Останавливаем у правого края
        if self.rect.left < 0:  # Если левая граница вышла за экран
            self.rect.left = 0  # Останавливаем у левого края
        if self.rect.bottom > WIN_HEIGHT:  # Если нижняя граница вышла за экран
            self.rect.bottom = WIN_HEIGHT  # Останавливаем у нижнего края
        if self.rect.top < 0:  # Если верхняя граница вышла за экран
            self.rect.top = 0  # Останавливаем у верхнего края

    def fire(self):
        """Выстрел (две пули — из правого и левого крыла)"""
        bullets.add(Bullet('all_sprites/bullet.png', self.rect.right - 20, self.rect.top, 15, 20, BULLET_SPEED))  # Пуля из правого крыла
        bullets.add(Bullet('all_sprites/bullet.png', self.rect.left, self.rect.top, 15, 20, BULLET_SPEED))  # Пуля из левого крыла
        fire_sound.play()  # Звук выстрела


class Enemy(GameSprite):
    """Враг (двигается влево-вправо и стреляет в случайные моменты)"""
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__(player_image, player_x, player_y, size_x, size_y, player_speed)  # Вызов конструктора родителя
        self.direction = 'right'  # Начальное направление движения
        self.shoot_timer = 0  # Счётчик кадров для определения момента выстрела
        self.shoot_delay = random.randint(ENEMY_SHOOT_MIN, ENEMY_SHOOT_MAX)  # Случайная задержка между выстрелами
        self.bullet_speed = ENEMY_BULLET_SPEED  # Скорость пули врага

    def fire(self):
        """Выстрел врага (пуля летит вниз)"""
        enemy_bullet = Bullet(
            'all_sprites/bullet_enemy.png',  # Картинка пули врага
            self.rect.centerx - 10,  # Центрируем по оси X
            self.rect.bottom,  # Появляется снизу врага
            25, 35,  # Размеры пули
            self.bullet_speed,  # Скорость
            2  # Направление вниз (положительное число)
        )
        enemy_bullets.add(enemy_bullet)  # Добавляем в группу вражеских пуль

    def update(self):
        """Обновление состояния врага (движение + стрельба)"""
        # Движение (ходим влево-вправо, отталкиваясь от стен)
        if self.rect.x < 0:  # Если упёрлись в левый край
            self.direction = 'right'  # Разворачиваемся направо
        if self.rect.x > WIN_WIDTH - 80:  # Если упёрлись в правый край (с учётом ширины корабля)
            self.direction = 'left'  # Разворачиваемся налево

        if self.direction == 'right':  # Если направление вправо
            self.rect.x += self.speed  # Двигаемся вправо
        else:  # Если направление влево
            self.rect.x -= self.speed  # Двигаемся влево

        # Стрельба (каждый кадр увеличиваем счётчик)
        self.shoot_timer += 1  # Увеличиваем счётчик на 1
        if self.shoot_timer >= self.shoot_delay:  # Если достигли задержки
            self.shoot_timer = 0  # Сбрасываем счётчик
            self.fire()  # Стреляем
            enemy_fire.play()  # Звук выстрела врага


# СОЗДАНИЕ ОБЪЕКТОВ И ГРУПП
ship = Player('all_sprites/ship3.png', 512, 610, 80, 80, PLAYER_SPEED)  # Создаём игрока

bullets = pygame.sprite.Group()  # Группа для пуль игрока
effects = pygame.sprite.Group()  # Группа для взрывов
enemy_bullets = pygame.sprite.Group()  # Группа для пуль врагов
enemies = pygame.sprite.Group()  # Группа для врагов

for i in range(ENEMIES_NUMBER):  # Создаём 5 врагов в ряд
    x = 50 + i * 200  # Расстояние между врагами 200 пикселей
    enemy = Enemy('all_sprites/ship_enemy.png', x, 10, 80, 80, ENEMY_SPEED)  # Создаём врага
    enemies.add(enemy)  # Добавляем в группу

# ЗВУКИ (загружаем все звуковые эффекты)
fire_sound = pygame.mixer.Sound('sounds/fire.wav')  # Выстрел игрока
boom_sound = pygame.mixer.Sound('sounds/boom.wav')  # Взрыв врага
ship_boom = pygame.mixer.Sound('sounds/ship_boom.wav')  # Взрыв игрока
enemy_fire = pygame.mixer.Sound('sounds/enemy_fire.wav')  # Выстрел врага
winner = pygame.mixer.Sound('sounds/winner.wav')  # Победа
# game_over = pygame.mixer.Sound('sounds/game_over.wav')  # Поражение


# ГЛАВНЫЙ ЦИКЛ (игровой процесс)
run = True  # Флаг, отвечающий за работу цикла (True = игра запущена)
while run:  # Пока игра запущена
    for e in event.get():  # Обрабатываем все события (нажатия клавиш, клики, закрытие окна)
        if e.type == QUIT:  # Если нажали крестик
            run = False  # Завершаем игру

        # Столкновение игрока с врагом (игрок умирает)
        hit_enemies = sprite.spritecollide(ship, enemies, False)  # Проверяем, столкнулся ли игрок с врагами
        if hit_enemies:  # Если столкнулся
            for enemy in hit_enemies:  # Перебираем всех врагов, с которыми столкнулись
                explosion = Explosion(enemy.rect.centerx, enemy.rect.centery, 'all_sprites/boom.png')  # Взрыв на месте врага
                effects.add(explosion)  # Добавляем взрыв в группу эффектов
                ship_boom.play()  # Звук взрыва игрока
            # game_over.play()  # Звук поражения
            run = False  # Игра окончена

        # Победа (если врагов не осталось)
        if len(enemies) == 0:  # Если в группе врагов 0 объектов
            print("Победа! Все враги уничтожены.")  # Выводим в консоль
            winner.play()  # Звук победы
            run = False  # Игра окончена

        # Выстрел игрока по клику левой кнопкой мыши
        if e.type == MOUSEBUTTONDOWN and e.button == 1:  # Если нажата левая кнопка мыши
            ship.fire()  # Стреляем

    # ОБНОВЛЕНИЕ И ОТРИСОВКА (каждый кадр)
    window.blit(background, (0, 0))  # Рисуем фон в координатах (0, 0)

    # Столкновение пуль игрока с врагами (пуля и враг уничтожаются)
    for enemy in sprite.groupcollide(enemies, bullets, True, True):  # True = удалять врага, True = удалять пулю
        explosion = Explosion(enemy.rect.centerx, enemy.rect.centery, 'all_sprites/boom.png')  # Взрыв на месте врага
        effects.add(explosion)  # Добавляем взрыв
        boom_sound.play()  # Звук взрыва врага

    # Попадание вражеской пули в игрока (игрок умирает)
    if sprite.spritecollide(ship, enemy_bullets, True):  # Если вражеская пуля попала в корабль
        explosion = Explosion(ship.rect.centerx, ship.rect.centery, 'all_sprites/boom.png')  # Взрыв на месте игрока
        effects.add(explosion)  # Добавляем взрыв
        ship_boom.play()  # Звук взрыва игрока
        # game_over.play()  # Звук поражения
        run = False  # Игра окончена

    # Обновление и отрисовка всех групп (пули, игрок, враги, эффекты)
    bullets.update()  # Обновляем состояние всех пуль игрока
    bullets.draw(window)  # Рисуем все пули игрока

    ship.reset()  # Отрисовываем игрока
    ship.move()  # Обрабатываем движение игрока

    enemies.update()  # Обновляем состояние врагов (движение + стрельба)
    enemies.draw(window)  # Рисуем всех врагов

    enemy_bullets.update()  # Обновляем все пули врагов
    enemy_bullets.draw(window)  # Рисуем все пули враговвввввв

    effects.update()  # Обновляем все эффекты (уменьшаем время жизни взрывов)
    effects.draw(window)  # Рисуем все эффекты

    display.update()  # Обновляем экран (отображаем все изменения)
    pygame.time.delay(DELAY_MS)  # Задержка, чтобы игра работала с постоянной скоростью

sleep(2.6)  # Ждём 2.6 секунды перед закрытием окна