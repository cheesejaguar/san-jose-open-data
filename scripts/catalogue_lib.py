"""Normalize publisher metadata without downloading underlying observations."""
import datetime,html,re

def plain(value):
    return ' '.join(html.unescape(re.sub(r'<[^>]*>', ' ',str(value or ''))).split())

def iso(value):
    if isinstance(value,(int,float)):
        return datetime.datetime.fromtimestamp(value/(1000 if value>1e11 else 1),datetime.timezone.utc).isoformat().replace('+00:00','Z')
    return value or None

def base(source,provider,id,title,kind,url):
    return dict(id=source+':'+str(id),source=source,provider=provider,publisher=None,title=title,kind=kind,url=url,description='',license=None,created=None,modified=None,data_modified=None,temporal=None,spatial=None,tags=[],resources=[],fields=[],notes=[],identifiers=[])

def ckan(data,source='city-ckan'):
    out=[]
    for p in data['result']['results']:
        a=base(source,'City of San José',p['id'],p['title'],'CKAN package','https://data.sanjoseca.gov/dataset/'+p['name'])
        a.update(publisher=(p.get('organization') or {}).get('title'),description=plain(p.get('notes')),license=p.get('license_title') if p.get('license_id')!='notspecified' else None,license_id=p.get('license_id'),license_url=p.get('license_url'),created=p.get('metadata_created'),modified=p.get('metadata_modified'),temporal=p.get('temporal'),spatial=p.get('spatial'),tags=[t.get('name','') for t in p.get('tags',[])],name=p['name'])
        for r in p.get('resources',[]):
            a['resources'].append(dict(id=r.get('id'),title=r.get('name'),url=r.get('url'),format=r.get('format'),created=r.get('created'),modified=r.get('last_modified'),datastore_active=r.get('datastore_active'),size=r.get('size'),description=plain(r.get('description'))))
        a['identifiers']=[p['id'],p['name']]
        if a['publisher']=='Enterprise GIS':a['notes'].append('Likely mirror of a GIS Hub item. Compare service URL and item/layer ID before combining.')
        out.append(a)
    return out

def socrata(data,views=None,dcat=None):
    vm={v['id']:v for v in (views or [])};dm={x['identifier'].rstrip('/').split('/')[-1]:x for x in (dcat or {}).get('dataset',[])};out=[]
    for r in data['results']:
        p=r['resource'];v=vm.get(p['id'],{});d=dm.get(p['id'],{})
        a=base('county-socrata','County of Santa Clara',p['id'],p['name'],'Socrata '+p['type'],r.get('link') or r['permalink'])
        a.update(publisher=p.get('attribution') or v.get('attribution') or 'County of Santa Clara (department not specified in metadata)',description=plain(p.get('description')),created=p.get('createdAt'),modified=p.get('metadata_updated_at'),data_modified=p.get('data_updated_at'),tags=r.get('classification',{}).get('domain_tags',[]),category=r.get('classification',{}).get('domain_category'),license=v.get('license',{}).get('name') if isinstance(v.get('license'),dict) else v.get('license'),license_id=v.get('licenseId'),provenance=p.get('provenance'),parent_ids=p.get('parent_fxf',[]),view_type=v.get('viewType'),metadata_url='https://data.sccgov.org/api/views/'+p['id']+'.json')
        cols=v.get('columns') or []
        if cols:
            a['fields']=[dict(name=c['fieldName'],label=c.get('name'),type=c.get('dataTypeName'),description=plain(c.get('description'))) for c in cols if not c['fieldName'].startswith(':')]
        else:
            a['fields']=[dict(name=n,type=(p.get('columns_datatype') or ['']*len(p.get('columns_field_name',[])))[i]) for i,n in enumerate(p.get('columns_field_name',[]))]
        a['resources']=[dict(title=x.get('title') or x.get('mediaType'),url=x.get('downloadURL') or x.get('accessURL'),format=x.get('format') or x.get('mediaType')) for x in d.get('distribution',[]) if x.get('downloadURL') or x.get('accessURL')]
        if p['type']=='dataset':
            a['resources'].append(dict(title='SODA resource query candidate (verify backing type)',url='https://data.sccgov.org/resource/'+p['id']+'.json',format='JSON'))
        if v.get('blobId'):
            a['resources'].append(dict(title=v.get('blobFilename') or 'Hosted source file',url='https://data.sccgov.org/api/views/'+p['id']+'/files/'+v['blobId']+'?download=true',format=v.get('blobMimeType'),size=v.get('blobFileSize')))
            a['notes'].append('Hosted file MIME labels may not describe actual content; inspect the file signature/schema. Pricing JSON is not necessarily GeoJSON.')
        for ap in v.get('metadata',{}).get('additionalAccessPoints',[]):
            for label,url in ap.get('urls',{}).items():a['resources'].append(dict(title=label,url=url,format='External link'))
        if not a['license']:a['notes'].append('No explicit license field in captured county view metadata. Public visibility does not establish unrestricted reuse.')
        a['identifiers']=[p['id']]
        out.append(a)
    return out

