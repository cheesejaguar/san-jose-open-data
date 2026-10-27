# San José Open Data

A Codex skill and searchable public-data catalogue for San José and Santa Clara County, including local government departments, regional agencies, utilities and relevant corporate datasets.

**[Browse the public catalogue](https://cheesejaguar.github.io/san-jose-open-data/)**

The research snapshot is dated **26 October 2026 (America/Los_Angeles)** and contains **113 researched source families** and **5,165 indexed metadata records**. Those records include overlapping GIS mirrors, applications, archives and recurring releases; they are not 5,165 distinct open-licensed databases. Access conditions, source licensing evidence, geography, field definitions, failed endpoints and coverage limits are documented individually.

## Install the Codex skill

Clone this repository into your personal Codex skills directory:

```bash
git clone https://github.com/cheesejaguar/san-jose-open-data.git \
  "${CODEX_HOME:-$HOME/.codex}/skills/san-jose-open-data"
```

The command requires that the destination does not already exist. If you already installed the standalone skill, keep your existing copy or review the repository before replacing it.

Invoke it in Codex with `$san-jose-open-data`, for example:

> Use $san-jose-open-data to find San José permit and parcel datasets, explain their coverage, and avoid double counting.

The skill entrypoint is [SKILL.md](SKILL.md). Its helpers require **Python 3.9+ and the standard library only**. No accounts, API keys or recurring automations are created by installation.

## Search locally

From the repository directory:

```bash
python3 scripts/search_catalogue.py water --sources
python3 scripts/search_catalogue.py ridership --provider VTA
python3 scripts/search_catalogue.py --id vuw7-jmjk --full
```

Search terms are ANDed and accent-insensitive. Add `--json`, `--provider`, `--source`, `--kind`, `--id` or `--limit` as needed. Source-family search uses `--sources`; the default searches the full metadata catalogue.

## Refresh metadata

Write a fresh, metadata-only snapshot into a new or empty directory:

```bash
python3 scripts/refresh_catalogue.py --output /tmp/san-jose-metadata-new
python3 scripts/search_catalogue.py \
  --catalogue /tmp/san-jose-metadata-new/catalogue.json permits
```

Use `--help` for individual sources. The refresh helper follows pagination, records errors and returns nonzero when a requested source is incomplete. It does not overwrite the installed catalogue, discover every new provider, update the authored source notes or download the underlying observation tables. Review fresh receipts before replacing bundled references.

## Catalogue and research files

- [Searchable catalogue](https://cheesejaguar.github.io/san-jose-open-data/): overview, source families, item inventory, domain guidance and coverage notes.
- [Full metadata JSON](docs/catalogue.json) and [source-family registry](docs/sources.json).
- [Raw public metadata snapshots](docs/metadata-snapshots.zip) and [research manifest](docs/research-manifest.json), including checksums and failed probes.
- [Standalone skill ZIP](docs/san-jose-open-data.zip).
- [Source-selection guidance](references/domains.md), [access recipes](references/access.md) and [coverage/methodology](references/coverage.md).

The HTML page works offline when opened locally. Download links require the corresponding files alongside it. The published GitHub Pages site uses `docs/index.html` and the assets in `docs/`, with `.nojekyll` to serve the static files directly.

## Updating the published site

GitHub Pages publishes the **`main` branch’s `/docs` folder**. Commit and push reviewed changes there to update the site. The skill at the repository root and the website/download copies should be kept in sync when updating the snapshot. There is no scheduled data refresh or publishing automation beyond GitHub’s standard Pages build.

## Licensing and provenance

The project’s original helper code, HTML interface, skill instructions and authored documentation are provided under the [MIT License](LICENSE). **Third-party source metadata, raw API responses and underlying datasets are excluded from that grant** and remain subject to their original publishers’ terms. No blanket open-data license is asserted for the catalogue’s source materials. Recheck the selected publisher’s live license/access conditions before reuse or redistribution; public visibility is not proof of unrestricted reuse.

No private customer, patient, tenant or voter database was accessed. The repository contains catalogue metadata and research, not the underlying bulk observation databases. See the coverage reference for the precise enumeration scope, duplication and known access failures.
