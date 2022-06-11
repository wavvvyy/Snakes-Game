import os
import random
import time
import pygame
x=pygame.init()
pygame.mixer.init()

#colors - RGB Values
white = (255,255,255)
lime = (155, 235, 52)
fadedlime = (207, 247, 119)
dgreen = (61, 102, 9)
yellow = (252, 252, 50)
black = (0, 0, 0)

swidth = 412
sheight	= 844
gameWindow=pygame.display.set_mode((swidth, sheight))
pygame.display.set_caption("Snakes")

mainmenu = pygame.image.load("mainmenu.jpg")
mainmenu = pygame.transform.scale(mainmenu, (swidth, sheight)).convert_alpha()

snakelogoig = pygame.image.load("snakes1.png")
snakelogoig = pygame.transform.scale(snakelogoig, (swidth, sheight)).convert_alpha()

paused = pygame.image.load("paused.jpg")
paused = pygame.transform.scale(paused, (swidth, sheight)).convert_alpha()

g_over = pygame.image.load("dead.jpg")
g_over = pygame.transform.scale(g_over, (swidth, sheight)).convert_alpha()

snake_food = pygame.image.load("foodsnek.png")
snake_food = pygame.transform.scale(snake_food, (20, 20)).convert_alpha()

clock = pygame.time.Clock()
font = pygame.font.SysFont('Adamsky SF', 40)

def play_mello():	
	pygame.mixer.stop()
	mello = pygame.mixer.Sound("mell-nova.mp3")
	pygame.mixer.Sound.play(mello)
	pygame.mixer.Sound.set_volume(mello,0.1)

def food_eaten():
	ding = pygame.mixer.Sound("ding.mp3")
	pygame.mixer.Sound.play(ding)
	pygame.mixer.Sound.set_volume(ding,0.2)

def snake_dies():
	dead = pygame.mixer.Sound("dead.mp3")
	pygame.mixer.Sound.play(dead)
	pygame.mixer.Sound.set_volume(dead,0.2)


def text_screen(text, color, x, y):
	screen_text = font.render(text, True, color)
	gameWindow.blit(screen_text, [x,y])

def draw_snake(gameWindow, color, snake_list, snake_size):
	for x,y in snake_list:
		pygame.draw.rect(gameWindow, dgreen, [x, y, snake_size, snake_size])

def gameloop(): #gameloop - Keeps the events in the game running
	play_mello()

	#Game specific variables
	exitgame = False
	gameover = False
	gamepaused = False
	gamestart = True


	fps = 60
	score = 0
	food_sens=15

	snake_x = 206
	snake_y = 422
	snake_size = 15
	snake_list = []
	snake_len = 1

	Vx = 0
	Vy = 0
	vel_variable = 5

	food_x = random.randint(30,370)
	food_y = random.randint(210,670)
	food_size = 15

	if (not os.path.exists('Highscore.txt')):
		with open('Highscore.txt','w') as f:
			f.write('0')

	with open('Highscore.txt','r') as f:
		highscore = f.read()
		highscore=int(highscore)


	while not exitgame:

		while gamestart:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					quit()

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_RETURN:
						gamestart = False
			
			gameWindow.fill(lime)
			gameWindow.blit(mainmenu,(0,0))
			pygame.display.update()
			clock.tick(fps)


		while gamepaused:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					quit()

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE and gamepaused == True:
						gamepaused= False
				


			gameWindow.fill(lime)
			gameWindow.blit(paused,(0,0))
			pygame.display.update()
			clock.tick(fps)
			

		if gameover:
			gameWindow.fill(lime)
			gameWindow.blit(g_over,(0,0))

			for event in pygame.event.get():
				if event.type == pygame.QUIT: exitgame=True

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_RETURN:
						gameloop()
		else:
			for event in pygame.event.get():
				if event.type == pygame.QUIT: exitgame=True

				if event.type == pygame.KEYDOWN:

					if event.key == pygame.K_DOWN or event.key == pygame.K_s:
						Vy=0
						Vy+=vel_variable
						Vx=0
					elif event.key == pygame.K_UP or event.key == pygame.K_w:
						Vy=0
						Vy-=vel_variable
						Vx=0
					elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
						Vx=0
						Vx+=vel_variable
						Vy=0
					elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
						Vx=0
						Vx-=vel_variable
						Vy=0
					elif event.key == pygame.K_ESCAPE and gamepaused == False:
						gamepaused = True

			snake_x+= Vx
			snake_y+= Vy

			if abs(snake_x - food_x) < food_sens and abs(snake_y - food_y) < food_sens:
				food_eaten()
				score+=1
				food_x = random.randint(30,370)
				food_y = random.randint(210,670)
				snake_len+=5

			if highscore < score:
				highscore = score
				with open('Highscore.txt','w') as f:
					f.write(str(highscore))


			gameWindow.fill(lime)
			gameWindow.blit(snakelogoig,(0,0))
			pygame.draw.rect(gameWindow, fadedlime, [20, 200, 372, 500])
			text_screen("Score: " + str(score), white, 140, 150)
			text_screen("Highscore: " + str(highscore), white, 90, 700)
			gameWindow.blit(snake_food,(food_x,food_y))
			#pygame.draw.rect(gameWindow, yellow, , , food_size, food_size])

			head = []
			head.append(snake_x)
			head.append(snake_y)
			snake_list.append(head)

			if len(snake_list)>snake_len:
				del snake_list[0]

			
			if head in snake_list[:-1]:
				Vx=0
				Vy=0
				snake_dies()
				time.sleep(1)
				gameover = True

			if snake_x < 20 or snake_y < 198 or snake_y > 686 or snake_x > 380:
				Vx=0
				Vy=0
				snake_dies()
				time.sleep(1)
				gameover = True
			draw_snake(gameWindow, black, snake_list, snake_size)
		
		pygame.display.update()
		clock.tick(fps)

	pygame.quit()
	quit()

gameloop()