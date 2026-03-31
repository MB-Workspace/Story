"""
Blockchain Monitor for Active Defense
"""
from web3 import Web3
from typing import Callable, Any
from project_vajra.logging_config import logger

class BlockchainMonitor:
    """Monitors addresses and triggers callbacks on new transactions."""
    
    def __init__(self, rpc_url: str = "https://mainnet.infura.io/v3/YOUR_INFURA_KEY") -> None:
        self.w3 = Web3(Web3.HTTPProvider(rpc_url))
        self.watch_list = set()
        
    def add_to_watch_list(self, address: str) -> None:
        """Add an address to monitor."""
        if self.w3.is_connected():
            checksum_addr = self.w3.to_checksum_address(address)
            self.watch_list.add(checksum_addr)
            logger.info(f"[Antigravity] Added {checksum_addr} to watch list")
        else:
            logger.warning("[Antigravity] Not connected to node. Will simulate monitoring addition.")
            self.watch_list.add(address)
            
    def monitor_blocks(self, callback: Callable[[dict], None], block_count: int = 1) -> None:
        """Scan recent blocks for watched addresses (polling)."""
        if not self.w3.is_connected():
            logger.error("[Antigravity] Cannot monitor blocks: not connected to node.")
            return
            
        latest_block = self.w3.eth.block_number
        start_block = max(0, latest_block - block_count)
        
        for block_num in range(start_block, latest_block + 1):
            block = self.w3.eth.get_block(block_num, full_transactions=True)
            for tx in block.transactions:
                if tx["from"] in self.watch_list or tx["to"] in self.watch_list:
                    callback(tx)
