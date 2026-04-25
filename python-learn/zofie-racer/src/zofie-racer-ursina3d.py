#!/usr/bin/env python3
import math

from ursina import Ursina, DirectionalLight, AmbientLight, Entity, Cylinder, Mesh, Vec3, color, copy, camera, time


class Meshes:
    @staticmethod
    def prism(base: list[tuple[float]], peak: tuple[float], add_base=False) -> Mesh:
        """
        Generates side triangles of an open prism.
        base: list of (x,y,z) tuples for base vertices
        peak: (x,y,z) tuple for the top vertex
        The base is NOT closed; you can handle base closure externally.
        """
        vertices = [Vec3(*v) for v in base]
        peak_vertex = Vec3(*peak)
        vertices.append(peak_vertex)
        peak_index = len(vertices) - 1

        triangles = []
        n = len(base)

        # Connect consecutive base vertices to the peak
        # Only i from 0..n-2, last edge is handled externally
        for i in range(n-1):
            triangles.append((i, i+1, peak_index))
        if add_base:
            for i in range(len(base) - 2):
                triangles.append((0, i + 2, i + 1))

        return Mesh(vertices=vertices, triangles=triangles, mode='triangle')


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
        #Entity(parent=self, model='cube', color=color.red, scale=(0.4, 0.2, 1.2), position=(0, 0, 2))
        Entity(parent=self, model=Meshes.prism(
            [
                (-0.2, 0.0, 1.5),
                (0, 0.15, 1.5),
                (0.2, 0.0, 1.5),
            ],
            (0, 0, 3),
            add_base=True
        ),
               color=color.green, position=(0, 0, 0)
               )
        # Top
        Entity(parent=self, model=Meshes.prism(
            [
                (0.5, 0.15, 0),
                (0, 0.45, 0),
                (-0.5, 0.15, 0),
            ],
            (0, 0.15, -1.5),
            add_base=True
        ),
               color=color.red, position=(0, 0, 0)
               )

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
