import re, pandas as pd, geopandas as gpd
B='/home/claude/'
v=gpd.read_file(B+'webgis/raw/id18_lampung_district.geojson'); v=v[v.regency_code=='id1810'].copy()
v['geometry']=v.geometry.make_valid()
g=pd.read_csv(B+'webgis-pringsewu/raw/desa_minmax.csv')
norm=lambda s: re.sub(r'[^a-z0-9]','',s.lower())
alias={'bulokarto':'bulukarto','fajaragung':'pajaragung','fajaresuk':'pajaresuk','sinarmulya':'sinarmulia','sinarwayah':'sinarwaya',
 'tambahrejo':'tambakrejo','tanjungdalom':'tanjungdalam','wargamulyo':'wargomulyo','wayngison':'wayngisom','yogyakarta':'jogyakarta'}
g['k']=g.Nama.map(norm).replace(alias); g['kk']=g.kec.map(norm)
v['k']=v.village.map(norm); v['kk']=v.district.map(norm)
m=v.merge(g[['k','kk','max','min']],on=['k','kk'],how='left')
print('tanpa data:',m[m['max'].isna()][['district','village']].values.tolist())
m['penduduk']=m['max'].fillna(0).astype(int)
m=m.rename(columns={'district':'kecamatan','village':'desa','village_code':'kode'})[['kode','kecamatan','desa','penduduk','geometry']]
m['kode']=m.kode.str[2:]
m['geometry']=m.geometry.buffer(0)
u=m.to_crs(32748); m['luas_km2']=(u.area/1e6).round(2)
m['kepadatan']=(m.penduduk/m.luas_km2).round(0)
print('desa',len(m),'total',m.penduduk.sum(),'luas',round(m.luas_km2.sum(),1))
m.to_file(B+'webgis-pringsewu/data/desa_full.geojson',driver='GeoJSON')
