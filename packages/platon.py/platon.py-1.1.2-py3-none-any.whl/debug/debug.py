from platon import Web3

# url = 'http://127.0.0.1:6789'
url = 'https://openapi.alaya.network/rpc'
w3 = Web3(Web3.HTTPProvider(url))

# address, private_key = 'atp1zkrxx6rf358jcvr7nruhyvr9hxpwv9uncjmns0', 'f51ca759562e1daf9e5302d121f933a8152915d34fcbc27e542baf256b5e4b74'
address = 'atp10kkmmxqxhxjqd6cj3g7cpqjyjhyw2tc53gvzls'

print(w3.restricting.get_restricting_info(address))