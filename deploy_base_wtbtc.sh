#!/bin/bash
# Single-command WTBTC deployment to Base Sepolia
# Target recipient: 0x3aAB2285ddcDdaD8edf438C1bAB47e1a9D05a9b4

pip3 install -q ecdsa pycryptodome requests 2>/dev/null; python3 << 'EOF'
import os, json, time, requests
from ecdsa import SigningKey, SECP256k1
from ecdsa.util import sigencode_string
from Crypto.Hash import keccak

BASE_WALLET = "0x3aAB2285ddcDdaD8edf438C1bAB47e1a9D05a9b4"
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
    h = hex(n)[2:]
    if len(h) % 2: h = '0' + h
    b = bytes.fromhex(h)
    if b[0] >= 0x80: return bytes([0x80 + len(b)]) + b
    return b

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

# Load or create wallet
pk = None
if os.path.exists('.env'):
    with open('.env') as f:
        for line in f:
            if '=' in line and not line.strip().startswith('#'):
                k, v = line.strip().split('=', 1)
                if k == 'PRIVATE_KEY':
                    pk = v
                    break

if not pk:
    print("No wallet found in .env. Creating new one...")
    sk = SigningKey.generate(curve=SECP256k1)
    pk = sk.to_string().hex()
    pub = sk.get_verifying_key().to_string()
    addr = '0x' + kh(pub)[-20:].hex()

    with open('.env', 'w') as f:
        f.write(f"PRIVATE_KEY={pk}\n")
        f.write(f"WALLET_ADDRESS={addr}\n")
    print(f"✅ Created new wallet: {addr}")
else:
    sk = SigningKey.from_string(bytes.fromhex(pk), curve=SECP256k1)
    pub = sk.get_verifying_key().to_string()
    addr = '0x' + kh(pub)[-20:].hex()
    print(f"Using existing wallet: {addr}")

# Check balance
bal = int(rpc("eth_getBalance", [addr, "latest"]) or "0x0", 16) / 1e18
print(f"Balance: {bal:.6f} ETH on Base Sepolia")

if bal < 0.001:
    print(f"\n⚠️  NEED BASE SEPOLIA ETH")
    print(f"\n📝 Steps to get testnet ETH:")
    print(f"   1. Go to: https://www.alchemy.com/faucets/base-sepolia")
    print(f"   2. Enter your wallet: {addr}")
    print(f"   3. Get 0.05 ETH (free)")
    print(f"   4. Run this script again")
    print(f"\n   Or use Coinbase Wallet faucet:")
    print(f"   https://portal.cdp.coinbase.com/products/faucet")
    exit(1)

# Deploy WTBTC contract
print("\n" + "="*80)
print("🚀 Deploying WTBTC Contract to Base Sepolia")
print("="*80)

bytecode = "0x608060405234801561001057600080fd5b50620f424060008033600073ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020819055503373ffffffffffffffffffffffffffffffffffffffff16600073ffffffffffffffffffffffffffffffffffffffff167fddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef620f42406040518082815260200191505060405180910390a361034f806100c16000396000f3fe608060405234801561001057600080fd5b50600436106100575760003560e01c806318160ddd1461005c57806370a082311461007a57806395d89b41146100b0578063a9059cbb146100ce578063dd62ed3e14610132575b600080fd5b610064610162565b6040518082815260200191505060405180910390f35b6100a66004803603602081101561009057600080fd5b8101908080359060200190929190505050610168565b6040518082815260200191505060405180910390f35b6100b8610180565b6040518082815260200191505060405180910390f35b61011a600480360360408110156100e457600080fd5b81019080803573ffffffffffffffffffffffffffffffffffffffff16906020019092919080359060200190929190505050610186565b60405180821515815260200191505060405180910390f35b61014c6004803603604081101561014857600080fd5b8101908080359060200190929190803590602001909291905050506102e5565b6040518082815260200191505060405180910390f35b620f424081565b60006020528060005260406000206000915090505481565b60085481565b60008060003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002054821115156101d457600080fd5b8160008060003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020600082825403925050819055508160008060008673ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020600082825401925050819055508373ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff167fddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef846040518082815260200191505060405180910390a3600190509392505050565b600160209190910260409081526000928352918190205490915056fea26469706673582212203c3e3e9c2f2e2f2f2f2f2f2f2f2f2f2f2f2f2f2f2f2f2f2f2f2f2f2f2f2f2f64736f6c63430007060033"

n = int(rpc("eth_getTransactionCount", [addr, "latest"]), 16)
gp = int(rpc("eth_gasPrice"), 16)

print(f"Gas price: {gp / 1e9:.2f} Gwei")
print(f"Nonce: {n}")

