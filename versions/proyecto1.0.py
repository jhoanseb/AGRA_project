from sys import stdin

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

  def get_Comments(self):
    return self.comments

  def comment(self,c):
    self.comments.append(c)
    c.dad = self
  """
  def preorder(self):
    ans = self.id
    for i in self.comments:
      ans += " " + i.preorder()
    return ans
  

def dfs(pub):
  stack = list()
  stack.append(pub)
  while len(stack)!=0:
    p = stack.pop()
    for c in p.comments:
      preorder =

  return 
"""

#votes = {}
votes = list()

def dfs(pub,lk,dlk):
  global votes
  preorder,likes,dislikes = pub.id,lk,dlk
  for c in pub.comments:
    sub = dfs(c,c.ups,c.downs)
    preorder = preorder + ' ' + sub[0]
    likes += sub[1] ; dislikes += sub[2]
    print(likes,dislikes)
  #print(lk,dlk)
  votes.append((likes,dislikes))
  #votes[pub.id] = (likes,dislikes)
  return (preorder, likes, dislikes)

def main():
  global votes
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
    elif pub.depth == 0:  prev = first = pub
    else:
      while prev.depth + 1 != pub.depth and prev.dad != None: prev = prev.dad
      prev.comment(pub) ; prev = pub
    #print(pub,end="\n\n")
    line = stdin.readline()
  #print(prev.preorder())
  print(first)
  print(dfs(first,first.ups,first.downs))
  print(votes)
  return
main()