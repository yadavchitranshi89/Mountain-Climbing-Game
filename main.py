import pygame
import random
import math
import sys

pygame.init()

# ============================================================
# WINDOW
# ============================================================

WIDTH = 1200
HEIGHT = 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mountain Climber - Blue Summit")

clock = pygame.time.Clock()
FPS = 60

# ============================================================
# WORLD
# ============================================================

WORLD_WIDTH = 6500
WORLD_HEIGHT = 3600

# ============================================================
# COLORS
# ============================================================
# ============================================================
# COLORS
# ============================================================

# ---------- SKY ----------
SKY_TOP = (25, 105, 175)
SKY_MIDDLE = (65, 145, 210)
SKY_BOTTOM = (155, 215, 245)

# ---------- GENERAL BLUE ----------
BLUE_DARK = (25, 70, 115)
BLUE = (45, 120, 180)
BLUE_LIGHT = (90, 165, 220)
LIGHT_BLUE = (125, 195, 240)
DARK_BLUE = (20, 60, 100)

# ---------- BLUE MOUNTAINS ----------
MOUNTAIN_BLUE_DARK = (25, 45, 65)
MOUNTAIN_BLUE = (50, 85, 120)
MOUNTAIN_BLUE_LIGHT = (85, 125, 155)

# ---------- BROWN MOUNTAINS ----------
MOUNTAIN_BROWN_DARK = (55, 40, 32)
MOUNTAIN_BROWN = (105, 72, 48)
MOUNTAIN_BROWN_LIGHT = (145, 105, 70)

# ---------- BLACK MOUNTAINS ----------
MOUNTAIN_BLACK = (18, 22, 27)

# ---------- OLD MOUNTAIN NAMES ----------
# These prevent errors in older parts of the code.
MOUNTAIN_DARK = MOUNTAIN_BLUE_DARK
MOUNTAIN = MOUNTAIN_BLUE
MOUNTAIN_LIGHT = MOUNTAIN_BLUE_LIGHT

# ---------- SNOW ----------
SNOW = (235, 245, 250)
SNOW_SHADOW = (190, 210, 225)

# ---------- WHITE / GRAY ----------
WHITE = (255, 255, 255)
LIGHT_GRAY = (210, 225, 235)

# ---------- ROCKS ----------
DARK_ROCK = (38, 43, 48)
ROCK = (75, 85, 92)
LIGHT_ROCK = (120, 130, 135)

# ---------- TREES ----------
VERY_DARK_GREEN = (2, 25, 12)
DARK_GREEN = (4, 40, 18)
GREEN = (7, 55, 24)

# ---------- BROWN ----------
BROWN = (120, 85, 55)
DARK_BROWN = (70, 48, 35)
LIGHT_BROWN = (165, 110, 65)

# ---------- UI / ITEMS ----------
RED = (220, 65, 65)
YELLOW = (255, 210, 60)
GOLD = (255, 185, 40)
PURPLE = (120, 80, 180)
ORANGE = (240, 140, 50)

# ---------- ENVIRONMENT ----------
FOG = (180, 210, 225)

# ---------- BLACK ----------
BLACK = (8, 15, 25)

# ============================================================
# PROCEDURAL MOUNTAIN SETTINGS
# ============================================================

MOUNTAIN_SEED = 8271

def mountain_noise(x, seed=0):
    """
    Deterministic smooth noise.
    Same x always gives the same mountain shape.
    """
    return (
        math.sin(x * 0.0042 + seed) * 55
        + math.sin(x * 0.0091 + seed * 2.1) * 28
        + math.sin(x * 0.017 + seed * 0.7) * 14
        + math.sin(x * 0.031 + seed * 1.8) * 7
    )

# ============================================================
# FONTS
# ============================================================

font_small = pygame.font.SysFont("arial", 17)
font_medium = pygame.font.SysFont("arial", 23, bold=True)
font_large = pygame.font.SysFont("arial", 38, bold=True)
font_title = pygame.font.SysFont("arial", 62, bold=True)

# ============================================================
# HELPER
# ============================================================

def clamp(value, minimum, maximum):
    return max(minimum, min(value, maximum))


def draw_text(text, font, color, x, y, center=False):

    image = font.render(text, True, color)

    if center:
        rect = image.get_rect(center=(x, y))
    else:
        rect = image.get_rect(topleft=(x, y))

    screen.blit(image, rect)


# ============================================================
# DEEP BLUE SKY
# ============================================================

def draw_sky():

    for y in range(HEIGHT):

        ratio = y / HEIGHT

        if ratio < 0.55:

            t = ratio / 0.55

            r = int(
                SKY_TOP[0] * (1 - t)
                + SKY_MIDDLE[0] * t
            )

            g = int(
                SKY_TOP[1] * (1 - t)
                + SKY_MIDDLE[1] * t
            )

            b = int(
                SKY_TOP[2] * (1 - t)
                + SKY_MIDDLE[2] * t
            )

        else:

            t = (ratio - 0.55) / 0.45

            r = int(
                SKY_MIDDLE[0] * (1 - t)
                + SKY_BOTTOM[0] * t
            )

            g = int(
                SKY_MIDDLE[1] * (1 - t)
                + SKY_BOTTOM[1] * t
            )

            b = int(
                SKY_MIDDLE[2] * (1 - t)
                + SKY_BOTTOM[2] * t
            )

        pygame.draw.line(
            screen,
            (r, g, b),
            (0, y),
            (WIDTH, y)
        )


# ============================================================
# MOON + STARS
# ============================================================

def draw_moon():

    # Moon glow
    glow = pygame.Surface(
        (WIDTH, HEIGHT),
        pygame.SRCALPHA
    )

    pygame.draw.circle(
        glow,
        (180, 205, 235, 20),
        (1010, 95),
        70
    )

    pygame.draw.circle(
        glow,
        (200, 220, 245, 25),
        (1010, 95),
        58
    )

    screen.blit(glow, (0, 0))

    # Moon
    pygame.draw.circle(
        screen,
        (220, 230, 240),
        (1010, 95),
        43
    )

    # Crescent shadow
    pygame.draw.circle(
        screen,
        SKY_TOP,
        (1028, 80),
        40
    )

    # Stars
    random.seed(10)

    for _ in range(85):

        x = random.randint(0, WIDTH)
        y = random.randint(15, 330)

        size = random.choice([1, 1, 1, 2])

        brightness = random.randint(175, 235)

        pygame.draw.circle(
            screen,
            (
                brightness - 15,
                brightness,
                255
            ),
            (x, y),
            size
        )

    random.seed()

