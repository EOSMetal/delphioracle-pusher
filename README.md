![EOSMetal](./logo-text-grey.jpg "EOSMetal")

[https://eosmetal.io](https://eosmetal.io)

# delphioracle-pusher
Python client for the delphi oracle that uses Kraken as a price feed.

Usage:
```bash
./oracle-pusher.py --help                                                               
usage: oracle-pusher.py [-h] [-v] [-d] [-l LOG_FILE] [-u API_ENDPOINT]
                        [-k KEY] [-o OWNER]

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Print logged info to screen
  -d, --debug           Print debug info
  -l LOG_FILE, --log_file LOG_FILE
                        Log file
  -u API_ENDPOINT, --api_endpoint API_ENDPOINT
                        EOSIO API endpoint URI
  -k KEY, --key KEY     Path to a file with the Private key
  -o OWNER, --owner OWNER
                        Account pushing the value
```

