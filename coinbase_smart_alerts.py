#!/usr/bin/env python3
"""
Coinbase Cloud Smart Alerts
Automated alerts for wallet activity, price changes, and contract events
"""

import json
import time
import requests
from datetime import datetime
from pathlib import Path

# Coinbase Cloud Configuration (⚠️ EXPOSED - REVOKE IMMEDIATELY)
COINBASE_PROJECT_ID = "92d85142-1115-49df-8eab-9177ae50693b"
COINBASE_API_KEY = "09uwnC3SBAm2eg99nHSVr08g1ud8Fq1mJvhNpHebJDFuFKO1E+2ndIffRHQ2Bc+PF8pQnduo535va6kvOmSR2Q=="

POLYGON_RPC = f"https://api.developer.coinbase.com/rpc/v1/polygon-amoy/{COINBASE_PROJECT_ID}"

# Alert Configuration
ALERTS = {
    "low_balance": {
        "enabled": True,
        "threshold": 0.01,  # Alert if MATIC < 0.01
        "wallets": [
            "0xD34beE1C52D05798BD1925318dF8d3292d0e49E6",
            "0xC4f7BaFDC2f7036B5e4Da73B0E77BBe0f0157145"
        ]
    },
    "new_transaction": {
        "enabled": True,
        "wallets": [
            "0xD34beE1C52D05798BD1925318dF8d3292d0e49E6"
        ]
    },
    "wtbtc_transfer": {
        "enabled": True,
        "contract": None  # Will be loaded from deployment
    }
}

class AlertSystem:
    def __init__(self):
        self.last_balances = {}
        self.last_tx_counts = {}
        self.alerts_sent = []

    def rpc_call(self, method, params=[]):
        """Make Coinbase Cloud RPC call"""
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {COINBASE_API_KEY}"
        }

        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "id": 1
        }

        try:
            response = requests.post(POLYGON_RPC, json=payload, headers=headers, timeout=10)
            return response.json().get("result")
        except:
            return None

    def get_balance(self, address):
        """Get MATIC balance"""
        result = self.rpc_call("eth_getBalance", [address, "latest"])
        if result:
            return int(result, 16) / 10**18
        return 0

    def get_tx_count(self, address):
        """Get transaction count"""
        result = self.rpc_call("eth_getTransactionCount", [address, "latest"])
        if result:
            return int(result, 16)
        return 0

    def send_alert(self, alert_type, message, data=None):
        """Send alert (console + log)"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        alert = {
            "timestamp": timestamp,
            "type": alert_type,
            "message": message,
            "data": data or {}
        }

        # Console output
        print()
        print("🚨" * 40)
        print(f"⚠️  ALERT: {alert_type.upper()}")
        print(f"🕐 Time: {timestamp}")
        print(f"📝 {message}")
        if data:
            print(f"📊 Data: {json.dumps(data, indent=2)}")
        print("🚨" * 40)
        print()

        # Save to log
        with open('alerts.jsonl', 'a') as f:
            f.write(json.dumps(alert) + '\n')

        self.alerts_sent.append(alert)

    def check_low_balance(self):
        """Check for low balance alerts"""
        if not ALERTS['low_balance']['enabled']:
            return

        for wallet in ALERTS['low_balance']['wallets']:
            balance = self.get_balance(wallet)

            if balance < ALERTS['low_balance']['threshold']:
                # Only alert once unless balance changes
                key = f"low_balance_{wallet}"
                if key not in self.last_balances or self.last_balances[key] != balance:
                    self.send_alert(
                        "low_balance",
                        f"Low balance detected: {balance:.6f} MATIC",
                        {
                            "wallet": wallet,
                            "balance": balance,
                            "threshold": ALERTS['low_balance']['threshold']
                        }
                    )
                    self.last_balances[key] = balance

    def check_new_transactions(self):
        """Check for new transactions"""
        if not ALERTS['new_transaction']['enabled']:
            return

        for wallet in ALERTS['new_transaction']['wallets']:
            tx_count = self.get_tx_count(wallet)

            if wallet in self.last_tx_counts:
                if tx_count > self.last_tx_counts[wallet]:
                    new_txs = tx_count - self.last_tx_counts[wallet]
                    self.send_alert(
                        "new_transaction",
                        f"{new_txs} new transaction(s) detected",
                        {
                            "wallet": wallet,
                            "new_count": tx_count,
                            "previous_count": self.last_tx_counts[wallet],
                            "explorer": f"https://amoy.polygonscan.com/address/{wallet}"
                        }
                    )

            self.last_tx_counts[wallet] = tx_count

    def run(self, interval=30):
        """Run alert system"""
        print("=" * 80)
        print("🚨 Coinbase Cloud Smart Alert System")
        print("=" * 80)
        print()
        print("⚠️  WARNING: API credentials exposed publicly - REVOKE IMMEDIATELY")
        print("   https://portal.cdp.coinbase.com/")
        print()

        # Load WTBTC contract if available
        if Path('wtbtc_deployment_success.json').exists():
            with open('wtbtc_deployment_success.json') as f:
                deployment = json.load(f)
                ALERTS['wtbtc_transfer']['contract'] = deployment.get('contract')
                print(f"✅ Loaded WTBTC contract: {ALERTS['wtbtc_transfer']['contract']}")

        print()
        print("📡 Active Alerts:")
        for alert_type, config in ALERTS.items():
            if config.get('enabled'):
                print(f"   ✅ {alert_type}")
        print()
        print(f"⏱️  Checking every {interval} seconds")
        print()
        print("-" * 80)

        try:
            while True:
                self.check_low_balance()
                self.check_new_transactions()

                time.sleep(interval)

        except KeyboardInterrupt:
            print()
            print("=" * 80)
            print("Alert system stopped")
            print(f"Total alerts sent: {len(self.alerts_sent)}")
            print("=" * 80)

if __name__ == "__main__":
    alert_system = AlertSystem()
    alert_system.run(interval=30)
