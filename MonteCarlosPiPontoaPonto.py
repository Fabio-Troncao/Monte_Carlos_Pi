#Exercício Somatório Distribuído onde o Mestre também Processa em MPI4PYArquivo com comunicação ponto a ponto/send-recv
from mpi4py import MPI
import datetime
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

if rank == 0:
  print("Digite o numero para calcular o somatorio de Pi Monte Carlos:")
  num=int(input())
  
  wt = MPI.Wtime()
  start_time = datetime.datetime.now()
  
  
  wt2 = MPI.Wtime()
  start_time2 = datetime.datetime.now()
  for i in range(1,size):
    comm.send(num, dest=i,tag=1)
  
  wt2 = MPI.Wtime() - wt2
  end_time2 = datetime.datetime.now()
    
  parte=int(num/size)
  inicio=parte*rank+1
  fim=parte*(rank+1)
  if(rank == size-1):
    fim=num

  soma=monteCarloPi(inicio,fim)

  wt3 = MPI.Wtime()
  start_time3 = datetime.datetime.now()
  for i in range(1,size):
     info = MPI.Status() 
     s=comm.recv(source=i,tag=2,status=info)
     print("rank do escravo do qual recebeu=",info.Get_source())
     soma=soma+s

  wt3 = MPI.Wtime() - wt3
  end_time3 = datetime.datetime.now()   
     
  wt = MPI.Wtime() - wt
  end_time = datetime.datetime.now()

  time_diff = (end_time - start_time)
  execution_time = time_diff.total_seconds() 

  print("Resultado final do somatorio de Pi Monte Carlos=",soma)
  print("Tempo de execucao em segundos de relogio: ",wt)
  print("Tempo de execucao02 em segundos de relogio: ",execution_time)
  print("Tempo de comunicacao: ", (wt2+wt3))
  
  
else:
  num = comm.recv(source=0,tag=1)
  print ("Escravo de rank %d: %d" % (rank, num))
  
  parte=int(num/size)
  inicio=parte*rank+1
  fim=parte*(rank+1)
  if(rank == size-1):
    fim=num

  soma=monteCarloPi(inicio,fim)
  comm.send(soma, dest=0,tag=2)