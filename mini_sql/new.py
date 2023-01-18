import re
import sys
import copy
import csv
import math
op=open('metadata.txt','r')
line=op.readlines()
count=0
flag=0
d={}
de={}
e={}
l=1
mie=[]
#print(line[0],end="")
for r in line:
    z=len(r)-1
    ro=r[0:z].lower()
    #print(ro,end="")
    if(ro=="<begin_table>"):
        mie=[]
        flag=1
        l=1
        #print('*')
        continue
    if(ro=="<end_table>"):
        e[temp]=mie.copy()
        continue
    if(flag==1):
        temp=ro
        flag=0
        continue
    d[ro]=(temp,l)
    mie.append(ro)
    l=l+1
    #print(d[ro],ro)
    #print(e)


def readtb(tab):
    try :
        red = open('{0}.csv'.format(tab), 'r')
    except :
        print("table not found")
        sys.exit()
    cs=csv.reader(red,delimiter=',')
    l=[]
    #print("p1",red,cs,l)
    for i in cs:
        te=[]
        for j in i :
            hi=(j.split('"'))
            hi=hi[0]
            te.append(int(hi))#each row in table store as a list
            #print("hi",hi)
            #print("te",te)
        l.append(te)
    #print("printing 3111",l)
    return l

def jointb(tab1,tab2):
    l=[]
    #print(tab1)
    #print(tab2)
    for i in range(len(tab1)):
        for j in range(len(tab2)):
            me1=tab1[i].copy()
            me1.extend(tab2[j])
            #print(me1)
            l.append(me1)
        #print("printing 32",l) #prints both the table columns as each list
    return l

def mtb(tab):
    if(len(tab)==1):
        return readtb(tab[0]),e[tab[0]]
    #print("ooo",tab[1])
    ta=readtb(tab[0])
    tem=e[tab[0]] #colum names(a,b,c)
    ta2=readtb(tab[1])
    tem2=e[tab[1]]
    #print("printing 31",tem,tem2)
    for i in range(1,len(tab)):
        #print(e[tab[i]])
        #print("kk",ta)
        ta=jointb(ta,readtb(tab[i]))
        tem.extend(e[tab[i]])
    #print("fin",ta,tem)   #it returns all the columns,columnames 
    return ta,tem

def etb(tab,cols,req):
    tab1=[[row[i] for row in tab] for i in range(len(tab[0]))]
    me=[]
    #print(req)
    #print(cols)
    for i in range(len(req)):
        for j in range(len(cols)):
            if(cols[j]==req[i]):
                me.append(tab1[j])
                break
    req=[x for x in req if x]
    if(len(me)!=len(req)):
        print("not every column is present in table")
        sys.exit()
    tab1=[[row[i] for row in me] for i in range(len(me[0]))]
    #print(tab1)
    return tab1


def liger(a,arr,coll):
    try : 
        int(a)
        return int(a)
    except :
        for i in range(len(coll)):
            if(coll[i]==a):
                return arr[i]
        print('column does not exist')
        sys.exit()
def cons(a,b,op,arr,colm):
    #print('hi--',integer(a,arr,cols),integer(b,arr,cols))
    if(op=='='):
        if(liger(a,arr,colm)==liger(b,arr,colm)):
            return True
        else :
            return False
    if(op=='<'):
        if(liger(b,arr,colm)>liger(a,arr,colm)):
            return True
        else :
            return False
    if(op=='<='):
        if(liger(b,arr,colm)>=liger(a,arr,colm)):
            return True
        else :
            return False
    if(op=='>='):
        if(liger(b,arr,colm)<=liger(a,arr,colm)):
            return True
        else :
            return False
    if(op=='>'):
        if(liger(b,arr,colm)<liger(a,arr,colm)):
            return True
        else :
            return False
    
