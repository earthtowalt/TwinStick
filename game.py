# Twin Stick shooter zombie game 
# 
# most of the code for the gunner class was modeled after the tank from this git:
# https://github.com/Mekire/pygame-samples/blob/master/tank_turret/turret_gamepad.py

import pygame
import os, sys
import math, random, time

CAPTION = "TWIN STICK" 
SCREEN_SIZE = (800, 600)
BACKGROUND_COLOR = (50,50,50)
COLOR_KEY = (255, 0, 255) 
GUNNER_WIDTH,GUNNER_HEIGHT = 150,150
FEET_WIDTH,FEET_HEIGHT = 150,150

# character class
class Gunner(object):
	'''the character who moves around screen. comprised of a top and bottom half of sprites.'''
	def __init__(self, controller, location):
		'''location is (x,y) coord pair.'''
		# gunner and bullet speed 
		self.speed = 8
		self.bullet_speed = 14
		# setup controller
		self.controller = controller 
		self.id = controller.get_id()
		# setup location and angle variables
		self.location = list(location)
		self.gunner_angle=0
		self.feet_angle=0
		# initialize original_gunner and og_feet 
		self.original_gunner = SPRITE_SHEET.subsurface((0,0,GUNNER_WIDTH,GUNNER_HEIGHT))
		self.original_feet = SPRITE_SHEET.subsurface((300,0,FEET_WIDTH,FEET_HEIGHT))
		# create firereate clock 
		self.shot_delay = (1/4)
		self.last_shot = time.time()
		# render initial gunner 
		self.set_position()
		
		
	def set_position(self):
		'''Move the gunner into place using angle and location'''
		# create gunner and feet copy with correct rotation.
		self.gunner = pygame.transform.rotate(self.original_gunner, self.gunner_angle)
		self.feet = pygame.transform.rotate(self.original_feet, self.feet_angle)
		# position the sprites correctly
		self.gunner_rect = self.gunner.get_rect(center=self.location)
		self.feet_rect = self.feet.get_rect(center=self.location)
		
		
	def fire(self, objects, deadzone=0.1):
		'''calculate gunner_angle'''
		rightx,righty = self.controller.get_axis(3), -self.controller.get_axis(4)
		if abs(rightx) > deadzone or abs(righty) > deadzone:
			if rightx == 0.0: rightx += 0.0001
			self.gunner_angle = 45.0 -math.degrees(math.atan2(float(righty), float(rightx)))
			# if fire_limit:
			current_time = time.time()
			if current_time - self.last_shot > self.shot_delay:
				objects.add(Bullet(self.gunner_rect.center, self.gunner_angle, self.bullet_speed))
				self.last_shot = current_time
			
	def update_location(self, deadzone=0.1):
		'''caclulate location and feet_angle'''
		leftx,lefty = self.controller.get_axis(0), self.controller.get_axis(1)
		if abs(leftx) > deadzone or abs(lefty) > deadzone:
			# set the feet angle
			if leftx == 0.0: leftx += 0.0001
			self.feet_angle = 225.0 -math.degrees(math.atan2(float(lefty), float(leftx)))
			# set the new location
			self.location[0] += self.speed * leftx
			self.location[1] += self.speed * lefty 
			# constrain left and right
			if self.location[0] > SCREEN_SIZE[0]-(GUNNER_WIDTH/2):
				self.location[0] = SCREEN_SIZE[0]-(GUNNER_WIDTH/2)
			elif self.location[0] < (GUNNER_WIDTH/2):
				self.location[0] = (GUNNER_WIDTH/2)
			# constrain top and bottom
			if self.location[1] > SCREEN_SIZE[1]-(GUNNER_HEIGHT/2):
				self.location[1] = SCREEN_SIZE[1]-(GUNNER_HEIGHT/2)
			elif self.location[1] < (GUNNER_HEIGHT/2):
				self.location[1] = (GUNNER_HEIGHT/2)
				
	def get_event(self, event):
		'''catch and process gamepad events.'''
		'''
		# fire
		if event.type == pygame.JOYBUTTONDOWN:
			if event.joy == self.id and event.button == 5:	# FIXME set fire button 
				objects.add(Bullet(self.gunner_rect.center, self.gunner_angle, self.bullet_speed))
		'''
		pass
	
	def draw(self, surface):
		'''draw gunner and feet to the target surface'''
		surface.blit(self.feet, self.feet_rect)
		surface.blit(self.gunner, self.gunner_rect)

class Bullet(pygame.sprite.Sprite):
	'''a class for the bullet sprites.'''
	def __init__(self, location, angle, speed):
		'''
		takes in a coordinate pair and angle in degrees. 
		These are passed in by the gunner class when the projectile is created
		'''
		pygame.sprite.Sprite.__init__(self)
		self.original_bullet = SPRITE_SHEET.subsurface((150,0,150,150)) # FIXME bullet from sprite image
		self.angle = -math.radians(angle-135)
		self.image = pygame.transform.rotate(self.original_bullet, angle)
		self.rect = self.image.get_rect(center=location)
		self.pos = [self.rect.x, self.rect.y]
		self.speed = speed
		self.velocity = (self.speed * math.cos(self.angle), self.speed * math.sin(self.angle))
		self.done = False 
	
	def update(self, screen_rect):
		'''update the bullet each frame'''
		self.pos[0] += self.velocity[0]
		self.pos[1] += self.velocity[1]
		self.rect.topleft = self.pos 
		self.remove(screen_rect)
		
	def remove(self, screen_rect):
		'''remove the bullet if it has left the screen'''
		if not self.rect.colliderect(screen_rect):
			self.kill()
	
