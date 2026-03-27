from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

window.size = (1200, 620)

player = FirstPersonController()
Sky(texture='sky_default')

boxes = []
paused = False

# --------------------
# Pause Menu
# --------------------
pause_menu = Entity(enabled=False)

Text('Game Paused', parent=pause_menu, origin=(0, 0), y=0.1, scale=2)

Button(
    text='Resume',
    parent=pause_menu,
    y=0,
    scale=(0.2, 0.1),
    on_click=lambda: toggle_pause()
)

Button(
    text='Quit',
    parent=pause_menu,
    y=-0.15,
    scale=(0.2, 0.1),
    on_click=application.quit
)

# --------------------
# Functions
# --------------------
def toggle_pause():
    global paused
    paused = not paused

    pause_menu.enabled = paused
    player.enabled = not paused
    mouse.locked = not paused
    mouse.visible = paused

def toggle_fullscreen():
    window.fullscreen = not window.fullscreen

# --------------------
# ONE input function ONLY
# --------------------
def input(key):
    if key == 'escape':
        toggle_pause()

    if key == 'f11':
        toggle_fullscreen()

    if not paused:
        if mouse.hovered_entity:
            if key == 'left mouse down':
                new_box = Button(
                    color=color.white,
                    model='cube',
                    texture='white_cube',
                    position=mouse.hovered_entity.position + mouse.normal,
                    parent=scene,
                    origin_y=0.5
                )
                boxes.append(new_box)

            elif key == 'right mouse down':
                destroy(mouse.hovered_entity)
                if mouse.hovered_entity in boxes:
                    boxes.remove(mouse.hovered_entity)

# --------------------
# Ground
# --------------------
for x in range(20):
    for z in range(20):
        box = Button(
            color=color.white,
            model='cube',
            texture='white_cube',
            position=(x, 0, z),
            parent=scene,
            origin_y=0.5
        )
        boxes.append(box)

app.run()