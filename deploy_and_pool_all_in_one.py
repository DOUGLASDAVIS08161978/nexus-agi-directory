#!/usr/bin/env python3
"""
ALL-IN-ONE: Deploy ERC-20 Token + Create Uniswap Pool + Add Liquidity
For Termux - No web3.py required
"""
import os
import sys
import json
import time
import requests
from ecdsa import SigningKey, SECP256k1
from Crypto.Hash import keccak

# Configuration
RPC_URL = "https://sepolia.base.org"
CHAIN_ID = 84532

# Uniswap V3 Addresses on Base Sepolia
WETH = "0x4200000000000000000000000000000000000006"
UNISWAP_V3_FACTORY = "0x4752ba5dbc23f44d87826276bf6fd6b1c372ad24"
POSITION_MANAGER = "0x27F971cb582BF9E50F397e4d29a5C7A34f11faA2"

# Token Configuration (CUSTOMIZE THIS!)
TOKEN_NAME = "Test Bitcoin"
TOKEN_SYMBOL = "tBTC"
TOKEN_DECIMALS = 8
TOKEN_SUPPLY = 21000000  # 21 million
POOL_PRICE = 20  # 1 token = 20 ETH (Bitcoin peg)

# ERC-20 Token Bytecode (with constructor for specified supply)
BYTECODE = "0x608060405234801561001057600080fd5b506a115eec47f6cf7e35000000600080803373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020819055503373ffffffffffffffffffffffffffffffffffffffff16600073ffffffffffffffffffffffffffffffffffffffff167fddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef6a115eec47f6cf7e350000006040516100c491906100e4565b60405180910390a36100ff565b6000819050919050565b6100de816100cb565b82525050565b60006020820190506100f960008301846100d5565b92915050565b6107018061010e6000396000f3fe608060405234801561001057600080fd5b50600436106100625760003560e01c806306fdde031461006757806318160ddd14610085578063313ce567146100a357806370a08231146100c157806395d89b41146100f1578063a9059cbb1461010f575b600080fd5b61006f61013f565b60405161007c9190610404565b60405180910390f35b61008d610178565b60405161009a919061043f565b60405180910390f35b6100ab610184565b6040516100b89190610476565b60405180910390f35b6100db60048036038101906100d691906104f4565b610189565b6040516100e8919061043f565b60405180910390f35b6100f96101a1565b6040516101069190610404565b60405180910390f35b6101296004803603810190610124919061054d565b6101da565b60405161013691906105a8565b60405180910390f35b6040518060400160405280600e81526020017f5465737420426974636f696e00000000000000000000000000000000000000081525081565b6a115eec47f6cf7e3500000081565b600881565b60006020528060005260406000206000915090505481565b6040518060400160405280600581526020017f7442544300000000000000000000000000000000000000000000000000000000815250815b6000816000803373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002054101561025d576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040161025490610626565b60405180910390fd5b816000803373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060008282546102ab919061066f565b92505081905550816000808573ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020600082825461030091906106a3565b925050819055508273ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff167fddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef84604051610364919061043f565b60405180910390a36001905092915050565b600081519050919050565b600082825260208201905092915050565b60005b838110156103b0578082015181840152602081019050610395565b60008484015250505050565b6000601f19601f8301169050919050565b60006103d882610376565b6103e28185610381565b93506103f2818560208601610392565b6103fb816103bc565b840191505092915050565b6000602082019050818103600083015261041e81846103cd565b905092915050565b6000819050919050565b61043981610426565b82525050565b60006020820190506104546000830184610430565b92915050565b600060ff82169050919050565b6104708161045a565b82525050565b600060208201905061048b6000830184610467565b92915050565b600080fd5b600073ffffffffffffffffffffffffffffffffffffffff82169050919050565b60006104c182610496565b9050919050565b6104d1816104b6565b81146104dc57600080fd5b50565b6000813590506104ee816104c8565b92915050565b60006020828403121561050a57610509610491565b5b6000610518848285016104df565b91505092915050565b61052a81610426565b811461053557600080fd5b50565b60008135905061054781610521565b92915050565b6000806040838503121561056457610563610491565b5b6000610572858286016104df565b925050602061058385828601610538565b9150509250929050565b60008115159050919050565b6105a28161058d565b82525050565b60006020820190506105bd6000830184610599565b92915050565b7f496e73756666696369656e742062616c616e636500000000000000000000000600082015250565b60006105f9601483610381565b9150610604826105c3565b602082019050919050565b60006020820190508181036000830152610628816105ec565b9050919050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052601160045260246000fd5b61066a81610426565b82525050565b600061067b82610426565b915061068683610426565b925082820390508181111561069e5761069d61062f565b5b92915050565b60006106af82610426565b91506106ba83610426565b92508282019050808211156106d2576106d161062f565b5b92915050565b600081519050919050565b600082825260208201905092915050565b6000819050602082019050919050565b61070d81610426565b82525050565b600061071f8383610704565b60208301905092915050565b6000602082019050919050565b6000610743826106d8565b61074d81856106e3565b9350610758836106f4565b8060005b8381101561078957815161077088826116713565b975061077b8361072b565b92505060018101905061075c565b5085935050505092915050565b60006020820190508181036000830152610ab08184610738565b90509291505056fea2646970667358221220d3e5c8f4e9b8c5f6e8c8e9f0c0f0c0f0c0f0c0f0c0f0c0f0c0f0c0f0c0f064736f6c63430008130033"

