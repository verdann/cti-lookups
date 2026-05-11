# Threatfox IOCs

Parse the current IOC list from threatfox to their IOC types for easy csv ingestion to proper searchtypes. Currently just grabs https://threatfox.abuse.ch/export/csv/recent/ and parses two sub-lists, one CSV with domains and the other with IPs. Outputs default [data/threatfox-iocs](data/threatfox-iocs):
 - threatfox-iocs-current.csv - just the raw file downloaded from abuse.ch
 - threatfox-ips.csv - IOC list with just the IPs as ioc_value
 - threatfox-domains.csv - IOC list with just the domains as ioc_value

 Todo - add the urls to another output