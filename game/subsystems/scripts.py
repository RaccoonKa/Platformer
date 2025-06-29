from __future__ import annotations

import pygame.time

from game.engine.script_system import Script
from game.engine.objects import MovingObject
from game.engine.render import Camera, ActivityManager


class MarioChaseScript(Script):
    def __init__(self, chase_object : MovingObject, target : MovingObject) -> None:
        super().__init__(enabled= True)
        self.chase_object : MovingObject = chase_object
        self.target : MovingObject = target

    def start(self) -> None:
        self.enabled = True
        print("Марио вышел на охоту")

    def stop(self) -> None:
        self.enabled = False

    def update(self, dt) -> None:
        c1 = self.chase_object.get_centre()
        c2 = self.target.get_centre()
        dx = c2[0]-c1[0]
        dy = c2[1]-c1[1]
        if (dx**2 + dy**2)**0.5 < 100:
            print("Догнал и устал")
            self.stop()
            return

        if self.chase_object.is_grounded:
            if self.chase_object.is_grounded:
                if abs(dy) > abs(dx) and abs(dx) < 200:
                    self.chase_object.velocity_y = -self.chase_object.max_speed_y
                    self.chase_object.is_grounded = False

                self.chase_object.velocity_x = dx
        else:
            if dx>0:
                self.chase_object.velocity_x += 0.005*self.chase_object.max_speed_x
            if dx<0:
                self.chase_object.velocity_x +=-  0.005*self.chase_object.max_speed_x

        if self.chase_object.velocity_x > self.chase_object.max_speed_x:
            self.chase_object.velocity_x = self.chase_object.max_speed_x
        elif self.chase_object.velocity_x < - self.chase_object.max_speed_x:
            self.chase_object.velocity_x = - self.chase_object.max_speed_x


class Patrol(Script):
    def __init__(self, obj: MovingObject, points: list[tuple[float, float]],
                 speed_x: float = 100.0, speed_y: float = -1, cyclic: bool = True,
                 teleport : bool = False, reach_distance: float = 5.0) -> None:
        super().__init__(enabled= True)
        self.obj = obj
        self.points = points
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.cyclic = cyclic
        self.teleport = teleport
        self.arrival_threshold = reach_distance

        self.current_point_index = 0
        self.is_moving = True

    def start(self) -> None:
        self.enabled = True
        if self.points and self.teleport:
            self.obj.x, self.obj.y = self.points[0]
        print(f"Patrol started with {len(self.points)} points")

    def stop(self) -> None:
        self.enabled = False
        self.obj.velocity_x = 0
        self.obj.velocity_y = 0

    def update(self, dt: float) -> None:
        if not self.enabled or not self.is_moving or not self.points or not self.obj.is_active:
            return

        current_target = self.points[self.current_point_index]
        obj_pos = (self.obj.x, self.obj.y)

        dx = current_target[0] - obj_pos[0]
        dy = current_target[1] - obj_pos[1]

        x_reached = self.speed_x == -1 or abs(dx) <= self.arrival_threshold
        y_reached = self.speed_y == -1 or abs(dy) <= self.arrival_threshold

        if x_reached and y_reached:
            if self.speed_x != -1:
                self.obj.x = current_target[0]
            if self.speed_y != -1:
                self.obj.y = current_target[1]
            self.next_point()
            return

        direction_x = 0
        direction_y = 0
        distance = (dx ** 2 + dy ** 2) ** 0.5

        if distance > 0:
            direction_x = dx / distance
            direction_y = dy / distance

        if self.speed_x != -1:
            self.obj.velocity_x = direction_x * self.speed_x

        if self.speed_y != -1:
            self.obj.velocity_y = direction_y * self.speed_y

    def next_point(self) -> None:
        self.current_point_index += 1

        if self.current_point_index >= len(self.points):
            if self.cyclic:
                self.current_point_index = 0
            else:
                self.is_moving = False
                self.obj.velocity_x = 0
                self.obj.velocity_y = 0
                self.stop()

    def resume(self) -> None:
        self.is_moving = True

    def pause(self) -> None:
        self.is_moving = False

    def set_speed_x(self, speed: float) -> None:
        self.speed_x = speed

    def set_speed_y(self, speed: float) -> None:
        self.speed_y = speed

    def add_point(self, point: tuple[float, float]) -> None:
        self.points.append(point)

    def skip_to_point(self, index: int) -> None:
        if 0 <= index < len(self.points):
            self.current_point_index = index


class LogScript(Script):
    def __init__(self, camera : Camera, clock : pygame.time.Clock,  player : MovingObject, activity_manager : ActivityManager ,game_time : float = 0):
        super().__init__()
        self.camera = camera
        self.clock = clock
        self.player =player
        self.activity_manager = activity_manager

        self.game_time = game_time
        self.log_delay = 0

    def start(self) -> None:
        self.enabled = True
        print("LogScript start working")

    def stop(self) -> None:
        self.enabled = False

    def update(self, dt: float) -> None:
        self.game_time += dt
        self.log_delay += dt
        if self.log_delay > 5:
            print("активных объектов:", len(self.activity_manager.get_active_objects()))
            print(
                f"camera: {self.camera.x, self.camera.y}, player: {self.player.x, self.player.y}, fps: {self.clock.get_fps()}, frame_time: {dt}")
            print("game time:", self.game_time)
            self.log_delay = 0

'''
class Script(ABC):
    def __init__(self) -> None:
        self.enabled: bool = True

    @abstractmethod
    def start(self) -> None:
        self.enabled = True

    @abstractmethod
    def stop(self) -> None:
        self.enabled = False

    @abstractmethod
    def update(self, dt: float) -> None:
        pass
'''