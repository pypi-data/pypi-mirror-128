from web3 import Web3, HTTPProvider
from loguru import logger


class AbiHandler:
    def __init__(self, abi: str, contract_addr: str, rpc: str):
        self.contract_addr = contract_addr
        self.web3 = Web3(HTTPProvider(rpc))
        self.contract = self.web3.eth.contract(address=self.web3.toChecksumAddress(contract_addr), abi=abi)

    def sign_transaction(self, func_name: str, private: str, **kwargs):
        try:
            func = getattr(self.contract.functions, func_name)(**kwargs)
            nonce = self.web3.eth.getTransactionCount(self.contract_addr)
            params = {
                "from": self.contract_addr,
                "value": web3.toWei(0, "ether"),
                "gasPrice": web3.toWei(5, "gwei"),
                "gas": 500000,
                "nonce": nonce,
            }
            tx = func.buildTransaction(params)
            signed_tx = self.web3.eth.account.sign_transaction(tx, private_key=private)
            tx_hash = self.web3.eth.sendRawTransaction(signed_tx.rawTransaction)
            return self.web3.toHex(tx_hash)

        except Exception as e:
            logger.error(f"{func_name} failed: {e}")

    def call(self, func_name: str, **kwargs):
        try:
            tx = getattr(self.contract.functions, func_name)(**kwargs).call()
            return tx
        except Exception as e:
            logger.error(f"Call {func_name} failed: {e}")

    def to_checksum_addr(self, addr):
        return self.web3.toChecksumAddress(addr)
