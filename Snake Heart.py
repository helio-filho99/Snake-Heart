import pygame, sys, random
from pygame.math import Vector2

class COBRA:
    def __init__(self):
        self.corpo = [Vector2(5, 10),Vector2(4,10),Vector2(3,10)]
        self.direcao = Vector2(0,0)
        self.novo_bloco = False

        self.cabeca_cima = pygame.image.load('Graphics/cabeca_cima.png').convert_alpha()
        self.cabeca_baixo = pygame.image.load('Graphics/cabeca_baixo.png').convert_alpha()
        self.cabeca_direita = pygame.image.load('Graphics/cabeca_direita.png').convert_alpha()
        self.cabeca_esquerda = pygame.image.load('Graphics/cabeca_esquerda.png').convert_alpha()

        self.rabo_cima = pygame.image.load('Graphics/rabo_cima.png').convert_alpha()
        self.rabo_baixo = pygame.image.load('Graphics/rabo_baixo.png').convert_alpha()
        self.rabo_direita = pygame.image.load('Graphics/rabo_direita.png').convert_alpha()
        self.rabo_esquerda = pygame.image.load('Graphics/rabo_esquerda.png').convert_alpha()

        self.corpo_vertical = pygame.image.load('Graphics/corpo_vertical.png').convert_alpha()
        self.corpo_horizontal = pygame.image.load('Graphics/corpo_horizontal.png').convert_alpha()

        self.corpo_superior_direito = pygame.image.load('Graphics/corpo_superior_direito.png').convert_alpha()
        self.corpo_superior_esquerdo = pygame.image.load('Graphics/corpo_superior_esquerdo.png').convert_alpha()
        self.corpo_botao_direito = pygame.image.load('Graphics/corpo_botao_direito.png').convert_alpha()
        self.corpo_botao_esquerdo = pygame.image.load('Graphics/corpo_botao_esquerdo.png').convert_alpha()
        self.som_triturar = pygame.mixer.Sound('Som/Som_triturar.wav')

    def draw_cobra(self):
        self.update_cabeca_graphics()
        self.update_rabo_graphics()

        for index,bloco in enumerate(self.corpo):
            x_pos = int(bloco.x * tamanho_da_celula)
            y_pos = int(bloco.y * tamanho_da_celula)
            bloco_retangulo = pygame.Rect(x_pos,y_pos,tamanho_da_celula,tamanho_da_celula)

            if index == 0:
                tela.blit(self.cabeca,bloco_retangulo)
            elif index == len(self.corpo) - 1:
                tela.blit(self.rabo, bloco_retangulo)
            else:
                bloco_anterior = self.corpo[index + 1] - bloco
                bloco_posterior = self.corpo[index - 1] - bloco
                if bloco_anterior.x == bloco_posterior.x:
                    tela.blit(self.corpo_vertical, bloco_retangulo)
                elif bloco_anterior.y == bloco_posterior.y:
                    tela.blit(self.corpo_horizontal, bloco_retangulo)
                else:
                    if bloco_anterior.x == -1 and bloco_posterior.y == -1 or bloco_anterior.y == -1 and bloco_posterior.x == -1:
                        tela.blit(self.corpo_superior_esquerdo,bloco_retangulo)
                    elif bloco_anterior.x == -1 and bloco_posterior.y == 1 or bloco_anterior.y == 1 and bloco_posterior.x == -1:
                        tela.blit(self.corpo_botao_esquerdo,bloco_retangulo)
                    elif bloco_anterior.x == 1 and bloco_posterior.y == -1 or bloco_anterior.y == -1 and bloco_posterior.x == 1:
                        tela.blit(self.corpo_superior_direito,bloco_retangulo)
                    elif bloco_anterior.x == 1 and bloco_posterior.y == 1 or bloco_anterior.y == 1 and bloco_posterior.x == 1:
                        tela.blit(self.corpo_botao_direito,bloco_retangulo)


    def update_cabeca_graphics(self):
        cabeca_relacao = self.corpo[1] - self.corpo[0]
        if cabeca_relacao == Vector2(1,0): self.cabeca = self.cabeca_esquerda
        elif cabeca_relacao == Vector2(-1, 0): self.cabeca = self.cabeca_direita
        elif cabeca_relacao == Vector2(0, 1): self.cabeca = self.cabeca_cima
        elif cabeca_relacao == Vector2(0, -1): self.cabeca = self.cabeca_baixo

    def update_rabo_graphics(self):
        rabo_relacao = self.corpo[-2] - self.corpo[-1]
        if rabo_relacao == Vector2(1, 0): self.rabo = self.rabo_esquerda
        elif rabo_relacao == Vector2(-1, 0): self.rabo = self.rabo_direita
        elif rabo_relacao == Vector2(0, 1): self.rabo = self.rabo_cima
        elif rabo_relacao == Vector2(0, -1): self.rabo = self.rabo_baixo

    def mover_cobra(self):
        if self.novo_bloco == True:
            copia_corpo = self.corpo[:]
            copia_corpo.insert(0, copia_corpo[0] + self.direcao)
            self.corpo = copia_corpo[:]
            self.novo_bloco = False
        else:
            copia_corpo = self.corpo[:-1]
            copia_corpo.insert(0,copia_corpo[0] + self.direcao)
            self.corpo = copia_corpo[:]

    def adicionar_bloco(self):
        self.novo_bloco = True

    def toque_triturar_som(self):
        self.som_triturar.play()

    def reset(self):
        self.corpo = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.direcao = Vector2(0, 0)

