import binascii
from functools import wraps
from platon import Web3
from platon.contract import ContractFunction
from platon_account import Account
from platon_account.signers.local import LocalAccount
from platon._utils.abi import filter_by_name


def deploy(web3: Web3, bytecode: str, abi: str, account: LocalAccount, **constructor_args):
    nonce = web3.platon.get_transaction_count(account.address)
    contract = web3.platon.contract(abi=abi, bytecode=bytecode)
    transaction = {
        'gas': 4012388,
        'gasPrice': 1000000000,
        "chainId": web3.chain_id,
        "nonce": nonce,
    }
    data = contract.constructor(kwargs=constructor_args)._encode_data_in_transaction()
    transaction["data"] = data
    signed_tx = web3.platon.account.sign_transaction(transaction, account.privateKey).rawTransaction
    tx_hex = web3.platon.send_raw_transaction(signed_tx)
    receipt = web3.platon.wait_for_transaction_receipt(tx_hex)
    address = receipt['contractAddress']
    return Contract(web3, bytecode, abi, address, account)


def get_bytecode(path: str):
    with open(path, 'rb') as f:
        contents = f.read()
    return binascii.b2a_hex(contents)


class Contract:

    def __init__(self, web3: Web3, bytecode: str, abi: str, address: str, account: LocalAccount = None):
        self.web3 = web3
        self.bytecode = bytecode
        self.abi = abi
        self.address = address
        self.account = account
        self.contract = web3.platon.contract(address=address, abi=abi, bytecode=bytecode)
        self.functions = self.contract.functions
        self.events = self.contract.events
        self._set_functions(self.contract.functions)
        self._set_events(self.contract.events)
        self._set_fallback(self.contract.fallback)

    def _set_functions(self, functions):
        for func in functions:
            # 通过方法名获取方法
            warp_function = self._function_wrap(getattr(functions, func))
            setattr(self, func, warp_function)

    def _set_events(self, events):
        for event in events:
            # 通过方法名获取方法
            warp_event = self._event_wrap(event)
            setattr(self, event.event_name, warp_event)

    def _set_fallback(self, fallback):
        if type(fallback) is ContractFunction:
            warp_fallback = self._fallback_wrap(fallback)
            setattr(self, fallback, warp_fallback)
        else:
            self.fallback = fallback

    def _function_wrap(self, func):
        @wraps(func)
        def call_selector(*args, **kwargs):
            fn_abi = filter_by_name(func.fn_name, self.abi)
            assert len(fn_abi) == 1, 'The method cannot be found in the ABI'
            if fn_abi[0].get('stateMutability') == 'view':
                return func(*args, **kwargs).call()
            else:
                tx = {
                    'chainId': self.web3.chain_id,
                    'nonce': self.web3.platon.get_transaction_count(self.account.address),
                    'gas': 4012388,
                    'value': 0,
                    'gasPrice': 1000000000,
                }
                txn = func(*args, **kwargs).build_transaction(tx)
                signed_txn = self.web3.platon.account.sign_transaction(txn, private_key=self.account.privateKey.hex())
                tx_hash = self.web3.platon.send_raw_transaction(signed_txn.rawTransaction).hex()
                return self.web3.platon.wait_for_transaction_receipt(tx_hash)

        return call_selector

    def _event_wrap(self, func):
        @wraps(func)
        def call_selector(*args, **kwargs):
            return func().processReceipt(*args, **kwargs)

        return call_selector

    def _fallback_wrap(self, func):
        @wraps(func)
        def call_selector(*args, **kwargs):
            tx = {
                'chainId': self.web3.chain_id,
                'nonce': self.web3.platon.get_transaction_count(self.account.address),
                'gas': 4012388,
                'value': 0,
                'gasPrice': 1000000000,
                'to': self.address
            }
            txn = func(*args, **kwargs).build_transaction(tx)
            signed_txn = self.web3.platon.account.signTransaction(txn, private_key=self.owner.privateKey.hex())
            tx_hash = self.web3.platon.send_raw_transaction(signed_txn.rawTransaction).hex()
            return self.web3.platon.wait_for_transaction_receipt(tx_hash)

        return call_selector


if __name__ == '__main__':
    from debug.wasm import abi, code

    url = 'http://192.168.120.121:6789'
    main_address, main_private_key = 'lat1rzw6lukpltqn9rk5k59apjrf5vmt2ncv8uvfn7', 'f90fd6808860fe869631d978b0582bb59db6189f7908b578a886d582cb6fccfa'

    w3 = Web3(Web3.HTTPProvider(url))
    account = Account().from_key(main_private_key, w3.hrp)

    bytecode = get_bytecode('./')
    contract = deploy(w3, code, abi, account)
    print(contract.address)