# ============================================================
# FAR MOUNTAINS - SIMPLE DISTANT BACKGROUND
# ============================================================

def draw_far_mountains(camera_x):

    parallax = camera_x * 0.10

    # Distant mountain silhouette
    points = [
        (0, HEIGHT),
        (-100 + parallax, 430),
        (100 + parallax, 300),
        (300 + parallax, 400),
        (520 + parallax, 260),
        (750 + parallax, 390),
        (950 + parallax, 290),
        (1180 + parallax, 370),
        (1400 + parallax, 280),
        (WIDTH, HEIGHT)
    ]

    pygame.draw.polygon(
        screen,
        (55, 85, 120),
        points
    )

    # Subtle mountain facets
    pygame.draw.polygon(
        screen,
        (45, 75, 110),
        [
            (100 + parallax, 300),
            (-20 + parallax, HEIGHT),
            (230 + parallax, HEIGHT)
        ]
    )

    pygame.draw.polygon(
        screen,
        (70, 105, 140),
        [
            (520 + parallax, 260),
            (350 + parallax, HEIGHT),
            (700 + parallax, HEIGHT)
        ]
    )

    pygame.draw.polygon(
        screen,
        (45, 75, 110),
        [
            (950 + parallax, 290),
            (780 + parallax, HEIGHT),
            (1120 + parallax, HEIGHT)
        ]
    )
# ============================================================
# MIDDLE MOUNTAINS - CLEAN MAIN BACKGROUND
# ============================================================

