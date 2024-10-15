import pygame
import sys
import Camera
import math

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
BACKGROUND_COLOR = (255, 255, 255)
multiplier = 1


def addCOSx(x):
    return x+SCREEN_WIDTH/2
def addCOSy(y):
    return SCREEN_HEIGHT/2-y

xLine = [[0,0,0],[50,0,0]]
yLine = [[0,0,0],[0,50,0]]
zLine = [[0,0,0],[0,0,50]]

floatingLine = [[50,-50,50],[-50, 50, -50]]

ab = [[-25,-25,-25],[-25, 25, -25]]
ac = [[-25,-25,-25],[-25, -25, 25]]
cd = [[-25, -25, 25],[-25, 25, 25]]
bd = [[-25, 25, -25],[-25, 25, 25]]

points = [
    {"corner": 1, "x": -25, "y": -25, "z": -25,"x'": -25, "y'": -25, "z'": -25, "radius": 3, "dragging": False},
    {"corner": 2, "x": -25, "y": 25,  "z": -25, "x'": -25, "y'": 25,  "z'": -25, "radius": 3, "dragging": False},
    {"corner": 3, "x": -25, "y": -25, "z": 25, "x'": -25, "y'": -25, "z'": 25, "radius": 3, "dragging": False},
    {"corner": 4, "x": -25, "y": 25,  "z": 25, "x'": -25, "y'": 25,  "z'": 25,  "radius": 3, "dragging": False},
    {"corner": 0, "x": 30, "y": 30,  "z": 30, "x'": 30, "y'": 30,  "z'": 30,  "radius": 3, "dragging": False},
    ]


def line2render(line,color):
    start = c.displayPosition(line[0][0],line[0][1],line[0][2])
    end = c.displayPosition(line[1][0],line[1][1],line[1][2])
    pygame.draw.line(screen, color, (addCOSx(start[0]), addCOSy(start[1])),(addCOSx(end[0]), addCOSy(end[1])))

def point2render(point,color, radius):
    center = c.displayPosition(point[0], point[1], point[2])
    pygame.draw.circle(screen, color, (addCOSx(center[0]),addCOSy(center[1])), radius)

def render_cube(center_x, center_y, center_z, side_length, color):
    # Half the side length for easier calculations
    hs = side_length / 2

    # Define the 8 vertices of the cube relative to the center
    vertices = [
        [center_x - hs, center_y - hs, center_z - hs],  # Vertex 0
        [center_x + hs, center_y - hs, center_z - hs],  # Vertex 1
        [center_x + hs, center_y + hs, center_z - hs],  # Vertex 2
        [center_x - hs, center_y + hs, center_z - hs],  # Vertex 3
        [center_x - hs, center_y - hs, center_z + hs],  # Vertex 4
        [center_x + hs, center_y - hs, center_z + hs],  # Vertex 5
        [center_x + hs, center_y + hs, center_z + hs],  # Vertex 6
        [center_x - hs, center_y + hs, center_z + hs],  # Vertex 7
    ]

    # Define the 12 edges of the cube by specifying pairs of vertices
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 0),  # Bottom square
        (4, 5), (5, 6), (6, 7), (7, 4),  # Top square
        (0, 4), (1, 5), (2, 6), (3, 7)   # Vertical edges
    ]

    # Convert 3D vertices to 2D screen positions
    projected_vertices = []
    for vertex in vertices:
        projected = c.displayPosition(vertex[0], vertex[1], vertex[2])
        projected_vertices.append((addCOSx(projected[0]), addCOSy(projected[1])))

    # Draw each edge
    for edge in edges:
        start_pos = projected_vertices[edge[0]]
        end_pos = projected_vertices[edge[1]]
        pygame.draw.line(screen, color, start_pos, end_pos, 1)  # 1 is the line thickness

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Scene')

c = Camera.camera()

# Set up font
font = pygame.font.SysFont(None, 36)

#Screen coordinaites for selected object
loc = [0,0]

