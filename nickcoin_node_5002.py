# Module 1 - Create a Blockchain
# Module 2 - Create a Cryptocurrency

# Importing the libraries
# each block will have its own timestamp
import datetime
# used to hash the blocks
import hashlib
# use dumps() function to encode the blocks before hashing
import json
# used to connect nodes
import requests
# generates a random and unique address
from uuid import uuid4
# parse node address 
from urllib.parse import urlparse
# Web application from Flask Class, jsonify to import messages from requests, request to connect nodes
from flask import Flask, jsonify, request

# Part 1 - Building a Blockchain

class Blockchain:

	# initialize blockchain
	def __init__(self):
		# blockchain containing all the blocks
		self.chain = []
		# list of transactions (before they're added to a block)
		self.transactions = []
		# genesis block, previous_hash is string because SHA256 accepts strings
		self.create_block(proof = 1, previous_hash = '0')
		# initialize nodes in a set, because they dont need a particular order
		self.nodes = set()

	# create next blocks with their 4 essential keys
	def create_block(self, proof, previous_hash):
		# dictionary to define each block with its 4 essential keys
		block = {'index': len(self.chain) + 1,
				 'timestamp': str(datetime.datetime.now()),
				 'proof': proof,
				 'previous_hash': previous_hash,
				 'transactions': self.transactions}
		# empty the transactions list for the next block
		self.transactions = []
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

	# create format for transactions, and to append transactions to list of transactions
	def add_transaction(self, sender, receiver, amount):
		self.transactions.append({'sender': sender,
								'receiver': receiver,
								'amount': amount})
		# get index of new block of the chain (last block + 1)
		previous_block = self.get_previous_block()
		return previous_block['index'] + 1

	# add nodes to set by their address
	def add_node(self, address):
		# first parse address of the node, address is parsed into multiple fields
		parsed_url = urlparse(address)
		# add the "X.X.X.X" address to the set of nodes
		self.nodes.add(parsed_url.netloc)

	# replace any chain that is shorter than the longest chain in the network (consensus)
	def replace_chain(self):
		# network containing all the nodes
		network = self.nodes
		# longest chain variable
		longest_chain = None
		max_length = len(self.chain)
		# iterate through all nodes in network to find longest chain
		for nodes in network:
			# use request library to get response from get_chain() request, to find length from each node
			# each node is already the "X.X.X.X" address from previous function def.
			response = requests.get(f'http://{nodes}/get_chain')
			# is status is ok, get the length, and make sure the chain is valid
			if response.status_code == 200:
				length = response.json()['length']
				chain = response.json()['chain']
				if length > max_length and self.is_chain_valid(chain):
					max_length = length
					longest_chain = chain
			# if longest chain was found (not None), make a permanent replacement
			if longest_chain:
				self.chain = longest_chain
				return True
			# if chain was not replaced (still None), return false
			return False

# Part 2 - Mining our Blockchain

# Creating a Web App
app = Flask(__name__)

# Creating an address for the node on Port 5000
# make the address a string and remove dashes
node_address = str(uuid4()).replace('-', '')

# Creating a Blockchain
blockchain = Blockchain()

# Welcome message
@app.route('/', methods=['GET'])
def home():
    response = {'message': 'Welcome to nickcoin node 2!'}
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
	# add transactions
	blockchain.add_transaction(sender = node_address, receiver = 'Kirill', amount = 10)
	# append new block that was just mined, by creatung a new block
	block = blockchain.create_block(proof, previous_hash)
	# response to GET request
	response = {'message': 'Congratulations, you just mined a block!',
				'index': block['index'],
				'timestamp': block['timestamp'],
				'proof': block['proof'],
				'previous_hash': block['previous_hash'],
				'transactions': block['transactions']}
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

# Adding a new transaction to the Blockchain
@app.route('/add_transaction', methods = ['POST'])
def add_transaction():
	# get json file posted on 'Postman'
	json = request.get_json()
	# keys that must be inside every transaction
	transaction_keys = ['sender', 'receiver', 'amount']
	if not all (key in json for key in transaction_keys):
		return 'Some elements of the transaction are missing', 400
	# add the transaction and get the index (which add_transaction() does)
	index = blockchain.add_transaction(json['sender'], json['receiver'], json['amount'])
	response = {'message': f'This transaction will be added to block {index}'}
	return jsonify(response), 201

# Part 3 - Decentralizing our Blockchain

# Connecting new nodes
@app.route('/connect_node', methods = ['POST'])
def connect_node():
	json = request.get_json()
	# connect new node to all other nodes in the network
	nodes = json.get('nodes')
	if nodes is None:
		return "No node", 400
	# iterate though all the nodes to connect them
	for node in nodes:
		blockchain.add_node(node)
	response = {'message': 'All the nodes are now connected. The nickcoin Blockchain now contains the following coins:',
				'total_nodes': list(blockchain.nodes)}
	return jsonify(response), 201

# Replacing the chain by the longest chain if needed
@app.route('/replace_chain', methods = ['GET'])
def replace_chain():
	# checks if we need to replace the chain (true, or false)
	is_chain_replaced = blockchain.replace_chain()
	if is_chain_replaced:
		response = {'message': 'The nodes had different chains so the chain was replaced by the longest one.',
					'new_chain': blockchain.chain}
	else:
		response = {'message': 'All good. The chain is the largest one.',
					'actual_chain': blockchain.chain}
	return jsonify(response), 200

# Running the app
app.run(host = 'localhost', port = 5002)
