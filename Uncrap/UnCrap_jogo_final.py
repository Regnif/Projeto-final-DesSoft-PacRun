# -*- coding: utf-8 -*-

# Importando as bibliotecas necessárias.
import pygame
import random
import time

from os import path

from config import WIDTH, HEIGHT, INIT, GAME, QUIT, HELP
from init_screen import init_screen
from help_screen import help_screen
from game_screen import game_screen

# Inicialização do Pygame.
pygame.init()
pygame.mixer.init()


# Tamanho da tela.
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Nome do jogop
pygame.display.set_caption("UnCrap")

# Comando para evitar travamentos.
try:
    state = INIT
    while state != QUIT:
        if state == INIT:
            state = init_screen(screen)
        elif state == GAME:
            state = game_screen(screen)
        elif state == HELP:
            state = help_screen(screen)
        else:
            state = QUIT
finally:
    pygame.quit()
