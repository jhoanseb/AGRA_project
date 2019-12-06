from sys import stdin
from collections import deque
from heapq import heappop, heappush

class post(object):
  def __init__(self,body="",author="",ups=0,downs=0,comment_id="",date="",depth=0,dad=None):
    self.body = body
    self.author = author
    self.ups = ups
    self.downs = downs
    self.id = comment_id
    self.date = date
    self.depth = depth
    self.comments = list()      # lista de mis comentarios hijos
    self.dad = dad              # comentario padre
  
  def __str__(self):
    p = self.body+' '+self.author+' '+str(self.ups)+' '+str(self.downs)
    p = p +' '+self.id+' '+self.date+' '+str(self.depth)
    return p

  def comment(self,c):
    self.comments.append(c)
    c.dad = self

def ancestro(i,padres):
  if i == padres[i]: return i
  j = ancestro(padres[i],padres)
  padres[i] = j
  return j

def merge(i,j,padres):
  if ancestro(i,padres)!=ancestro(j,padres):
    padres[i] = ancestro(j,padres)
  return padres

votes,order = {},list()
# grafo de los usuarios
users,aorder,grado = None,None,None
INF = float('inf')

def dfs(pub,lk,dlk):
  """calcula la cantidad de likes y dislikes por usuario en el arbol"""
  global votes,order
  preorder,likes,dislikes = pub.id,lk,dlk
  order.append(pub.id)
  for c in pub.comments:
    sub = dfs(c,c.ups,c.downs)
    preorder = preorder + ' ' + sub[0]
    likes += sub[1] ; dislikes += sub[2]
  #votes.append((likes,dislikes))
  votes[pub.id] = (likes,dislikes)
  return (preorder, likes, dislikes)

# des : desendencia del nodo u
def relations(u,cam,t):
  """crea las relaciones de los usuarios en el grafo users"""
  global users,aorder,grado
  des,delt,tmp = None,t,cam[:]
  for v in u.comments:
    tv = diftime(u,v)
    #print(tv)
    des = relations(v,cam,tv) ; j = aorder[u.author]
    #print(des)
    for i in range(len(des)):
      us,a,b,findj,findus = des[i][0],0,0,False,False
      while (a<len(users[j]) or b<len(users[us])) and (not(findj) or not(findus)):
        if a<len(users[j]) and users[j][a][0] == us: findj = True 
        if b<len(users[us]) and users[us][b][0] == j: findus = True
        if not findj: a+=1
        if not findus: b+=1
      if findj:
        prom = (users[j][a][1]+users[us][b][1])/2
        users[j][a] = (users[j][a][0],int(prom))
        users[us][b] = (users[us][b][0],int(prom))
      elif us!=j:
        grado[us] += 1 ; grado[j] += 1
        users[us].append((j,des[i][1])) ; users[j].append((us,des[i][1]))
      des[i][1] += delt
      #print(des)
    tmp += des
  #for i in range(len(users)):
  #    print(i, users[i])
  return tmp + [[aorder[u.author],delt]]

def voronoi(users, centers, conv):
  padres = [ i for i in range(len(users)) ]
  way = [ INF for _ in users ]
  ans = [ conv[s] for s in centers ]
  for s in centers: way[s] = 0
  visited = [ False for _ in users ]
  heap = [ (0, s, s) for s in centers ]
  while len(heap)!=0:
    #print(padres)
    t,u,c = heappop(heap)          
    if visited[u] == False:
      for v,tv in users[u]:
        if t+tv<way[v] and not(v in centers):
          way[v] = t+tv
          #print(v,c)
          #ans[c] += " " + conv[v]
          padres = merge(v,c,padres)
          heappush(heap, (way[v], v, c)) 
      visited[u] = True
  #print(conv[2])
  #print(padres)
  #times = [ "" for _ in centers ]
  times = [ 0 for _ in centers ]
  for i in range(len(padres)):
    #if i == 99: print(way[i])
    if padres[i]!=i: 
      ans[padres[i]] += " " + conv[i]
      #times[padres[i]] += " " + str(way[i])
      times[padres[i]] += way[i]
  for s in centers:
    print(ans[s],times[s])
    print()

  return way


def diftime(pub0, pub1):
  """funcion que me retorna la diferencia de tiempo entre publicaciones"""
  # siempre el más reciente será pub1
  
  seg0,seg1 = 0,0
  # diferencia de segundos
  seg1 = int(pub1.date[17:19]) ; seg0 = int(pub0.date[17:19])

  if pub1.date[0:17] != pub0.date[0:17]:
    # diferencia de minutos
    if pub1.date[14:16] != pub0.date[14:16]:
      seg1 += 60*int(pub1.date[14:16])
      seg0 += 60*int(pub0.date[14:16]) 

      if pub1.date[0:14] != pub0.date[0:14]:
        # diferencia de horas
        seg1 += 3600*int(pub1.date[11:13]) 
        seg0 +=  3600*int(pub0.date[11:13]) 

        if pub1.date[0:11] != pub0.date[0:11]:
          # diferencia de días
          seg1 += 86400*int(pub1.date[8:10])
          seg0 += 86400*int(pub0.date[8:10]) 
          
          if pub1.date[0:8] != pub0.date[0:8]:
            # diferencia de meses
            seg1 += (2.628*(10**6))*int(pub1.date[5:7]) 
            seg0 += (2.628*(10**6))*int(pub0.date[5:7]) 

            if pub1.date[0:4] != pub0.date[0:4]:
              # diferencia de años
              seg1 += (3.154*(10**7))*int(pub1.date[5:7])
              seg0 += (3.154*(10**7))*int(pub0.date[5:7]) 
  segs = seg1 - seg0 if seg1-seg0>=0 else seg0 - seg1
  return int(segs)

