import pygame

#Allgemein---------------------------------------------------------------------------


#MIT License
#Sophie Kroder
#04.07.2022

#Fenstergrößen
WIDTH = 800
HEIGHT = 600
FPS = 60

# definitionen farben
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

#definitionen aktionen
sprung = 0 #An/Aus
sprungzeit = 0 #zähler
sprungsperre = 0 #An/Aus
sprungsperrzeit = 0 #zähler
kollisions_indikator = 0
aktive_pause = 0 #An/Aus

#Benutzeroberfläche
schriftart = pygame.font.match_font('arial')
def text_ausgabe (bildschirm, text, groesse, x, y, farbe):
    schrift = pygame.font.Font(schriftart, groesse)
    text_umwandlung = schrift.render(text, True, farbe)
    text_flaeche = text_umwandlung.get_rect()
    text_flaeche.center = (x, y)
    bildschirm.blit(text_umwandlung, text_flaeche)


spiel_zustand = 0
# 0 Menü
# 1 Spiel Initialisieren
# 2 Spielen
# 3 Pause
# 4 Game Over

#-----------------------------------------------------------------------------
#objeke aus den Klassen generieren

#spieler
anfangsposition = [WIDTH / 5, HEIGHT / 3 * 2]
anzahl_leben = 3

class Spieler(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20, 40))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        #self.rect.center = (anfangsposition[0] , anfangsposition[1])
        self.rect.x = anfangsposition[0] 
        self.rect.y = anfangsposition[1]
        
    def update(self):
        if sprung == 0:
            self.rect.y = anfangsposition[1] #keine sprung
        if sprung == 1:
            self.rect.y = anfangsposition[1] - 50 # sprung ausgeführt
            
#---------------------------------------------------------------------------------
#hindernisse
spawn = [WIDTH + 9 , HEIGHT/ 3 * 2 + 20 ] # um aus dem bild zu sein WIDTH + 10
clock = pygame.time.Clock()
beschleunigung = 1.5

