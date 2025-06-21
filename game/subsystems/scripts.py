from __future__ import annotations

from game.engine.script_system import Script
from game.engine.objects import MovingObject, Hitbox


class MarioChaseScript(Script):
    def __init__(self, chase_object : MovingObject, target : MovingObject):
        super().__init__()
        self.enabled = True
        self.chase_object : MovingObject = chase_object
        self.target : MovingObject = target

    def start(self):
        print("Марио вышел на охоту")

    def update(self, dt) -> None:
        c1 = self.chase_object.get_centre()
        c2 = self.target.get_centre()
        dx = c2[0]-c1[0]
        dy = c2[1]-c1[1]
        if (dx**2 + dy**2)**0.5 < 100:
            print("Догнал и устал")
            self.destroy()
            return
        if self.chase_object.is_grounded:
            if self.chase_object.is_grounded:
                if abs(dy) > abs(dx):
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




    def destroy(self) -> None:
        self.enabled = False

'''
class Script(ABC):
    def __init__(self):
        self.enabled: bool = True

    @abstractmethod
    def start(self) -> None:
        pass

    @abstractmethod
    def update(self, dt: float) -> None:
        pass

    @abstractmethod
    def destroy(self) -> None:
        self.enabled = False
'''