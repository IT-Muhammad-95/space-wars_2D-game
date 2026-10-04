import pygame
from pygame import *


# КОНСТАНТЫ (все настройки в одном месте, чтобы легко менять)
WIN_WIDTH = 1024  # Ширина игрового окна
WIN_HEIGHT = 720  # Высота игрового окна
GAME_FPS = 60  # Количество кадров в секунду
DELAY_MS = 1000 // GAME_FPS  # Задержка между кадрами в миллисекундах

# Параметры игрока
PLAYER_SPEED = 10  # Скорость движения игрока

# СОЗДАНИЕ ОКНА
pygame.init()  # Запускаем все системы Pygame (графика, звук, события)
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


# СОЗДАНИЕ ОБЪЕКТОВ И ГРУПП
ship = Player('all_sprites/ship3.png', 512, 610, 80, 80, PLAYER_SPEED)  # Создаём игрока


# ГЛАВНЫЙ ЦИКЛ (игровой процесс)
run = True  # Флаг, отвечающий за работу цикла (True = игра запущена)
while run:  # Пока игра запущена
    for e in event.get():  # Обрабатываем все события (нажатия клавиш, клики, закрытие окна)
        if e.type == QUIT:  # Если нажали крестик
            run = False  # Завершаем игру

    # ОБНОВЛЕНИЕ И ОТРИСОВКА (каждый кадр)
    window.blit(background, (0, 0))  # Рисуем фон в координатах (0, 0)
    ship.reset()  # Отрисовываем игрока
    ship.move()  # Обрабатываем движение игрока

    display.update()  # Обновляем экран (отображаем все изменения)
    pygame.time.delay(DELAY_MS)  # Задержка, чтобы игра работала с постоянной скоростью