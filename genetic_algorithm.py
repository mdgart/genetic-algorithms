import random


class Chromosome(object):
    def __init__(self, code=""):
        # initialize the object with the provided
        # string of genes and with an arbitrary cost
        # of 9999
        self.code = code
        self.cost = 9999

    def randomize(self, length=0):
        # create a random chromosome (string of genes)
        self.code = ""
        while length:
            length -= 1
            self.code += unichr(random.randint(0,127))

    def calculate_cost(self, model):
        # calculate the cost (smaller is better)
        # of the chromosome based on the given model (the answer)
        total = 0
        for i in range(0, len(self.code)):
            diff = ord(self.code[i]) - ord(model[i])
            total += pow(diff, 2)
        self.cost = total

    def mate(self, chromosome):
        half_length = len(chromosome.code) / 2
        child1 = "%s%s" % (self.code[:half_length], chromosome.code[half_length:])
        child2 = "%s%s" % (chromosome.code[:half_length], self.code[half_length:])
        return [Chromosome(child1), Chromosome(child2)]

    def mutate(self, chance):
        if random.random() > chance:
            return None
        index = int(random.random() * len(self.code))
        direction = -1 if random.random() > 0.5 else +1
        chromosome = list(self.code)
        char_ord = ord(chromosome[index]) + direction
        # prevent overflow
        if char_ord > 127:
            char_ord = 127
        if char_ord < 0:
            char_ord = 0

        chromosome[index] = chr(char_ord)
        self.code = "".join(chromosome)


class Population(object):
    def __init__(self, goal, size):
        self.members = []
        self.goal = goal
        self.generation_number = 0
        self.goalReached = False

        while size:
            chromosome = Chromosome()
            chromosome.randomize(len(self.goal))
            self.members.append(chromosome)
            size -= 1

    def sort_population(self):
        self.members.sort(key=lambda x: x.cost)

    def generation(self):
        while not self.goalReached:
            for member in self.members:
                member.calculate_cost(self.goal)

            self.sort_population()

            # mate
            children = self.members[0].mate(self.members[1])
            len_members = len(self.members)
            self.members[len_members-2] = children[0]
            self.members[len_members-1] = children[1]

            for i in range(0, len_members):
                print self.members[i].code
                self.members[i].mutate(0.5)
                self.members[i].calculate_cost(self.goal)
                if self.members[i].code == self.goal:
                    self.goalReached = True
                    self.sort_population()
                    print "Generation:%s  Code:%s" % (self.generation_number, self.goal)
                    return True
            self.generation_number += 1


population = Population("Hello, World!", 30)
population.generation()