import numpy as np

MAX_OSUMAT = 21

class Lauta:
    
    def __init__(self):
        self.agenttilaiva = {1: np.array([[1,1],[1,1]]),
         2: np.array([[1,1,1]]),
         3: np.array([[0,1,0],[1,1,1]]),
         4: np.array([[1,1,1],[1,0,0],[1,0,0]]),
         5: np.array([[1,1,1,1,1]])
         }

        self.hits_of_agent = 0
        self.hits_of_human = 0
        
        self.hits_of_agent_play = 0
        self.hits_of_human_play = 0

        self.board = np.array([0 for _ in range(16*16)])
        self.pelilauta = np.array([0 for _ in range(16*16)])
        self.pelilauta2 = np.array([0 for _ in range(16*16)])
        self.pelilauta2 = np.array([0 for _ in range(16*16)])

    def get_q_table(self):
        return self.q_table
    
    def set_q_table(self, q_table):
        self.q_table = q_table

    def mark_hit(self, pos):
        self.pelilauta2[pos] = 5

    def mark_miss(self, pos):
        self.pelilauta2[pos] = 6

    def get_board(self):
        return self.board
    
    def get_pelilauta(self):
        return self.pelilauta
    
    def put_ships_to_board(self, ships):
        self.board = ships.copy()

    def set_ship_to_board(self, ship, x, y, data):
                
        dim = ship.shape
        
        for rj in range(dim[1]):
            for ri in range(dim[0]):
                if ship[ri][rj] == 1: self.board[rj+x+(ri+y)*16] = data

        self.pelilauta = self.board.copy()
        self.pelilauta2 = self.board.copy()

    """
        Arvotaan agentin laivoille paikat.
        Pähkinän kuoressa sanottuna pelilautaan tutkitaan agentin laivan kokoisissa paloissa.
        Yksittäinen tällainen pala on näyte (sample), jolle tehdään looginen and-operaatio
        agentin laivamatriisin kanssa. Jos tuloksena olevan matriisin summa = 0, niin paikka on vapaa.

    """
    def set_ship1(self):

        board = self.board.copy().reshape(16,16)
        board[board == 4] = 1
        
        agenttilaiva = self.agenttilaiva[1].copy()
        dim = agenttilaiva.shape

        emptys = []

        for j in range(16-dim[1]):
            for i in range(16-dim[0]):
                sample = board[i:(dim[0]+i),j:(dim[1]+j)]
                m = np.ma.bitwise_and(agenttilaiva, sample)
                if np.sum(m) == 0:
                    emptys.append((j,i))

        p = np.random.choice(np.arange(0,len(emptys)))
        p = emptys[p]

        self.set_ship_to_board(agenttilaiva.copy(), p[0], p[1], 4)

        self.pelilauta = self.board.copy()

    def set_ship2(self):

        board = self.board.copy().reshape(16,16)
        board[board == 4] = 1
        
        random_rotation = np.random.randint(0,2)
        
        agenttilaiva = self.agenttilaiva[2].copy()

        if random_rotation == 1:
            agenttilaiva = np.rot90(agenttilaiva)

        dim = agenttilaiva.shape

        emptys = []

        for j in range(16-dim[1]):
            for i in range(16-dim[0]):
                sample = board[i:(dim[0]+i),j:(dim[1]+j)]
                m = np.ma.bitwise_and(agenttilaiva, sample)
                if np.sum(m) == 0:
                    emptys.append((j,i))

        p = np.random.choice(np.arange(0,len(emptys)))
        p = emptys[p]

        self.set_ship_to_board(agenttilaiva.copy(), p[0], p[1], 4)

        self.pelilauta = self.board.copy()

    def set_ship3(self):

        board = self.board.reshape(16,16).copy()
        board[board == 4] = 1

        random_rotation = np.random.randint(0,4)
        agenttilaiva = self.agenttilaiva[3].copy()
    
        if random_rotation == 1:
            agenttilaiva = np.rot90(agenttilaiva)
           

        elif random_rotation == 2:
            agenttilaiva = np.rot90(agenttilaiva)
            agenttilaiva = np.rot90(agenttilaiva)
           

        elif random_rotation == 3:
            agenttilaiva = np.rot90(agenttilaiva)
            agenttilaiva = np.rot90(agenttilaiva)
            agenttilaiva = np.rot90(agenttilaiva)

        
        dim = agenttilaiva.shape

        emptys = []

        for j in range(16-dim[1]):
            for i in range(16-dim[0]):
                sample = board[i:(dim[0]+i),j:(dim[1]+j)]
                m = np.ma.bitwise_and(agenttilaiva, sample)
                if np.sum(m) == 0:
                    emptys.append((j,i))

        p = np.random.choice(np.arange(0,len(emptys)))
        p = emptys[p]

        self.set_ship_to_board(agenttilaiva.copy(), p[0], p[1], 4)
        self.pelilauta = self.board.copy()

    def set_ship4(self):

        board = self.board.reshape(16,16).copy()
        board[board == 4] = 1

        random_rotation = np.random.randint(0,4)
        agenttilaiva = self.agenttilaiva[4].copy()

        
        if random_rotation == 1:
            agenttilaiva = np.rot90(agenttilaiva)
           

        elif random_rotation == 2:
            agenttilaiva = np.rot90(agenttilaiva)
            agenttilaiva = np.rot90(agenttilaiva)
           

        elif random_rotation == 3:
            agenttilaiva = np.rot90(agenttilaiva)
            agenttilaiva = np.rot90(agenttilaiva)
            agenttilaiva = np.rot90(agenttilaiva)

        dim = agenttilaiva.shape

        emptys = []

        for j in range(16-dim[1]):
            for i in range(16-dim[0]):
                sample = board[i:(dim[0]+i),j:(dim[1]+j)]
                m = np.ma.bitwise_and(agenttilaiva, sample)
                if np.sum(m) == 0:
                    emptys.append((j,i))

        p = np.random.choice(np.arange(0,len(emptys)))
        p = emptys[p]

        self.set_ship_to_board(agenttilaiva.copy(), p[0], p[1], 4)

        self.pelilauta = self.board.copy()

    def set_ship5(self):
    
        board = self.board.reshape(16,16).copy()
        board[board == 4] = 1

        random_rotation = np.random.randint(0,2)
        agenttilaiva = self.agenttilaiva[5].copy()

        if random_rotation == 1: agenttilaiva = np.rot90(agenttilaiva)

        dim = agenttilaiva.shape

        emptys = []

        for j in range(16-dim[1]):
            for i in range(16-dim[0]):
                sample = board[i:(dim[0]+i),j:(dim[1]+j)]
                m = np.ma.bitwise_and(agenttilaiva, sample)
                if np.sum(m) == 0:
                    emptys.append((j,i))

        p = np.random.choice(np.arange(0,len(emptys)))
        p = emptys[p]

        self.set_ship_to_board(agenttilaiva.copy(), p[0], p[1], 4)
        self.pelilauta = self.board.copy()

    def ship_at_valid_position(self, x, y, ship):

        board = self.board.reshape(16,16).copy()

        dim = ship.shape

        sopii = True

        # sijoitettavan laivan oltava sovitetavalla rivillä kokonaisuudessaan
        if 16-y-dim[0] < 0 or 16-x-dim[1] < 0: return False

        # Laiva ei saa olla muiden laivojen päällä
        sopii = False

        try:
            sample = board[y:(dim[0]+y), x:(dim[1]+x)]
            m = np.ma.bitwise_and(ship, sample)
            if np.sum(m) == 0:
                sopii = True
        except:
            pass

        return sopii
    
    def render(self):
        
        board = self.pelilauta.reshape(16,16)
        for j in range(16):
            row = ""
            for i in range(16):
                row += str(board[j][i])
            print(row)

    def put_human_move(self, upotusX, upotusY):
        if self.pelilauta[upotusX + upotusY * 16] == 0:
            self.pelilauta[upotusX + upotusY * 16] = 6
            self.pelilauta2[upotusX + upotusY * 16] = 6

    def mark_empty(self, p):
        if self.pelilauta2[p] == 0:
            self.pelilauta2[p] = 3
 
    def reset(self):
    
        self.hits_of_agent = 0
        self.hits_of_human = 0

        self.hits_of_agent_play = 0
        self.hits_of_human_play = 0

        self.pelilauta = self.board.copy()
        self.pelilauta2 = self.board.copy()

        actions = self.get_valid_moves()
        
        return self.pelilauta[np.random.choice(np.array(actions))]
    
    def agent_won(self):

        if self.hits_of_agent == MAX_OSUMAT:
            self.hits_of_agent = 0
            self.hits_of_human = 0
            return True

        return False
        
    def get_valid_moves(self):

        actions = []

        for i in range(len(self.pelilauta2)):
            if self.pelilauta2[i] in [1, 0]:
                actions.append(i)

        return actions
    
    def random_action(self):

        actions = self.get_valid_moves()
        return np.random.choice(actions)
    
    """
        Agentti pelaa siirron peliä Q-taulusta.

        Opetusvaiheessa joskus pelilauta voi muuttua siten, että agentti ampuu omaan laivaansa.
        Tällöin satunnaispelaaja on palkittava tästä osumasta, ja agentti ei saa voittaa kyseistä
        pelikierrosta.
    """
    def step(self, action):

        reward = 0
        again = False

        # osuma ihmispelaajan laivaan
        if self.pelilauta2[action] == 1:
            self.hits_of_agent += 1
            self.pelilauta2[action] = 2
            reward = 500.0
        
        # onko ammuttu hutilaukauskohtiin?
        elif self.pelilauta2[action] == 3:
            reward = -200.0
            again = True

        elif self.pelilauta2[action] == 6:
            reward = -200.0
            again = True

        # ei osumaa
        elif self.pelilauta2[action] == 0:
            self.pelilauta2[action] = 3
            reward = -250.0

        # Satunnaispelaajan kanssa joskus Q-taulun vielä kehittyessä
        # Q-agentti saattaa pelata satunnaispelaajan pussiin
        elif self.pelilauta2[action] == 4:
            self.pelilauta2[action] = 5
            reward = -np.inf
            again = True

        elif self.pelilauta2[action] == 5:
            reward = -np.inf
            again = True
        elif self.pelilauta2[action] == 2:
            reward = 0  # jos osutaan jo osuttuun pelaajan laivan osaan, siitä ei rangaista,
                        # mutta ei palkitajaan. Näin siksi, että jotta agentti joka tapauksessa
                        # oppii tunnistamaan pelaajan laivat parametrilla alpha pidetään huolta,
                        # että aiempia Q-arvoja huomioidaan vähemmän.
                        #
            again = True
        # havainto, palkkio, tieto onko peli pelattu läpi
        return self.pelilauta2[action], reward, again
    
    def step_train(self, action):

        reward = 0
        again = False

        # osuma ihmispelaajan laivaan
        if self.pelilauta2[action] == 1:
            reward = 500.0
        
        # onko ammuttu hutilaukauskohtiin?
        elif self.pelilauta2[action] == 3:
            reward = -200.0
            again = True

        elif self.pelilauta2[action] == 6:
            reward = -200.0
            again = True

        # ei osumaa
        elif self.pelilauta2[action] == 0:
            reward = -250.0

        # Satunnaispelaajan kanssa joskus Q-taulun vielä kehittyessä
        # Q-agentti saattaa pelata satunnaispelaajan pussiin
        elif self.pelilauta2[action] == 4:
            reward = -np.inf
            again = True
        elif self.pelilauta2[action] == 5:
            reward = -np.inf
            again = True
        elif self.pelilauta2[action] == 2:
            reward = 0  # jos osutaan jo osuttuun pelaajan laivan osaan, siitä ei rangaista,
                        # mutta ei palkitajaan. Näin siksi, että jotta agentti joka tapauksessa
                        # oppii tunnistamaan pelaajan laivat parametrilla alpha pidetään huolta,
                        # että aiempia Q-arvoja huomioidaan vähemmän.
                        #
            again = True

        # havainto, palkkio, tieto onko peli pelattu läpi
        return self.pelilauta2[action], reward, again
    
    def render(self):
        print(self.pelilauta2.reshape(16,16))