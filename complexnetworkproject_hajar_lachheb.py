# -*- coding: utf-8 -*-
"""ComplexNetworkProject_Hajar Lachheb.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/19BaGIYvR4rJ1JtEgVcYvVAbZMIGipSZq

#Complex Network Project : Evolotuionary Game Theory Analaysis 

The aim of my project is to conduct an analysis of the behavior of three evolutionary games, namely weak prisoner’s dilemma, stag hunt, and snowdrift, on different network topologies. In addition to these three games, additional games may also be explored if time permits.

The analysis will be carried out through simulations using different update rules, including the replicator rule, multiple replicator rule, unconditional imitation rule, Moran rule, and Fermi rule. Due to the high computational cost, the analysis will be limited to networks with a finite size. Specifically, complete networks, homogeneous random graphs, Erdos Renyi network, and Barabasi Albert network will be explored. 

Furthermore, my project aims to investigate the equilibrium states and dynamics of the games on these networks while considering varying values of T and S. The primary objective of my project would be to understand how network topology and update rules impact the evolution of cooperation in different games.

The project will utilize several resources to deepen the understanding of the subject matter and enhance the analysis. Three specific resources will be thoroughly examined to support the development of the project.

##Importing all the libraries ✅
"""

# Commented out IPython magic to ensure Python compatibility.
import networkx as nx
import numpy as np
import random as rd
import matplotlib.pyplot as plt
from itertools import combinations

# %matplotlib inline

"""##Introducing the first function : Game Simulation ✅

This part of the code was develeped actually to be able to simulate a game on a network where each node represents a player. In our case we will use only two players. 

The game is a variation of the Prisoner's Dilemma, where players can either cooperate (C) or defect (D) with their neighbors. We developed two functions and then finally the game simulation part. 

The function payoff_node calculates the total payoff of a node (player) based on its neighbors. It takes inputs n (the node), G (the network), C (the set of cooperators), S (the suckers payoff), and T (the temptation payoff). The function then calculates the payoff by iterating over the neighbors of the node. If the node and the neighbor are both cooperators, the payoff increases by 1. If the node is a cooperator and the neighbor is a defector, the payoff increases by the value of S. If the node is a defector, the payoff increases by the value of T if the neighbor is a cooperator, and it remains unchanged if the neighbor is also a defector.

Then we switch to developing the function game_simulation. It was developed to be able to perform a Monte Carlo simulation of the game. It takes inputs G (the network), T (the temptation payoff), S (the suckers payoff), update_rule (a function that defines the update rule for player strategies), and plot_time (a boolean flag indicating whether to plot the fraction of cooperators over time). The simulation initializes the game parameters and sets the initial fraction of defector nodes (d_0). It then iterates over a specified number of time steps (Tmax) and computes the payoffs for each node using the payoff_node function. What is important is that the strategy of each node is updated based on the update_rule function. 

The update is done synchronously, meaning all players are updated simultaneously. The simulation tracks the fraction of cooperators (C) over time and returns the final fraction of cooperators (p).
"""

Nrep = 20
d_0 = 0.5 
Tmax = 500
Ttrans = 400

# C: collaborators
# D: defectors

def payoff_node(n, G, C, S, T): 
    payoff = 0
    if n in C:
        for i in G.neighbors(n):
            if i in C:
                payoff += 1
            else:
                payoff += S
    else:
        for i in G.neighbors(n):
            if i in C:
                payoff += T
            else:
                payoff += 0
    return payoff                        

def game_simulation(G,T,S, update_rule, plot_time=False): 
    nodes = list(G.nodes())
    C = set(nodes) 
    N = len(nodes)
    n_d_0 = round(d_0 * N)
    D_0 = set(rd.sample(C, n_d_0)) 
    C = C - D_0 
    P = 0 
    p_t=[len(C)/N,]
    for t in range(0,Tmax):

        payoffs = []
        for n in nodes:
            payoffs.append(payoff_node(n,G, C, S, T))
        new_C = set() # nomore_D
        new_D = set() # nomore_C
        for i in nodes: 
            s = update_rule(i,G, C, S, T, payoffs)
            if s == 'C':
                new_C.add(i)
            if s == 'D':
                new_D.add(i)
        C = (C | new_C) - new_D 
        C_len = len(C)
        if C_len == 0:
            return 0
        if C_len == N:
            return 1
            
        if plot_time == True:
            p_t.append(C_len/N)

        if t>=Ttrans:
            P += len(C)
            
    p = P/(N*(Tmax-Ttrans))
    
    if plot_time == True:
        plt.figure(figsize=(10,6))
        plt.title(f'N = {N}, S = {S}, T = {T}')
        plt.plot(p_t)
        plt.xlabel('time')
        plt.ylabel('fraction of cooperators')
        
    return p