def max_g(grado,n):
  i_grado,max_grado = {}, grado[0]
  for i in range(n):
    i_grado[grado[i]] = i_grado[grado[i]]+1 if grado[i] in i_grado else 1
    if i_grado[grado[i]] > i_grado[max_grado]: max_grado = grado[i]
  #print(i_grado)
  max_grado = 2 if max_grado<2 else max_grado
  return max_grado

def preorderSecuencia(pub):
  print(pub.id, end=" ")
  secuencia(pub)
  for i in pub.comments:
    preorderSecuencia(i)

def secuencia(pub):
  body = pub.body
  body = body.lower()
  palabra = ""
  palabras = []
  centinela = True
  for i in range(len(body)):
    #  or 140<=ord(body[i]) - anexar para que funcionen los emojis
    if(97 <= ord(body[i]) <= 122 or 48 <= ord(body[i]) <= 57):
      palabra+=body[i]
    elif(len(palabra)!= 0):
      centinela = False
    if(centinela==False):
      palabras.append(palabra)
      palabra=""
      centinela=True
  if(palabra != ""):
    palabras.append(palabra)
  sinRep = list(set(palabras))
  i=0
  aux = []
  centinela = True
  interi = i
  pos = [0,INF]
  ordenes=[]
  while(i < len(palabras)):  
    if (palabras[i] not in aux):
      aux.append(palabras[i])
    if(len(aux) == len(sinRep)):
      centinela = False
      nuevo = [interi,i]
      if(pos[1] == INF):
        pos=nuevo
        pos[1]+=1
        if(pos not in ordenes):
          ordenes.append(pos)
      res2 = pos[1]-pos[0]
      res1 = nuevo[1]-nuevo[0]
      if (res2 >= res1):
        pos1, pos2= nuevo[0],nuevo[1]+1               
        if([pos1,pos2] not in ordenes):
          ordenes.append([pos1,pos2])
    if(centinela==False):
      aux = []
      i=interi+1
      interi=i
      centinela = True
    else:
      i+=1
  mini=(ordenes[0][0],ordenes[0][1])
  actual= ordenes[0][1]-ordenes[0][0]
  for i in range(len(ordenes)):
    if(ordenes[i][1]-ordenes[i][0]<actual):
      actual=ordenes[i][1]-ordenes[i][0]
      mini=(ordenes[i][0],ordenes[i][1])
  print(mini[0],mini[1])

def main():
  global votes,order,users,aorder,grado
  line = stdin.readline()
  prev = post() ; authors = {}
  first = prev
  while len(line)!=0:
    body,author,ups,downs,comment_id,date,depth = "","","","","","",0
    #print(line[len(line)-4])
    i,a = len(line)-3,""
    while line[depth]!='>': depth+=1
    while line[i]!='[':
      a = line[i] + a
      if line[i-1]=='|':
        if len(date)==0: date = a ; a = "" 
        elif len(comment_id)==0: comment_id = a ; a = ""
        elif len(downs)==0: downs = a ; a = ""
        elif len(ups)==0: ups = a ; a = ""
        i-=1
      if line[i-1]=='[' and len(author)==0: author = a ; a = ""
      i-=1
    if author in authors: authors[author]+=1
    else: authors[author]=1
    j = depth+1
    while j<i:
      body += line[j] ; j+=1
    depth=depth>>1

    pub = post(body,author,int(ups),int(downs),comment_id,date,depth)

    """
    # prueba de la correctitud del tiempo
    if len(prev.body)!=0:
      print(pub.date,end="\n")
      print(diftime(prev,pub))
      print(prev.date, end="\n")
    """

    if pub.depth > prev.depth: prev.comment(pub) ; prev = pub
    # si es una raíz
    elif pub.depth == 0:  prev = pub ; first = pub
    else:
      while prev.depth + 1 != pub.depth and prev.dad != None: prev = prev.dad
      prev.comment(pub) ; prev = pub
    #print(pub,end="\n\n")
    line = stdin.readline()
  #print(first)
  
  # Entrega 0: A y B
  ansA = dfs(first,first.ups,first.downs)
  print(ansA[0])
  
  for v in order:
    print(votes[v][0],votes[v][1])
  
  aux,ansC = list(),list()
  
  for at in authors:
    heappush(aux,(authors[at],at))
  
  k,num,tmp = 0,0,list()

  while k<len(authors):
    """organiza los usuarios en el orden pedido"""
    cnt,us = heappop(aux)
    #print(cnt,us)
    if num != cnt:
      ansC = tmp + ansC
      tmp = list()
    tmp.append((us,cnt))
    num = cnt
    k+=1
  ansC = tmp + ansC
  
  # Entrega 0: C
  for an in ansC:
    print(an[0],an[1])
  
  #print(order)
  #print(votes)

  """
  users   : grafo de usuarios
  aorder  : conversion de nombres de usuarios a indices numericos
            en orden.
  valeria : conversion de indices al respectivo nombre de usuario.
  """
  grado,users,aorder,valeria = list(),list(),{},list()
  for j in range(k):
    """ciclo inicializador de las variables"""
    users.append(list())
    grado.append(0)
    aorder[ansC[j][0]] = j
    valeria.append(ansC[j][0])

  relations(first,list(),0)     
  """
  print(users)
  print(valeria[0])
  print(len(users[0]))
  for us in users[0]:
    print(valeria[us[0]])
  """
  max_grado = max_g(grado,k)
  #print(max_grado)
  #print(aorder["eggonsnow"])
  voronoi(users, [i for i in range(max_grado)],valeria)

  preorderSecuencia(first)
  return
main()