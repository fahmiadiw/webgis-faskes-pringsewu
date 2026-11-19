import sys, pandas as pd, geopandas as gpd
vil, tsv = sys.argv[1:3]
v = gpd.read_file(vil); v = v[v.regency_code=='id1810']
v['geometry']=v.geometry.make_valid()
kec = v.dissolve(by='district', as_index=False)[['district','geometry']]
print('Kecamatan BPS 2020:', ', '.join(kec.district), '| desa:', len(v))
d = pd.read_csv(tsv, sep='\t')
p = gpd.GeoDataFrame(d, geometry=gpd.points_from_xy(d.lon, d.lat), crs=4326)
j = gpd.sjoin(p, v[['district','village','geometry']], how='left', predicate='within')
for _,r in j.iterrows():
    ok = 'OK ' if isinstance(r.district,str) and r.district.replace(' ','').lower()==r.kecamatan.replace(' ','').lower() else '!! '
    print(f"{ok}{r.nama:28s} tulis={r.kecamatan:16s} peta={r.district if isinstance(r.district,str) else 'DI LUAR PRINGSEWU'} / desa {r.village}")
# nearest-neighbour duplicates
pm = p.to_crs(32748)
for i in range(len(pm)):
    for k in range(i+1,len(pm)):
        dd = pm.geometry.iloc[i].distance(pm.geometry.iloc[k])
        if dd<300: print(f"DEKAT {dd:.0f} m: {pm.nama.iloc[i]} - {pm.nama.iloc[k]}")
