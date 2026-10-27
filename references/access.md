# Access recipes and metadata refresh

These recipes are for public reads. Examples are discovery/query patterns, not claims that every source endpoint is operational. Record request time and inspect HTTP and application-level errors.

## City CKAN

- Catalogue: https://data.sanjoseca.gov/
- Enumerate packages: `https://data.sanjoseca.gov/api/3/action/package_search?rows=100&start=0&sort=name%20asc`
- Next page: increment `start` by returned rows until the reported `count` is reached. This audit received all **170** packages in one `rows=1000` response.
- Resolve a package: `/api/3/action/package_show?id=<name-or-uuid>`.
- Retrieve its actual resource URLs from `result.resources`; do not construct yearly filenames or treat the package page as a CSV.
- Use DataStore SQL/search only if that resource’s `datastore_active` and live endpoint support it. Static resource downloads are common.
- In this snapshot: **17 CC0, 152 CC BY, one unspecified**. The CC BY packages are the GIS mirror group; do not apply one city-wide license assumption to every item.
- `metadata_modified`, resource `last_modified`, reporting year and the latest row date are different. Recent permit files are rolling snapshots; archive source version and retrieval date when used.

A bounded discovery read using only Python’s standard library:

```python
import json, urllib.parse, urllib.request
base = 'https://data.sanjoseca.gov/api/3/action/'
url = base + 'package_show?' + urllib.parse.urlencode({'id': '311-service-request-data'})
with urllib.request.urlopen(url, timeout=45) as response:
    result = json.load(response)
assert result['success']
resources = result['result']['resources']
# Choose the requested year and actual CSV URL from resources before downloading.
```

Do not download all police/fire/311 years just to inspect columns. Those resources can be large. A current resource-header check is a more appropriate first operation.

## County Socrata

- Discovery catalogue: `https://api.us.socrata.com/api/catalog/v1?domains=data.sccgov.org&limit=1000&offset=0`.
- Follow `offset` and `resultSetSize`; check unique resource IDs. Audit response contained **1,806** resources, all marked official in the captured discovery metadata.
- View metadata/schema: `https://data.sccgov.org/api/views/<four-four-id>.json`.
- All public view metadata: `https://data.sccgov.org/api/views.json` (1,806 in audit).
- DCAT: `https://data.sccgov.org/data.json` (**1,737**, fewer than discovery/view inventories).
- Supported tabular SODA query pattern: `https://data.sccgov.org/resource/<id>.json?...`.
- Bulk CSV export pattern, after checking item support: `/api/views/<id>/rows.csv?accessType=DOWNLOAD`.
- Hosted files are separate assets; use their DCAT distribution or `blobId` download link from view metadata. A file MIME label of `application/vnd.geo+json` may actually contain health-plan pricing JSON, not a geographic feature collection.

An anonymous count query successfully tested in the audit:

```python
import json, urllib.parse, urllib.request
params = {'$select': 'count(*)'}
url = 'https://data.sccgov.org/resource/vuw7-jmjk.json?' + urllib.parse.urlencode(params)
with urllib.request.urlopen(url, timeout=45) as response:
    count = json.load(response)
```

For an extract, select needed columns and a bounded `$where`; choose an explicit stable order based on verified fields, and paginate until completion. Offset pagination on changing source data can skip/duplicate rows; use keyset pagination or a fixed export/snapshot where practical. Do not interpret a successful discovery request as validation that every asset supports `/resource`. Public views, maps, external links, files and stories need their own access routes. Anonymous throttling can occur; use a user-provided application token if needed, keep it out of files/logs, and respect published limits.

For food-inspection join details, read [domains.md](domains.md). The inspection field is **`inpsection_id`**, not `inspection_id`, in captured INSPECTIONS metadata. Most dates/scores/coordinates in those source tables are text; parse and validate explicitly.

## ArcGIS Hub, organizations and REST

Verified public GIS organization IDs:

| Organization | ID | Public item count in audit |
|---|---|---:|
| City of San José | `6kSayNlqm3HvsYZ8` | 1,042 |
| County central GIS | `NkcnS0qk4w2wasOJ` | 457 |
| County Planning and Development | `tcv2cMrq63AgvbHF` | 417 |
| VTA | `cEcV2eKpmBtlBVpA` | 471 |
| Valley Water | `9KdAx8qBsHiGXOEw` | 206 |
| San Jose Water | `ixApgzWW1LUCWXMY` | 101 |

These are **public item** counts, including apps/images/forms/documents/maps and duplicate/test layers, not counts of distinct open databases. Rehosted third-party content has its own publisher and terms.

