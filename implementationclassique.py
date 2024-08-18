#Jobs de la forme [[m_ij, p_j]]
#Taches de la forme [J(i), m(i), p(i), number(i)]
# sequences de la forme o_i_1, o_i_2, ...

import random

#%% code utile


#par la suite, n est toujours le nombre de tache du problème qui nous intéresse, m le nombre de machine,
#J la liste des jobs, O la listes des taches, pmax le temps max d'exécution d'une tache.

#entrée: nombre jobs, nombre machine, temps max d'une tache. Sortie: problème aléatoire des dimensions précisée
def randomJobs(n, m, pmax):     #tout est dans le nom, pour pouvoir faire des tests
    J=[ [] for i in range(n)]
    numeros=[j for j in range(m)]
    for i in range(n):
        random.shuffle(numeros)
        for j in numeros:
            J[i].append([j, random.randint(1, pmax)])
    return J


#entrée: nombre jobs, nombre machine, longueur de la séquence voulue. Sortie: une séquence aléatoire
def randomSequence(n, m, longueur):
    T=[i for i in range(n*m)]
    random.shuffle(T)
    return T[:longueur]

#entrée: nombre jobs, nombre machine, longueur de la séquence voulue, liste des taches du problème.. Sortie: séquence 
def randomViableSequence(n, m, longueur, O):
    T=randomSequence(n, m, longueur)
    while not viable(T, O, n, m):
        T=randomSequence(n, m, longueur)
    return T

#entrée : liste de jobs.
#sortie: liste de taches correpsondant au même problème, avec J[i][j] correspondant à O[i+j*n]
def jobVersTaches(J):
    O=[]
    for j in range(len(J[1])):
        for i in range(len(J)):
            O.append([i, J[i][j][0], J[i][j][1], j])
    return O

#entrée : liste de taches.
#sortie: liste de jobs correpsondant au même problème
def tachesVersJobs(O, n, m):
    J=[ [ [] for i in range(m)] for j in range(n)]
    for t in O:
        J[t[0]][t[3]]=[t[1], t[2]]
    return J


#entrée: une séquence, un entier désignant une tache, une liste de taches
#sortie: est ce que la tache peut être rajoutée en queue de la séquence et garder une séquence viable
def CanFollow(sequence, o, O):
    T=[False for i in range(O[o][3])]
    j=O[o][0]
    for i in sequence:
        if i==o:
            return False
        if O[i][0]==j:
            T[O[i][3]]=True
    for b in T:
        if not b:
            return False
    return True

#entrée: une séquence, une liste de taches, un nombre de machine
#sortie: le nombre d'apparition de chaque job dans la séquence
def numberOfApparence(sequence, O, n):
    apparitions=[0]*n
    for o in sequence:
        apparitions[O[o][0]]+=1
    return apparitions
        

#entrée: séquence, liste de tache
#sortie: les taches qui peuvent être rajoutée en queue
def epsilon(sequence, O):   #epsilon(sequence, O) est l'ensemble des taches pouvant être la prochaine dans la séquence
    Res=[]                  #ceci est une façon extrêmement inefficace de le programmer, mais facilement lisible.
    for o in range(len(O)):
        if CanFollow(sequence, o, O):
            Res.append(o)
    return Res

#entrée: séquence, nombre jobs, liste de tache
#sortie: même qu'au dessus
def epsilon2(sequence, n, O):     #version légèrement peu plus efficace de epsilon (ne parcourt la séquence qu'une fois)
    apparition=numberOfApparence(sequence, O, n)
    res=[]
    for o in range(len(O)):
        if apparition[O[o][0]]==O[o][3]:
            res.append(o)
    return res


#entrée: séquence, liste de jobs, liste de taches, nombre de jobs, nombre de machines
def epsilon3(sequence, J, O, n, m): #version encore plus efficace, mais qui ne fonctionne qu'en étant sûr du nombre de tache par job et de la manière de convertir la liste de jobs en liste de tache
    apparition=numberOfApparence(sequence, O, n)
    T=[]
    for i in range(n):
        if apparition[i]<m:
            T.append(apparition[i]*n+i)
    return T