def wher_ext(t,s,strri,arr,cols): 
    str11=''
    str12=''
    str21=''
    str22=''
    op1=''
    op2=''
    #print("ws1",t,s,len(t))
    for i in range(len(t)):
        if(t[i]=='<' or t[i]=='>' or t[i]=='='):
            if(t[i]=='='):
                #print("hhh")
                str11=t[:i]
                str12=t[i+1:]
                op1='='
          #      print("ws2",str11,str12,op1)
            else :
                if(t[i+1]=='='):
                    str11=t[:i]
                    str12=t[i+2:]
                    op1=t[i]+t[i+1]
         #           print("ws3",str11,str12,op1)
                else :
                    str11=t[:i]
                    str12=t[i+1:]
                    op1=t[i]
        #            print("brooo")
       #             print("ws4",str11,str12,op1)
            break
    for i in range(len(s)):
        if(s[i]=='<' or s[i]=='=' or s[i]=='>'):
            if(s[i]=='='):
                str21=s[:i]
                str22=s[i+1:]
                op2='='
            else :
                if(s[i+1]=='='):
                    str21=s[:i]
                    str22=s[i+2:]
                    op2=s[i]+s[i+1]
                else :
                    str21=s[:i]
                    str22=s[i+1:]
                    op2=s[i]
            break
    l=[] 
    for i in range(len(arr)):
        #print("ws5",len(arr),arr[i])
        if(strri=='and'):
            #print('*')
            if(cons(str11,str12,op1,arr[i],cols) and cons(str21,str22,op2,arr[i],cols)):
                l.append(arr[i])
        if(strri=='or'):
            #print('^')
            if(cons(str11,str12,op1,arr[i],cols) or cons(str21,str22,op2,arr[i],cols)):
                l.append(arr[i])
               # print("sd",l,cols)
    return l

def wher(comm,arr,cols):
    #print('in wher',comm)
    #lc=len(comm)
   # print("lc",lc)
    if(('and' in comm) or ('or'in comm)):
        t=''
        s=''
        if('or' in comm):
            for j in range(len(comm)):
                if(comm[j]=='or'):
                    break
                t=t+comm[j]
            for j in range(len(comm)):
                if(comm[0]=='or'):
                    comm.pop(0)
                    break
                comm.pop(0)
            for j in range(len(comm)):
                if(comm[j]=='group' or comm[j]=='order'):
                    break
                s=s+comm[j]
            return wher_ext(t,s,'or',arr,cols)
        if('and' in comm):
            t=''
            s=''
            for j in range(len(comm)):
                if(comm[j]=='and'):
                    break
                t=t+comm[j]
    #            print("w1",t)
            for j in range(len(comm)):
                if(comm[0]=='and'):
                    comm.pop(0)
                    break
                comm.pop(0)
     #           print("w3",len(comm))
            for j in range(len(comm)):
                if(comm[j]=='group' or comm[j]=='order'):
                    break
                s=s+comm[j]
      #          print("w2",s)
            return wher_ext(t,s,'and',arr,cols)
        
    else :
        t=''
        for i in range(len(comm)):
            if(comm[i]=='group' or comm[i]=='order'):
                break
            t=t+comm[i]
        return wher_ext(t,t,'or',arr,cols)



def func(a,b):
    #print(a,b)
    if(b.lower()=='count'):
        return len(a)
    if(b.lower()=='sum'):
        return sum(a)
    if(b.lower()=='avg'):
        return sum(a)/len(a)
    if(b.lower()=='min'):
        return min(a)
    if(b.lower()=='max'):
        #print('here')
        #print(max(a))
        return max(a)
def col_func(cols,aggs):
    temp=[]
    for i in range(len(cols)):
        if(aggs[i]!=''):
            temp.append(aggs[i]+'('+cols[i]+')')
        else:
            temp.append(cols[i])
    return temp
def group(arr,cols,aggs,n):
    gro=[]
    for i in range(n,len(cols)):
        arr=sorted(arr,key = lambda x:x[i])
    while(1):
        if(len(arr)==0):
            break
        temp=arr[0].copy()
        #arr.pop(0)
        me=[]
        l=[[]for i in range(len(cols))]
        #for i in range(len(temp)):
         #   if(aggs[i]!=''):
        for i in range(len(arr)):
            flag_here=0
            for j in range(len(aggs),len(cols)):
                if(temp[j]!=arr[i][j]):
                    flag_here=1
            if(flag_here==0):
                me.append(arr[i])
                for ii in range(len(aggs)):
                    if(aggs[ii]!=''):
                        l[ii].append(arr[i][ii])
        #print('--',me)
        for i in range(len(aggs)):
            if(aggs[i]!=''):
                temp[i]=func(l[i],aggs[i])
            #print('hi madhuri',temp[i])
        for i in range(len(me)):
            for j in range(len(arr)):
                if(me[i]==arr[j]):
                    #print('*',i,end='')
                    arr.pop(j)
                    break
        gro.append(temp)
        #print('--',temp)
    #print(cols,aggs)
    cols[:n]=col_func(cols[:n],aggs)
    gro=etb(gro,cols,cols[:n])
    return gro,cols[:n]


def order(arr,cols,req):
    #print('order by--',arr)
    req.reverse()
    oder=1
    for j in range(len(req)):
        tempoo=0
        if(req[j]=='desc'):
            oder=-1
        if(req[j]=='desc' or req[j]=='asc'):
            continue
        for i in range(len(cols)):
            if(cols[i]==req[j]):
                arr=sorted(arr,key=lambda x:oder*x[i])
                tempoo=1
                oder=1
                break
        if(tempoo==0):
            print('column not found for ordering')
            sys.exit()
        oder=1
    return arr,cols


