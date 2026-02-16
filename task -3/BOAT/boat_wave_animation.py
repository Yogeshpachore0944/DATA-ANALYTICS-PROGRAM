import tkinter as tk
import random
import math

# Window setup
WIDTH = 950
HEIGHT = 550

root = tk.Tk()
root.title("🚤 Boat Sailing on Waves")
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="#87CEEB")
canvas.pack()

# -------------------- Water --------------------
WATER_LEVEL = HEIGHT - 170
canvas.create_rectangle(0, WATER_LEVEL, WIDTH, HEIGHT, fill="#159bd6", outline="")

# -------------------- Waves --------------------
wave_offset = 0
wave_lines = []
WAVE_GAP = 30
WAVE_AMPLITUDE = 14

def create_waves():
    for x in range(0, WIDTH + WAVE_GAP, WAVE_GAP):
        wave_lines.append(canvas.create_line(x, WATER_LEVEL, x+WAVE_GAP, WATER_LEVEL, fill="white", width=2))
create_waves()

def animate_waves():
    global wave_offset
    wave_offset += 0.25
    for i, line in enumerate(wave_lines):
        y = WATER_LEVEL + math.sin(wave_offset + i) * WAVE_AMPLITUDE
        canvas.coords(line, i*WAVE_GAP, y, i*WAVE_GAP + WAVE_GAP, y)

