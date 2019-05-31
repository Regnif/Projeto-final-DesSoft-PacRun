# -*- codingp: utf-8 -*-

# Importando as bibliotecas necessárias.
import pygame
import random
import time

from os import path

from config import WIDTH, HEIGHT, INIT, GAME, QUIT, HELP, OVER
from init_screen import init_screen
from help_screen import help_screen
from game_screen import game_screen
from gameover_screen import gameover_screen

# Inicialização do Pygame.
pygame.init()
pygame.mixer.init()


# Tamanho da tela.
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Nome do jogo
pygame.display.set_caption("UnCrap")

# Comando para evitar travamentos.
try:
    state = INIT
    score = 0
    while state != QUIT:
        if state == INIT:
            state = init_screen(screen)
        elif state == GAME:
            state, score = game_screen(screen)
        elif state == HELP:
            state = help_screen(screen)
        elif state == OVER:
            state = gameover_screen(screen, score - 100)
        else:
            state = QUIT
finally:
    pygame.quit()
