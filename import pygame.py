import pygame
import math
import sys

pygame.init()
WIDTH, HEIGHT = 800, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Human-Robot Collaboration - Safe System")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 18, bold=True)
small_font = pygame.font.SysFont("Arial", 14)

# Colors
WHITE = (255, 255, 255)
BLUE = (30, 144, 255)
RED = (255, 60, 60)
GREEN = (0, 200, 100)
YELLOW = (255, 200, 0)
GREY = (200, 200, 200)
BLACK = (0, 0, 0)
COOL_COLOR = (150, 220, 255)

# Robot position
robot_x, robot_y = 400, 250
robot_speed = 2.0
temp = 35.0  # Starting temp
mode = "WORKING"
cooling_zone = pygame.Rect(20, 20, 140, 100)

# Human position (mouse control)
human_x, human_y = 100, 400

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    human_x, human_y = pygame.mouse.get_pos()

    # Distance calculation
    dist = math.hypot(robot_x - human_x, robot_y - human_y)

    # --- LOGIC 1: Safe Distance & Speed ---
    if dist > 150:
        target_speed = 2.0
        status = "FULL SPEED - Safe"
        status_color = GREEN
    elif dist > 80:
        target_speed = 0.8
        status = "SLOW SPEED - Human Near!"
        status_color = YELLOW
    else:
        target_speed = 0
        status = "STOP! Human Too Close!"
        status_color = RED

    # --- LOGIC 2: Heat Management ---
    # Kaj korle gorom hobe, theme thakle thanda hobe
    if mode == "WORKING":
        temp += 0.05 * target_speed + 0.02
        if temp > 95:
            mode = "GO TO COOLING"
            status = "OVERHEATED! Going to Cooling"
            status_color = RED
        elif temp > 85:
            target_speed = target_speed * 0.5
            status = "HOT! Auto Slow Down"
            status_color = YELLOW
    elif mode == "GO TO COOLING":
        # Cooling zone er dike jao
        dx = (cooling_zone.centerx - robot_x)
        dy = (cooling_zone.centery - robot_y)
        d = math.hypot(dx, dy)
        if d > 5:
            robot_x += (dx/d) * 2
            robot_y += (dy/d) * 2
        else:
            mode = "COOLING"
        temp -= 0.05
    elif mode == "COOLING":
        temp -= 0.3
        status = "COOLING... Please Wait"
        status_color = BLUE
        if temp < 40:
            mode = "WORKING"
            status = "Cooled! Back to Work"
    
    # Robot movement (Working mode e left-right move korbe)
    if mode == "WORKING":
        robot_x += target_speed
        if robot_x > 750 or robot_x < 200:
            robot_speed = -robot_speed
            # Simple bounce logic
            robot_x += target_speed * 2
        # Actually move with speed
        robot_x += target_speed * 0.5
        if robot_x > 750:
            robot_x = 200

    # --- DRAWING ---
    screen.fill(WHITE)
    
    # Cooling Zone
    pygame.draw.rect(screen, COOL_COLOR, cooling_zone, border_radius=10)
    pygame.draw.rect(screen, BLUE, cooling_zone, 3, border_radius=10)
    text = small_font.render("COOLING AREA", True, BLACK)
    screen.blit(text, (35, 60))
    pygame.draw.rect(screen, (0,150,255), (35, 85, 110, 10))
    
    # Safe Zone Circle around Robot
    pygame.draw.circle(screen, (255, 230, 230), (int(robot_x), int(robot_y)), 80, 2)
    pygame.draw.circle(screen, (230, 255, 230), (int(robot_x), int(robot_y)), 150, 1)

    # Distance Line
    pygame.draw.line(screen, GREY, (robot_x, robot_y), (human_x, human_y), 2)

    # Human - Blue Circle (Mouse)
    pygame.draw.circle(screen, BLUE, (human_x, human_y), 20)
    text = small_font.render("HUMAN", True, BLACK)
    screen.blit(text, (human_x - 25, human_y + 25))

    # Robot - Red Square
    pygame.draw.rect(screen, RED, (robot_x-25, robot_y-25, 50, 50), border_radius=8)
    text = small_font.render("ROBOT", True, WHITE)
    screen.blit(text, (robot_x - 22, robot_y - 8))

    # Dashboard
    pygame.draw.rect(screen, BLACK, (0, 430, 800, 70))
    info1 = font.render(f"Distance: {int(dist)} cm | Speed: {target_speed:.1f} | Temp: {int(temp)} C", True, WHITE)
    info2 = font.render(f"Status: {status} | Mode: {mode}", True, status_color)
    screen.blit(info1, (20, 440))
    screen.blit(info2, (20, 465))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()