def aggregates(arr,cols,req,aggs,ms):
    aggs=[x for x in aggs if x]
    if(len(aggs)!=0 and len(aggs)!=len(req)):
        print('aggregates found without group by')
    if(len(aggs)==0):
        return [arr,cols],ms
    etb(arr,cols,req)
    arr1=[[row[i] for row in arr] for i in range(len(arr[0]))]
    x=[0 for i in range(len(aggs))]
    for i in range(len(aggs)):
        x[i]=func(arr1[i],aggs[i])
    return [[x],col_func(req,aggs)],col_func(req,aggs)

def print_ans(arr,cols,aggs=False):
    if(aggs):
        cols1=col_func(cols,aggs)
        cols1,cols=cols,cols1
    else :
        cols1=cols.copy()
        for i in range(len(cols1)):
            if('(' in cols[i]):
                for j in range(len(cols[i])):
                    if(cols[i][j]=='('):
                        cols1[i]=cols[i][j+1:]
                        break
            cols1[i]=cols1[i].rstrip("()")
    print(d[cols1[0]][0],'.',cols[0],sep='',end='')
    for i in range(1,len(cols)):
        print(',',d[cols1[i]][0],'.',cols[i],sep='',end='')
    print()
    if(len(arr)==0 or len(arr[0])==0):
        print('empty table or no rows')
        sys.exit()
    for i in range(len(arr)):
        print(arr[i][0],end='',sep='')
        for j in range(1,len(arr[i])):
            print(',',arr[i][j],sep='',end='')
        print()
    #print(len(arr))
    sys.exit()


def sown(a): #passing the columns (before From)
    tp1=[]
    tp2=[]
    #print("number of elements in l passing to fun ",len(a))
    for i in range(len(a)):
        flag=0
        here=''
        here1=''
        for j in range(len(a[i])):
         #   print("print19=",i,j)
         #  print("print199=",a[i][j])

            if(a[i][j]=='('):
                #print(j)
                here1=a[i][:j]
                here=a[i][j+1:-1]
                flag=1
                break
        #print("print20=",here1)
        #print("print21=",here)        
        if(flag==1):

            tp1.append(here)
            tp2.append(here1)
        else:
            tp1.append(a[i])  #if there is no brackets the colums(before From) get appended into temp1 
            tp2.append('')   #if there is bracket the thing before bracket gets appended here and after bracket gets appended in temp1
        #print("print22=",temp1)
        #print("print23=",temp2)

    return tp1,tp2
def main():
    c=sys.argv[1]                #query which we give
    #print("actual query=",c)
    c=c.lower()              #converting query into lowercase
    #print("actual query in lowercase=",c)
    c=c.strip()

    s1_c=c
    cstore=c
    com_dup=c.lower()
    if(bool(re.match('select.*from.*',com_dup))==False):
        print('wrong format:select or from in the query are missing')
        sys.exit()
    #print("splitting=",c)
    #print("print6=",c[0])

    if(c[-1]!=';'):         #checking whether query is ending with semicolon or not
        print('semicolon at the end of query is missing')
        sys.exit()
    c=c[:-1]      
    c=c.split()  #splits the string(query) into individual words
    #print("print4=",c)
    #c=c.split()  #splits the string(query) into individual words
    #print("splitting=",c)
    #print("print6=",c[0])
    #if(c[0].lower()!='select'):
      #  print('select is missing')
     #   sys.exit()
    c.pop(0)  #poping the select
    er=0
    l=[]
    #print("printimg l and com",l,com)
    for i in c :
        #print("print11=",i)
        if(i.lower()=='from'):
            #print('1.from after select is not possible')
            er=1
            break
        l.extend(i.split(','))  #if there is any columns or star infront of FROM gets copied into "l" 

    #print("print12 list l=",l)
    n=len(c)
    #print("print13 =",c)
    #print("print14 length of c=",n)
    for i in range(n):
        if(c[0].lower()=='from'):
           # print('2.from after select is not possible')
            c.pop(0)
            break
        c.pop(0)
     #   print("printing 15",c) # in com we have from,table

    col=[x for x in l if x] #.....................................??????????????????????
    flag_distinct=0
    if(col[0]=='distinct'):
        col.pop(0)
        flag_distinct=1
    col_copy=col.copy()
    #print("printing 16 in list l",col_copy)


