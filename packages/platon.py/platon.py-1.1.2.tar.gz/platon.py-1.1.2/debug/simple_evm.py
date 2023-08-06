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
    url = 'http://192.168.120.121:6789'
    w3 = Web3(Web3.HTTPProvider(url))
    main_address, main_private_key = 'atp1zkrxx6rf358jcvr7nruhyvr9hxpwv9uncjmns0', 'f51ca759562e1daf9e5302d121f933a8152915d34fcbc27e542baf256b5e4b74'

    false = False
    true = True
    bytecode = "0x608060405234801561001057600080fd5b5060dd8061001f6000396000f3fe6080604052348015600f57600080fd5b506004361060285760003560e01c806326121ff014602d575b600080fd5b6033607b565b604080519586526001600160f01b031990941660208601526001600160e81b031990921684840152151560608401526001600160a01b03166080830152519081900360a00190f35b60029061abcd60f01b906261626360e81b90600190735edbc4160ca598fd3b87f1197e65a2eafdb039769056fea265627a7a72315820f6ea7e6a97ccc10eac37c5fd663baf86c59a364f91fdd3e2afbb04b773b4100164736f6c63430005110032"
    abi = [{"constant":true,"inputs":[],"name":"f","outputs":[{"internalType":"uint256","name":"w","type":"uint256"},{"internalType":"bytes2","name":"x","type":"bytes2"},{"internalType":"bytes3","name":"y","type":"bytes3"},{"internalType":"bool","name":"z","type":"bool"},{"internalType":"address","name":"t","type":"address"}],"payable":false,"stateMutability":"view","type":"function"}]
    account = Account().from_key(main_private_key, w3.hrp)
    contract = deploy(w3, bytecode, abi, account)
    print(contract.address)
    result = contract.f()
    print(result)
    # result = contract.createTokenContract(_name='aETH123', _symbol='aETH', _decimals=18, _cap=10 ** 18 * 10000)
    # print(result)

