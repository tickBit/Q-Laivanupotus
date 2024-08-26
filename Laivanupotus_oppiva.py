import pygame
import numpy as np
import math
import datetime
from lauta_oppiva import Lauta

"""
    Ideana on aluksi opettaa optimaalisesti peliä pelaava Q-agentti.
    Käytännössä luodaan Q-taulu, jota hyödyntämällä löytyy aina osuma
    pelaajan laivaan. Vain agentin hutilaukaukset ovat satunnaisia
    vaikeusasteen mukaan.

    Jotta agentin pelaaminen ei näytä liian hölmöltä, satunnaisuus
    hutilaukaukseen pienee logaritmisesti sen mukaan, mitä useamman osuman
    agentti on ampunut. 
"""
EPOOKIT = 16*16

SIJOITA_LAIVAT = 0
PELAA = 1
GAME_OVER = 2
MIETI = 3

# käytetään nykyistä aikaa satunnaissiemenenä
np.random.seed(int(round(datetime.datetime.now().timestamp())))

laiva = {1: np.array([[1,1],[1,1]]),
         2: np.array([[1,1,1]]),
         3: np.array([[0,1,0],[1,1,1]]),
         4: np.array([[1,1,1],[1,0,0],[1,0,0]]),
         5: np.array([[1,1,1,1,1]])
         }

# kummallakin pelaajalla laivoissa yhteensä 21 osaa,
# huomaa, että jos muutat laivojen osien määrää, MAX_OSUMAT
# on muutettava myös lauta.py-tiedostoon
MAX_OSUMAT = 21

ALPHA = 0.8
GAMMA = 0.8

# arvoa pienetämällä Q-agentti pelaa heikommin, vastaavasti suurentamalla agentti pelaa paremmin
TRAINING_ROUNDS = 25

q_table = np.zeros([7, 16*16])
epsilons = []
observation = 0
action = 0
eps = 0
train = True

# env.pelilauta3 on omistettu agentin Q-oppimiselle,
# env.pelilauts2:ssa on pelaajan ja agentin siirrot
env = Lauta()

def epsilon_greedy_q_learning_policy(observation, epsilon):
    
    '''
        Palauttaa toiminnon (action) agentille.
        Toiminto valitaan tutkimalla (satunnainen validi paikka) tai hyödyntämällä Q-taulua.

        Aluksi tutkimista tulisi olla enemmän, jotta agentti tulee tutuksi ympäristönsä kanssa.
        Vähitellen kuitenkin Q-taulun hyödyntämistä tulisi olla enemmän.

    '''

    random_number = np.random.random()
    
    # Jos epsilon < satunnaisluku, valitaan seuraava siirto Q-taulusta
    if epsilon < random_number:

        action = np.argmax(q_table[observation, :])
    
    # Tutkiminen: valitaan satunnainen validi paikka
    else:
        action = env.random_action()

    return action

def new_q_value(old_q_value, reward, next_greatest_q_value):
    
    return old_q_value +  ALPHA * (reward + GAMMA * next_greatest_q_value - old_q_value)

def alusta_peli():
    
    q_table = np.zeros([7, 16*16])
    a = 1.75    # epsilon-käyrän laskemisjyrkkyyteen vaikuttava parametri

    # kaava on käytännössä tuulesta temmattu..
    epsilons = np.array([math.exp(-(i*a+(i*0.001))/((EPOOKIT)/2)) for i in range(EPOOKIT)])

    observation = env.reset()
    return observation, q_table, epsilons, 0

game_state = SIJOITA_LAIVAT

# pygame setup
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

pygame.font.init() # you have to call this at the start, 
                   # if you want to use this module.
my_font = pygame.font.SysFont('Sans Serif', 27)
text1 = my_font.render('Pelaa', True, (0, 0, 0))
text2 = my_font.render('Nyt voit pelata painamalla pelaa-painiketta', True, (0, 0, 0))
text3 = my_font.render("GAME OVER - VOITIN! Vaalealla laivojeni sijainnit. Paina hiirellä ikkunassa jatkaaksesi.", True, (0,0,0))
text4 = my_font.render("GAME OVER - VOITIT, HIENOA! Paina hiirellä ikkunassa jatkaaksesi.", True, (0,0,0))
text5 = my_font.render("Tyhjennä", True, (0,0,0))
text6 = my_font.render("Peli käynnissä!", True, (0,0,0))
text7 = my_font.render("Voit sijoittaa laivat", True, (0,0,0))

running = True

playerHits = 0
human_won = False

click = False

valittu_laiva = 0

sijoitetut_laivat = []

bg = pygame.image.load("./Meri-ja-laivat.jpg")
imagerect = bg.get_rect()

