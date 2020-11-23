import random

class Zahrada:
    def __init__(self):
        self.povodna_zahrada = []
        self.riesena_zahrada = []


# vytvorenie zahrady
    def vytvaranie_zahrady_ukazkovy_priklad(self):
        self.obvod = 2*(10+12)
        self.pocet_kamenov = 6

        for riadky in range(10):
            while True:
                pole1 = []
                for stlpce in range(12):
                    pole1.append(0)
                self.povodna_zahrada.append(pole1)
                self.riesena_zahrada.append(pole1)
                break

        # pridanie kamenov z ukazkoveho prikladu
        self.povodna_zahrada[1][5] = -1
        self.povodna_zahrada[2][1] = -1
        self.povodna_zahrada[3][4] = -1
        self.povodna_zahrada[4][2] = -1
        self.povodna_zahrada[6][8] = -1
        self.povodna_zahrada[6][9] = -1

        self.riesena_zahrada[1][5] = -1
        self.riesena_zahrada[2][1] = -1
        self.riesena_zahrada[3][4] = -1
        self.riesena_zahrada[4][2] = -1
        self.riesena_zahrada[6][8] = -1
        self.riesena_zahrada[6][9] = -1

# vytvorernie 1 populacie ktora ma 10 chromozomov po 28 genov
    def vytvor_populaciu(self):
        populacia = []
        # chromozomy, kazda populacia ma 10 chromozomov
        for i in range(10):
            chromozom = []

            # vytvaranie genov, kazdy chromozom ma 28 genov
            for j in range(28):
                gen = []
                # random vstup do zahrady z obvodu
                vstup = random.randint(0,44)
                gen.append(vstup)

                # nahodne smery pohybu 0=L, 1=P
                smery = []
                for smer in range(4):
                    smery.append(random.randint(0,1))

                gen.append(smery)
                chromozom.append(gen)
            populacia.append(chromozom)

        return populacia

# vypisanie zahrady
    def vypis_zahradu(self, zahradka):
        for riadok in zahradka:
            for stlpec in riadok:
                if stlpec:
                    print('K ',end='')
                else:
                    print(str(stlpec) + ' ', end='')
            print()

    def vyries_zahradu_pre_populaciu(self, pop):

        return

#zaciatok
    def __str__(self):
        self.vytvaranie_zahrady_ukazkovy_priklad()
        self.vypis_zahradu(self.povodna_zahrada)
        self.vypis_zahradu(self.riesena_zahrada)

        for generacia in range(1000):
            populacia = self.vytvor_populaciu()

        return(" ")

print(Zahrada())