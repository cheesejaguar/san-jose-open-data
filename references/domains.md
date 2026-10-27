# Local source selection and interpretation

Contents: local government; land and housing; transport; safety/health; water; energy; environment; corporate and regional complements.

## Local government and geographic scope

The City of San José is an incorporated municipality. Santa Clara County publishes countywide administrative data, sheriff-service data and unincorporated-area planning data; these scopes differ. The City of Santa Clara is another municipality. VTA and Valley Water are separate special districts; San Jose Water is an investor-owned water utility. MTC/ABAG and the Bay Area Air District cover the broader region. County Office of Education, Midpen and the Open Space Authority are separate entities.

Start with city CKAN, county Socrata and the appropriate GIS Hub, then search departmental sources. For legislative matters, use the city Legistar calendar/matters and attachments. For city campaign contributions/expenditures and lobbyists, use the Clerk’s current Campaign Reports page; its filing system changed in December 2025, so historical third-party portal links may be obsolete. Public lookup and document systems may have no verified bulk API.

Budget reporting distinguishes proposed, recommended, adopted, revised and actual amounts, and city/county fiscal years run July–June. City CKAN Employee Compensation Plans is not employee-level actual compensation. Use source-specific payroll releases or State Controller public compensation data when that is the question. County VHP monthly pricing files greatly inflate portal file counts; do not describe every file as a separate operational database.

## Land, permits, housing and property

Use city permit CSVs for bounded bulk extracts, SJPermits for record-level permit status/history, and city GIS for zoning, General Plan, growth areas, vacant land, development footprints and affordable housing. Six city permit extract packages cover recent planning, recent building, active, expired and under-inspection records. These overlap and are not a complete immutable event history. Capture extract date and determine what each date/status means.

County Planning permits/zoning primarily govern unincorporated territory. City permits inside incorporated San José are a separate dataset. County parcel geometry and addresses support spatial joins; assessment lookup supplies assessment-year attributes under its own restrictive terms. Assessed value is not sale price or market value. A parcel is not a building, dwelling unit or business. APNs can change after splits/merges; retain punctuation and leading zeros in the original and a documented normalized key.

For housing production, distinguish entitled units, issued permits, starts, completions and occupied units. Combine city housing dashboards, HCD Annual Progress Reports and Census/DOF only after aligning dates and geography. Affordable-housing directories are programme/property inventories, not all affordable housing or individual tenant records.

For homelessness, distinguish PIT snapshot estimates, HMIS service cohorts and housing-system outcomes. A household, person, placement and episode are not interchangeable. HMIS client-level records and individual rent-registry/tenant cases are not established as public open data.

For corporate market indicators, use Zillow ZHVI/ZORI for model-based value/rent indexes, Redfin for published market measures, and Realtor.com for listing inventories/hotness. Inspect city versus county versus metro, property type, adjustment method, rolling versus calendar period, revisions and publisher terms. The San José metro is not San José city. Realtor.com revised metro definitions with January 2025 releases. Listing prices are not closed sales or executed leases.

## Transit, streets, traffic and mobility

Use VTA’s official static GTFS at https://gtfs.vta.org/gtfs_vta.zip for current schedules; use the data.vta.org Hub for stops/routes, ridership, passenger survey, productivity, high-quality transit corridors and bicycle planning. Some Hub records are apps, documents, component buffers or third-party reference layers. VTA’s October ridership snapshots and route averages do not represent raw every-trip passenger-counter readings or full-year totals.

Use 511 for regional transit/traffic and documented GTFS-Realtime; it requires a free API token and attribution. Confirm operator IDs and realtime capability from current documentation. Regional `RG` consolidated feeds exist, but do not assume all agencies expose all realtime message types. Caltrain and BART publish their own developer resources; ACE and Capitol Corridor are covered in 511’s regional scope. Do not assume stop/trip identifiers match between regional and individual feeds.

GTFS service calendars and exceptions determine whether a trip runs on a given date. A service-day time can exceed `24:00:00`; timestamps cannot be naively parsed as ordinary wall-clock times. Preserve feed version, agency timezone and identifier strings. GTFS vehicle positions, trip predictions and actual ridership are different products.

