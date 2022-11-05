import requests
import random

website="http://163.117.164.219/age/test?c="

def eval_chromosome(chromosome):
    """
    Returns the chromosome score
    """
    r=requests.get(website+chromosome)
    return float(r.text)


def eval_poblation(poblation):
    """
    Returns the minimal score of a given poblation
    """
    minimal=(99999, None)
    for chromosome in poblation:
        score = eval_chromosome(chromosome)
        if score < minimal[0]:
            minimal = (score, chromosome)
    return minimal

# [Settings]
M = 200              # Poblation size
n = 80               # Chromosome size (nº of gens)
tournament_size = 10 # Tournament size
mutation = 10        # Percentage of mutation for each bit
CYCLES = 10000       # Maximum cycles of the program

poblation = []
values = (0,1)

# Initialize a list which contains strings of 0/1 generated randomly
for _ in range (M):
    c =""
    for _ in range(n):
        c+=str(random.choice(values))
    poblation.append(c)

evaluation_list = [None, None, None, None, None]
count_repeat = 0
for generation, _ in enumerate(range(CYCLES)):
    
    # [------Selection------]
    # Initialize the poblation which contains winners of tournament
    chosen_poblation = []
    # Select the best (fitness guide)
    score_poblation = []
    for chromosome in poblation:
        score = eval_chromosome(chromosome)
        score_poblation.append(score)
    for _ in range(M):
        contestants = []
        contestants_score = []
        for _ in range(tournament_size):
            c = random.randrange(0,M)
            participant = poblation[c]
            contestants.append(participant)
            contestants_score.append(score_poblation[c])

        chosen_poblation.append(contestants[contestants_score.index(min(contestants_score))])

    # [------Genetic crossing------]
    poblation = []
    counter = 0
    for _ in range (M//2):
        p1 = chosen_poblation[counter]
        p2 = chosen_poblation[counter+1]
        # Create childs
        c1 = ""
        c2 = ""
        counter_pair = 0
        for _ in range(n//8):
            choose_parent_bit = random.choice(values)  # 0 / 1
            if choose_parent_bit: #1
                c1+=p2[counter_pair:counter_pair+8]
            else:
                c1+=p1[counter_pair:counter_pair+8]
            choose_parent_bit2 = random.choice(values)  # 0 / 1
            if choose_parent_bit2: #1
            
                c2+=p2[counter_pair:counter_pair+8]
            else:
                c2+=p1[counter_pair:counter_pair+8]

            counter_pair += 8
        poblation.append(c1)
        poblation.append(c2)
        counter+=2
    # [------Mutation------]
    for chromosome in poblation:
        counter_bit=0
        chromosome=list(chromosome)
        for _ in chromosome:
            if random.randrange(0, 100//mutation) == 1:            
                chromosome[counter_bit] = str(int(not(chromosome[counter_bit])))
            counter_bit+=1
        chromosome="".join(chromosome)

    # Show best fitness each cycle
    e = eval_poblation(poblation)
    e_value = e[0]
    
    print(f"Generation {generation+1}: {e}")

    # Stop condition: Have the same value 5 times consequently
    if evaluation_list.count(e_value)==3:
        print(f"[Resultado alcanzado]\nGeneration: {generation-2}\nSolution: {e}")
        break
    else:
        evaluation_list[count_repeat] = e_value
        if count_repeat!=4:
            count_repeat+=1
        else:
            count_repeat=0