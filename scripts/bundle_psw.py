import json, pandas as pd, geopandas as gpd, numpy as np
B='/home/claude/webgis-pringsewu/'
d=gpd.read_file(B+'data/desa_analisis.geojson')
d['geometry']=d.geometry.simplify(0.0004,preserve_topology=True)
f=pd.read_csv(B+'data/faskes_analisis.csv')
s=json.load(open(B+'data/stats.json'))
k=d.dissolve(by='kecamatan',as_index=False)[['kecamatan','geometry']]
k['geometry']=k.geometry.boundary.simplify(0.0004)
w=d.penduduk
kt=d.groupby('kecamatan').apply(lambda x: pd.Series({'penduduk':int(x.penduduk.sum()),'desa':int((x.penduduk>0).sum()),'luas':round(float(x.luas_km2.sum()),1),
   'avg_pkm':round(float((x.jarak_pkm*x.penduduk).sum()/x.penduduk.sum()),1),'avg_rs':round(float((x.jarak_rs*x.penduduk).sum()/x.penduduk.sum()),1),
   'maks_rs':round(float(x.jarak_rs.max()),1)}),include_groups=False).reset_index()
kt['puskesmas']=kt.kecamatan.map(lambda n: int(((f.jenis=='puskesmas')&(f.kecamatan.str.replace(' ','').str.lower()==n.replace(' ','').lower())).sum()))
keep=['kode','kecamatan','desa','penduduk','luas_km2','kepadatan','jarak_pkm','pkm_terdekat','jarak_fktp','fktp_terdekat','jarak_rs','rs_terdekat','jarak_poned']
d=d[keep+['geometry']]
fx=f.replace({np.nan:None}).to_dict('records')
out={'desa':json.loads(d.to_json(drop_id=True)),'kec':json.loads(k.to_json(drop_id=True)),'faskes':fx,'stats':s,'kec_tabel':kt.to_dict('records')}
js=json.dumps(out,ensure_ascii=False,separators=(',',':'))
# round coords
import re
js=re.sub(r'(\d+\.\d{5})\d+',r'\1',js)
open(B+'data/bundle.json','w').write(js); print(len(js)); print(kt.to_string())