def draw_middle_mountains(camera_x):

    parallax = camera_x * 0.28

    # --------------------------------------------------------
    # LARGE CLEAN MOUNTAIN RANGE
    # --------------------------------------------------------

    points = [(0, HEIGHT)]

    peaks = [
        (-100, 560),
        (180, 430),
        (480, 510),
        (760, 390),
        (1040, 470),
        (1320, 400)
    ]

    for x, y in peaks:

        points.append(
            (x - 150 + parallax, y + 130)
        )

        points.append(
            (x + parallax, y)
        )

        points.append(
            (x + 150 + parallax, y + 130)
        )

    points.append((WIDTH, HEIGHT))

    pygame.draw.polygon(
        screen,
        MOUNTAIN_BLUE,
        points
    )

    # --------------------------------------------------------
    # ONLY A FEW LARGE DARK ROCK FACES
    # --------------------------------------------------------

    rock_faces = [
        (180, 430, 120, 180),
        (760, 390, 140, 230),
        (1040, 470, 110, 170)
    ]

    for x, y, width, height in rock_faces:

        x += parallax

        # Dark left face
        pygame.draw.polygon(
            screen,
            MOUNTAIN_BLUE_DARK,
            [
                (x, y),
                (x - width, y + height),
                (x - 30, y + height + 80),
                (x + 10, y + 65)
            ]
        )

        # Lighter right face
        pygame.draw.polygon(
            screen,
            MOUNTAIN_BLUE_LIGHT,
            [
                (x, y),
                (x + width, y + height),
                (x + 35, y + height + 70),
                (x - 10, y + 65)
            ]
        )

    # --------------------------------------------------------
    # ONLY 3 SNOW CAPS
    # --------------------------------------------------------

    snow_peaks = [
        (180, 430, 55),
        (760, 390, 65),
        (1040, 470, 50)
    ]

    for x, y, size in snow_peaks:

        x += parallax

        # Shadow
        pygame.draw.polygon(
            screen,
            SNOW_SHADOW,
            [
                (x, y),
                (x - size, y + 85),
                (x + size, y + 85)
            ]
        )

        # Snow
        pygame.draw.polygon(
            screen,
            SNOW,
            [
                (x, y),
                (x - size // 2, y + 60),
                (x - 8, y + 45),
                (x + 12, y + 65),
                (x + size // 2, y + 55)
            ]
        )

    # --------------------------------------------------------
    # DARK BLUE LOWER MOUNTAIN BODY
    # --------------------------------------------------------
    # This ensures the mountain reaches the bottom.

    pygame.draw.polygon(
        screen,
        MOUNTAIN_BLUE,
        [
            (0, 560),
            (180, 500),
            (400, 560),
            (650, 500),
            (900, 550),
            (1200, 490),
            (1200, HEIGHT),
            (0, HEIGHT)
        ]
    )
    # --------------------------------------------------------
    # FEW CLEAN SNOW PEAKS
    # --------------------------------------------------------

    peaks = [
        (170, 350, 55),
        (480, 400, 48),
        (780, 320, 60),
        (1080, 375, 52)
    ]

    for x, y, size in peaks:

        # Shadow
        pygame.draw.polygon(
            screen,
            SNOW_SHADOW,
            [
                (x, y),
                (x - size, y + 90),
                (x + size, y + 90)
            ]
        )

        # Snow
        pygame.draw.polygon(
            screen,
            SNOW,
            [
                (x, y),
                (x - size // 2, y + 65),
                (x - 10, y + 48),
                (x + 12, y + 68),
                (x + size // 2, y + 58)
            ]
        )

    # --------------------------------------------------------
    # A FEW DARK BLUE RIDGES
    # --------------------------------------------------------

    random.seed(MOUNTAIN_SEED + 40)

    for _ in range(7):

        x = random.randint(
            -50,
            WIDTH + 50
        )

        peak_y = random.randint(
            430,
            550
        )

        width = random.randint(
            80,
            150
        )

        pygame.draw.polygon(
            screen,
            MOUNTAIN_BLUE_DARK,
            [
                (x, peak_y),
                (x - width, HEIGHT),
                (x + width, HEIGHT)
            ]
        )

    random.seed()

    # --------------------------------------------------------
    # FEW SMALL SNOW CAPS
    # --------------------------------------------------------

    peaks = [
        (180, 410, 45),
        (520, 455, 40),
        (850, 395, 48),
        (1120, 445, 42)
    ]

    for x, y, size in peaks:

        pygame.draw.polygon(
            screen,
            SNOW_SHADOW,
            [
                (x, y),
                (x - size, y + 70),
                (x + size, y + 70)
            ]
        )

        pygame.draw.polygon(
            screen,
            SNOW,
            [
                (x, y),
                (x - size // 2, y + 50),
                (x, y + 38),
                (x + size // 2, y + 50)
            ]
        )

    # --------------------------------------------------------
    # ROCK FACES
    # --------------------------------------------------------

    random.seed(MOUNTAIN_SEED)

    for _ in range(18):

        x = random.randint(
            -100,
            WIDTH + 100
        )

        peak_y = random.randint(
            240,
            470
        )

        width = random.randint(
            70,
            150
        )

        height = random.randint(
            110,
            230
        )

        color = random.choice([
            MOUNTAIN_BLUE_DARK,
            MOUNTAIN_BLUE_DARK,
            MOUNTAIN_BLUE,
            MOUNTAIN_BLUE_LIGHT,
            
        ])

        # Left rock face
        pygame.draw.polygon(
            screen,
            color,
            [
                (x, peak_y),
                (x - width, peak_y + height),
                (x - width // 3, peak_y + height - 35),
                (x + 5, peak_y + 75)
            ]
        )

        # Right shaded face
        pygame.draw.polygon(
            screen,
            MOUNTAIN_BLUE_DARK,
            [
                (x, peak_y),
                (x + width, peak_y + height),
                (x + width // 3, peak_y + height - 40),
                (x - 5, peak_y + 75)
            ]
        )

    random.seed()

    # --------------------------------------------------------
    # SNOW-CAPPED PEAKS
    # --------------------------------------------------------

    peaks = [
        (120, 290),
        (390, 350),
        (690, 270),
        (1000, 330),
        (1260, 260)
    ]

    for x, y in peaks:

        # Snow shadow
        pygame.draw.polygon(
            screen,
            SNOW_SHADOW,
            [
                (x, y),
                (x - 80, y + 125),
                (x - 40, y + 105),
                (x, y + 145),
                (x + 40, y + 105),
                (x + 85, y + 130)
            ]
        )

        # Main snow
        pygame.draw.polygon(
            screen,
            SNOW,
            [
                (x, y),
                (x - 48, y + 82),
                (x - 18, y + 65),
                (x + 5, y + 90),
                (x + 38, y + 70),
                (x + 55, y + 90)
            ]
        )

        # Snow shadow facet
        pygame.draw.polygon(
            screen,
            (165, 190, 210),
            [
                (x - 18, y + 65),
                (x, y + 145),
                (x - 40, y + 105)
            ]
        )

# ============================================================
# PROCEDURAL ROCK DETAILS
# ============================================================

def draw_rocky_details(camera_x, camera_y):

    random.seed(50)

    for _ in range(12):

        world_x = random.randint(
            0,
            WORLD_WIDTH
        )

        world_y = random.randint(
            900,
            3300
        )

        x = int(
            world_x - camera_x
        )

        y = int(
            world_y - camera_y
        )

        if not (
            -80 < x < WIDTH + 80
            and -80 < y < HEIGHT + 80
        ):
            continue

        size = random.randint(
            12,
            25
        )

        color = random.choice([
            MOUNTAIN_BLUE_DARK,
            MOUNTAIN_BLUE_DARK,
            MOUNTAIN_BLUE,
            MOUNTAIN_BLUE,
            MOUNTAIN_BLUE_LIGHT
            
        ])

        # Irregular rock
        pygame.draw.polygon(
            screen,
            color,
            [
                (x, y + size),
                (x + size * 0.25, y + size * 0.25),
                (x + size * 0.65, y),
                (x + size, y + size * 0.55),
                (x + size * 0.7, y + size)
            ]
        )

    random.seed()


# ============================================================
# BLUE FOG
# ============================================================

def draw_fog():

    fog = pygame.Surface(
        (WIDTH, HEIGHT),
        pygame.SRCALPHA
    )

    pygame.draw.ellipse(
        fog,
        (100, 145, 190, 25),
        (-100, 430, 700, 160)
    )

    pygame.draw.ellipse(
        fog,
        (130, 170, 210, 30),
        (400, 470, 800, 180)
    )

    pygame.draw.ellipse(
        fog,
        (150, 185, 220, 25),
        (850, 390, 600, 170)
    )

    screen.blit(
        fog,
        (0, 0)
    )


# ============================================================
# PINE TREE
# ============================================================

def draw_pine_tree(x, y, scale=1):

    trunk_width = max(
        4,
        int(9 * scale)
    )

    trunk_height = max(
        15,
        int(40 * scale)
    )

    pygame.draw.rect(
        screen,
        DARK_BROWN,
        (
            int(x - trunk_width / 2),
            int(y - trunk_height),
            trunk_width,
            trunk_height
        )
    )

    color = random.choice([
        VERY_DARK_GREEN,
        DARK_GREEN,
        DARK_GREEN  
    ])

    # Bottom leaves
    pygame.draw.polygon(
        screen,
        color,
        [
            (
                int(x),
                int(y - 105 * scale)
            ),
            (
                int(x - 40 * scale),
                int(y - 40 * scale)
            ),
            (
                int(x + 40 * scale),
                int(y - 40 * scale)
            )
        ]
    )

    # Middle leaves
    pygame.draw.polygon(
        screen,
        color,
        [
            (
                int(x),
                int(y - 75 * scale)
            ),
            (
                int(x - 50 * scale),
                int(y - 15 * scale)
            ),
            (
                int(x + 50 * scale),
                int(y - 15 * scale)
            )
        ]
    )


def draw_trees(camera_x, camera_y):

    random.seed(100)

    for _ in range(30):

        x_world = random.randint(
            0,
            WORLD_WIDTH
        )

        y_world = random.randint(
            2300,
            3200
        )

        x = int(
            x_world - camera_x
        )

        y = int(
            y_world - camera_y
        )

        if (
            -100 < x < WIDTH + 100
            and -150 < y < HEIGHT + 100
        ):

            draw_pine_tree(
                x,
                y,
                random.uniform(
                    0.45,
                    0.9
                )
            )

    random.seed()


# ============================================================
# PARTICLES
# ============================================================

particles = []


class Particle:

    def __init__(self, x, y, color):

        self.x = x
        self.y = y

        self.vx = random.uniform(
            -2,
            2
        )

        self.vy = random.uniform(
            -3,
            -0.5
        )

        self.life = random.randint(
            20,
            45
        )

        self.color = color

        self.size = random.randint(
            2,
            5
        )

    def update(self):

        self.x += self.vx
        self.y += self.vy

        self.vy += 0.1

        self.life -= 1

    def draw(
        self,
        camera_x,
        camera_y
    ):

        if self.life <= 0:
            return

        pygame.draw.circle(
            screen,
            self.color,
            (
                int(
                    self.x - camera_x
                ),
                int(
                    self.y - camera_y
                )
            ),
            self.size
        )


def create_particles(
    x,
    y,
    color,
    amount
):

    for _ in range(amount):

        particles.append(
            Particle(
                x,
                y,
                color
            )
        )


def update_particles():

    for p in particles[:]:

        p.update()

        if p.life <= 0:

            particles.remove(p)


def draw_particles(
    camera_x,
    camera_y
):

    for p in particles:

        p.draw(
            camera_x,
            camera_y
        )


# ============================================================
# PLATFORM
# ============================================================

class Platform:

    def __init__(
        self,
        x,
        y,
        width,
        height=35
    ):

        self.rect = pygame.Rect(
            x,
            y,
            width,
            height
        )

    def draw(
        self,
        camera_x,
        camera_y
    ):

        r = self.rect.move(
            -camera_x,
            -camera_y
        )

        # Shadow
        shadow = pygame.Rect(
            r.x + 8,
            r.y + 8,
            r.width,
            r.height
        )

        pygame.draw.rect(
            screen,
            MOUNTAIN_BLACK,
            shadow,
            border_radius=8
        )

        # Main rock
        pygame.draw.rect(
            screen,
            MOUNTAIN_BLUE_DARK,
            r,
            border_radius=8
        )

        # Brown rock face
        pygame.draw.polygon(
            screen,
            MOUNTAIN_BLUE,
            [
                (r.left, r.top + 8),
                (r.left + 35, r.top),
                (r.right - 20, r.top + 5),
                (r.right, r.bottom),
                (r.left, r.bottom)
            ]
        )

        # Dark lower part
        pygame.draw.polygon(
            screen,
            MOUNTAIN_BLACK,
            [
                (r.left, r.top + 22),
                (r.left + 60, r.top + 18),
                (r.right - 30, r.top + 20),
                (r.right, r.bottom),
                (r.left, r.bottom)
            ]
        )

        # Snow top
        snow_points = [
            (r.left, r.top + 8),
            (r.left + 35, r.top),
            (r.centerx, r.top + 5),
            (r.right - 35, r.top),
            (r.right, r.top + 8),
            (r.right - 10, r.top + 14),
            (r.left + 10, r.top + 14)
        ]

        pygame.draw.polygon(
            screen,
            SNOW,
            snow_points
        )

        # Cracks
        pygame.draw.line(
            screen,
            MOUNTAIN_BLACK,
            (
                r.left + 50,
                r.top + 18
            ),
            (
                r.left + 65,
                r.bottom - 5
            ),
            2
        )

        pygame.draw.line(
            screen,
            MOUNTAIN_BLACK,
            (
                r.centerx + 30,
                r.top + 17
            ),
            (
                r.centerx + 45,
                r.bottom - 5
            ),
            2
        )


# ============================================================
# PLAYER
# ============================================================

class Player:

    def __init__(
        self,
        x,
        y
    ):

        self.x = x
        self.y = y

        self.width = 42
        self.height = 62

        self.vx = 0
        self.vy = 0

        self.speed = 6
        self.jump_power = -15
        self.gravity = 0.72

        self.on_ground = False

        self.max_health = 100
        self.health = 100

        self.max_stamina = 100
        self.stamina = 100

        self.coins = 0
        self.potions = 1

        self.has_rope = True
        self.has_axe = True

        self.checkpoint_x = x
        self.checkpoint_y = y

        self.facing = 1

        self.invincible = 0

    @property
    def rect(self):

        return pygame.Rect(
            int(self.x),
            int(self.y),
            self.width,
            self.height
        )

    def jump(self):

        if (
            self.on_ground
            and self.stamina >= 12
        ):

            self.vy = self.jump_power

            self.on_ground = False

            self.stamina -= 12

            create_particles(
                self.x + self.width / 2,
                self.y + self.height,
                SNOW,
                8
            )

    def take_damage(self, amount):

        if self.invincible > 0:
            return

        self.health -= amount

        self.invincible = 60

        create_particles(
            self.x + self.width / 2,
            self.y + self.height / 2,
            RED,
            12
        )

        if self.health <= 0:

            self.health = 100

            self.respawn()

    def respawn(self):

        self.x = self.checkpoint_x
        self.y = self.checkpoint_y

        self.vx = 0
        self.vy = 0

    def use_potion(self):

        if (
            self.potions > 0
            and self.health < self.max_health
        ):

            self.health = min(
                self.max_health,
                self.health + 40
            )

            self.stamina = min(
                self.max_stamina,
                self.stamina + 40
            )

            self.potions -= 1

            create_particles(
                self.x + self.width / 2,
                self.y + self.height / 2,
                PURPLE,
                20
            )

    def update(self, platforms):

        keys = pygame.key.get_pressed()

        self.vx = 0

        # Movement
        if (
            keys[pygame.K_a]
            or keys[pygame.K_LEFT]
        ):

            self.vx = -self.speed
            self.facing = -1

        if (
            keys[pygame.K_d]
            or keys[pygame.K_RIGHT]
        ):

            self.vx = self.speed
            self.facing = 1

        # Sprint
        if (
            keys[pygame.K_LSHIFT]
            and self.stamina > 0
            and self.vx != 0
        ):

            self.vx *= 1.45
            self.stamina -= 0.55

        else:

            self.stamina = min(
                self.max_stamina,
                self.stamina + 0.3
            )

        # Gravity
        self.vy += self.gravity

        # Horizontal
        self.x += self.vx

        self.x = clamp(
            self.x,
            0,
            WORLD_WIDTH - self.width
        )

        # Vertical
        old_bottom = (
            self.y + self.height
        )

        self.y += self.vy

        self.on_ground = False

        # Platform collision
        for platform in platforms:

            r = platform.rect

            if (
                self.rect.right > r.left
                and self.rect.left < r.right
                and self.vy >= 0
                and old_bottom <= r.top + 6
                and self.y + self.height >= r.top
            ):

                self.y = (
                    r.top - self.height
                )

                self.vy = 0

                self.on_ground = True

        if self.invincible > 0:

            self.invincible -= 1

        # Fell
        if self.y > WORLD_HEIGHT + 250:

            self.take_damage(25)

            self.respawn()

    def draw(
        self,
        camera_x,
        camera_y
    ):

        if (
            self.invincible > 0
            and self.invincible % 10 < 5
        ):

            return

        x = int(
            self.x - camera_x
        )

        y = int(
            self.y - camera_y
        )

        # Backpack
        pygame.draw.rect(
            screen,
            DARK_BLUE,
            (
                x - 8,
                y + 20,
                14,
                29
            ),
            border_radius=5
        )

        # Body
        pygame.draw.rect(
            screen,
            (150, 45, 45),
            (
                x + 5,
                y + 22,
                32,
                29
            ),
            border_radius=8
        )

        # Jacket highlight
        pygame.draw.line(
            screen,
            (220, 80, 70),
            (
                x + 20,
                y + 25
            ),
            (
                x + 20,
                y + 46
            ),
            3
        )

        # Head
        pygame.draw.circle(
            screen,
            (225, 175, 135),
            (
                x + 21,
                y + 13
            ),
            13
        )

        # Hair
        pygame.draw.arc(
            screen,
            (35, 28, 25),
            (
                x + 8,
                y + 2,
                26,
                18
            ),
            math.pi,
            math.pi * 2,
            5
        )

        # Helmet
        pygame.draw.arc(
            screen,
            ORANGE,
            (
                x + 5,
                y - 3,
                32,
                22
            ),
            math.pi,
            math.pi * 2,
            5
        )

        # Legs
        pygame.draw.rect(
            screen,
            DARK_BLUE,
            (
                x + 8,
                y + 49,
                11,
                13
            ),
            border_radius=4
        )

        pygame.draw.rect(
            screen,
            DARK_BLUE,
            (
                x + 25,
                y + 49,
                11,
                13
            ),
            border_radius=4
        )

        # Axe
        if self.has_axe:

            ax = (
                x + 45
                if self.facing == 1
                else x - 5
            )

            pygame.draw.line(
                screen,
                DARK_BROWN,
                (
                    ax,
                    y + 25
                ),
                (
                    ax,
                    y + 48
                ),
                4
            )

            pygame.draw.arc(
                screen,
                LIGHT_GRAY,
                (
                    ax - 8,
                    y + 15,
                    17,
                    16
                ),
                math.pi,
                math.pi * 2,
                3
            )


# ============================================================
# COIN
# ============================================================

class Coin:

    def __init__(
        self,
        x,
        y
    ):

        self.x = x
        self.y = y

        self.collected = False

        self.angle = random.random() * 6

    def update(self):

        self.angle += 0.08

    def draw(
        self,
        camera_x,
        camera_y
    ):

        if self.collected:
            return

        x = int(
            self.x - camera_x
        )

        y = int(
            self.y
            - camera_y
            + math.sin(self.angle) * 4
        )

        pygame.draw.circle(
            screen,
            (150, 115, 30),
            (x, y),
            16
        )

        pygame.draw.circle(
            screen,
            GOLD,
            (x, y),
            11
        )

        pygame.draw.circle(
            screen,
            YELLOW,
            (
                x - 3,
                y - 3
            ),
            5
        )


# ============================================================
# POTION
# ============================================================

class Potion:

    def __init__(
        self,
        x,
        y
    ):

        self.x = x
        self.y = y

        self.collected = False

        self.angle = 0

    def update(self):

        self.angle += 0.05

    def draw(
        self,
        camera_x,
        camera_y
    ):

        if self.collected:
            return

        x = int(
            self.x - camera_x
        )

        y = int(
            self.y
            - camera_y
            + math.sin(self.angle) * 4
        )

        # Glow
        pygame.draw.circle(
            screen,
            (100, 60, 160),
            (x, y),
            20
        )

        # Bottle
        pygame.draw.rect(
            screen,
            PURPLE,
            (
                x - 9,
                y - 8,
                18,
                22
            ),
            border_radius=5
        )

        # Liquid
        pygame.draw.rect(
            screen,
            (190, 90, 225),
            (
                x - 6,
                y - 1,
                12,
                12
            ),
            border_radius=3
        )

        # Cap
        pygame.draw.rect(
            screen,
            DARK_BROWN,
            (
                x - 6,
                y - 15,
                12,
                7
            )
        )


# ============================================================
# CHECKPOINT
# ============================================================

class Checkpoint:

    def __init__(
        self,
        x,
        y
    ):

        self.x = x
        self.y = y

        self.activated = False

    def activate(self, player):

        if not self.activated:

            self.activated = True

            player.checkpoint_x = self.x

            player.checkpoint_y = (
                self.y - player.height
            )

            create_particles(
                self.x,
                self.y,
                YELLOW,
                25
            )

    def draw(
        self,
        camera_x,
        camera_y
    ):

        x = int(
            self.x - camera_x
        )

        y = int(
            self.y - camera_y
        )

        # Pole
        pygame.draw.rect(
            screen,
            DARK_BROWN,
            (
                x - 3,
                y - 80,
                6,
                80
            )
        )

        # Flag
        color = (
            GREEN
            if self.activated
            else RED
        )

        pygame.draw.polygon(
            screen,
            color,
            [
                (x, y - 80),
                (x + 55, y - 62),
                (x, y - 45)
            ]
        )

        # Light
        pygame.draw.circle(
            screen,
            YELLOW,
            (
                x,
                y - 90
            ),
            6
        )


# ============================================================
# FALLING ROCK
# ============================================================

class FallingRock:

    def __init__(
        self,
        x,
        y
    ):

        self.x = x
        self.y = y

        self.radius = random.randint(
            13,
            22
        )

        self.speed = random.uniform(
            3,
            6
        )

        self.active = True

    def update(self):

        self.y += self.speed

        self.speed += 0.08

        if self.y > WORLD_HEIGHT + 200:

            self.active = False

    def draw(
        self,
        camera_x,
        camera_y
    ):

        if not self.active:
            return

        x = int(
            self.x - camera_x
        )

        y = int(
            self.y - camera_y
        )

        pygame.draw.circle(
            screen,
            MOUNTAIN_BLACK,
            (
                x,
                y
            ),
            self.radius
        )

        pygame.draw.circle(
            screen,
            ROCK,
            (
                x - 5,
                y - 5
            ),
            max(
                3,
                self.radius // 3
            )
        )


# ============================================================
# PLATFORM CREATION
# ============================================================

def create_platforms():

    return [

        Platform(
            100,
            3250,
            430
        ),

        Platform(
            610,
            3130,
            320
        ),

        Platform(
            1000,
            3010,
            320
        ),

        Platform(
            1400,
            2890,
            330
        ),

        Platform(
            1810,
            2770,
            320
        ),

        Platform(
            2200,
            2650,
            300
        ),

        Platform(
            2580,
            2530,
            340
        ),

        Platform(
            3000,
            2410,
            300
        ),

        Platform(
            3370,
            2290,
            330
        ),

        Platform(
            3770,
            2170,
            320
        ),

        Platform(
            4160,
            2050,
            330
        ),

        Platform(
            4550,
            1930,
            300
        ),

        Platform(
            4910,
            1810,
            320
        ),

        Platform(
            5300,
            1690,
            330
        ),

        Platform(
            5700,
            1570,
            300
        ),

        Platform(
            5300,
            1450,
            260
        ),

        Platform(
            4900,
            1330,
            280
        ),

        Platform(
            4500,
            1210,
            280
        ),

        Platform(
            4100,
            1090,
            300
        ),

        Platform(
            3700,
            970,
            280
        ),

        Platform(
            3300,
            850,
            300
        ),

        Platform(
            2900,
            730,
            280
        ),

        Platform(
            2500,
            610,
            300
        ),

        Platform(
            2100,
            490,
            320
        ),

        Platform(
            1600,
            370,
            650
        )
    ]


# ============================================================
# COINS
# ============================================================

def create_coins():

    positions = [

        (250, 3185),
        (760, 3065),
        (1150, 2945),
        (1540, 2825),

        (1950, 2705),
        (2340, 2585),
        (2720, 2465),
        (3140, 2345),

        (3510, 2225),
        (3910, 2105),
        (4300, 1985),
        (4690, 1865),

        (5050, 1745),
        (5440, 1625),
        (5840, 1505),

        (5410, 1385),
        (5010, 1265),
        (4610, 1145),
        (4210, 1025),

        (3810, 905),
        (3410, 785),
        (3010, 665),
        (2610, 545),
        (2210, 425),

        (1800, 305)
    ]

    return [
        Coin(x, y)
        for x, y in positions
    ]


# ============================================================
# POTIONS
# ============================================================

def create_potions():

    positions = [

        (700, 3070),
        (2670, 2470),
        (4650, 1870),
        (5000, 1270),
        (3010, 670)
    ]

    return [
        Potion(x, y)
        for x, y in positions
    ]


# ============================================================
# CHECKPOINTS
# ============================================================

def create_checkpoints():

    positions = [

        (1420, 2890),
        (3000, 2410),
        (4550, 1930),
        (4100, 1090),
        (2500, 610)
    ]

    return [
        Checkpoint(x, y)
        for x, y in positions
    ]


# ============================================================
# CAMERA
# ============================================================

def update_camera(
    player,
    camera_x,
    camera_y
):

    target_x = (
        player.x
        + player.width / 2
        - WIDTH / 2
    )

    target_y = (
        player.y
        + player.height / 2
        - HEIGHT / 2
    )

    target_x = clamp(
        target_x,
        0,
        WORLD_WIDTH - WIDTH
    )

    target_y = clamp(
        target_y,
        0,
        WORLD_HEIGHT - HEIGHT
    )

    camera_x += (
        target_x - camera_x
    ) * 0.08

    camera_y += (
        target_y - camera_y
    ) * 0.08

    return camera_x, camera_y


# ============================================================
# ROCK SPAWN
# ============================================================

def spawn_rocks(
    player,
    rocks
):

    if random.random() < 0.012:

        x = (
            player.x
            + random.randint(
                -300,
                500
            )
        )

        y = (
            player.y
            - random.randint(
                300,
                550
            )
        )

        x = clamp(
            x,
            0,
            WORLD_WIDTH
        )

        rocks.append(
            FallingRock(
                x,
                y
            )
        )


def update_rocks(
    player,
    rocks
):

    for rock in rocks[:]:

        rock.update()

        if not rock.active:

            rocks.remove(rock)

            continue

        rock_rect = pygame.Rect(
            rock.x - rock.radius,
            rock.y - rock.radius,
            rock.radius * 2,
            rock.radius * 2
        )

        if player.rect.colliderect(
            rock_rect
        ):

            player.take_damage(20)

            create_particles(
                rock.x,
                rock.y,
                ORANGE,
                10
            )

            rock.active = False


# ============================================================
# COLLECT ITEMS
# ============================================================

def handle_collectibles(
    player,
    coins,
    potions,
    checkpoints
):

    center_x = player.rect.centerx
    center_y = player.rect.centery

    # Coins
    for coin in coins:

        if coin.collected:
            continue

        distance = math.hypot(
            center_x - coin.x,
            center_y - coin.y
        )

        if distance < 42:

            coin.collected = True

            player.coins += 1

            create_particles(
                coin.x,
                coin.y,
                YELLOW,
                12
            )

    # Potions
    for potion in potions:

        if potion.collected:
            continue

        distance = math.hypot(
            center_x - potion.x,
            center_y - potion.y
        )

        if distance < 42:

            potion.collected = True

            player.potions += 1

            create_particles(
                potion.x,
                potion.y,
                PURPLE,
                15
            )

    # Checkpoints
    for checkpoint in checkpoints:

        distance = math.hypot(
            center_x - checkpoint.x,
            center_y - checkpoint.y
        )

        if distance < 60:

            checkpoint.activate(
                player
            )


# ============================================================
# HUD BAR
# ============================================================

def draw_bar(
    x,
    y,
    width,
    height,
    value,
    maximum,
    color
):

    pygame.draw.rect(
        screen,
        MOUNTAIN_BLACK,
        (
            x,
            y,
            width,
            height
        ),
        border_radius=6
    )

    fill = int(
        width * value / maximum
    )

    pygame.draw.rect(
        screen,
        color,
        (
            x,
            y,
            fill,
            height
        ),
        border_radius=6
    )

    pygame.draw.rect(
        screen,
        LIGHT_GRAY,
        (
            x,
            y,
            width,
            height
        ),
        2,
        border_radius=6
    )


# ============================================================
# HUD
# ============================================================

def draw_hud(player):

    # Main HUD
    pygame.draw.rect(
        screen,
        (8, 20, 45),
        (
            15,
            15,
            310,
            145
        ),
        border_radius=15
    )

    pygame.draw.rect(
        screen,
        BLUE,
        (
            15,
            15,
            310,
            145
        ),
        2,
        border_radius=15
    )

    draw_text(
        "MOUNTAIN CLIMBER",
        font_medium,
        WHITE,
        30,
        27
    )

    draw_text(
        "HEALTH",
        font_small,
        WHITE,
        30,
        62
    )

    draw_bar(
        105,
        63,
        190,
        16,
        player.health,
        player.max_health,
        RED
    )

    draw_text(
        "STAMINA",
        font_small,
        WHITE,
        30,
        91
    )

    draw_bar(
        105,
        92,
        190,
        16,
        player.stamina,
        player.max_stamina,
        GREEN
    )

    draw_text(
        "Coins: " + str(player.coins),
        font_medium,
        YELLOW,
        30,
        120
    )

    # Equipment HUD
    pygame.draw.rect(
        screen,
        (8, 20, 45),
        (
            WIDTH - 280,
            15,
            265,
            145
        ),
        border_radius=15
    )

    pygame.draw.rect(
        screen,
        BLUE,
        (
            WIDTH - 280,
            15,
            265,
            145
        ),
        2,
        border_radius=15
    )

    draw_text(
        "EQUIPMENT",
        font_medium,
        WHITE,
        WIDTH - 260,
        27
    )

    draw_text(
        "Potion: " + str(player.potions),
        font_small,
        PURPLE,
        WIDTH - 260,
        63
    )

    draw_text(
        "Rope: "
        + (
            "Available"
            if player.has_rope
            else "Used"
        ),
        font_small,
        ORANGE,
        WIDTH - 260,
        91
    )

    draw_text(
        "Axe: "
        + (
            "Equipped"
            if player.has_axe
            else "None"
        ),
        font_small,
        LIGHT_GRAY,
        WIDTH - 260,
        119
    )

    # Bottom controls
    pygame.draw.rect(
        screen,
        (8, 20, 45),
        (
            15,
            HEIGHT - 55,
            610,
            40
        ),
        border_radius=10
    )

    draw_text(
        "A/D Move   SPACE Jump   SHIFT Sprint   E Potion   I Inventory",
        font_small,
        WHITE,
        28,
        HEIGHT - 43
    )


# ============================================================
# INVENTORY
# ============================================================

def draw_inventory(player):

    overlay = pygame.Surface(
        (WIDTH, HEIGHT),
        pygame.SRCALPHA
    )

    overlay.fill(
        (3, 8, 25, 225)
    )

    screen.blit(
        overlay,
        (0, 0)
    )

    box = pygame.Rect(
        WIDTH // 2 - 310,
        HEIGHT // 2 - 220,
        620,
        440
    )

    pygame.draw.rect(
        screen,
        (15, 35, 65),
        box,
        border_radius=20
    )

    pygame.draw.rect(
        screen,
        BLUE,
        box,
        3,
        border_radius=20
    )

    draw_text(
        "INVENTORY",
        font_title,
        WHITE,
        WIDTH // 2,
        HEIGHT // 2 - 165,
        center=True
    )

    draw_text(
        "Coins: " + str(player.coins),
        font_large,
        YELLOW,
        WIDTH // 2,
        HEIGHT // 2 - 90,
        center=True
    )

    draw_text(
        "Health Potions: "
        + str(player.potions),
        font_medium,
        PURPLE,
        WIDTH // 2,
        HEIGHT // 2 - 30,
        center=True
    )

    draw_text(
        "Climbing Rope: "
        + (
            "Available"
            if player.has_rope
            else "Used"
        ),
        font_medium,
        ORANGE,
        WIDTH // 2,
        HEIGHT // 2 + 20,
        center=True
    )

    draw_text(
        "Climbing Axe: "
        + (
            "Equipped"
            if player.has_axe
            else "None"
        ),
        font_medium,
        LIGHT_GRAY,
        WIDTH // 2,
        HEIGHT // 2 + 70,
        center=True
    )

    draw_text(
        "Press I to close",
        font_medium,
        WHITE,
        WIDTH // 2,
        HEIGHT // 2 + 140,
        center=True
    )


# ============================================================
# START SCREEN
# ============================================================

def draw_start_screen():

    draw_sky()

    draw_moon()

    draw_far_mountains(0)

    draw_middle_mountains(0)

    draw_fog()

    draw_text(
        "MOUNTAIN",
        font_title,
        WHITE,
        WIDTH // 2,
        170,
        center=True
    )

    draw_text(
        "CLIMBER",
        font_title,
        BLUE_LIGHT,
        WIDTH // 2,
        240,
        center=True
    )

    draw_text(
        "BLUE SUMMIT",
        font_large,
        SNOW,
        WIDTH // 2,
        310,
        center=True
    )

    draw_text(
        "Reach the summit. Survive the mountain.",
        font_medium,
        WHITE,
        WIDTH // 2,
        370,
        center=True
    )

    button = pygame.Rect(
        WIDTH // 2 - 145,
        450,
        290,
        70
    )

    pygame.draw.rect(
        screen,
        BLUE_DARK,
        button,
        border_radius=15
    )

    pygame.draw.rect(
        screen,
        BLUE_LIGHT,
        button,
        2,
        border_radius=15
    )

    draw_text(
        "PRESS ENTER",
        font_large,
        WHITE,
        WIDTH // 2,
        485,
        center=True
    )


# ============================================================
# PAUSE
# ============================================================

def draw_pause():

    overlay = pygame.Surface(
        (WIDTH, HEIGHT),
        pygame.SRCALPHA
    )

    overlay.fill(
        (0, 5, 25, 150)
    )

    screen.blit(
        overlay,
        (0, 0)
    )

    draw_text(
        "PAUSED",
        font_title,
        WHITE,
        WIDTH // 2,
        HEIGHT // 2 - 50,
        center=True
    )

    draw_text(
        "Press ESC to continue",
        font_medium,
        WHITE,
        WIDTH // 2,
        HEIGHT // 2 + 30,
        center=True
    )


# ============================================================
# VICTORY
# ============================================================

def draw_victory(player):

    overlay = pygame.Surface(
        (WIDTH, HEIGHT),
        pygame.SRCALPHA
    )

    overlay.fill(
        (3, 12, 30, 225)
    )

    screen.blit(
        overlay,
        (0, 0)
    )

    draw_text(
        "SUMMIT REACHED",
        font_title,
        YELLOW,
        WIDTH // 2,
        170,
        center=True
    )

    draw_text(
        "You conquered the mountain!",
        font_large,
        WHITE,
        WIDTH // 2,
        260,
        center=True
    )

    draw_text(
        "Coins collected: "
        + str(player.coins),
        font_medium,
        YELLOW,
        WIDTH // 2,
        330,
        center=True
    )

    draw_text(
        "Press R to climb again",
        font_medium,
        GREEN,
        WIDTH // 2,
        430,
        center=True
    )

    draw_text(
        "Press ESC to exit",
        font_small,
        WHITE,
        WIDTH // 2,
        485,
        center=True
    )


# ============================================================
# RESET
# ============================================================

def reset_game():

    global particles

    particles.clear()

    platforms = create_platforms()

    coins = create_coins()

    potions = create_potions()

    checkpoints = create_checkpoints()

    rocks = []

    player = Player(
        170,
        3250 - 62
    )

    return (
        player,
        platforms,
        coins,
        potions,
        checkpoints,
        rocks
    )


# ============================================================
# MAIN
# ============================================================

def main():

    (
        player,
        platforms,
        coins,
        potions,
        checkpoints,
        rocks
    ) = reset_game()

    camera_x = 0
    camera_y = 0

    game_state = "menu"

    inventory_open = False

    running = True

    while running:

        clock.tick(FPS)

        # ====================================================
        # EVENTS
        # ====================================================

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                running = False

            if event.type == pygame.KEYDOWN:

                # MENU
                if game_state == "menu":

                    if event.key == pygame.K_RETURN:

                        game_state = "playing"

                # PLAYING
                elif game_state == "playing":

                    if event.key == pygame.K_SPACE:

                        player.jump()

                    elif event.key == pygame.K_e:

                        player.use_potion()

                    elif event.key == pygame.K_i:

                        inventory_open = not inventory_open

                    elif event.key == pygame.K_ESCAPE:

                        game_state = "paused"

                # PAUSED
                elif game_state == "paused":

                    if event.key == pygame.K_ESCAPE:

                        game_state = "playing"

                # VICTORY
                elif game_state == "victory":

                    if event.key == pygame.K_r:

                        (
                            player,
                            platforms,
                            coins,
                            potions,
                            checkpoints,
                            rocks
                        ) = reset_game()

                        camera_x = 0
                        camera_y = 0

                        inventory_open = False

                        game_state = "playing"

                    elif event.key == pygame.K_ESCAPE:

                        running = False

        # ====================================================
        # MENU
        # ====================================================

        if game_state == "menu":

            draw_start_screen()

            pygame.display.flip()

            continue

        # ====================================================
        # PLAYING
        # ====================================================

        if game_state == "playing":

            if not inventory_open:

                player.update(
                    platforms
                )

                handle_collectibles(
                    player,
                    coins,
                    potions,
                    checkpoints
                )

                for coin in coins:

                    coin.update()

                for potion in potions:

                    potion.update()

                spawn_rocks(
                    player,
                    rocks
                )

                update_rocks(
                    player,
                    rocks
                )

                update_particles()

                camera_x, camera_y = update_camera(
                    player,
                    camera_x,
                    camera_y
                )

                # Summit
                if (
                    player.y < 300
                    and 1500 < player.x < 2300
                ):

                    game_state = "victory"

            # =================================================
            # DRAW WORLD
            # =================================================

            draw_sky()

            draw_moon()

            draw_far_mountains(
                camera_x
            )

            draw_middle_mountains(
                camera_x
            )

            draw_rocky_details(
                camera_x,
                camera_y
            )

         #   draw_trees(
        #        camera_x,
          #      camera_y
         #   )

            # Platforms
            for platform in platforms:

                r = platform.rect

                if (
                    r.right > camera_x
                    and r.left < camera_x + WIDTH
                    and r.bottom > camera_y
                    and r.top < camera_y + HEIGHT
                ):

                    platform.draw(
                        camera_x,
                        camera_y
                    )

            # Coins
            for coin in coins:

                coin.draw(
                    camera_x,
                    camera_y
                )

            # Potions
            for potion in potions:

                potion.draw(
                    camera_x,
                    camera_y
                )

            # Checkpoints
            for checkpoint in checkpoints:

                checkpoint.draw(
                    camera_x,
                    camera_y
                )

            # Falling rocks
            for rock in rocks:

                rock.draw(
                    camera_x,
                    camera_y
                )

            # Player
            player.draw(
                camera_x,
                camera_y
            )

            # Particles
            draw_particles(
                camera_x,
                camera_y
            )

            # Fog
            draw_fog()

            # =================================================
            # SUMMIT SIGN
            # =================================================

            summit_x = int(
                1900 - camera_x
            )

            summit_y = int(
                300 - camera_y
            )

            if (
                -200 < summit_x < WIDTH + 200
                and -100 < summit_y < HEIGHT + 100
            ):

                pygame.draw.rect(
                    screen,
                    DARK_BROWN,
                    (
                        summit_x - 5,
                        summit_y,
                        10,
                        90
                    )
                )

                pygame.draw.polygon(
                    screen,
                    BLUE,
                    [
                        (
                            summit_x,
                            summit_y
                        ),
                        (
                            summit_x + 135,
                            summit_y + 25
                        ),
                        (
                            summit_x,
                            summit_y + 52
                        )
                    ]
                )

                draw_text(
                    "SUMMIT",
                    font_medium,
                    WHITE,
                    summit_x + 60,
                    summit_y + 20,
                    center=True
                )

            # HUD
            draw_hud(player)

            if inventory_open:

                draw_inventory(
                    player
                )

            pygame.display.flip()

        # ====================================================
        # PAUSED
        # ====================================================

        elif game_state == "paused":

            draw_sky()

            draw_moon()

            draw_far_mountains(
                camera_x
            )

            draw_middle_mountains(
                camera_x
            )

            draw_rocky_details(
                camera_x,
                camera_y
            )

            for platform in platforms:

                platform.draw(
                    camera_x,
                    camera_y
                )

            player.draw(
                camera_x,
                camera_y
            )

            draw_hud(player)

            draw_pause()

            pygame.display.flip()

        # ====================================================
        # VICTORY
        # ====================================================

        elif game_state == "victory":

            draw_sky()

            draw_moon()

            draw_far_mountains(
                camera_x
            )

            draw_middle_mountains(
                camera_x
            )

            draw_victory(
                player
            )

            pygame.display.flip()

    pygame.quit()

    sys.exit()


# ============================================================
# START
# ============================================================

if __name__ == "__main__":
    main()


