import json, numpy as np, pandas as pd, geopandas as gpd
B='/home/claude/webgis-pringsewu/'
d=gpd.read_file(B+'data/desa_full.geojson')
f=pd.read_csv(B+'data/faskes_pringsewu_v1.tsv',sep='\t')
def num(x):
    x=str(x).strip()
    if x in ('-','','nan'): return (None,False)
    return (float(x.replace('~','')), x.startswith('~'))
for c in ['tempat_tidur','dokter','bidan','perawat']:
    f[c+'_est']=f[c].map(lambda x:num(x)[1]); f[c]=f[c].map(lambda x:num(x)[0])
f['rs_umum']=(f.jenis=='rs')&(~f.nama.str.startswith('RSIA'))
fp=gpd.GeoDataFrame(f,geometry=gpd.points_from_xy(f.lon,f.lat),crs=4326).to_crs(32748)
du=d.to_crs(32748); pts=du.geometry.representative_point()
P=np.c_[pts.x,pts.y]; F=np.c_[fp.geometry.x,fp.geometry.y]
D=np.sqrt(((P[:,None,:]-F[None,:,:])**2).sum(-1))/1000  # km
def near(mask):
    idx=np.where(mask)[0]; sub=D[:,idx]; j=sub.argmin(1); return sub.min(1).round(2), [fp.nama.iloc[idx[k]] for k in j]
d['jarak_pkm'],d['pkm_terdekat']=near(f.jenis=='puskesmas')
d['jarak_fktp'],d['fktp_terdekat']=near(f.jenis.isin(['puskesmas','klinik_pratama']))
d['jarak_rs'],d['rs_terdekat']=near(f.rs_umum)
d['jarak_pkm_ri'],_=near((f.jenis=='puskesmas')&(f.rawat_inap=='ya'))
d['jarak_poned'],_=near((f.jenis=='puskesmas')&(f.poned=='ya'))
w=d.penduduk; T=w.sum()
def cov(col,km): return round(w[d[col]<=km].sum()/T*100,1)
stats={'total_pend':int(T),'n_desa':int((d.penduduk>0).sum()),'luas':round(float(d.luas_km2.sum()),1),
 'cov_pkm3':cov('jarak_pkm',3),'cov_pkm5':cov('jarak_pkm',5),'cov_rs5':cov('jarak_rs',5),'cov_rs10':cov('jarak_rs',10),'cov_rs15':cov('jarak_rs',15),
 'avg_rs':round(float((d.jarak_rs*w).sum()/T),1),'avg_pkm':round(float((d.jarak_pkm*w).sum()/T),1),'avg_poned':round(float((d.jarak_poned*w).sum()/T),1),
 'pend_rs_gt15':int(w[d.jarak_rs>15].sum()),'pend_pkm_gt5':int(w[d.jarak_pkm>5].sum())}
# beban puskesmas (model wilayah = puskesmas terdekat)
pk=f[f.jenis=='puskesmas'].copy()
agg=d.groupby('pkm_terdekat').agg(desa=('desa','count'),penduduk=('penduduk','sum'),jarak_maks=('jarak_pkm','max')).reset_index().rename(columns={'pkm_terdekat':'nama'})
pk=pk.merge(agg,on='nama',how='left')
pk['pend_per_dokter']=(pk.penduduk/pk.dokter).round(0); pk['pend_per_bidan']=(pk.penduduk/pk.bidan).round(0)
print(pk[['nama','kecamatan','rawat_inap','desa','penduduk','jarak_maks','dokter','pend_per_dokter','pend_per_bidan']].sort_values('penduduk',ascending=False).to_string())
# RS
rs=f[f.jenis=='rs'][['nama','kecamatan','tempat_tidur','dokter']]
beds=f[f.rs_umum].tempat_tidur.sum(); stats['tt_rs_umum']=int(beds); stats['tt_per_1000']=round(beds/T*1000,2)
stats['tt_all']=int(f[f.jenis=='rs'].tempat_tidur.sum())
# kandidat lokasi faskes rujukan baru (greedy: kurangi rata2 jarak berbobot penduduk ke RS umum)
cur=d.jarak_rs.values; Pd=np.sqrt(((P[:,None,:]-P[None,:,:])**2).sum(-1))/1000
gain=[(w.values*(cur-np.minimum(cur,Pd[:,i]))).sum() for i in range(len(d))]
order=np.argsort(gain)[::-1]
cand=[]; seenk=set()
for i in order:
    k=d.kecamatan.iloc[i]
    if k in seenk: continue
    seenk.add(k); new=np.minimum(cur,Pd[:,i])
    cand.append({'desa':d.desa.iloc[i],'kecamatan':k,'avg_baru':round(float((new*w).sum()/T),1),
      'pend_turun_gt15':int(w[(cur>15)&(new<=15)].sum()),'pend_dalam10':int(w[(cur>10)&(new<=10)].sum()),
      'lat':round(float(gpd.GeoSeries([pts.iloc[i]],crs=32748).to_crs(4326).y[0]),5),'lon':round(float(gpd.GeoSeries([pts.iloc[i]],crs=32748).to_crs(4326).x[0]),5)})
    if len(cand)==3: break
stats['kandidat']=cand
print(json.dumps(stats,indent=1,ensure_ascii=False))
print(d.groupby('kecamatan').apply(lambda s: pd.Series({'pend':s.penduduk.sum(),'avg_rs':round((s.jarak_rs*s.penduduk).sum()/s.penduduk.sum(),1),'avg_pkm':round((s.jarak_pkm*s.penduduk).sum()/max(s.penduduk.sum(),1),1)})).sort_values('avg_rs').to_string())
d.to_file(B+'data/desa_analisis.geojson',driver='GeoJSON',COORDINATE_PRECISION=5)
fo=f.drop(columns=[]).merge(pk[['nama','desa','penduduk','jarak_maks','pend_per_dokter','pend_per_bidan']],on='nama',how='left')
fo.to_csv(B+'data/faskes_analisis.csv',index=False)
json.dump(stats,open(B+'data/stats.json','w'),ensure_ascii=False,indent=1)
