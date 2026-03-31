"""
Ethereum Blockchain Adapter using web3.py
"""
from web3 import Web3
from typing import Any, Dict, List

class EthereumAdapter:
    """Adapter for Ethereum blockchain analysis"""
    
    def __init__(self, rpc_url: str = "https://mainnet.infura.io/v3/YOUR_INFURA_KEY") -> None:
        self.w3 = Web3(Web3.HTTPProvider(rpc_url))
        
    def get_transactions(self, address: str, blocks: int = 10000) -> List[Dict[str, Any]]:
        """Get transactions for an Ethereum address"""
        if not self.w3.is_connected():
            raise ConnectionError("Failed to connect to Ethereum node")
            
        address = self.w3.to_checksum_address(address)
        transactions = []
        
        # Get latest block number
        latest_block = self.w3.eth.block_number
        
        # Scan blocks for transactions
        for block_num in range(latest_block - blocks, latest_block):
            block = self.w3.eth.get_block(block_num, full_transactions=True)
            for tx in block.transactions:
                if tx["from"] == address or tx["to"] == address:
                    transactions.append(self._normalize_tx(tx))
                    
        return transactions
    
    def get_smart_contract_logs(self, contract_address: str, event_signature: str) -> List[Dict]:
        """Get event logs for a smart contract"""
        contract_address = self.w3.to_checksum_address(contract_address)
        event_hash = self.w3.keccak(text=event_signature).hex()
        
        logs = self.w3.eth.get_logs({
            "fromBlock": "earliest",
            "toBlock": "latest",
            "address": contract_address,
            "topics": [event_hash]
        })
        
        return [self._decode_log(log) for log in logs]
    
    def _normalize_tx(self, tx: Any) -> Dict[str, Any]:
        """Normalize transaction to Vajra format"""
        return {
            "tx_id": tx["hash"].hex(),
            "timestamp": self.w3.eth.get_block(tx["blockNumber"])["timestamp"],
            "value": self.w3.from_wei(tx["value"], "ether"),
            "from_address": tx["from"],
            "to_address": tx["to"],
            "gas": tx["gas"],
            "gas_price": self.w3.from_wei(tx["gasPrice"], "gwei"),
            "input": tx["input"],
            "type": "contract" if tx["to"] is None else "transfer"
        }
    
    def _decode_log(self, log: Any) -> Dict[str, Any]:
        """Decode raw log data"""
        return {
            "block_number": log["blockNumber"],
            "transaction_hash": log["transactionHash"].hex(),
            "log_index": log["logIndex"],
            "data": log["data"],
            "topics": [topic.hex() for topic in log["topics"]]
        }
    
    def get_erc20_transfers(self, address: str) -> List[Dict]:
        """Get ERC-20 token transfers for an address"""
        # ERC-20 Transfer event signature
        transfer_event = "Transfer(address,address,uint256)"
        return self.get_smart_contract_logs(address, transfer_event)