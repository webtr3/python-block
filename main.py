from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()
window.title = 'Block Builder'
window.size = (1200, 620)
window.fps_counter.enabled = True
window.exit_button.visible = False

BLOCK_TYPES = [
    ('Grass',  color.lime,        'white_cube'),
    ('Dirt',   rgb(139, 90, 43),  'white_cube'),
    ('Stone',  color.gray,        'white_cube'),
    ('Sand',   rgb(240, 210, 130),'white_cube'),
    ('Wood',   rgb(160, 100, 40), 'white_cube'),
    ('Snow',   color.white,       'white_cube'),
    ('Lava',   rgb(255, 80, 0),   'white_cube'),
    ('Water',  color.azure,       'white_cube'),
]

selected_block_index = 0

def make_block(position, block_index=None):
    if block_index is None:
        block_index = selected_block_index
    name, col, tex = BLOCK_TYPES[block_index]
    b = Button(
        color=col,
        model='cube',
        texture=tex,
        position=position,
        parent=scene,
        origin_y=0.5,
        collider='box',
        highlight_color=color.white33,
    )
    b.block_index = block_index
    return b

GROUND_SIZE = 20
for gx in range(GROUND_SIZE):
    for gz in range(GROUND_SIZE):
        make_block((gx, 0, gz), block_index=0)

player = FirstPersonController(
    position=(GROUND_SIZE // 2, 2, GROUND_SIZE // 2),
    mouse_sensitivity=Vec2(40, 40),
)
player.cursor.color = color.clear

sky = Sky(texture='sky_default')
scene.fog_color = color.rgb(180, 210, 230)
scene.fog_density = 0.02
is_day = True

crosshair = Entity(
    parent=camera.ui,
    model='quad',
    color=color.white66,
    scale=0.002,
)
Entity(parent=crosshair, model='quad', color=color.white66,
       scale=(10, 1), position=(0, 0, 0))
Entity(parent=crosshair, model='quad', color=color.white66,
       scale=(1, 10), position=(0, 0, 0))

HOTBAR_SLOTS = len(BLOCK_TYPES)
SLOT_SIZE    = 0.06
SLOT_GAP     = 0.005
hotbar_bg = Entity(
    parent=camera.ui,
    model='quad',
    color=color.black50,
    scale=(SLOT_SIZE * HOTBAR_SLOTS + SLOT_GAP * (HOTBAR_SLOTS + 1), SLOT_SIZE + SLOT_GAP * 2),
    position=(0, -0.44),
)

hotbar_slots   = []
hotbar_labels  = []
hotbar_selector = None

for i, (bname, bcol, _) in enumerate(BLOCK_TYPES):
    x = (i - (HOTBAR_SLOTS - 1) / 2) * (SLOT_SIZE + SLOT_GAP)
    slot = Entity(
        parent=camera.ui,
        model='quad',
        color=bcol,
        scale=SLOT_SIZE * 0.85,
        position=(x, -0.44),
    )
    label = Text(
        text=bname,
        parent=camera.ui,
        position=(x, -0.48),
        origin=(0, 0),
        scale=0.6,
        color=color.white,
    )
    hotbar_slots.append(slot)
    hotbar_labels.append(label)

hotbar_selector = Entity(
    parent=camera.ui,
    model='quad',
    color=color.clear,
    scale=SLOT_SIZE * 0.95,
    position=(0, -0.44),
)

selector_border = Entity(
    parent=camera.ui,
    model='quad',
    color=color.white,
    scale=SLOT_SIZE,
    position=(0, -0.44),
    z=0.01,
)

block_count_text = Text(
    text='Blocks: 0',
    parent=camera.ui,
    position=(-0.85, 0.45),
    origin=(-0.5, 0),
    scale=1.2,
    color=color.white,
)

controls_text = Text(
    text='LMB: Place  RMB: Break  Scroll/1-8: Select  F11: Fullscreen  N: Night  Esc: Pause',
    parent=camera.ui,
    position=(0, -0.47),
    origin=(0, 0),
    scale=0.6,
    color=color.white66,
)

placed_count = 0

def update_hotbar_selector():
    x = (selected_block_index - (HOTBAR_SLOTS - 1) / 2) * (SLOT_SIZE + SLOT_GAP)
    hotbar_selector.position = (x, -0.44, -0.01)
    selector_border.position = (x, -0.44, 0.02)

update_hotbar_selector()

paused = False

pause_bg = Entity(
    parent=camera.ui,
    model='quad',
    color=color.black66,
    scale=(0.5, 0.5),
    enabled=False,
    z=-1,
)
pause_title = Text(
    text='⏸  Paused',
    parent=camera.ui,
    origin=(0, 0),
    position=(0, 0.12),
    scale=2.5,
    color=color.white,
    enabled=False,
)
resume_btn = Button(
    text='Resume',
    parent=camera.ui,
    position=(0, -0.02),
    scale=(0.18, 0.07),
    color=color.dark_gray,
    highlight_color=color.gray,
    enabled=False,
)
quit_btn = Button(
    text='Quit',
    parent=camera.ui,
    position=(0, -0.12),
    scale=(0.18, 0.07),
    color=color.dark_gray,
    highlight_color=color.gray,
    enabled=False,
)
pause_entities = [pause_bg, pause_title, resume_btn, quit_btn]

def toggle_pause():
    global paused
    paused = not paused
    for e in pause_entities:
        e.enabled = paused
    player.enabled   = not paused
    mouse.locked     = not paused
    mouse.visible    = paused

resume_btn.on_click = toggle_pause
quit_btn.on_click   = application.quit

def toggle_day_night():
    global is_day
    is_day = not is_day
    if is_day:
        sky.texture         = load_texture('sky_default')
        scene.fog_color     = color.rgb(180, 210, 230)
        scene.fog_density   = 0.02
        scene.ambient_light = color.rgb(200, 200, 200)
    else:
        sky.color           = color.rgb(5, 5, 25)
        scene.fog_color     = color.rgb(5, 5, 25)
        scene.fog_density   = 0.03
        scene.ambient_light = color.rgb(30, 30, 60)

def input(key):
    global selected_block_index, placed_count

    if key == 'escape':
        toggle_pause()
        return

    if key == 'f11':
        window.fullscreen = not window.fullscreen
        return

    if key == 'n':
        toggle_day_night()
        return

    if key.isdigit() and 1 <= int(key) <= HOTBAR_SLOTS:
        selected_block_index = int(key) - 1
        update_hotbar_selector()
        return

    if paused:
        return

    if key == 'scroll up':
        selected_block_index = (selected_block_index - 1) % HOTBAR_SLOTS
        update_hotbar_selector()

    elif key == 'scroll down':
        selected_block_index = (selected_block_index + 1) % HOTBAR_SLOTS
        update_hotbar_selector()

    elif key == 'left mouse down':
        target = mouse.hovered_entity
        if target and hasattr(target, 'block_index'):
            new_pos = target.position + mouse.normal
            make_block(new_pos)
            placed_count += 1
            block_count_text.text = f'Blocks placed: {placed_count}'

    elif key == 'right mouse down':
        target = mouse.hovered_entity
        if target and hasattr(target, 'block_index'):
            destroy(target)

def update():
    crosshair.position = (0, 0)

app.run()