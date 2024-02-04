import pygame
import numpy as np
import sys
import math
import datetime
from lauta import Lauta

"""
    Ideana on aluksi opettaa optimaalisesti peliä pelaava Q-agentti.
    Käytännössä luodaan Q-taulu, jota hyödyntämällä löytyy aina osuma
    pelaajan laivaan. Vain agentin hutilaukaukset ovat satunnaisia
    vaikeusasteen mukaan.

    Jotta agentin pelaaminen ei näytä liian hölmöltä, satunnaisuus
    hutilaukaukseen pienee logaritmisesti sen mukaan, mitä useamman osuman
    agentti on ampunut. 
"""

SIJOITA_LAIVAT = 0
PELAA = 1
GAME_OVER = 2
OPETA = 3

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

ALPHA = 0.9
GAMMA = 0.45

q_table = np.zeros([7, 16*16])

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


game_state = SIJOITA_LAIVAT

# pygame setup
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

pygame.font.init() # you have to call this at the start, 
                   # if you want to use this module.
my_font = pygame.font.SysFont('Sans Serif', 27)
text1 = my_font.render('Opeta ja pelaa', True, (0, 0, 0))
text2 = my_font.render('Nyt voit pelata', True, (0, 0, 0))
text3 = my_font.render("GAME OVER - VOITIN! Vaalealla laivojeni sijainnit. Paina hiirellä ikkunassa jatkaaksesi.", True, (0,0,0))
text4 = my_font.render("GAME OVER - VOITIT, HIENOA! Paina hiirellä ikkunassa jatkaaksesi.", True, (0,0,0))
text5 = my_font.render("Tyhjennä", True, (0,0,0))
text6 = my_font.render("Valitse vaikeustaso ennen opettamista: 1 2 3 4", True, (0,0,0))
text7 = my_font.render("Voit sijoittaa laivat", True, (0,0,0))

running = True

playerHits = 0
human_won = False

click = False

valittu_laiva = 0

