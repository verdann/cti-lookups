# CTI Lookups

This project pulls cyber threat intelligence (CTI) and reference data from various external sources, reformats and enriches it as needed, and publishes the results in this repository so other data tools can consume them directly.

## Purpose

- **Ingest** — fetch data from upstream CTI feeds, threat intel providers, and other reference sources
- **Transform** — normalize and reformat raw data into consistent, machine-readable structures
- **Enrich** — augment records with additional context where applicable
- **Publish** — commit the processed data to this repo so downstream tools, pipelines, and queries can access it without re-fetching from source
