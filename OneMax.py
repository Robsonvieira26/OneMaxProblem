import random, sys
from msvcrt import getch

def gerar_individuo(qtd_genes):
    ind = ''
    for i in range(qtd_genes):
        ind += str(random.randint(0,1)) # Escolhe aleatoriamente o valor do gene
    return ind

def gerar_populacao(tam_pop,qtd_genes): #Cria a população inicial 
    pop = []
    for i in range(tam_pop):
        pop.append(gerar_individuo(qtd_genes))
    return pop

def fitness(ind): #retorna a quantidade de 1's de ind
    return sum(int(gene) for gene in ind)
    #transforma a strig em int e soma todos os 1s e 0s

def selecionar_pais(pop,tam_pop,K=3): #K é quantos disputam o torneio
    pais = []
    for torneio in range(tam_pop):
        competidores = []
        for i in range(K):
            indice = random.randint(0,tam_pop-1)
            competidores.append(pop[indice])
            #a maior avaliação se inicia como a primeira, depois e avaliado
        maior_score = fitness(competidores[0])
        vencedor = competidores[0]
        for i in range(1,K):
            avaliacao = fitness(competidores[i])
            if avaliacao > maior_score: #uma avaliação maior foi encontrada 
                maior_score = avaliacao
                vencedor = competidores[i]
        pais.append(vencedor)
    return pais

def gerar_filhos(pais, tam_pop, taxa_crossover=0.7):
	nova_pop = []
	for i in range(tam_pop//2):
		pai1 = random.choice(pais)
		pai2 = random.choice(pais)
		if random.random() < taxa_crossover:
			corte = random.randint(1, len(pai1)-1)
			filho1 = pai1[0:corte] + pai2[corte:]
			filho2 = pai2[0:corte] + pai1[corte:]
			nova_pop.append(filho1)
			nova_pop.append(filho2)
		else:
			nova_pop.append(pai1)
			nova_pop.append(pai2)
	return nova_pop
            
def mutacao(pop, tam_pop,qt_genes,taxa_mutacao=0.005):
    nova_pop = [] 
    for i in range(tam_pop):
        individuo = ''
        for j in range(qtd_genes):
            if random.random() <=taxa_mutacao:
                if pop[i][j] == '0':
                    individuo += '1'
                else:
                    individuo += '0'
            else: #não ocorre mutação
                individuo += pop[i][j]
        nova_pop.append(individuo)
    return nova_pop

def melhor_individuo(pop,tam_pop):
    melhor_score=fitness(pop[0])
    indice_melhor = 0
    for i in range(1,tam_pop):
        avaliacao = fitness(pop[i])
        if avaliacao >= melhor_score:
            melhor_score = avaliacao
            indice_melhor = i
    return pop[indice_melhor]

tam_pop, qtd_genes = int(sys.argv[1]), int(sys.argv[2])
crossover_tax,taxa_mutacao = float(sys.argv[3]),float(sys.argv[4])
geracoes_max = int(sys.argv[5])
seenGeneration= int(sys.argv[6])

pop = gerar_populacao(tam_pop,qtd_genes)
if seenGeneration == 1:
    print('Populacao inicial')
    print(pop)
    getch()

for geracao_atual in range(geracoes_max):
    pais = selecionar_pais(pop,tam_pop) 
    pop = gerar_filhos(pais,tam_pop,crossover_tax) #filhos criados
    pop=mutacao(pop,tam_pop,qtd_genes,taxa_mutacao)#mutação aplicada
    if seenGeneration == 1:
        print(geracao_atual+1,'° Geracao ')
        print(pop)
        getch()
    if fitness(melhor_individuo(pop,tam_pop)) == qtd_genes:
        print('O objetivo foi encontrado na %s° geracao'% (geracao_atual+1))
        break    
    
print("O melhor individuo:", melhor_individuo(pop,tam_pop))
print('Melhor score: ',fitness(melhor_individuo(pop,tam_pop)))