For road safety, use city crash locations/vehicles and Vision Zero data with explicit event/party/victim grain; SWITRS/TIMS provide state crash data with their own coding, completeness and access terms. County sheriff incidents, city police crime and traffic collisions should not be pooled as interchangeable events.

For traffic, inspect city Average Daily Traffic and Turning Movement Counts, VTA congestion/corridor releases, Caltrans counts and registered PeMS access. Detector traffic, annual averages, sample-day counts and model forecasts differ. Keep station IDs, roadway direction, imputation and detector outage flags. Do not double-count the same corridor across city/VTA/state mirrors.

Lyft/Bay Wheels supplies anonymized trip-history files and GBFS live system data under its own license. Use the current publisher link, which can redirect from older Bay Wheels branding. Filter to city stations/coordinates with a documented origin/destination rule. Current station availability cannot reconstruct historical trips. SJC’s official monthly airport activity reports contain passengers, flight activity and cargo; use flysanjose.com to avoid similarly named unaffiliated or Costa Rica airport sites.

## Health, food safety, sheriff and coroner

County food data is unusually useful for relational examples. Current source IDs:

| Table | Socrata ID | Relevant fields captured 2026-10-26 |
|---|---|---|
| BUSINESS | `vuw7-jmjk` | `business_id`, `name`, `address`, `city`, `postal_code`, `latitude`, `longitude`, `geo_address` |
| INSPECTIONS | `2u2d-8jej` | `business_id`, **`inpsection_id`**, `date`, `score`, `result`, `description`, `type` |
| VIOLATIONS | `wkaa-4ccv` | `inspection_id`, `description`, `code`, `critical` |
| FEED_INFO | `itys-r3sp` | `feed_date`, `feed_version`, `municipality_name`, `municipality_url` |

The inspection key is actually misspelled **`inpsection_id`** in captured INSPECTIONS metadata. Join it to VIOLATIONS.`inspection_id` only after checking current schemas, uniqueness and match rates; do not silently correct an API field name. BUSINESS to INSPECTIONS is one-to-many; inspection to violations is also one-to-many. Aggregate violations before calculating business/inspection-level metrics if necessary. Many numeric/date values are typed as text. The publisher says the current feed is updated daily and contains a rolling two-year window; older annual files are separate and can overlap. Placard status and numeric score are different concepts; an old closure need not be current status.

County sheriff Crime Reports `n9u6-aijz` cover sheriff jurisdiction, not every police agency in the county. City police calls represent incidents, with repeated calls for an incident collapsed, and annual/quarterly files overlap. Calls are not established crimes, arrests or convictions. Crime reporting classifications and methodologies can change.

Medical Examiner-Coroner full dataset `s3fb-yrjp` and thematic datasets/views overlap: fentanyl, opioids, drug deaths, unhoused deaths, suicide, homicide, custody and heat/cold, among others. Do not sum them as mutually exclusive categories. Case finalization, occurrence/residency and investigation jurisdiction matter; the coroner universe is not all-cause resident mortality.

Public Health has respiratory-virus, wastewater, vaccination, HIV/STI/TB, overdose, population assessment and climate-health reports/dashboards. Respect suppressed cells and reporting lags; missing is not zero. Wastewater concentrations describe sampled sewage and sewersheds, not a direct count of infected city residents. WastewaterSCAN is a separate university/research programme with a San José location and its own data-sharing conditions.

County VHP insurer price-transparency files and county hospital standard-charge files are different products. Keep plan/payer/provider and billing-code definitions. Neither is an individual patient medical record or a reliable estimate of that patient’s final bill.

## Water and wastewater

Resolve the retailer first using official provider/service-area geography or address lookup. **San Jose Water, San José Municipal Water System and Great Oaks Water Company are different retailers.** Valley Water is the regional water/flood/groundwater special district and wholesale supplier; California Water Service and SFPUC supply roles add further regional context. City, retail territory, source-water zone and wastewater service area differ.

