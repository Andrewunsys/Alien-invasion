import json

class GameStats():
	"""Отслеживание статитстики для игры."""

	def __init__(self,ai_game):
		"""Инициализирует статистику."""
		self.settings = ai_game.settings
		self.reset_stats()

		# Игра запускается в неактивном состоянии.
		self.game_active = False

		# Рекорд не должен сбрасываться
		high_score_file_name = 'hs.json'
		try:
			with open(high_score_file_name) as f:
				high_score_from_file = int(json.load(f))
		except FileNotFoundError:
			high_score_from_file = 0
		self.high_score = high_score_from_file




	def reset_stats(self):
		"""Инициализирует статистику, изменяющуюся в ходе игры."""
		self.ships_left = self.settings.ship_limit
		self.score = 0
		self.level = 1
