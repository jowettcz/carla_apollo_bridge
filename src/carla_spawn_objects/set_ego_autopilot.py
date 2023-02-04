
import carla

print("enter into set autopilot...")
client = carla.Client("172.17.0.1", 2000)
client.set_timeout(30.0)
world = client.get_world()
print("get world done")
# ego_vehicle = world.get_actor(197)
ego_vehicle = world.get_actor(211)
print("get ego vehicle done")
ego_vehicle.set_autopilot(True)
print("set autopilot done")