# Azure Cloud Service Ranges

Azure cloud IPs don't have easily determined service types via rDNS or other means, though it is published in JSON format by Microsoft. This script downloads and parses out the service and CIDR ranges into data/msft-azurecloud in this repo.

The files are:
- ServiceTags_Public_YYYYMMDD.json - raw file from MS, datestamp same as downloaded filename
- 