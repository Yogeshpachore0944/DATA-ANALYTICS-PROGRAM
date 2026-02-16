import pygame
import sys

pygame.init()

# ---------------- Screen ----------------
WIDTH, HEIGHT = 1200, 520
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Kid Smart Stops")

clock = pygame.time.Clock()

# ---------------- Load Background ----------------
road = pygame.image.load("images/road.png").convert()
road = pygame.transform.scale(road, (WIDTH, HEIGHT))

# ---------------- Load Places ----------------
food_shop_img   = pygame.image.load("images/food_shop.png").convert_alpha()
friend_home_img = pygame.image.load("images/friend_home.png").convert_alpha()
my_home_img     = pygame.image.load("images/my_home.png").convert_alpha()

food_shop_img   = pygame.transform.scale(food_shop_img, (200, 100))
friend_home_img = pygame.transform.scale(friend_home_img, (200, 100))
my_home_img     = pygame.transform.scale(my_home_img, (200, 100))

# ---------------- Load Obstacles ----------------
cow_img = pygame.image.load("images/cow.png").convert_alpha()
barrier_img = pygame.image.load("images/barrier.png").convert_alpha()

cow_img = pygame.transform.scale(cow_img, (160, 80))
barrier_img = pygame.transform.scale(barrier_img, (200, 80))

# ---------------- Load Sprite Sheet ----------------
sprite_sheet = pygame.image.load("images/kid_sprite.png").convert_alpha()

ROWS, COLS = 2, 4
FRAME_WIDTH = sprite_sheet.get_width() // COLS
FRAME_HEIGHT = sprite_sheet.get_height() // ROWS

def get_frames(sheet):
    frames = []
    for r in range(ROWS):
        for c in range(COLS):
            frame = sheet.subsurface(
                c * FRAME_WIDTH,
                r * FRAME_HEIGHT,
                FRAME_WIDTH,
                FRAME_HEIGHT
            )
            frame = pygame.transform.scale(frame, (80, 80))
            frames.append(frame)
    return frames

walk_frames = get_frames(sprite_sheet)
idle_frame = walk_frames[0]

# ---------------- Road Lines ----------------
MAIN_Y = 360
SIDE_Y = 260

# ---------------- Kid ----------------
kid_x = 40
kid_y = MAIN_Y
speed = 2.5
curve_speed = 2.0

# ---------------- Stops ----------------
food_x   = 350
friend_x = 700
home_x   = 1020

SLOW_ZONE = 80
SLOW_SPEED = 1.0

# ---------------- Places Positions ----------------
food_shop_pos   = (food_x + 20, MAIN_Y - 150)
friend_home_pos = (friend_x - 40, MAIN_Y - 150)
my_home_pos     = (home_x - 40, MAIN_Y - 170)

# ---------------- Obstacles ----------------
obstacles = [
    {"img": cow_img, "x": 250, "y": MAIN_Y - 30},
    {"img": barrier_img, "x": 560, "y": MAIN_Y - 30},
]

# ---------------- Curved Avoidance ----------------
avoiding = False
avoid_phase = "none"
current_obstacle = None

# ---------------- Stop Control ----------------
stop_mode = False
stop_phase = "none"
stop_timer = 0

# ---------------- Footstep Dust ----------------
dust_particles = []
DUST_LIFE = 30

# ---------------- Animation ----------------
frame_index = 0
frame_timer = 0
animation_speed = 7

# ---------------- Timing ----------------
WAIT_TIME = 5000

# ---------------- Final Message Control ----------------
show_final_message = False
final_timer = 0
FINAL_DISPLAY_TIME = 2000

# ---------------- Stages ----------------
stage = "to_food"

font = pygame.font.SysFont(None, 34)

