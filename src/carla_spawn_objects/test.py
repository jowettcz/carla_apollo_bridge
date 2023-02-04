import sys
import time
import carla
import glob
import os
import sys
import time
from carla import VehicleLightState as vls

import argparse
import logging
from numpy import random

def get_actor_blueprints(world, filter, generation):
    bps = world.get_blueprint_library().filter(filter)

    if generation.lower() == "all":
        return bps

    # If the filter returns only one bp, we assume that this one needed
    # and therefore, we ignore the generation
    if len(bps) == 1:
        return bps

    try:
        int_generation = int(generation)
        # Check if generation is in available generations
        if int_generation in [1, 2]:
            bps = [x for x in bps if int(x.get_attribute('generation')) == int_generation]
            return bps
        else:
            print("   Warning! Actor Generation is not valid. No actor will be spawned.")
            return []
    except:
        print("   Warning! Actor Generation is not valid. No actor will be spawned.")
        return []


client = carla.Client("172.17.0.1", 2000)
client.set_timeout(30.0)
world = client.get_world()

batch = []
walker_speed = []
for spawn_point in spawn_points:
    walker_bp = random.choice(blueprintsWalkers)
    # set as not invincible
    if walker_bp.has_attribute('is_invincible'):
        walker_bp.set_attribute('is_invincible', 'false')
    # set the max speed
    if walker_bp.has_attribute('speed'):
        if (random.random() > percentagePedestriansRunning):
            # walking
            walker_speed.append(walker_bp.get_attribute('speed').recommended_values[1])
        else:
            # running
            walker_speed.append(walker_bp.get_attribute('speed').recommended_values[2])
    else:
        print("Walker has no speed")
        walker_speed.append(0.0)
    batch.append(SpawnActor(walker_bp, spawn_point))
results = client.apply_batch_sync(batch, True)