"""##Introducing the second function : Snowdrift inspired Game Simulation ✅

We hoped we could have enough time to use the second simulation game and then observe the different results and conclude if changing the game simulation changes the overall results. 

To explain it briefly, the first code simulates a game based on the Prisoner's Dilemma, where players can choose to cooperate or defect. The payoffs are defined based on the cooperation or defection of the player and its neighbors. The goal is to study the evolution of cooperation in a networked setting.

In the second game simulation, we instead simulate a game known as the Snowdrift game, where players can choose to be hawks or doves. The payoffs are determined by the interaction between hawks and doves in the neighborhood. Hawks engage in a fight with a cost, and the winner receives a reward. The goal is to examine the evolution of hawk and dove strategies in a networked context.
"""

Nrep = 20
d_0 = 0.5 
Tmax = 500
Ttrans = 400

R = 1.0  
C = 0.5  

def payoff_node(n, G, H, R, C):
    payoff = 0
    if n in H:
        hawks = [i for i in G.neighbors(n) if i in H]
        doves = [i for i in G.neighbors(n) if i not in H]
        total_players = len(hawks) + len(doves)
        payoff += R / 2  

        if len(hawks) > 0: 
            payoff -= C / 2
            payoff += R / 2

    else:
        hawks = [i for i in G.neighbors(n) if i in H]
        doves = [i for i in G.neighbors(n) if i not in H]
        total_players = len(hawks) + len(doves)
        payoff += R / 2  

        if len(hawks) > 0: 
            payoff += R

    return payoff


def update_rule(n, G, H, R, C, payoffs):
    if random.random() < payoffs[n]:
        return 'H'
    else:
        return 'D'


def snowdrift_game_simulation(G, R, C, update_rule, plot_time=False):
    nodes = list(G.nodes())
    H = set(nodes)  
    N = len(nodes)
    n_d_0 = round(d_0 * N)  
    D_0 = set(random.sample(H, n_d_0))  
    H = H - D_0  
    P = 0
    p_t = [len(H) / N, ]

    for t in range(Tmax):
        payoffs = [payoff_node(n, G, H, R, C) for n in nodes]
        new_H = set() 
        new_D = set()  

        for i in nodes:
            s = update_rule(i, G, H, R, C, payoffs)
            if s == 'H':
                new_H.add(i)
            if s == 'D':
                new_D.add(i)

        H = (H | new_H) - new_D

        H_len = len(H)
        if H_len == 0:
            return 0
        if H_len == N:
            return 1

        if plot_time:
            p_t.append(H_len / N)

        if t >= Ttrans:
            P += H_len

    p = P / (N * (Tmax - Ttrans))

    if plot_time:
        plt.figure(figsize=(10, 6))
        plt.title(f'N = {N}, R = {R}, C = {C}')
        plt.plot(p_t)
        plt.xlabel('time')
        plt.ylabel('fraction of Hawks')

    return p

"""##Defining the update rules  ✅

In this part, we are trying to define all the update rules we will use in our experiment. Further explanation of these rules will be detailed in the report. The update rules are : Random Rule, Stochastic Best Response Rule, Generous tit for tat rule, Replicator Rule, Multiple Replicator Rule, unconditional_imitation_rule, Moran Rule and Fermi Rule.
"""

import random

def random_rule(i, G, C, S, T, payoffs):
    if random.random() < 0.5:
        return 'C'
    else:
        return 'D'

