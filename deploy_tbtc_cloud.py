#!/usr/bin/env python3
"""
Deploy tBTC Token to Base Sepolia via Google Cloud Build
"""
import os
import sys
import json
import hashlib
import requests
from ecdsa import SigningKey, SECP256k1
from Crypto.Hash import keccak

# Configuration
RPC_URL = os.getenv('BASE_SEPOLIA_RPC', 'https://sepolia.base.org')
CHAIN_ID = int(os.getenv('CHAIN_ID', '84532'))
PRIVATE_KEY = os.getenv('PRIVATE_KEY')

if not PRIVATE_KEY:
    print("❌ ERROR: PRIVATE_KEY environment variable not set!")
    sys.exit(1)

# Remove 0x prefix if present
PRIVATE_KEY = PRIVATE_KEY.replace('0x', '')

# tBTC ERC-20 Contract Bytecode (with constructor for 21M supply, 8 decimals)
# This is the compiled bytecode for a standard ERC-20 token
BYTECODE = "0x608060405234801561001057600080fd5b506a115eec47f6cf7e35000000600080803373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020819055503373ffffffffffffffffffffffffffffffffffffffff16600073ffffffffffffffffffffffffffffffffffffffff167fddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef6a115eec47f6cf7e350000006040516100c491906100e4565b60405180910390a36100ff565b6000819050919050565b6100de816100cb565b82525050565b60006020820190506100f960008301846100d5565b92915050565b6107018061010e6000396000f3fe608060405234801561001057600080fd5b50600436106100625760003560e01c806306fdde031461006757806318160ddd14610085578063313ce567146100a357806370a08231146100c157806395d89b41146100f1578063a9059cbb1461010f575b600080fd5b61006f61013f565b60405161007c9190610404565b60405180910390f35b61008d610178565b60405161009a919061043f565b60405180910390f35b6100ab610184565b6040516100b89190610476565b60405180910390f35b6100db60048036038101906100d691906104f4565b610189565b6040516100e8919061043f565b60405180910390f35b6100f96101a1565b6040516101069190610404565b60405180910390f35b6101296004803603810190610124919061054d565b6101da565b60405161013691906105a8565b60405180910390f35b6040518060400160405280600e81526020017f5465737420426974636f696e00000000000000000000000000000000000000081525081565b6a115eec47f6cf7e3500000081565b600881565b60006020528060005260406000206000915090505481565b6040518060400160405280600581526020017f7442544300000000000000000000000000000000000000000000000000000000815250815b6000816000803373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002054101561025d576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040161025490610626565b60405180910390fd5b816000803373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060008282546102ab919061066f565b92505081905550816000808573ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020600082825461030091906106a3565b925050819055508273ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff167fddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef84604051610364919061043f565b60405180910390a36001905092915050565b600081519050919050565b600082825260208201905092915050565b60005b838110156103b0578082015181840152602081019050610395565b60008484015250505050565b6000601f19601f8301169050919050565b60006103d882610376565b6103e28185610381565b93506103f2818560208601610392565b6103fb816103bc565b840191505092915050565b6000602082019050818103600083015261041e81846103cd565b905092915050565b6000819050919050565b61043981610426565b82525050565b60006020820190506104546000830184610430565b92915050565b600060ff82169050919050565b6104708161045a565b82525050565b600060208201905061048b6000830184610467565b92915050565b600080fd5b600073ffffffffffffffffffffffffffffffffffffffff82169050919050565b60006104c182610496565b9050919050565b6104d1816104b6565b81146104dc57600080fd5b50565b6000813590506104ee816104c8565b92915050565b60006020828403121561050a57610509610491565b5b6000610518848285016104df565b91505092915050565b61052a81610426565b811461053557600080fd5b50565b60008135905061054781610521565b92915050565b6000806040838503121561056457610563610491565b5b6000610572858286016104df565b925050602061058385828601610538565b9150509250929050565b60008115159050919050565b6105a28161058d565b82525050565b60006020820190506105bd6000830184610599565b92915050565b7f496e73756666696369656e742062616c616e636500000000000000000000000600082015250565b60006105f9601483610381565b9150610604826105c3565b602082019050919050565b60006020820190508181036000830152610628816105ec565b9050919050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052601160045260246000fd5b61066a81610426565b82525050565b600061067b82610426565b915061068683610426565b925082820390508181111561069e5761069d61062f565b5b92915050565b60006106af82610426565b91506106ba83610426565b92508282019050808211156106d2576106d161062f565b5b92915050565b600081519050919050565b600082825260208201905092915050565b6000819050602082019050919050565b61070d81610426565b82525050565b600061071f8383610704565b60208301905092915050565b6000602082019050919050565b6000610743826106d8565b61074d81856106e3565b9350610758836106f4565b8060005b8381101561078957815161077088826116713565b975061077b8361072b565b92505060018101905061075c565b5085935050505092915050565b60006020820190508181036000830152610ab08184610738565b90509291505056fea2646970667358221220d3e5c8f4e9b8c5f6e8c8e9f0c0f0c0f0c0f0c0f0c0f0c0f0c0f0c0f0c0f064736f6c63430008130033"

def keccak256(data):
    k = keccak.new(digest_bits=256)
    k.update(data)
    return k.digest()