def set_ship_to_board(screen, ship, x, y):
                
        try:
            rows = len(list(ship))
            for j in range(rows):
                for i, _ in enumerate(ship[j]):
                    if ship[j][i] != 0:
                        pygame.draw.rect(screen, (180, 120, 120), ((x+i*32), (y+j*32), 32, 32))
        except:
            for i, _ in enumerate(ship):
                pygame.draw.rect(screen, (180, 120, 120), ((x+i*32), (y+j*32), 32, 32))

# pääsilmukka               
while running:

    event_list = pygame.event.get()
    for event in event_list:
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            click = True

            if click:
                mouse_location = pygame.mouse.get_pos()

                if event.button == 3 and valittu_laiva != 0:
                    laiva[valittu_laiva] = np.rot90(laiva[valittu_laiva])

                if game_state == GAME_OVER:

                    if mouse_location[0] >= 0 and mouse_location[0] <= screen.get_width()-1 and mouse_location[1] >= 0 and mouse_location[1] <= screen.get_height() - 1:

                        valittu_laiva = 0
                        human_won = False
                        sijoitetut_laivat = []
                        env.board = np.array([0 for _ in range(16*16)])
                        env.pelilauta = env.board.copy()
                        env.pelilauta2 = env.board.copy()
                        playerHits = 0

                        game_state = SIJOITA_LAIVAT

                        break

                if game_state == SIJOITA_LAIVAT and event.button == 1:
                    
                    # Opeta ja pelaa -painike
                    if mouse_location[0] >= 32 + 32 * 16 + 32 and mouse_location[0] < 32 + 32 * 16 + 32 + 32*5 and mouse_location[1] >= 480 and mouse_location[1] < 480 + 27:
                        
                        if len(sijoitetut_laivat) == 5:
                            env.set_ship1()
                            env.set_ship2()
                            env.set_ship3()
                            env.set_ship4()
                            env.set_ship5()

                            observation, q_table, epsilons, eps = alusta_peli()
                            game_state  = MIETI
                        else:
                            print("Pelaaja ei ole sijoittanut kaikkia laivojaan")

                        break
                    

                    # Vaikeustason valinta hiirellä
                    if mouse_location[0] >= 32 + 50*7 and mouse_location[0] <= 32 + 50*7 + 17 and mouse_location[1] >= 32*17 + 3 and mouse_location[1] <= 32*17 + 3 + 22:
                        vaikeustaso = 1

                    if mouse_location[0] >= 32 + 50*7 + 15 and mouse_location[0] <= 32 + 50*7 + 15 + 17 and mouse_location[1] >= 32*17 + 3 and mouse_location[1] <= 32*17 + 3 + 22:
                        vaikeustaso = 2

                    if mouse_location[0] >= 32 + 50*7 + 30 and mouse_location[0] <= 32 + 50*7 + 30 + 17 and mouse_location[1] >= 32*17 + 3 and mouse_location[1] <= 32*17 + 3 + 22:
                        vaikeustaso = 3

                    if mouse_location[0] >= 32 + 50*7 + 45 and mouse_location[0] <= 32 + 50*7 + 45 + 17 and mouse_location[1] >= 32*17 + 3 and mouse_location[1] <= 32*17 + 3 + 22:
                        vaikeustaso = 4

                    # Tyhjennä-painike
                    if mouse_location[0] >= 32 + 32*16 + 32 and mouse_location[0] < 32 + 32*16 + 32 + 27*5 and mouse_location[1] >= 27*19 and mouse_location[1] < 27*19 + 20:
                        env.board = np.array([0 for _ in range(16*16)])
                        env.pelilauta2 = env.board.copy()
                        sijoitetut_laivat = []
                        break

                    #
                    # Poimitaan laiva
                    #

                    if mouse_location[0] >= 32 + 32 * 16 + 32 and mouse_location[0] < 32 + 32 * 16 + 32 + 32 * 2 and mouse_location[1] >= 32 and mouse_location[1] < 32 + 32 * 2:
                        valittu_laiva = 1
                        break

                    if mouse_location[0] >= 32 + 32 * 16 + 32 and mouse_location[0] < 32 + 32 * 16 + 32 + 32 * 3 and mouse_location[1] >= 32 + 32 * 2 + 32 and mouse_location[1] < 32 + 32 * 2 + 32 + 32:
                        valittu_laiva = 2
                        break

                    if mouse_location[0] >= 32 + 32 * 16 + 32 and mouse_location[0] < 32 + 32 * 16 + 32 + 32 * 3 and mouse_location[1] >= 32 + 32 * 2 + 32 + 32 + 32 and mouse_location[1] < 32 + 32 * 2 + 32 + 32 + 32 + 32 * 2:
                        valittu_laiva = 3
                        break
                    if mouse_location[0] >= 32 + 32 * 16 + 32 and mouse_location[0] < 32 + 32 * 16 + 32 + 32 * 4 and mouse_location[1] >= 32 + 32 * 2 + 32 + 32 + 32 + 32 * 2 + 32 and mouse_location[1] < 32 + 32 * 2 + 32 + 32 + 32 + 32 * 2 + 32 + 32 * 4:
                        valittu_laiva = 4
                        break

                    if mouse_location[0] >= 32 + 32 * 16 + 32 and mouse_location[0] < 32 + 32 * 16 + 32 + 32 * 5 and mouse_location[1] >= 32 + 32 * 2 + 32 + 32 + 32 + 32 * 2 + 32 + 32 * 4 and mouse_location[1] < 32 + 32 * 2 + 32 + 32 + 32 + 32 * 2 + 32 + 32 * 4 + 32:
                        valittu_laiva = 5
                        break

                    if mouse_location[0] >= 32 and mouse_location[0] < 32 + 32*16 and mouse_location[1] >= 32 and mouse_location[1] <= 32 + 32*16:

                        if valittu_laiva not in sijoitetut_laivat and valittu_laiva != 0:

                            if env.ship_at_valid_position(int((mouse_location[0] - 32) / 32), int((mouse_location[1] - 32) / 32), laiva[valittu_laiva]):

                                # Jos päästään tänne, pelaajan laiva voidaan sijoittaa pelikentälle
                                env.set_ship_to_board(laiva[valittu_laiva], int((mouse_location[0] - 32) / 32), int((mouse_location[1] - 32) / 32), 1)
                                env.pelilauta2 = env.board.copy()

                                sijoitetut_laivat.append(valittu_laiva)
                            
                                break

                    click = False
                    break
                    

                if game_state == PELAA:    

                    # tarkistetaan, onko pointteri pelilaudan sisällä
                    if mouse_location[0] >= 32 and mouse_location[1] >= 32 and mouse_location[0] < 32 + 32*16 and mouse_location[1] < 32 + 32*16:

                        board = env.pelilauta2.reshape(16,16)

                        upotusX = int((mouse_location[0] - 32) / 32)
                        upotusY = int((mouse_location[1] - 32) / 32)

                        """
                            Kun pelilaidalle on suoritettu reshape(16,16),
                            edustaa y-koordinaatti riviä ja x-koordinaatti saraketta.
                            Siksi board[upotusY, upotusX] antaa oikean paikan.
                        """
                        if board[upotusY, upotusX] not in [4, 0]:
                            print("Valitse jokin muu ruutu.")
                            break

                        elif board[upotusY,upotusX] == 4:
                            playerHits += 1
                            env.mark_hit(upotusX + upotusY*16)

                        elif board[upotusY,upotusX] == 0:
                            env.mark_miss(upotusX + upotusY*16)

                        if playerHits == MAX_OSUMAT:
                            game_state = GAME_OVER
                            human_won = True
                            break

                        game_state = MIETI

                    click = False
                    break
    
    if game_state == SIJOITA_LAIVAT or game_state == PELAA or game_state == GAME_OVER:
         # Taustaväri
        pygame.draw.rect(screen, (200,200,255),(0, 0, 800, 600))

        # Piirretään AI-generoitu taustakuva
        screen.blit(bg, (32,32), imagerect)

    # Liikutetaan valittua laivaa
    if valittu_laiva != 0 and game_state == SIJOITA_LAIVAT:

        mouse_location = pygame.mouse.get_pos()

        set_ship_to_board(screen, laiva[valittu_laiva], mouse_location[0], mouse_location[1])


    if game_state == PELAA or game_state == SIJOITA_LAIVAT or game_state == GAME_OVER:


        board = env.pelilauta2.reshape(16,16)

        for j in range(16):
            for i in range(16):

                # ihmispelaajan laiva
                if board[j][i] == 1:
                    pygame.draw.rect(screen, (180,120,120), (32 + i*32, 32 + j*32, 32, 32))
                
                # osuma ihmispelaajan laivaan
                if board[j][i] == 2:
                    pygame.draw.rect(screen, (255,0,0), (32 + i*32, 32 + j*32, 32, 32))

                # osuma agentin laivaan
                if board[j][i] == 5:
                    pygame.draw.rect(screen, (10,255,10), (32 + i*32, 32 + j*32, 32, 32))
                        
                # pelaajan hutilaukaus
                if board[j][i] == 6:
                    pygame.draw.rect(screen, (100,100,100), (32 + i*32, 32 + j*32, 32, 32))

                # agentin hutilaukaus
                if board[j][i] == 3:
                    pygame.draw.rect(screen, (100,40,40), (32 + i*32, 32 + j*32, 32, 32))

                if game_state == GAME_OVER:
                    if board[j][i] == 4:
                        # jos agentti voitti pelin, niin näytetään agentin laivat
                        pygame.draw.rect(screen, (200,255,200), (32 + i*32, 32 + j*32, 32, 32))

    """
        Q-agentti "miettii" eli oppii
    """
    if game_state == MIETI:

        # Jos valittu siirto johtaisi tilanteeseen, missä ei tehtäisi uutta siirtoa, niin silmukassa pyöritään,
        # kunnes uusi aito uusi siirto tapahtuu. Esim. jos Q-taulusta otettu siirto johtaisi agentin oman laivan
        # päälle, niin tehdään siirto, kunnes siirto osuu laudalle
        again = True
        
        while again:
            for i in range(TRAINING_ROUNDS):
                epsilon = epsilons[eps]


                # Yleisesti epsilon greedy action selection -toimintona tunnettu mekanismi,
                # jolla valitaan tutkitaanko (satunnainen paikkanvalinta) vai hyödynnetäänkö Q-taulua
                action = epsilon_greedy_q_learning_policy(observation, epsilon)

                # Toteuteaan toiminto, ts. agentti pelaa peliä, ja poimitaan uusi havainto, palkkio ja
                # tieto siitä, onko peli pelattu läpi

                if i == TRAINING_ROUNDS-1:
                    new_observation, reward, again = env.step(action)
                else:
                    new_observation, reward, again = env.step_train(action)
                # Haetaan vanha (nykyinen) Q-arvo
                old_q_value = q_table[observation,action]  

                # Otetaan seuraava suurin Q-arvo
                next_greatest_q_value = np.max(q_table[observation, :])

                # Lasketaan uusi q-arvo
                new_q = new_q_value(old_q_value, reward, next_greatest_q_value)   

                # Päivitetään Q-taulua
                q_table[observation,action] = new_q
               
                # Asetetaan uusi tila nykyiseksi tilaksi
                observation = new_observation

        game_state = PELAA
        eps += 1

        # Voittiko agentti?
        if env.agent_won():
            human_won = False
            game_state = GAME_OVER
        
    # Tulostetaan game over -tapauksen eri tekstit voittjasta riippuen
    if game_state == GAME_OVER:
        if human_won == False:
            screen.blit(text3,(16, 32*18))
        else:
            screen.blit(text4,(32 , 32*18))

    # Laiva 1
    pygame.draw.rect(screen, (200,100,255),(32 + 16*32 + 32, 32, 32*2, 32*2))

    # Laiva 2
    pygame.draw.rect(screen, (200,100,255),(32 + 16*32 + 32, 32*4, 32*3, 32))

    # Laiva 3
    pygame.draw.rect(screen, (200,100,255),(32 + 17*32 + 32, 32*6, 32, 32))   
    pygame.draw.rect(screen, (200,100,255),(32 + 16*32 + 32, 32*7, 32*3, 32))

    # Laiva 4
    pygame.draw.rect(screen, (200,100,255),(32 + 16*32 + 32, 32*9, 32, 32*3))
    pygame.draw.rect(screen, (200,100,255),(32 + 16*32 + 32*2, 32*9, 32*2, 32))

    # Laiva 5
    pygame.draw.rect(screen, (200,100,255),(32 + 16*32 + 32, 32*13, 32*5, 32))

    # Pelaa-painike
    if len(sijoitetut_laivat) == 5 and game_state == SIJOITA_LAIVAT:
        pygame.draw.rect(screen, (20,200,80),(32 + 32*16 + 32, 32*15, 27*5, 20))
    elif len(sijoitetut_laivat) < 5 or game_state != SIJOITA_LAIVAT:
        pygame.draw.rect(screen, (200,20,80),(32 + 32*16 + 32, 32*15, 27*5, 20))

    screen.blit(text1, (32 + 32*18 + 10, 32*15))

    # Tyhjennä lauta -painike
    if len(sijoitetut_laivat) > 0 and game_state == SIJOITA_LAIVAT:
        pygame.draw.rect(screen, (20,200,80),(32 + 32*16 + 32, 27*19, 27*5, 20))
    else:
        pygame.draw.rect(screen, (200,20,80), (32 + 32*16 + 32, 27*19, 27*5, 20))

    screen.blit(text5, (32 + 32 * 16 + 57, 27*19))

    # Tulostetaan tekstejä
    if game_state == SIJOITA_LAIVAT and len(sijoitetut_laivat) < 5:
        screen.blit(text7, (32, 32*18))
    elif game_state == SIJOITA_LAIVAT and len(sijoitetut_laivat) == 5:
        screen.blit(text2, (32, 32*17))

    if game_state == PELAA:
        screen.blit(text6, (32, 32*18))

    clock.tick(60)  # FPS

    # flip(): näytetään kaksoispuskuroinnissa bufferiin piirretty
    pygame.display.flip()


pygame.quit()