class Control(object):
	'''main control class'''
	def __init__(self):
		'''create a gunner and create a group for bullets '''
		#init screen 
		self.screen = pygame.display.get_surface()
		self.screen_rect = self.screen.get_rect()
		# game fps and loop condiiton
		self.done = False
		self.clock = pygame.time.Clock()
		self.fps = 30
		self.keys = pygame.key.get_pressed()
		# setup joystick, if no joysticks found, initializes player with joy=None 
		self.joys = initialize_all_gamepads()
		if len(self.joys) == 0: joy = None 
		else: joy = self.joys[0]
		self.player = Gunner(joy, self.screen_rect.center)
		# sprite groups
		self.bullets = pygame.sprite.Group()
		self.zombies = pygame.sprite.Group()
		
	def event_loop(self):
		''' events are passed to appropriate object'''
		for event in pygame.event.get():
			self.keys = pygame.key.get_pressed()
			if event.type == pygame.QUIT or self.keys[pygame.K_ESCAPE]:
				self.done = True 
			self.player.get_event(event) #FIXME CHECK THIS
			
	def update(self):
		'''update all bullets, and the player motion'''
		self.player.update_location()
		self.player.fire(self.bullets)
		self.player.set_position()
		self.bullets.update(self.screen_rect)
		
	def draw(self):
		'''draw all elements to the display surface'''
		self.screen.fill(BACKGROUND_COLOR)
		self.player.draw(self.screen)
		self.bullets.draw(self.screen)
		
	def display_fps(self):
		'''show the program's FPS in the window handle'''
		caption = '{} - FPS: {:.2f}'.format(CAPTION, self.clock.get_fps())
		pygame.display.set_caption(caption)
		
	def main_loop(self):
		'''main loop'''
		while not self.done:
			self.event_loop()
			self.update()
			self.draw()
			pygame.display.flip()
			self.clock.tick(self.fps)
			self.display_fps()
			
			
class Zombie(pygame.sprite.Sprite):
	'''a class for the zombie sprites.'''
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.original_zombie = ZOMBIE_SPRITE.subsurface(()) # figure out
		self.angle = 0 # get angle
		#self.image = 
		self.location = [self.rect.x, self.rect.y]
		self.speed = 5
		self.done = False 
	
	def update(self, player):
		self.zombie = pygame.transform.rotate(self.original_zombie, self.angle)
		self.zombie_rect = self.zombie.get_rect(center=self.location)
		
	'''
	pygame.sprite.Sprite.__init__(self)
		self.original_bullet = SPRITE_SHEET.subsurface((150,0,150,150)) # FIXME bullet from sprite image
		self.angle = -math.radians(angle-135)
		self.image = pygame.transform.rotate(self.original_bullet, angle)
		self.rect = self.image.get_rect(center=location)
		self.pos = [self.rect.x, self.rect.y]
		self.speed = speed
		self.velocity = (self.speed * math.cos(self.angle), self.speed * math.sin(self.angle))
		self.done = False 
	'''



def get_spawn_location(): # fixme optimize
	boundary = 20
	
	x_range = random.randint(0, SCREEN_SIZE[0])
	y_range = random.randint(0, SCREEN_SIZE[1])
	# Top, Right, Bottom, Left
	coord_pairs = [(x_range, -boundary), (SCREEN_SIZE[0] + boundary, y_range), (x_range, SCREEN_SIZE[1] + boundary), (-boundary, y_range)]
	return list(coord_pairs[random.randint(0, 3)])
	
			
def initialize_all_gamepads():
	'''checks for gamepads and returns an intialized list of them if found'''
	joysticks = []
	for joy_id in range(pygame.joystick.get_count()):
		joysticks.append(pygame.joystick.Joystick(joy_id))
		joysticks[joy_id].init()
	return joysticks

	
def main():
	'''prepare display, load sprite image, and start program'''
	global SPRITE_SHEET 
	os.environ['SDL_VIDEO_CENTERED'] = '1'
	# pygame window setup 
	pygame.init()
	pygame.display.set_caption(CAPTION)
	pygame.display.set_mode(SCREEN_SIZE)
	# load sprite images
	dir_path = os.path.dirname(os.path.realpath(__file__))
	SPRITE_SHEET = pygame.image.load(dir_path + '\\sprite_sheet.png').convert()
	SPRITE_SHEET.set_colorkey(COLOR_KEY)
	ZOMBIE_SPRITE = pygame.image.load(dir_path + '\\assets\\zombiebasic.png').convert()
	
	
	Control().main_loop()
	pygame.quit()
	sys.exit()

if __name__ == '__main__':
	main()
	

	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
