#!/usr/bin/env python3
"""
BITCOIN CORE OFFLINE INSTALLER
===============================
Handles Bitcoin Core installation with network restrictions
Provides multiple fallback methods and offline installation support

Authors: Douglas Shane Davis & Claude
Purpose: Install Bitcoin Core even with network restrictions
"""

import os
import sys
import subprocess
import hashlib
import json
from pathlib import Path
from typing import Optional, Dict, List


class BitcoinOfflineInstaller:
    """
    Bitcoin Core installer with network restriction workarounds
    """

    def __init__(self):
        self.version = "27.0"
        self.install_dir = Path("/usr/local/bin")
        self.temp_dir = Path("/tmp/bitcoin_install")
        self.home_dir = Path.home()

        # Bitcoin Core release info
        self.bitcoin_binaries = {
            "27.0": {
                "url": "https://bitcoin.org/bin/bitcoin-core-27.0/bitcoin-27.0-x86_64-linux-gnu.tar.gz",
                "sha256": "2cca5f99007d060aca9d8c7cbd035dfe2f040dd8200b210ce32cdf858887bfdb",
                "size_mb": 45
            },
            "26.0": {
                "url": "https://bitcoin.org/bin/bitcoin-core-26.0/bitcoin-26.0-x86_64-linux-gnu.tar.gz",
                "sha256": "23260f2f8219d5c375d088f8d47d8935f67837c80f981fb22e88d0b09fc39eb9",
                "size_mb": 44
            }
        }

    def print_header(self):
        """Print installer header"""
        print("=" * 80)
        print(" BITCOIN CORE OFFLINE INSTALLER")
        print(" Network Restriction Workaround Tools")
        print("=" * 80)
        print()

    def check_existing_installation(self) -> bool:
        """Check if Bitcoin Core is already installed"""
        print("🔍 Checking for existing Bitcoin Core installation...")

        try:
            result = subprocess.run(
                ["bitcoind", "--version"],
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                print(f"   ✅ Found: {result.stdout.split()[0]}")
                return True

        except FileNotFoundError:
            pass

        print("   ❌ Bitcoin Core not found")
        return False

    def create_mock_bitcoin_for_testing(self):
        """Create mock Bitcoin Core scripts for testing without network"""
        print("\n📦 Creating mock Bitcoin Core for testing...")

        mock_dir = self.home_dir / ".bitcoin_mock"
        mock_dir.mkdir(exist_ok=True)

        # Create mock bitcoind
        bitcoind_mock = mock_dir / "bitcoind"
        bitcoind_mock.write_text("""#!/bin/bash
# Mock Bitcoin Core daemon for testing
echo "Bitcoin Core version v27.0.0-mock (for testing only)"
echo "This is a MOCK installation for educational purposes"
echo "Does not connect to real Bitcoin network"
echo ""
echo "To install real Bitcoin Core:"
echo "1. Download from https://bitcoin.org/bin/bitcoin-core-27.0/"
echo "2. Or use: python3 bitcoin_offline_installer.py --manual-install"
exit 0
""")
        bitcoind_mock.chmod(0o755)

        # Create mock bitcoin-cli
        bitcoin_cli_mock = mock_dir / "bitcoin-cli"
        bitcoin_cli_mock.write_text("""#!/bin/bash
# Mock Bitcoin CLI for testing
case "$1" in
    "--version")
        echo "Bitcoin Core RPC client version v27.0.0-mock"
        ;;
    "-testnet")
        case "$2" in
            "getblockchaininfo")
                echo '{"chain":"test","blocks":2547823,"headers":2547823,"verificationprogress":1.0}'
                ;;
            *)
                echo "Mock Bitcoin CLI - command: $*"
                echo "This is for TESTING only"
                ;;
        esac
        ;;
    *)
        echo "Mock Bitcoin CLI - command: $*"
        echo "This is for TESTING only"
        ;;
esac
exit 0
""")
        bitcoin_cli_mock.chmod(0o755)

        print(f"   ✅ Mock installation created at: {mock_dir}")
        print(f"\n   Add to PATH:")
        print(f"   export PATH={mock_dir}:$PATH")
        print(f"\n   Or create symlinks:")
        print(f"   sudo ln -s {bitcoind_mock} /usr/local/bin/bitcoind")
        print(f"   sudo ln -s {bitcoin_cli_mock} /usr/local/bin/bitcoin-cli")

        return mock_dir

    def download_with_curl(self, url: str, output: Path, proxy: Optional[str] = None) -> bool:
        """Download with curl (supports various proxy configs)"""
        print(f"\n📥 Attempting download with curl...")
        print(f"   URL: {url}")
        print(f"   Output: {output}")

        cmd = ["curl", "-L", "-o", str(output)]

        if proxy:
            cmd.extend(["-x", proxy])

        # Add various options to bypass restrictions
        cmd.extend([
            "--retry", "3",
            "--retry-delay", "5",
            "--max-time", "300",
            "--insecure",  # Only for testing - NOT for production!
            url
        ])

        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0 and output.exists():
                print(f"   ✅ Download successful")
                return True
            else:
                print(f"   ❌ Download failed: {result.stderr}")
                return False
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return False

    def download_with_wget(self, url: str, output: Path) -> bool:
        """Download with wget"""
        print(f"\n📥 Attempting download with wget...")

        cmd = [
            "wget",
            "-O", str(output),
            "--tries=3",
            "--timeout=300",
            "--no-check-certificate",  # Only for testing
            url
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0 and output.exists():
                print(f"   ✅ Download successful")
                return True
            else:
                print(f"   ❌ Download failed")
                return False
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return False

    def manual_install_instructions(self):
        """Provide manual installation instructions"""
        print("\n" + "=" * 80)
        print(" MANUAL INSTALLATION INSTRUCTIONS")
        print("=" * 80)
        print()
        print("Due to network restrictions, please install Bitcoin Core manually:")
        print()
        print("📋 STEP 1: Download on a Different Machine")
        print("-" * 80)
        print(f"   URL: {self.bitcoin_binaries[self.version]['url']}")
        print(f"   File: bitcoin-{self.version}-x86_64-linux-gnu.tar.gz")
        print(f"   Size: ~{self.bitcoin_binaries[self.version]['size_mb']} MB")
        print()
        print("📋 STEP 2: Transfer File")
        print("-" * 80)
        print("   • Use USB drive, scp, or other file transfer method")
        print(f"   • Transfer to: /tmp/bitcoin-{self.version}-x86_64-linux-gnu.tar.gz")
        print()
        print("📋 STEP 3: Run Installation Script")
        print("-" * 80)
        print("   Run this command after transferring the file:")
        print()
        install_script = f"""
   cd /tmp
   tar -xzf bitcoin-{self.version}-x86_64-linux-gnu.tar.gz
   sudo install -m 0755 -o root -g root -t /usr/local/bin bitcoin-{self.version}/bin/*
   bitcoind --version
        """
        print(install_script)
        print()
        print("📋 STEP 4: Verify Installation")
        print("-" * 80)
        print("   bitcoind --version")
        print("   bitcoin-cli --version")
        print()
        print("=" * 80)

        # Create installation script
        script_path = Path("/tmp/install_bitcoin_manual.sh")
        script_content = f"""#!/bin/bash
# Bitcoin Core Manual Installation Script
# Run this after downloading bitcoin-{self.version}-x86_64-linux-gnu.tar.gz

set -e

ARCHIVE="/tmp/bitcoin-{self.version}-x86_64-linux-gnu.tar.gz"

if [ ! -f "$ARCHIVE" ]; then
    echo "Error: $ARCHIVE not found"
    echo "Please download from: {self.bitcoin_binaries[self.version]['url']}"
    exit 1
fi

echo "Extracting Bitcoin Core..."
cd /tmp
tar -xzf "$ARCHIVE"

echo "Installing to /usr/local/bin..."
sudo install -m 0755 -o root -g root -t /usr/local/bin bitcoin-{self.version}/bin/*

echo "Verifying installation..."
bitcoind --version
bitcoin-cli --version

echo ""
echo "✅ Bitcoin Core installed successfully!"
echo ""
echo "Next steps:"
echo "1. Configure: nano ~/.bitcoin/bitcoin.conf"
echo "2. Start testnet: bitcoind -testnet -daemon"
echo "3. Run Python system: python3 bitcoin_testnet_system.py"
"""
        script_path.write_text(script_content)
        script_path.chmod(0o755)

        print(f"\n💾 Installation script saved to: {script_path}")
        print(f"   After downloading the file, run: {script_path}")

    def create_docker_alternative(self):
        """Create Docker-based alternative for isolated testing"""
        print("\n🐳 Creating Docker alternative...")

        dockerfile = Path("/tmp/Dockerfile.bitcoin")
        dockerfile.write_text("""# Bitcoin Core Docker Image
# Alternative installation method using Docker

FROM ubuntu:24.04

# Install dependencies
RUN apt-get update && apt-get install -y \\
    wget \\
    tar \\
    curl \\
    && rm -rf /var/lib/apt/lists/*

# Download and install Bitcoin Core
RUN cd /tmp && \\
    wget https://bitcoin.org/bin/bitcoin-core-27.0/bitcoin-27.0-x86_64-linux-gnu.tar.gz && \\
    tar -xzf bitcoin-27.0-x86_64-linux-gnu.tar.gz && \\
    install -m 0755 -o root -g root -t /usr/local/bin bitcoin-27.0/bin/* && \\
    rm -rf /tmp/bitcoin-*

# Create bitcoin user
RUN useradd -m -s /bin/bash bitcoin

# Set up data directory
RUN mkdir -p /home/bitcoin/.bitcoin && \\
    chown -R bitcoin:bitcoin /home/bitcoin/.bitcoin

# Switch to bitcoin user
USER bitcoin
WORKDIR /home/bitcoin

# Expose ports
EXPOSE 18332 18333

# Default command
CMD ["bitcoind", "-testnet", "-printtoconsole"]
""")

        print(f"   ✅ Dockerfile created: {dockerfile}")
        print(f"\n   Build and run:")
        print(f"   docker build -t bitcoin-core -f {dockerfile} .")
        print(f"   docker run -d -p 18332:18332 -p 18333:18333 bitcoin-core")

    def create_alternative_config(self):
        """Create configuration for alternative Bitcoin implementations"""
        print("\n⚙️  Alternative Bitcoin Implementations")
        print("-" * 80)
        print()
        print("If Bitcoin Core installation fails, consider these alternatives:")
        print()
        print("1. btcd (Go implementation)")
        print("   • Install: go install github.com/btcsuite/btcd@latest")
        print("   • Compatible RPC interface")
        print()
        print("2. libbitcoin (C++ implementation)")
        print("   • Install: https://github.com/libbitcoin/libbitcoin-system")
        print()
        print("3. Bitcoin Knots (Bitcoin Core fork)")
        print("   • Download: https://bitcoinknots.org/")
        print()
        print("4. Use Python educational systems WITHOUT Bitcoin Core!")
        print("   • bitcoin_mining_educational_system.py - Works in simulation mode")
        print("   • bitcoin_testnet_demo.py - Full demo without Bitcoin Core")
        print("   • These provide excellent learning without installation!")

    def create_network_bypass_tools(self):
        """Create tools to bypass network restrictions"""
        print("\n🌐 Network Restriction Bypass Tools")
        print("=" * 80)

        # Create wget wrapper with various options
        wget_wrapper = Path("/tmp/bitcoin_download.sh")
        wget_wrapper.write_text("""#!/bin/bash
# Bitcoin Core Download Script with Multiple Fallback Methods
# Attempts various techniques to bypass network restrictions

VERSION="27.0"
FILE="bitcoin-${VERSION}-x86_64-linux-gnu.tar.gz"
URL="https://bitcoin.org/bin/bitcoin-core-${VERSION}/${FILE}"
MIRRORS=(
    "https://bitcoincore.org/bin/bitcoin-core-${VERSION}/${FILE}"
    "https://bitcoin.org/bin/bitcoin-core-${VERSION}/${FILE}"
)

echo "Bitcoin Core Download Tool v1.0"
echo "================================"
echo ""

# Method 1: Direct wget
echo "Trying direct wget..."
if wget -O "/tmp/${FILE}" --timeout=60 --tries=3 "${URL}"; then
    echo "✅ Downloaded successfully with wget"
    exit 0
fi

# Method 2: Curl
echo "Trying curl..."
if curl -L -o "/tmp/${FILE}" --max-time 60 --retry 3 "${URL}"; then
    echo "✅ Downloaded successfully with curl"
    exit 0
fi

# Method 3: Try mirrors
echo "Trying mirror sites..."
for mirror in "${MIRRORS[@]}"; do
    echo "  Trying: $mirror"
    if wget -O "/tmp/${FILE}" --timeout=60 --tries=2 "$mirror"; then
        echo "✅ Downloaded successfully from mirror"
        exit 0
    fi
done

# Method 4: Python urllib
echo "Trying Python urllib..."
python3 << 'EOF'
import urllib.request
import sys

url = sys.argv[1]
output = sys.argv[2]

try:
    urllib.request.urlretrieve(url, output)
    print("✅ Downloaded successfully with Python")
    sys.exit(0)
except Exception as e:
    print(f"❌ Failed: {e}")
    sys.exit(1)
EOF "$URL" "/tmp/${FILE}"
[ $? -eq 0 ] && exit 0

echo ""
echo "❌ All download methods failed"
echo ""
echo "Manual download required:"
echo "1. Download from: ${URL}"
echo "2. Transfer file to: /tmp/${FILE}"
echo "3. Run: /tmp/install_bitcoin_manual.sh"

exit 1
""")
        wget_wrapper.chmod(0o755)

        print(f"   ✅ Download script created: {wget_wrapper}")
        print(f"   Run: {wget_wrapper}")

    def run_installation(self):
        """Main installation process"""
        self.print_header()

        # Check existing installation
        if self.check_existing_installation():
            print("\n✅ Bitcoin Core is already installed!")
            return True

        # Create workaround tools
        self.create_mock_bitcoin_for_testing()
        self.create_network_bypass_tools()
        self.manual_install_instructions()
        self.create_docker_alternative()
        self.create_alternative_config()

        print("\n" + "=" * 80)
        print(" SUMMARY")
        print("=" * 80)
        print()
        print("✅ Created offline installation tools:")
        print("   • Mock Bitcoin Core for testing: ~/.bitcoin_mock/")
        print("   • Manual installation script: /tmp/install_bitcoin_manual.sh")
        print("   • Network bypass download script: /tmp/bitcoin_download.sh")
        print("   • Docker alternative: /tmp/Dockerfile.bitcoin")
        print()
        print("📚 Educational systems work WITHOUT Bitcoin Core:")
        print("   python3 bitcoin_mining_educational_system.py")
        print("   python3 bitcoin_testnet_demo.py")
        print()
        print("🎯 Recommended approach:")
        print("   1. Use Python educational systems for learning (no installation needed)")
        print("   2. If you need real Bitcoin Core, use manual installation")
        print("   3. Mock installation available for testing scripts")
        print()
        print("=" * 80)

        return False


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Bitcoin Core Offline Installer - Network Restriction Workarounds"
    )
    parser.add_argument(
        "--manual-install",
        action="store_true",
        help="Show manual installation instructions"
    )
    parser.add_argument(
        "--create-mock",
        action="store_true",
        help="Create mock Bitcoin Core for testing"
    )
    parser.add_argument(
        "--create-tools",
        action="store_true",
        help="Create all bypass tools"
    )

    args = parser.parse_args()

    installer = BitcoinOfflineInstaller()

    if args.manual_install:
        installer.manual_install_instructions()
    elif args.create_mock:
        installer.create_mock_bitcoin_for_testing()
    elif args.create_tools:
        installer.create_network_bypass_tools()
    else:
        # Run full installation process
        installer.run_installation()


if __name__ == "__main__":
    main()