- Search organization: `https://www.arcgis.com/sharing/rest/search?f=json&q=orgid:<ID>%20AND%20access:public&num=100&start=1`. Follow `nextStart` until `-1`; retain and reconcile `total`. Search cannot expose private items and has a 10,000-result ceiling; partition if ever reached.
- Item metadata: `https://www.arcgis.com/sharing/rest/content/items/<item-id>?f=pjson`.
- Item config: same path with `/data?f=pjson`; useful to resolve the service referenced by a current official app.
- Hub metadata feed: `<hub-origin>/api/feed/dcat-us/1.1.json`. Captured city GIS 152, County Planning 70, VTA 97, Valley Water 25. Hub feeds can include sublayers, documents and apps.
- City service: `https://geo.sanjoseca.gov/server/rest/services/OPN/OPN_OpenDataService/MapServer`.
- All city layer schemas: service path + `/layers?f=pjson` (**151** layers, no separately listed tables in this response).
- VTA directory: `https://gis.vta.org/gis/rest/services/`; Hosted and thematic folders expose additional technical discovery beyond the Hub.

Inspect a layer’s `capabilities`, `fields`, `objectIdField`, `geometryType`, `spatialReference`, `maxRecordCount`, `advancedQueryCapabilities`, `editingInfo` and service URL. Check service and item licensing/copyright. Public queries commonly use `/query` with `where`, selected `outFields`, `returnGeometry`, `f=json` or `f=geojson`, and `outSR=4326` when supported. Encode query parameters with a URL library. Only request geometry when needed.

For a complete large extract, request `returnCountOnly=true` and/or `returnIdsOnly=true`, then batch verified object IDs, or paginate with `resultOffset`/`resultRecordCount` and a stable object-ID order if pagination is supported. Reconcile counts/IDs and inspect `exceededTransferLimit`; a single response is often truncated. Some services expose only maps/tiles, some require authentication, and an ArcGIS HTTP 200 may contain `error` JSON.

**Audit failure:** city layer `126` (Police Stations) returned ArcGIS error code `500`, “Error performing query operation,” despite advertising Query capability. Schema discovery succeeded. Do not extrapolate this failure to all layers, but do not claim that the entire service was data-query tested.

The city root service reports spatial reference `102643` / EPSG **2227**, NAD83 California zone 3 in US survey feet. Individual layers/exports may differ. Reproject correctly before using metre distances or combining WGS84 coordinates; preserve vertical datum separately for elevation. The service root extent can be distorted by bad/outlier geometries and is not a reliable city boundary.

Older county hosts found in published metadata had problems during this audit: `mapservices.sccgov.org` and `prod.sccgov.opendata.arcgis.com` failed certificate hostname checks, `webgis.sccgov.org` timed out, and a guessed `gis.sccgov.org/arcgis/rest/services` endpoint returned 403. Do not disable TLS verification. Prefer current county Socrata, verified ArcGIS Online items, Planning Hub or official current Map Viewer links. Legacy links remain in raw metadata for audit purposes, not as endorsed live endpoints.

## Transit and conditional-access sources

- VTA schedule: https://gtfs.vta.org/ and https://gtfs.vta.org/gtfs_vta.zip ; HEAD request succeeded during audit.
- 511: https://511.org/open-data ; free token required; use current docs for operators, GTFS, trip updates, vehicle positions, alerts and traffic endpoints. Attribution is required. Never include a real API key in a redistributable catalogue.
- PG&E public energy downloads: https://pge-energydatarequest.com/public_datasets ; guide at https://pge-energydatarequest.com/user-guide describes name/email and terms acknowledgement, quarterly ZIP/CSV releases and merged ZIP confidentiality. The catalogue does not submit those details.
- Registered PeMS/TIMS, platform-account Earth Engine, PurpleAir API points, PG&E limited-access GIS and customer-consent energy/water portals have different access models. Use their exact source-family record; do not label them anonymous open downloads.

## Refresh helper

```bash
python3 <skill-directory>/scripts/refresh_catalogue.py --help
python3 <skill-directory>/scripts/refresh_catalogue.py \
  --source city_ckan --source county_socrata \
  --output <new-empty-work-directory>
python3 <skill-directory>/scripts/search_catalogue.py \
  --catalogue <new-empty-work-directory>/catalogue.json permits
```

Requires Python 3.9+ standard library and authorized public internet access; no external Python packages. Metadata-only harvest uses at most three concurrent source workers and up to three attempts per failing request. It writes a new snapshot and returns nonzero if any requested source fails. It checks paging totals for CKAN/Socrata/ArcGIS; reports failure rather than silently claiming a partial scrape is complete. Portal contents can change while paging. Use the receipt URLs and raw snapshots to investigate a mismatch.

The helper does not refresh the manually curated source-family notes, inspect every data-resource URL, enumerate all sublayers in all organization services, or discover new providers. Those require targeted research. To update the installed snapshot, first review the new receipts and catalogue and then explicitly replace references; automatic refresh never mutates the installed skill or third-party services.
