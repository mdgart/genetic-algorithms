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
            self.code += unichr(random.randint(0,255))

    def calculate_cost(self, model):
        # calculate the cost (smaller is better)
        # of the chromosome based on the given model (the answer)
        total = 0
        for i in range(0, len(self.code)):
            diff = ord(self.code[i]) - ord(model[i])
            total += pow(diff, 2)
        self.cost = total

    def mate(self, chromosome):
        half_length = len(chromosome) / 2
        child1 = "%s%s" % (self.code[:half_length], chromosome[half_length:])
        child2 = "%s%s" % (chromosome[:half_length], self.code[half_length:])
        return [Chromosome(child1), Chromosome(child2)]

    def mutate(self, chance):
        if random.random() > chance:
            return None
        index = int(random.random() * len(self.code))
        direction = -1 if random.random() > 0.5 else +1
        chromosome = list(self.code)
        chromosome[index] = unichr(ord(chromosome[index]) + direction)
        self.code = "".join(chromosome)



class Population(object):
    def __init__(self, goal, size):
        self.members = []
        self.goal = goal
        self.generation_number = 0

        while size:
            chromosome = Chromosome()
            chromosome.randomize(len(self.goal))
            self.members.append(chromosome)
            size -= 1

    def sort_population(self):
        self.members.sort(key=lambda x: x.cost)

    def generation(self):
        for member in self.members:
            member.calculate_cost(self.goal)

        self.sort_population()
        print self.members

        children = self.members[0].mate(self.members[1])

        ## to be finished


if __name__ == "__main__":
    """
    g1 = Chromosome()
    g1.randomize(12)
    g1.calculate_cost("Hello World!")
    print g1.cost
    children = g1.mate("asdfghjklqwe")
    print children[0].code
    print children[1].code

    g2 = Chromosome("1234567890qw")
    children = g2.mate("asdfghjklzxc")
    print children[0].code
    print children[1].code
    g2.mutate(1)
    print g2.code
    """

    p1 = Population("Hello, world!", 20)
    for member in p1.members:
        print u"%s" % member.code