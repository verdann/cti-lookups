# Azure Cloud Service Ranges

Azure cloud IPs don't have easily determined service types via rDNS or other means, though it is published in JSON format by Microsoft. This script downloads and parses out the service and CIDR ranges into data/msft-azurecloud in this repo.

The files are:
- ServiceTags_Public_Current.json - raw file from Microsoft
- azure-ipv4-servicetag.csv - ipv4 cidr ranges with systemService attribute
- azure-ipv6-servicetag.csv - ipv6 cidr ranges with systemService attribute
- azurecloud-ipv4.csv - only the ipv4 cidr ranges supernetted where possible against sequential ranges
- azurecloud-ipv6.csv - only the ipv6 cidr ranges supernetted where possible against sequential ranges

See also [O365 Service Ranges](sources/msft-office) for further eligible Microsoft ASN enrichments.