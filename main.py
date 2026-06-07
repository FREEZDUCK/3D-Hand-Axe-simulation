from ursina import *
from ursina.shaders import *
import random, threading, time, math
from pathlib import Path

APP_WIDTH = 720
APP_HRIGHT = 1280

app = Ursina(title="Hand Axe Simulater", size=(APP_WIDTH, APP_HRIGHT), borderless=False, development_mode=False)

try:
    screen = window.main_monitor
    screen_size : str = f"{screen.width}x{screen.height}"
    size_data = {
        "2560x1440" : (720, 1280),
        "1920x1080" : (480, 854)
    }

    window.size = (size_data[screen_size][0], size_data[screen_size][1])
except:
    print("해당 스크린의 데이터를 찾을 수 없습니다.")

# ======================================================================

# 스레드로 실행되어서 비동기로 작동되는 타이머
class ThreadTimer():
    def __init__(self, sleep : float, func : Func):
        self.func = func
        threading.Thread(target=self._sleep, daemon=True, args=[sleep]).start()
    def _sleep(self, duration : float):
        time.sleep(duration)
        self.func()

# 카메라 설정
camera.orthographic = True
camera.fov = 10
camera.ortho_scale = 10
camera.position = (0, 0, -100)


class StartScene(Entity):
    def __init__(self):
        super().__init__()

        self.ui_root = Entity(parent=camera.ui)

        self.bg = Entity(
        parent=self,
        model='quad',
        scale=20,
        texture='textures/bg.png'
        )

        self.start_t = Text(
            parent=self.ui_root,
            text='터치하여 시작', 
            font_size = 100, 
            origin=(0, 0.5), 
            position=(0, -0.2), 
            scale=1, 
            color=color.hex("#f5f4ee"), 
            font="assets/fonts/black.ttf")
        
        self.title_t = Text(
            parent=self.ui_root,
            text='행소박물관\n\n체험하기', 
            font_size = 100, 
            origin=(0, 0.5), 
            position=(0, 0.3), 
            scale=1.4, 
            color=color.hex("#f5f4ee"), 
            font="assets/fonts/serif.otf")
        
        self.start_rock = Entity(
            parent=self,
            position = (0, -0.6, -10),
            model="rocks/hand_axe_title.obj",
            shader=basic_lighting_shader,
            color=color.rgba(0.8196, 0.7373, 0.6314, 1.0),
            texture="textures/rock1.jpg",
            collider='mesh',
        )
        self.once_key = False

        def end_fade_out():
            if self.once_key:
                return
            self.start_t.fade_in(1, 3)
            ThreadTimer(4, end_fade_in)
        def end_fade_in():
            if self.once_key:
                return
            self.start_t.fade_out(0, 3)
            ThreadTimer(4, end_fade_out)

        self.start_t.fade_out(0, 3)
        ThreadTimer(4, end_fade_out)

    def update(self):
        self.start_rock.rotation_y += 5 * time.dt

    def change(self):
        self.once_key = False

        def end_fade_out():
            if self.once_key:
                return
            self.start_t.fade_in(1, 3)
            ThreadTimer(4, end_fade_in)
        def end_fade_in():
            if self.once_key:
                return
            self.start_t.fade_out(0, 3)
            ThreadTimer(4, end_fade_out)

        self.start_rock.fade_in(1, 1)
        self.title_t.fade_in(1, 1)
        self.start_t.fade_in(1, 1)
        ThreadTimer(2, end_fade_in)
        
    
    def input(self, key):
        if key == "left mouse down" and self.once_key == False:
            self.start_t.animations.clear()
            self.once_key = True
            self.start_t.color = color.rgba(1, 1, 1, 1)
            self.start_t.fade_out(0, 1)
            self.title_t.fade_out(0, 1)
            self.start_rock.fade_out(0, 1)

            ThreadTimer(1.2, Func(change_current_scene, title_scene))


