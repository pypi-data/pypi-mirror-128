import json
import time
from platon import HTTPProvider, Web3
from hexbytes import HexBytes
from platon_account.account import Account
from loguru import logger


# 通用信息
class SimpleTx:
    pip_txn = {'gasPrice': 3000000000000000}

    def __init__(self, rpc):
        self.rpc = rpc
        self.web3 = Web3(HTTPProvider(rpc))
        # self.web3.middleware_stack.inject(geth_poa_middleware, layer=0)
        self.platon = self.web3.platon
        self.restricting = self.web3.restricting
        self.ppos = self.web3.ppos
        self.pip = self.web3.pip
        self.admin = self.web3.node.admin
        self.personal = self.web3.node.personal
        self.txpool = self.web3.node.txpool
        # self.debug = self.web3.node.debug
        self.hrp = self.web3.hrp
        self.chain_id = self.platon.chain_id

    # 创建账户
    def create_account(self):
        account = self.platon.account.create(hrp=self.hrp)
        address = account.address
        private_key = account.privateKey.hex()[2:]
        logger.info(f"create account = {address}, {private_key}")
        return address, private_key

    # 创建HD钱包
    # def create_hd_account():
    #     logger.info("==== create hd account =====")
    #     # account = self.web3.platon.account.(hrp=self.hrp)
    #     master_key, mnemonic = HDPrivateKey.master_key_from_entropy()
    #     logger.info(master_key)
    #     logger.info(mnemonic)
    #     root_keys = HDKey.from_path(master_key, "m/44'/206'/0'")
    #     logger.info(root_keys)
    #     acct_priv_key = root_keys[-1]
    #     logger.info(acct_priv_key)
    # for j in range(30):
    #     keys = HDKey.from_path(acct_priv_key, '{change}/{index}'.format(change=0, index=j))
    #     private_key = keys[-1]
    #     public_address = private_key.public_key.address('atp')
    #     keystores[public_address] = json.dumps(private_key._key.to_keyfile_json(password))
    #     privateKeys[public_address] = private_key._key.get_private_key()
    #     addresses_df.loc[(prikey_manager, account_use, wallet_type, i, j), :] = [public_address]

    # rlp解码
    # def decode_rlp(self, byte):
    #     if byte == b'':
    #         return byte.hex()
    #     decoded = rlp.decode(byte)
    #     if type(decoded) is list:
    #         values = []
    #         for i, byte in enumerate(decoded):
    #             value = self.decode_rlp(byte)
    #             values.append(value)
    #         return values
    #     else:
    #         length = len(decoded)
    #         if length in [0, 20, 64, 128, 192]:
    #             value = decoded.hex()
    #             return value
    #         try:
    #             value = decoded.decode('utf-8')
    #             return value
    #         except Exception:
    #             pass
    #         try:
    #             value = int.from_bytes(decoded, 'big')
    #             return value
    #         except Exception:
    #             pass

    # 转账交易
    def transfer(self, from_private_key, to_address, amount):
        from_address = Account.from_key(from_private_key, self.hrp).address
        txn = {
            "to": to_address,
            "gasPrice": self.platon.gas_price,
            "gas": 21000,
            "nonce": self.platon.get_transaction_count(from_address),
            "data": '',
            "chainId": self.chain_id,
            "value": amount,
        }
        result = self.send_transaction(txn, from_private_key)
        if result['status'] == 1:
            logger.info(f'transfer result = 0')
        else:
            logger.info(f'transfer result = {result}')
        return result

    # 锁仓交易
    def create_restricting(self, from_private_key, to_address, restricting_plan):
        func = self.restricting.create_restricting(to_address, restricting_plan)
        print(func.estimate_gas())
        txn = func.build_transaction()
        result = bytes(self.send_transaction(txn, from_private_key)).hex
        logger.info(f"restricting result = {result}")
        return result

    # 创建质押
    def staking(self, staking_private_key, balance_type, node_url, amount=10 ** 18 * 2000000, reward_per=1000):
        w3 = Web3(HTTPProvider(node_url))
        version_info = w3.node.admin.get_program_version()
        version = version_info['Version']
        version_sign = version_info['Sign']
        node_info = w3.node.admin.node_info()
        node_id = node_info['id']
        bls_pubkey = node_info['blsPubKey']
        bls_proof = w3.node.admin.get_schnorr_NIZK_prove()
        address = Account.from_key(staking_private_key, self.hrp).address
        tx_obj = self.ppos.staking.create_staking(balance_type, address, node_id, 'external_id', 'node_name', 'website', 'details', amount, reward_per,
                                                  version, version_sign, bls_pubkey, bls_proof)
        txn = tx_obj.build_transaction({'nonce': self.web3.platon.get_transaction_count(address)})
        signed_txn = self.web3.platon.account.sign_transaction(txn, staking_private_key, self.web3.hrp)
        tx_hash = self.web3.platon.send_raw_transaction(signed_txn.rawTransaction)
        result = self.web3.platon.wait_for_transaction_receipt(tx_hash)
        logger.info(f"staking result = {result['code']}, {result}")
        return result

    # 增持质押
    def increase_staking(self, staking_private_key, node_id, balance_type, amount=10 ** 18 * 100):
        result = self.ppos.increase_staking(balance_type, node_id, amount, staking_private_key)
        logger.info(f"incress staking result = {result['code']}, {result}")
        return result

    # 修改质押信息
    def edit_staking(self, staking_private_key, node_id, benefit_address=None, external_id=None, node_name=None, website=None, details=None,
                     reward_per=None):
        result = self.ppos.edit_candidate(staking_private_key, node_id, benefit_address, external_id, node_name, website, details, reward_per)
        logger.info(f"edit staking result = {result['code']}, {result}")
        return result

    # 解除质押
    def withdrew_staking(self, staking_private_key, node_id):
        result = self.ppos.withdrew_staking(node_id, staking_private_key)
        logger.info(f"withdrew staking result = {result['code']}, {result}")
        return result

    # 查询质押信息
    def get_candidate_info(self, node_id):
        result = self.ppos.get_candidate_info(node_id)
        logger.info(f"get candidate info = {result['Code']}, {result}")

    # 查询当前轮验证人信息
    def get_validator_list(self):
        result = self.ppos.get_validator_list()
        logger.info(f"get Validator list = {result['Code']}, {result}")

    # 查询验证人信息
    def get_verifier_list(self):
        result = self.ppos.get_verifier_list()
        logger.info(f"get Verifier list = {result['Code']}, {result}")

    # 查询全部质押信息
    def get_candidate_list(self):
        result = self.ppos.get_candidate_list()
        logger.info(f"get candidate list = {result['Code']}, {result}")

    # 创建委托
    def delegate(self, delegation_private_key, node_id, balance_type, amount=10 * 10 ** 18):
        result = self.ppos.delegate(balance_type, node_id, amount, delegation_private_key)
        logger.info(f"delegate result = {result['code']}, {result}")
        return result

    # 解除委托
    def undelegate(self, delegation_private_key, node_id, block_number, amount=1 * 10 ** 18):
        result = self.ppos.withdrew_delegate(block_number, node_id, amount, delegation_private_key)
        logger.info(f"undelegate result = {result['code']}, {result}")
        return result

    # 获取可委托节点列表
    def get_delegable_nodes(self, cdf_account):
        result = self.ppos.get_candidate_list()
        delegable_nodes = [i for i in result['Ret'] if i['StakingAddress'] != cdf_account]
        logger.info(f"get delegable nodes = {delegable_nodes}")
        return delegable_nodes

    # 查询委托信息
    def get_delegate_list(self, delegation_address):
        result = self.ppos.get_related_list_by_delAddr(delegation_address)
        logger.info(f"get delegate list = {result['Code']}, {result}")
        return result

    # 获取账户对某个节点的委托信息
    def get_delegate_list_for_node(self, address, node_id):
        delegated_list = []
        result = self.get_delegate_list(address)
        if result['Code'] == 0:
            for delegated_info in result['Ret']:
                if delegated_info['NodeId'] is node_id:
                    delegated_list.append(delegated_info)
            if delegated_list:
                result['Ret'] = delegated_list
            else:
                result = {'Code': 301203, 'Ret': 'Retreiving delegation related mapping failed:RelatedList info is not found'}
        logger.info(f"get delegated list for node = {result['Code']}, {result}")
        return result

    # 获取账户对某个节点的委托详情
    def get_delegate_info(self, address, node_id, block_number):
        result = self.ppos.get_delegate_info(block_number, address, node_id)
        logger.info(f"get delegated info = {result['Code']}, {result}")
        return result

    # 领取委托分红
    def withdraw_delegate_reward(self, delegate_private_key):
        result = self.ppos.withdraw_delegate_reward(delegate_private_key)
        logger.info(f"withdraw delegate result = {result['code']}, {result}")
        return result

    # 创建升级提案
    def version_proposal(self, staking_private_key, node_id, upgrade_version, voting_rounds):
        result = self.pip.submitVersion(node_id, str(time.time()), upgrade_version, voting_rounds, staking_private_key, self.pip_txn)
        logger.info(f"version proposal result = {result['code']}, {result}")
        return result

    # 创建文本提案
    def text_proposal(self, node_id, staking_private_key):
        func = self.pip.submit_text_proposal(node_id, str(time.time()))
        address = self.web3.platon.account.from_key(staking_private_key).address
        nonce = self.web3.platon.get_transaction_count(address)
        txn = func.build_transaction({'nonce': nonce})
        txn.update(self.pip_txn)
        result = self.send_transaction(txn, staking_private_key)
        logger.info(f"text proposal result = {result['code']}, {result}")
        return result

    def send_transaction(self, txn, private_key, is_hash=False):
        signed_txn = self.platon.account.sign_transaction(txn, private_key, self.hrp)
        tx_hash = self.platon.send_raw_transaction(signed_txn.rawTransaction)
        if is_hash:
            return bytes(tx_hash).hex()
        return self.platon.wait_for_transaction_receipt(tx_hash)

    # 查询提案列表
    def get_proposal_list(self):
        result = self.pip.proposal_list()
        result = json.loads(bytes(result).decode('utf-8'))
        logger.info(f"proposal list = {result['Code']}, {result}")
        return result

    # 提案投票
    def vote(self, staking_private_key, node_url, proposal_id, vote_type):
        w3 = Web3(HTTPProvider(node_url), hrp=self.hrp)
        program_version = w3.admin.getProgramVersion()['Version']

        print(f'program_version == {program_version}')
        version_sign = w3.admin.getProgramVersion()['Sign']
        node_id = w3.admin.nodeInfo['id']
        # proposal_id = w3.pip.listProposal().get('Ret')[0].get('ProposalID')
        # assert proposal_id != ''
        logger.info(f'vote node: {node_url}, {node_id}')
        result = self.pip.vote(node_id, proposal_id, vote_type, program_version, version_sign, staking_private_key)
        logger.info(f"vote result = {result['code']}, {result}")
        return result

    # 版本声明
    def declare_version(self, staking_private_key, node_url):
        w3 = Web3(HTTPProvider(node_url), hrp=self.hrp)
        node_id = w3.admin.nodeInfo['id']
        program_version = w3.admin.getProgramVersion()['Version']
        version_sign = w3.admin.getProgramVersion()['Sign']
        result = self.pip.declareVersion(node_id, program_version, version_sign, staking_private_key)
        logger.info(f"declare version result = {result['code']}, {result}")
        return result

    # 获取当前版本号
    def get_version(self):
        result = self.pip.getActiveVersion()
        logger.info(f'chain version = {result}')

    # 等待块高
    def wait_block(self, block_number):
        current_block = self.platon.blockNumber
        end_block = current_block + block_number
        while current_block < end_block:
            logger.info(f'wait block: {current_block} -> {end_block}')
            time.sleep(5)
            current_block = self.platon.blockNumber


