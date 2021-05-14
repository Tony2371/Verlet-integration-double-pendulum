import pygame
import math

pygame.init()
resolution = (1280, 720)
screen = pygame.display.set_mode(resolution)
clock = pygame.time.Clock()

running = True

colors = {"blue": (0, 0, 225),
		  "red": (240, 10, 10),
		  "grey": (125, 125, 125),
		  "white": (255, 255, 255),
		  "green": (40, 240, 40)}

class Mesh(object):
	def __init__(self):
		self.radius = 10
		self.gravity = 0.5

		self.points = {
			"point_1": [resolution[0] / 2, 100, resolution[0] / 2, 100],
			"point_2": [350, 200, 345, 195],
			"point_3": [100, 300, 110, 305]
		}

	def move_points(self):
		for p in self.points:
			# CALCULATE VELOCITY
			vel_x = self.points[p][0] - self.points[p][2]
			vel_y = self.points[p][1] - self.points[p][3]

			# SET OLD POSITION TO CURRENT POSITION
			self.points[p][2] = self.points[p][0]
			self.points[p][3] = self.points[p][1]

			# ADDING VELOCITY TO CURRENT POSITION
			self.points[p][0] += vel_x
			self.points[p][1] += vel_y
			if p != "point_1":
				self.points[p][1] += self.gravity

	def calc_distances(self):
		# LOOP IS USED FOR STABILITY PURPOSE
		for i in range(5):
			dist_1 = 200
			dist_2 = 200

			diff_1 = dist_1 - math.sqrt((self.points["point_2"][0] - self.points["point_1"][0]) ** 2 + (
						self.points["point_2"][1] - self.points["point_1"][1]) ** 2)
			diff_2 = dist_2 - math.sqrt((self.points["point_3"][0] - self.points["point_2"][0]) ** 2 + (
						self.points["point_3"][1] - self.points["point_2"][1]) ** 2)

			percent_1 = diff_1/dist_1
			percent_2 = diff_2/dist_2

			offset_x_1 = (self.points["point_2"][0]-self.points["point_1"][0])*percent_1
			offset_y_1 = (self.points["point_2"][1]-self.points["point_1"][1])*percent_1
			offset_x_2 = (self.points["point_3"][0]-self.points["point_2"][0])*percent_2
			offset_y_2 = (self.points["point_3"][1]-self.points["point_2"][1])*percent_2

			self.points["point_2"][0] += offset_x_1
			self.points["point_2"][1] += offset_y_1
			self.points["point_3"][0] += offset_x_2
			self.points["point_3"][1] += offset_y_2


	def draw(self):
		for p in self.points:
			pygame.draw.circle(screen, colors["green"], (self.points[p][0], self.points[p][1]), self.radius)
		pygame.draw.line(screen, colors["white"], (self.points["point_1"][0], self.points["point_1"][1]), (self.points["point_2"][0], self.points["point_2"][1]))
		pygame.draw.line(screen, colors["white"], (self.points["point_3"][0], self.points["point_3"][1]),
						 (self.points["point_2"][0], self.points["point_2"][1]))

mesh = Mesh()

while running:
	for event in pygame.event.get():
		if event.type == "QUIT":
			running = False

	# MOVES SECOND POINT TO CURSOR'S LOCATION
	if pygame.mouse.get_pressed()[0]:
		mesh.points["point_2"][0] = pygame.mouse.get_pos()[0]
		mesh.points["point_2"][1] = pygame.mouse.get_pos()[1]

	screen.fill((25, 25, 25))

	mesh.move_points()
	mesh.calc_distances()

	mesh.draw()

	pygame.display.update()
	clock.tick(60)
