#coding:utf-8

class unionfind:
    def __init__(self, groups):
        self.groups=groups
        self.items=[]
        for g in groups:
            self.items+=list(g)
        self.items=set(self.items)
        self.parent={}
        self.rootdict={} #记住每个root下节点的数量
        for item in self.items:
            self.rootdict[item]=1
            self.parent[item]=item
 
    def union(self, r1, r2):
        rr1=self.findroot(r1)
        rr2=self.findroot(r2)
        cr1=self.rootdict[rr1]
        cr2=self.rootdict[rr2]
        if cr1>=cr2:  #将节点数量较小的树归并给节点数更大的树
            self.parent[rr2]=rr1
            self.rootdict.pop(rr2)
            self.rootdict[rr1]=cr1+cr2
        else:
            self.parent[rr1]=rr2
            self.rootdict.pop(rr1)
            self.rootdict[rr2]=cr1+cr2
 
    def findroot(self, r):
        """
        可以通过压缩路径来优化算法,即遍历路径上的每个节点直接指向根节点
        """
        if r in self.rootdict.keys():
            return r
        else:
            return self.findroot(self.parent[r])
 
    def createtree(self):
        for g in self.groups:
            if len(g)< 2:
                continue
            else:
                for i in range(0, len(g)-1):
                    if self.findroot(g[i]) != self.findroot(g[i+1]): #如果处于同一个集合的节点有不同的根节点，归并之
                        self.union(g[i], g[i+1])
 
    def printree(self):
        rs={}
        for item in self.items:
            root=self.findroot(item)
            rs.setdefault(root,[])
            rs[root]+=[item]
        return [rs[key] for key in rs.keys()]
 
 
# u=unionfind([[4,3],[5,4],[4,5]])
# u.createtree()
# u.printree()