# ---------------- Main Loop ----------------
running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # -------- Draw Road --------
    screen.blit(road, (0, 0))
    pygame.draw.line(screen, (200,200,200), (0, SIDE_Y+40), (WIDTH, SIDE_Y+40), 2)

    # -------- Draw Places --------
    screen.blit(food_shop_img, food_shop_pos)
    screen.blit(friend_home_img, friend_home_pos)
    screen.blit(my_home_img, my_home_pos)

    # -------- Draw Obstacles --------
    obstacle_rects = []
    for obs in obstacles:
        rect = obs["img"].get_rect(topleft=(obs["x"], obs["y"]))
        obstacle_rects.append(rect)
        screen.blit(obs["img"], (obs["x"], obs["y"]))

    kid_rect = pygame.Rect(kid_x, kid_y, 70, 80)

    # -------- Trigger Stop Zones (Exact Align) --------
    if not stop_mode and not avoiding:

        target_x = None
        if stage == "to_food":
            target_x = food_x
        elif stage == "to_friend":
            target_x = friend_x
        elif stage == "to_home":
            target_x = home_x

        if target_x is not None and kid_x >= target_x:
            kid_x = target_x
            stop_mode = True
            stop_phase = "up"

    # -------- Stop Movement Logic --------
    if stop_mode:
        if stop_phase == "up":
            kid_y -= curve_speed
            if kid_y <= SIDE_Y:
                kid_y = SIDE_Y
                stop_phase = "wait"
                stop_timer = pygame.time.get_ticks()

        elif stop_phase == "wait":
            if pygame.time.get_ticks() - stop_timer >= WAIT_TIME:
                stop_phase = "down"

        elif stop_phase == "down":
            kid_y += curve_speed
            if kid_y >= MAIN_Y:
                kid_y = MAIN_Y
                stop_mode = False
                stop_phase = "none"

                if stage == "to_food":
                    stage = "to_friend"

                elif stage == "to_friend":
                    stage = "to_home"

                elif stage == "to_home":
                    show_final_message = True
                    final_timer = pygame.time.get_ticks()

    # -------- Detect Obstacle --------
    if stage in ["to_food", "to_friend", "to_home"] and not avoiding and not stop_mode:
        for obs in obstacle_rects:
            if kid_rect.colliderect(obs.inflate(80, 40)):
                avoiding = True
                avoid_phase = "up"
                current_obstacle = obs
                break

    # -------- Curved Avoidance Logic --------
    if avoiding:
        if avoid_phase == "up":
            kid_y -= curve_speed
            kid_x += speed * 0.5
            if kid_y <= SIDE_Y:
                avoid_phase = "forward"

        elif avoid_phase == "forward":
            kid_x += speed
            if kid_x > current_obstacle.right + 40:
                avoid_phase = "down"

        elif avoid_phase == "down":
            kid_y += curve_speed
            kid_x += speed * 0.5
            if kid_y >= MAIN_Y:
                kid_y = MAIN_Y
                avoiding = False
                avoid_phase = "none"

    # -------- Animation Control --------
    moving = (stage in ["to_food", "to_friend", "to_home"] and not stop_mode) or avoiding

    if moving:
        frame_timer += 1
        if frame_timer >= animation_speed:
            frame_timer = 0
            frame_index = (frame_index + 1) % len(walk_frames)
        kid_img = walk_frames[frame_index]
    else:
        kid_img = idle_frame

    screen.blit(kid_img, (kid_x, kid_y))

    # -------- Footstep Dust --------
    if moving and not stop_mode and not avoiding and kid_y == MAIN_Y:
        if frame_timer % 6 == 0:
            dust_particles.append({
                "x": kid_x + 10,
                "y": kid_y + 70,
                "life": DUST_LIFE
            })

    for dust in dust_particles[:]:
        dust["life"] -= 1
        dust["y"] -= 0.2
        radius = max(1, dust["life"] // 6)
        pygame.draw.circle(screen, (180,180,180),
                           (int(dust["x"]), int(dust["y"])), radius)
        if dust["life"] <= 0:
            dust_particles.remove(dust)

    # -------- Forward Movement (Slow Down Near Stops) --------
    if not stop_mode and not avoiding:

        target_x = None
        if stage == "to_food":
            target_x = food_x
        elif stage == "to_friend":
            target_x = friend_x
        elif stage == "to_home":
            target_x = home_x

        if target_x is not None:
            distance = target_x - kid_x
            move_speed = SLOW_SPEED if 0 < distance < SLOW_ZONE else speed
            kid_x += move_speed

    # -------- Final Message Display --------
    if show_final_message:
        msg = font.render("🏡 Kid Reached Home Successfully!", True, (0, 150, 0))
        screen.blit(msg, (380, 40))

        if pygame.time.get_ticks() - final_timer >= FINAL_DISPLAY_TIME:
            running = False

    pygame.display.update()

pygame.quit()
sys.exit()
