#!/usr/bin/env python3
import math

from ursina import Ursina, DirectionalLight, AmbientLight, Entity, Cylinder, color, copy, camera, time

app = Ursina()
DirectionalLight()
AmbientLight(color=color.rgba(100,100,100,0.5))

class RaceCar(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.make_car()
        self.rotation_y += 45

    def make_car(self):
        # Body
        Entity(parent=self, model='cube', color=color.orange, scale=(1, 0.3, 3))
        # Nose
        Entity(parent=self, model='cube', color=color.red, scale=(0.4, 0.2, 1.2), position=(0, 0, 2))
        # Rear wing
        Entity(parent=self, model='cube', color=color.black, scale=(1.2, 0.1, 0.3), position=(0, 0.35, -1.4))
        # Front wing
        Entity(parent=self, model='cube', color=color.black, scale=(1.4, 0.1, 0.3), position=(0, 0.15, 3))

        wheel_width = 0.4
        wheel_position = 0.7
        wheel_mesh = Cylinder(radius=0.3, height=wheel_width, resolution=32)
        axle_mesh = Cylinder(radius=0.05, height=wheel_position, resolution=32)
        def make_wheel(x, z):
            #Entity(parent=car, model='cube', color=color.black, scale=(0.4, 0.4, 0.4), position=(x, 0, z))
            wheel = Entity(
                parent=self,
                model=copy(wheel_mesh),
                color=color.black,
                position=(x, 0, z),
                rotation=(0,0,90),   # axle left-right
                origin=(0,0,0),
                scale=(1, math.copysign(1, x), 1)
            )
            Entity(parent=self,
                model=copy(axle_mesh),
                color=color.yellow,
                position=(0, 0, z),
                rotation=(0,0,90),   # axle left-right
                origin=(0,0,0),
                scale=(1, math.copysign(1, x), 1)
           )
            return wheel

        # Wheels
        self.wheels = []
        self.wheels.append(make_wheel(-wheel_position, 1.5))
        self.wheels.append(make_wheel(wheel_position, 1.5))
        self.wheels.append(make_wheel(-wheel_position, -1.5))
        self.wheels.append(make_wheel( wheel_position, -1.5))

    def update(self):
        self.rotation_y += 60 * time.dt
        for w in self.wheels:
            w.rotation_x += 600 * time.dt
            pass


car = RaceCar()


# Camera
camera.position = (0, 3, -8)
camera.look_at(car)

app.run()