class CORACAO:
    def __init__(self):
        self.randomize()

    def draw_coracao(self):
        coracao_retangulo = pygame.Rect(int(self.pos.x * tamanho_da_celula),int(self.pos.y * tamanho_da_celula),tamanho_da_celula,tamanho_da_celula)
        tela.blit(coracao, coracao_retangulo)
        #pygame.draw.rect(tela,(126,166,114),coracao_retangulo)

    def randomize(self):
        self.x = random.randint(0, numero_da_celula - 1)
        self.y = random.randint(0, numero_da_celula - 1)
        self.pos = pygame.math.Vector2(self.x,self.y)

class MAIN:
    def __init__(self):
        self.cobra = COBRA()
        self.coracao = CORACAO()

    def update(self):
        self.cobra.mover_cobra()
        self.checar_colisao()
        self.checar_falha()

    def draw_elementos(self):
        self.draw_grama()
        self.coracao.draw_coracao()
        self.cobra.draw_cobra()
        self.draw_score()

    def checar_colisao(self):
        if self.coracao.pos == self.cobra.corpo[0]:
            self.coracao.randomize()
            self.cobra.adicionar_bloco()
            self.cobra.toque_triturar_som()

        for bloco in self.cobra.corpo[1:]:
            if bloco == self.coracao.pos:
                self.coracao.randomize()

    def checar_falha(self):
        if not 0 <= self.cobra.corpo[0].x < numero_da_celula or not 0 <= self.cobra.corpo[0].y < numero_da_celula:
            self.game_over()

        for bloco in self.cobra.corpo[1:]:
            if bloco == self.cobra.corpo[0]:
                self.game_over()

    def game_over(self):
        self.cobra.reset()

    def draw_grama(self):
        cor_da_grama = (167,209,61)
        for fileira in range(numero_da_celula):
            if fileira % 2 == 0:
                for col in range(numero_da_celula):
                    if col % 2 == 0:
                        grama_retangulo = pygame.Rect(col * tamanho_da_celula,fileira * tamanho_da_celula,tamanho_da_celula,tamanho_da_celula)
                        pygame.draw.rect(tela,cor_da_grama,grama_retangulo)
            else:
                for col in range(tamanho_da_celula):
                    if col % 2 != 0:
                        grama_retangulo = pygame.Rect(col * tamanho_da_celula, fileira * tamanho_da_celula, tamanho_da_celula, tamanho_da_celula)
                        pygame.draw.rect(tela, cor_da_grama, grama_retangulo)

    def draw_score(self):
        texto_score = str(len(self.cobra.corpo) - 3)
        superficie_score = fonte_jogo.render(texto_score,True,(56,74,12))
        score_x = int(tamanho_da_celula * numero_da_celula - 60)
        score_y = int(tamanho_da_celula * numero_da_celula - 40)
        retangulo_score = superficie_score.get_rect(center = (score_x,score_y))
        coracao_retangulo = coracao.get_rect(midright = (retangulo_score.left,retangulo_score.centery))
        retangulo_background = pygame.Rect(coracao_retangulo.left,coracao_retangulo.top,coracao_retangulo.width + retangulo_score.width + 6,coracao_retangulo.height)

        pygame.draw.rect(tela,(167,209,61),retangulo_background)
        tela.blit(superficie_score,retangulo_score)
        tela.blit(coracao,coracao_retangulo)
        pygame.draw.rect(tela,(56,74,12),retangulo_background,2)

pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()
tamanho_da_celula = 40
numero_da_celula = 20
tela = pygame.display.set_mode((numero_da_celula * tamanho_da_celula, numero_da_celula * tamanho_da_celula))
relogio = pygame.time.Clock()
coracao = pygame.image.load('Graphics/coracao.png').convert_alpha()
fonte_jogo = pygame.font.Font('Fonte/PoetsenOne-Regular.ttf', 35)

TELA_UPDATE = pygame.USEREVENT
pygame.time.set_timer(TELA_UPDATE, 150)

main_game = MAIN()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == TELA_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if main_game.cobra.direcao.y != 1:
                    main_game.cobra.direcao = Vector2(0,-1)
            if event.key == pygame.K_RIGHT:
                if main_game.cobra.direcao.x != -1:
                    main_game.cobra.direcao = Vector2(1,0)
            if event.key == pygame.K_DOWN:
                if main_game.cobra.direcao.y != -1:
                    main_game.cobra.direcao = Vector2(0,1)
            if event.key == pygame.K_LEFT:
                if main_game.cobra.direcao.x != 1:
                    main_game.cobra.direcao = Vector2(-1,0)

    tela.fill((175, 215, 70))
    main_game.draw_elementos()
    pygame.display.update()
    relogio.tick(60)