class TitleScene(Entity):
    def __init__(self):
        super().__init__()

        self.ui_root = Entity(parent=camera.ui)
        self.bg = Entity(
        parent=self,
        model='quad',
        scale=20,
        texture='textures/bg.png'
        )

        self.make_t = Text(
            parent=self.ui_root,
            text = "만들기",
            font_size = 100,
            origin = (0, 0.5), 
            position = (0, 0.45 - 1 * 0.2), 
            scale = 1, 
            color = color.rgba(245, 244, 238, 0), 
            font = "assets/fonts/black.ttf"
            )
        
        self.make_t_coll = Button(
                parent=self.ui_root,
                origin=(0.0, 0.1),
                scale=(0.3, 0.1),
                color=color.rgba(0, 0, 0.3, 0.0),   # 투명
                position=self.make_t.position
                )
        
        self.see_another_t = Text(
            parent=self.ui_root,
            text = "다른 작품 보기",
            font_size = 100,
            origin = (0, 0.5), 
            position = (0, 0.45 - 2 * 0.2), 
            scale = 1, 
            color = color.rgba(245, 244, 238, 0), 
            font = "assets/fonts/black.ttf"
            )
        
        self.see_another_t_coll = Button(
                parent=self.ui_root,
                origin=(0.0, 0.1),
                scale=(0.3, 0.1),
                color=color.rgba(0, 0, 0.3, 0.0),   # 투명
                position=self.see_another_t.position
                )
        
        self.to_start_t = Text(
            parent=self.ui_root,
            text = "시작 화면으로",
            font_size = 100,
            origin = (0, 0.5), 
            position = (0, 0.45 - 3 * 0.2), 
            scale = 1, 
            color = color.rgba(245, 244, 238, 0), 
            font = "assets/fonts/black.ttf"
            )
        
        self.to_start_t_coll = Button(
                parent=self.ui_root,
                origin=(0.0, 0.1),
                scale=(0.3, 0.1),
                color=color.rgba(0, 0, 0.3, 0.0),   # 투명
                position=self.to_start_t.position
                )
        
        self.changing = False
        
    def change(self):
        self.ui_list = [self.make_t, self.see_another_t, self.to_start_t]
        self.changing = False
        if current_scene == title_scene:
            for ui in self.ui_list:
                ui.color = color.rgba(245, 244, 238, 0)
                ui.fade_in(1, 2)
                time.sleep(0.4)

    def update(self):
        pass

    def input(self, key):
        if key == "left mouse down":
            if self.to_start_t_coll.hovered and self.changing == False:
                for ui in self.ui_list:
                    ui.fade_out(0, 0.3)
                self.changing = True
                ThreadTimer(0.7, Func(change_current_scene, start_scene))
            if self.make_t_coll.hovered:
                for ui in self.ui_list:
                    ui.fade_out(0, 0.8)
                self.changing = True
                ThreadTimer(1.3, Func(change_current_scene, main_scene))
            

