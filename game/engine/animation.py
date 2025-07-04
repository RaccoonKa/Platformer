import pygame
from game.engine.objects import StaticObject, HitboxParams
from game.engine.render import ActivityManager

class Animation:
    def __init__(self, frames : list[tuple[pygame.Surface, HitboxParams]], delay : float):
        self.frames : list[tuple[pygame.Surface, HitboxParams]] = frames
        self.delay : float = delay

class AnimationContainer:
    def __init__(self):
        self.cycled : bool = False
        self.current_animation : Animation | None = None
        self.current_frame : int = 0
        self.current_delay : float = 0
        self.all_animations : dict[str, Animation] = dict()


class AnimationEngine:
    def __init__(self):
        self.containers : dict[StaticObject, AnimationContainer] = dict()
        self.updatable_objects : list[StaticObject] = list()

    def add_object(self, obj : StaticObject) -> None:
        if obj in self.containers:
            return

        sprite = None
        if obj.sprite:
            sprite = obj.sprite

        hb_params = None
        if obj.hitbox:
            hb_params = HitboxParams(
                size = obj.hitbox.size,
                offset = obj.get_hitbox_offset()
            )

        container = AnimationContainer()
        container.all_animations['normal'] = Animation(frames = [(sprite, hb_params)], delay= -100)

        self.containers[obj] = container

        self.switch_anim(obj = obj, animation_name= 'normal')

    def remove_object(self, obj : StaticObject):
        self.containers.pop(obj)

    def add_anim(self, obj : StaticObject, animation_name : str, anim_delay : float, frames_list : list[tuple[pygame.Surface, HitboxParams]]) -> None:
        if not self.containers.get(obj):
            self.add_object(obj)

        container = self.containers[obj]

        container.all_animations[animation_name] = Animation(frames_list,anim_delay)

    def switch_anim(self, obj: StaticObject, animation_name: str, play_now: bool = False, cycle: bool = True):
        container = self.containers[obj]
        container.cycled = cycle
        container.current_animation = container.all_animations[animation_name]
        container.current_delay = 0
        container.current_frame = 0

        self.switch_frame(obj, container.current_animation.frames[0])

        if play_now or animation_name != 'normal':
            self.turn_on(obj, cycle)

    def turn_on(self, obj : StaticObject, cycle : bool = True) -> None:
        container = self.containers[obj]
        container.cycled = cycle
        container.current_delay = container.current_animation.delay

        if obj not in self.updatable_objects:
            self.updatable_objects.append(obj)

    def turn_off(self, obj : StaticObject)-> None:
        self.switch_anim(obj, 'normal', play_now = True)

    def update(self, dt: float, activity_manager: ActivityManager):
        obj_to_remove = []

        for obj in self.updatable_objects[:]:
            if obj not in activity_manager.active_objects:
                continue

            container = self.containers[obj]
            anim = container.current_animation

            if anim.delay < 0:
                if anim.delay == -100:
                    obj_to_remove.append(obj)
                continue

            container.current_delay += dt

            if container.current_delay >= anim.delay:
                container.current_delay = 0
                container.current_frame += 1

                if container.current_frame >= len(anim.frames):
                    if container.cycled:
                        container.current_frame = 0
                    else:
                        self.switch_anim(obj, 'normal', play_now=True)
                        continue

                self.switch_frame(obj, anim.frames[container.current_frame])

        for obj in obj_to_remove:
            if obj in self.updatable_objects:
                self.updatable_objects.remove(obj)

    @staticmethod
    def switch_frame(obj : StaticObject, frame : tuple[pygame.Surface,HitboxParams]):
        obj.sprite = frame[0]
        obj.size = frame[0].get_size()
        obj.set_hitbox_by_params(frame[1])
