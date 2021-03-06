
import codification as codify
import FNC as ts
import DPLL as dp
import visualizadorProyecto as vs

#psewudomian

#hace referencia al corro uno donde comiuenza
x_st = [0,2]
y_st = [0,2]
#donde deberia terminar
x_ob = [2,0]
y_ob = [2,0]
#el tamano de donde lo vamos a hacer
Nfilas = 3
Ncols = 3
#numero de carros
Ncarros = 2
#cuantos tuernos maximos hay
#NMax = Nfilas - 1 + Ncols - 1
NMax = 5
#solo un carro en la visualizacion
letras = []
for k in range(Ncarros):
    for i in range(Ncols):
        for e in range(Nfilas):
            for j in range(NMax):
                v1 = codify.codifica4(k, i,e,j, Ncarros, Ncols , Nfilas, NMax)
                cod = chr(v1+256)
                print(cod, end=" ")
                letras.append(cod)
            print("")


def crear_regla0():
    #cada carro en un solo x, y en dado turno
    iniciaRegla = True
    for  t in range(NMax):
        for c in range(Ncarros):
            for x in range(Ncols):
                for y in range(Nfilas):
                    inicializaClausula = True
                    for i in range(Ncols):
                        for j in range(Nfilas):
                            if not(i == 0 and j == 0):
                                if inicializaClausula:
                                    claus = chr(256+codify.codifica4(c,(x+i)%Ncols,(y+j)%Nfilas,t, Ncarros, Ncols, Nfilas, NMax))
                                    inicializaClausula = False
#                                    print("se inicializo la clausula",claus)

                                else:
                                    #a->b = ba->
                                    claus+= chr(256+codify.codifica4(c,(x+i)%Ncols,(y+j)%Nfilas,t, Ncarros, Ncols, Nfilas, NMax))+ "O"
#                                    print("clausula else", claus)
                    #P(c,x,y,t)->¬
#                    f = codify.string2Tree(claus, letras)
#                    print("aca va la clausula")
#                    print(codify.Inorder(f))

                    if iniciaRegla:
                        regla = claus+"-"+chr(256+codify.codifica4(c,x,y,t, Ncarros, Ncols, Nfilas, NMax))+">"
                        iniciaRegla = False
                    else:
                        regla += claus+"-"+chr(256+codify.codifica4(c,x,y,t, Ncarros, Ncols, Nfilas, NMax))+">"+"Y"

    return regla

def crear_regla1():
    #cada carro en un solo x, y en dado turno
    iniciaRegla = True
    for c in range(Ncarros):
        for  t in range(NMax):
            inicializaClausula = True
            for x in range(Ncols):
                for y in range(Nfilas):
                    if inicializaClausula:
                        claus = chr(256+codify.codifica4(c,x,y,t, Ncarros, Ncols, Nfilas, NMax))
                        inicializaClausula = False
                        #print("se inicializo la clausula",claus)

                    else:
                        #a->b = ba->
                        claus+= chr(256+codify.codifica4(c,x,y,t, Ncarros, Ncols, Nfilas, NMax))+ "O"
                        #print("clausula else", claus)
                    #P(c,x,y,t)->¬
#                    f = codify.string2Tree(claus, letras)
#                    print("aca va la clausula")
#                    print(codify.Inorder(f))

            if iniciaRegla:
                regla = claus
                iniciaRegla = False
            else:
                regla += claus+"Y"

    return regla


def crear_regla2():
    #corresponde a la regla que hace referencia a que un carro que sale de x_0 lugar debe llegar  a y_1 lugar en t turnos
    cons = ""
    
    inicial_regla = True
    for c in range(Ncarros):
        inicial_imp = True
        Obj = codify.codifica4(c, x_ob[c], y_ob[c], NMax-1, Ncarros, Ncols, Nfilas, NMax)
        print("*******")
        for n in range(NMax):
            inicial_con = True
            for k in range(n + 1,NMax):
                if inicial_con:
                    cons = chr(codify.codifica4(c, x_ob[c], y_ob[c], k, Ncarros, Ncols, Nfilas, NMax) + 256)
                    inicial_con = False
                else:
                    cons += chr(codify.codifica4(c, x_ob[c], y_ob[c], k, Ncarros, Ncols, Nfilas, NMax) + 256) + "Y"
            if cons != "":
                if inicial_imp: 
                    imp = cons + chr(codify.codifica4(c, x_ob[c], y_ob[c], n, Ncarros, Ncols, Nfilas, NMax) + 256) + ">"
                    inicial_imp = False
                else:
                    imp += cons + chr(codify.codifica4(c, x_ob[c], y_ob[c], n, Ncarros, Ncols, Nfilas, NMax) + 256) + ">" + "Y"
        if inicial_regla:
            regla = imp
            inicial_regla = False
        else:
            regla += imp + "Y"
            