class MainScene(Entity):
    def __init__(self):
        super().__init__()

        self.ui_root = Entity(parent=camera.ui)

        self.bg = Entity(
            parent=self,
            model='quad',
            scale=20,
            texture='textures/bg.png'
        )

        self.des_t = Text(
            parent=self.ui_root,
            text='당신에게 주어진 돌입니다',
            font_size=100,
            origin=(0, 0.5),
            position=(0, -0.4),
            scale=1,
            color=color.rgba(245, 244, 238, 0),
            font="assets/fonts/black.ttf"
        )

        self.exit_t = Text(
            parent=self.ui_root,
            text='X',
            font_size=100,
            origin=(0, 0.5),
            position=(0, 0.45),
            scale=1,
            color=color.rgba(245, 244, 238, 0),
            font="assets/fonts/light.ttf"
        )

        self.exit_t_coll = Button(
            parent=self.ui_root,
            origin=(0.0, 0.1),
            scale=(0.05, 0.05),
            color=color.rgba(0, 0, 0.3, 0),   # 투명
            position=self.exit_t.position
            )

        self.main_rock = Entity(
            parent=self,
            position=(0, 0, -10),
            scale=1.3,
            model="rocks/example.obj",
            shader=basic_lighting_shader,
            color=color.rgba(0.8196, 0.7373, 0.6314, 0),
            texture="textures/rock" + str(random.randint(1, 3)) + ".jpg",
            collider='mesh',
        )

        # =========================
        # 랜덤 시드
        # ========================

        # =========================
        # mesh 가져오기
        # =========================

        self.base_mesh = load_model("rocks/example.obj", use_deepcopy=True)
        self.mesh = self.base_mesh
        self.main_rock.model = self.mesh

        self.rock_randomize()

        # =========================
        # 조명
        # =========================

        self.sun = DirectionalLight()
        self.sun.look_at(Vec3(1, -1, -1))

        AmbientLight(
            color=color.rgba(120, 120, 120, 0.3)
        )

        self.dragging = False

        self.last_mouse_x = 0
        self.last_mouse_y = 0

        self.target_rot_y = 0
        self.target_rot_x = 0

        self.allow_exit = False

    def rock_randomize(self):
        self.mesh = load_model("rocks/example.obj", use_deepcopy=True)
        self.main_rock.model = self.mesh

        self.main_rock.texture = load_texture("textures/rock" + str(random.randint(1, 3)) + ".jpg")

        self.vertices = [
            Vec3(v[0], v[1], v[2])
            for v in self.mesh.vertices
        ]

        self.vertex_groups = {}
        for i, v in enumerate(self.vertices):

            key = (
                round(v.x, 5),
                round(v.y, 5),
                round(v.z, 5)
            )

            if key not in self.vertex_groups:
                self.vertex_groups[key] = []

            self.vertex_groups[key].append(i)

        self.original_vertices = self.vertices.copy()

        # 여기서 부터 돌 Vertex 랜덤 변형 (돌 느낌 나게)
        new_vertices = self.vertices.copy()

        for indices in self.vertex_groups.values():

            original = self.vertices[indices[0]]

            # 중심에서 바깥 방향
            direction = original.normalized()

            # 변형 강도
            strength = random.uniform(-0.1, 0.7)

            offset = direction * strength

            # 같은 위치 vertex 전부 같이 이동
            for idx in indices:
                new_vertices[idx] = self.vertices[idx] + offset

        self.mesh.vertices = [
            (v.x, v.y, v.z)
            for v in new_vertices
        ]

        # 재생성
        self.mesh.generate()
        self.mesh.generate_normals()
        

    def set_allow_exit(self):
        self.exit_t.fade_in(1, 3)
        self.allow_exit = True

    def hide_des(self):
        self.des_t.fade_out(0, 5)
        ThreadTimer(5.5, self.set_allow_exit)

    def show_next_des(self):
        self.des_t.text = "터치하여 주먹도끼 처럼 깎아보세요\n(주변을 드래그하여 회전할 수 있습니다)"
        self.des_t.fade_in(1, 3.5)
        ThreadTimer(5, self.hide_des)

    def fade_out_des(self):
        self.des_t.fade_out(0, 4)
        ThreadTimer(5, self.show_next_des)

    def change(self):
        self.rock_randomize()
        self.main_rock.fade_in(1, 3)
        self.des_t.fade_in(1, 3.5)
        self.des_t.fade_in(1, 3.5)
        ThreadTimer(5, self.fade_out_des)

    def update(self):
        if self.dragging:
            # 현재 마우스 좌표와 마지막 좌표로 계산
            dx = mouse.x - self.last_mouse_x
            dy = mouse.y - self.last_mouse_y

            # 반대로 해야 방향이 맞음
            rotate_speed = -300

            self.target_rot_y += dx * rotate_speed
            self.target_rot_x -= dy * rotate_speed

            self.target_rot_x = clamp(
                self.target_rot_x,
                -80,
                80
            )

            self.last_mouse_x = mouse.x
            self.last_mouse_y = mouse.y

        # lerp로 끊기는 움직임 보간 = 부드럽게
        self.main_rock.rotation_y = lerp(
            self.main_rock.rotation_y,
            self.target_rot_y,
            time.dt * 8
        )

        self.main_rock.rotation_x = lerp(
            self.main_rock.rotation_x,
            self.target_rot_x,
            time.dt * 8
        )
    def create_break_particles(self, position):

        for i in range(10):

            p = Entity(
                model='cube',
                scale=0.03,
                color=color.light_gray,
                position=position
            )

            direction = Vec3(
                random.uniform(-1, 1),
                random.uniform(-1, 1),
                random.uniform(-1, 1)
            ).normalized()

            p.animate_position(
                p.position + direction * random.uniform(0.1, 0.4),
                duration=0.4,
                curve=curve.out_quad # 움직임 속도 곡선 (자체 제공해줌)
            )

            p.animate_scale(
                0,
                duration=0.4
            )

            destroy(p, delay=0.45)

    def distance_between(self, a, b):
        return (a - b).length()

    def input(self, key):
        if key == 'left mouse down':

            self.dragging = True

            self.last_mouse_x = mouse.x
            self.last_mouse_y = mouse.y

            if self.exit_t_coll.hovered and self.allow_exit:
                self.des_t.animations.clear()
                self.main_rock.fade_out(0, 3)
                self.des_t.fade_out(0, 3)
                self.allow_exit = False
                self.exit_t.fade_out(0, 1)
                self.des_t.text = "당신에게 주어진 돌입니다"
                ThreadTimer(4, Func(change_current_scene, title_scene))

        if key == 'left mouse up':
            self.dragging = False


        if key != 'left mouse down':
            return

        if mouse.hovered_entity != self.main_rock:
            return

        hit_point = mouse.world_point

        if not hit_point:
            return

        p = self.main_rock.getRelativePoint(
            scene,
            hit_point
        )

        local_hit = Vec3(p.x, p.y, p.z)

        radius = 0.3
        power = 1.0

        for indices in self.vertex_groups.values():

            idx = indices[0]

            vertex_tuple = self.mesh.vertices[idx]

            v = Vec3(
                vertex_tuple[0],
                vertex_tuple[1],
                vertex_tuple[2]
            )

            distance = self.distance_between(v, local_hit)

            if distance > radius:
                continue

            falloff = 1.0 - (distance / radius)

            direction = (local_hit - v).normalized()

            strength = random.uniform(0.8, 1.2)

            offset = direction * power * falloff * 0.15 * strength

            # 같은 위치 vertex 전부 이동
            for i in indices:

                current_tuple = self.mesh.vertices[i]

                current = Vec3(
                    current_tuple[0],
                    current_tuple[1],
                    current_tuple[2]
                )

                new_pos = current + offset

                self.mesh.vertices[i] = (
                    new_pos.x,
                    new_pos.y,
                    new_pos.z
                )
        self.mesh.generate()
        self.mesh.generate_normals()

        # collider 갱신
        self.main_rock.collider = MeshCollider(
            self.main_rock,
            mesh=self.mesh
        )
        self.create_break_particles(hit_point)

start_scene = StartScene()
title_scene = TitleScene()
main_scene = MainScene()
current_scene = start_scene

start_scene.enabled = True
start_scene.ui_root.enabled = True
title_scene.enabled = False
title_scene.ui_root.enabled = False
main_scene.enabled = False
main_scene.ui_root.enabled = False

def change_current_scene(goal_scene):
    global current_scene, start_scene, title_scene, main_scene

    current_scene = goal_scene
    start_scene.enabled = False
    start_scene.ui_root.enabled = False
    title_scene.enabled = False
    title_scene.ui_root.enabled = False
    main_scene.enabled = False
    main_scene.ui_root.enabled = False

    # 현재 씬 활성화
    current_scene.enabled = True
    current_scene.ui_root.enabled = True
    current_scene.change()

app.run()