San Jose Water publishes annual Consumer Confidence Reports, Public Health Goals reporting, UWMP/shortage plans, source map, public service-line materials inventory and main-replacement project maps. Its current service-line Experience ID is `d1d4a56e5b07472fb959a774d7a300d5`. Its public ArcGIS organization ID is `ixApgzWW1LUCWXMY`. The indexed organization includes duplicate/older apps and survey components; prefer the current app linked by the company. Do not collect survey submissions or infer that public map visibility provides an open reuse license. Material classifications and possible goosenecks are not measurements of lead concentration at the tap. Private customer usage portals are not open databases.

The State Water Board also publishes accepted service-line inventories as large county-grouped text files and a dictionary. Santa Clara uses state county number **43**, in the CA39–CA58 group. This is a better bulk-discovery lead than reverse-engineering a public utility lookup. Inspect acceptance dates and material reclassifications; the current retailer inventory may differ from the state snapshot.

Valley Water’s GIS Hub includes creeks, groundwater subbasins, water zones, reservoirs, water bodies, depth-to-first-groundwater, sensors, wells, land/easements and contours. Its ALERT portal provides rainfall and stream/reservoir telemetry. Keep gauge identity, units, observation versus retrieval time, provisional flags and accumulation windows. Stage and discharge are not interchangeable. Groundwater elevation, depth to water and well construction depth have different reference surfaces.

For laboratory water-quality results and system/facility identities, use Water Boards/DWR/EPA structured products as complements, keyed by PWS/station/permit IDs. Consumer Confidence Reports often report ranges and historical sample years; report year can differ from collection year. Wastewater discharge monitoring via CIWQS/ECHO is different from pathogen surveillance. Large elevation products need explicit spatial/size selection: the Valley Water contour record describes a roughly **31 GB** archive from late-2022 LiDAR.

## Energy, connectivity, environment and corporate complements

SJCE, SVCE, Silicon Valley Power and PG&E have different supply/delivery roles and service areas. Power Content Labels describe annual supplier mix and emissions intensity; they are not local hourly generation or city electricity consumption. PG&E’s public energy-data programme publishes monthly usage by ZIP/customer category in quarterly files; confidentiality can merge neighbouring ZIPs. Download may require name/email and terms acknowledgment. Customer Green Button/Share My Data and SVCE’s historical Data Hive require customer authorization; restricted PG&E GIS modules are not an open public utility database. PG&E’s official planning page directs users from legacy ICA/DIDF maps to Grid Resource Integration Portal; do not hard-code a retired map as the canonical source.

For grid/system context, CAISO OASIS and CEC have prices, loads, plants, consumption and power disclosures. Avoid adding delivered energy, supplier sales and generation as if all were consumption. Distributed interconnection capacity is not guaranteed available capacity or project approval.

Use local authoritative GIS for parcels/addresses, hazards, tree canopy, trails, infrastructure and regulatory planning. Supplement with USGS elevation/water, NOAA weather, FEMA effective flood maps, CAL FIRE hazards, state environmental data and air-district/EPA monitors. Specify projected units, vertical datum, acquisition date and mapping scale. Flood regulatory zones, modeled flood exposure and live flood observations are different products. For canopy/land cover, imagery classification is not zoning or parcel land use.

Microsoft US building footprints is ODbL; Overture’s themes have source/theme-specific licenses. Google Dynamic World has CC BY 4.0 dataset terms with separate platform access. These are useful corporate-supported geographic complements, not authoritative city planning decisions. Ookla’s public tiles carry **CC BY-NC-SA 4.0**, which restricts commercial reuse; the release describes Parquet/WKT and shapefile, so inspect rather than assuming GeoParquet. Self-selected speed tests do not measure universal availability. FCC/CPUC broadband availability and the separately licensed Fabric are different products. PurpleAir requires checking key/points/pricing and sensor QA rather than treating it as an unrestricted free bulk source.

For local business/economic research, city Business Tax Lookup, county permitted-facility tables, Census/LEHD/BLS/DOF and state business registration provide different universes. SEC EDGAR supplies corporate financial filings for local public companies, but companywide operations are not San José-only measurements. Overture/OSM places are not comprehensive business registration datasets. Joint Venture Silicon Valley indicators are nonprofit synthesis; inspect the underlying source and regional definition.
