# Binary Edge Scanners

Binary Edge runs a number of scanners (last cound around 2k) but they use randomly allocated VPS/compute hosts across several providers such as Akamai Linode and AWS instead of getting their own subnet. Their IP list is published as [minions](https://api.binaryedge.io/v1/minions) in JSON format. Two files are created with just formatting changes:
* [binaryedge-ipv4-cidr.csv](data/binaryedge/binaryedge-ipv4-cidr.csv) - CSV header 'cidr' with addresses appended with /32
* [binaryedge-ipv4-ip.csv](data/binaryedge/binaryedge-ipv4-cidr.csv) - CSV header 'ip' with just plain ip address