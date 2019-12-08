# -*- coding: utf-8 -*-
import sys
sys.path.append(r".\Implémentation")
""" LA LIGNE AU DESSUS EST A MODIFIER SELON L'EMPLACEMENT SUR LE PC """
from Bitcoin_user import *
import datetime as date
"""
Created on Wed Mar 21 02:29:07 2018

@author: Faycel

from tkinter import *


fenetre = Tk()
label = Label(fenetre, text="Please press Start to begin.")
label.pack(side=BOTTOM)
bouton=Button(fenetre, text="Start",fg="green", bg="white")
bouton.pack(side=TOP)
canvas = Canvas(fenetre, width=150, height=200, bg="ivory")
canvas.pack(side=LEFT)
value = StringVar() 
value.set("Nom d'utilisateur")
entree = Entry(fenetre, textvariable=value, width=30)
entree.pack(side=TOP)
liste = Listbox(fenetre)
liste.insert(1, "Effectuer une transaction")
liste.insert(2, "Consulter mon solde")
liste.insert(3, "Historique de mes transactions")
liste.insert(4, "Précédent")
liste.insert(5, "Quitter")
liste.pack()

fenetre.mainloop()
"""

def consulterSolde(ID) :
    user=User.getUserFromID(ID)
    print(str(user))
    print("Solde : " + str(user.getSolde()))
    input("Appuez sur entrée pour revenir au menu principal")
    menu(ID)
    return

def Deconnexion(ID):
    print("Vous êtes déconnecté.")
    start()
    return

def historique(ID):
    print("Historique :")
    return

def transaction(ID):
    nom=input("Vous allez effectuer une transaction :\nNom de la personne à qui vous voulez envoyer de l'argent: ")
    prenom=input("Prénom de la personne : ")
    sender=User.getUserFromID(ID)
    receiver=User.getUserFromName(nom, prenom)
    print("Avant transaction :")
    for element in sender.Wallet :
        print("Bitcoin : "+str(element))
    if receiver == None :
        print("Données incorrectes. Veuillez réessayer ultérieurement.")
    else :
        print("Votre solde est de "+str(sender.getSolde()))
        amount=float(input("Somme à verser = "))
        tr=Transaction(sender, receiver, amount, date.datetime.now())
        print("Solde à vous : "+str(sender.getSolde()))
        print("Solde du recepteur : "+str(receiver.getSolde()))
        print("Après transaction :")
        for element in sender.Wallet :
            print("Bitcoin : "+str(element))
        input("Appuez sur entrée pour revenir au menu principal")
        menu(ID)
    return

def start() :
    ID_Database=["Marouane","Maroua","Mehdi","Faycal","Elsa"]
    ID=input("Bienvenue dans l'application.\nDonnez votre ID : ")
    compteur=1
    while ( ID not in ID_Database ) and ( compteur != 3 ) :
        ID=input("Nom d'utilisateur incorrect.\n Redonnez votre ID :")
        if ID not in ID_Database :
            compteur=compteur+1
    if compteur==3 :
        print("Erreur, veuillez relancer l'application.")
    else:    
        mdp={"Marouane":"1","Maroua":"2","Faycal":"3","Mehdi":"4"}
        i=0 
        modp=input("donnez votre MDP : ")
        while (mdp.get(ID)!=modp) and (i!=2):
            modp=input("Mot de passe incorrect. Reessayez : ")
            if (mdp.get(ID)!=modp) :
                i+=1
        if i==3 :
            print("Erreur, veuillez relancer l'application.")
        else :
            menu(ID)

def menu(ID) :
    print("Vous êtes connectés. Bienvenue :)")
    options={1: consulterSolde, 2 : Deconnexion, 3 : historique, 4 : transaction}
    num=int(input("Entrez le numéro de votre opération :\n1- Consulter votre solde\n2- Deconnexion\n3-Consulter l'historique de vos transactions\n4-Effectuer une transaction\n"))
    options[num](ID)
    

start()

        
        
    