#cear todas las letras proposicinales
        if inicial_imp:
            regla = chr(Obj+256)
            inicial_imp = False
        else:
            regla += chr(Obj+256)+"Y"
    return regla



def crear_regla3():
    #esta regla establece que si hay un carro en cierta ubicacion en dado momento el otro no puede estar en esa misma ubicacion en el mismo momentoo
    regla = ""
    #si P(C1,x ,y, n) -> -(P(C2, x, y, n)
    #sin variar el carro
    inicicial_re = True
    inicial_re2 = True
    for t in range(NMax):
        inicicial_re = True
        for x in range(Ncols):
            for y in range(Nfilas):
                if(inicicial_re):
                    ##a->b = >ab =ba->
                    #P Y -(q O r)//YP-Oqr  // p->-q
                    #//>p-q // q-p>
                    claus =  chr(codify.codifica4(0,x,y, t, Ncarros, Ncols, Nfilas, NMax)+ 256)+ "-" +chr(codify.codifica4(1,x,y, t, Ncarros, Ncols, Nfilas, NMax)+ 256)+">"
                    claus += chr(codify.codifica4(1,x,y, t, Ncarros, Ncols, Nfilas, NMax)+ 256)+ "-" +chr(codify.codifica4(0,x,y, t, Ncarros, Ncols, Nfilas, NMax)+ 256)+">" + "Y"
                    inicicial_re = False
                else:
                    claus += chr(codify.codifica4(0,x,y, t, Ncarros, Ncols, Nfilas, NMax)+ 256)+ "-" +chr(codify.codifica4(1,x,y, t, Ncarros, Ncols, Nfilas, NMax)+ 256)+">" + "Y"
                    claus += chr(codify.codifica4(1,x,y, t, Ncarros, Ncols, Nfilas, NMax)+ 256)+ "-" +chr(codify.codifica4(0,x,y, t, Ncarros, Ncols, Nfilas, NMax)+ 256)+">" + "Y"
        if inicial_re2:
            regla = claus
            inicial_re2 = False
        else:
            regla += claus + "Y"
    return regla

def crear_regla4():
    inicial_re = True
    for c in range(Ncarros):
        if (inicial_re):
            claus = chr(codify.codifica4(c,x_st[c],y_st[c], 0, Ncarros, Ncols, Nfilas, NMax)+ 256)
            inicial_re = False
        else:
            claus += chr(codify.codifica4(c,x_st[c],y_st[c], 0, Ncarros, Ncols, Nfilas, NMax)+ 256)+ "Y"
    return claus

