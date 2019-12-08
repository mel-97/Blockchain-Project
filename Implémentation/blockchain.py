# -*- coding: utf-8 -*-
"""
Implémentation de la BlockChain
"""
import sys
sys.path.append(r"C:\Users\Faycel\Desktop\IMT Studies\Projet DEV\Implémentation")
import hashlib as hasher
import datetime as date
from Bitcoin_user import *
import random
import time

def install_and_import(package):
    import importlib
    try:
        importlib.import_module(package)
    except ImportError:
        import pip
        pip.main(['install', package])
    finally:
        globals()[package] = importlib.import_module(package)


install_and_import('schedule')

def rountineCheck():
    print("\n\tRountine check Ongoing.\n")
    for user in User.UsersList :
        for bitcoin in user.Wallet :
            if bitcoin not in Bitcoin.BitcoinList :
                input("\n\tForgery found and deleted :\nBitcoin of value "+str(bitcoin.value)+" in possession of the user "+user.nom+" "+user.prenom+"\n")
                user.Wallet.remove(bitcoin)
                del bitcoin

def proofOfWork(last_proof) :
    incrementor=last_proof+1
    while not (incrementor % 719 == 0 and incrementor % last_proof == 0):
        incrementor+=1
    string="Proof of work just achieved -> Last_proof was : "+str(last_proof)+" and current proof is : "+str(incrementor)
    input(string)
    return incrementor

def proofOfWork2(last_proof, current_data) :
    origin=str(last_proof)+str(current_data)
    temp=0
    proved=origin+str(temp)
    sha=hasher.sha256()
    sha.update(proved.encode())
    sha=sha.hexdigest()
    string=str(sha)
    while string[:4] != "0000" :
        temp+=1
        proved=origin+str(temp)
        sha=hasher.sha256()
        sha.update(proved.encode())
        sha=sha.hexdigest()
        string=str(sha)
    print("temp="+str(temp))
    return temp
        
        

class Block:
    def __init__(self, index, timestamp, data, previous_hash, proof):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.hash_block()
        self.proof = proof
  
    def hash_block(self):
        sha = hasher.sha256()
        block = str(self.index) + str(self.timestamp) + str(self.data) + str(
            self.previous_hash)
        sha.update(block.encode('utf-8'))
        return sha.hexdigest()
    
    def __str__(self):
        return "Block <%s>: %s" % (self.hash, self.data)

    def next_block(last_block):
        this_index = last_block.index + 1
        this_timestamp = date.datetime.now()
        this_data = "Hey! I'm block " + repr(this_index)
        this_hash = last_block.hash
        this_proof = proofOfWork2(last_block.proof, this_data)
        return Block(this_index, this_timestamp, this_data, this_hash, this_proof)
    
def transactionTreatment(last_block):
    Blocks=[last_block]
    current=0
    for transaction in Transaction.TransactionsList :
        rountineCheck()
        print("Transaction en cours : "+str(transaction))
        if not len(transaction.block) : #if it wasn't already treated
            sender=transaction.sender
            receiver=transaction.receiver
            allGood=True
            for pending in receiver.pendingBitcoins :
                state = pending[0]
                bitcoin = pending[1]
                trans = pending[2]
                if trans == transaction :
                    allGood*=receiver.verify(bitcoin, bitcoin.signature)
                    if allGood and state == "In" :
                        bitcoin.data[0]=0
                        bitcoin.giveBitcoin(receiver)
                        bitcoin.removeBitcoin(sender)
                        receiver.pendingBitcoins.remove(pending) #no longer pending
                        
            for pending in sender.pendingBitcoins :
                state = pending[0]
                bitcoin = pending[1]
                trans = pending[2]
                if trans == transaction and allGood :
                    if state == "Out" :
                        sender.pendingBitcoins.remove(pending)
                    print("next")     
            if allGood :
                print("A new transaction has been verified.")
                data=str(transaction)
                newBlock=Block(Blocks[current].index+1,date.datetime.now(),data,Blocks[current].hash,proofOfWork(Blocks[current].proof))
                Blocks.append(newBlock)
                current+=1
                transaction.block.append(newBlock)
            else :
                print("\nTransaction is forged.\nTransaction cancelled.\n")
                for pending in receiver.pendingBitcoins :
                    state = pending[0]
                    bitcoin = pending[1]
                    trans = pending[2]
                    if trans == transaction :
                        if state == "In" :
                            receiver.pendingBitcoins.remove(pending)
                for pending in sender.pendingBitcoins :
                    state = pending[0]
                    bitcoin = pending[1]
                    trans = pending[2]
                    if trans == transaction :
                        if state == "Out" :
                            sender.pendingBitcoins.remove(pending)
                            bitcoin.giveBitcoin(sender)
    return Blocks

def create_genesis_block():
  # Manually construct a block with
  # index zero and arbitrary previous hash
    data="Genesis Block"
    proof=proofOfWork2("", data)
    return Block(0, date.datetime.now(), data, "0",proof)
    
# Create the blockchain and add the genesis block
    """
def job() :
    print("test")
schedule.every(10).seconds.do(job)
"""

input("\t\tDemonstration\nLet's see the users :")
for user in User.UsersList :
    print(str(user))
    print("Solde :"+str(user.getSolde()))
input("\t Transaction 1 : Hafid Fayçal -> Maachou Marouane : 1 bitcoin")
tr=Transaction(User.getUserFromName("Hafid", "Faycal"),User.getUserFromName("Maachou", "Marouane"),1,date.datetime.now())
input("\t Transaction 2 : Hafid Fayçal -> Maachou Marouane : 0.2 bitcoin")
tr2=Transaction(User.getUserFromName("Hafid", "Faycal"),User.getUserFromName("Maachou", "Marouane"),0.2,date.datetime.now())
input("Now we're illegally giving Maroua 500 Bitcoins")
b0=Bitcoin(500)
b0.giveBitcoin(user4)
input("\t Transaction 2 : Dahoumane Mehdi -> Dupraz Elsa : 3 bitcoin")
tr3=Transaction(User.getUserFromName("Dahoumane", "Mehdi"),User.getUserFromName("Dupraz", "Elsa"),3,date.datetime.now())

input("\n\nBEGINNING THE CREATION OF THE BLOCKCHAIN\n\n")
blockchain = []
blocks=transactionTreatment(create_genesis_block())
for block in blocks :
    blockchain.append(block)
#print(str(blocks))
for block in blockchain :
    input("New block : "+str(block)+"\n\n")
input("\n\nNow let's trace Marouane's bitcoins :\n")
for bitcoin in user2.Wallet :
    input(bitcoin.previousOwners())
"""
while True:
    schedule.run_pending()
    time.sleep(1)
"""
"""
# How many blocks should we add to the chain
# after the genesis block
num_of_blocks_to_add = 20

# Add blocks to the chain
for i in range(0, num_of_blocks_to_add):
  block_to_add = Block.next_block(previous_block)
  blockchain.append(block_to_add)
  previous_block = block_to_add
  # Tell everyone about it!
  print("Block #{} has been added to the blockchain!".format(block_to_add.index))
  print(str(block_to_add))
  """