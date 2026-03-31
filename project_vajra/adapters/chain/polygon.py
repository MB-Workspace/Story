"""
Polygon Blockchain Adapter using web3.py
"""
from web3 import Web3
from typing import Any, Dict, List

class PolygonAdapter:
    """Adapter for Polygon blockchain analysis"""
    
    def __init__(self, rpc_url: str = "https://polygon-rpc.com") -> None:
        self.w3 = Web3(Web3.HTTPProvider(rpc_url))
        
    def get_transactions(self, address: str, blocks: int = 10000) -> List[Dict[str, Any]]:
        """Get transactions for a Polygon address"""
        if not self.w3.is_connected():
            raise ConnectionError("Failed to connect to Polygon node")
            
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
    
    def get_balance(self, address: str) -> float:
        """Get current MATIC balance"""
        address = self.w3.to_checksum_address(address)
        return self.w3.from_wei(self.w3.eth.get_balance(address), "ether")
    
    def get_token_balance(self, contract_address: str, wallet_address: str) -> float:
        """Get token balance for a wallet"""
        contract_address = self.w3.to_checksum_address(contract_address)
        wallet_address = self.w3.to_checksum_address(wallet_address)
        
        # ERC-20 balanceOf function ABI
        abi = '[{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"type":"function"}]'
        contract = self.w3.eth.contract(address=contract_address, abi=abi)
        
        balance = contract.functions.balanceOf(wallet_address).call()
        return self.w3.from_wei(balance, "ether")
    
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