#entrée: une séquence, une liste de tache, nombre de jobs, nombre de machine
#sortie: est que la séquence est viable/réalisable
def viable(sequence, O, n, m):  #regarde si une séquence est réalisable
    J=[0 for i in range(n)]
    for t in sequence:
        if J[O[t][0]]!=O[t][3]:
            return False
        J[O[t][0]]+=1
    return True

#entrée: une séquence, une liste de tache, un nombre de jobs, un nombre de machine
#sortie: est que la séquence est ordonnée
def ordonne(sequence, O, n, m): #vérifie si une séquence est ordonnée
    viable(sequence, O, n, m)
    Cmax=0
    TJobs=[0 for i in range(n)]
    TMachines=[0 for i in range(m)]
    nummach=-1
    for o in sequence:
        m=O[o][1]
        p=O[o][2]
        j=O[o][0]
        tempsfin=max(TMachines[m], TJobs[j])+p
        if tempsfin < Cmax:
            return False
        elif (tempsfin==Cmax):
            if nummach>m:
                return False
        TMachines[m]=tempsfin
        TJobs[j]=tempsfin
        nummach=m
        Cmax=tempsfin
    return True

"""
def seqversensemble(sequence, n, m):
    T=[False]*(n*m)
    for o in sequence:
        T[o]=True
    return tuple(T)                  #T représente de manière unique et hashable l'ensemble des éléments d'une séquence
"""
#entrée: une séquence, la liste des taches, le nombre de jobs de l'instance
#sortie:  une représentation unique de l'ensemble des taches présente dans la séquence (utilisée pour pouvoir être hashée pour un dictionnaire)
def seqversensemble(sequence, O, n): #ne fonction que sur les séquences viables   
    T=numberOfApparence(sequence, O, n)
    return tuple(T)

#entrée: une séquence viable, la liste des taches, le nombre de jobs, le nombre de machines
#sortie: liste des temps de fins de chaque tache, machine et le temps de completion
def tempsfin(sequence, O, n, m):        #en supposant fournie une séquence viable, donne les temps de fin selon la solution semi-active correspondante
    Tfinjobs=[0]*n
    Tfinmachines=[0]*m
    Tcompletion=0
    for o in sequence:
        jo=O[o][0]
        mo=O[o][1]
        tfino=max(Tfinjobs[jo], Tfinmachines[mo])+O[o][2]
        Tfinjobs[jo]=tfino
        Tfinmachines[mo]=tfino
        Tcompletion=max(Tcompletion, tfino)
    return (Tfinjobs, Tfinmachines, Tcompletion)
        
#entrée: séquence, liste jobs, liste tache, nombre jobs, nombre machine
#sortie: liste des numéros des taches qui peuvent être accolé à la séquence et conserver une séquence ordonnée
def eta(sequence,J, O, n, m):
    if not ordonne(sequence, O, n, m):
        return []
    et=[]
    TJobs, TMachines, Tc= tempsfin(sequence, O, n, m)
    """    TJobs=[0 for i in range(n)]
    TMachines=[0 for i in range(m)]
    numjob=-1
    for o in sequence:
        m=O[o][1]
        p=O[o][2]
        j=O[o][0]
        tempsfin=max(TMachines[m], TJobs[j])+p
        if tempsfin < Cmax:
            return []
        elif (tempsfin==Cmax):
            if numjob>j:
                return []
        TMachines[m]=tempsfin
        TJobs[j]=tempsfin
        numjob=j
        Cmax=tempsfin
    et=[]
    for o in epsilon(sequence, O):
        if ( (max(TMachines[O[o][1]], TJobs[O[o][0]])+O[o][3]) > Cmax):
            et.append(o)
        elif (max(TMachines[O[o][1]], TJobs[O[o][0]])+O[o][3] == Cmax) and O[o][0]>numjob:
            et.append(o)
    """
    for o in epsilon3(sequence, J,O,n,m):
        if ( (max(TMachines[O[o][1]], TJobs[O[o][0]])+O[o][2]) > Tc):
            et.append(o)
        elif (max(TMachines[O[o][1]], TJobs[O[o][0]])+O[o][2] == Tc) and O[o][1]>O[sequence[-1]][1]:
            et.append(o)
    return et



