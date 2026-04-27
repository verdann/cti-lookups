# iCloud Proxy Egress IP Ranges

Apple devices provide a private relay service as part of their iCloud+ service. The source IPs seen by services being accessed are from a variety of ASNs including Fastly and Akamai meaning there are lots of other activities from those network providers as well. Source info in https://developer.apple.com/icloud/prepare-your-network-for-icloud-private-relay/ 

This script pulls the CSV provided by Apple and munges some data artifacts into:
 - egress-ip-ranges20260427.csv : the current full source file
 - icloud-egress-ipv4.csv : filtered list to IPv4 subnets 
 - icloud-egress-ipv6.csv : filtered list to IPv6 subnets
 - icloud-egress-compresscidr-ipv4.csv : IPv4 subnets only without geolocation data, with CIDR ranges expanded to larger supernets where ranges were consecutive. Currently < 10% of full list size.
 - icloud-egress-compresscidr-ipv6.csv : IPv6 subnets only without geolocation data, with CIDR ranges expanded to larger supernets where ranges were consecutive. Currently < 5% of full list size.

 Env variables:
- url_icloudegress : https://mask-api.icloud.com/egress-ip-ranges.csv
- output_icloudegress : "."