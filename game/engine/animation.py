import pygame
from game.engine.objects import StaticObject
from game.engine.render import ActivityManager

class AnimationContainer:
    def __init__(self):
        self.cycled : bool = False
        self.current_animation : list[pygame.Surface] = list()
        self.current_id : int = 0
        self.current_delay : float = 0
        self.animation_delay : float = 0
        self.all_anims : dict[str, dict[str,float | list[pygame.Surface]]] = dict()


class AnimationEngine:
    def __init__(self):
        self.containers : dict[StaticObject, AnimationContainer] = dict()
        self.updatable_objects : list[StaticObject] = list()

    def add_object(self, obj : StaticObject) -> None:
        container = AnimationContainer()
        container.all_anims['normal'] = {'delay' : 0 , 'list' : obj.sprite}
        container.current_animation = [obj.sprite]
        self.containers[obj] = container

    def remove_object(self, obj : StaticObject):
        self.containers.pop(obj)
        if obj in self.updatable_objects:
            self.updatable_objects.remove(obj)

    def add_anim(self, obj : StaticObject, animation_name : str, anim_delay : float, anim_list : list[pygame.Surface]) -> None:
        if obj not in self.containers.keys():
            self.add_object(obj)

        container = self.containers[obj]
        container.all_anims[animation_name] = {'delay' : anim_delay, 'list' : anim_list}

    def switch_anim(self,obj : StaticObject, animation_name : str, play_now : bool = False, cycle : bool = True, to_normal : bool = False):
        if animation_name not in self.containers[obj].all_anims:
            raise ValueError(f"Animation {animation_name} not found")
        container = self.containers[obj]
        container.current_animation = container.all_anims[animation_name]['list']
        container.animation_delay = container.all_anims[animation_name]['delay']
        container.cycled = False
        container.current_id = -1
        container.current_delay = 0
        if to_normal:#Костыльненько, но окей
            obj.sprite = container.current_animation
            return

        if play_now:
            self.turn_on(obj, cycle=cycle)
        elif obj in self.updatable_objects:
            self.updatable_objects.remove(obj)


    def turn_on(self, obj : StaticObject, cycle : bool = True) -> None:
        if obj not in self.updatable_objects:
            self.updatable_objects.append(obj)

        self.containers[obj].cycled = cycle

    def turn_off(self, obj : StaticObject)-> None:
        if obj in self.updatable_objects:
            self.updatable_objects.remove(obj)

        self.switch_anim(obj,'normal', to_normal=True)


    def update(self, dt : float, activity_manager: ActivityManager):
        active_objects = activity_manager.get_active_objects()

        for obj in self.updatable_objects:
            if obj not in active_objects:
                continue
            container = self.containers[obj]
            container.current_delay += dt
            if container.current_id == -1:
                container.current_delay = 0
                container.current_id += 1
                obj.sprite = container.current_animation[container.current_id]
                continue
            if container.current_delay > container.animation_delay:
                container.current_id +=1
                if container.current_id > len(container.current_animation)-1:
                    if not container.cycled:
                        self.turn_off(obj)
                        continue
                    else:
                        container.current_id = 0
                        obj.sprite = container.current_animation[container.current_id]
                        container.current_delay = 0
                else:
                    obj.sprite = container.current_animation[container.current_id]
                    container.current_delay = 0



