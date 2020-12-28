# creating a simple blockchain

# each block will have its own timestamp
import datetime
# used to hash the blocks
import hashlib
# use dumps() function to encode the blocks before hashing
import json
# Web application from Flask Class, jsonify to import messages from requests
from flask import Flask, jsonify

# Building a Blockchain

class Blockchain:
    
    # initialize blockchain
    def __init__(self):
        # blockchain containing all the blocks
        self.chain = []
        # genesis block, previous_hash is string because SHA256 accepts strings
        self.create_block(proof = 1, previous_hash = '0')
        
    # create next blocks with their 4 essential keys
    def create_block(self, proof, previous_hash):
        # dictionary to define each block with its 4 essential keys
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash}
        # append new block to the chain
        self.chain.append(block)
        return block
    
    # get previous block (the last block in the chain)
    def get_previous_block(self):
        return self.chain[-1]
    
    # proof of work, hard to find and easy to verify (problem to impose on miner)
    # number or peice of data that miners need to find to mine a new block
    def proof_of_work(self, previous_proof):
        # to solve problem, incremement by 1 until right proof is found
        new_proof = 1
        check_proof = False
        while check_proof is False:
            # convert to string and encode in order to format for hash sha256(), then run hexdigest() 
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            # the more leading zeros you impose, the harder it is for miner to solve the problem
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof
    
    # hash the block
    def hash(self, block):
        # dumps() makes block dictionary a string
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    # check if each block has correct proof of work and that the previous hash of each block
    # is equal to the hash of the previous block 
    def is_chain_valid(self, chain): 
        # initialize the first previous block
        previous_block = chain[0] 
        block_index = 1
        # iterate through all blocks in the blockchain
        while block_index < len(chain):
            # current block (starts at chain[1]) 
            block = chain[block_index]
            # check if current blocks previous hash is equivalent to the hash of the previous block
            if block['previous_hash'] != self.hash(previous_block):
                return False
            # get previous and current proof, apply hash_operation and check if proof is valid
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            # update previous block to current block for next iteration
            previous_block = block
            block_index += 1
        return True
           
# Mining our Blockchain

# Creating a Web App
app = Flask(__name__)

# Creating a Blockchain
blockchain = Blockchain()

# Welcome message
@app.route('/', methods = ['GET'])
def home():
    response = {'message': 'Welcome to nickcoin!'}
    return jsonify(response), 200

# Mining a new block, by solving proof of work problem, finding the proof based
# on the previous proof (the last proof given in the last block).
@app.route('/mine_block', methods = ['GET'])
def mine_block():
    # first we need the previous proof
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    # proof of future new block
    proof = blockchain.proof_of_work(previous_proof)
    # get the previous hash, to create a new block  
    previous_hash = blockchain.hash(previous_block)
    # append new block that was just mined, by creatung a new block
    block = blockchain.create_block(proof, previous_hash)
    # response to GET request 
    response = {'message': 'Congratulations, you just mined a block!',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash']}
    return jsonify(response), 200

# Getting the full Blockchain
@app.route('/get_chain', methods = ['GET'])
def get_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200    

# Check if the Blockchain is valid
@app.route('/is_valid', methods = ['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message': 'All good. The Blockchain is valid.'}
    else:
        response = {'message': 'Houston, we have a problem. The Blockchain is not valid.'}
    return jsonify(response), 200

# Running the app
app.run(host = 'localhost', port = 5000)
    
    


    
    
    
    
    
            
    
    
    
    
    
    
    
    
