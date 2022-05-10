# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 16:42:58 2022

@author: abdlb
"""
import pulp
import pandas as pd

phoc = 0.95
phod = 0.95
nu=40

#Fonction indicatrice
def indic(a):
    if a<=nu:
        return 1
    else:
        return 0
    
#Renvoie le delta_t 
#tarriv est un tableau de taille 365 de tableaux de taille 4
#tel que tarriv[i][j] renvoie l'heure d'arrivée de la voiture j au jour i (avec j de 1à4 et i de 1à365)
#df = pd.read_csv("C://Users//thoma//Desktop//ENPC - 1A//Optimisation et énergie//serious_game//ev_scenarios_v2.csv", sep=";", decimal=".")
#df = pd.read_csv("C://Users//thoma//Desktop//ENPC - 1A//Optimisation et énergie//serious_game//ev_scenarios_v2.csv", sep=";", decimal=".")

df = pd.read_csv("C://Users//abdlb//Downloads//ev_scenarios_v2.csv", sep=";", decimal=".")


time_dep1 = df.loc[:,"time_slot_dep"]
time_dep = []

for i in range(0,1460,4):
    time_dep.append([time_dep1[k] for k in range(i,i+4)])
    
time_arr1 = df.loc[:,"time_slot_arr"]
time_arr = []
for i in range(0,1460,4):
    time_arr.append([time_arr1[k] for k in range(i,i+4)])
    
lam=[]
for i in range(48):
    lam.append([1,1,1,1])
    
    
def take_decisionbis(lam,phoc,phol,tarriv,tdep):
    exemple = pulp.LpProblem("gestion bornes recharges", pulp.LpMinimize)
    a1={}
    a2={}
    a3={}
    a4={}
    delta=30
    t1arriv=delta*tarriv[0]
    t2arriv=delta*tarriv[1]
    t3arriv=delta*tarriv[2]
    t4arriv=delta*tarriv[3]
    t1dep=tdep[0]
    t2dep=tdep[1]
    t3dep=tdep[2]
    t4dep=tdep[3]
    for t in range(int(t1arriv)):
        a1[t]=pulp.LpVariable("a1_"+str(t), 0.0 )
    for t in range(int(t2arriv)):    
        a2[t]=pulp.LpVariable("a2_"+str(t), 0.0 )
    for t in range(int(t3arriv)):   
        a3[t]=pulp.LpVariable("a3_"+str(t), 0.0 )
    for t in range(int(t4arriv)):   
        a4[t]=pulp.LpVariable("a4_"+str(t), 0.0 )
    # variables (continues de valeur minimale 0)
    l1 = pulp.LpVariable("l1",0,3)
    l1pos=pulp.LpVariable("l1pos",0)
    l1neg=pulp.LpVariable("l1neg",0)
    l2 = pulp.LpVariable("l2",0,3)
    l2pos=pulp.LpVariable("l2pos",0)
    l2neg=pulp.LpVariable("l2neg",0)
    l3 = pulp.LpVariable("l3",-22,22)
    l3pos=pulp.LpVariable("l3pos",0)
    l3neg=pulp.LpVariable("l3neg",0)
    l4 = pulp.LpVariable("l4",-22,22)
    l4pos=pulp.LpVariable("l4pos",0)
    l4neg=pulp.LpVariable("l4neg",0)
    exemple += l1+l2+l3+l4  <=40
    exemple += -l1-l2-l3-l4 <=40
    L=[l1,l2,l3,l4]
    exemple += a1[0] == 0
    exemple += a2[0] == 0
    exemple += a3[0] == 0
    exemple += a4[0] == 0
    for t in range(int(t1arriv)-1):
       exemple +=  a1[t+1] == (a1[t]+(phoc*l1pos)-(1/(phod))*l1neg*delta)
    for t in range(int(t2arriv)-1):
       exemple +=  a2[t+1]== (a2[t]+(phoc*l2pos)-(1/(phod))*l2neg*delta)
    for t in range(int(t3arriv)-1):
       exemple +=  a3[t+1]== (a3[t]+(phoc*l3pos)-(1/(phod))*l3neg*delta)
    for t in range(int(t4arriv)-1):
       exemple +=  a4[t+1]== (a4[t]+(phoc*l4pos)-(1/(phod))*l4neg*delta)
    exemple += a1[int(t1arriv)-1]==a1[int(t1dep)]-4
    exemple += a2[int(t2arriv)-1]==a2[int(t2dep)]-4
    exemple += a3[int(t3arriv)-1]==a3[int(t3dep)]-4
    exemple += a4[int(t4arriv)-1]==a4[int(t4dep)]-4
    exemple += l1== l1pos - l1neg
    exemple += l2== l2pos - l2neg
    exemple += l3== l3pos - l3neg
    exemple += l4== l4pos - l4neg
    exemple+= ( pulp.lpSum(lam[i]*L[i] for i in range(4)) 
                          + 5*indic(a1[t1dep]) + 5*indic(a2[t2dep]) + 5*indic(a3[t3dep]) + 5*indic(a4[t4dep]) )  
    exemple.objective.setName('z')
    exemple.solve()
    l=[pulp.value(l1),pulp.value(l2),pulp.value(l3),pulp.value(l4)]
    return l

def take_decision(lam,phoc,phod):
    lopti=[]
    for i in range(48):
        lam1=lam[i]
        for i in range(len(time_dep)):
            tarriv=time_arr[i]
            tdep=time_dep[i]
            lopti.append(take_decisionbis(lam1,phoc,phod,tarriv,tdep))
    return lopti

lopti=take_decision(lam,phoc,phod) 
       
#df=pd.red_csv(filename,rep=";")