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


votes,order = list(),list()
votes = {}

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

def main():
  global votes,order
  line = stdin.readline()
  prev = post() ; authors = {}
  first = prev
  while len(line)!=0:
    body,author,ups,downs,comment_id,date,depth = "","","","","","",0
    #print(line[len(line)-4])
    i,a = len(line)-4,""
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
    if pub.depth > prev.depth: prev.comment(pub) ; prev = pub
    # si es una raíz
    elif pub.depth == 0:  prev = pub ; first = pub
    else:
      while prev.depth + 1 != pub.depth and prev.dad != None: prev = prev.dad
      prev.comment(pub) ; prev = pub
    #print(pub,end="\n\n")
    line = stdin.readline()
  #print(first)
  ansA = dfs(first,first.ups,first.downs)
  print(ansA[0])
  
  for v in order:
    print(votes[v][0],votes[v][1])
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

  for an in ansC:
    print(an[0],an[1])
  
  #print(order)
  #print(votes)
  return
main()