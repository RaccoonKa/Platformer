from game.menu_classes.menu_objects import InteractiveObject
from game.menu_things.special_effects import CoffeeEffect


def setup_secrets(objects_manager, GAME_WIDTH, GAME_HEIGHT):
    coffee_effect = CoffeeEffect(GAME_WIDTH, GAME_HEIGHT)
    secrets = [
        InteractiveObject(
            x = GAME_WIDTH // 1.2 + 10,
            y = GAME_HEIGHT // 2.5,
            shape = "rect",
            width = 250,
            height = 400,
            sound_path = "assets/audio/menu/secrets/coon.mp3"
        ),
        InteractiveObject(
            x = GAME_WIDTH // 2.17,
            y = GAME_HEIGHT // 1.22,
            shape = "rect",
            width = 515,
            height = 120,
            angle = 9,
            sound_path = "assets/audio/menu/secrets/keyboard.mp3"
        ),
        InteractiveObject(
            x = GAME_WIDTH // 1.618,
            y = GAME_HEIGHT // 1.38,
            shape = "rect",
            width = 100,
            height = 50,
            angle = 312,
            sound_path = "assets/audio/menu/secrets/mouse.wav"
        ),
        InteractiveObject(
            x = GAME_WIDTH // 1.1 + 55,
            y = GAME_HEIGHT // 1.1 - 60,
            shape = "rect",
            width = 150,
            height = 150,
            angle = 293,
            sound_path = "assets/audio/menu/secrets/floppy_disk.mp3"
        ),
        InteractiveObject(
            x = GAME_WIDTH // 2.9,
            y = GAME_HEIGHT // 1.51,
            shape = "rect",
            width = 140,
            height = 65,
            angle = 35,
            sound_path = "assets/audio/menu/secrets/phone.mp3"
        ),
        InteractiveObject(
            x = GAME_WIDTH // 4.65,
            y = GAME_HEIGHT // 2.5,
            shape = "rect",
            width = 250,
            height = 180,
            angle = 90,
            sound_path = "assets/audio/menu/secrets/face.mp3"
        ),
        InteractiveObject(
            x = GAME_WIDTH // 1.07,
            y = GAME_HEIGHT // 45,
            shape = "circle",
            width = 300,
            height = 250,
            sound_path = "assets/audio/menu/secrets/moon.mp3"
        ),
        InteractiveObject(
            x = GAME_WIDTH // 1 - 90,
            y = GAME_HEIGHT // 1.7 - 20,
            shape = "circle",
            width = 150,
            height = 150,
            sound_path = "assets/audio/menu/secrets/capybara.mp3"
        ),
        InteractiveObject(
            x = GAME_WIDTH // 6,
            y = GAME_HEIGHT // 1.36,
            shape = "rect",
            width = 180,
            height = 180,
            angle = 90,
            sound_path = "assets/audio/menu/secrets/coffee.mp3",
            effect = coffee_effect
        ),
        InteractiveObject(
            x = GAME_WIDTH // 13,
            y = GAME_HEIGHT // 1.27,
            shape = "rect",
            width = 100,
            height = 50,
            angle = 312,
            sound_path = "assets/audio/menu/secrets/candy.mp3"
        ),
        InteractiveObject(
            x = GAME_WIDTH // 1.38,
            y = GAME_HEIGHT // 1.1,
            shape = "rect",
            width = 570,
            height = 400,
            angle = 64,
            sound_path = "assets/audio/menu/secrets/chair.mp3"
        ),
        InteractiveObject(
            x = GAME_WIDTH // 1.25 + 10,
            y = GAME_HEIGHT // 1.5,
            shape = "rect",
            width = 380,
            height = 160,
            sound_path = "assets/audio/menu/secrets/chair.mp3"
        ),
        InteractiveObject(
            x = GAME_WIDTH // 13,
            y = GAME_HEIGHT // 1.6 + 10,
            shape = "circle",
            width = 180,
            height = 180,
            sound_path = "assets/audio/menu/secrets/donut.mp3"
        ),
        InteractiveObject(
            x = GAME_WIDTH // 8.5,
            y = GAME_HEIGHT // 2.4 + 15,
            shape = "rect",
            width = 130,
            height = 200,
            sound_path = "assets/audio/menu/secrets/flower.mp3"
        )
    ]

    special_sounds = {
        10: "assets/audio/menu/secrets/chair_falling.mp3",
        11: "assets/audio/menu/secrets/chair_falling.mp3"
    }

    for idx, obj in enumerate(secrets):
        objects_manager.add(obj)
        if idx in special_sounds:
            objects_manager.add_special(obj, special_sounds[idx])

    return coffee_effect
