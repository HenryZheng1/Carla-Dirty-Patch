import carla   
import math
import numpy as np
from PIL import Image
import time

client = carla.Client('localhost', 2000)
client.set_timeout(10.0) # seconds

world = client.get_world()
blueprint_library = world.get_blueprint_library()
world_map = world.get_map()



vehicle_bp = blueprint_library.filter('vehicle.tesla.*')[1]
spawn_points = world_map.get_spawn_points()
spawn_point = spawn_points[16] # y -= 100+
spawn_point.location.y   -= 80

#=====add 1st vehicle=====
spawn_point1 = carla.Transform(spawn_point.location,spawn_point.rotation)
spawn_point1.location.y   += 25
vehicle = world.spawn_actor(vehicle_bp, spawn_point1)

#=====add second vehicle=====
spawn_point2 = carla.Transform(spawn_point.location,spawn_point.rotation)
spawn_point2.location.y   += 100
vehicle2 = world.spawn_actor(vehicle_bp, spawn_point2)
# vehicle2.set_autopilot(True)


spectator = world.get_spectator()
transform = vehicle.get_transform()

W, H = 1164, 874

blueprint = blueprint_library.find('sensor.camera.rgb')
blueprint.set_attribute('image_size_x', str(W))
blueprint.set_attribute('image_size_y', str(H))
blueprint.set_attribute('fov', '70')
blueprint.set_attribute('sensor_tick', '0.05')
#blueprint.set_attribute('enable_postprocess_effects', "False")
spawn_point3 = carla.Transform(spawn_point.location,carla.Rotation(pitch=-90))

spawn_point3.location.y += 35
spawn_point3.location.z += 5

#camera = world.spawn_actor(blueprint, transform, attach_to=vehicle)

spectator.set_transform(spawn_point3)

camera = world.spawn_actor(blueprint, spawn_point3)



camera.listen(lambda image: image.save_to_disk('Images/pallet.png'))

time.sleep(5.0)



