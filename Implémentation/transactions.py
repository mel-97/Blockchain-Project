import hashlib as hasher
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
        self.address.update(str(Bitcoin.nbObjects).encode())
        self.data=[0,[]]
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
        user.Wallet.append(self)
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
    
    def __init__(self, nom,prenom) : 
         self.nom=nom
         self.prenom=prenom
         self.Wallet=[]

         #for b in Bitcoin.BitcoinList:
             #if b.IsCurrentUser(self,b)==True :
                 #self.Wallet.append(b)
         self.Transactions=[]
         User.UsersList.append(self)
    def getSolde(self):
         solde=0
         for b in self.Wallet:
             solde=solde+b.value
         return solde
    def __str__(self):
        return "nom : "+str(self.nom)+"\nprenom : "+str(self.prenom)

import datetime as date

class Transaction():
    def __init__(self,sender,receiver,amount,timestamp):
        self.sender=sender
        self.receiver=receiver
        self.timestamp=timestamp
        self.amount=amount
        """self.adress=hasher.sha256()
        sh=str(self.sender)+str(self.receiver)+str(self.amount)+str(self.timestamp)
        self.address.update(str(sh).encode())"""
        if sender.getSolde()<amount:
            return "solde insuffisant"
        else:
            values=[0]
            bits=[]
            t=0
            while t==0:
                for bit in sender.Wallet:
                    if bit.value>=amount:
                        bit.ShatterBitcoin(amount,(bit.value-amount))
                        print (bit.value)
                        t=1
            if t==1:
                for bit in sender.Wallet:
                    if bit.value==amount:
                        bit.giveBitcoin(receiver)
                        sender.Wallet.remove(bit)
            else:
                while t==0:
                    for bit in sender.Wallet:
                        bits.append(bit)
                        values.append(bit.value)
                        if sum(values)==amount:
                            t=1
                        if sum(values)>amount:
                            b=bits(-1)
                            diff=sum(values)-amount
                            b.ShatterBitcoin(diff,(b.value-diff))
                            t=2
            values=[0]
            if t==2:
                for bit in sender.Wallet:
                    values.append(bit.value)
                    if values<=amount:
                        bit.giveBitcoun(receiver)
                    else:
                        values.remove(bit.value)
user1=User("Hafid","Faycal")
b1=Bitcoin(0.4)
b2=Bitcoin(3)
b3=Bitcoin(0.5)
b4=Bitcoin(5)
user2=User("Elsa","Dupraz")
b1.giveBitcoin(user1)
b4.giveBitcoin(user1)
b2.giveBitcoin(user2)
timestamp1 = date.datetime.now()
Transaction(user1,user2,4,timestamp1)
for user in User.UsersList:
    print(str(user)+"\n Solde ="+str(user.getSolde())) 
    for bitcoin in user.Wallet:
        print(str(bitcoin))
for bit in user1.Wallet:
    print (bit.value)
                
            
                            

    
    
    
        

    
