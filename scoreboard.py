import pygame.font

class Scoreboard():
	"""Класс для вывода игровой информации."""

	def __init__(self, ai_game):
		"""Инициализируются атрибуты подсчета очков."""
		self.screen = ai_game.screen
		self.screen_rect = self.screen.get_rect()
		self.settings = ai_game.settings
		self.stats = ai_game.stats

		# Настройка шрифта для вывода счета.
		self.text_color = (30, 30, 30)
		self.font = pygame.font.SysFont(None, 38)

		# Подготовка изображений счетов.
		self.prep_score()
		self.prep_high_score()
		#self.prep_level()


	def prep_score(self):
		"""преобразует текущий счет в графическое изображение."""
		rounded_score = round(self.stats.score, -1)
		score_str1 = "{:,}".format(rounded_score) # str(self.stats.score)

		score_str= f"Life: {self.stats.ships_left} Level: {self.stats.level} Score: {score_str1}"
		self.score_image = self.font.render(score_str, True, 
				self.text_color, self.settings.bg_color)

		# Вывод счета в правой верхней части экрана.
		self.score_rect = self.score_image.get_rect()
		self.score_rect.right = self.screen_rect.right - 20
		self.score_rect.top = 20

	def prep_high_score(self):
		"""Преобразует рекордный счет в графическое изображение."""
		high_score = round(self.stats.high_score, -1)
		aux = "{:,}".format(high_score)
		high_score_str = f"Record score is: {aux}"
		self.high_score_image = self.font.render(high_score_str, True, 
						self.text_color, self.settings.bg_color)

		# Рекорд выравнивается по центру верхней стороны.
		self.high_score_rect = self.high_score_image.get_rect()
		self.high_score_rect.centerx = self.screen_rect.centerx
		self.high_score_rect.top = self.score_rect.top

	def show_score(self):
		"""выводит счет на экран."""
		self.screen.blit(self.score_image, self.score_rect)
		self.screen.blit(self.high_score_image, self.high_score_rect)

	def check_high_score(self):
		"""Проверяет, появился ли новый рекорд."""
		if self.stats.score > self.stats.high_score:
			self.stats.high_score = self.stats.score
			self.prep_high_score()

	#def prep_level(self):


