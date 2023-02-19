from web3 import Web3
from web3.auto import w3
import json
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)
url = "http://127.0.0.1:8545"
web3 = Web3(Web3.HTTPProvider(url))

def getBalance(address):
    return web3.fromWei(w3.eth.get_balance(address), "ether")

def getAccounts():
    return web3.eth.accounts

def getPrivateKey():
    file = open("private.txt", "r")
    data = file.read()
    data_into_list = data.replace('\n', ' ').split(" ")
    file.close()
    return data_into_list

def getAccountPair():
    keys = getPrivateKey()
    acc = getAccounts()
    kp = []
    i = 1
    for x in acc:
        kp.append( { "address" : x , "key" : keys[i] } )
        i = i + 2
    return json.dumps(kp)

def transfer(sender_addr, key, ether, recv_addr):
    transaction = {
        'to' : recv_addr,
        'value' : web3.toWei(ether, 'ether'),
        'gas' : 21000,
        'gasPrice' : w3.toWei('50', 'gwei'),
        'nonce' : web3.eth.getTransactionCount(sender_addr)
    }
    signed_txn = w3.eth.account.sign_transaction(transaction, key)
    tx_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
    return web3.toWei(tx_hash)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/getaccounts')
def getAccount():
    return getAccountPair()

@app.route('/getbalance', methods=['POST'])
def tx_getBalance():
    data = request.json
    message = {
        "status" : "success",
        "ether" : getBalance(data['address'])
    }
    return jsonify(message), 200

@app.route('/transfer', methods=['POST'])
def tx_transfer():
    data = request.json
    message = {
        "status" : "Transfer success",
        "hash" : transfer(data['tx'], data['key'], data['ether'], data['rx'])
    }
    return jsonify(message), 200

if __name__ == "__main__":
    app.run(debug=True)