# Main game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Check if a number key is pressed
        if event.type == pygame.KEYDOWN:
            if pygame.K_0 <= event.key <= pygame.K_9:
                multiplier = event.key - pygame.K_0  # Get the numeric value from the key
                if multiplier == 0:
                    multiplier = 1  # Prevent multiplier from being zero

        # Mouse button down: Check if clicking on any corner
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            for circle in points:
                s = c.displayPosition(circle["x"],circle["y"],circle["z"])
                s[0] = addCOSx(s[0])
                s[1] = addCOSy(s[1])
                if (mouse_x - s[0]) ** 2 + (mouse_y - s[1]) ** 2 <= circle["radius"] ** 2:
                    circle["dragging"] = True
                    loc = s
                    offset_x = s[0] - mouse_x
                    offset_y = s[1] - mouse_y

    # Mouse button up: Stop dragging any circle
    if event.type == pygame.MOUSEBUTTONUP:
        for circle in points:
            if circle["dragging"]:
                circle["dragging"] = False
                circle["x'"] = circle["x"]
                circle["y'"] = circle["y"]
                circle["z'"] = circle["z"]

    # Key handling
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        c.addTheta((-1)*(math.pi/720)* multiplier)
    if keys[pygame.K_RIGHT]:
        c.addTheta((1)*(math.pi/720)* multiplier)
    if keys[pygame.K_UP]:
        c.addPhi((-1)*(math.pi/720)* multiplier)
    if keys[pygame.K_DOWN]:
        c.addPhi((1)*(math.pi/720)* multiplier)
    if keys[pygame.K_MINUS]:
        c.addR((-1)*multiplier)
    if keys[pygame.K_PLUS]:
        c.addR(1*multiplier)

    # If dragging, move the circle to the mouse position
    mouse_x, mouse_y = pygame.mouse.get_pos()
    for circle in points:
        if circle["dragging"]:
            xp = c.getXprime()
            yp = c.getYprime()
            xc = offset_x+mouse_x-loc[0]
            yc = offset_y+mouse_y-loc[1]
            circle["x"] = (xp[0]*(xc)-yp[0]*(yc)) + circle["x'"]
            circle["y"] = (xp[1]*(xc)-yp[1]*(yc)) + circle["y'"]
            circle["z"] = (xp[2]*(xc)-yp[2]*(yc)) + circle["z'"]

            if circle["corner"] == 1:
                ab[0] = [circle["x"],circle["y"],circle["z"]]
                ac[0] = [circle["x"],circle["y"],circle["z"]]
            elif circle["corner"] == 2:
                ab[1] = [circle["x"],circle["y"],circle["z"]]
                bd[0] = [circle["x"],circle["y"],circle["z"]]
            elif circle["corner"] == 3:
                ac[1] = [circle["x"],circle["y"],circle["z"]]
                cd[0] = [circle["x"],circle["y"],circle["z"]]
            elif circle["corner"] == 4:
                bd[1] = [circle["x"],circle["y"],circle["z"]]
                cd[1] = [circle["x"],circle["y"],circle["z"]]

    # Drawing
    screen.fill(BACKGROUND_COLOR)
    
    #Draw X -> x color is red
    line2render(xLine,(255,0,0))

    #Draw Y -> x color is green
    line2render(yLine,(0,255,0))

    #Draw Z -> x color is blue
    line2render(zLine,(0,0,255))

    #square
    line2render(ab,(200,255,0))
    line2render(ac,(200,255,0))
    line2render(bd,(200,255,0))
    line2render(cd,(200,255,0))
    point2render(ab[0],(200,255,0), 3)
    point2render(ab[1],(200,255,0), 3)
    point2render(ac[1],(200,255,0), 3)
    point2render(bd[1],(200,255,0), 3)

    # New cube render
    center =[points[4]["x"], points[4]["y"], points[4]["z"]]
    point2render(center,(200,0,200), 3)
    render_cube(points[4]["x"], points[4]["y"], points[4]["z"], 50, (200, 0, 200))  # Example cube

    # Render the speed multiplier
    multiplier_text = font.render(f'{multiplier}', True, (0, 0, 0))
    screen.blit(multiplier_text, (10, 10))

    # Update the display
    pygame.display.flip()

    # Frame rate (FPS)
    pygame.time.Clock().tick(60)