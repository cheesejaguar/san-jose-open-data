#!/usr/bin/env python3
"""Search the local metadata snapshot; no network access or data-row downloads."""
import argparse,json,pathlib,re,sys,unicodedata
ROOT=pathlib.Path(__file__).resolve().parents[1]
def fold(x):
    return ''.join(c for c in unicodedata.normalize('NFKD',str(x)) if not unicodedata.combining(c)).lower()
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('query',nargs='?',default='');p.add_argument('--sources',action='store_true',help='Search curated source families instead of metadata records')
    p.add_argument('--provider',default='');p.add_argument('--source',default='');p.add_argument('--kind',default='');p.add_argument('--id',default='')
    p.add_argument('--limit',type=int,default=12);p.add_argument('--full',action='store_true');p.add_argument('--json',action='store_true')
    p.add_argument('--catalogue',type=pathlib.Path,help='Alternative catalogue JSON (for a refreshed snapshot)')
    a=p.parse_args()
    if a.limit<1 or a.limit>500:p.error('--limit must be between 1 and 500')
    path=a.catalogue or ROOT/'references'/('sources.json' if a.sources else 'catalogue.json')
    d=json.loads(path.read_text());rows=d if isinstance(d,list) else d['records'];terms=re.findall(r'[\w-]+',fold(a.query));found=[]
    for r in rows:
        if a.provider and fold(a.provider) not in fold(r.get('provider','')):continue
        if a.source and fold(a.source) not in fold(r.get('source','')):continue
        if a.kind and fold(a.kind) not in fold(r.get('kind','')):continue
        if a.id and fold(a.id) not in fold(json.dumps([r.get('id'),r.get('identifiers')])):continue
        title=fold(r.get('title',''));body=fold(json.dumps(r,ensure_ascii=False))
        if not all(t in body for t in terms):continue
        score=sum(12 if t in title else 1 for t in terms)
        if a.id and (fold(r.get('id',''))==fold(a.id) or fold(r.get('id','')).endswith(':'+fold(a.id))):score+=100
        if r.get('source')=='county-socrata' or r.get('source')=='city-ckan':score+=2
        if r.get('source')=='city-rest-layers':score+=1
        found.append((score,r))
    found.sort(key=lambda x:(-x[0],x[1].get('title','')));selected=[r for _,r in found[:a.limit]]
    if a.json:
        print(json.dumps({'matched':len(found),'returned':len(selected),'records':selected},ensure_ascii=False,indent=2));return
    stamp = '2026-10-26' if isinstance(d,list) else d.get('snapshot_local_date',d.get('retrieved_at_utc','unspecified'))
    print(f'{len(found)} matches; showing {len(selected)}. Snapshot: {stamp}; verify live availability and terms.')
    for r in selected:
        print('\n'+r['title']+'\n  '+r['id']+'\n  '+r.get('url',''))
        if a.sources:
            keys=['provider','topic','contents','access','formats','geography','temporal_coverage','update_cadence','license','notes','verification']
        else:
            keys=['source','provider','publisher','kind','description','license','data_modified','modified','temporal','spatial','category','notes']
        for k in keys:
            v=r.get(k)
            if v:
                s=v if isinstance(v,str) else json.dumps(v,ensure_ascii=False)
                print('  '+k+': '+(s if a.full else s[:1000]))
        if r.get('resources'):
            for z in r['resources'] if a.full else r['resources'][:6]:print('  resource: '+str(z.get('format') or '')+' | '+str(z.get('title') or '')+' | '+str(z.get('url') or ''))
        if r.get('fields'):print('  fields: '+', '.join(z['name'] for z in r['fields']))
        if a.full:print('  full metadata: '+json.dumps(r,ensure_ascii=False))
if __name__=='__main__':main()
