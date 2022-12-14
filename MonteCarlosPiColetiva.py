#Código com resultado para Pi Monte Carlo com comunicação coletiva/broadcast-reduce
from mpi4py import MPI
import datetime
import numpy as np
import random as r
import math as m

def monteCarloPi(inicio, fim):
    acertos=0
    for i in range(inicio, fim+1):
        x2 = r.random()**2
        y2 = r.random()**2
        if m.sqrt(x2 + y2) < 1.0:
            acertos += 1
    return (float(acertos) / num) * 4   


comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

val = np.zeros(1,"i") #cria um vetor de inteiros com um valor e preenchido com zeros

if rank == 0:
  print("Digite o numero para calcular o somatorio de Pi Monte Carlos:")
  num=int(input())
  
  wt = MPI.Wtime()
  start_time = datetime.datetime.now()
  
  val[0]=num
  
  val=comm.bcast(val,root=0) #faz o broadcast de val para todos os processos com raiz(root) no mestre(0)

  parte=int(num/size)
  inicio=parte*rank+1
  fim=parte*(rank+1)
  if(rank == size-1):
    fim=num

  soma=monteCarloPi(inicio,fim)
  
  soma=comm.reduce(soma,op=MPI.SUM, root=0) #faz o reduce de soma de todos os processos com raiz(root) no mestre(0) com operacao de soma (MPI.SUM)
     
  wt = MPI.Wtime() - wt
  
  end_time = datetime.datetime.now()

  time_diff = (end_time - start_time)
  execution_time = time_diff.total_seconds() 

  print("Resultado final do somatorio de Pi Monte Carlos=",soma)
  print("Tempo de execucao em segundos de relogio: ",wt)
  print("Tempo de execucao02 em segundos de relogio: ",execution_time)
  
  
else:
  val=comm.bcast(val,root=0) #faz o broadcast de val para todos os processos com raiz(root) no mestre(0)
  
  num=val[0]
  
  parte=int(num/size)
  inicio=parte*rank+1
  fim=parte*(rank+1)
  if(rank == size-1):
    fim=num

  soma=monteCarloPi(inicio,fim)
  
  soma=comm.reduce(soma,op=MPI.SUM, root=0) #faz o reduce de soma de todos os processos com raiz(root) no mestre(0) com operacao de soma (MPI.SUM)
  
   
  