# vaikeustaso = 1..4, 4 vaikein
vaikeustaso = 1

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

    # Taustaväri
    pygame.draw.rect(screen, (200,200,255),(0, 0, 800, 600))

    # Piirretään AI-generoitu taustakuva
    screen.blit(bg, (32,32), imagerect)
    
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
                        AIHits = 0
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

                            game_state = OPETA

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
                        env.pelilauta = env.board.copy()
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
                                env.pelilauta = env.board.copy()

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

                        # haetaan opetusvaiheessa määritetyn Q-taulun seuraava arvo
                        action = np.argmax(q_table[observation,:])

                        actX = action % 16
                        actY = action // 16

                        AIHits = env.hits_of_agent

                        # Kokeillaan 5 kertaa arpoa satunnainen hutilaukaus.
                        # Jollei onnistu, otetaan optimaalinen siirto Q-taulusta
                        # Satunnaisuutta voisi hallita elegantimminkin...
                        Q_table_used = False

                        for i in range(5):

                            # logaritminen pelin vaikeutuminen sen perusteella, mitä useamman osuman agentti on saanut              
                            random_luku = np.random.randint(0, round((math.log10(MAX_OSUMAT-AIHits+1)) * (5-vaikeustaso) * 1.5) + 1)

                            # 1:llä negatoidaan arvo
                            rnd_minus_plus = np.random.randint(0,2)
                            rndX = random_luku

                            if rnd_minus_plus == 1: rndX = -rndX
                        
                            rnd_minus_plus = np.random.randint(0,2)
                            rndY = random_luku
                            if rnd_minus_plus == 1: rndY = -rndY
                  
                            actX += rndX
                            actY += rndY

                            if actX < 0: actX += np.random.randint((-actX)*2+1)
                            if actY < 0: actY += np.random.randint((-actY)*2+1)
                            if actX > 15: actX -= np.random.randint((actX-15)*2+1)
                            if actY > 15: actY -= np.random.randint((actY-15)*2+1)
                            
                            try:
                                # Säkällä agentti ei saa osua, jotta Q-taulu ei mene sekaisin.
                                # Jos säkällä tulisi osuma, osuma poimitaan seuraava osuma Q-taulusta. Ks. alla.
                                #
                                # Säkälaukaukset sallittuja vain tyhjiin ruutuihin
                                # env.pelilauta edustaa Q-agentin pelaamista Q-taulun tilanteesta
                                # env.pelilauta2 edustaa ihmispelaajan panosta peliin, johon myös Q-agentin
                                # hutilaukset tulevat 
                                if env.pelilauta[actX + actY * 16] == 0 and env.pelilauta2[actX + actY * 16] == 0:
                                    env.pelilauta2[actX + actY * 16] = 3
                                    #print(f"Arovttiin huti kierroksella {i+1} / 5.")
                                    break
                            
                                # ..kuitenkin, jos säkällä satutaan osumaan, on osuma haettava Q-taulusta, jossa
                                # seuraava osumapaikka ei välttämättä ole ruudussa, johon satunnaisesti osuttiin
                                if env.pelilauta2[actX + actY * 16] == 1:
                                    #print("Säkällä osuma.\nOsumaan hyödynnetään Q-taulua, mutta ei välttämättä säkäpositiosta.")
                                    #print()
                                    Q_table_used = True
                                    break
                            except:
                                #print("Ei korjausta. Hyödynnetään Q-taulua.")
                                #print()

                                if i == 4: Q_table_used = True

                        # Vaikka ihmispelaaja aloittaa, Q-agentti ei saa tasoittavaa vuoroaan.
                        # Jos ihminen tuhoaa kaikki agentin laivat, agentti ei saa enää tehdä siirtoa.
                        if Q_table_used and human_won == False:
                            # step-metodi hakee pelilaudalta seuraavan optimaalisen siirron
                            # käyttää env.pelilauta-lautaa

                            observation, _, done, _  = env.step(action)
                            env.pelilauta2[action] = 2  # päivtetään sama tilanne env.pelilauta2-lautaaan

                            if done:
                                game_state = GAME_OVER
                                human_won = False
                                
                            # Jos agentti on osunut pelaajan laivaan, paikka merkitään Q-taulussa mahd. itseisarvoltaan
                            # mahdollisimman suurella negatiivisella arvolla, jotta samaa ruutua ei valita uudelleen
                            q_table[observation,action] = -np.inf

                            #print("Q-taulusta osuma.")

                        else:                           
                            done = False

                        
                        # Voittiko agentti?
                        if env.agent_won():
                            human_won = False
                            game_state = GAME_OVER
                            break
                    
                    click = False
                    break

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
        Q-agentin opettaminen.
        Tehdään pienimuotoinen grid search toivottavasti optimaalisen pelin löytämiseksi
    """
    if game_state == OPETA:
                
        print("Opetusprosessi alkoi...")

        optimal_Q_table_found = False
        episode = 0
        agents_skill = 0

        a = 1.75    # epsilon-käyrän laskemisjyrkkyyteen vaikuttava parametri

        # Grid search optimaalisen Q-taulun löytämiseksi.
        # Tämä siksi, että käytetään satunnaissiementä.
        # 
        # Maksimi arvo 10000 on suurehko, mutta usein ainakin itselläni optimaalinen Q-taulu
        # löytyy jo ennen kuin kaikki ensimmäiset 50 epookkia on käyty läpi
        for epookit in np.arange(50, 10000, 10):
            
            print("Opetuskierros alkoi. Epookkeja max:", epookit)

            q_table = np.zeros([7, 16*16])

            # kaava on käytännössä tuulesta temmattu..
            epsilons = np.array([math.exp(-(i*a+(i*0.001))/((epookit)/2)) for i in range(epookit)])

            for episode in range(1, epookit+1, 1):
    
                # Ympäristön resetoiminen. Tämä tulee tehdä aina uuden pelin alkaessa alusta.
                observation = env.reset()
                
                done = False
                human_won = False

                epsilon = epsilons[episode-1]

                # pelataan peliä, kunnes peli pelattu loppuun
                while not done:

                    # opetusvaiheen satunnaispelaaja (pelilauta)
                    done = env.simulated_human_player_step()

                    # satunnaispelaaja voitti
                    if done:
                        human_won = True
                        break

                    # Yleisesti epsilon greedy action selection -toimintona tunnettu mekanismi,
                    # jolla valitaan tutkitaanko (satunnainen paikkanvalinta) vai hyödynnetäänkö Q-taulua
                    action = epsilon_greedy_q_learning_policy(observation, epsilon)

                    # Toteuteaan toiminto, ts. agentti pelaa peliä, ja poimitaan uusi havainto, palkkio ja
                    # tieto siitä, onko peli pelattu läpi

                    # HUOM! Opetusvaiheessa saatetaan ampua myös omaan laivaan, jolloin ihmis/satunnaispelaaja
                    # saa tililleen osuman. Siksi alla palautetaan myös tieto "human_won"
                    new_observation, reward, done, human_won = env.step(action)

                    if human_won:
                        break

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


                if human_won == False:
                    observation = env.reset_play()

                    test_done = False
                    kierrokset = 0
                    q_table_test = q_table.copy()
                
                    agent_skill = 0
                    optimal_Q_table_found = False

                    while not test_done:

                        # testipelaamisvaiheen satunnaispelaaja (pelilauta2)
                        test_done = env.simulated_human_player_step_play()
                        if test_done:
                            #print("Satunnaispelaaja voitti.")
                            break
                        
                        action = np.argmax(q_table_test[observation, :])
                        observation, test_done = env.step_play(action)
                        if env.pelilauta2[action] == 2: q_table_test[observation,action] = -np.inf

                        kierrokset += 1
                        agent_skill += 1

                        if test_done:
                            #print("Agentti pelasi pelin loppuun.")
                            if kierrokset == MAX_OSUMAT: optimal_Q_table_found = True
                            break

                if episode % 50 == 0: print("   Epookki", episode)

                if optimal_Q_table_found == True:
                    print("Optimaalinen Q-taulu löytyi.")
                    break    
            
            if optimal_Q_table_found: break
        
        print("Opetus loppui.")
        
        # tämän ei pitäisi koskaan toteutua...
        if optimal_Q_table_found == False:
            print("Optimaalista Q-taulua ei löytynyt. Valitettavaa, sillä peli ei voi toimia. Poistutaan...")
            sys.exit(0)

        print("Agentti pelaa 21 palasta", agent_skill,"kierroksessa, kun epookkeja oli yhteensä", epookit,f"\nOptimaalinen pelikierros löytyi näistä epookilla {episode}.")
        print("Peli alkakoon!")
        print()

        game_state = PELAA
        
        _ = env.reset_play()
        observation = env.reset()   # 1. havainto pelilaudalta, jossa on vain sijoitetut laivat,
                                    # tämä on ollut myös agentin opetuksessa lähtökohta
        
    if game_state == PELAA:
        screen.blit(text2, (32, 32*18))

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

    # Opeta-painike
    if len(sijoitetut_laivat) == 5 and game_state == SIJOITA_LAIVAT:
        pygame.draw.rect(screen, (20,200,80),(32 + 32*16 + 32, 32*15, 27*5, 20))
    elif len(sijoitetut_laivat) < 5 or game_state != SIJOITA_LAIVAT:
        pygame.draw.rect(screen, (200,20,80),(32 + 32*16 + 32, 32*15, 27*5, 20))

    screen.blit(text1, (32 + 32*16 + 32 + 4, 32*15))

    # Tyhjennä lauta -painike
    if len(sijoitetut_laivat) > 0 and game_state == SIJOITA_LAIVAT:
        pygame.draw.rect(screen, (20,200,80),(32 + 32*16 + 32, 27*19, 27*5, 20))
    else:
        pygame.draw.rect(screen, (200,20,80), (32 + 32*16 + 32, 27*19, 27*5, 20))

    screen.blit(text5, (32 + 32 * 16 + 57, 27*19))

    # Vaikeustasopainikkeet ja tekstit
    if game_state == SIJOITA_LAIVAT:
        pygame.draw.rect(screen, (45,200,55), (32+50*7, 32*17+3, 17,22))
        pygame.draw.rect(screen, (100,195,55), (32+50*7+15, 32*17+3, 17, 22))
        pygame.draw.rect(screen, (195,100,55), (32+50*7+30, 32*17+3, 17,22))
        pygame.draw.rect(screen, (255,45,55), (32+50*7+45, 32*17+3, 17, 22))
        screen.blit(text6, (32, 32*17+4))
        screen.blit(text7, (32, 32*18))
        
        # piirretään viiva valitun vaikeustason alle
        if vaikeustaso == 1:
            pygame.draw.line(screen, (0,0,255), (32+50*7,32*17+3+22), (32+50*7+14,32*17+3+22), width=1)
        elif vaikeustaso == 2:
            pygame.draw.line(screen, (0,0,255), (32+50*7+15,32*17+3+22), (32+50*7+15+14,32*17+3+22), width=1)
        elif vaikeustaso == 3:
            pygame.draw.line(screen, (0,0,255), (32+50*7+30,32*17+3+22), (32+50*7+30+14,32*17+3+22), width=1)
        elif vaikeustaso == 4:
            pygame.draw.line(screen, (0,0,255), (32+50*7+45,32*17+3+22), (32+50*7+45+14,32*17+3+22), width=1)

    # flip(): näytetään kaksoispuskuroinnissa bufferiin piirretty
    pygame.display.flip()

    clock.tick(30)  # FPS

pygame.quit()