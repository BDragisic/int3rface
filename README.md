# Int3rface
A script to enumerate subdomains and detect if any of them host a login portal that can be accessed publicly.

## Prerequisites

* PostgreSQL
    * MacOS - ```brew install postgresql@14```
    * Windows - https://www.postgresql.org/download

* Pip Modules
    * pip3 install -r requirements.txt

## Usage

```
python3 int3rface.py -h
```

## Features

* ```-i``` used to specify a list of domains
* ```-x``` used to automatically open all matches in browser
* ```-o``` used to specify an output file for the results
* ```-s``` used to take screenshots of all matches
* ```-c``` will crawl all links present on each subdomain to check for login pages




