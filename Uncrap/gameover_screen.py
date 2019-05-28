# -*- coding: utf-8 -*-
"""
Created on Tue May 28 10:23:12 2019

@author: gabig_000
"""

import pygame
import random
from os import path

from config import img_dir, BLACK, FPS, INIT, QUIT, YELLOW, HEIGHT, WIDTH

def gameover_screen(screen):
    
    score_font = pygame.font.Font(path.join(fnt_dir, "PressStart2P.ttf"), 28)
    
    # Variável para o ajuste de velocidade
    clock = pygame.time.Clock()

    # Carrega o fundo da tela de ajuda
    background = pygame.image.load(path.join(img_dir, 'Congrats.png')).convert()
    background_rect = background.get_rect()

    running = True
    while running:
        
        # Ajusta a velocidade do jogo.
        clock.tick(FPS)
        
        # Processa os eventos (mouse, teclado, botão, etc).
        for event in pygame.event.get():
            # Verifica se foi fechado.
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_x:
                    state = QUIT
                    running = False
            


            if event.type == pygame.KEYUP:
                if event.key == pygame.K_p:
                    state = INIT
                    running = False
            
        # A cada loop, redesenha o fundo e os sprites
        screen.fill(BLACK)
        screen.blit(background, background_rect)

        text_surface = score_font.render("{:08d}".format(score), True, YELLOW)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (WIDTH / 2,  HEIGHT / 2)
        screen.blit(text_surface, text_rect)

        # Depois de desenhar tudo, inverte o display.
        pygame.display.flip()

    return state