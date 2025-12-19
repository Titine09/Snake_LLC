import pyxel
import random

pyxel.init(300,200,"Snake_LLC")

snake_x = 150
snake_y = 100
time = 0
direction = "RIGHT"
snake = [ (snake_x,snake_y), (snake_x -8,snake_y), (snake_x -8,snake_y -8) ]

pyxel.load("univ.pyxres")
speed = 6
etat = "jeu"
score = 0
meilleur_score = 0

fruits = []
double_points = False
double_timer = 0
bouclier = False


def passage_autorise(x, y):
    ouverture = 32
    centre_x = 300 // 2
    centre_y = 200 // 2

    if y < 0:
        return abs(x - centre_x) < ouverture // 2
    if y >= 200:
        return abs(x - centre_x) < ouverture // 2
    if x < 0:
        return abs(y - centre_y) < ouverture // 2
    if x >= 300:
        return abs(y - centre_y) < ouverture // 2

    return True


def deplace_snake():
    global direction , etat, bouclier

    snake_x, snake_y = snake[0]

    if pyxel.btn(pyxel.KEY_RIGHT):
        direction ="RIGHT"
    if pyxel.btn(pyxel.KEY_LEFT):
        direction ="LEFT"
    if pyxel.btn(pyxel.KEY_UP):
        direction ="UP"
    if pyxel.btn(pyxel.KEY_DOWN):
        direction ="DOWN"
    
    if direction == "RIGHT":
        snake_x += 8
    if direction == "LEFT":
        snake_x -= 8
    if direction == "UP":
        snake_y -= 8
    if direction == "DOWN":
        snake_y += 8

    if not passage_autorise(snake_x, snake_y):
        if bouclier:
            bouclier = False
            return snake[0]
        etat = "mort"
        return snake[0]

    if snake_x < 0:
        snake_x = 292
    elif snake_x >= 300:
        snake_x = 0
    if snake_y < 0:
        snake_y = 192
    elif snake_y >= 200:
        snake_y = 0

    return snake_x, snake_y


def update():
    global time, snake, etat, score, meilleur_score, double_points

    if etat == "mort":
        if pyxel.btnp(pyxel.KEY_SPACE):
            if score > meilleur_score:
                meilleur_score = score
            reset_game()
        return

    time += 1

    snake_x, snake_y = snake[0]
    nsnake_x, nsnake_y = deplace_snake()

    if time % 3 == 0:
        debut_ancien_snake = snake[:-1]
        if snake_x != nsnake_x or snake_y != nsnake_y:
            snake = [(nsnake_x, nsnake_y)] + debut_ancien_snake
            manger_fruit(nsnake_x, nsnake_y)

    if double_points and time - double_timer > 1800:
        double_points = False


def reset_game():
    global snake, time, etat, score

    fruits.clear()
    for i in range(3):
        ajouter_fruit()

    snake = [(150,100),(142,100),(134,100)]
    time = 0
    score = 0
    etat = "jeu"


def ajouter_fruit():
    x = random.randrange(0, 300, 8)
    y = random.randrange(0, 200, 8)
    t = random.choice(["pomme", "raisin", "orange", "cerise"])
    fruits.append([x, y, t, time])


def manger_fruit(x, y):
    global score, speed, bouclier, double_points, double_timer

    for fruit in fruits:
        fx, fy, t, spawn = fruit
        if x == fx and y == fy:
            fruits.remove(fruit)
            ajouter_fruit()

            score += 2 if double_points else 1

            if t == "raisin":
                speed = max(2, speed - 1)
            if t == "orange":
                bouclier = True
            if t == "cerise":
                double_points = True
                double_timer = time
            return True
    return False


def texte_centre(y, texte, couleur):
    x = 300//2 - len(texte) * 4 // 2
    pyxel.text(x, y, texte, couleur)


def draw():
    pyxel.cls(0)
    draw_fond()
    draw_murs()
    draw_fruits()
    draw_snake()
    draw_hud()
    
    for fx, fy, t, spawn in fruits:
        couleurs = {"pomme":8,"raisin":12,"orange":9,"cerise":11}
        pyxel.rect(fx, fy, 8, 8, couleurs[t])

    for block_x, block_y in snake:
        pyxel.rect(block_x, block_y,8,8,11)

    pyxel.text(5,5,f"SCORE : {score}",7)
    pyxel.text(200,5,f"BEST : {meilleur_score}",10)

    if etat == "mort":
        texte_centre(90,"GAME OVER",8)
        texte_centre(110,"ESPACE POUR REJOUER",7)
        
def draw_fond():
    for x in range (0, 300, 8):
        for y in range (0, 200,8):
            pyxel.blt(x,y,0,8,8,8,8)
            
def draw_murs():
    ouverture = 32
    cx, cy = 150, 100

    for x in range(0,300,8):
        if abs(x - cx) > ouverture//2:
            pyxel.blt(x, 0, 0, 24, 8, 8, 8)
            pyxel.blt(x,192, 0, 24, 8, 8, 8)

    for y in range(0,200,8):
        if abs(y - cy) > ouverture//2:
            pyxel.blt(0, y, 0, 24, 8, 8, 8)
            pyxel.blt(292,y,0, 24, 8, 8, 8)

def draw_fruits():
    for fx, fy, t, spawn in fruits:
        if t == "pomme":
            pyxel.blt(x,y,2,32,48,8,8)
        if t == "raisin":
            pyxel.blt(x,y,2,32,63,8,8)
        if t == "orange":
            pyxel.blt(x,y,2,32,79,8,8)
        if t == "cerise":
            pyxel.blt(x,y,2,32,96,8,8)
            
def draw_snake():
    for i,(x,y) in enumerate(snake):
        if i == 0:
            pyxel.blt(x,y,1, 32,32,8,8)
        else:
            pyxel.blt(x,y,1, 32,40,8,8)
            
def draw_hud():
    pyxel.text(5, 5, f"SCORE : {score}", 7)
    pyxel.text(200, 5, f"BEST : {meilleur_score}", 10)

    if etat == "mort":
        texte_centre(90,"GAME OVER",8)
        texte_centre(110,"ESPACE POUR REJOUER",7)
   

pyxel.run(update, draw)
