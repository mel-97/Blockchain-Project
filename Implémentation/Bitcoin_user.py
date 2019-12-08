# -*- coding: utf-8 -*-
"""
Created on Tue Mar 27 15:46:32 2018

@author: Faycel
"""
from ecdsa import SigningKey
from ecdsa import VerifyingKey
import ecdsa
import hashlib as hasher
import random
import datetime as date
#import User as User
class Bitcoin() :
    addressesList=[]
    BitcoinList=[]
    nbObjects=0
    maxValue=20
    currentValue=0
    def __init__(self, value) :        
        self.value=value
        self.address = hasher.sha256()        
        self.address.update((str(Bitcoin.nbObjects)+str(self.value)).encode())
        self.data=[0,[]]
        self.signature=""
        if self.value + Bitcoin.currentValue <= Bitcoin.maxValue :
            Bitcoin.addressesList.append(self.address)
            Bitcoin.BitcoinList.append(self)
            Bitcoin.nbObjects+=1
            Bitcoin.currentValue+=self.value
        else :
            pass
        
        
    def __str__(self):
        return "Value : "+str(self.value)+"\nAddress : "+str(self.address)
    def getCurrentUser(self):
        return self.data[1][-1]
    def addUser(self,user):
        self.data[1].append(user)
    def IsCurrentUser(self,user):
        return self.getCurrentUser()==user
    def giveBitcoin(self,user):
        self.data[1].append(user)
        #user.Wallet.append(self)
        Bitcoin.putInRightPlace(self,user.Wallet)
    
    def trace(self):
        if len(self.data[1]) > 1 :
            return self.data[1][::-1]
        return self.data[1]
    
    def previousOwners(self) :
        display="Owners from most recent to least recent :\n\n"
        liste=self.trace()
        for element in liste :
            display+=str(element)+"\n"
        return display
    
    def pending(self, sender, receiver, Transaction):
        self.data[0]=1 # == en cours de transaction
        self.removeBitcoin(sender)
        if sender == receiver :
            pass
            """
            sender.pendingBitcoins.append(["Idle", self, Transaction])
            self.signature=sender.sign(self)
            """
        else :
            sender.pendingBitcoins.append(["Out", self, Transaction])
            receiver.pendingBitcoins.append(["In",self, Transaction])
            self.signature=sender.sign(self)
        
        
    def putInRightPlace(bitcoin, wallet):
        wallet.append(bitcoin)
        for i in range(len(wallet)) :
            for j in range(len(wallet)-1) :
                if wallet[j].value > wallet[j+1].value :
                    tmp=wallet[j]
                    wallet[j]=wallet[j+1]
                    wallet[j+1]=tmp
                    
    def removeBitcoin(self, user):
        if self.IsCurrentUser(user) :
            user.Wallet.remove(self)
        
    def ShatterBitcoin(self,serf1,serf2):
        b1=Bitcoin(serf1)
        b2=Bitcoin(serf2)
        b1.data[1]=self.data[1]
        b2.data[1]=self.data[1]
        Bitcoin.addressesList.remove(self.address)
        self.nbObjects+=1
        self.BitcoinList.append(b1)
        self.BitcoinList.append(b2)
        user=self.getCurrentUser()
        user.Wallet.remove(self)
        user.Wallet.append(b1)
        user.Wallet.append(b2)
        
        return (b1,b2)
    
    
class User():
    UsersList=[]
    
    def __init__(self, nom,prenom, ID) : 
         self.nom=nom
         self.prenom=prenom
         self.ID=ID
         self.Wallet=[]
         self.sk=SigningKey.generate(curve=ecdsa.SECP256k1)
         #for b in Bitcoin.BitcoinList:
             #if b.IsCurrentUser(self,b)==True :
                 #self.Wallet.append(b)
         self.Transactions=[]
         self.pendingBitcoins=[] #contains [state, bitcoin in transaction, transaction]
         #self.publicKey=hash(random.getrandbits(1024))
         User.UsersList.append(self)
    
    def sign(self, bitcoin):
        sk = SigningKey.generate(curve=ecdsa.SECP256k1)
        signature=sk.sign(str(bitcoin).encode())
        return (signature, sk.get_verifying_key())
     
    def getSolde(self):
         solde=0
         for b in self.Wallet:
             solde=solde+b.value
         """    
         for bitcoin in self.pendingBitcoins :
             if bitcoin[0] == "Idle" :
                 solde+=bitcoin[1].value
         """
         return solde
    
    def getUserFromName(nom, prenom):
        for user in User.UsersList :
            if (user.nom , user.prenom) == (nom, prenom) :
                return user
        return None
    
    def getUserFromID(ID):
        for user in User.UsersList :
            if user.ID == ID :
                return user
        return None
        
    def __str__(self):
        return "Nom : "+str(self.nom)+"\nPrenom : "+str(self.prenom)
    
    def verify (self, bitcoin, signature):
        allGood=True
        currentMessage=str(bitcoin).encode()
        vk = signature[1]
        print("==> "+str(signature[1]) )
        allGood=vk.verify(signature[0], currentMessage)
        return allGood
    