def dcat(data,source,provider):
    out=[]
    for i,p in enumerate(data.get('dataset',[])):
        ident=p.get('identifier',str(i));a=base(source,provider,ident,p.get('title','Untitled'),'DCAT entry',p.get('landingPage') or ident)
        a.update(publisher=(p.get('publisher') or {}).get('name'),description=plain(p.get('description')),license=p.get('license') or None,created=p.get('issued'),modified=p.get('modified'),temporal=p.get('temporal'),spatial=p.get('spatial'),tags=p.get('keyword',[]))
        a['resources']=[dict(title=r.get('title'),url=r.get('downloadURL') or r.get('accessURL'),format=r.get('format') or r.get('mediaType')) for r in p.get('distribution',[]) if r.get('downloadURL') or r.get('accessURL')]
        a['identifiers']=[ident]
        if provider=='VTA':a['notes'].append('Portal may include third-party reference data; inspect publisher and service owner.')
        out.append(a)
    return out

def arcgis(data,source,provider):
    out=[]
    for p in data.get('items',[]):
        a=base(source,provider,p['id'],p['title'],'ArcGIS '+p['type'],'https://www.arcgis.com/home/item.html?id='+p['id'])
        a.update(publisher=p.get('accessInformation') or None,description=plain(p.get('description') or p.get('snippet')),license=plain(p.get('licenseInfo')) or None,created=iso(p.get('created')),modified=iso(p.get('modified')),spatial=p.get('extent'),tags=p.get('tags',[]),owner=p.get('owner'),orgid=p.get('orgId') or data.get('orgid'),access=p.get('access'))
        if p.get('url'):a['resources']=[dict(title='Published item URL',url=p['url'],format=p['type'])]
        a['identifiers']=[p['id']]
        a['notes'].append('Public organization index: may be an application, draft, test copy, archive or third-party reference. Index visibility does not validate production use, query availability or an open license.')
        out.append(a)
    return out

def city_layers(data):
    out=[]
    for p in data.get('layers',[])+data.get('tables',[]):
        u='https://geo.sanjoseca.gov/server/rest/services/OPN/OPN_OpenDataService/MapServer/'+str(p['id'])
        a=base('city-rest-layers','City of San José',p['id'],p['name'],'ArcGIS REST '+p.get('type','Layer'),u)
        a.update(publisher='City of San José GIS',description=plain(p.get('description')),spatial=p.get('extent'),geometry_type=p.get('geometryType'),capabilities=p.get('capabilities'),max_record_count=p.get('maxRecordCount'),advanced_query_capabilities=p.get('advancedQueryCapabilities'),data_modified=(p.get('editingInfo') or {}).get('lastEditDate'))
        a['fields']=[dict(name=c['name'],label=c.get('alias'),type=c.get('type'),domain=c.get('domain')) for c in p.get('fields',[])]
        a['resources']=[dict(title='Layer metadata',url=u+'?f=pjson',format='JSON'),dict(title='Query endpoint (verify availability/capabilities)',url=u+'/query',format='ArcGIS REST')]
        a['identifiers']=[u];a['notes'].append('Schema captured. Query capability in metadata is not a successful data query; representative layer 126 count query returned ArcGIS error 500 during audit.')
        out.append(a)
    return out

def normalize(raw):
    out=[]
    if 'city_ckan' in raw:out+=ckan(raw['city_ckan'])
    if 'county_socrata' in raw:out+=socrata(raw['county_socrata'],raw.get('county_views'),raw.get('county_dcat'))
    dcats={'city_gis_dcat':('city-gis-hub','City of San José'),'county_planning_dcat':('county-planning-hub','County Planning and Development'),'vta_dcat':('vta-hub','VTA'),'valleywater_dcat':('valleywater-hub','Valley Water')}
    for key,(source,provider) in dcats.items():
        if key in raw:out+=dcat(raw[key],source,provider)
    orgs={'city':('city-arcgis','City of San José'),'county_central':('county-central-arcgis','County of Santa Clara'),'county_planning':('county-planning-arcgis','County Planning and Development'),'vta':('vta-arcgis','VTA'),'valleywater':('valleywater-arcgis','Valley Water'),'sjwater':('sjwater-arcgis','San Jose Water')}
    for k,(source,provider) in orgs.items():
        if k+'_arcgis' in raw:out+=arcgis(raw[k+'_arcgis'],source,provider)
    if 'city_gis_layers' in raw:out+=city_layers(raw['city_gis_layers'])
    return out
