# Snapshot coverage and limits

Research date: **2026-10-26, America/Los_Angeles**. The snapshot records public metadata, not downloaded source observations.

## Enumeration results

| Inventory | Records captured |
|---|---:|
| city-ckan | 170 |
| county-socrata | 1,806 |
| city-gis-hub | 152 |
| county-planning-hub | 70 |
| vta-hub | 97 |
| valleywater-hub | 25 |
| city-arcgis | 1,042 |
| county-central-arcgis | 457 |
| county-planning-arcgis | 417 |
| vta-arcgis | 471 |
| valleywater-arcgis | 206 |
| sjwater-arcgis | 101 |
| city-rest-layers | 151 |

Total: **5,165 metadata records**, **9,059 resource/access URLs, including generated query/metadata candidates**, and **282 records with captured field definitions**. These are counts of records/links in overlapping inventories, not distinct databases or independently tested downloads. The 170 city CKAN packages contain 1,021 resources. Six public GIS organization inventories total 2,694 items; organization searches reconciled every page against reported totals.

County discovery and view APIs each returned 1,806 IDs. County DCAT contained 1,737, all a subset of those IDs; using only DCAT would miss 69. County discovery types were 131 datasets, 1,568 files, 52 maps, 35 stories, 17 charts and 3 external links. Many files are repeated plan/month-specific health insurance pricing releases. All 1,806 discovery entries carried `provenance:official`; that platform flag does not establish a reuse license. All captured county views lacked a populated `licenseId`.

City CKAN package license IDs: 17 `cc-zero`, 152 `cc-by`, one `notspecified`. The 152 GIS mirror packages overlap the GIS Hub feed. City ArcGIS public item inventory includes many applications and reference/test content. City OpenDataService returned 151 layer definitions; those are additional access/schema records for overlapping city GIS content.

The manually researched **113 source families** add departmental records, water and electric utilities, transportation, regional agencies, corporate public datasets and state/federal complements. These are source families rather than an item-level enumeration of every federal/corporate dataset. The source registry records public download/API versus lookup/report versus conditional/restricted access.

## What completeness means here

The city CKAN, county discovery/view inventories, four Hub metadata feeds, six GIS organizations and city primary REST layer list were enumerated to their reported totals for the captured requests. This is the strongest reproducible coverage claim. It is not a proof that every public local-government record, unindexed departmental document, legacy GIS service, newly published database or corporate data product has been discovered.

Only public entries are in scope. No authenticated customer/patient/tenant/voter database was accessed, no accounts or API keys were created, and no underlying bulk observation tables were downloaded. Archived/mirrored/test/application metadata remains visible and is explicitly identified by its source and type; it has not been endorsed as production-quality open data.

## Verification levels and failures

- Full metadata inventory requests succeeded for the 13 included inventory groups; ArcGIS organizational search counts were reconciled.
- Representative county food schemas and an anonymous food-business count query succeeded; VTA static GTFS HEAD succeeded. No claim is made that every listed resource or every current row is usable.
- City GIS layer 126 count query returned an ArcGIS error 500 although layer metadata advertised query support. This is recorded in the layer notes/access guide.
- Older county `mapservices.sccgov.org` and `prod.sccgov.opendata.arcgis.com` hosts failed certificate hostname verification; `webgis.sccgov.org` timed out; a `gis.sccgov.org` directory probe returned 403. TLS verification was not bypassed.
- Many city/county departmental sites and several other publishers rejected automated requests with HTTP 403; authoritative search-index results or official cross-links informed source discovery. The registry retains per-source fetch failures. An HTTP 403 is not evidence the public source has been discontinued.
- A guessed Midpen portal resolved to an ArcGIS shell with `site:null`/404 despite HTTP 200. It was replaced with the officially linked `opendata-mrosd.hub.arcgis.com`. An obsolete Caltrans Hub returned 404; the official Caltrans Open Data Inventory and CA state portal are used instead.
- Public PG&E energy downloads can require name/email and terms acknowledgment; 511 requires a token; PeMS/TIMS and some corporate APIs have additional access conditions. These are not anonymous unrestricted open downloads.

## Retention, deduplication and authority

Records are namespaced by source. Exact source IDs are unique within the normalized catalogue; mirrors across systems are deliberately retained to preserve provenance. Use item ID + sublayer, current service/layer URL, source table identifier and dataset description to establish equivalence before combining data. Title equality alone is insufficient. ArcGIS public organization ownership, original publisher and portal hosting are separately represented when the API supplies them.

Full descriptions and resource metadata remain in the machine-readable catalogue; the HTML catalogue uses shortened display excerpts for performance and links to the full JSON. Resource-link counts include alternative formats and service endpoints. They are not download-success counts. Missing license or temporal metadata stays null/unspecified rather than being invented. Source modified time is not the latest observation date.

## Catalogue schema

`catalogue.json` is an object with snapshot date, timezone, counts and `records`. Each record includes `id`, `source`, `provider` (portal/organizational context), `publisher` when supplied, `title`, `kind`, canonical `url`, `description`, `license`/license metadata, created/modified/data-modified times, temporal/spatial metadata, tags, resource links, captured fields, identifiers and caveats. Source-specific fields such as category, owner, orgid, geometry type, query capabilities and record limits are retained when supplied.

`sources.json` is a list of source-family objects: ID, provider, title, topic, official URL, contents, access, formats, geography, temporal coverage, update cadence, license evidence, notes, local checked date and automated HTTP verification result. A landing-page HTTP check is not a test of every advertised capability.

The research manifest contains checksums and request provenance for preserved raw JSON. The metadata-snapshots ZIP preserves exact API responses and request logs. Source HTML pages are not republished in that archive. The installed skill uses the normalized catalogue and registry; the standalone archive is for audit/reconstruction.

## Reuse and refresh

“Open source” properly refers to software; this survey covers public information, with open-license status stated separately. Public reports and proprietary/conditional datasets are included because they are relevant, not because they share one license. Explicit publisher licenses and terms take precedence over catalogue labels. The catalogue does not grant rights in source data.

Refresh public metadata with `scripts/refresh_catalogue.py` into a new directory, read the failure receipts, then search the resulting normalized catalogue. The helper does not discover new organizations or refresh manually written source notes. Re-research source-family URLs, geographic assumptions and terms when doing a new substantive analysis. No recurring automation is installed.