def crear_regla5():
    #esta regla establece que un carro solo se puede mover un paso por cada turno
    #P(c,x,y,t) > ( O )
    inicial_regla = True
    claus= ""
    for c in range(Ncarros):
        inicial = True
        for t in range(NMax-1):
            for x in range(Ncols):
                for y in range(Nfilas):
                    if inicial:
                        # P(c,x+1,y, t+1)+P(c,x,y+1, t+1)+O+P(c,x,y,t)+>                     
                            claus = chr(codify.codifica4(c,x+1,y,t+1, Ncarros, Ncols, Nfilas, NMax)+256)+chr(codify.codifica4(c,x,y+1,t+1, Ncarros, Ncols, Nfilas, NMax) +256)+"O"+chr(codify.codifica4(c,x,y,t,Ncarros, Ncols, Nfilas, NMax)+256)+">"
                            inicial = False
                    
                    else:
                        if (x>= 1 and y>=1 and x<Ncols-1 and y<Nfilas-1 ):
                            claus += chr(codify.codifica4(c,x,y-1,t+1, Ncarros, Ncols, Nfilas, NMax)+256) + chr(codify.codifica4(c,x-1,y,t+1, Ncarros, Ncols, Nfilas, NMax)+256) + "O" +chr(codify.codifica4(c,x+1,y,t+1, Ncarros, Ncols, Nfilas, NMax)+256)+chr(codify.codifica4(c,x,y+1,t+1, Ncarros, Ncols, Nfilas, NMax) +256) + chr(codify.codifica4(c,x,y,t+1, Ncarros, Ncols, Nfilas, NMax) +256) + "O" + "O"  + "O"+ chr(codify.codifica4(c,x,y,t,Ncarros, Ncols, Nfilas, NMax)+256) + ">" + "Y"
                        elif (x>=1 and y == 0 and x<Ncols-1):
                            claus += chr(codify.codifica4(c,x-1,y,t+1, Ncarros, Ncols, Nfilas, NMax)+256) + chr(codify.codifica4(c,x+1,y,t+1, Ncarros, Ncols, Nfilas, NMax)+256)+ "O" +chr(codify.codifica4(c,x,y+1,t+1, Ncarros, Ncols, Nfilas, NMax) +256)+ chr(codify.codifica4(c,x,y,t+1, Ncarros, Ncols, Nfilas, NMax) +256) + "O" +  "O" + chr(codify.codifica4(c,x,y,t,Ncarros, Ncols, Nfilas, NMax)+256)+">" + "Y"                      
                        elif (y>=1 and x == 0 and y<Nfilas-1):
                            claus += chr(codify.codifica4(c,x,y-1,t+1, Ncarros, Ncols, Nfilas, NMax)+256) + chr(codify.codifica4(c,x+1,y,t+1, Ncarros, Ncols, Nfilas, NMax)+256)+ "O" +chr(codify.codifica4(c,x,y+1,t+1, Ncarros, Ncols, Nfilas, NMax) +256)+ chr(codify.codifica4(c,x,y,t+1, Ncarros, Ncols, Nfilas, NMax) +256) + "O" + "O"  + chr(codify.codifica4(c,x,y,t,Ncarros, Ncols, Nfilas, NMax)+256)+">" + "Y"
                        elif (x == Ncols-1 and y>0 and y<Nfilas-1):
                            claus += chr(codify.codifica4(c,x-1,y,t+1, Ncarros, Ncols, Nfilas, NMax)+256)+chr(codify.codifica4(c,x,y+1,t+1, Ncarros, Ncols, Nfilas, NMax) +256)+ "O" + chr(codify.codifica4(c,x,y-1,t+1, Ncarros, Ncols, Nfilas, NMax)+256) + chr(codify.codifica4(c,x,y,t+1, Ncarros, Ncols, Nfilas, NMax) +256) + "O" + "O"+  chr(codify.codifica4(c,x,y,t,Ncarros, Ncols, Nfilas, NMax)+256)+">" + "Y"
                        elif (y == Nfilas-1 and x>0 and x<Ncols-1):
                            claus += chr(codify.codifica4(c,x,y-1,t+1, Ncarros, Ncols, Nfilas, NMax)+256)+chr(codify.codifica4(c,x+1,y,t+1, Ncarros, Ncols, Nfilas, NMax) +256)+ "O" + chr(codify.codifica4(c,x-1,y,t+1, Ncarros, Ncols, Nfilas, NMax)+256) + chr(codify.codifica4(c,x,y,t+1, Ncarros, Ncols, Nfilas, NMax) +256) + "O" + "O" + chr(codify.codifica4(c,x,y,t,Ncarros, Ncols, Nfilas, NMax)+256)+">" + "Y"
                        elif (x == Ncols-1 and y==0 ):
                            claus += chr(codify.codifica4(c,x-1,y,t+1, Ncarros, Ncols, Nfilas, NMax)+256)+chr(codify.codifica4(c,x,y+1,t+1, Ncarros, Ncols, Nfilas, NMax) +256)+ chr(codify.codifica4(c,x,y,t+1, Ncarros, Ncols, Nfilas, NMax) +256) + "O" + "O" + chr(codify.codifica4(c,x,y,t,Ncarros, Ncols, Nfilas, NMax)+256)+">" + "Y"                          
                        elif (y == Nfilas-1 and x==0 ):
                            claus += chr(codify.codifica4(c,x,y-1,t+1, Ncarros, Ncols, Nfilas, NMax)+256)+chr(codify.codifica4(c,x+1,y,t+1, Ncarros, Ncols, Nfilas, NMax) +256)+ chr(codify.codifica4(c,x,y,t+1, Ncarros, Ncols, Nfilas, NMax) +256) + "O" + "O" + chr(codify.codifica4(c,x,y,t,Ncarros, Ncols, Nfilas, NMax)+256)+">" + "Y"                            
                        elif (x == Ncols-1 and y == Nfilas-1):
                            claus+= chr(codify.codifica4(c,x-1,y,t+1, Ncarros, Ncols, Nfilas, NMax)+256)+chr(codify.codifica4(c,x,y-1,t+1, Ncarros, Ncols, Nfilas, NMax) +256) + chr(codify.codifica4(c,x,y,t+1, Ncarros, Ncols, Nfilas, NMax) +256) + "O" +  "O" +chr(codify.codifica4(c,x,y,t,Ncarros, Ncols, Nfilas, NMax)+256)+">"+"Y"
                            
                        else:            
                            print("x",x , " y ", y)
                            claus+= chr(codify.codifica4(c,x+1,y,t+1, Ncarros, Ncols, Nfilas, NMax)+256)+chr(codify.codifica4(c,x,y+1,t+1, Ncarros, Ncols, Nfilas, NMax) +256)+ chr(codify.codifica4(c,x,y,t+1, Ncarros, Ncols, Nfilas, NMax) +256) + "O" + "O"+chr(codify.codifica4(c,x,y,t,Ncarros, Ncols, Nfilas, NMax)+256)+">"+"Y"
        if inicial_regla:
            regla = claus
            inicial_regla = False
        else:
            regla += claus + "Y"
    
    return regla
