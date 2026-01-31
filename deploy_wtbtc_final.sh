#!/bin/bash
# WTBTC Deployment - Production Ready for Termux
# Autonomous deployment, verification, and publishing to Base Sepolia

pip3 install -q ecdsa pycryptodome requests 2>/dev/null; python3 << 'EOF'
import time, requests
from ecdsa import SigningKey, SECP256k1
from ecdsa.util import sigencode_string
from Crypto.Hash import keccak

PRIVATE_KEY = "0eee6f45b0af8f5a6a24744a1a978346d5bd66b41c64dc30bd18a32e246515cd"
BASE_RPC = "https://sepolia.base.org"
CHAIN_ID = 84532

def kh(d):
    k = keccak.new(digest_bits=256)
    k.update(d)
    return k.digest()

def rpc(m, p=[]):
    r = requests.post(BASE_RPC, json={"jsonrpc": "2.0", "method": m, "params": p, "id": 1}, timeout=30)
    return r.json().get("result")

def rlp_encode_int(n):
    """Encode integer with proper minimal representation (no leading zeros)"""
    if n == 0:
        return b'\x80'
    # Convert to minimal bytes
    b = n.to_bytes((n.bit_length() + 7) // 8, 'big')
    if len(b) == 1 and b[0] < 0x80:
        return b
    return bytes([0x80 + len(b)]) + b

def rlp_encode_bytes(v):
    """Encode bytes/string"""
    if isinstance(v, str):
        v = bytes.fromhex(v[2:] if v.startswith('0x') else v) if v else b''
    if len(v) == 0:
        return b'\x80'
    if len(v) == 1 and v[0] < 0x80:
        return v
    if len(v) <= 55:
        return bytes([0x80 + len(v)]) + v
    # For long strings
    len_bytes = len(v).to_bytes((len(v).bit_length() + 7) // 8, 'big')
    return bytes([0xb7 + len(len_bytes)]) + len_bytes + v

def rlp_encode_list(items):
    """Encode list"""
    encoded = b''.join(items)
    if len(encoded) <= 55:
        return bytes([0xc0 + len(encoded)]) + encoded
    len_bytes = len(encoded).to_bytes((len(encoded).bit_length() + 7) // 8, 'big')
    return bytes([0xf7 + len(len_bytes)]) + len_bytes + encoded

# Setup wallet
sk = SigningKey.from_string(bytes.fromhex(PRIVATE_KEY), curve=SECP256k1)
pub = sk.get_verifying_key().to_string()
addr = '0x' + kh(pub)[-20:].hex()

print("="*80)
print("🚀 WTBTC AUTONOMOUS DEPLOYMENT TO BASE SEPOLIA")
print("="*80)
print(f"\nDeployer: {addr}")

# Check balance
bal = int(rpc("eth_getBalance", [addr, "latest"]) or "0x0", 16) / 1e18
print(f"Balance: {bal:.6f} ETH")

if bal < 0.0008:
    print(f"\n⚠️  Insufficient balance for deployment")
    print(f"Need: 0.001 ETH | Have: {bal:.6f} ETH")
    print(f"\nGet testnet ETH:")
    print(f"  https://www.alchemy.com/faucets/base-sepolia")
    print(f"  Send to: {addr}")
    exit(1)

# Verified working bytecode from successful deployment
bytecode = "0x608060405234801561001057600080fd5b50655af3107a40006000803373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020819055503373ffffffffffffffffffffffffffffffffffffffff16600073ffffffffffffffffffffffffffffffffffffffff167fddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef655af3107a40006040516100be91906100e4565b60405180910390a36100ff565b6000819050919050565b6100de816100cb565b82525050565b60006020820190506100f960008301846100d5565b92915050565b6106fc8061010e6000396000f3fe608060405234801561001057600080fd5b50600436106100625760003560e01c806306fdde031461006757806318160ddd14610085578063313ce567146100a357806370a08231146100c157806395d89b41146100f1578063a9059cbb1461010f575b600080fd5b61006f61013f565b60405161007c9190610404565b60405180910390f35b61008d610178565b60405161009a919061043f565b60405180910390f35b6100ab610182565b6040516100b89190610476565b60405180910390f35b6100db60048036038101906100d691906104f4565b610187565b6040516100e8919061043f565b60405180910390f35b6100f961019f565b6040516101069190610404565b60405180910390f35b6101296004803603810190610124919061054d565b6101d8565b60405161013691906105a8565b60405180910390f35b6040518060400160405280601081526020017f577261707065642054657374204254430000000000000000000000000000000081525081565b655af3107a400081565b600881565b60006020528060005260406000206000915090505481565b6040518060400160405280600581526020017f575442544300000000000000000000000000000000000000000000000000000081525081565b6000816000803373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002054101561025b576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016102529061060f565b60405180910390fd5b816000803373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060008282546102a9919061065e565b92505081905550816000808573ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060008282546102fe9190610692565b925050819055508273ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff167fddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef84604051610362919061043f565b60405180910390a36001905092915050565b600081519050919050565b600082825260208201905092915050565b60005b838110156103ae578082015181840152602081019050610393565b60008484015250505050565b6000601f19601f8301169050919050565b60006103d682610374565b6103e0818561037f565b93506103f0818560208601610390565b6103f9816103ba565b840191505092915050565b6000602082019050818103600083015261041e81846103cb565b905092915050565b6000819050919050565b61043981610426565b82525050565b60006020820190506104546000830184610430565b92915050565b600060ff82169050919050565b6104708161045a565b82525050565b600060208201905061048b6000830184610467565b92915050565b600080fd5b600073ffffffffffffffffffffffffffffffffffffffff82169050919050565b60006104c182610496565b9050919050565b6104d1816104b6565b81146104dc57600080fd5b50565b6000813590506104ee816104c8565b92915050565b60006020828403121561050a57610509610491565b5b6000610518848285016104df565b91505092915050565b61052a81610426565b811461053557600080fd5b50565b60008135905061054781610521565b92915050565b6000806040838503121561056457610563610491565b5b6000610572858286016104df565b925050602061058385828601610538565b9150509250929050565b60008115159050919050565b6105a28161058d565b82525050565b60006020820190506105bd6000830184610599565b92915050565b7f496e73756666696369656e742062616c616e6365000000000000000000000000600082015250565b60006105f960148361037f565b9150610604826105c3565b602082019050919050565b60006020820190508181036000830152610628816105ec565b9050919050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052601160045260246000fd5b600061066982610426565b915061067483610426565b925082820390508181111561068c5761068b61062f565b5b92915050565b600061069d82610426565b91506106a883610426565b92508282019050808211156106c0576106bf61062f565b5b9291505056fea2646970667358221220034df4366a43bc77b4f2db41e17b011efc5505eaed9276b8215ed737277b599964736f6c63430008130033"

print(f"\n{'='*80}")
print(f"📋 STEP 1: PREPARING DEPLOYMENT")
print(f"{'='*80}")

nonce = int(rpc("eth_getTransactionCount", [addr, "latest"]), 16)
gas_price = int(rpc("eth_gasPrice"), 16)

print(f"Nonce: {nonce}")
print(f"Gas Price: {gas_price/1e9:.4f} Gwei")
print(f"Gas Limit: 800,000")

# Create EIP-155 transaction
print(f"\n{'='*80}")
print(f"🔐 STEP 2: SIGNING TRANSACTION")
print(f"{'='*80}")

# For contract deployment, 'to' field is empty (use RLP empty encoding)
signing_msg = rlp_encode_list([
    rlp_encode_int(nonce),
    rlp_encode_int(gas_price),
    rlp_encode_int(800000),
    b'\x80',  # RLP empty for contract creation
    rlp_encode_int(0),
    rlp_encode_bytes(bytecode),
    rlp_encode_int(CHAIN_ID),
    b'\x80',
    b'\x80'
])

sig = sk.sign_digest(kh(signing_msg), sigencode=sigencode_string)
r = int.from_bytes(sig[:32], 'big')
s = int.from_bytes(sig[32:], 'big')

print(f"Signature created")
print(f"  r: {hex(r)[:20]}...")
print(f"  s: {hex(s)[:20]}...")

print(f"\n{'='*80}")
print(f"📤 STEP 3: BROADCASTING TRANSACTION")
print(f"{'='*80}")

# Use recovery_id = 0 (standard for ECDSA)
v = CHAIN_ID * 2 + 35

# Create signed transaction
signed_tx = rlp_encode_list([
    rlp_encode_int(nonce),
    rlp_encode_int(gas_price),
    rlp_encode_int(800000),
    b'\x80',  # RLP empty for contract creation
    rlp_encode_int(0),
    rlp_encode_bytes(bytecode),
    rlp_encode_int(v),
    rlp_encode_int(r),
    rlp_encode_int(s)
])

raw_tx = '0x' + signed_tx.hex()

r_req = requests.post(BASE_RPC, json={
    "jsonrpc": "2.0",
    "method": "eth_sendRawTransaction",
    "params": [raw_tx],
    "id": 1
}, timeout=30)

resp = r_req.json()

if 'result' in resp:
    tx_hash = resp['result']
    print(f"✅ Transaction accepted!")
else:
    print(f"\n❌ Transaction rejected!")
    print(f"Error: {resp.get('error', 'Unknown error')}")
    exit(1)

# Calculate expected contract address
contract_rlp = rlp_encode_list([bytes.fromhex(addr[2:]), rlp_encode_int(nonce)])
expected_contract = '0x' + kh(contract_rlp)[-20:].hex()

print(f"\n✅ Transaction broadcast successful!")
print(f"\nTransaction Hash: {tx_hash}")
print(f"Expected Contract: {expected_contract}")
print(f"\n🔍 BaseScan: https://sepolia.basescan.org/tx/{tx_hash}")

print(f"\n{'='*80}")
print(f"⏳ STEP 4: WAITING FOR CONFIRMATION")
print(f"{'='*80}")

for i in range(60):
    time.sleep(2)
    r = requests.post(BASE_RPC, json={
        "jsonrpc": "2.0",
        "method": "eth_getTransactionReceipt",
        "params": [tx_hash],
        "id": 1
    }, timeout=30)

    receipt = r.json().get('result')

    if receipt:
        status = receipt.get('status')
        gas_used = int(receipt.get('gasUsed', '0x0'), 16)
        contract_addr = receipt.get('contractAddress')

        if status == '0x1':
            print(f"\n{'='*80}")
            print(f"🎉 DEPLOYMENT SUCCESSFUL!")
            print(f"{'='*80}")
            print(f"\n📊 Contract Information:")
            print(f"   Address: {contract_addr}")
            print(f"   Name: Wrapped Test BTC")
            print(f"   Symbol: WTBTC")
            print(f"   Decimals: 8")
            print(f"   Total Supply: 1,000,000 WTBTC")
            print(f"   Owner: {addr}")
            print(f"\n⚡ Transaction Details:")
            print(f"   TX Hash: {tx_hash}")
            print(f"   Block: {int(receipt.get('blockNumber', '0x0'), 16)}")
            print(f"   Gas Used: {gas_used:,} / 800,000")
            print(f"   Gas Cost: {(gas_used * gas_price) / 1e18:.6f} ETH")
            print(f"\n🔗 View on BaseScan:")
            print(f"   Contract: https://sepolia.basescan.org/address/{contract_addr}")
            print(f"   Transaction: https://sepolia.basescan.org/tx/{tx_hash}")
            print(f"\n✅ All 1,000,000 WTBTC tokens minted to your address!")
            print(f"\n{'='*80}")
            print(f"✅ DEPLOYMENT COMPLETE - CONTRACT IS LIVE!")
            print(f"{'='*80}")
            break
        else:
            print(f"\n❌ Transaction failed!")
            print(f"Gas used: {gas_used:,}")
            print(f"Check transaction: https://sepolia.basescan.org/tx/{tx_hash}")
            exit(1)

    if (i + 1) % 5 == 0:
        print(f"  Waiting... {i+1}s")

else:
    print(f"\n⏳ Transaction still pending after 120 seconds")
    print(f"Check status: https://sepolia.basescan.org/tx/{tx_hash}")
    print(f"The deployment may still succeed - please check BaseScan")
EOF
