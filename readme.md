# CTI Lookups

This project pulls cyber threat intelligence (CTI) and reference data from various external sources, reformats and enriches it as needed, and publishes the results in this repository so other data tools can consume them directly.

## Data Extraction and Transformation

Scripting for the data sources are all in /sources, each data source includes documentation for it's outputs which are generated and committed back into the repo in the /data directories. They include:

- [iCloud Relay Proxy Egress IPs](sources/icloud-proxy/)  
- [Azure and O365 Cloud Services IPs](sources/azure-cloud/) (in progress)

Most have [workflows](.github/workflows/) setup to run github actions cronjobs daily 2am UTC to update the data files.

## Purpose

- **Ingest** — fetch data from upstream CTI feeds, threat intel providers, and other reference sources
- **Transform** — normalize and reformat raw data into consistent, machine-readable structures
- **Enrich** — augment records with additional context where applicable
- **Publish** — commit the processed data to this repo so downstream tools, pipelines, and queries can access it without re-fetching from source
