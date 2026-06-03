from ursina import *
from ursina.shaders import lit_with_shadows_shader
import random

app = Ursina()

# =========================
# 돌 생성
# =========================

rock = Entity(
    model='test.obj',
    color=color.gray,
    shader=lit_with_shadows_shader,
    collider='mesh'
)

mesh = rock.model
rock.scale = 1.8

# =========================
# 랜덤 시드
# =========================

random.seed(20070525)

# =========================
# tuple -> Vec3 변환
# =========================

vertices = [
    Vec3(v[0], v[1], v[2])
    for v in mesh.vertices
]

# =========================
# 같은 위치 vertex 그룹화
# =========================

vertex_groups = {}

for i, v in enumerate(vertices):

    key = (
        round(v.x, 5),
        round(v.y, 5),
        round(v.z, 5)
    )

    if key not in vertex_groups:
        vertex_groups[key] = []

    vertex_groups[key].append(i)

# =========================
# 랜덤 돌 변형
# =========================

new_vertices = vertices.copy()

for indices in vertex_groups.values():

    original = vertices[indices[0]]

    # 중심에서 바깥 방향
    direction = original.normalized()

    # 랜덤 돌 느낌
    strength = random.uniform(-0.1, 1)

    offset = direction * strength

    # 같은 위치 vertex 전부 같이 이동
    for idx in indices:
        new_vertices[idx] = vertices[idx] + offset

# =========================
# 메쉬 적용
# =========================

mesh.vertices = [
    (v.x, v.y, v.z)
    for v in new_vertices
]

# 재생성
mesh.generate()

# 노멀 재계산
mesh.generate_normals()

# =========================
# 햇빛
# =========================

sun = DirectionalLight()

# 햇빛 방향
sun.look_at(Vec3(1, -1, -1))

# =========================
# 주변광
# =========================

AmbientLight(
    color=color.rgba(120, 120, 120, 0.01)
)

# =========================
# 돌 파티클
# =========================

def create_break_particles(position):

    for i in range(100):

        p = Entity(
            model='cube',
            scale=0.1,
            color=color.light_gray,
            position=position
        )

        direction = Vec3(
            random.uniform(-10, 10),
            random.uniform(-10, 10),
            random.uniform(-10, 10)
        ).normalized()

        p.animate_position(
            p.position + direction * random.uniform(0.01, 0.3),
            duration=0.4,
            curve=curve.out_quad
        )

        p.animate_scale(
            0,
            duration=0.4
        )

        destroy(p, delay=0.45)

# =========================
# 거리 계산 함수
# =========================

def distance_between(a, b):
    return (a - b).length()

# =========================
# 클릭 시 돌 깨짐
# =========================

def input(key):

    if key != 'left mouse down':
        return

    if mouse.hovered_entity != rock:
        return

    hit_point = mouse.world_point

    if not hit_point:
        return

    local_hit = hit_point - rock.world_position

    radius = 0.7
    power = 1.0

    # =========================
    # vertex 변형
    # =========================

    for indices in vertex_groups.values():

        idx = indices[0]

        vertex_tuple = mesh.vertices[idx]

        v = Vec3(
            vertex_tuple[0],
            vertex_tuple[1],
            vertex_tuple[2]
        )

        distance = distance_between(v, local_hit)

        if distance > radius:
            continue

        # 중심부일수록 강함
        falloff = 1.0 - (distance / radius)

        # 돌 중심 방향으로 눌러넣기
        direction = (-v).normalized()

        offset = direction * power * falloff * 0.08

        # 같은 위치 vertex 전부 이동
        for i in indices:

            current_tuple = mesh.vertices[i]

            current = Vec3(
                current_tuple[0],
                current_tuple[1],
                current_tuple[2]
            )

            new_pos = current + offset

            mesh.vertices[i] = (
                new_pos.x,
                new_pos.y,
                new_pos.z
            )

    # =========================
    # 메쉬 갱신
    # =========================

    mesh.generate()
    mesh.generate_normals()

    # =========================
    # 파티클 생성
    # =========================

    create_break_particles(hit_point)

# =========================
# 카메라
# =========================

EditorCamera()

app.run()