import sys, pandas as pd
d = pd.read_csv(sys.argv[1], sep='\t', dtype={'Kode':str})
d['lvl'] = d.Kode.str.count(r'\.')
kec = {'01':'Pringsewu','02':'Gading Rejo','03':'Ambarawa','04':'Pardasuka','05':'Pagelaran','06':'Banyumas','07':'Adi Luwih','08':'Sukoharjo','09':'Pagelaran Utara'}
d['kec'] = d.Kode.str[6:8].map(kec)
ds = d[d.lvl==3].copy(); kt = d[d.lvl==2].copy()
g = ds.groupby(['kec','Nama']).Jumlah.agg(['count','min','max']).reset_index()
print('desa:', len(g), '| baris per desa:', g['count'].value_counts().to_dict())
s = g.groupby('kec')[['min','max']].sum()
kt['jenis'] = kt.Nama.str.startswith('KECAMATAN').map({True:'B (KECAMATAN ...)',False:'A (nama saja)'})
s = s.join(kt.pivot_table(index='kec', columns='jenis', values='Jumlah'))
print(s.to_string()); print('TOTAL', s.sum().to_dict())
print(g[g.Nama=='SIDODADI'])
g.to_csv(sys.argv[2], index=False)
