---
name: san-jose-open-data
description: Find, assess, retrieve and combine public datasets for San José and Santa Clara County using official city/county catalogues, local utilities, transit agencies and relevant corporate or regional data. Use for local data discovery, source selection, API access and analysis; not as authority to access private customer, tenant, patient or voter records.
---

# San José open data

Use the catalogue to identify the authoritative publisher, actual access route, geographic coverage and reuse terms before retrieving observations. The bundled research snapshot is dated **2026-10-26, America/Los_Angeles**; it is a discovery aid, not a live guarantee of completeness, availability, freshness or licensing.

## Find the right source

Search the compact source registry first for a topic or provider:

```bash
python3 <skill-directory>/scripts/search_catalogue.py water --sources
python3 <skill-directory>/scripts/search_catalogue.py ridership --provider VTA
python3 <skill-directory>/scripts/search_catalogue.py "food inspections" --source county-socrata
python3 <skill-directory>/scripts/search_catalogue.py --id vuw7-jmjk --full
```

Resolve `<skill-directory>` to the directory containing this SKILL.md. `--sources` searches 113 curated source families; the default searches the full metadata inventory. Search terms are ANDed, accent-insensitively, across metadata. Use `--kind`, `--source`, `--provider`, `--id`, `--limit` and `--json` to narrow results. If a long query has no results, try a distinctive noun or an ID. Do not load the entire catalogue into context.

Read only relevant references:

- [domains.md](references/domains.md): source selection and interpretation for permits/housing, transport, public safety/health, utilities, environment and corporate data.
- [access.md](references/access.md): verified APIs, pagination, field quirks, GIS coordinate systems and metadata-refresh commands.
- [coverage.md](references/coverage.md): captured endpoints/counts, deduplication, limitations and data schema.
- [sources.json](references/sources.json): 113 source-family records with source URLs, access, formats, coverage, dates, licenses, caveats and fetch results. Search via helper.
- [catalogue.json](references/catalogue.json): item-level metadata, resource/download URLs and captured field schemas. Search via helper.

Prioritize official data appropriate to the task. City CKAN and GIS Hub overlap heavily. County Socrata and county GIS organizations overlap too; VTA, Valley Water and San Jose Water are separate publishers. GIS organization membership identifies the publishing account, not necessarily the original data producer. Some VTA and county items rehost state/national reference layers, and public organization indexes include tests, archives, surveys and apps.

## Use the evidence correctly

- Distinguish open-licensed datasets, publicly accessible data with unspecified terms, public reports/lookups, key/registration-based services and restricted programmes. A public URL, HTTP 200, `access:public`, `isopen` label or enterprise-system inventory is not sufficient evidence of unrestricted reuse.
- Re-read the selected item’s current metadata, schema and terms; verify the query or download before promising it. Report a failed request accurately, including ArcGIS JSON errors inside HTTP 200. Keep metadata timestamps distinct from observation dates and reporting periods.
- State publisher, direct source link, retrieval time, vintage, spatial/temporal coverage, units, access conditions, license evidence and material gaps in the result. For derived outputs, preserve source IDs and attribution. Avoid implying that a bounding-box subset is an exact city boundary clip.
- San José city, Santa Clara County, unincorporated county, City of Santa Clara, San José metro, census areas, utility service territories and wastewater sewersheds are different. Use FIPS **06085** for Santa Clara County and **0668000** for San José place (state `06`, place `68000`). Determine boundary vintage before joining.
- Retain APNs, census GEOIDs, provider/inspection identifiers and stop IDs as strings. Check one-to-many relationships, overlap, suppressed values, provisional data and revisions before aggregating. Do not sum annual/quarterly copies, full/thematic views or GIS mirrors.

## Retrieve and refresh

Use publisher APIs or explicit download links in the matched record, preserving source metadata alongside a bounded extract. Read [access.md](references/access.md) for local API examples and known failures. Do not invent API keys or substitute restricted customer portals for public data. Respect the user’s chosen scope; discovery does not authorize registration, submitting their identity, accepting new terms for them or purchasing data.

For a fresh metadata inventory, use the read-only helper in a new work directory:

```bash
python3 <skill-directory>/scripts/refresh_catalogue.py --output <new-empty-directory>
```

Limit a refresh with repeated `--source` arguments (see `--help`). It downloads catalogue metadata, not full observation tables, uses conservative concurrency and pagination, and emits raw metadata, a normalized `catalogue.json`, request receipts and explicit failures. It never overwrites installed references. Search a refreshed inventory using `search_catalogue.py --catalogue <directory>/catalogue.json ...`. A refresh covers known endpoints; discover newly created departmental portals separately. Read the failure receipts before calling a refresh complete.
