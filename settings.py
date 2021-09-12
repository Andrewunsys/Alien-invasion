# import sys 

class Settings():
	"""Класс для хранения всех настроек игры Alien Invasion."""

	def __init__(self):
		"""Инициализирует настройки игры."""
		# Параметры экрана (размеры и цвет фона).

		self.screen_wight = 1280
		self.screen_height = 660

		# self.screen_wight = self.screen.get_rect().wight
		# self.screen_height = self.screen.get_rect().height 

		self.bg_color = (230, 230, 230) 

		# Настройки корабля.
		self.ship_speed = 1.5
		self.ship_limit = 3

		# Настройки снаряда.
		self.bullet_speed = 2
		self.bullet_wight = 5
		self.bullet_height = 15
		self.bullet_color = (60, 60, 60)
		self.bullets_allowed = 5

		# Настройки пришельцев.
		self.alien_speed = 1
		self.fleet_drop_speed = 10

		# Темп ускорения игры.
		self.speedup_scale = 1.1

		# Темп роста стоимости пришельца.
		self.score_scale = 1.5

		self.initialize_dynamic_settings()

	def initialize_dynamic_settings(self):
		"""Инициализирует настройки, изменяющиеся в ходе игры."""
		self.ship_speed = 1.5
		self.bullet_speed = 3.0
		self.alien_speed = 1.0

		# fleet_direction = 1 обозначание движение вправо, -1 - влево.
		self.fleet_direction = 1

		# Подсчет отков
		self.alien_points = 50

	def increase_speed(self):
		"""Увеличивает настройки скорости."""
		self.ship_speed *= self.speedup_scale
		self.bullet_speed *= self.speedup_scale
		self.alien_speed *= self.speedup_scale
		self.alien_points = int(self.alien_points * self.score_scale)	

