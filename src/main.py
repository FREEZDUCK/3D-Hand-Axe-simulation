from ursina import *

app = Ursina()

# 플레이어 기준점 (몸)
ground = Entity(
    model='plane',
    scale=20,
    color=color.gray,
    texture='grass',
    collider='box'
)

player = Entity()

# 카메라를 플레이어에 붙임
camera.parent = player
camera.position = (0, 1.8, 0)
camera.fov = 110

# 마우스 잠금 (중요)
mouse.locked = True

# 감도
sensitivity = 40

def update():
    # 좌우 회전 (Yaw)
    player.rotation_y += mouse.velocity[0] * sensitivity

    # 상하 회전 (Pitch)
    camera.rotation_x -= mouse.velocity[1] * sensitivity
    camera.rotation_x = clamp(camera.rotation_x, -90, 90)

    if held_keys["w"]:
        player.position += player.forward * time.dt * 2
    if held_keys["s"]:
        player.position -= player.forward * time.dt * 2
    if held_keys["a"]:
        player.position += player.left * time.dt * 2
    if held_keys["d"]:
        player.position += player.right * time.dt * 2
    
    if held_keys["space"]:
        player.position += player.up * time.dt * 2
    if held_keys["shift"]:
        player.position += player.down * time.dt * 2

app.run()