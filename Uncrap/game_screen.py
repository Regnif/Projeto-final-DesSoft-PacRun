import pygame
import random
from os import path

from config import img_dir, snd_dir, fnt_dir, WIDTH, HEIGHT, WHITE, BLACK, YELLOW, RED, FPS, QUIT

SOBE = 0
DIREITA = 1
DESCE = 2
ESQUERDA = 3
PARADO = 4
SALTANDO = 5

# Classe Jogador que representa o Pac
class Player(pygame.sprite.Sprite):
    
    # Construtor da classe.
    def __init__(self, player_img):
        
        # Construtor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self)
        
        # Carregando a imagem de fundo.
        self.image = player_img
        
        # Diminuindo o tamanho da imagem.
        self.image = pygame.transform.scale(player_img, (40, 40))
        
        # Deixando transparente.
        self.image.set_colorkey(WHITE)
        
        # Detalhes sobre o posicionamento.
        self.rect = self.image.get_rect()
        
        # Centraliza embaixo da tela.
        self.rect.x = 40
        self.rect.y = 40
        
        self.previous_pos_x = self.rect.x
        self.previous_pos_y = self.rect.y
        
        # Velocidade da nave
        self.speedx = 0
        self.speedy = 0
        
        self.dir_prox = PARADO
        
        # Melhora a colisão estabelecendo um raio de um circulo
        self.radius = 20
    
    # Metodo que atualiza a posição da navinha
    def update(self):
        self.previous_pos_x = self.rect.x
        self.previous_pos_y = self.rect.y
        
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        
        if self.rect.x % 40 == 0 and self.rect.y % 40 == 0:
            
            if self.dir_prox == SOBE:
                self.speedx = 0
                self.speedy = -4
            elif self.dir_prox == DIREITA:
                self.speedx = 4
                self.speedy = 0
            elif self.dir_prox == DESCE:
                self.speedx = 0
                self.speedy = 4
            elif self.dir_prox == ESQUERDA:
                self.speedx = -4
                self.speedy = 0
        if self.dir_prox == PARADO:
            self.speedx = 0
            self.speedy = 0

    def rollback(self):
        self.rect.x = self.previous_pos_x
        self.rect.y = self.previous_pos_y
        self.dir_prox = PARADO
                    
# Classe Mob que representa os fantasmas
class Mob(pygame.sprite.Sprite):
    
    # Construtor da classe.
    def __init__(self, mob_img):
        
        # Construtor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self)
        
        # Diminuindo o tamanho da imagem.
        self.image = pygame.transform.scale(mob_img, (40, 40))
        
        # Deixando transparente.
        self.image.set_colorkey(WHITE)
        
        # Detalhes sobre o posicionamento.
        self.rect = self.image.get_rect()
        self.centerx = 1200
        self.centery = 40
        
        # Sorteia um lugar inicial em x
        self.rect.x = self.centerx
        # Sorteia um lugar inicial em y
        self.rect.y = self.centery
        # Sorteia uma velocidade inicial
        self.speedx = 0
        self.speedy = 0
        
        # Melhora a colisão estabelecendo um raio de um circulo
        self.radius = int(self.rect.width * .40 / 2)
        
    # Metodo que atualiza a posição do meteoro
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        
        # Mantem dentro da tela
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
            self.speedx *= -1
        if self.rect.left < 0:
            self.rect.left = 0
            self.speedx *= -1
        if self.rect.top < 0:
            self.rect.top = 0
            self.speedy *= -1
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.speedy *= -1

class Wall(pygame.sprite.Sprite):
    
    # Construtor da classe.
    def __init__(self, x, y):
        
        # Construtor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.Surface((40, 40))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
class Food(pygame.sprite.Sprite):
    
    def __init__(self,food_img,x,y):
        
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.transform.scale(food_img,(40,40))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.radius = 5
    """
    def refeicao(self):
        #Apaga a comida
        self.kill()
    """
