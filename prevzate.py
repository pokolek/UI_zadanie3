#!/usr/bin/env python

import random
import copy
import statistics

MAX_M = 10
MAX_N = 10


class Garden:
    def __init__(self, map=None):
        if map:
            self.m = len(map)
            self.n = len(map[0])
            self.map = copy.deepcopy(map)
        else:
            self.m = random.randrange(2, MAX_M + 1)
            self.n = random.randrange(2, MAX_N + 1)
            self.map = []
            for _ in range(self.m):
                row = []
                for _ in range(self.n):
                    row.append(-1 if random.random() < 0.05 else 0)
                self.map.append(row)
        self.rock_count = sum(row.count(-1) for row in self.map)
        self.max_fitness = sum(row.count(0) for row in self.map)

    def __str__(self):
        s = ""
        for row in self.map:
            for col in row:
                s += ' K ' if col == -1 else '%2d ' % col
            s += '\n'
        return s


class Gene:
    def __init__(self, garden):
        m = garden.m
        n = garden.n
        x = random.randrange(2 * (m + n))
        if x < n:
            self.start = (0, x)
            self.direction = 'down'
        elif n <= x < m + n:
            self.start = (x - n, n - 1)
            self.direction = 'left'
        elif m + n <= x < 2 * n + m:
            self.start = (m - 1, 2 * n + m - x - 1)
            self.direction = 'up'
        else:
            self.start = (2 * (m + n) - x - 1, 0)
            self.direction = 'right'
        self.generate_rotation()

    def generate_rotation(self):
        self.rotation = [
            int(a) for a in bin(random.randrange(1024))[2:].zfill(10)
        ]

    def __str__(self):
        return '%s, %s, %s' % (str(self.start), self.rotation, self.direction)


class Individual:
    def __init__(self, garden, initialize=True):
        self.garden = garden
        self.final_garden = Garden(self.garden.map)
        self.genes = []
        self.fitness = 0
        if initialize:
            for _ in range(garden.m + garden.n + garden.rock_count):
                self.genes.append(Gene(self.garden))
            self.process()

    def __str__(self):
        return '\n'.join(str(g) for g in self.genes)

    def process(self):
        g = self.final_garden

        i = 0
        for gene in self.genes:
            pos = list(gene.start)
            direction = gene.direction
            ri = 0

            # Ak sa neda vstupit do mapy, ideme na dalsi gen
            if g.map[pos[0]][pos[1]] != 0:
                continue
            i += 1

            while True:
                # Pohrabeme policko
                g.map[pos[0]][pos[1]] = i

                # Vyberieme dalsie policko v smere ktorym sa pohybujeme
                if direction == 'up':
                    pos[0] -= 1
                elif direction == 'down':
                    pos[0] += 1
                elif direction == 'left':
                    pos[1] -= 1
                else:
                    pos[1] += 1

                # Ak je tam okraj mapy tak ideme na dalsi gen
                if pos[0] not in range(g.m) or pos[1] not in range(g.n):
                    break

                # Ak je nepohrabane tak tam prejdeme
                if g.map[pos[0]][pos[1]] == 0:
                    continue

                # Ak je tam prekazka tak sa vratime...
                if direction == 'up':
                    pos[0] += 1
                elif direction == 'down':
                    pos[0] -= 1
                elif direction == 'left':
                    pos[1] += 1
                else:
                    pos[1] -= 1

                # ...a vyberieme ine policko
                if direction == 'up' or direction == 'down':
                    n = (
                        [pos[0], pos[1] - 1],
                        [pos[0], pos[1] + 1],
                    )
                else:
                    n = (
                        [pos[0] - 1, pos[1]],
                        [pos[0] + 1, pos[1]],
                    )
                nv = []
                for p in n:
                    try:
                        nv.append(g.map[p[0]][p[1]])
                    except IndexError:
                        nv.append('e')

                # Ak je len jedno nepohrabane tak ho vyberieme
                if nv.count(0) == 1:
                    pos = n[nv.index(0)]

                # A ak su dve tak jedno vyberieme
                elif nv.count(0) == 2:
                    pos = n[gene.rotation[ri]]
                    ri += 1
                    if ri == len(gene.rotation):
                        ri = 0

                # Ak ani jedno nie je nepohrabane tak koncime
                else:
                    # Ak sme skoncili v strede mapy tak uz sa neda pokracovat
                    # na dalsi gen
                    if 'e' not in nv:
                        self.set_fitness()
                        return
                    break

                # Nastavime novy smer pohybu
                if direction in ('up', 'down'):
                    direction = 'left' if n.index(pos) == 0 else 'right'
                else:
                    direction = 'up' if n.index(pos) == 0 else 'down'

            self.set_fitness()

    def set_fitness(self):
        self.fitness = sum(1 for x in sum(self.final_garden.map, []) if x > 0)

    def crossover(self, other):
        new = Individual(self.garden, False)

        # Krizenie
        p = random.random()
        if p < 0.40:
            # 1. typ: jedna cast je z prveho jedinca, druha z druheho
            # 1112222222
            point = random.randrange(len(self.genes))
            new.genes = self.genes[:point] + other.genes[point:]
        elif p < 0.80:
            # 2. typ: nahodne vyberame z prveho alebo druheho
            # 1221221112
            new.genes = []
            for i in range(len(self.genes)):
                new.genes.append(random.choice((self.genes[i], other.genes[i])))
        else:
            # 3.typ: bez krizenia
            # 1111111111
            new.genes = random.choice((self.genes, other.genes))

        # Mutacie
        for i in range(len(new.genes)):
            # S pravdepodobnostou 5% vygenerujeme cely gen novy
            p = random.random()
            if p < 0.05:
                new.genes[i] = Gene(self.garden)
            # S pravdepodobnostou 10% mu vygenerujeme nove rotacie
            elif p < 0.1:
                new.genes[i].generate_rotation()

        # Spocitame fitness noveho jedinca
        new.process()

        return new


def solve(map=None):
    if map:
        g = Garden(map)
    else:
        g = Garden()
    population = []
    for _ in range(100):
        population.append(Individual(g))
    for gc in range(1000):
        best = max(population, key=lambda x: x.fitness)
        next_generation = [best]
        for _ in range(99):
            sample = random.sample(population, 4)
            i1, i2 = sorted(sample, key=lambda x: x.fitness, reverse=True)[:2]
            next_generation.append(i1.crossover(i2))
        population = next_generation
        avg_fitness = statistics.mean(x.fitness for x in population)
        print('generacia: %4d, max: %4d, best: %4d, avg: %7.2f'
              % (gc + 1, g.max_fitness, best.fitness, avg_fitness))
        if best.fitness == g.max_fitness:
            break
    else:
        print()
        print('Nepohrabanych: %d' % (g.max_fitness - best.fitness))

    print()
    print(g)
    print(best.final_garden)


if __name__ == '__main__':
    solve([
        [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00],
        [00, 00, 00, 00, 00, -1, 00, 00, 00, 00, 00, 00],
        [00, -1, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00],
        [00, 00, 00, 00, -1, 00, 00, 00, 00, 00, 00, 00],
        [00, 00, -1, 00, 00, 00, 00, 00, 00, 00, 00, 00],
        [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00],
        [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00],
        [00, 00, 00, 00, 00, 00, 00, 00, -1, -1, 00, 00],
        [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00],
        [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00],
        [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00],
    ])