# nickcoin-blockchain

A small and simple blockchain implementation using 4 nodes through Flask and JSON, using Python.

# How to run the Blockchain:

The Blockchain can be run on your local machine through localhost, using ports 5000-5003.
http://localhost:5000/

To run multiple nodes: Run all 4 programs through 4 different terminal windows.

In order to mine blocks, retrieve the current chain, check if a chain is valid, add transactions,
connect nodes, or replace a chain, we can visit the following url's:
(visiting these url's will give information or make changes to the blockchain)

http://localhost:5000/mine_block OR /get_chain OR /is_valid
http://localhost:5001/mine_block OR /get_chain OR /is_valid OR /add_transaction OR /connect_node OR /replace_chain
http://localhost:5002/mine_block OR /get_chain OR /is_valid OR /add_transaction OR /connect_node OR /replace_chain
http://localhost:5003/mine_block OR /get_chain OR /is_valid OR /add_transaction OR /connect_node OR /replace_chain

# Index

mine_block, mines a new block and adds it to its chain for each respective blockchain.

get_chain, will give you all information relating to its respective chain.

is_valid, will check the proof of work and validate the chain.
(checks if each block has correct proof of work and that the previous hash of each block is equal to the hash of the previous block)

add_transaction, mimicks the sending and recieving of funds which is recorded in the chain.

connect_node, connects all available nodes together.

replace_chain, in a large block chain there could be a lag between nodes...
(two nodes far away from each other can mine two blocks (same blocks, two systems) at the same time. It has to pick one of the two blocks (biggest) to keep growing.)
