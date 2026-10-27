#!/usr/bin/env python3
"""Read-only harvest of known public metadata. Writes a new snapshot directory, never overwrites installed references."""
import argparse,concurrent.futures,datetime,hashlib,json,pathlib,time,urllib.parse,urllib.request
from catalogue_lib import normalize
ORGS={'city':'6kSayNlqm3HvsYZ8','county_central':'NkcnS0qk4w2wasOJ','county_planning':'tcv2cMrq63AgvbHF','vta':'cEcV2eKpmBtlBVpA','valleywater':'9KdAx8qBsHiGXOEw','sjwater':'ixApgzWW1LUCWXMY'}
ENDPOINTS={
'city_ckan':'https://data.sanjoseca.gov/api/3/action/package_search',
'county_socrata':'https://api.us.socrata.com/api/catalog/v1',
'county_views':'https://data.sccgov.org/api/views.json',
'county_dcat':'https://data.sccgov.org/data.json',
'city_gis_dcat':'https://gisdata-csj.opendata.arcgis.com/api/feed/dcat-us/1.1.json',
'county_planning_dcat':'https://gisdata-sccplanning.hub.arcgis.com/api/feed/dcat-us/1.1.json',
'vta_dcat':'https://data.vta.org/api/feed/dcat-us/1.1.json',
'valleywater_dcat':'https://data-valleywater.opendata.arcgis.com/api/feed/dcat-us/1.1.json',
'city_gis_layers':'https://geo.sanjoseca.gov/server/rest/services/OPN/OPN_OpenDataService/MapServer/layers?f=pjson'}
def read(url):
    for attempt in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'SanJoseOpenDataMetadata/1.0'}),timeout=60) as r:d=json.load(r)
            if isinstance(d,dict) and d.get('error'):raise ValueError(str(d['error']))
            return d
        except Exception:
            if attempt==2:raise
            time.sleep(attempt+1)
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',required=True,type=pathlib.Path);p.add_argument('--source',action='append',choices=list(ENDPOINTS)+[k+'_arcgis' for k in ORGS],help='Repeat to limit the harvest; default all')
    a=p.parse_args()
    if a.output.exists() and any(a.output.iterdir()):p.error('--output must be new or empty; existing snapshots are preserved')
    a.output.mkdir(parents=True,exist_ok=True);raw={};receipts=[];keys=a.source or list(ENDPOINTS)+[k+'_arcgis' for k in ORGS]
    def harvest(key):
        urls=[]
        if key.endswith('_arcgis'):
            org=ORGS[key[:-7]];items=[];start=1;expected=None
            while start!=-1:
                u='https://www.arcgis.com/sharing/rest/search?'+urllib.parse.urlencode(dict(f='json',q='orgid:'+org+' AND access:public',num=100,start=start,sortField='title',sortOrder='asc'));urls.append(u);d=read(u)
                expected=d['total'] if expected is None else expected;items+=d['results'];start=d['nextStart']
                if len(items)>10000:raise ValueError('ArcGIS search limit reached; partition query instead of claiming completeness')
            if len(items)!=expected:raise ValueError('ArcGIS total changed or paging incomplete; retry snapshot')
            result=dict(orgid=org,total=len(items),items=items)
        elif key=='city_ckan':
            items=[];start=0;expected=None
            while True:
                u=ENDPOINTS[key]+'?'+urllib.parse.urlencode(dict(rows=100,start=start,sort='name asc'));urls.append(u);d=read(u)
                if not d.get('success'):raise ValueError('CKAN failed')
                expected=d['result']['count'] if expected is None else expected;batch=d['result']['results'];items+=batch;start+=len(batch)
                if start>=d['result']['count']:break
                if not batch:raise ValueError('CKAN pagination stalled')
            if len(items)!=expected:raise ValueError('CKAN count changed; retry')
            result={'success':True,'result':{'count':len(items),'results':items}}
        elif key=='county_socrata':
            items=[];offset=0;expected=None
            while True:
                u=ENDPOINTS[key]+'?'+urllib.parse.urlencode(dict(domains='data.sccgov.org',limit=1000,offset=offset));urls.append(u);d=read(u)
                expected=d['resultSetSize'] if expected is None else expected;batch=d['results'];items+=batch;offset+=len(batch)
                if offset>=d['resultSetSize']:break
                if not batch:raise ValueError('Socrata pagination stalled')
            if len({r['resource']['id'] for r in items})!=expected:raise ValueError('Socrata paging duplicate/missing records; retry')
            result={'results':items,'resultSetSize':expected}
        else:
            urls.append(ENDPOINTS[key]);result=read(urls[0])
        b=json.dumps(result,ensure_ascii=False,indent=2).encode();(a.output/(key+'.json')).write_bytes(b)
        return key,result,dict(source=key,urls=urls,status='complete',sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        futures={pool.submit(harvest,key):key for key in keys}
        for f in concurrent.futures.as_completed(futures):
            key=futures[f]
            try:key,result,receipt=f.result();raw[key]=result;receipts.append(receipt);print(key,'complete',flush=True)
            except Exception as e:receipts.append(dict(source=key,status='failed',error=str(e)));print(key,'FAILED',str(e),flush=True)
    records=normalize(raw);stamp=datetime.datetime.now(datetime.timezone.utc).isoformat();out={'retrieved_at_utc':stamp,'scope':'Known public metadata endpoints; no underlying observation tables fetched','complete':all(r['status']=='complete' for r in receipts),'records':records,'receipts':receipts}
    (a.output/'catalogue.json').write_text(json.dumps(out,ensure_ascii=False,indent=2));(a.output/'receipts.json').write_text(json.dumps(receipts,indent=2));print(len(records),'metadata records; complete =',out['complete'])
    if not out['complete']:raise SystemExit(1)
if __name__=='__main__':main()
