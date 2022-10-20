import datetime
import json
import hashlib
from urllib import response
from flask import Flask , jsonify

class Blockchain:
    def __init__(self):
        #Save group block's
        self.chain = [] #list save block
        
        self.transaction = 0 #Value Money

        #genesis block
        self.create_block(nonce = 1, previous_hash = "0")

    #build block on the blockchain
    def create_block(self, nonce, previous_hash):
        #save other data block's
        block = {
            "index" : len(self.chain) + 1,
            "timestamp" : str(datetime.datetime.now()), 
            "nonce" : nonce,
            "data" : self.transaction,
            "previous_hash" : previous_hash
        }
        self.chain.append(block)
        return block

    #Service about block after
    def get_previous_block(self):
        return self.chain[-1]
    
    #Encode block
    def hash(self, block):
        #Trasfer python object (dict) => json object
        encode_block = json.dumps(block, sort_keys = True).encode()
        #sha-256
        return hashlib.sha256(encode_block).hexdigest()

    def proof_of_work(self, previous_nonce):
        #Need value nonce ==> ???? so target hash => int 4 of fisrt ==> 0000xxxxxxxxxx
        new_nonce = 1  #value for need 
        check_proof = False #Check value nonce's so

        #Edit for math
        while check_proof is False:
            #int base16 for 1 
            hash_operation = hashlib.sha256(str(new_nonce ** 2 - previous_nonce ** 2).encode()).hexdigest() 
            if hash_operation[:4] == "0000":
                check_proof = True
            else:
                new_nonce += 1
        return new_nonce

    #Proof block
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        
        while block_index < len(chain):
            block = chain[block_index] # block for proof
            if block["previious_hash"] != self.hash(previous_block):
                return False
            
            previous_nonce = previous_block["nonce"] #nonce after
            nonce = block["nonce"] # nonce proof block's
            hash_operation = hashlib.sha256(str(nonce ** 2 - previous_nonce ** 2).encode()).hexdigest()
            
            if hash_operation[: 4] != "0000":
                return False

            previous_block = block
            block_index += 1
    
        return True

#web server
app = Flask(__name__)

blockchain = Blockchain()
#use blockchain
#routing
@app.route("/")
def hello():
    return "<h1>Hello Blockchain</h1>"

@app.route("/get_chain", methods = ["GET"])
def get_chain():
    response = {
        "chain": blockchain.chain, 
        "length": len(blockchain.chain),
    }
    return jsonify(response), 200

@app.route("/mining", methods = ["GET"])
def mining_block():
    amount = 1000000 #Value money for Transaction
    blockchain.transaction = blockchain.transaction + amount
    
    #WOF 
    previous_block = blockchain.get_previous_block()
    previous_nonce = previous_block["nonce"]
    
    #nonce
    nonce = blockchain.proof_of_work(previous_nonce)
    
    #Search value nonce after
    previous_hash = blockchain.hash(previous_block)

    #update new block
    block = blockchain.create_block(nonce, previous_hash)

    response = {
        "message": "Mining Block Successfully",
        "index": block["index"],
        "timestamp": block["timestamp"],
        "data": block["data"],
        "nonce": block["nonce"],
        "previous_hash": block["previous_hash"]
    }
    return jsonify(response), 20010

@app.route("/is_valid", methods = ["GET"])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)

    if is_valid:
        response = {"message": "Blockchain Valid"}
    else :
        response = {"message": "Have Problem, Blockchain IS Not Valid"}

    return jsonify(response), 200

#Inside encode fisrt block
#print(blockchain.hash(blockchain.chain[0]))
#Inside encode II block
#print(blockchain.hash(blockchain.chain[1]))


#run server

if __name__ == "__main__":
    app.run()