#print(col_copy)
    col,agg=sown(col)
    agg_copy=[x for x in agg if x]
    #print("print25=",col,agg,len(agg))
    #print("print26=",agg_copy,len(agg_copy))
    #print("print27 after from =",c)  #after from

#print(col,agg)
    if(len(agg_copy)!=len(col) and 'group' not in c and len(agg_copy)!=0):
        print('group not found in less number of aggregates')
        sys.exit()
    flag_group=0
    if('group' in c):
        flag_group=1
#print(col,agg,agg_copy)
    l=[]
    splitting=['where','group','order']
    for i in c:
        if(i.lower() in splitting):
            break
        l.extend(i.split(','))
     #   print("printing 28 new l",l)
    tab=[x for x in l if x]
    n=len(c)
    #print("printing 29",c,n,l)
    for i in range(n):
        if(c[0].lower() in splitting):
            break
        c.pop(0)
     #   print("printing 30",c,set(tab),len(set(tab)),tab)
    
#print(tab)
    if(er==0):
        print('from not found after any space ie. spacing error')
        sys.exit()
    if(len(set(tab))!=len(tab)):
        print('tables you entered are not unique')
        sys.exit()

#print(c)


# In[9]:
    fin=mtb(tab)
    #print(fin)
    star=['*']
    m=len(agg)
    #print("print m",agg,len(agg))
    for i in range (m):
     #   print("print 34",i)
        if(agg[i]=='count'):
            if(col[i]=='*'):
                col[i]=fin[1][0]
                #print("worked")
                #print("sim",fin[1],fin[1][0])

#print(col)
#print()
#print()
    if(col[0]=='*'):
        col.pop(0)
        t=fin[1].copy()
      #  print("dd",t,col)
        t.extend(col)
        col=t
     #   print("coo",col,t)
        agg1=['' for i in range(len(fin[1])-1)]
        #print("cook0",agg,agg1)
        agg1.extend(agg)
        #print("cook1",agg,agg1)
        agg=agg1
        #print("cook",agg,agg1)
#print('*',col)
    save=fin[1]
    #print("hii",save)
#print(fin[0])
#print(s1_c)
    if(len(c)!=0 and c[0].lower()=='where'):
      #  print("d1",c)
        fin=[wher(c[1:],fin[0],fin[1]),save]
       # print("done",fin)
       # print("d1",fin[0])
    if(len(fin[0])==0):
        print_ans(fin[0],col_func(col,agg))
        sys.exit()
    #print("sm",c,len(c))
    for i in range(len(c)):
        if(c[0]=='group' or c[0]=='order'):
            break
        c.pop(0)

    if(len(c)!=0 and c[0]=='group'):
        if(c[1]!='by'):
            print('group by is not found')
            sys.exit()
        c.pop(0)
        c.pop(0)
        temps=[]
        for i in range(len(c)):
            if(c[0]=='order'):
                break
            temps.extend(c[0].split(','))
            c.pop(0)
        temps=[x for x in temps if x]
    #print(agg)
    #print(col)
    #print(temps)
        for i in range(len(col)):
            if(agg[i]=='' and col[i] not in temps):
            #print(col[i])
                print('group command error , columns in left and right are not same')
                sys.exit()
        gr=len(col)
        temps.reverse()
        col.extend(temps)
        #print(agg)
        fin=etb(fin[0],fin[1],col)
        fin=group(fin,col,agg,gr)
        #print(fin)
        col=fin[1]
#print(c)
    if(flag_group==0):
        fin=[etb(fin[0],fin[1],col),col]
        fin,col=aggregates(fin[0],fin[1],col,agg,col)
    #print('aggregates--',fin)
    if(len(c)!=0 and c[0]=='order'):
        if(c[1]!='by'):
            print('order found but not by ')
            sys.exit()
        c.pop(0)
        c.pop(0)
        req=[]
        for i in range(len(c)):
            req.extend(c[0].split(','))
            c.pop(0)
        req=[x for x in req if x]
        fin=order(fin[0],fin[1],req)
    #print(fin[1])
    #print()
    #print()
    #print()
        if(len(c)!=0):
            print('something is mistaken only one column in order by allowed and string is not empty')
            sys.exit()
    #print(fin[0],fin[1],req,oder)
#print(fin)
    fin=[etb(fin[0],fin[1],col),col]
#fin=extract_table(fin[0],fin[1],col)
#print(fin[1],col)
#print(flag_distinct)
#print(fin)
    if(flag_distinct==1):
        temp=[]
        for x in fin[0]:
            if(x not in temp):
                temp.append(x)
        fin[0]=temp.copy()
#print_self(fin)
#print()
#print(fin,len(fin))
    print_ans(fin[0],col)
if __name__ == '__main__':
    main()