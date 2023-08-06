# from platon.chains.platon import w3 as w3_platon
# from platon.chains.platon.testnet import w3 as w3_platon_testnet
# from platon.chains.alaya import w3 as w3_alaya
# from platon.chains.alaya.testnet import w3 as w3_alaya_testnet
#
# print(w3_platon.chain_id)
# print(w3_platon_testnet.chain_id)
# print(w3_alaya.chain_id)
# print(w3_alaya_testnet.chain_id)



# from web3 import HTTPProvider, Web3
# from platon_utils import to_checksum_address

# rpc = 'http://192.168.120.121:6789'
# print(to_checksum_address('atp1ldt5hpryxprayq7facczx4j2cx9atzeu9j53a3'))
#
# client = Web3(HTTPProvider(rpc))
# print(client.eth.get_balance(main_address))


# import asyncio
# import json
# import requests
# from websockets import connect
#
# async def get_event():
#     async with connect("ws://192.168.16.121:7789") as ws:
#         await ws.send({"id": 1, "method": "eth_subscribe", "params": ["newHeads"]})
#         subscription_response = await ws.recv()
#         print(subscription_response)
#         # you are now subscribed to the event
#         # you keep trying to listen to new events (similar idea to longPolling)
#         while True:
#             try:
#                 message = await asyncio.wait_for(ws.recv(), timeout=60)
#                 print(json.loads(message))
#                 pass
#             except:
#                 pass
#
# if __name__ == "__main__":
#     loop = asyncio.get_event_loop()
#     while True:
#         loop.run_until_complete(get_event())