def stochastic_best_response_rule(i, G, C, S, T, payoffs):
    Ni = list(G.neighbors(i))
    if Ni != []:
        best_response = max(Ni, key=lambda j: payoffs[j])
        probability = (payoffs[best_response] - payoffs[i]) / max(payoffs)
        if random.random() < probability:
            if best_response in C:
                return 'C'
            else:
                return 'D'

def generous_tit_for_tat_rule(i, G, C, S, T, payoffs):
    Ni = list(G.neighbors(i))
    if Ni != []:
        j = random.choice(Ni)
        if payoffs[j] > payoffs[i]:
            probability = 0.8  
            if random.random() < probability:
                if j in C:
                    return 'C'
                else:
                    return 'D'
    return 'C'

def replicator_rule(i,G, C, S, T, payoffs):
    Ni = list(G.neighbors(i))
    ki = len(Ni)
    if Ni!=[]:
        j = rd.choice(Ni)                
        if payoffs[j] > payoffs[i]:
            kj = G.degree(j) 
            phi = max(ki,kj)*(max(1,T) - min(0,S)) 
            probability = (payoffs[j]-payoffs[i])/phi
            if rd.random() < probability:
                if j in C:
                    return 'C'
                else:  
                    return 'D'

def multiple_replicator_rule(i,G, C, S, T, payoffs):
    Ni = list(G.neighbors(i))
    ki = len(Ni)
    probabilities = {}
    if Ni==[]:
        return
    for j in Ni:
        if payoffs[j] > payoffs[i]:
            kj = G.degree(j) 
            phi = max(ki,kj)*(max(1,T) - min(0,S)) 
            probabilities[j] = (payoffs[j]-payoffs[i])/phi
    if probabilities == {}:
        return

    for j in probabilities.keys():
        if rd.random() < probabilities[j]:
            if j in C:
                return 'C'
            else:  
                return 'D'

def unconditional_imitation_rule(i,G, C, S, T, payoffs): 
    j = np.argmax(payoffs)
    if payoffs[j] > payoffs[i]:
        if j in C:
            return 'C'
        else:  
            return 'D'

def moran_rule(i,G, C, S, T, payoffs): 
    Ni = list(G.neighbors(i))
    ki = len(Ni)
    if Ni==[]:
        return 
    j = rd.choice(Ni)
    psi = ki
    for n in Ni:
        kn = G.degree(n) 
        if kn > psi:
            psi = kn
    psi *= min(0,S)
    probability = (payoffs[j] - psi)/ np.sum([payoffs[k]-psi for k in Ni+[i]])
    if rd.random() < probability:
        if j in C:
            return 'C'
        else:  
            return 'D'

def fermi_rule(i,G, C, S, T, payoffs): 
    Ni = list(G.neighbors(i))
    if Ni!=[]:
        j = rd.choice(Ni)   
        beta = 0.1 
        probability = 1/(1+np.exp(-beta*(payoffs[j]-payoffs[i])))
        if rd.random() < probability:
            if j in C:
                return 'C'
            else:  
                return 'D'

"""##Defining the Monte Carlo Simulation ✅

It's time to perform simulations and generate plots for the different game scenarios and update rules.

The MC function takes inputs G (the network), Nrep (the number of repetitions), T (a parameter), S (another parameter), and update_rule (the strategy update rule). It runs the game_simulation function Nrep times and returns the average fraction of cooperators over the repetitions.

We can therefore define the fourth game theories we are using in our experiment :

- The weak_prisoner_dilemma function defines a game scenario called the weak prisoner's dilemma, where T ranges from 1 to 2 and S is fixed at 0. It returns a list of tuples representing different combinations of T and S.

- The hawk_dove function defines a game scenario called the Hawk-Dove game, where T ranges from 2 to 3 and S ranges from 1 to 2. It also returns a list of tuples representing different combinations of T and S.

- The stag_hunt function defines a game scenario called the stag hunt, where T ranges from 0 to 1 and S ranges from 0 to -1. It returns a list of tuples representing different combinations of T and S.

- The snow_drift function defines a game scenario called the snow drift, where T ranges from 1 to 2 and S ranges from 1 to 0. It returns a list of tuples representing different combinations of T and S.

Then we developed the plot function. In fact, this function takes inputs G (the network), name (a string), game (a function representing a game scenario), and update_rules (a list of strategy update rules). It generates a plot for the specified game scenario and update rules. For each update rule, it calculates the average fraction of cooperators for different combinations of T and S using the MC function. It then plots the results on the graph, with T and S values on the x-axis and the fraction of cooperators on the y-axis. The legend displays the names of the update rules used.
"""

