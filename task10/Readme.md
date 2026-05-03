# Task 10: Simple Blockchain Implementation

A functional blockchain prototype built in **Python** featuring Proof-of-Work (PoW), distributed nodes, wallet management, and secure transactions.

---

## Features

- **Proof-of-Work (PoW) Mining**
  - Implements a difficulty-based hashing system.
  - Requires finding a SHA-256 hash with a specific number of leading zeros.

- **Distributed P2P Nodes**
  - Simulates multiple network nodes communicating via sockets.
  - Implements block propagation across the network.

- **Cryptographic Wallets**
  - Generates public/private key pairs for secure identity.
  - Uses digital signatures to verify the authenticity of transactions.

- **Transaction Management**
  - Maintains a "mempool" for pending transactions.
  - Supports miner rewards for successfully added blocks.
  - Validates balances before transaction confirmation.

- **Merkle Trees**
  - Uses Merkle Roots to efficiently verify the integrity of transactions within a block.

---

## Tech Stack

- **Python 3**
- **Hashlib** (SHA-256)
- **Cryptography** (RSA/ECDSA for signatures)
- **Sockets** & **Threading** (for node communication)

---

## Project Workflow

1. **Initialization**: Start multiple nodes, each with its own wallet and local copy of the blockchain.
2. **Transaction Creation**: A user creates a transaction, signs it with their private key, and broadcasts it to the network.
3. **Mempool**: Nodes receive the transaction and add it to their pool of pending transactions.
4. **Mining**: A node selects transactions from the mempool and begins the Proof-of-Work process to create a new block.
5. **Propagation**: Once mined, the block is broadcast to all peers.
6. **Validation**: Peers verify the block's hash, index, and previous hash before adding it to their local chain.

---

## Blockchain Logic

- **Genesis Block**: The hardcoded first block of the chain.
- **Difficulty**: Adjustable parameter that controls how hard it is to mine a block.
- **Verification**: Each block contains the hash of the previous block, creating a cryptographically linked chain.

---

## Installation

```bash
pip install cryptography
python main.py
```