class Hindernisse(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (spawn[0], spawn[1])


    def update(self):
        zeit = int(pygame.time.get_ticks() / 1000) #methode holt zeit in ms
        
        #-----------------
        
        # geschwindigkeit in pixel pro loopdurchlauf
        
        # gleichmäßig beschleunigte bewegung 
        # geschwindigkeit = int(beschleunigung * (zeit - anfangs_zeit))       
        
        #-----------------
        
        # exponentialfunktion
        a = 3 #basis für exponentialfkt.
        geschwindigkeit = - a ** (round (-(zeit - 50)/20,2)) +17
        
        print(geschwindigkeit)
        # genutz um herauszufinden was
        # die maximale geschwindigkeit
        # ungefähr sein sollte
        # damit man unendlich weiter spielen könnte

        self.rect.x -= int(geschwindigkeit)
        
        if self.rect.x < - 10 :
            self.rect.x = (spawn[0])
        
#-----------------------------------------------------------------------------------------------

# Spiel erstellen
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jump 'n Run")


#Erstelle Gruppe Spieler und erstelle die Spielfigur
spieler_sprites = pygame.sprite.Group()
spieler = Spieler()
spieler_sprites.add(spieler)

#Erstelle Gruppe Hindernisse und erstelle die Hindernisfigur
hindernis_sprites = pygame.sprite.Group()
hindernis = Hindernisse()
hindernis_sprites.add(hindernis)

# --------------------------------------------------------------------------------------------

running = True
while running:
    # lässt schleife mit richtiger geschwindigkeit laufen
    clock.tick(FPS)
    
    #wird das x zum schließen gedrückt
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    #Tastenabfrage----------------------------------------------------------------------------
    
    keystate = pygame.key.get_pressed() # fragt gedrückte taste ab
    
    if keystate[pygame.K_ESCAPE]:
        running = False #esc taste schließt spiel ebenfalls
    
    # spiel_zustand wird auf (zwischenschritt: spiel_init )auf spielen umgestellt
    # wenn im menü oder game over screen die eingabetast gedrückt wird
    if keystate[pygame.K_RETURN] or  keystate[pygame.K_KP_ENTER]:
        if spiel_zustand == 0 or spiel_zustand == 4:
            spiel_zustand = 1
        
    #pause wenn im spielmodus
    if keystate[pygame.K_b]:
        if spiel_zustand == 2:
            spiel_zustand = 3
        else:
            spiel_zustand = 2
        
    if keystate[pygame.K_SPACE]:
        if sprungsperre == 0:
            sprung = 1
    
    # Falls der sprung aktiv ist, soll gezählt werden bis der spieler wieder runter soll
    if sprung == 1:
        if sprungzeit < FPS/2 :
            sprungzeit += 1
        else:
            sprung = 0
            sprungzeit = 0
            sprungsperre = 1
    
    if sprungsperre == 1:
        sprungsperrzeit += 1
        if sprungsperrzeit > FPS/6:
            sprungsperre = 0
            sprungsperrzeit = 0
    
    
    # Updates
    
    if spiel_zustand == 2:
        spieler_sprites.update()
        hindernis_sprites.update()
            
        # Kollision -------------------------------------------------------------------------------------------------
        
        # k_i soll gleich 0 sein, wenn es keine Kollision gibt
        # wenn eine kollision bemerkt wird, soll k_i sofort auf 1 umgestellt werden
        # und ein leben abgezogen werden
        # k_i soll wieder gleich 0 sein, wenn es wieder keine Kollision gibt
        
        if pygame.sprite.spritecollide(spieler, hindernis_sprites, False):
            if kollisions_indikator == 0:
                kollisions_indikator = 1
                anzahl_leben -= 1
                # print("Kollision", anzahl_leben) zum testen
                if anzahl_leben == 0:
                    spiel_zustand = 4
        else:
            kollisions_indikator = 0
        
        
    
    # Draw / render ------------------------------------------------------------------------------------------------    
    screen.fill(BLACK)
    
    #Menü
    if spiel_zustand == 0:
        # Titel
        text_ausgabe (screen, "Jump 'n Run Game", 80, WIDTH / 2 , HEIGHT / 3, WHITE) 
        # Spiel starten
        text_ausgabe (screen, "Zum Starten Enter tippen ", 40, WIDTH / 2 , HEIGHT / 3 + 140, WHITE) 
        # Spiel beenden
        text_ausgabe (screen, "Zum Beenden ESC tippen", 40, WIDTH / 2 , HEIGHT / 3 + 200, WHITE)
        # Spiel beenden
        text_ausgabe (screen, "(C) 29.06.2022 Sophie Kroder", 20, WIDTH / 2 , HEIGHT / 3 + 320, WHITE) 

    #Spiel initialisieren und automatisch losspielen
    if spiel_zustand == 1:
        anzahl_leben = 3
        #damit die geschwindigkeit immer neu initialisiert wird
        anfangs_zeit = pygame.time.get_ticks() / 1000 
        hindernis.rect.center = (spawn[0], spawn[1])
        spiel_zustand = 2
    
    #spielen
    if spiel_zustand == 2:
        spieler_sprites.draw(screen)
        hindernis_sprites.draw(screen)
        
    #Pause
    if spiel_zustand == 3:
        text_ausgabe (screen, "Pause", 80, WIDTH / 2 , HEIGHT / 3, WHITE) 
        
    #Game Over
    if spiel_zustand == 4:
        #End-Screen
        text_ausgabe (screen, "Game Over", 80, WIDTH / 2 , HEIGHT / 3, WHITE)
        #Spiel starten
        text_ausgabe (screen, "Zum Neustarten Enter tippen ", 40, WIDTH / 2 , HEIGHT / 3 + 140, WHITE) 
        #Spiel beenden
        text_ausgabe (screen, "Zum Beenden ESC tippen", 40, WIDTH / 2 , HEIGHT / 3 + 200, WHITE) 
    
    # Anzahl Leben oben rechts anzeigen
    text_ausgabe (screen, str(anzahl_leben), 44, WIDTH - 30, 30, BLUE) 
    pygame.display.flip() #gehört zu draw()
    
    #print(pygame.time.get_ticks())

print(pygame.time.get_ticks())

pygame.quit()
