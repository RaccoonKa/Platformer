from __future__ import annotations
from typing import Set
from game.engine.objects import GameObject, StaticObject, MovingObject, Hitbox
from game.engine.render import ActivityManager


class PhysicEngine:
    def __init__(self, fps : float, g : float = 9.8*16):
        self.static_objects : list[StaticObject] = []
        self.unstoppable_objects : list[MovingObject] = []
        self.stoppable_objects: list[MovingObject] = []
        self.fps = fps
        self.g = g

    @property
    def fps(self) -> float:
        return self._fps

    @fps.setter
    def fps(self, value : float) -> None:
        if value == 0:
            value +=0.001
        self._fps = value

    def add_static_object(self, obj : StaticObject) -> None:
        if obj not in self.static_objects:
            if not obj.hitbox:
                obj.generate_hitbox()
            self.static_objects.append(obj)

    def add_unstoppable_object(self, obj : MovingObject) -> None:
        if obj not in self.unstoppable_objects:
            if not obj.hitbox:
                obj.generate_hitbox()
            self.unstoppable_objects.append(obj)

    def add_stoppable_object(self, obj : MovingObject) -> None:
        if obj not in self.stoppable_objects:
            if not obj.hitbox:
                obj.generate_hitbox()
            self.stoppable_objects.append(obj)

    def update_velocity(self,dt : float, active_objects: Set[GameObject]) -> None:
        for obj in self.unstoppable_objects + self.stoppable_objects:
            if obj not in active_objects:
                continue
            if obj.is_gravitate:
                obj.velocity_y += dt * self.g
                if abs(obj.velocity_y) > obj.max_speed_y:
                    obj.velocity_y = obj.max_speed_y if obj.velocity_y > 0 else -obj.max_speed_y

    def move_objects(self, dt : float, active_objects: Set[GameObject]) -> None:
        for obj in self.unstoppable_objects + self.stoppable_objects:
            if obj not in active_objects:
                continue

            dx = obj.velocity_x * dt
            dy = obj.velocity_y * dt

            obj.x += dx
            obj.y += dy

            obj.hitbox.x += dx
            obj.hitbox.y += dy
            if obj.is_grounded:
                obj.velocity_x *= (1 - obj.ground_friction_x * dt)
            else:
                obj.velocity_x *= (1 - obj.air_friction_x * dt)
                obj.velocity_y *= (1 - obj.air_friction_y * dt)


    @staticmethod
    def collide_detect(hb1: Hitbox, hb2: Hitbox) -> bool:
        if not hb1 or not hb2:
            return False

        return (hb1.x < hb2.x + hb2.size[0] and
                hb1.x + hb1.size[0] > hb2.x and
                hb1.y < hb2.y + hb2.size[1] and
                hb1.y + hb1.size[1] > hb2.y)

    def process_collisions(self, old_positions: dict[MovingObject: tuple[float,float,float,float]], active_objects: Set[GameObject]) -> None:
        active_static = [obj for obj in self.static_objects if obj in active_objects]
        active_unstoppable = [obj for obj in self.unstoppable_objects if obj in active_objects]
        active_stoppable = [obj for obj in self.stoppable_objects if obj in active_objects]

        for obj1 in active_stoppable:
            obj1.is_grounded = False
            for obj2 in active_static:
                PhysicEngine.collide_stop_to_stat(obj1, obj2)
            for obj2 in active_unstoppable:
                PhysicEngine.collide_stop_to_unstop(obj1,obj2,old_positions)
            for obj2 in active_stoppable:
                PhysicEngine.collide_stop_to_stop(obj1, obj2)

    @staticmethod
    def collide_stop_to_stat(obj1: MovingObject, obj2: StaticObject)  -> None:
        if not PhysicEngine.collide_detect(obj1.hitbox, obj2.hitbox):
            return

        overlaps = {
            'left': obj2.hitbox.x + obj2.hitbox.size[0] - obj1.hitbox.x,
            'right': obj1.hitbox.x + obj1.hitbox.size[0] - obj2.hitbox.x,
            'top': obj2.hitbox.y + obj2.hitbox.size[1] - obj1.hitbox.y,
            'bottom': obj1.hitbox.y + obj1.hitbox.size[1] - obj2.hitbox.y
        }

        positive_overlaps = {k: v for k, v in overlaps.items() if v > 0}
        if not positive_overlaps:
            return

        min_key = min(positive_overlaps, key=positive_overlaps.get)

        if min_key == 'left':  # Столкновение справа
            obj1.x = obj2.hitbox.x + obj2.hitbox.size[0]
            obj1.velocity_x = max(obj1.velocity_x, 0)
        elif min_key == 'right':  # Столкновение слева
            obj1.x = obj2.hitbox.x - obj1.hitbox.size[0]
            obj1.velocity_x = min(obj1.velocity_x, 0)  # Гасим движение вправо
        elif min_key == 'top':  # Столкновение снизу
            obj1.y = obj2.hitbox.y + obj2.hitbox.size[1]
            obj1.velocity_y = max(obj1.velocity_y, 0)  # Гасим движение вверх
        elif min_key == 'bottom':  # Столкновение сверху
            obj1.y = obj2.hitbox.y - obj1.hitbox.size[1]
            obj1.velocity_y = min(obj1.velocity_y, 0)  # Останавливаем падение
            obj1.is_grounded = True

        obj1.hitbox.x = obj1.x
        obj1.hitbox.y = obj1.y


    @staticmethod
    def collide_stop_to_unstop(obj1: MovingObject, obj2: MovingObject, old_positions : dict[MovingObject: tuple[float,float,float,float]]) -> None:
        if not PhysicEngine.collide_detect(obj1.hitbox, obj2.hitbox):
            return

        overlaps = {
            'left': obj2.hitbox.x + obj2.hitbox.size[0] - obj1.hitbox.x,
            'right': obj1.hitbox.x + obj1.hitbox.size[0] - obj2.hitbox.x,
            'top': obj2.hitbox.y + obj2.hitbox.size[1] - obj1.hitbox.y,
            'bottom': obj1.hitbox.y + obj1.hitbox.size[1] - obj2.hitbox.y
        }

        positive_overlaps = {k: v for k, v in overlaps.items() if v > 0}
        if not positive_overlaps:
            return

        min_key = min(positive_overlaps, key=positive_overlaps.get)
        #min_overlap = positive_overlaps[min_key]

        if min_key == 'left':  # obj1 справа от obj2
            obj1.x = obj2.hitbox.x + obj2.hitbox.size[0]
            obj1.velocity_x = max(obj1.velocity_x, 0)
        elif min_key == 'right':  # obj1 слева от obj2
            obj1.x = obj2.hitbox.x - obj1.hitbox.size[0]
            obj1.velocity_x = min(obj1.velocity_x, 0)
        elif min_key == 'top':  # obj1 под obj2
            obj1.y = obj2.hitbox.y + obj2.hitbox.size[1]
            obj1.velocity_y = max(obj1.velocity_y, 0)
        elif min_key == 'bottom':  # obj1 над obj2
            obj1.y = obj2.hitbox.y - obj1.hitbox.size[1]
            obj1.velocity_y = min(obj1.velocity_y, 0)
            obj1.is_grounded = True

            # Если obj2 двигался, перемещаем игрока вместе с ним
            if obj2 in old_positions:
                old_x, old_y, old_hb_x, old_hb_y = old_positions[obj2]
                dx = obj2.x - old_x
                obj1.x += dx

        obj1.hitbox.x = obj1.x
        obj1.hitbox.y = obj1.y


    @staticmethod
    def collide_stop_to_stop(obj1: MovingObject, obj2: MovingObject) -> None:
        if obj1 == obj2:
            return

        if not PhysicEngine.collide_detect(obj1.hitbox, obj2.hitbox):
            return

        overlaps = {
            'left': obj2.hitbox.x + obj2.hitbox.size[0] - obj1.hitbox.x,
            'right': obj1.hitbox.x + obj1.hitbox.size[0] - obj2.hitbox.x,
            'top': obj2.hitbox.y + obj2.hitbox.size[1] - obj1.hitbox.y,
            'bottom': obj1.hitbox.y + obj1.hitbox.size[1] - obj2.hitbox.y
        }

        positive_overlaps = {k: v for k, v in overlaps.items() if v > 0}
        if not positive_overlaps:
            return

        min_key = min(positive_overlaps, key=positive_overlaps.get)
        overlap = positive_overlaps[min_key]

        if min_key == 'left' or min_key == 'right':
            if min_key == 'left': # obj1 справа от obj2
                push = overlap / 2
                obj1.x += push
                obj2.x -= push
            else: # obj1 слева от obj2
                push = overlap / 2
                obj1.x -= push
                obj2.x += push

            # Обмен импульсами по X
            total_vx = obj1.velocity_x + obj2.velocity_x
            obj1.velocity_x = total_vx - obj1.velocity_x
            obj2.velocity_x = total_vx - obj2.velocity_x

        else:
            # Вертикальное столкновение
            if min_key == 'top': # obj1 под obj2
                push = overlap / 2
                obj1.y += push
                obj2.y -= push
            else: # obj1 над obj2
                push = overlap / 2
                obj1.y -= push
                obj2.y += push

            # Обмен импульсами по Y
            total_vy = obj1.velocity_y + obj2.velocity_y
            obj1.velocity_y = total_vy - obj1.velocity_y
            obj2.velocity_y = total_vy - obj2.velocity_y

            # Проверка приземления
            if min_key == 'bottom':
                obj1.is_grounded = True
            elif min_key == 'top':
                obj2.is_grounded = True

        obj1.hitbox.x = obj1.x
        obj1.hitbox.y = obj1.y
        obj2.hitbox.x = obj2.x
        obj2.hitbox.y = obj2.y


    def update(self, dt : float, activity_manager: ActivityManager) -> None:
        if dt == 0:
            return

        active_objects = activity_manager.get_active_objects()
        old_positions = {}

        for obj in self.unstoppable_objects + self.stoppable_objects:
            if obj not in active_objects:
                continue
            old_positions[obj] = (obj.x, obj.y, obj.hitbox.x, obj.hitbox.y)

        self.update_velocity(dt, active_objects)

        self.move_objects(dt, active_objects)

        self.process_collisions(old_positions, active_objects)