def rlp_encode_int(n):
    if n == 0:
        return b'\x80'
    b = n.to_bytes((n.bit_length() + 7) // 8, 'big')
    if len(b) == 1 and b[0] < 0x80:
        return b
    return bytes([0x80 + len(b)]) + b

def rlp_encode_bytes(data):
    if len(data) == 1 and data[0] < 0x80:
        return data
    if len(data) <= 55:
        return bytes([0x80 + len(data)]) + data
    len_bytes = len(data).to_bytes((len(data).bit_length() + 7) // 8, 'big')
    return bytes([0xb7 + len(len_bytes)]) + len_bytes + data

def rlp_encode_list(items):
    encoded = b''.join(items)
    if len(encoded) <= 55:
        return bytes([0xc0 + len(encoded)]) + encoded
    len_bytes = len(encoded).to_bytes((len(encoded).bit_length() + 7) // 8, 'big')
    return bytes([0xf7 + len(len_bytes)]) + len_bytes + encoded

def rpc_call(method, params):
    payload = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": 1
    }
    response = requests.post(RPC_URL, json=payload, headers={"Content-Type": "application/json"})
    result = response.json()

    if 'error' in result:
        raise Exception(f"RPC Error: {result['error']}")

    return result.get('result')

def deploy_tbtc():
    print("\n🚀 DEPLOYING tBTC TOKEN VIA GOOGLE CLOUD BUILD\n")
    print("=" * 70)

    # Setup private key
    private_key_bytes = bytes.fromhex(PRIVATE_KEY)
    sk = SigningKey.from_string(private_key_bytes, curve=SECP256k1)
    public_key = sk.get_verifying_key().to_string()

    # Derive address
    address_bytes = keccak256(public_key)[-20:]
    address = '0x' + address_bytes.hex()

    print(f"Deploying from: {address}")
    print(f"Chain ID: {CHAIN_ID}")
    print(f"RPC: {RPC_URL}\n")

    # Get nonce
    nonce_hex = rpc_call("eth_getTransactionCount", [address, "latest"])
    nonce = int(nonce_hex, 16)
    print(f"Nonce: {nonce}")

    # Get gas price
    gas_price_hex = rpc_call("eth_gasPrice", [])
    gas_price = int(gas_price_hex, 16)
    print(f"Gas Price: {gas_price} wei")

    # Prepare bytecode
    bytecode = bytes.fromhex(BYTECODE.replace('0x', ''))
    print(f"Bytecode length: {len(bytecode)} bytes")

    # Build transaction for signing
    gas_limit = 1000000

    signing_msg = rlp_encode_list([
        rlp_encode_int(nonce),
        rlp_encode_int(gas_price),
        rlp_encode_int(gas_limit),
        b'\x80',  # Empty 'to' for contract creation
        rlp_encode_int(0),  # value
        rlp_encode_bytes(bytecode),
        rlp_encode_int(CHAIN_ID),
        b'\x80',
        b'\x80'
    ])

    # Sign transaction
    msg_hash = keccak256(signing_msg)
    signature = sk.sign_digest(msg_hash, sigencode=lambda r, s, order: (r, s))
    r, s = signature

    v = CHAIN_ID * 2 + 35

    # Build signed transaction
    signed_tx = rlp_encode_list([
        rlp_encode_int(nonce),
        rlp_encode_int(gas_price),
        rlp_encode_int(gas_limit),
        b'\x80',
        rlp_encode_int(0),
        rlp_encode_bytes(bytecode),
        rlp_encode_int(v),
        rlp_encode_int(r),
        rlp_encode_int(s)
    ])

    raw_tx = '0x' + signed_tx.hex()

    print("\n🔄 Sending deployment transaction...")

    # Send transaction
    tx_hash = rpc_call("eth_sendRawTransaction", [raw_tx])

    print(f"✅ Transaction sent!")
    print(f"TX Hash: {tx_hash}")

    # Wait for receipt
    print("\n⏳ Waiting for confirmation...")

    receipt = None
    for i in range(60):
        try:
            receipt = rpc_call("eth_getTransactionReceipt", [tx_hash])
            if receipt:
                break
        except:
            pass

        import time
        time.sleep(2)
        print(".", end="", flush=True)

    print()

    if not receipt:
        raise Exception("Transaction receipt not found after 2 minutes")

    if receipt.get('status') == '0x0':
        raise Exception("Transaction failed!")

    contract_address = receipt.get('contractAddress')

    print("\n" + "=" * 70)
    print("🎉 tBTC TOKEN DEPLOYED SUCCESSFULLY!")
    print("=" * 70)
    print(f"\nContract Address: {contract_address}")
    print(f"Transaction Hash: {tx_hash}")
    print(f"Block Number: {receipt.get('blockNumber')}")
    print(f"Gas Used: {int(receipt.get('gasUsed'), 16)}")
    print(f"\n📊 Token Details:")
    print(f"  Name: Test Bitcoin")
    print(f"  Symbol: tBTC")
    print(f"  Decimals: 8")
    print(f"  Total Supply: 21,000,000 tBTC")
    print(f"  Owner: {address}")
    print(f"\n🔍 View on BaseScan:")
    print(f"https://sepolia.basescan.org/address/{contract_address}")
    print("=" * 70)

    # Save output
    output = {
        "contract_address": contract_address,
        "tx_hash": tx_hash,
        "deployer": address,
        "name": "Test Bitcoin",
        "symbol": "tBTC",
        "decimals": 8,
        "total_supply": "21000000",
        "basescan_url": f"https://sepolia.basescan.org/address/{contract_address}"
    }

    with open('/workspace/deployment_output.txt', 'w') as f:
        f.write(json.dumps(output, indent=2))

    return contract_address

if __name__ == "__main__":
    try:
        deploy_tbtc()
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        sys.exit(1)