regla0 = crear_regla0()
regla1 = crear_regla1()
regla2 = crear_regla2()
regla3 = crear_regla3()
regla4 = crear_regla4()
regla5 = crear_regla5()

#print("***regla 5 ",regla5)
#
#arbol = codify.Inorder(codify.string2Tree(regla5,letras))
#
#
#
#for c in arbol:
#    if c in letras:
#        lista = codify.decodifica4(ord(c)-256,Ncarros, Ncols, Nfilas, NMax) 
#        print(c, " El carro ", lista[0], "esta en (",lista[1],"," , lista[2],") en el turno ", lista[3] )
#        
##
#print(codify.Inorder(codify.string2Tree(regla0,letras)))


#print("******************************* ****")
#print("REGLA 0")
#print(stringRe)
#print("************************************")

#print("INORDER regla 0")


#print(codify.Inorder(codify.string2Tree(regla2,letras)))
#
#print("INORDER regla 1")
#
#
#print(codify.Inorder(codify.string2Tree(string1,letras)))
#
#regla3 + regla4 + regla2
#



#
#
#regla =  regla0 + regla4 + regla5 + regla3 +"Y" +"Y" +"Y"
regla = regla0 + regla1 + regla2  + regla3 + regla4 + regla5 + "Y" +"Y" +"Y" +"Y" +"Y"
###print("INORDER")
#print(codify.Inorder(codify.string2Tree(regla,letras)))
##
##

literales = ts.Tseitin(codify.Inorder(codify.string2Tree(regla,letras)),letras)

lista = []

for x in literales:
    if x not in ["Y","O","-"]:
        lista.append(ord(x)-256)

print("Length: ",len(lista), "Max of the list: " , max(lista))
#print("**Tseitin")
#print(literales)
#
lista_literales = ts.formaClausal(literales)
print("**Forma clausal")
#print(lista_literales)

#print(lista_literales[68])
final = dp.DPLL(lista_literales,{})
#print("solucion: ",final)

for literal in final[1]:
    if literal in letras:
        if final[1][literal] == 1:
            lista = codify.decodifica4(ord(literal)-256,Ncarros, Ncols, Nfilas, NMax)
            print(literal, " El carro ", lista[0], "esta en (",lista[1],"," , lista[2],") en el turno ", lista[3] )
    
            

vs.showIt(final[1])