n_points = 50

def MC(G, Nrep, T, S, update_rule):
    sum_p = 0
    for _ in range(0,Nrep):
        sum_p += game_simulation(G, T, S, update_rule)
    return sum_p/Nrep

def weak_prisoner_dilemma():
    print('weak prisoner’s dilemma: T in [1,2], S=0')
    t_list = np.linspace(1.0, 2.0, num=n_points)
    s_list = np.zeros(len(t_list))
    return list(zip(t_list, s_list))

def hawk_dove():
    print("Hawk-Dove Game: T in [2,3], S in [1,2]")
    t_list = np.linspace(2, 3, num=n_points)
    s_list = np.linspace(1, 2, num=n_points)
    return list(zip(t_list, s_list))

def stag_hunt(): 
    print('stag hunt: diagonal line between (T,S)=(0,0) and (T,S)=(1,-1)')
    t_list = np.linspace(0, 1.0, num=n_points)
    s_list = np.linspace(0, -1, num=n_points)
    return list(zip(t_list, s_list))

def snow_drift():
    print('snow drift: diagonal line between (T,S)=(1,1) and (T,S)=(2,0)')
    t_list = np.linspace(1, 2.0, num=n_points)
    s_list = np.linspace(1, 0, num=n_points)
    return list(zip(t_list, s_list))

def plots(G, name, game, update_rules = [random_rule, stochastic_best_response_rule, generous_tit_for_tat_rule, replicator_rule, multiple_replicator_rule, unconditional_imitation_rule, moran_rule, fermi_rule]):
    _, ax = plt.subplots(figsize=(15,6))
    TS_list = game()
    TS_labels = [f'T,S = ({ts[0]:.3f},{ts[1]:.3f})' for ts in TS_list]
    plt.title(name + ' : ' + game.__name__)
    ax.set_ylim([0, 1])
    plt.grid()
    for update_rule in update_rules:
        print(update_rule.__name__)
        p_list = []
        for t,s in TS_list:
            p = MC(G, Nrep, t, s, update_rule)
            p_list.append(p)
        ax.plot(TS_labels, p_list, '-o', markersize=3, label = update_rule.__name__)
    ax.set_xticklabels(labels = TS_labels, rotation=90)
    plt.xlabel('T,S')
    plt.ylabel('fraction of cooperators')
    plt.legend()

"""##Defining the graph functions

We will nextly experiment using different graph structures and functions.
"""

def generate_scale_free_network(N, m):
    return nx.barabasi_albert_graph(N, m)

def generate_small_world_network(N, k, p):
    return nx.watts_strogatz_graph(N, k, p)

def generate_community_network(N, k, p_in, p_out, num_communities):
    G = nx.Graph()
    nodes_per_community = N // num_communities

    for i in range(num_communities):
        community = nx.watts_strogatz_graph(nodes_per_community, k, p_in)
        G = nx.disjoint_union(G, community)

    for i in range(num_communities):
        for j in range(i+1, num_communities):
            if rd.random() < p_out:
                nodes_i = list(range(i * nodes_per_community, (i+1) * nodes_per_community))
                nodes_j = list(range(j * nodes_per_community, (j+1) * nodes_per_community))
                edge = (rd.choice(nodes_i), rd.choice(nodes_j))
                G.add_edge(*edge)

    return G

"""##  ▶ First experiment : Complete graphs"""

complete_graph_100 = nx.complete_graph(100)

nx.draw(complete_graph_100, with_labels=True)

"""##Results using the first game simulation defined

Each simulation had a time of running equal to 2 full hours and sometimes even 3 hours.

The "Moran_rule" Update rule took a lot of time to completely run.

###Weak Prisoner Dilemma for the following update rules : replicator_rule, multiple_replicator_rule, unconditional_imitation_rule, moran_rule and fermi_rule.
"""

plots(complete_graph_100, 'complete graph 100', weak_prisoner_dilemma, update_rules=[replicator_rule, multiple_replicator_rule, unconditional_imitation_rule, moran_rule, fermi_rule])

