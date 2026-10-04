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
    """Игрок (пока просто стоит на месте)"""
    pass


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

    display.update()  # Обновляем экран (отображаем все изменения)
    pygame.time.delay(DELAY_MS)  # Задержка, чтобы игра работала с постоянной скоростью