if __name__ == '__main__':
    rpc = 'http://192.168.120.121:6789'
    main_address, main_private_key = 'atp1zkrxx6rf358jcvr7nruhyvr9hxpwv9uncjmns0', 'f51ca759562e1daf9e5302d121f933a8152915d34fcbc27e542baf256b5e4b74'
    cdf_address, cdf_private_key = 'atp1ur2hg0u9wt5qenmkcxlp7ysvaw6yupt4vll2fq', '64bc85af4fa0e165a1753b762b1f45017dd66955e2f8eea00333db352198b77e'
    tx = SimpleTx(rpc)

    main_address, main_private_key = to_bech32_address('atp1zkrxx6rf358jcvr7nruhyvr9hxpwv9uncjmns0', 'atp'), 'f51ca759562e1daf9e5302d121f933a8152915d34fcbc27e542baf256b5e4b74'
    cdf_address, cdf_private_key = to_bech32_address('atp1ur2hg0u9wt5qenmkcxlp7ysvaw6yupt4vll2fq', 'atp'), '64bc85af4fa0e165a1753b762b1f45017dd66955e2f8eea00333db352198b77e'

    nonce = w3.platon.get_transaction_count(main_address)
    base_transaction = {'from': main_address, 'gas': 100000, 'nonce': nonce}

    print(tx.platon.get_balance(main_address))
    # 转账
    # to_address, to_private_key = tx.create_account()
    # tx.transfer(main_private_key, cdf_address, 2 * 10 ** 18)
    # 锁仓
    plans = [{'Epoch': 1, 'Amount': 100 * 10 ** 18}]
    tx.create_restricting(main_private_key, cdf_address, plans)
    # 质押
    # print(tx.staking(main_private_key, 0, 'http://192.168.120.121:6790'))
    # 提案
    # node_id = '35bb5daad814fe902030cba6fd2d3ec60906dab70ba5df4d42a19448d300ab203cfd892c325f6716965dd93d8de2a377a2806c9703b69b68287577c70f9e7c07'
    # tx.text_proposal(node_id, cdf_private_key)
    # tx.get_proposal_list()

    # signed_txn = w3.platon.account.sign_transaction(txn, main_private_key, w3.hrp)
    # tx_hash = bytes(w3.platon.send_raw_transaction(signed_txn.rawTransaction)).hex()
    # print(tx_hash)
    # receipt = w3.platon.wait_for_transaction_receipt(tx_hash)
    # print(receipt)

    # print(w3.debug.get_block_rlp(1))
    # print(w3.platon.consensus_status())
    # result = w3.debug.get_wait_slashing_node_list()
    # print(w3.debug.get_wait_slashing_node_list())

    ### 基础方法
    # print(Web3.toVon(1, 'ether'))
    # print(w3.isConnected())
    # print(w3.clientVersion)
    # print(w3.toVon(1, 'ether'))
    # print(w3.platon.chain_id)
    # print(w3.platon.get_address_hrp())
    # print(w3.platon.get_balance(cdf_address))
    # print(w3.platon.evidences())
    # print(w3.platon.get_transaction_count('lat1rzw6lukpltqn9rk5k59apjrf5vmt2ncv8uvfn7'))
    # print(w3.platon.get_transaction_receipt('0x53a3bed97b583d9571f7839e584488c6ba33aa2536989a85e3908c63281592f3'))
    # print(w3.platon.get_block(0))
    # print(to_canonical_address("0xd3cda913deb6f67967b99d67acdfa1712c293601"))
    # print(to_bech32_address('0x189DAff2C1faC1328ed4B50Bd0c869A336B54F0C', 'lat'))
    # print(w3.platon.accounts)

    ### 转账交易
    # pass

    ### 内置合约
    # _result = w3.node.admin.node_info()
    # node_id = _result['id']
    # bls_pub_key = _result['blsPubKey']
    # bls_proof = w3.node.admin.get_schnorr_NIZK_prove()
    # _result = w3.node.admin.get_program_version()
    # version = _result['Version']
    # version_sign = _result['Sign']
    # nonce = w3.platon.get_transaction_count(main_address)

    # 锁仓
    # plans = [{'Epoch': 1, 'Amount': 1 * 10 ** 18}]
    # func = w3.restricting.create_restricting(cdf_address, plans)
    # receipt = send_transaction(func, main_private_key, base_transaction)
    # data = InnerContractEvent().get_event(receipt)
    # print(data)

    # print(w3.restricting.get_restricting_info(main_address))

    # ppos call
    # print(w3.ppos.staking.get_candidate_list())
    # print(w3.ppos.staking.get_verifier_list())
    # print(w3.ppos.staking.get_validator_list())
    # print(w3.ppos.staking.get_avg_block_time())
    # print(w3.ppos.staking.get_staking_reward())
    # print(w3.ppos.staking.get_block_reward())

    # # ppos tx
    # staking = w3.ppos.staking.create_staking(0, main_address, node_id, '', 'test node', '', '', w3.toVon(1000000, 'lat'), 5000, version, version_sign, bls_pub_key, bls_proof)
    # txn = staking.build_transaction({'nonce': nonce})
    # signed_txn = w3.platon.account.sign_transaction(txn, main_private_key, w3.hrp)
    # tx_hash = bytes(w3.platon.send_raw_transaction(signed_txn.rawTransaction)).hex()
    # print(tx_hash)
    # receipt = w3.platon.wait_for_transaction_receipt(tx_hash)
    # print(receipt)

    # func = w3.ppos.delegate.withdraw_delegate_reward()
    # txn = func.build_transaction({'from': main_address})
    # print(txn)

    # result = w3.ppos.delegate.get_delegate_reward(address=main_address, node_ids=['35bb5daad814fe902030cba6fd2d3ec60906dab70ba5df4d42a19448d300ab203cfd892c325f6716965dd93d8de2a377a2806c9703b69b68287577c70f9e7c07'])
    # print(result)

    # pip call
    # print(w3.pip.proposal_list())
    # print(w3.pip.get_chain_version())
    # proposal_id = bytes.fromhex('910908154a4c9917bf9764a174f91c86c9661b91a380745e684922cefb6a57e3')
    # #
    # print(w3.platon.get_block('latest'))
    # block.hash
    # block_hash = block.hash
    # print(w3.pip.get_proposal_votes(proposal_id, block_hash))
    # print(w3.pip.get_proposal_result(proposal_id))

    # pip tx
    # text_proposal = w3.pip.submit_text_proposal(node_id, 'test')
    # txn = text_proposal.build_transaction({
    #     'nonce': w3.platon.get_transaction_count(cdf_address),
    #     'gasPrice': w3.toVon(3, 'microether')
    # })
    # signed_txn = w3.platon.account.sign_transaction(txn, main_private_key, w3.hrp)
    # tx_hash = bytes(w3.platon.send_raw_transaction(signed_txn.rawTransaction)).hex()
    # print(tx_hash)
    # receipt = w3.platon.wait_for_transaction_receipt(tx_hash)
    # print(receipt)
