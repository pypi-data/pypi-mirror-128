from platon import Web3, HTTPProvider
import time


rpc = 'http://127.0.0.1:6789'
w3 = Web3(HTTPProvider(rpc))
# res_address = w3.toChecksumAddress('1000000000000000000000000000000000000001')
res_address = 'lat1zqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqp7pn3ep'


def handle_event(event):
    print(event)


def log_loop(event_filter, poll_interval):
    while True:
        for event in event_filter.get_new_entries():
            handle_event(event)
        time.sleep(poll_interval)


def main():
    block_filter = w3.platon.get_logs({"address": res_address})
    print(block_filter)


if __name__ == '__main__':
    main()