"""###Weak Prisoner Dilemma for all the update rules"""

plots(complete_graph_100, 'complete graph 100', weak_prisoner_dilemma)

"""###Stag Hunt for the following update rules : replicator_rule, multiple_replicator_rule, unconditional_imitation_rule, moran_rule and fermi_rule."""

plots(complete_graph_100, 'complete graph 100', stag_hunt)

"""We only presented these update rules because they were more significant when plotting all of the update rules. """

plots(complete_graph_100, 'complete graph 100', stag_hunt, update_rules=[replicator_rule, multiple_replicator_rule, unconditional_imitation_rule, fermi_rule])

"""###Snow Drift for all the update rules"""

plots(complete_graph_100, 'complete graph 100', snow_drift)

"""###Hawk Dove for all the updates rules"""

plots(complete_graph_100, 'complete graph 100', hawk_dove)

"""According to the paper "Evolutionary game theory: Temporal and spatial effects beyond replicator dynamics" by Roca, Cuesta, and Sánchez, the impact of update rules in a complete network, which represents a well-mixed or unstructured population, may not significantly alter the overall evolutionary outcome. In such networks, differences between update rules may have minimal relevance.

###Game Simulation temporal representation
"""

game_simulation(complete_graph_100, T = 0.49005001, S = -0.49005001, update_rule=replicator_rule, plot_time=True)

"""##Some results using the second game simulation

In this part, we wanted to experiment with the second game simulation and see what result we can get. Overall we tried it with the weak prisoner dilemma and the stag hunt. And we see already some differences with the first simulation result.
"""

plots(complete_graph_100, 'complete graph 100', weak_prisoner_dilemma)

plots(complete_graph_100, 'complete graph 100', stag_hunt)

"""## ▶ Second Experiment : Community networks

##Built In Community Graph

We said that it's bilt i sice we are defiig te vales : 
- Total number of nodes : N = 100  
- Average node degree : k = 10 
- Probability of generating an edge within the same community : p_in = 0.3 
- Probability of generating an edge between different communities : p_out = 0.05 
- num_communities = 4
"""

N = 100  # Total number of nodes
k = 10   # Average node degree
p_in = 0.3  # Probability of generating an edge within the same community
p_out = 0.05  # Probability of generating an edge between different communities
num_communities = 4  # Number of communities

G = generate_community_network(N, k, p_in, p_out, num_communities)

nx.draw(G, with_labels=True)

"""###Weak Prisoner Dilemma"""

plots(G, 'community network', weak_prisoner_dilemma)

"""###Stag Hunt"""

plots(G, 'community network', stag_hunt)

"""###Hawk Dove"""

plots(G, 'community network', hawk_dove )

"""###Snow Drift"""

plots(G, 'community network', snow_drift)

"""##LFR Community Grap :  Lancichinetti–Fortunato–Radicchi benchmark"""

n = 100
tau1 = 4
tau2 = 2.5
mu = 0.2
LFR_100 = nx.LFR_benchmark_graph(n, tau1, tau2, mu, average_degree=5, min_community=10)

nx.draw(LFR_100, with_labels=True)

"""###Weak Prisoner Dilemma"""

plots(LFR_100, 'LFR_100', weak_prisoner_dilemma)

"""###Hawk Dove"""

plots(LFR_100, 'LFR_100', hawk_dove)

"""###Snow Drift"""

plots(LFR_100, 'LFR_100', snow_drift)

"""###Stag Hunt"""

plots(LFR_100, 'LFR_100', stag_hunt)

"""##Stochastic Block Model Graph"""

import networkx as nx
import numpy as np

n = 100  # Total number of nodes
k = 5  # Average node degree
p_in = 0.8  # Probability of generating an edge within the same community
p_out = 0.1  # Probability of generating an edge between different communities
num_communities = 4  # Number of communities

# Create the block connectivity matrix
p_matrix = np.full((num_communities, num_communities), p_out)
np.fill_diagonal(p_matrix, p_in)

