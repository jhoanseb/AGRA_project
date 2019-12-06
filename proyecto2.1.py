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


votes,order = {},list()
users = None    # grafo de los usuarios

def dfs(pub,lk,dlk):
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


def diftime(pub0, pub1):
  # siempre el más reciente será pub1
  segs = 0
  # diferencia de segundos
  segs = int(pub1.date[17:19])-int(pub0.date[17:19])

  if pub1.date[0:17] != pub0.date[0:17]:
    # diferencia de minutos
    if pub1.date[14:16] != pub0.date[14:16]:
      segs += 60*( int(pub1.date[14:16]) - int(pub0.date[14:16]) )

      if pub1.date[0:14] != pub0.date[0:14]:
        # diferencia de horas
        segs += 3600*( int(pub1.date[11:13]) - int(pub0.date[11:13]) )

        if pub1.date[0:11] != pub0.date[0:11]:
          # diferencia de días
          segs += 86400*( int(pub1.date[8:10]) - int(pub0.date[8:10]) )  
          
          if pub1.date[0:8] != pub0.date[0:8]:
            # diferencia de meses
            segs += (2.628*(10**6))*( int(pub1.date[5:7]) - int(pub0.date[5:7]) )    

            if pub1.date[0:4] != pub0.date[0:4]:
              # diferencia de años
              segs += (3.154*(10**7))*( int(pub1.date[5:7]) - int(pub0.date[5:7]) )
  print(segs)
  return int(segs)

# n : cantidad de usuarios 
def relations(pub,n):
  global users
  stack = list()
  stack.append((pub,0))
  while len(stack)!=0:
    u,t = stack.pop()
    for v in u.comments:
      tv,c = diftime(u,v),u
      while c.dad != None:
        find,i = False,0
        """
        while i<len(users[c]) and not(find):
          if users[c][i][0] == v: 
            j=0
            while users[v][j][0]!=c: j+=1
            users[c][i][1] 
            users[v][j]
            find = True 
          i+=1
        """
        # caso donde la relacion no existía
        if not(find):
          users[v].append((c,tv)) ; users[c].append((v,tv))
        c = c.dad
        tv = diftime(c,v)
      stack.append()
  return

def relations2(pub):
  global users
  stack = list()
  # publicacion, tiempo acumulado, tiempo del arco anterior
  stack.append((pub,0,0)) 
  while len(stack)!=0:
    u,t,bt = stack.pop()
    for v in u.comments:
      tv = diftime(u,v)
      stack.append((v,t+tv,tv))
  return 

def main():
  global votes,order, users
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
  """
  # Entrega 0: A y B
  ansA = dfs(first,first.ups,first.downs)
  print(ansA[0])
  
  for v in order:
    print(votes[v][0],votes[v][1])
  """
  aux,ansC = list(),list()
  
  for at in authors:
    heappush(aux,(authors[at],at))
  
  k,num,tmp = 0,0,list()

  while k<len(authors):
    cnt,us = heappop(aux)
    #print(cnt,us)
    if num != cnt:
      ansC = tmp + ansC
      tmp = list()
    tmp.append((us,cnt))
    num = cnt
    k+=1
  ansC = tmp + ansC

  users = [ list() for _ in range(k) ]



  """
  # Entrega 0: C
  for an in ansC:
    print(an[0],an[1])
  """
  #print(order)
  #print(votes)
  return
main()