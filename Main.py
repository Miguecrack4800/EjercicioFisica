import pygame, math

# Constantes ------------------------------------ ( NO CAMBIAR )

SCREEN_SIZE = (1280, 512)
BACKGROUND_COLOR = (152, 237, 182)
AMPLIFICADOR = 1.5
SNAP = 2

# -----------------------------------------------

class TextBox():
    def __init__(self, width, height, font, x, y, text = ""):
        self.width = width
        self.height = height
        self.font = font
        self.x = x
        self.y = y
        self.text = text

    def show(self, screen, anim_tick, selected):
        pygame.draw.rect(screen, (250, 250, 250), (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, (25, 25, 25), (self.x, self.y, self.width, self.height), 1)
        texto = self.font.render(self.text + ("|" if (anim_tick<45 and selected) else ""), True, (25, 25, 25))
        screen.blit(texto, (self.x+5, self.y+3))

    def get_text(self):
        if(self.text != ""):
            return self.text
        return "0"

class Slider():
    def __init__(self, width, x, y, start, finish, pos = 50):
        self.width = width
        self.x = x
        self.y = y
        self.start = start
        self.finish = finish
        self.pos = pos

    def snap(self):
        for x in range(5):
            dst = abs(25*x - self.pos)
            if(dst <= SNAP):
                self.pos = 25*x

    def show(self, screen):
        self.snap()
        pygame.draw.rect(screen, (120, 120, 120), (self.x, self.y-1, self.width, 4))
        pygame.draw.rect(screen, (25, 25, 25), (self.x, self.y-1, self.width, 4), 1)
        self.point = [self.x + self.width * self.pos // 100, self.y+1]
        pygame.draw.circle(screen, (230, 230, 230), self.point, 5)
        pygame.draw.circle(screen, (25,25,25), self.point, 5, 1)
        self.value = (self.finish-self.start) * self.pos / 100 + self.finish

def checkin(pos, textbox):
    if(pos[0] >= textbox.x and pos[0] <= textbox.x + textbox.width):
        if(pos[1] >= textbox.y and pos[1] <= textbox.y + textbox.height):
            return True
    return False

pygame.init()

screen = pygame.display.set_mode(SCREEN_SIZE)

fontmin = pygame.font.Font('font.ttf', 13)
fontmid = pygame.font.Font("font.ttf", 16)
fontmax = pygame.font.Font('font.ttf', 24)

clock = pygame.time.Clock()

textbox = []
for x in range(0, 4):
    textbox.append([])
    for y in range(2):
        textbox[x].append(TextBox(90, 24, fontmin, 132 + 96*y, 66 + 26*x, str(30 if y == 1 else 60)))

fuerzas = [[0, 0] for _ in range(4)]

dirr = Slider(160, 140, 190, -180, 180)

anim_tick = 0
selected = dirr

mousepos = (0, 0)
mosmov = False

run = True
while(run):
    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            run = False
        if(event.type == pygame.MOUSEMOTION):
            mousepos = event.pos
            if(mosmov):
                dirr.pos = max(0, min(100, ((mousepos[0] - dirr.x) / dirr.width * 100)))
        if(event.type == pygame.MOUSEBUTTONUP):
            if(event.button == 1):
                if(mosmov):
                    mosmov = False
        if(event.type == pygame.MOUSEBUTTONDOWN):
            if(event.button == 1):
                dst = (mousepos[0] - dirr.point[0]) ** 2 + (mousepos[1] - dirr.point[1]) ** 2
                if(dst <= 25):
                    mosmov = True
                newselect = False
                for x in textbox:
                    for y in x:
                        if(checkin(mousepos, y)):
                            selected = y
                            anim_tick = 0
                            newselect = True
                if(not newselect):
                    selected = None
        if(selected):
            if(event.type == pygame.KEYDOWN):
                if(event.key == 8):
                    selected.text = selected.text[:len(selected.text)-1]
                else:
                    if(event.key >= 48 and event.key <= 57):
                        selected.text += event.unicode

    screen.fill(BACKGROUND_COLOR)

    #Paragraph

    fuerza = fontmax.render("Fuerza", True, (25,25,25))
    ang = fontmax.render("Angulo", True, (25,25,25))
    screen.blit(fuerza, (136, 32))
    screen.blit(ang, (232, 32))
    for x in range(1, 5):
        text = fontmid.render("Fuerza " + str(x), True, (25,25,25))
        screen.blit(text, (64, 44+26*x))#235

    for x in textbox:
        for y in x:
            y.show(screen, anim_tick, selected==y)

    texto = fontmid.render("Direccion: ", True, (25,25,25))
    screen.blit(texto, (64, 180))
    dirr.show(screen)
    ang = fontmid.render(str(round(dirr.pos*3.6)-180), True, (25,25,25))
    screen.blit(ang, (310, 180))

    fs = fontmax.render("Fuerzas",  True, (25,25,25))
    screen.blit(fs, (186, 204))
    for x in range(8):
        fur = x // 2
        text = fontmin.render("F. " + str(fur+1) + " " + ("X" if x % 2 == 0 else "Y") + " :", True, (25,25,25))
        screen.blit(text, (64, 232+20*x))
        if(textbox[fur][0].get_text() != "" and textbox[fur][1].get_text() != ""):
            angulo = int(textbox[fur][1].get_text()) + (int(textbox[3][1].get_text()) if fur == 0 else 0) + (int(textbox[2][1].get_text()) if fur == 1 else 0)
            angulo = ((180 - angulo) if (fur == 0 or fur == 3) else (angulo)) - dirr.value
            if(x % 2 == 0):
                text = math.cos(math.radians(angulo % 360))
            else:
                text = math.sin(math.radians(angulo % 360))
            text *= int(textbox[fur][0].get_text())
            fuerzas[fur][x%2] = text
            text = fontmid.render(str(round(text, 8)), True, (205 if (fur % 2 == 1) else 12, 205 if (fur % 3 == 0) else 12, 205 if (fur % 2 == 0) else 12))
            screen.blit(text, (156, 232+20*x))

    ft = fontmax.render("Fuerza Total",  True, (25,25,25))
    screen.blit(ft, (152, 388))
    fx = fontmid.render("F.Total X :", True, (25,25,25))
    screen.blit(fx,(64, 416))
    ffx = sum([fuerzas[x][0] for x in range(4)])
    text = fontmid.render(str(round(ffx, 8)), True, (205,12,205))
    screen.blit(text, (166, 416))

    fy = fontmid.render("F.Total Y :", True, (25,25,25))
    screen.blit(fy,(64, 438))
    ffy = sum([fuerzas[x][1] for x in range(4)])
    text = fontmid.render(str(round(ffy, 8)), True, (205,12,205))
    screen.blit(text, (166, 438))

    ang = fontmid.render("Angulo :", True, (25,25,25))
    screen.blit(ang,(64, 460))
    angu = math.degrees(math.atan2(ffy, ffx))
    text = fontmid.render(str(round(angu,3)), True, (205,12,205))
    screen.blit(text, (166, 460))

    ff = fontmid.render("Fuerza :", True, (25,25,25))
    screen.blit(ff,(64, 482))
    fuer = math.sqrt(ffx**2 + ffy**2)
    text = fontmid.render(str(round(fuer,8)), True, (205,12,205))
    screen.blit(text, (166, 482))

    #Graph 1

    pygame.draw.line(screen, (25,25,25), (384, 256), (768, 256), 3)
    pygame.draw.line(screen, (25,25,25), (576, 64), (576, 448), 3)
    for x in range(len(fuerzas)):
        y = fuerzas[x]
        color = (205 if (x % 2 == 1) else 12, 205 if (x % 3 == 0) else 12, 205 if (x % 2 == 0) else 12)
        pygame.draw.line(screen, color, (576, 256), (round(576+y[0]*AMPLIFICADOR), round(256-y[1]*AMPLIFICADOR)), 3)

    #Graph 2

    pygame.draw.line(screen, (25,25,25), (832, 256), (1216, 256), 3)
    pygame.draw.line(screen, (25,25,25), (1024, 64), (1024, 448), 3)
    pygame.draw.line(screen, (205, 12, 205), (1024, 256), (round(1024+ffx), round(256-ffy)), 4)


    pygame.display.flip()

    anim_tick += 1
    anim_tick %= 90
    clock.tick(60)

pygame.quit()
quit()