# Generate the SBM graph
G = nx.stochastic_block_model([n//num_communities]*num_communities, p_matrix)

# Print some information about the graph
print("Generated Stochastic Block Model (SBM) graph:")
print("Number of nodes:", G.number_of_nodes())
print("Number of edges:", G.number_of_edges())

nx.draw(G, with_labels=True)

"""###Weak Prisoner Dilemma"""

plots(G, 'SBM', weak_prisoner_dilemma)

"""###Hawk Dove"""

plots(G, 'SBM', hawk_dove)

"""###Stag Hunt"""

plots(G, 'SBM', stag_hunt)

"""###Snow Drift"""

plots(G, 'SBM', snow_drift)

"""## ▶ Tird Experiment : Small World Network"""

N = 100  # Total number of nodes
k = 10   # Average node degree
p = 0.3  # Probability of rewiring edges

G = generate_small_world_network(N, k, p)

nx.draw(G, with_labels=True)

"""###Weak Prisoner Dilemma"""

plots(G, 'Watts–Strogatz', weak_prisoner_dilemma)

"""###Hawk Dove"""

plots(G, 'Watts–Strogatz', hawk_dove)

"""###Snow Drift"""

plots(G, 'Watts–Strogatz', snow_drift)

"""###Stag Hunt"""

plots(G, 'Watts–Strogatz', stag_hunt)

"""## ▶ Fort Experiment : Real World Network"""

import networkx as nx

G = nx.karate_club_graph()

nx.draw(G, with_labels=True)

"""###Weak Prisoner Dilemma"""

plots(G, 'Karate Club', weak_prisoner_dilemma)

"""###Hawk Dove"""

plots(G, 'Karate Club', hawk_dove)

"""###Stag Hunt"""

plots(G, 'Karate Club', stag_hunt)

"""###Snow Drift"""

plots(G, 'Karate Club', snow_drift)

"""## ▶ Fift Experiment : Homogeneous Random Graph"""

randregular_100_5 = nx.random_regular_graph(5,100)

nx.draw(randregular_100_5, with_labels=True)

"""###Weak Prisoner Dilemma"""

plots(randregular_100_5, 'random regular graph 100 5', weak_prisoner_dilemma)

"""###Stag Hunt"""

plots(randregular_100_5, 'random regular graph 100 5', stag_hunt)

"""###Snow Drift"""

plots(randregular_100_5, 'random regular graph 100 5', snow_drift)

"""###Hawk Dove"""

plots(randregular_100_5, 'random regular graph 100 5', hawk_dove)

"""###Game Simulation temporal representation """

game_simulation(randregular_100_5, T = 0.49005001, S = -0.49005001, update_rule=replicator_rule, plot_time=True)

"""###Snow Drift with Tmax = 1000"""

Tmax = 1000
Tmin = 900
plots(randregular_100_5, 'random regular graph 100 5', snow_drift, update_rules=[generous_tit_for_tat_rule, replicator_rule, unconditional_imitation_rule, fermi_rule])

"""###Weak Prisoner Dilemma with Tmax = 1000"""

Tmax = 1000
Tmin = 900
plots(randregular_100_5, 'random regular graph 100 5', weak_prisoner_dilemma, update_rules=[generous_tit_for_tat_rule, replicator_rule, unconditional_imitation_rule, fermi_rule])

"""###Hawk Dove with Tmax = 1000"""

Tmax = 1000
Tmin = 900
plots(randregular_100_5, 'random regular graph 100 5', hawk_dove, update_rules=[generous_tit_for_tat_rule, replicator_rule, unconditional_imitation_rule, fermi_rule])

"""###Stag Hunt with Tmax = 1000"""

Tmax = 1000
Tmin = 900
plots(randregular_100_5, 'random regular graph 100 5', stag_hunt, update_rules=[generous_tit_for_tat_rule, replicator_rule, unconditional_imitation_rule, fermi_rule])

"""###Game Simulation temporal representation with T = 1000"""

game_simulation(randregular_100_5, T = 0.49005001, S = -0.49005001, update_rule=replicator_rule, plot_time=True)

"""###Game Simulation temporal representation with T = 10000"""

Tmax = 10000
game_simulation(randregular_100_5, T = 0.49005001, S = -0.49005001, update_rule=replicator_rule, plot_time=True)

"""###Game Simulation temporal representation with T = 1000 and T = 1 and S = 1"""

game_simulation(randregular_100_5, T = 1, S = 1, update_rule=replicator_rule, plot_time=True)

"""###Game Simulation temporal representation with T = 1000 and T = 1,5 and S = 0,5"""

game_simulation(randregular_100_5, T = 1.5, S = 0.5, update_rule=replicator_rule, plot_time=True)

"""
The results indicate that the fraction of cooperators in the unconditional imitation rule varies significantly based on the random initialization of cooperator and defector nodes, even when the S and T values remain constant."""

Ttrans = 9000
Tmax = 10000
for _ in range(0,10):
    print(game_simulation(randregular_100_5, T = 1.5, S = 0.5, update_rule=unconditional_imitation_rule, plot_time=True))

"""In the case of homogeneous random networks, it takes a considerably longer time to reach a stationary state compared to the other models. To accommodate this, we have adjusted the maximum simulation time (Tmax) and transient time (Ttrans) accordingly: Ttrans = 9000 and Tmax = 10000. However, due to the increased computational cost, we will only display plots for the replicator rule and unconditional imitation rule. This will allow us to compare the outcomes with subsequent networks that exhibit different degrees of heterogeneity.

Furthermore, we have reduced the number of repetitions for the Monte Carlo simulation to 20, considering the computational demands. This adjustment will still provide meaningful insights while reducing the overall computational burden.

###Weak Prisoner Dilemma with T = 10000
"""

Tmax = 10000
Trans = 9000

plots(randregular_100_5, 'random regular graph 100 5', weak_prisoner_dilemma, update_rules=[generous_tit_for_tat_rule, replicator_rule, unconditional_imitation_rule, fermi_rule])

"""###Stag Hunt with T = 10000"""

plots(randregular_100_5, 'random regular graph 100 5', stag_hunt, update_rules=[generous_tit_for_tat_rule, replicator_rule, unconditional_imitation_rule, fermi_rule])

"""###Snow Drift with T = 10000"""

plots(randregular_100_5, 'random regular graph 100 5', snow_drift, update_rules=[generous_tit_for_tat_rule, replicator_rule, unconditional_imitation_rule, fermi_rule])

"""###Hawk Dove  with T = 10000"""

plots(randregular_100_5, 'random regular graph 100 5', hawk_dove, update_rules=[generous_tit_for_tat_rule, replicator_rule, unconditional_imitation_rule, fermi_rule])

"""## ▶ Sixth Experiment : Barabasi Albert Graph """

Nrep = 50
Tmax = 500
Trans = 400

N = 100
K = 5
BA_100_5 = nx.barabasi_albert_graph(N, K)

nx.draw(BA_100_5, with_labels=True)

"""###Weak Prisoner Dilemma"""

plots(BA_100_5, 'BA_100_5', weak_prisoner_dilemma)

"""###Hawk Dove"""

plots(BA_100_5, 'BA_100_4', hawk_dove)

"""###Stag Hunt"""

plots(BA_100_5, 'BA_100_4', stag_hunt)

"""###Snow Drift"""

plots(BA_100_5, 'BA_100_4', snow_drift)

"""## ▶ Seventh Experiment : Erdos Renyi Graph"""

def ER_Gnk(N,K):
    G=nx.Graph()
    G.add_nodes_from([i for i in range(N)])
    n_edges=0
    while n_edges<K:
        edge=rd.choice(list(combinations(G,2)))
        if (edge[0],edge[1]) not in G.edges():
            G.add_edge(edge[0],edge[1])
            n_edges+=1
    return G

N = 100
avg_degree = 5
K = N*(avg_degree)/2
ER_100_5 = ER_Gnk(N,K)

nx.draw(ER_100_5, with_labels=True)

"""###Weak Prisoner Dilemma"""

plots(ER_100_5, 'ER_100_5', weak_prisoner_dilemma)

"""###Hawk Dove"""

plots(ER_100_5, 'ER_100_5', hawk_dove)

"""###Stag Hunt"""

plots(ER_100_5, 'ER_100_5', stag_hunt)

"""###Snow Drift"""

plots(ER_100_5, 'ER_100_5', snow_drift)