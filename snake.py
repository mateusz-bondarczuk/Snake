#!/usr/bin/python3

#  Copyright (c) 2020 Mateusz Bondarczuk

import random
import pygame
import os

pygame.init()

#rozmiar okna gry
szer = 400
wys = 400
coPokazuje = "menu"
wielkosc = 20
rozmiarCzcionki = 36
punkty = 0

screen = pygame.display.set_mode((szer,wys))

def napisz(tekst, x, y, rozmiar) :
    cz = pygame.font.SysFont("Conacry", rozmiar)
    rend = cz.render(tekst, 1, (240,9,192))
    x = (szer - rend.get_rect().width)/2
#   y = (wys - rend.get_rect().height)/2
    screen.blit(rend, (x,y))

class Waz():
    def __init__(self):
        global wielkosc
        self.x = szer/2
        self.y = wys/2
        #wielkosc = 20
        self.cialo = [
            pygame.Rect(self.x, self.y, wielkosc, wielkosc),
            pygame.Rect(self.x-wielkosc, self.y, wielkosc, wielkosc),
            pygame.Rect(self.x-(2*wielkosc), self.y, wielkosc, wielkosc)
        ]
    def rysuj(self, dx, dy):
        self.cialo.insert(0, pygame.Rect((self.cialo[0].x + dx), (self.cialo[0].y+dy), wielkosc, wielkosc))
        self.cialo.pop()
        for i in range(len(self.cialo)):
            pygame.draw.rect(screen, (0,0,0), self.cialo[i])
    def czyZezar(self, dx, dy):
        global jedz, punkty
        if self.cialo[0].colliderect(jedz.cialo):
            #dodac nowy element do ciala weza
            self.cialo.insert(0, pygame.Rect((self.cialo[0].x + dx), (self.cialo[0].y+dy), wielkosc, wielkosc))
            #usunac jedzonko i stworzyc nowe
            del jedz
            jedz = Pokarm()
            #for i in range(len(self.cialo)):

            punkty += 1
    def kolizja(self):
        global gad, coPokazuje
        for i in range(len(self.cialo)-1):
            if self.cialo[0].colliderect(self.cialo[i+1]):
                coPokazuje = "koniec"
                del gad

class Pokarm():
    def __init__(self):
        global wielkosc
        #wielkosc = 10
        self.x = random.randint(0, (szer-wielkosc))
        self.y = random.randint(0, (wys - wielkosc))
        self.cialo = pygame.Rect(self.x, self.y, wielkosc, wielkosc)
    def rysuj(self):
        pygame.draw.rect(screen, (0, 0, 0), self.cialo)

#pierwsza deklaracja gada, jedzonka i ruchu - wykozystywana przy przejsciu z menu do gramy
gad = Waz()
jedz = Pokarm()
vx, vy = wielkosc, 0
while True :
    screen.fill((0, 128, 0))
    events = pygame.event.get()


    #reakcje na nacisniecie klawiszy
    for event in events :
        if event.type == pygame.QUIT :
            pygame.quit()
            quit()
        #ruch
        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_ESCAPE :
                pygame.quit()
                quit()
            elif event.key == pygame.K_SPACE :
                if coPokazuje != "gramy":
                    punkty = 0
                coPokazuje = "gramy"


    if coPokazuje == "menu":
        grafika = pygame.image.load(os.path.join("snake.png"))
        screen.blit(grafika, (0, 0))
        napisz("W Ą Ż", szer/2, wys/2, rozmiarCzcionki)
        napisz("Naciśnij spację aby rozpocząć.", szer/2, wys-rozmiarCzcionki, rozmiarCzcionki)

        # odświeżenie ekranu
        pygame.display.flip()
    elif coPokazuje=="gramy" :
        screen.fill((116, 111, 115))
        jedz.rysuj()

        # reakcje na nacisniecie klawiszy
        for event in events:
            # ruch
            if event.type == pygame.KEYDOWN:
                # ruch w górę
                if event.key == pygame.K_UP:
                    vx = 0
                    vy = -wielkosc
                # ruch w dół
                elif event.key == pygame.K_DOWN:
                    vx = 0
                    vy = wielkosc
                # ruch w lewo
                elif event.key == pygame.K_LEFT:
                    vx = -wielkosc
                    vy = 0
                # ruch w prawo
                elif event.key == pygame.K_RIGHT:
                    vx = wielkosc
                    vy = 0

        gad.rysuj(vx, vy)
        gad.czyZezar(vx, vy)

        #kolizja ze ścianami
        if gad.cialo[0].left < 0 or (gad.cialo[0].right) > szer :
            del gad
            coPokazuje = "koniec"
        elif gad.cialo[0].top < 0 or (gad.cialo[0].bottom) > wys :
            del gad
            coPokazuje = "koniec"
        else:
            # kolizja ze soba
            gad.kolizja()
    elif coPokazuje == "koniec" :
        napisz("KONIEC GRY!!!", szer/2, wys/3, rozmiarCzcionki)
        napisz("Twoje punkty: " + str(punkty), szer / 2, (wys / 3) * 2, rozmiarCzcionki - 10)
        #deklaracja gada, jedzonka i kierunku ruchu po zakonczeniu gry i jej wznowieniu
        gad = Waz()
        jedz = Pokarm()
        vx, vy = wielkosc, 0
     # odświeżenie ekranu
    pygame.display.flip()
    pygame.event.pump()
    pygame.time.delay(100)

