import numpy as np
import matplotlib.pyplot as plt
import copy
import tqdm
def fill_square(up,left,i,j,n):
    uplist=[(i,j),((i+1)%n,j)]
    leftlist=[(i,j),(i,(j+1)%n)]
    if (up[i,j]+up[(i+1)%n,j]+left[i,j]+left[i,(j+1)%n])%2 == 0:
        target=0
    else:
        target=1
    if up[i,j]==2:
        up[i,j]=target
    elif up[(i+1)%n,j]==2:
        up[(i+1)%n,j]=target
    elif left[i,j]==2:
        left[i,j]=target
    elif left[i,(j+1)%n]==2:
        left[i,(j+1)%n]=target
    
def fill_plane(up1,left1,n):
    planelist=[]
    for i in range(2**((n-1)**2)):
        up=copy.deepcopy(up1)
        left=copy.deepcopy(left1)
        fill_vec=np.zeros((n-1)**2)
        s=i
        for j in range((n-1)**2):
            fill_vec[j]=(s%2)
            s=(s-fill_vec[j])/2
        #print(fill_vec)
        up[1:,:-1]=fill_vec.reshape([n-1,n-1])
        #print(up,left)
        for i in range(n):
            for j in range(n-1):
                fill_square(up,left,i,j,n)
        for i in range(n):
            fill_square(up,left,i,n-1,n)
        a=toricplane(n)
        a.init_from(up,left)
        planelist.append(a)
    return planelist



class toricplane(object):
    
    def __init__(self,l):
        self.l=l
        self.up=np.zeros([l,l])
        self.left=np.zeros([l,l])

    def init_from(self,a,b):

        assert self.up.size==a.size and self.left.size==b.size,'数组大小不正确' 
        self.up=a
        self.left=b

    def compare(self,b,up_comp_list,left_comp_list):
        for i in up_comp_list:
            w=int(i % self.l)
            h=int((i-w)/self.l)
            #print(w,h,self.up[h][w])
            if self.up[h][w] != b.up[h][w]:
                
                return False
        for i in left_comp_list:
            w=int(i % self.l)
            h=int((i-w)/self.l)
            if self.left[h][w] != b.left[h][w]:
                return False
        return True

    def print(self):
        l=self.l
        plt.figure(figsize=(l+1,l+1))
        plt.xticks([i for i in range(l+1)],fontsize=0)
        plt.yticks([i for i in range(l+1)],fontsize=0)
        for i in range(l):
            for j in range(l):
                plt.text(i+0.5,l-j+0.03,f'{self.up[j][i]}',c='blue')
                plt.text(i+0.03,l-j-0.5,f'{self.left[j][i]}',c='blue')
        for i in range(l):
            plt.text(i+0.5,0.03,f'{self.up[0][i]}',c='blue')
            plt.text(l+0.03,l-i-0.5,f'{self.left[i][0]}',c='blue')
        plt.grid()
        plt.show()

class toric(object):

    def __init__(self,n):
        self.n=n
        self.planelist=[]

    def append(self,plane:toricplane):
        self.planelist.append(plane)

    def print(self):
        for i in self.planelist:
            i.print()
            plt.show()

    def trace_print(self,up_comp_list,left_comp_list):
        l=len(self.planelist)
        res=[]
        for i in range(l):
            for j in range(l-i-1):
                a=self.planelist[i]
                b=self.planelist[i+j+1]
                if a.compare(b,up_comp_list,left_comp_list):
                    a.print()
                    b.print()
                    print('==================================================')

    def trace(self,up_comp_list,left_comp_list):
        l=len(self.planelist)
        res=[]
        for i in tqdm.tqdm(range(l)):
            for j in range(l-i-1):
                a=self.planelist[i]
                b=self.planelist[i+j+1]
                if a.compare(b,up_comp_list,left_comp_list):
                    res.append((i,i+j+1))
        return res
    
    def generate_plane(self):
        n=self.n
        edge=np.zeros(n)
        edgelist=[]

        #生成边的可选列表
        for i in range(2**n):
            s=i
            for j in range(n):
                edge[j]=(s%2)
                s=(s-edge[j])/2
            if edge.sum()%2==0:
                edgelist.append(copy.deepcopy(edge))

        planeup=2*np.ones([n,n])
        planeleft=2*np.ones([n,n])
        #print(edgelist)
        for indexi,i in enumerate(edgelist):
            for indexj,j in enumerate(edgelist):
                planeup[0,:]=i
                planeleft[:,0]=j
                a=fill_plane(planeup,planeleft,n)
                self.planelist.extend(a)
                