#entrée: séquence ordonnée, un entier correspondant au numéro d'une tache,listejobs, liste des taches, nombre de jobs, nombre de machines
#sortie: le temps minimal auquel le job peut se terminer dans un schedule tiré d'une séquence ordonnée obtenue en complétant celle d'entrée
def tempsMinOrdonne(sequence, o, O, n, m):
    TJobs, Tmachines, Tc = tempsfin(sequence, O, n, m)
    tempsMinFin=max(Tmachines[O[o][1]], TJobs[O[o][0]])+O[o][3]
    if ( (max(Tmachines[O[o][1]], TJobs[O[o][0]])+O[o][3]) > Tc):
        return tempsMinFin
    elif (max(Tmachines[O[o][1]], TJobs[O[o][0]])+O[o][3] == Tc) and O[o][0] > O[sequence[-1]][0]:
        return tempsMinFin
    else:
        return Tc + O[o][2]

#entrée: séquence, liste jobs, liste tache, nombre jobs, nombre machine
#sortie: liste des temps de la forme précédente
def tempsMinOrdonneListe(sequence,J, O, n, m):
    TJobs, Tmachines, Tc=tempsfin(sequence, O, n, m)
    et=eta(sequence, J,O, n, m)
    Tmins={}
    for o in epsilon(sequence,O):
        tempsMinFin=max(Tmachines[O[o][1]], TJobs[O[o][0]])+O[o][3]
        if o in et:
            Tmins[o]=tempsMinFin
        else:
            Tmins[o] = Tc + O[o][2]
    return Tmins

#entrée: une liste de jobs, le nombre de jobs, le nombre de machine
#sortie: un dictionnaire qui si le programme fonctionne contient une seule clée: un tuple de n fois le nombre de machine, et l'élément associé à cette clef est une séquence optimale
def Gromicho(J):
    n=len(J)
    m=len(J[0])
    O=jobVersTaches(J)
    sequencesNonDomines={}
    sequencesNonDominesPrec={}
    for o in epsilon([], O):
        sequencesNonDomines[seqversensemble([o], O, n)]=[[o]]
    for i in range(2, (n * m) +1):
#        print(i)
        sequencesNonDominesPrec=sequencesNonDomines.copy()
        sequencesNonDomines={}
        for ensemble in sequencesNonDominesPrec.keys():
            for sequence in sequencesNonDominesPrec[ensemble]:
                for o in eta(sequence, J, O, n, m):
                    ensemblesuivant=seqversensemble(sequence+[o], O, n)
                    if ensemblesuivant not in sequencesNonDomines.keys():
                        sequencesNonDomines[ensemblesuivant]=[]
                    Tmins=tempsMinOrdonneListe(sequence+[o], J,O, n, m)
                    nondomine=True
                    taillens=len(sequencesNonDomines[ensemblesuivant])
                    j=0
                    while j<taillens and nondomine:
                        Tmincomparaison=tempsMinOrdonneListe(sequencesNonDomines[ensemblesuivant][j], J, O, n, m)
                        dominationOriginalSurNouveau=True
                        dominationNouveauSurOriginal=True
                        for compare in Tmins.keys():
                            if compare not in Tmincomparaison.keys():
                                print(" \n \n")
                                print(ensemblesuivant)
                                print(sequencesNonDomines[ensemblesuivant])
                                print(sequencesNonDomines[ensemblesuivant][j], sequence+[o],compare, Tmins)
                                print("erreur")
                                return 0
                            if Tmins[compare]<Tmincomparaison[compare]:
                                dominationOriginalSurNouveau=False
                            elif Tmincomparaison[compare]<Tmins[compare]:
                                dominationNouveauSurOriginal=False
                        if i==(n*m):    #dans le cas où l'ensemble représente toute la liste, il n'y a pas de nouveaux éléments à comparer
                            inutile1, inutile2, tcn=tempsfin(sequence+[o], O, n, m)
                            inutile1, inutile2, tco=tempsfin(sequencesNonDomines[ensemblesuivant][j], O, n, m)
                            if tcn<tco:
                                dominationOriginalSurNouveau=False
                        if dominationOriginalSurNouveau==True:
                            nondomine=False
                        elif dominationNouveauSurOriginal:
                            sequencesNonDomines[ensemblesuivant]=sequencesNonDomines[ensemblesuivant][:j]+sequencesNonDomines[ensemblesuivant][j+1:]
                            taillens-=1
                        else:
                            j+=1
                    if nondomine:
                        sequencesNonDomines[ensemblesuivant].append(sequence+[o])
    return sequencesNonDomines


