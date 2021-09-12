import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
	"""Класс для управления пришельцем (Одним)."""

	def __init__(self, ai_game):
		"""Инициализирует пришельца и задает его начальную позицию."""
		super().__init__()
		self.screen = ai_game.screen
		self.settings = ai_game.settings
			# self.screen_rect = ai_game.screen.get_rect()

		# Загружает изображение корабля и назначение атрибута rect.
		self.image = pygame.image.load('images/alien.bmp')
		self.rect = self.image.get_rect()

		# Каждый новый корабль появляется в левом верхнем углу экрана.
		self.rect.x = 58 # self.rect.wight
		self.rect.y = 58 # self.rect.height

		# Сохранение точной горизонтальной позиции пришельца.
		self.x = float(self.rect.x)

	def check_edges(self):
		"""Возвращает True, если пришелец находится у экрана."""
		screen_rect = self.screen.get_rect()
		if self.rect.right >= screen_rect.right or self.rect.left <=0:
			return True

	def update(self):
		"""Перемещает пришельца вправо или влево."""
		# # Обновляется атрибут x объекта ship, не rect.

		self.x += (self.settings.alien_speed * self.settings.fleet_direction)

		# Обновление атрибута rect на основе self.x.
		self.rect.x = self.x

# 	def blitme(self):
# 		"""Рисует корабль в текущей позиции."""
# 		self.screen.blit(self.image, self.rect)