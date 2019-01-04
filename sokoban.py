# -*- coding: utf-8 -*-
"""
Created on Mon Dec 24 11:38:22 2018

@author: tisco
"""
import pickle
import pygame


niveis = []

## Lers os niveis a partir do ficheiro
def ler_nivel(nivel):
    with open('niveis.txt') as f:
        while nivel > 0:
            linha = f.readline()
            if linha == '---------------\n':  # acabou de ler nivel
                nivel -= 1
        linhas = []
        for linha in f:
            if linha == '---------------\n':
                break
            linhas.append(linha)
        tipos = (' ', '#', '*', '.')
        altura = len(linhas)
        largura = max(map(len, linhas))-1
        caixotes = []
        paredes=[]
        deposito=[]
        matriz = [[0 for _ in range(largura)] for _ in range(altura)]
        for l in range(altura):
            for c in range(largura):
                if c < len(linhas[l])-1:
                    if linhas[l][c] == '@':
                        jogador = [l, c]
                    elif linhas[l][c] == '$':
                        caixotes.append([l, c])
                    else:
                        matriz[l][c] = tipos.index(linhas[l][c])
                        if linhas[l][c] == '#':
                            paredes.append([l,c])
                        elif linhas[l][c]== '.':
                            deposito.append([l,c])
        return jogador, caixotes, matriz, paredes, deposito

##################################################


def carregar_nivel(nivel):
    global nivel_atual, pos_jogador, pos_caixotes, matriz, screen, pos_paredes, pos_depositos
    nivel_atual = nivel
    pos_jogador, pos_caixotes, matriz, pos_paredes, pos_depositos = ler_nivel(nivel)
    # muda tamanho do ecrã para tamanho do nível
    altura = len(matriz)
    largura = len(matriz[0]) 
    screen = pygame.display.set_mode((largura*40, altura*40))



def jogo(level, theme):
    global pos_caixotes, pos_jogador
    score=0
    tema=theme
    
    ## Abrir ecra e etc
    nivel = level
    carregar_nivel(nivel)
    inicial_pos_jogador = pos_jogador.copy()

    # carregar tema
    
    caixa_img = pygame.image.load(theme + "_caixa.png")
    parede_img = pygame.image.load(theme + "_parede.png")
    jogador_img = pygame.image.load(theme + "_jogador.png")
    deposito_img = pygame.image.load(theme + "_deposito.png")  
             
    
## Ciclo

    sair = False
    while not sair:  
        
        ## Desenhar nível
    
        #Espaço vazio - 0
        #Paredes - 1
        #deposito - 3
        for i, row in enumerate(matriz):
            for j, local in enumerate(row):
                if (i, j) not in pos_caixotes and (i, j) != pos_jogador:
                    if local == 0: #Espaço vazio
                        block = pygame.Surface((40, 40))
                        block.fill((255,255,255))
                        #Tirar as duas linhas em cima e colocar imageload do espaço vazio
                        pos = (40*j, 40*i)
                        screen.blit(block, pos)
                    elif local == 1 or local == 2: #Paredes
                        pos = (40*j, 40*i)
                        screen.blit(parede_img, pos)
                        
                    elif local == 3: #Entregar caixas
                        pos = (40*j, 40*i)
                        screen.blit(deposito_img, pos)
    
        #Caixas
        for pos in pos_caixotes:
            x, y = pos
            pos = (40*y, 40*x)
            screen.blit(caixa_img, pos)
        
        #Jogador
        x, y = pos_jogador
        pos = (40*y, 40*x)
        screen.blit(jogador_img, pos)
    
        pygame.draw.rect(screen, (255, 255, 255), (0, 0, 110, 20))
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, 110, 20), 2)
        screen.blit(font.render("Level: {} / {}".format(nivel,"89"), 1, (0,0,0)), (4, 4))
    
        pygame.display.update()
            
            
        
        # Eventos
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            sair = True
        print(pos_caixotes)
        if event.type == pygame.KEYDOWN:
            # cima, baixo, esquerda, direito
           
            #LEFT
            if event.key == pygame.K_LEFT:
                move=True
                #ver se vai contra a parede
                if [pos_jogador[0], pos_jogador[1]-1] in pos_paredes:
                        move=False
                #ver se vai contra a caixa
                elif [pos_jogador[0], pos_jogador[1]-1] in pos_caixotes:
                    for pos_caixote in pos_caixotes:
                        if pos_caixote == [pos_jogador[0], pos_jogador[1]-1]:
                            caixote=pos_caixote
                    if  [caixote[0],caixote[1]-1] in pos_paredes or [caixote[0],caixote[1]-1] in pos_caixotes:
                            move=False
                    else:
                        caixote[1] -= 1
                        move=True
                if move:
                    pos_jogador[1] -= 1
                    score+=1
                
             #RIGHT
            if event.key == pygame.K_RIGHT:
                move=True
                #ver se vai contra a parede
                if [pos_jogador[0], pos_jogador[1]+1] in pos_paredes:
                        move=False
                #ver se vai contra a caixa
                elif [pos_jogador[0], pos_jogador[1]+1] in pos_caixotes:
                    for pos_caixote in pos_caixotes:
                        if pos_caixote == [pos_jogador[0], pos_jogador[1]+1]:
                            caixote=pos_caixote
                    if  [caixote[0],caixote[1]+1] in pos_paredes or [caixote[0],caixote[1]+1] in pos_caixotes:
                            move=False
                    else:
                        caixote[1] += 1
                        move=True
                if move:
                    pos_jogador[1] += 1
                    score+=1
                    
            #UP
            
            if event.key == pygame.K_UP:
                move=True
                #ver se vai contra a parede
                if [pos_jogador[0]-1, pos_jogador[1]] in pos_paredes:
                        move=False
                #ver se vai contra a caixa
                elif [pos_jogador[0]-1, pos_jogador[1]] in pos_caixotes:
                    for pos_caixote in pos_caixotes:
                        if pos_caixote == [pos_jogador[0]-1, pos_jogador[1]]:
                            caixote=pos_caixote
                    if  [caixote[0]-1,caixote[1]] in pos_paredes or [caixote[0]-1,caixote[1]] in pos_caixotes:
                            move=False
                    else:
                        caixote[0] -= 1
                        move=True
                if move:
                    pos_jogador[0] -= 1
                    score+=1
                
            #DOWN  
            
            if event.key == pygame.K_DOWN:
                move=True
                #ver se vai contra a parede
                if [pos_jogador[0]+1, pos_jogador[1]] in pos_paredes:
                        move=False
                #ver se vai contra a caixa
                elif [pos_jogador[0]+1, pos_jogador[1]] in pos_caixotes:
                    for pos_caixote in pos_caixotes:
                        if pos_caixote == [pos_jogador[0]+1, pos_jogador[1]]:
                            caixote=pos_caixote
                    if  [caixote[0]+1,caixote[1]] in pos_paredes or [caixote[0]+1,caixote[1]] in pos_caixotes:
                            move=False
                    else:
                        caixote[0] += 1
                        move=True
                if move:
                    pos_jogador[0] += 1
                    score+=1
    
            if event.key == pygame.K_n:
                # cheat code: end level
                pos_caixotes = pos_depositos

            print("jogador: ", pos_jogador)
            # escape para sair do jogo
            if event.key == pygame.K_ESCAPE:
                if inicial_pos_jogador == pos_jogador:
                    sair = True
                else:
                    carregar_nivel(nivel)
                    inicial_pos_jogador = pos_jogador.copy()

        
        pos_caixotes.sort()
        pos_depositos.sort()
        
        ## Se o utilizador ganhou, fazer:
        if pos_caixotes == pos_depositos:
            if nivel < 89:
                nivel += 1
            else:
                sair = True
            win()
            carregar_nivel(nivel)
            inicial_pos_jogador = pos_jogador.copy()

        # nivel += 1
        # carregar_nivel(nivel)
        print(score)
        
    #save game
    global foo
    foo = [nivel,tema]
    with open("savegame", "wb") as f:
        pickle.dump(foo, f)
    