def make_map(ground_img, dirt_img, food_img):
    map_image = pygame.Surface((1280,720)) # used as the surface for rendering, which is scaled        
    map_image.set_colorkey(BLACK)

    game_map = [['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
                ['1','0','0','0','0','0','0','0','0','0','0','1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','1','0','0','0','0','1'],
                ['1','0','1','0','1','1','1','0','1','1','0','1','0','1','0','1','1','1','0','1','1','0','1','1','1','0','1','0','0','0','0','1'],
                ['1','0','1','0','0','0','0','0','0','1','0','1','0','1','0','0','0','0','0','0','1','0','0','0','0','0','1','0','0','0','0','1'],
                ['1','0','1','0','1','1','1','1','0','1','0','1','0','1','0','1','0','1','1','0','1','0','1','1','1','0','1','0','1','1','1','1'],
                ['1','0','0','0','0','0','0','0','0','1','0','0','0','0','0','0','0','0','0','0','0','0','1','0','0','0','0','0','0','0','0','1'],
                ['1','1','1','1','1','0','1','1','0','1','0','1','1','0','1','1','0','1','0','1','1','0','1','0','1','1','1','0','1','1','0','1'],
                ['1','0','0','0','1','0','1','0','0','0','0','0','0','0','0','0','0','0','0','1','1','0','0','0','1','0','0','0','0','1','0','1'],
                ['1','0','1','0','0','0','0','0','1','1','1','1','1','0','1','0','1','1','0','0','0','0','1','0','0','0','1','1','0','0','0','1'],
                ['1','0','1','0','1','1','1','0','0','0','0','0','0','0','1','0','1','1','1','0','1','0','1','1','1','0','1','0','0','1','0','1'],
                ['1','0','1','0','0','0','0','0','1','1','0','1','0','1','1','0','0','0','1','0','1','0','0','0','0','0','0','0','1','1','0','1'],
                ['1','0','1','0','1','1','1','0','0','0','0','1','0','0','0','0','1','0','1','0','1','0','1','1','0','1','0','1','1','0','0','1'],
                ['1','0','0','0','1','0','0','0','1','1','0','1','1','0','1','0','1','0','1','0','1','0','1','1','0','1','0','1','1','0','1','1'],
                ['1','1','1','0','1','0','1','1','1','0','0','0','1','0','1','0','1','0','1','0','1','0','1','1','0','1','0','0','0','0','1','1'],
                ['1','0','0','0','1','0','0','0','0','0','1','0','1','0','0','0','0','0','0','0','0','0','0','1','0','0','0','1','1','0','0','1'],
                ['1','0','1','1','1','0','1','1','1','0','1','0','1','0','1','1','0','1','1','0','1','1','0','1','0','1','0','1','1','1','0','1'],
                ['1','0','0','0','0','0','0','0','0','0','1','0','0','0','1','1','0','0','0','0','0','0','0','1','0','0','0','0','0','0','0','1'],
                ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1']]


    # Pinta o background.    
    for y, layer in enumerate(game_map):
        for x, tile in enumerate(layer):
            if tile == '0':
                map_image.blit(ground_img,(x*40,y*40))
            if tile == '1':
                map_image.blit(dirt_img,(x*40,y*40))
                
    # Monta as paredes para colisão.
    wall_group = pygame.sprite.Group()
    food_group = pygame.sprite.Group()
    for y, layer in enumerate(game_map):
        for x, tile in enumerate(layer):
            if tile == '1':
                wall_group.add(Wall(x*40,y*40))
            if tile == '0':
                food_group.add(Food(food_img,x*40,y*40))
    
    return map_image, wall_group, food_group
            
# Classe que representa uma explosão de meteoro
class Explosion(pygame.sprite.Sprite):

    # Construtor da classe.
    def __init__(self, center, explosion_anim):
        # Construtor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self)

        # Carrega a animação de explosão
        self.explosion_anim = explosion_anim

        # Inicia o processo de animação colocando a primeira imagem na tela.
        self.frame = 0
        self.image = self.explosion_anim[self.frame]
        self.rect = self.image.get_rect()
        self.rect.center = center

        # Guarda o tick da primeira imagem
        self.last_update = pygame.time.get_ticks()

        # Controle de ticks de animação: troca de imagem a cada self.frame_ticks milissegundos.
        self.frame_ticks = 50

    def update(self):
        # Verifica o tick atual.
        now = pygame.time.get_ticks()

        # Verifica quantos ticks se passaram desde a ultima mudança de frame.
        elapsed_ticks = now - self.last_update

        # Se já está na hora de mudar de imagem...
        if elapsed_ticks > self.frame_ticks:

            # Marca o tick da nova imagem.
            self.last_update = now

            # Avança um quadro.
            self.frame += 1

            # Verifica se já chegou no final da animação.
            if self.frame == len(self.explosion_anim):
                # Se sim, tchau explosão!
                self.kill()
            else:
                # Se ainda não chegou ao fim da explosão, troca de imagem.
                center = self.rect.center
                self.image = self.explosion_anim[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

# Carrega todos os assets uma vez só.
def load_assets(img_dir, snd_dir, fnt_dir):
    assets = {}
    assets["player_img"] = pygame.image.load(path.join(img_dir, "Pac.png")).convert()
    assets["ground_img"] = pygame.image.load(path.join(img_dir, "fund_cla.png")).convert()
    assets["dirt_img"] = pygame.image.load(path.join(img_dir, "fund_esc.png")).convert()
    assets["mob_img"] = pygame.image.load(path.join(img_dir, "Personagem.png")).convert()
    assets["background"] = pygame.image.load(path.join(img_dir, 'Plano_de_fundo.png')).convert()
    assets["boom_sound"] = pygame.mixer.Sound(path.join(snd_dir, 'expl3.wav'))
    assets["destroy_sound"] = pygame.mixer.Sound(path.join(snd_dir, 'expl6.wav'))
    assets["food_img"] = pygame.image.load(path.join(img_dir, "comida.png")).convert()
    explosion_anim = []
    for i in range(9):
        filename = 'regularExplosion0{}.png'.format(i)
        img = pygame.image.load(path.join(img_dir, filename)).convert()
        img = pygame.transform.scale(img, (32, 32))        
        img.set_colorkey(BLACK)
        explosion_anim.append(img)
    assets["explosion_anim"] = explosion_anim
    assets["score_font"] = pygame.font.Font(path.join(fnt_dir, "PressStart2P.ttf"), 28)
    return assets

def game_screen(screen):
    # Carrega todos os assets uma vez só e guarda em um dicionário
    assets = load_assets(img_dir, snd_dir, fnt_dir)

    # Variável para o ajuste de velocidade
    clock = pygame.time.Clock()

    # Carrega os sons do jogo
    pygame.mixer.music.load(path.join(snd_dir, 'tgfcoder-FrozenJam-SeamlessLoop.ogg'))
    pygame.mixer.music.set_volume(0.4)
    boom_sound = assets["boom_sound"]
    
    # Cria um jogador. O construtor será chamado automaticamente.
    wall, wall_group, food_group = make_map(assets["ground_img"],assets["dirt_img"],assets["food_img"])
    player = Player(assets["player_img"])

    # Carrega a fonte para desenhar o score.
    score_font = assets["score_font"]

    # Cria um grupo de todos os sprites e adiciona a nave.
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    all_sprites.add(food_group)

    # Cria um grupo só dos meteoros
    mobs = pygame.sprite.Group()
    
    # Cria 8 meteoros e adiciona no grupo meteoros
    for i in range(1):
        m = Mob(assets["mob_img"])
        all_sprites.add(m)
        mobs.add(m)
       

    # Loop principal.
    pygame.mixer.music.play(loops=-1)

    score = -100

    lives = 3

    PLAYING = 0
    EXPLODING = 1
    DONE = 2

    state = PLAYING
    while state != DONE:
        
        # Ajusta a velocidade do jogo.
        clock.tick(FPS)
        
        if state == PLAYING:
            # Processa os eventos (mouse, teclado, botão, etc).
            for event in pygame.event.get():
                
                # Verifica se foi fechado.
                if event.type == pygame.QUIT:
                    state = DONE
                
                # Verifica se apertou alguma tecla.
                if event.type == pygame.KEYDOWN:
                    # Dependendo da tecla, altera a velocidade.
                    if event.key == pygame.K_UP:
                        player.dir_prox = SOBE
                    if event.key == pygame.K_DOWN:
                        player.dir_prox = DESCE
                    if event.key == pygame.K_LEFT:
                        player.dir_prox = ESQUERDA
                    if event.key == pygame.K_RIGHT:
                        player.dir_prox = DIREITA
                
        # Depois de processar os eventos atualiza a acao de cada sprite.
        all_sprites.update()
        
        if state == PLAYING:
            # Verifica se houve colisão entre nave e meteoro
            hits = pygame.sprite.spritecollide(player, mobs, False, pygame.sprite.collide_circle)
            if hits:
                # Toca o som da colisão
                boom_sound.play()
                player.kill()
                lives -= 1
                explosao = Explosion(player.rect.center, assets["explosion_anim"])
                all_sprites.add(explosao)
                state = EXPLODING
                explosion_tick = pygame.time.get_ticks()
                explosion_duration = explosao.frame_ticks * len(explosao.explosion_anim) + 400
           
            # Verifica se houve colisão entre jogador e paredes
            hits = pygame.sprite.spritecollide(player, wall_group, False, pygame.sprite.collide_rect)
            if hits:
                player.rollback()
            
            #Verifica se houve colisao entre jogador e comida
            
            hits = pygame.sprite.spritecollide(player, food_group, True, pygame.sprite.collide_circle)
            if hits:
                score += 100
           
        elif state == EXPLODING:
            now = pygame.time.get_ticks()
            if now - explosion_tick > explosion_duration:
                if lives == 0:
                    state = DONE
                else:
                    state = PLAYING
                    player = Player(assets["player_img"])
                    all_sprites.add(player)

        #repopula de comida
        if len(food_group) == 0 :
            print ("Fim") # fazer aparecer novamente a comida
        
        
        # A cada loop, redesenha o fundo e os sprites
        screen.fill(BLACK)
        screen.blit(wall, (0,0))
        all_sprites.draw(screen)

        # Desenha o score
        text_surface = score_font.render("{:08d}".format(score), True, YELLOW)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (WIDTH / 2,  10)
        screen.blit(text_surface, text_rect)

        # Desenha as vidas
        text_surface = score_font.render(chr(9829) * lives, True, RED)
        text_rect = text_surface.get_rect()
        text_rect.bottomleft = (10, HEIGHT - 10)
        screen.blit(text_surface, text_rect)
        
        # Depois de desenhar tudo, inverte o display.
        pygame.display.flip()

    return QUIT