def keccak256(data):
    k = keccak.new(digest_bits=256)
    k.update(data)
    return k.digest()

def rlp_encode_int(n):
    if n == 0: return b'\x80'
    b = n.to_bytes((n.bit_length() + 7) // 8, 'big')
    if len(b) == 1 and b[0] < 0x80: return b
    return bytes([0x80 + len(b)]) + b

def rlp_encode_bytes(data):
    if len(data) == 1 and data[0] < 0x80: return data
    if len(data) <= 55: return bytes([0x80 + len(data)]) + data
    len_bytes = len(data).to_bytes((len(data).bit_length() + 7) // 8, 'big')
    return bytes([0xb7 + len(len_bytes)]) + len_bytes + data

def rlp_encode_list(items):
    encoded = b''.join(items)
    if len(encoded) <= 55: return bytes([0xc0 + len(encoded)]) + encoded
    len_bytes = len(encoded).to_bytes((len(encoded).bit_length() + 7) // 8, 'big')
    return bytes([0xf7 + len(len_bytes)]) + len_bytes + encoded

def rpc_call(method, params):
    payload = {"jsonrpc": "2.0", "method": method, "params": params, "id": 1}
    response = requests.post(RPC_URL, json=payload, headers={"Content-Type": "application/json"})
    result = response.json()
    if 'error' in result:
        raise Exception(f"RPC Error: {result['error']}")
    return result.get('result')

def send_transaction(private_key, to, data, value=0, gas_limit=500000):
    """Send a transaction and return the receipt"""
    private_key_bytes = bytes.fromhex(private_key.replace('0x', ''))
    sk = SigningKey.from_string(private_key_bytes, curve=SECP256k1)
    public_key = sk.get_verifying_key().to_string()
    address_bytes = keccak256(public_key)[-20:]
    address = '0x' + address_bytes.hex()

    # Get nonce and gas price
    nonce = int(rpc_call("eth_getTransactionCount", [address, "latest"]), 16)
    gas_price = int(rpc_call("eth_gasPrice", []), 16)

    # Build signing message
    to_bytes = bytes.fromhex(to.replace('0x', '')) if to else b''
    data_bytes = bytes.fromhex(data.replace('0x', '')) if data else b''

    signing_msg = rlp_encode_list([
        rlp_encode_int(nonce),
        rlp_encode_int(gas_price),
        rlp_encode_int(gas_limit),
        rlp_encode_bytes(to_bytes) if to else b'\x80',
        rlp_encode_int(value),
        rlp_encode_bytes(data_bytes) if data else b'\x80',
        rlp_encode_int(CHAIN_ID),
        b'\x80',
        b'\x80'
    ])

    # Sign
    msg_hash = keccak256(signing_msg)
    signature = sk.sign_digest(msg_hash, sigencode=lambda r, s, order: (r, s))
    r, s = signature
    v = CHAIN_ID * 2 + 35

    # Build signed transaction
    signed_tx = rlp_encode_list([
        rlp_encode_int(nonce),
        rlp_encode_int(gas_price),
        rlp_encode_int(gas_limit),
        rlp_encode_bytes(to_bytes) if to else b'\x80',
        rlp_encode_int(value),
        rlp_encode_bytes(data_bytes) if data else b'\x80',
        rlp_encode_int(v),
        rlp_encode_int(r),
        rlp_encode_int(s)
    ])

    raw_tx = '0x' + signed_tx.hex()
    tx_hash = rpc_call("eth_sendRawTransaction", [raw_tx])

    # Wait for receipt
    for _ in range(30):
        try:
            receipt = rpc_call("eth_getTransactionReceipt", [tx_hash])
            if receipt:
                return tx_hash, receipt
        except:
            pass
        time.sleep(2)

    raise Exception(f"Transaction timeout: {tx_hash}")

def main():
    private_key = os.getenv('PRIVATE_KEY')
    if not private_key:
        print("❌ ERROR: PRIVATE_KEY environment variable not set!")
        sys.exit(1)

    print("\n🚀 ALL-IN-ONE: DEPLOY TOKEN + CREATE UNISWAP POOL")
    print("=" * 70)

    # Get address
    pk_bytes = bytes.fromhex(private_key.replace('0x', ''))
    sk = SigningKey.from_string(pk_bytes, curve=SECP256k1)
    pub = sk.get_verifying_key().to_string()
    addr = '0x' + keccak256(pub)[-20:].hex()

    print(f"Deployer: {addr}")
    print(f"Token: {TOKEN_NAME} ({TOKEN_SYMBOL})")
    print(f"Supply: {TOKEN_SUPPLY:,} tokens")
    print(f"Pool Price: 1 {TOKEN_SYMBOL} = {POOL_PRICE} ETH\n")

    # STEP 1: Deploy Token
    print("=" * 70)
    print("STEP 1: DEPLOYING TOKEN")
    print("=" * 70)

    bytecode = BYTECODE.replace('0x', '')
    tx_hash, receipt = send_transaction(private_key, None, bytecode, gas_limit=1000000)

    token_address = receipt.get('contractAddress')
    print(f"✅ Token deployed: {token_address}")
    print(f"   TX: {tx_hash}\n")
    time.sleep(3)

    # STEP 2: Wrap ETH
    print("=" * 70)
    print("STEP 2: WRAPPING ETH TO WETH")
    print("=" * 70)

    wrap_amount = 500000000000000  # 0.0005 ETH in wei
    tx_hash, receipt = send_transaction(private_key, WETH, "", value=wrap_amount, gas_limit=50000)
    print(f"✅ Wrapped 0.0005 ETH to WETH")
    print(f"   TX: {tx_hash}\n")
    time.sleep(3)

    # STEP 3: Approve Token
    print("=" * 70)
    print("STEP 3: APPROVING TOKEN FOR UNISWAP")
    print("=" * 70)

    approve_data = "095ea7b3" + POSITION_MANAGER[2:].zfill(64) + "f" * 64
    tx_hash, receipt = send_transaction(private_key, token_address, approve_data, gas_limit=100000)
    print(f"✅ Token approved")
    print(f"   TX: {tx_hash}\n")
    time.sleep(3)

    # STEP 4: Approve WETH
    print("=" * 70)
    print("STEP 4: APPROVING WETH FOR UNISWAP")
    print("=" * 70)

    tx_hash, receipt = send_transaction(private_key, WETH, approve_data, gas_limit=100000)
    print(f"✅ WETH approved")
    print(f"   TX: {tx_hash}\n")
    time.sleep(3)

    # STEP 5: Create Pool
    print("=" * 70)
    print("STEP 5: CREATING UNISWAP POOL")
    print("=" * 70)

    # createPool(address tokenA, address tokenB, uint24 fee)
    create_pool_data = "a1671295"  # function selector
    create_pool_data += WETH[2:].zfill(64)
    create_pool_data += token_address[2:].zfill(64)
    create_pool_data += hex(3000)[2:].zfill(64)  # 0.3% fee

    try:
        tx_hash, receipt = send_transaction(private_key, UNISWAP_V3_FACTORY, create_pool_data, gas_limit=5000000)
        print(f"✅ Pool created")
        print(f"   TX: {tx_hash}\n")
        time.sleep(3)
    except Exception as e:
        if "already" in str(e).lower():
            print(f"✅ Pool already exists\n")
        else:
            raise

    # Get pool address
    get_pool_data = "1698ee82"  # getPool selector
    get_pool_data += WETH[2:].zfill(64)
    get_pool_data += token_address[2:].zfill(64)
    get_pool_data += hex(3000)[2:].zfill(64)

    pool_result = rpc_call("eth_call", [{"to": UNISWAP_V3_FACTORY, "data": "0x" + get_pool_data}, "latest"])
    pool_address = "0x" + pool_result[-40:]

    print(f"Pool address: {pool_address}\n")

    # STEP 6: Initialize Pool
    print("=" * 70)
    print("STEP 6: INITIALIZING POOL WITH PRICE")
    print("=" * 70)

    sqrt_price = int((POOL_PRICE ** 0.5) * (2 ** 96))
    init_data = "f637731d" + hex(sqrt_price)[2:].zfill(64)

    try:
        tx_hash, receipt = send_transaction(private_key, pool_address, init_data, gas_limit=500000)
        print(f"✅ Pool initialized at price {POOL_PRICE} ETH per token")
        print(f"   TX: {tx_hash}\n")
        time.sleep(3)
    except Exception as e:
        if "already" in str(e).lower():
            print(f"✅ Pool already initialized\n")
        else:
            raise

    # STEP 7: Add Liquidity
    print("=" * 70)
    print("STEP 7: ADDING LIQUIDITY")
    print("=" * 70)

    # mint((address,address,uint24,int24,int24,uint256,uint256,uint256,uint256,address,uint256))
    mint_data = "88316456"  # mint selector
    mint_data += "0000000000000000000000000000000000000000000000000000000000000020"  # offset
    mint_data += WETH[2:].zfill(64)  # token0
    mint_data += token_address[2:].zfill(64)  # token1
    mint_data += hex(3000)[2:].zfill(64)  # fee
    mint_data += "f" * 63 + "4"  # tickLower (-887220 in two's complement)
    mint_data += "0" * 59 + "d89b4"  # tickUpper (887220)
    mint_data += hex(200000000000000)[2:].zfill(64)  # amount0Desired (0.0002 WETH)
    mint_data += hex(10000)[2:].zfill(64)  # amount1Desired (0.0001 tokens with 8 decimals)
    mint_data += "0" * 64  # amount0Min
    mint_data += "0" * 64  # amount1Min
    mint_data += addr[2:].zfill(64)  # recipient
    mint_data += hex(int(time.time()) + 3600)[2:].zfill(64)  # deadline

    tx_hash, receipt = send_transaction(private_key, POSITION_MANAGER, mint_data, gas_limit=5000000)
    print(f"✅ Liquidity added!")
    print(f"   TX: {tx_hash}\n")

    # Final Summary
    print("=" * 70)
    print("🎉 SUCCESS! YOUR TOKEN IS LIVE ON UNISWAP!")
    print("=" * 70)
    print(f"\nToken Address: {token_address}")
    print(f"Pool Address: {pool_address}")
    print(f"Name: {TOKEN_NAME}")
    print(f"Symbol: {TOKEN_SYMBOL}")
    print(f"Supply: {TOKEN_SUPPLY:,} {TOKEN_SYMBOL}")
    print(f"Pool Price: 1 {TOKEN_SYMBOL} = {POOL_PRICE} ETH")
    print(f"\n🔍 View on BaseScan:")
    print(f"Token: https://sepolia.basescan.org/address/{token_address}")
    print(f"Pool: https://sepolia.basescan.org/address/{pool_address}")
    print("=" * 70)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
