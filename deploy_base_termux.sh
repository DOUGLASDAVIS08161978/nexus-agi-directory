#!/bin/bash
# WTBTC Deployment for Base Sepolia (Termux Compatible)
# Deployer: 0x9FE74D9D6f1Ae0Ce1fb3B51d4a82c05b74e280f3

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

def ei(n):
    if n == 0: return b'\x80'
    # Convert to bytes, removing leading zeros
    b = n.to_bytes((n.bit_length() + 7) // 8, 'big')
    if len(b) == 0: return b'\x80'
    if len(b) == 1 and b[0] < 0x80: return b
    return bytes([0x80 + len(b)]) + b

def eb(v):
    if isinstance(v, str):
        v = bytes.fromhex(v[2:] if v.startswith('0x') else v) if v else b''
    if len(v) == 0: return b'\x80'
    if len(v) == 1 and v[0] < 0x80: return v
    if len(v) <= 55: return bytes([0x80 + len(v)]) + v
    lb = len(v).to_bytes((len(v).bit_length() + 7) // 8, 'big')
    return bytes([0xb7 + len(lb)]) + lb + v

def el(items):
    enc = b''.join(items)
    if len(enc) <= 55: return bytes([0xc0 + len(enc)]) + enc
    lb = len(enc).to_bytes((len(enc).bit_length() + 7) // 8, 'big')
    return bytes([0xf7 + len(lb)]) + lb + enc

sk = SigningKey.from_string(bytes.fromhex(PRIVATE_KEY), curve=SECP256k1)
pub = sk.get_verifying_key().to_string()
addr = '0x' + kh(pub)[-20:].hex()

print("="*80)
print("🚀 WTBTC DEPLOYMENT TO BASE SEPOLIA")
print("="*80)
print(f"\nDeployer: {addr}")

bal = int(rpc("eth_getBalance", [addr, "latest"]) or "0x0", 16) / 1e18
print(f"Balance: {bal:.6f} ETH\n")

if bal < 0.0008:
    print("⚠️  Need more testnet ETH")
    print(f"Get from: https://www.alchemy.com/faucets/base-sepolia")
    print(f"Send to: {addr}")
    exit(1)

# Pre-compiled WTBTC bytecode (from successful deployment at 0x465bab589E344e7e48e2E072A677dADeF5EE8b31)
# Contract: 1,000,000 WTBTC total supply, decimals=8
bytecode = "0x608060405234801561001057600080fd5b50655af3107a40006000803373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020819055503373ffffffffffffffffffffffffffffffffffffffff16600073ffffffffffffffffffffffffffffffffffffffff167fddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef655af3107a40006040516100be91906100e4565b60405180910390a36100ff565b6000819050919050565b6100de816100cb565b82525050565b60006020820190506100f960008301846100d5565b92915050565b6106fc8061010e6000396000f3fe608060405234801561001057600080fd5b50600436106100625760003560e01c806306fdde031461006757806318160ddd14610085578063313ce567146100a357806370a08231146100c157806395d89b41146100f1578063a9059cbb1461010f575b600080fd5b61006f61013f565b60405161007c9190610404565b60405180910390f35b61008d610178565b60405161009a919061043f565b60405180910390f35b6100ab610182565b6040516100b89190610476565b60405180910390f35b6100db60048036038101906100d691906104f4565b610187565b6040516100e8919061043f565b60405180910390f35b6100f961019f565b6040516101069190610404565b60405180910390f35b6101296004803603810190610124919061054d565b6101d8565b60405161013691906105a8565b60405180910390f35b6040518060400160405280601081526020017f577261707065642054657374204254430000000000000000000000000000000081525081565b655af3107a400081565b600881565b60006020528060005260406000206000915090505481565b6040518060400160405280600581526020017f575442544300000000000000000000000000000000000000000000000000000081525081565b6000816000803373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002054101561025b576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016102529061060f565b60405180910390fd5b816000803373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060008282546102a9919061065e565b92505081905550816000808573ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060008282546102fe9190610692565b925050819055508273ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff167fddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef84604051610362919061043f565b60405180910390a36001905092915050565b600081519050919050565b600082825260208201905092915050565b60005b838110156103ae578082015181840152602081019050610393565b60008484015250505050565b6000601f19601f8301169050919050565b60006103d682610374565b6103e0818561037f565b93506103f0818560208601610390565b6103f9816103ba565b840191505092915050565b6000602082019050818103600083015261041e81846103cb565b905092915050565b6000819050919050565b61043981610426565b82525050565b60006020820190506104546000830184610430565b92915050565b600060ff82169050919050565b6104708161045a565b82525050565b600060208201905061048b6000830184610467565b92915050565b600080fd5b600073ffffffffffffffffffffffffffffffffffffffff82169050919050565b60006104c182610496565b9050919050565b6104d1816104b6565b81146104dc57600080fd5b50565b6000813590506104ee816104c8565b92915050565b60006020828403121561050a57610509610491565b5b6000610518848285016104df565b91505092915050565b61052a81610426565b811461053557600080fd5b50565b60008135905061054781610521565b92915050565b6000806040838503121561056457610563610491565b5b6000610572858286016104df565b925050602061058385828601610538565b9150509250929050565b60008115159050919050565b6105a28161058d565b82525050565b60006020820190506105bd6000830184610599565b92915050565b7f496e73756666696369656e742062616c616e6365000000000000000000000000600082015250565b60006105f960148361037f565b9150610604826105c3565b602082019050919050565b60006020820190508181036000830152610628816105ec565b9050919050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052601160045260246000fd5b600061066982610426565b915061067483610426565b925082820390508181111561068c5761068b61062f565b5b92915050565b600061069d82610426565b91506106a883610426565b92508282019050808211156106c0576106bf61062f565b5b9291505056fea2646970667358221220034df4366a43bc77b4f2db41e17b011efc5505eaed9276b8215ed737277b599964736f6c63430008130033"

n = int(rpc("eth_getTransactionCount", [addr, "latest"]), 16)
gp = int(rpc("eth_gasPrice"), 16)

print(f"Deploying WTBTC contract...")
print(f"Gas Price: {gp/1e9:.4f} Gwei")

# Sign deployment with EIP-155
signing_rlp = el([ei(n), ei(gp), ei(800000), b'', ei(0), eb(bytecode), ei(CHAIN_ID), b'', b''])
sig = sk.sign_digest(kh(signing_rlp), sigencode=sigencode_string)
r, s = int.from_bytes(sig[:32], 'big'), int.from_bytes(sig[32:], 'big')
v = 35 + CHAIN_ID * 2

signed_tx = el([ei(n), ei(gp), ei(800000), b'\x80', ei(0), eb(bytecode), ei(v), ei(r), ei(s)])

r = requests.post(BASE_RPC, json={"jsonrpc": "2.0", "method": "eth_sendRawTransaction", "params": ['0x' + signed_tx.hex()], "id": 1})
resp = r.json()

if 'error' in resp:
    print(f"❌ Error: {resp['error']}")
    exit(1)

tx_hash = resp['result']
print(f"\n✅ TX: {tx_hash}")
print(f"🔍 https://sepolia.basescan.org/tx/{tx_hash}\n")

# Calculate contract address
contract_rlp = el([bytes.fromhex(addr[2:]), ei(n)])
contract = '0x' + kh(contract_rlp)[-20:].hex()

print("⏳ Waiting for confirmation...")
for i in range(60):
    time.sleep(2)
    r = requests.post(BASE_RPC, json={"jsonrpc": "2.0", "method": "eth_getTransactionReceipt", "params": [tx_hash], "id": 1})
    receipt = r.json().get('result')

    if receipt and receipt.get('status') == '0x1':
        deployed = receipt['contractAddress']
        gas = int(receipt['gasUsed'], 16)

        print(f"\n{'='*80}")
        print(f"🎉 DEPLOYMENT SUCCESSFUL!")
        print(f"{'='*80}")
        print(f"\n📊 Contract Details:")
        print(f"   Address: {deployed}")
        print(f"   Symbol: WTBTC")
        print(f"   Decimals: 8")
        print(f"   Total Supply: 1,000,000 WTBTC")
        print(f"   Owner: {addr}")
        print(f"   Gas Used: {gas:,}")
        print(f"\n🔗 BaseScan:")
        print(f"   https://sepolia.basescan.org/address/{deployed}")
        print(f"\n✅ All tokens minted to your address!")
        break

    if receipt and receipt.get('status') == '0x0':
        print(f"❌ Deployment failed")
        break

    if (i+1) % 10 == 0:
        print(f"  {i+1}s...")
else:
    print("\n⏳ Still pending - check BaseScan for status")
EOF
