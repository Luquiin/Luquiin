from email.mime import image
from turtle import Screen
import pygame
from pygame.locals import *
from sys import exit
import os
from random import randrange

pygame.init() #adicionar mais coisas do pygame
pygame.mixer.init() #sons

diretorio_principal = os.path.dirname(__file__) #rodar em quapquer pc
diretorio_imagens = os.path.join(diretorio_principal, "imagens")#juntar pnde fica as patas com as imagens
diretorio_sons = os.path.join(diretorio_principal, "sons") #juntei com a pasta sons

pygame.mixer.music.set_volume(0.3)#volume da música
musica_fundo = pygame.mixer.music.load("Hu tao 930.mp3") #Programar para por a música
pygame.mixer.music.play(-1) #com o (-1) a música irá tocar repetidamente

LARGURA = 640
ALTURA = 480
x = 640
y = 480

BRANCO = (255,255,255)

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Medico game")

sprite_sheet = pygame.image.load(os.path.join(diretorio_imagens, "medico.png")).convert_alpha() # concervar a transparência

imagem_de_fundo = pygame.image.load("fundo_tela.png").convert_alpha()
imagem_de_fundo = pygame.transform.scale(imagem_de_fundo, (LARGURA, ALTURA))


rodando = True

class Medico(pygame.sprite.Sprite): #class com o nome medico
    def __init__(self):
       pygame.sprite.Sprite.__init__(self)
       self.som_pulo = pygame.mixer.Sound(os.path.join(diretorio_sons, "jump.wav"))
       self.som_pulo.set_volume(1)
       self.imagens_medico = []
       for i in range(3): # a i começa com 0 e vai parar no 3
           img = img = sprite_sheet.subsurface((i*128,0), (128,64)) #começa 0 e vai até 2
           img = pygame.transform.scale(img, (128*2, 64*2)) #tamanho do medico
           self.imagens_medico.append(img)
    
       
       
       self.index_lista = 0 #variaveis
       self.image = self.imagens_medico[self.index_lista]
       self.rect = self.image.get_rect() #pegar a ponta da imagem
       self.pos_y_inicial = ALTURA - 38 - 192/2 #fazendo uma variável
       self.rect.center = (100, LARGURA - 88) #posicionar aqui 
       self.pulo = False #variável de pulo começa False
    def pular(self):
        self.pulo = True #quando apertar space vai para True
        self.som_pulo.play() #toda vez que pular sair o som

    def update(self): 
        if self.pulo == True: #se a variável pulo for verdadeira
            if self.rect.y <= 200: #se pular nessa altura
                self.pulo = False #vai desativar o comando do SPACE
            self.rect.y -= 20 #pegando a posição atual e colocando -20
        else:
            if self.rect.y < self.pos_y_inicial: #se Y for menor que a posição Y inicial (se o medico n estiver encostado no chão)
                self.rect.y += 20 #seja somada com 20
            else: #se o medico já estiver encostado no chão
                self.rect.y = self.pos_y_inicial
                
                                      
        if self.index_lista > 2: #se for maior que 2
            self.index_lista = 0 #volta para o 0
        self.index_lista += 0.25 #vai receber ela mesmo + 0.25
        self.image = self.imagens_medico[int (self.index_lista)]

class Nuvens(pygame.sprite.Sprite): #comando padrão
    def __init__(self):
       pygame.sprite.Sprite.__init__(self)
       self.sprites = []
       self.sprites.append(pygame.image.load("nuvem.png")) #selecionar o arquivo
       self.atual = 0
       self.image = self.sprites[self.atual]
       self.image = pygame.transform.scale(self.image, (32*3, 32*3))


       self.rect = self.image.get_rect() #colocar na tela
       self.rect.y = randrange(50, 200, 50) #entre 50 a 200 com o paso de 50
       self.rect.x = LARGURA - randrange(30, 300, 90)     
        


    def update(self):
        if self.rect.topright[0] < 0: #se ultrapassar a borda esquedar #(topright pegando a parte superior direita da nuvem)
            self.rect.x = LARGURA 

            self.rect.y = randrange(50, 200, 50)
        self.rect.x -= 10 #10 vai ser a velocidade da nuvem (10 PIXELS A CADA FRAME)


todas_as_sprites = pygame.sprite.Group() #um grupo de sprites
medico = Medico()
todas_as_sprites.add(medico)

for i in range(4): #fazer as 4 nuvens
    nuvem = Nuvens()
    todas_as_sprites.add(nuvem)


relogio = pygame.time.Clock()
while True:
    relogio.tick(30)
    tela.fill(BRANCO)
    for event in pygame.event.get():
        if event.type == QUIT:    
            rodando = False
            pygame.quit()
            exit()

    
        if pygame.key.get_pressed()[K_a]: #se eu prescionar e segura a tecla (A)
                medico.rect.x = medico.rect.x - 8 #movimentação
        if pygame.key.get_pressed()[K_d]:
                medico.rect.x = medico.rect.x + 8
        
      

        if event.type == KEYDOWN: #se apertar a tecla
            if event.key == K_SPACE: #espaço
                if medico.rect.y != medico.pos_y_inicial:  #se a osição do medico for diferente a posição inicial
                   pass
                else:
                    medico.pular()   #vai fazer o medico.pular  

    tela.blit(imagem_de_fundo, (0,0)) 

    rel_x = x % imagem_de_fundo.get_rect().width # fazer a tela mexer
    tela.blit(imagem_de_fundo, (rel_x - imagem_de_fundo.get_rect().width,0))
    if rel_x < 640:
        tela.blit(imagem_de_fundo, (rel_x, 0))

    x-=2 #velocidade da tela

    
    todas_as_sprites.draw(tela)
 
    todas_as_sprites.update()

    pygame.display.flip()

    
