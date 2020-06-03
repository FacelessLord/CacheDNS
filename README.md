# Caching DNS Server

## Requirements
Python 3.7+

## Algorithm
Server receives dns-packets, checks whether it can answer all queries.
If not it resends packet to parent dns-server. 
Then it receives parent response and caches all resource records from response.
Then server resends parent response to client

If it can, it collects all resource records associated with every query.
compiles new packet and sends it back

## Usage
Server started as python-executable file:
```bash
python server_runner.py
```

##Configuration
To configure server settings open `config.json` file and change value at `time_offset`:
* `ns` section controls server Internet setting
* `fwd` section describes parent dns-server
* `buffersize` is max length (in bytes) of dns-packet
* `cache_file` is filename where to store cache