#entrée: une séquence, un nombre de machine
#sortie: un vecteur de bierwith correspondant au même schedule
def seqversbierwith(sequence, n):
    bierwith=[]
    for o in sequence:
        bierwith.append(o % n)
    return bierwith
#inverse de la fonction précédente.
def bierwithversseq(bierwith, n):
    sequence=[]
    apparition=[0*n]
    for j in bierwith:
        sequence.append(j+apparition[j]*n)
        apparition[j]+=1
    return sequence

#%% fonctions de tests
def bruteForce(listeTaches, n,m):
    liste1=[]
    liste2=[[]]
    for i in range(len(listeTaches)):
        liste1=liste2.copy()
        liste2=[]
        for j in range(len(liste1)):
            for o in range(len(listeTaches)):
                if CanFollow(liste1[j], o, listeTaches):
                    liste2.append(liste1[j]+[o])
    a, b, tc=tempsfin(liste2[0], listeTaches, n, m)
    s=liste2[0]
    for i in range(len(liste2)): 
        a, b, ttemp=tempsfin(liste2[i], listeTaches, n, m)
        if ttemp<tc:
            tc=ttemp
            s=liste2[i]
    return (tc, s)

#entrée: une sequence, une liste de taches, nb jobs, nbmachines
#sortie:une sous instance du problème avec exactmeent les taches présentes dudans la séquence
#utilité: chercher l'emplacement précis d'une erreur (inutile pour l'utilisateur, vu que tous les bugs ont déjà été corrigé si mes tests ont été assez exaustifs)
def seqToTaches(sequence, O, n, m):
    taches=[]
    for o in sequence:
        taches.append(O[o])
    return taches

#entrée: séquence, un numéro de tache, liste des taches, nombre de jobs, nombre de machines
def tempsFinTache(sequence, t, O,n,m):
    Tfinjobs=[0]*n
    Tfinmachines=[0]*m
    for o in sequence:
        jo=O[o][0]
        mo=O[o][1]
        tfino=max(Tfinjobs[jo], Tfinmachines[mo])+O[o][2]
        if t==o:
            return tfino
        Tfinjobs[jo]=tfino
        Tfinmachines[mo]=tfino
    return -1


#entrée: une séquence, la liste des taches, nombre jobs, nombre machines
#sortie: une séquence ordonnée décrivant la même  solution semi-active que celle en entrée (sert pour vérifier le point auquel la solution trouvé par le brutforce a été perdu, et en inférer où se trouve l'erreur dans mon code)
def rendordonne(sequence, O, n, m):
    i=0
    for j in range(len(sequence)):
        while i<len(sequence)-1:
            if (tempsFinTache(sequence, sequence[i], O, n, m) > tempsFinTache(sequence, sequence[i+1], O,n, m)) or ( tempsFinTache(sequence, sequence[i], O, n, m)==tempsFinTache(sequence,sequence[i+1], O,n, m) and O[sequence[i]][1]>O[sequence[i+1]][1] )  :
                sequence[i], sequence[i+1]=sequence[i+1], sequence[i]
            else:
                i+=1
    return sequence

