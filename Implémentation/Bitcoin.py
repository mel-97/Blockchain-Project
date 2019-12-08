# -*- coding: utf-8 -*-
"""
Created on Tue Mar 27 15:46:32 2018

@author: Faycel
"""
import hashlib as hasher

class Bitcoin() :
    addressesList=[]
    nbObjects=0
    maxValue=20
    currentValue=0
    def __init__(self, value) :        
        self.value=value
        self.address = hasher.sha256()        
        self.address.update(str(Bitcoin.nbObjects).encode())
        self.data=(0,[])
        if self.value + Bitcoin.currentValue <= Bitcoin.maxValue :
            Bitcoin.addressesList.append(self.address)
            Bitcoin.nbObjects+=1
            Bitcoin.currentValue+=self.value
        else :
            pass
        
        
    def __str__(self):
        return "Value : "+str(self.value)+"\nAddress : "+str(self.address)
Bitcoin.nbObjects=0    
bt=Bitcoin(2)
bt2=Bitcoin(0.3)
bt3=Bitcoin(0.4)
bt4=Bitcoin(17)
bt5=Bitcoin(0.4)
print(str(bt))
print(str(bt2))
print(str(bt3))
print(str(bt4))
print(str(bt5))
print(str(Bitcoin.nbObjects))
print("Adresses list : ")
for adress in Bitcoin.addressesList :
    print(adress)