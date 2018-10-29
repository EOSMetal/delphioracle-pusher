#!/usr/bin/env python3

import logging
import argparse
import os
import colorlog
import inspect
import requests
import eospy.cleos
import eospy.keys


SCRIPT_PATH = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))

parser = argparse.ArgumentParser()
parser.add_argument("-v", '--verbose', action="store_true",
                    dest="verbose", help='Print logged info to screen')
parser.add_argument("-d", '--debug', action="store_true",
                    dest="debug", help='Print debug info')
parser.add_argument('-l', '--log_file', default='{}.log'.format(
    os.path.basename(__file__).split('.')[0]), help='Log file')
parser.add_argument('-u', '--api_endpoint',
                    default='https://api.eosmetal.io', help='EOSIO API endpoint URI')
parser.add_argument('-k', '--key', default='{}/oracle.key'.format(
    SCRIPT_PATH), help='Path to a file with the Private key')
parser.add_argument('-o', '--owner', default='eosmetaliobp',
                    help='Account pushing the value')
args = parser.parse_args()

VERBOSE = args.verbose
DEBUG = args.debug
LOG_FILE = args.log_file
API_ENDPOINT = args.api_endpoint
KEY_FILE = args.key
OWNER = args.owner

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = colorlog.ColoredFormatter(
    '%(log_color)s%(asctime)s - %(levelname)s - %(message)s%(reset)s')
if DEBUG:
    logger.setLevel(logging.DEBUG)
if VERBOSE:
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)

fh = logging.FileHandler(LOG_FILE)
logger.addHandler(fh)
fh.setFormatter(formatter)

SCRIPT_PATH = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))

cleos = eospy.cleos.Cleos(url=API_ENDPOINT)


def push_tick(tick, key):
    data = cleos.abi_json_to_bin('delphioracle', 'write', {
        "owner": OWNER, "value": tick})
    trx = {"actions": [{"account": "delphioracle", "name": "write", "authorization": [
        {"actor": OWNER, "permission": "oracle"}], "data": data['binargs']}]}
    return cleos.push_transaction(trx, key, broadcast=True)


def get_last_tick():
    try:
        result = requests.get(
            'https://api.kraken.com/0/public/Ticker?pair=EOSUSD').json()
        if result['error']:
            logger.critical(
                'Error getting tick from kraken: {}'.format(result['error']))
            return None
        return int(float(result['result']['EOSUSD']['c'][0]) * 10000)
    except Exception as e:
        logger.critical('Error getting tick from kraken: {}'.format(e))
        return None


def main():
    try:
        with open(KEY_FILE, 'r') as keyfile:
            key = keyfile.read().replace('\n', '')
    except Exception as e:
        logger.critical('Error reading private key file: {}'.format(e))

    try:
        tick = get_last_tick()
    except Exception as e:
        logger.critical('Error getting last tick from Kraken: {}'.format(e))

    try:
        resp = push_tick(tick, key)
    except Exception as e:
        logger.critical('Error pushing transaction: {}'.format(e))


if __name__ == "__main__":
    main()
