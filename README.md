# Akses Fasilitas Kesehatan Kabupaten Pringsewu

WebGIS analisis jangkauan dan kapasitas fasilitas kesehatan di 131 desa Kabupaten Pringsewu, Lampung: dari klinik pratama dan puskesmas sampai rumah sakit.

**Demo:** `https://<username-github>.github.io/<nama-repo>/`

## Pertanyaan bisnis

1. Seberapa jauh warga tiap desa dari puskesmas dan rumah sakit?
2. Puskesmas mana yang bebannya paling berat dibanding tenaga yang dimiliki?
3. Kalau dibangun satu atau dua faskes rujukan baru, di mana dampaknya paling besar?

## Temuan utama

- **Layanan dasar relatif merata.** 89,9% penduduk tinggal ≤ 5 km dari puskesmas, rata-rata 2,7 km.
- **Layanan rujukan timpang.** Kelima RS umum berada di Kecamatan Pringsewu. 20,3% penduduk tinggal lebih dari 10 km dari RS umum, dan 27.231 jiwa lebih dari 15 km. Rata-rata jarak ke RS di Pagelaran Utara 13,3 km, Adi Luwih 13,1 km, Pardasuka 12,4 km.
- **Beban puskesmas tidak seimbang.** Puskesmas Bandung Baru (44.522 jiwa/dokter) dan Rejosari (43.830 jiwa/dokter) menanggung sekitar 7 kali beban Puskesmas Sukoharjo dan Adiluwih.
- **Pagelaran Utara paling terisolasi.** Satu puskesmas non rawat inap dengan 1 dokter, desa terjauh 14 km.

## Rekomendasi

| Urutan | Area kandidat | Rata-rata jarak ke RS | Penduduk ≤ 10 km dari RS |
|---|---|---|---|
| Saat ini | – | 6,8 km | 79,7% |
| 1 | Desa Waringinsari Barat, Kec. Sukoharjo | 5,6 km | 89,7% |
| 2 | Desa Kresnomulyo, Kec. Ambarawa | 4,6 km | 94,6% |

Kandidat menunjukkan area, bukan alamat. Bentuknya bisa RS tipe D, klinik utama dengan spesialis dasar, atau peningkatan puskesmas rawat inap terdekat.

## Data

| Data | Sumber |
|---|---|
| Penduduk per desa (131 desa) | Disdukcapil Kab. Pringsewu via portal PRIMA |
| Titik 21 faskes, status rawat inap/PONED, tenaga | Dikumpulkan dan diverifikasi manual |
| Batas desa dan kecamatan | BPS 2020 via HDX (repo `JfrAziz/indonesia-district`) |

## Metode

1. **Validasi titik faskes:** setiap koordinat diuji *point-in-polygon* terhadap batas kecamatan BPS. 4 titik yang jatuh di luar kabupaten (Pesawaran dan Lampung Tengah) dikoreksi.
2. **Pencocokan nama desa:** 131 desa dicocokkan antara data Disdukcapil dan peta BPS. 10 nama berbeda ejaan dicocokkan manual (mis. Fajaresuk = Pajar Esuk). Desa kembar (Sidodadi di Pardasuka dan Pagelaran) dibedakan dengan kode wilayah.
3. **Pemisahan periode data penduduk:** sumber memuat dua periode tanpa label. Angka per desa diuji terhadap total kecamatan kedua periode; dipakai periode yang lebih baru (selisih 77 jiwa, 0,02%).
4. **Jarak:** garis lurus dari titik tengah desa ke faskes terdekat, di proyeksi UTM 48S (EPSG:32748).
5. **Wilayah layanan puskesmas:** model puskesmas terdekat, lalu dihitung penduduk per dokter dan per bidan.
6. **Lokasi kandidat:** algoritma *greedy* yang memilih desa paling menurunkan rata-rata jarak berbobot penduduk ke RS umum, dua tahap.

## Keterbatasan

- Jarak garis lurus, bukan waktu tempuh lewat jalan (rencana versi 2: jaringan jalan OSM).
- Wilayah layanan adalah model, bukan wilayah kerja resmi Dinas Kesehatan.
- Kapasitas RS (tempat tidur, tenaga) masih perkiraan dan ditandai di peta.
- Baru 2 klinik pratama yang terpetakan.

## Struktur

```
index.html                         # aplikasi (Leaflet, data tertanam)
data/faskes_pringsewu_v1.tsv       # titik faskes terverifikasi
data/penduduk_desa_pringsewu.csv   # penduduk per desa
data/desa_analisis.geojson         # desa + jarak ke faskes
data/faskes_analisis.csv           # faskes + beban
data/stats.json                    # ringkasan & kandidat lokasi
scripts/                           # skrip pengolahan Python
src/template.html                  # sumber halaman
```

## Publikasi ke GitHub Pages

1. Buat repo baru, upload semua isi folder ini.
2. **Settings → Pages**, pilih branch `main`, folder `/ (root)`, **Save**.
3. Situs aktif dalam 1–2 menit.

---
Fahmi Adi Wicaksono · Data Analyst & Geomatics Engineer
