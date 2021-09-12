import sys
import json

from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion():
	"""Класс управления ресурсами и поведения игры."""

	def __init__(self):
		"""Инициализирует игру и создает игровые ресурсы."""
		pygame.init()
		self.settings = Settings()

		self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
			#self.settings.screen_wight = self.screen.get_rect().wight    # - ???
			#self.settings.screen_height = self.screen.get_rect().height  # - ???
		pygame.display.set_caption("Alien Invasion")
		# Создание экземпляра для хранения числовой статистики 
		# и панели результатов
		self.stats = GameStats(self)
		self.sb = Scoreboard(self)
		self.ship = Ship(self)
		self.bullets = pygame.sprite.Group()
		self.aliens = pygame.sprite.Group()

		self._create_fleet()
		self.play_button = Button(self, "Play")
		self.laser_sound = pygame.mixer.Sound("sounds/sound_laser.wav")
		self.explosion_sound = pygame.mixer.Sound("sounds/sounds_explosion.wav")

	def run_game(self):
		"""Запуск основноо цикла игры."""
		while True:
			self._check_events()

			if self.stats.game_active:
				self.ship.update()
				self._update_bullet()
				self._update_aliens()
				self.sb.prep_score()

					
			self._update_screen()


	def _check_events(self):
		"""Обрабатывает нажатие клавиш и события мыши."""
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.exit_from_game() #sys.exit()
			elif event.type == pygame.KEYDOWN:
				self._chek_keydown_events(event)
			elif event.type == pygame.KEYUP:
				self._chek_keyup_events(event)
			elif event.type == pygame.MOUSEBUTTONDOWN:
				mouse_pos = pygame.mouse.get_pos()
				self._check_play_button(mouse_pos)

	def _check_play_button(self,mouse_pos):
		"""Запукает новую игру при нажатии кнопки Play."""
		button_clicked = self.play_button.rect.collidepoint(mouse_pos)
		if button_clicked and not self.stats.game_active:
			# Сброс игровых настроек
			self.settings.initialize_dynamic_settings()

			# Сброс игровой статистики.
			self.stats.reset_stats()
			self.stats.game_active = True
			self.sb.prep_score()

			# Очистка списка пришельцев и снарядов.
			self.aliens.empty()
			self.bullets.empty()

			# Создание нового флота и размещение корабля в центре.
			self._create_fleet()
			self.ship.center_ship()

			# Указатель мыши скрывается.
			pygame.mouse.set_visible(False)

	def _chek_keydown_events(self,event):
		"""Реагирует на нажатие клавиш."""
		if event.key == pygame.K_RIGHT:
			self.ship.moving_right = True
		elif event.key == pygame.K_LEFT:
			self.ship.moving_left = True
		elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
			self.exit_from_game() #sys.exit()
		elif event.key == pygame.K_SPACE:
			self._fire_bullet()

	def _chek_keyup_events(self,event):
		"""Реагирует на отпускание клавиш."""
		if event.key == pygame.K_RIGHT:
			self.ship.moving_right = False
		elif event.key == pygame.K_LEFT:
			self.ship.moving_left = False					

	def _fire_bullet(self):
		""" Создание нового снаряда и включение его в группу bullets."""
		if len(self.bullets)<self.settings.bullets_allowed:
			new_bullet = Bullet(self)
			self.bullets.add(new_bullet)
		# Звуки выстрелов лазером.
		pygame.mixer.Sound.play(self.laser_sound)
		pygame.mixer.music.stop()

	def _update_bullet(self):
		"""Обновляет позиции снарядов и уничтожает старых снарядов."""
		# Обновление позиций снарядов.
		self.bullets.update()
		# Удаление снарядов вышедших за край экрана.
		for bullet in self.bullets.copy():
			if bullet.rect.bottom <= 0:
				self.bullets.remove(bullet)

		self._check_bullet_alien_collisions()

	def _check_bullet_alien_collisions(self):
		"""Обработка коллизий снарядов с пришельцами."""
		# Удаление снарядов и пришельцев, участвующих в коллизиях.
		collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, 
			True, True)

		if collisions:
			for aliens in collisions.values():
				self.stats.score += self.settings.alien_points * len (aliens)
				# Звуки взрывов пришельцев.				
				pygame.mixer.Sound.play(self.explosion_sound)
				pygame.mixer.music.stop()

			self.sb.prep_score()
			self.sb.check_high_score()

		if not self.aliens:
			# Уничтожение существующих снарядов и создание нового флота.
			self.bullets.empty()
			self._create_fleet()
			self.settings.increase_speed()
			self.stats.level += 1

	def _create_fleet(self):
		"""Создание флота вторжения пришельцев."""
		# Создание пришельца и вычисление количества пришельцев в ряду.
		# Интервал между соседними пришельцами равен ширине пришельца.
		alien = Alien(self)
		alien_wight = 58 # ???
		alien_height = 58 # ???
		available_space_x = self.settings.screen_wight - (2 * alien_wight)
		number_aliens_x = available_space_x // (2 * alien_wight) 

		# Определяет количество рядов, помещающихся на экране.
		ship_height = self.ship.rect.height
		available_space_y = (self.settings.screen_height - 
								(3 * alien_height) - ship_height)
		number_rows = available_space_y // (2 * alien_height)

		# Создание первого ряда пришельцев.
		for row_number in range(number_rows):
			for alien_number in range(number_aliens_x):
				self._create_alien(alien_number,row_number)

	def _create_alien(self, alien_number, row_number):
		"""Создание пришельца и размещения его в ряду."""
		alien = Alien(self)
		alien_wight = 58 # ???
		alien_height = 58 # ???
		alien.x = alien_wight + 2 * alien_wight * alien_number
		alien.rect.x = alien.x
		alien.rect.y = alien_height = 2 * alien_height * row_number
		self.aliens.add(alien)	

	def _update_aliens(self):
		"""Обновляет позиции всех пришельцев во флоте."""
		self._check_fleet_edges()
		self.aliens.update()
		# Кроверка коллизий "Пришелец - Корабль".
		if pygame.sprite.spritecollideany(self.ship, self.aliens):
			self._ship_hit()

		# Проверить добрались ли пришельцы до нижнего края экрана.
		self._check_aliens_bottom()

	def _check_aliens_bottom(self):
		"""Прроверяет, добрались ли пришельцы до нижнего края экрана."""
		screen_rect = self.screen.get_rect()
		for alien in self.aliens.sprites():
			if alien.rect.bottom >= screen_rect.bottom:
				# Происходить то же, что и при столкновении с кораблем.
				self._ship_hit()
				break

	def _check_fleet_edges(self):
		"""Реагирует на достижение пришельцем края экрана."""
		for alien in self.aliens.sprites():
			if alien.check_edges():
				self._change_fleet_direction()
				break

	def _change_fleet_direction(self):
		"""Опускает весь флот и меняет направление движения флота."""
		for alien in self.aliens.sprites():
			alien.rect.y += self.settings.fleet_drop_speed
		self.settings.fleet_direction *= -1

	def _ship_hit(self):
		"""Обрабатывает столкновения корабля с пришельцем."""
		
		if self.stats.ships_left > 0:
			# Уменьшение ships_left.
			self.stats.ships_left -= 1

			# Очистка списка пришельцев и снарядов.
			self.aliens.empty()
			self.bullets.empty()

			# Создание флота и размещение корабля в центре.
			self._create_fleet()
			self.ship.center_ship()	

			# Пауза.
			sleep(0.99)			
		else:
			self.stats.game_active = False
			pygame.mouse.set_visible(True)
		

	def _update_screen(self):
		"""Обновляет изображения на экране и отображает новый экран."""
		self.screen.fill(self.settings.bg_color)
		self.ship.blitme()
		for bullet in self.bullets.sprites():
			bullet.draw_bullet()
		self.aliens.draw(self.screen)
		
		# Вывод информации о счете
		self.sb.show_score()


		# Кнопка Play отображается в том случае, если игра неактивна.
		if not self.stats.game_active:
			self.play_button.draw_button()

		pygame.display.flip()

	def exit_from_game(self):
		"""Выход из игры с предварительным сохранением рекордного счета."""
		high_score_file_name = 'hs.json'
		with open(high_score_file_name,'w') as f:
			json.dump(self.stats.high_score, f)				
		sys.exit()

if __name__ == '__main__':
	# Создание экземпляоа и запуска игры.
	ai = AlienInvasion()
	ai.run_game()






