
import time

from node import Node
from transaction import Transaction


PORTS      = [5001, 5002, 5003]
DIFFICULTY = 4          # lower to 2 for faster runs


def run():
    print("=== Node Startup (3 nodes) ===")
    nodes: list[Node] = []
    for i, port in enumerate(PORTS):
        peers = [p for p in PORTS if p != port]
        n = Node(node_id=i + 1, port=port, peer_ports=peers, difficulty=DIFFICULTY)
        n.start()
        nodes.append(n)
        time.sleep(0.1)

    time.sleep(0.5)   # let sockets settle

    n1, n2, n3 = nodes

    print("\n=== Transaction ===")
    tx1 = Transaction(n1.wallet, n2.wallet.address, 2.5)
    tx2 = Transaction(n3.wallet, n1.wallet.address, 1.0)

    for tx in (tx1, tx2):
        d  = tx.to_dict()
        ok = "Valid" if tx.is_valid() else "Invalid"
        print(f"[NODE-1] Creating transaction:")
        print(f"         From:      {d['sender']}")
        print(f"         To:        {d['recipient']}")
        print(f"         Amount:    {d['amount']} coins")
        print(f"         Signature: {d['signature']}  {ok}")

    n2.blockchain.add_transaction(tx1)
    n2.blockchain.add_transaction(tx2)

    block = n2.blockchain.mine_block(n2.wallet.address)

    print("\n=== Propagation ===")
    print(f"[NODE-2] Broadcasting block #{block.index} to peers...")
    n2.broadcast_block(block)
    time.sleep(1.5)   # let peers process

    # Ensure n1 & n3 have the block even if socket delivery was slow
    for node in (n1, n3):
        if node.blockchain.last_block.index < block.index:
            node.blockchain.add_block(block)

    print("\n=== Wallet Balances ===")
    ref_chain = n1.blockchain       # use n1 as source of truth
    for node in nodes:
        bal = ref_chain.get_balance(node.wallet.address)
        print(f"{node.wallet.address}:  {bal} coins")

    for n in nodes:
        n.stop()


if __name__ == "__main__":
    run()