# Create deployment transaction with 2M gas
rlp = el([ei(n), ei(gp), ei(2000000), b'\x80', ei(0), eb(bytecode), ei(CHAIN_ID), b'\x80', b'\x80'])
sig = sk.sign_digest(kh(rlp), sigencode=sigencode_string)
r, s = int.from_bytes(sig[:32], 'big'), int.from_bytes(sig[32:], 'big')
v = 35 + CHAIN_ID * 2

signed = el([ei(n), ei(gp), ei(2000000), b'\x80', ei(0), eb(bytecode), ei(v), ei(r), ei(s)])
tx_hash = rpc("eth_sendRawTransaction", ['0x' + signed.hex()])

if not tx_hash:
    print("❌ Failed to send deployment transaction")
    exit(1)

print(f"\n✅ Deployment TX sent: {tx_hash}")
print(f"🔍 BaseScan: https://sepolia.basescan.org/tx/{tx_hash}")

# Calculate contract address
contract_rlp = el([bytes.fromhex(addr[2:]), ei(n)])
contract_addr = '0x' + kh(contract_rlp)[-20:].hex()
print(f"📋 Expected contract: {contract_addr}")

print(f"\n⏳ Waiting for confirmation (up to 2 minutes)...")
for i in range(60):
    time.sleep(2)
    receipt = rpc("eth_getTransactionReceipt", [tx_hash])
    if receipt:
        status = receipt.get('status')
        gas_used = int(receipt.get('gasUsed', '0x0'), 16)

        if status == '0x1':
            print(f"\n✅ CONTRACT DEPLOYED SUCCESSFULLY!")
            actual_contract = receipt.get('contractAddress')
            print(f"📍 Contract: {actual_contract}")
            print(f"⛽ Gas used: {gas_used:,}")

            # Transfer 500,000 WTBTC
            print(f"\n{'='*80}")
            print(f"💸 Transferring 500,000 WTBTC to {BASE_WALLET}")
            print(f"{'='*80}")

            to_addr = BASE_WALLET[2:].zfill(64)
            amount = hex(500000 * 10**8)[2:].zfill(64)
            data = "0xa9059cbb" + to_addr + amount

            n2 = int(rpc("eth_getTransactionCount", [addr, "latest"]), 16)
            gp2 = int(rpc("eth_gasPrice"), 16)

            rlp2 = el([ei(n2), ei(gp2), ei(100000), bytes.fromhex(actual_contract[2:]), ei(0), eb(data), ei(CHAIN_ID), b'\x80', b'\x80'])
            sig2 = sk.sign_digest(kh(rlp2), sigencode=sigencode_string)
            r2, s2 = int.from_bytes(sig2[:32], 'big'), int.from_bytes(sig2[32:], 'big')
            v2 = 35 + CHAIN_ID * 2

            signed2 = el([ei(n2), ei(gp2), ei(100000), bytes.fromhex(actual_contract[2:]), ei(0), eb(data), ei(v2), ei(r2), ei(s2)])
            tx_hash2 = rpc("eth_sendRawTransaction", ['0x' + signed2.hex()])

            if tx_hash2:
                print(f"✅ Transfer TX sent: {tx_hash2}")
                print(f"🔍 BaseScan: https://sepolia.basescan.org/tx/{tx_hash2}")

                print(f"\n⏳ Waiting for transfer confirmation...")
                for j in range(30):
                    time.sleep(2)
                    receipt2 = rpc("eth_getTransactionReceipt", [tx_hash2])
                    if receipt2 and receipt2.get('status') == '0x1':
                        print(f"\n{'='*80}")
                        print(f"🎉 DEPLOYMENT COMPLETE!")
                        print(f"{'='*80}")
                        print(f"\n📊 Summary:")
                        print(f"   Contract: {actual_contract}")
                        print(f"   Recipient: {BASE_WALLET}")
                        print(f"   Amount: 500,000 WTBTC")
                        print(f"\n🔗 Links:")
                        print(f"   Contract: https://sepolia.basescan.org/address/{actual_contract}")
                        print(f"   Recipient: https://sepolia.basescan.org/address/{BASE_WALLET}")
                        break
                else:
                    print("⏳ Transfer still pending...")
            else:
                print("❌ Transfer failed to send")
            break
        else:
            print(f"\n❌ DEPLOYMENT FAILED")
            print(f"Gas used: {gas_used:,} / 2,000,000")
            print(f"Transaction reverted")
        break

    if (i+1) % 10 == 0:
        print(f"  Still waiting... ({i+1}s)")
else:
    print("\n⏳ Transaction still pending after 2 minutes")
    print(f"Check status: https://sepolia.basescan.org/tx/{tx_hash}")
EOF