#entrée: un ensemble de tache (ou instance)
#sortie: toutes les séquences obtenues par étape(utile pour débuguer, donc inutile pour quiconque d'autre que moi) 
def testGromicho(J, n, m):
    O=jobVersTaches(J)
    sequencesNonDomines={}
    sequencesNonDominesPrec={}
    enregistrement=[{} for i in range(n*m)]
    for o in epsilon([], O):
        sequencesNonDomines[seqversensemble([o], O, n)]=[[o]]
    for i in range(2, (n * m) +1):
        print(i)
        enregistrement[i-2]=sequencesNonDomines.copy()
        sequencesNonDominesPrec=sequencesNonDomines.copy()
        sequencesNonDomines={}
        for ensemble in sequencesNonDominesPrec.keys():
            for sequence in sequencesNonDominesPrec[ensemble]:
                a, b, temp=tempsfin(sequence, O, n, m)
                for o in eta(sequence, J, O, n, m):
                    ensemblesuivant=seqversensemble(sequence+[o], O, n)
                    if ensemblesuivant not in sequencesNonDomines.keys():
                        sequencesNonDomines[ensemblesuivant]=[]
                    Tmins=tempsMinOrdonneListe(sequence+[o], J,O, n, m)
                    nondomine=True
                    taillens=len(sequencesNonDomines[ensemblesuivant])
                    j=0
                    while j<taillens and nondomine:
                        Tmincomparaison=tempsMinOrdonneListe(sequencesNonDomines[ensemblesuivant][j], J, O, n, m)
                        dominationOriginalSurNouveau=True
                        dominationNouveauSurOriginal=True
                        for compare in Tmins.keys():
                            if compare not in Tmincomparaison.keys():
                                print(" \n \n")
                                print(ensemblesuivant)
                                print(sequencesNonDomines[ensemblesuivant])
                                print(sequencesNonDomines[ensemblesuivant][j], sequence+[o],compare, Tmins)
                                print("erreur")
                                return 0
                            if Tmins[compare]<Tmincomparaison[compare]:
                                dominationOriginalSurNouveau=False
                            elif Tmincomparaison[compare]<Tmins[compare]:
                                dominationNouveauSurOriginal=False
                        if i==(n*m):    #dans le cas où l'ensemble représente toute la liste, il n'y a pas de nouveaux éléments à comparer
                            inutile1, inutile2, tcn=tempsfin(sequence+[o], O, n, m)
                            inutile1, inutile2, tco=tempsfin(sequencesNonDomines[ensemblesuivant][j], O, n, m)
                            if tcn<tco:
                                dominationOriginalSurNouveau=False
                        if dominationOriginalSurNouveau==True:
                            nondomine=False
                        elif dominationNouveauSurOriginal:
                            sequencesNonDomines[ensemblesuivant]=sequencesNonDomines[ensemblesuivant][:j]+sequencesNonDomines[ensemblesuivant][j+1:]
                            taillens-=1
                        else:
                            j+=1
                    if nondomine:
                        sequencesNonDomines[ensemblesuivant].append(sequence+[o])
    enregistrement[-1]=sequencesNonDomines
    return enregistrement

#entrée: nombre de test, taille des instances
#sortie: liste de tous ceux sur lequel l'algorithme a échoué (si l'algo fonctionne, renvoie donc une liste vide)
def serietest(nb, n, m, pmax):
    echecs=[]
    for i in range(nb):
        print(i)
        J=randomJobs(n, m, pmax)
        O=jobVersTaches(J)
        resGromicho=Gromicho(J)
        i=0
        for key in resGromicho.keys():
            i+=len(resGromicho[key])
            sequence=resGromicho[key][0]
        if (i!=1):
            echecs.append(J)
        else:
            t2, s2=bruteForce(O, n, m)
            inutile1, inutile2, t=tempsfin(sequence, O, n, m)
            if t2!=t:
                echecs.append(J)
    return echecs
        
            

# %% tests
nb, n, m, pmax=100, 3, 3, 4
E=serietest(nb, n, m, pmax)
print("nombre d'erreur sur ", 100, "instances de ", m, "machines,", n,"jobs, avec pmax de ", pmax," :", len(E) )

"""
n=6
m=6
pmax=3
#J=randomJobs(n, m, pmax)
J=[[[2 , 1],  [0 , 3] , [1,  6] , [3 , 7] , [5 , 3] , [4 , 6]], [[1 , 8] , [2 , 5] , [4, 10] , [5, 10] , [0 ,10] , [3 , 4]],[[2 , 5] , [3 , 4] , [5 , 8] , [0,  9] , [1 , 1] , [4 , 7]],[[1 , 5] , [0 , 5] , [2 , 5] , [3 , 3] , [4 , 8] , [5 , 9]], [[2 , 9] , [1 , 3] , [4 , 5] , [5 , 4] , [0 , 3] , [3 , 1]],[[1 , 3] , [3 , 3] , [5 , 9] , [0 ,10] , [4 , 4] , [2 , 1]] ]
O=jobVersTaches(J)
res=Gromicho(J)
i=0
for key in res.keys():
    i+=len(res[key])
    sequence=res[key][0]
    
print("\n\n")
#inutil, brut, gro=testGromicho(J, n, m)

a,b,tc=tempsfin(sequence, O, n, m)
print(sequence, tc)
#t2, s2=bruteForce(O, n, m)
#print(s2, t2)
"""