def get_wave_y(x):
    index = int(x // WAVE_GAP)
    return WATER_LEVEL + math.sin(wave_offset + index) * WAVE_AMPLITUDE

# -------------------- Clouds --------------------
clouds = []

def create_cloud():
    x = random.randint(-200, -50)
    y = random.randint(30, WATER_LEVEL-220)
    speed = random.uniform(0.5, 1.2)

    c1 = canvas.create_oval(x, y, x+60, y+40, fill="white", outline="")
    c2 = canvas.create_oval(x+30, y-20, x+100, y+30, fill="white", outline="")
    c3 = canvas.create_oval(x+70, y, x+140, y+40, fill="white", outline="")

    clouds.append([c1, c2, c3, speed])

def move_clouds():
    for cloud in clouds[:]:
        for part in cloud[:-1]:
            canvas.move(part, cloud[-1], 0)

        coords = canvas.coords(cloud[0])
        if coords and coords[0] > WIDTH + 200:
            for part in cloud[:-1]:
                canvas.delete(part)
            clouds.remove(cloud)

    if len(clouds) < 5 and random.random() < 0.01:
        create_cloud()

# -------------------- Birds --------------------
birds = []

def create_bird():
    x = random.randint(WIDTH+50, WIDTH+300)
    y = random.randint(60, WATER_LEVEL-200)
    speed = random.uniform(2.5, 4.5)
    size = random.randint(12, 18)

    wing1 = canvas.create_arc(x, y, x+size, y+size, start=0, extent=180, style="arc", width=2)
    wing2 = canvas.create_arc(x+size, y, x+size*2, y+size, start=0, extent=180, style="arc", width=2)

    birds.append([wing1, wing2, speed])

def move_birds():
    for bird in birds[:]:
        canvas.move(bird[0], -bird[2], math.sin(random.random()*3) * 0.5)
        canvas.move(bird[1], -bird[2], math.sin(random.random()*3) * 0.5)

        coords = canvas.coords(bird[0])
        if coords and coords[2] < -50:
            canvas.delete(bird[0])
            canvas.delete(bird[1])
            birds.remove(bird)

    if len(birds) < 4 and random.random() < 0.02:
        create_bird()

# -------------------- Boat --------------------
# -------------------- Attractive Realistic Boat --------------------
boat_x = 150
boat_speed = 2
boat_angle = 0

hull_shadow = canvas.create_polygon(0,0,1,1,2,2, fill="#2a2a2a", outline="", smooth=True)
hull_main   = canvas.create_polygon(0,0,1,1,2,2, fill="#ffffff", outline="black", width=2, smooth=True)
waterline   = canvas.create_polygon(0,0,1,1,2,2, fill="#0077b6", outline="", smooth=True)

cabin       = canvas.create_polygon(0,0,1,1,2,2, fill="#f1f1f1", outline="black", width=2)
windshield  = canvas.create_polygon(0,0,1,1,2,2, fill="#48cae4", outline="")
railing     = canvas.create_line(0,0,1,1, fill="silver", width=2)

flag        = canvas.create_polygon(0,0,1,1,2,2, fill="red")
flag_pole   = canvas.create_line(0,0,1,1, fill="black", width=3)

def rotate_point(px, py, cx, cy, angle):
    rad = math.radians(angle)
    s = math.sin(rad)
    c = math.cos(rad)
    px -= cx
    py -= cy
    return (px * c - py * s + cx, px * s + py * c + cy)

def rotate_points(points, center, angle):
    rotated = []
    for p in points:
        rotated += rotate_point(p[0], p[1], center[0], center[1], angle)
    return rotated

def draw_boat():
    global boat_x, boat_angle

    boat_x += boat_speed
    if boat_x > WIDTH + 200:
        boat_x = -200

    cx = boat_x + 110
    wave_c = get_wave_y(cx)
    wave_f = get_wave_y(cx + 60)
    wave_b = get_wave_y(cx - 60)

    boat_y = wave_c - 25
    slope = wave_f - wave_b
    boat_angle = slope * 0.6
    center = (cx, boat_y)

    # --- Smooth Modern Hull ---
    hull = [
        (boat_x, boat_y+8),
        (boat_x+30, boat_y-18),
        (boat_x+90, boat_y-28),
        (boat_x+160, boat_y-25),
        (boat_x+210, boat_y-10),
        (boat_x+230, boat_y+8),
        (boat_x+180, boat_y+35),
        (boat_x+90, boat_y+40),
        (boat_x+30, boat_y+30)
    ]

    shadow = [(x, y+12) for (x,y) in hull]

    canvas.coords(hull_shadow, *rotate_points(shadow, center, boat_angle))
    canvas.coords(hull_main, *rotate_points(hull, center, boat_angle))

    # --- Blue Waterline Stripe ---
    stripe = [
        (boat_x+40, boat_y+10),
        (boat_x+190, boat_y+10),
        (boat_x+170, boat_y+18),
        (boat_x+60, boat_y+18)
    ]

    canvas.coords(waterline, *rotate_points(stripe, center, boat_angle))

    # --- Cabin ---
    cabin_shape = [
        (boat_x+90, boat_y-75),
        (boat_x+160, boat_y-75),
        (boat_x+180, boat_y-28),
        (boat_x+70, boat_y-28)
    ]

    canvas.coords(cabin, *rotate_points(cabin_shape, center, boat_angle))

    # --- Windshield Glass ---
    glass = [
        (boat_x+105, boat_y-65),
        (boat_x+145, boat_y-65),
        (boat_x+160, boat_y-40),
        (boat_x+90, boat_y-40)
    ]

    canvas.coords(windshield, *rotate_points(glass, center, boat_angle))

    # --- Front Railing ---
    rail_start = rotate_point(boat_x+40, boat_y-5, center[0], center[1], boat_angle)
    rail_end   = rotate_point(boat_x+80, boat_y-20, center[0], center[1], boat_angle)
    canvas.coords(railing, rail_start[0], rail_start[1], rail_end[0], rail_end[1])

    # --- Flag ---
    # --- Center Top Flag ---
    flag_x = boat_x + 125
    flag_base_y = boat_y - 75
    flag_top_y  = boat_y - 120

    pole_top  = rotate_point(flag_x, flag_top_y, center[0], center[1], boat_angle)
    pole_base = rotate_point(flag_x, flag_base_y, center[0], center[1], boat_angle)

    canvas.coords(flag_pole,
                  pole_base[0], pole_base[1],
                  pole_top[0], pole_top[1])

    # Flag animation
    wave_flag = math.sin(wave_offset * 4) * 6

    flag_shape = [
        (flag_x, flag_top_y),
        (flag_x + 35 + wave_flag, flag_top_y + 12),
        (flag_x, flag_top_y + 24)
    ]

    canvas.coords(flag, *rotate_points(flag_shape, center, boat_angle))
# -------------------- Underwater ROCK Obstacles --------------------
obstacles = []

def create_rock(x, y):
    size = random.randint(25, 40)
    points = [
        (x, y),
        (x+size, y-10),
        (x+size+20, y+10),
        (x+size-10, y+30),
        (x-10, y+20)
    ]
    rock = canvas.create_polygon(*sum(points, ()), fill="#9c7c5c", outline="black")
    return rock

for i in range(6):
    x = random.randint(WIDTH+200, WIDTH+1200)
    y = random.randint(WATER_LEVEL+60, HEIGHT-30)
    speed = random.randint(2,5)
    rock = create_rock(x, y)
    obstacles.append([rock,x,y,speed])

def move_obstacles():
    for obs in obstacles:
        rock,x,y,speed = obs
        canvas.move(rock, -speed - boat_speed, 0)
        x -= speed + boat_speed

        if x < -100:
            x = random.randint(WIDTH+400, WIDTH+1400)
            y = random.randint(WATER_LEVEL+60, HEIGHT-30)
            canvas.coords(rock, *sum(create_rock(x, y) and [], ()))

        obs[1],obs[2] = x,y

# -------------------- Fish --------------------
# -------------------- Realistic Fish (Both Directions Correct) --------------------
fishes = []

def create_fish():
    direction = random.choice([-1, 1])
    y = random.randint(WATER_LEVEL+60, HEIGHT-40)
    speed = random.uniform(1.5, 3.0) * direction

    if direction == 1:
        x = random.randint(-200, 0)  # start left
    else:
        x = random.randint(WIDTH, WIDTH+200)  # start right

    tag = f"fish{len(fishes)}"

    if direction == 1:
        # Moving RIGHT → head on right
        canvas.create_polygon(x, y,
                              x-15, y-12,
                              x-15, y+12,
                              fill="#ff6347", outline="black", tags=tag)  # tail

        canvas.create_oval(x, y-10, x+30, y+10,
                           fill="#ff7f50", outline="black", tags=tag)  # body

        canvas.create_oval(x+20, y-4, x+26, y+2,
                           fill="white", outline="", tags=tag)  # eye

        canvas.create_oval(x+22, y-2, x+24, y,
                           fill="black", outline="", tags=tag)

    else:
        # Moving LEFT → head on left
        canvas.create_polygon(x, y,
                              x+15, y-12,
                              x+15, y+12,
                              fill="#ff6347", outline="black", tags=tag)  # tail

        canvas.create_oval(x-30, y-10, x, y+10,
                           fill="#ff7f50", outline="black", tags=tag)  # body

        canvas.create_oval(x-26, y-4, x-20, y+2,
                           fill="white", outline="", tags=tag)  # eye

        canvas.create_oval(x-24, y-2, x-22, y,
                           fill="black", outline="", tags=tag)

    fishes.append([tag, speed])

for i in range(8):
    create_fish()

def move_fishes():
    for fish in fishes:
        tag, speed = fish

        canvas.move(tag, speed, 0)
        coords = canvas.coords(tag)

        if not coords:
            continue

        # If moving right and exits screen
        if speed > 0 and coords[2] > WIDTH + 50:
            canvas.move(tag, -WIDTH - 250, random.randint(-40, 40))

        # If moving left and exits screen
        if speed < 0 and coords[0] < -50:
            canvas.move(tag, WIDTH + 250, random.randint(-40, 40))
# -------------------- Bubble Spark Trails --------------------
bubbles = []

def create_bubble(x, y):
    size = random.randint(4,7)
    spark = canvas.create_line(x, y, x+size, y-size, fill="white", width=2)
    bubbles.append([spark, random.uniform(-0.4,0.4), random.uniform(-2,-1), 50])

def move_bubbles():
    for b in bubbles[:]:
        canvas.move(b[0], b[1], b[2])
        b[3] -= 1
        if b[3] <= 0:
            canvas.delete(b[0])
            bubbles.remove(b)

# -------------------- Animation Loop --------------------
def animate():
    animate_waves()
    draw_boat()
    move_clouds()
    move_birds()
    move_obstacles()
    move_fishes()
    move_bubbles()

    if random.random() < 0.4:
        create_bubble(boat_x + 40, WATER_LEVEL + 25)

    root.after(30, animate)

animate()
root.mainloop()