#SELECT THEME
    
def menu_theme():
    while True:
        #Cria o ecrã global do jogo
        global screen
        screen = pygame.display.set_mode((600, 600))
        bg = pygame.image.load("desenho_theme.png")
        screen.blit(bg, (0, 0))
        pygame.display.update()

        event = pygame.event.wait()
        if event.type == pygame.MOUSEBUTTONDOWN:
            (j, i) = pygame.mouse.get_pos()
            #standard
            if 96 < j < 223 and 134 < i < 258:
                return "standard"
            
            #rainbow
            if 350 < j < 485 and 134 < i < 258:
                return "rainbow"
            
            #ghost
            if 96 < j < 223 and 366 < i < 500:
                return "ghost"
            
            #space
            if 350 < j < 485 and 366 < i < 500:
                return "space"
        if event.type == pygame.QUIT:
            return "standard"
       
        
#NEXT LEVEL

def win():
    
    screen = pygame.display.set_mode((600, 600))
    bg = pygame.image.load("desenho_complete.png")
    screen.blit(bg, (0, 0))
    pygame.display.update()
    pygame.time.delay(1000)

                

#MENU PRINCIPAL   
                    
def menu(main_theme):
    
## Abrir ecra e etc
    
    while True:
        #Cria o ecrã global do jogo
        global screen
        screen = pygame.display.set_mode((600, 600))
        bg = pygame.image.load("desenho_menu_1.png")
        screen.blit(bg, (0, 0))
        pygame.display.update()

        event = pygame.event.wait()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                break
        if event.type == pygame.MOUSEBUTTONDOWN:
            (j, i) = pygame.mouse.get_pos()
            
            #CONTINUE
            
            if 380 < j < 545 and 150 < i < 210:
                with open("savegame", "rb") as f:
                    foo = pickle.load(f)
                n=foo[0]
                t=foo[1]
                jogo(n,t)

            #NEW GAME
            if 380 < j < 545 and 260 < i < 315:
                jogo(0,main_theme)
            
            #SELECT THEME
            if 380 < j < 545 and 370 < i < 426:
                main_theme = menu_theme()
            
            #EXIT
            if 380 < j < 545 and 475 < i < 533:
                break
        if event.type == pygame.QUIT:
            break

# Main code

pygame.init()
pygame.display.set_caption('Sokoban')

pygame.event.set_allowed(None)
pygame.event.set_allowed(pygame.QUIT)
pygame.event.set_allowed(pygame.MOUSEBUTTONDOWN)
pygame.event.set_allowed(pygame.KEYDOWN)
pygame.key.set_repeat(1, 200) 

pygame.font.init()
font = pygame.font.Font(pygame.font.get_default_font(), 16)

menu("standard")

pygame.quit()