user1=User("Hafid","Faycal","Faycal")
user2=User("Maachou","Marouane","Marouane")
user3=User("Dahoumane","Mehdi","Mehdi")
user4=User("Houicha","Maroua","Maroua")
user5=User("Dupraz","Elsa","Elsa")
b1=Bitcoin(0.4)
b2=Bitcoin(3)
b3=Bitcoin(0.5)
b4=Bitcoin(5)
Bitcoin(1).giveBitcoin(user5)
Bitcoin(2).giveBitcoin(user4)
b1.giveBitcoin(user1)
b2.giveBitcoin(user1)
b3.giveBitcoin(user1)
b4.giveBitcoin(user3)
"""
for user in User.UsersList:
    print("\n\n"+str(user)+"\n Solde ="+str(user.getSolde())) 
    for bitcoin in user.Wallet:
        print(str(bitcoin))
"""
class Transaction():
    TransactionsList=[]
    def __init__(self,sender,receiver,amount,timestamp):
        self.sender=sender
        self.receiver=receiver
        self.timestamp=timestamp
        self.amount=amount
        self.inputs=[] #bitcoins that remain in the sender's wallet
        self.outputs=[] #bitcoins that go to the receiver's wallet
        self.block=[]
        """self.adress=hasher.sha256()
        sh=str(self.sender)+str(self.receiver)+str(self.amount)+str(self.timestamp)
        self.address.update(str(sh).encode())"""
        if sender.getSolde()<amount:
            print("solde insuffisant")
        else :
            Transaction.TransactionsList.append(self)
            t=0
            out=0
            liste=self.sender.Wallet
            while not out :
                if liste[t].value < amount :
                    t=t+1
                else :
                    out=1
                    (b1,b2)=liste[t].ShatterBitcoin(amount,liste[t].value-amount)
            if b1.value == amount :
                b1.pending(sender, receiver, self)
                #Bitcoin.putInRightPlace(b2,sender.Wallet)
                self.inputs.append(b2)
                self.outputs.append(b1)
                #print("b1 is : "+str(b1.signature))
                print("Verification of the signature : \n"+str(receiver.verify(b1,b1.signature)))
                
            else :
                b2.pending(sender, receiver, self)
                #Bitcoin.putInRightPlace(b1,sender.Wallet)
                self.inputs.append(b1)
                self.outputs.append(b2)
                print("Verification of the signature : \n"+str(receiver.verify(b1,b1.signature)))
            print("Transaction effectuée avec succès, attente de validation par la BlockChain :\n"+str(self))
            self.sender.Transactions.append(self)
            self.receiver.Transactions.append(self)
        
    def __str__(self):
        return "\tFrom : \n"+str(self.sender)+"\n\tTo : \n"+str(self.receiver)+"\n\tAmount sent : "+str(self.amount)
"""
tr=Transaction(User.getUserFromName("Hafid", "Faycal"),User.getUserFromName("Maachou", "Marouane"),1,date.datetime.now()) 
b0=Bitcoin(500)
b0.giveBitcoin(user4)
tr2=Transaction(User.getUserFromName("Hafid", "Faycal"),User.getUserFromName("Maachou", "Marouane"),0.2,date.datetime.now())
tr3=Transaction(User.getUserFromName("Dahoumane", "Mehdi"),User.getUserFromName("Dupraz", "Elsa"),3,date.datetime.now())
"""
"""
for user in User.UsersList:
    print("\n\n"+str(user)+"\n Solde ="+str(user.getSolde())) 
    for bitcoin in user.Wallet:
        print(str(bitcoin))
    for bitcoin in user.pendingBitcoins :
        print("State : "+bitcoin[0]+"\nBitcoin : "+str(bitcoin[1])+"\nSignature : "+str(bitcoin[1].signature))
marouane=User.getUserFromName("Maachou","Marouane")
"""
"""    
user1=User("Hafid","Faycal")
b1=Bitcoin(0.4)
b2=Bitcoin(3)
b3=Bitcoin(0.5)
b4=Bitcoin(5)
user2=User("test","tet")
b1.giveBitcoin(user1)
b4.giveBitcoin(user1)
b2.giveBitcoin(user2)
b3.giveBitcoin(user2)
for user in User.UsersList:
    print(str(user)+"\n Solde ="+str(user.getSolde())) 
    for bitcoin in user.Wallet:
        print(str(bitcoin))
print("\nAprès la monétisation\n")
b4.ShatterBitcoin(2.5,2.5)
for user in User.UsersList:
    print(str(user)+"\n Solde ="+str(user.getSolde())) 
    for bitcoin in user.Wallet:
        print(str(bitcoin))
"""
        
            