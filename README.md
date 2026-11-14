# Sistem Pakar Identifikasi Kualitas dan Kesegaran Telur Ayam Mentah

## Identitas
- Nama: Melani Putri Zahari
- NIM: F1D02410073
- Mata kuliah: Kecerdasan Buatan
- Program studi: Teknik Informatika

## 1. Deskripsi
Proyek ini merupakan sistem pakar sederhana untuk mengidentifikasi klasifikasi mutu fisik telur ayam mentah berdasarkan kondisi cangkang, kekentalan putih telur, bentuk dan posisi kuning telur, kedalaman kantung udara, serta bau telur.

Sistem menggunakan metode **Forward Chaining**, yaitu penalaran yang dimulai dari fakta yang diberikan pengguna, mencocokkan fakta dengan aturan IF–THEN, menyimpan hasil aturan ke memori, lalu mengulang proses sampai tidak ada aturan baru.

> Batasan: sistem hanya mengidentifikasi mutu fisik berdasarkan parameter yang dimasukkan. Sistem tidak dapat memastikan telur bebas Salmonella atau mikroorganisme lain dan bukan pengganti pengujian laboratorium atau seluruh prosedur SNI.

## 2. Sumber Pengetahuan

**S1 — Sumber pemerintah**

Nuraini. (2024, 28 Juni). *Standar Mutu Telur Ayam Konsumsi sesuai SNI 3926:2023*. Balai Penerapan Standar Instrumen Pertanian (BPSIP) Kepulauan Bangka Belitung, Kementerian Pertanian Republik Indonesia.  
Tautan: https://babel.brmp.pertanian.go.id/berita/standar-mutu-telur-ayam-konsumsi-sesuai-sni-3926-2023

Sumber ini digunakan untuk merujuk klasifikasi mutu fisik telur, termasuk kondisi kerabang, kedalaman kantung udara, kekentalan putih telur, bentuk dan posisi kuning telur, serta bau khas telur.

**S2 — Artikel jurnal/prosiding ilmiah**

Baskoro, T. A., Al Amin, M. F., Wijaksono, M. A., & Fadhlurrohman, I. (2026). *Perubahan Kualitas Internal Telur selama Penyimpanan Ditinjau dari Indeks Kuning Telur, Indeks Putih Telur, dan Haugh Unit*. Prosiding Seminar Nasional Pembangunan dan Pendidikan Vokasi Pertanian, 7(1), 1042–1049.  
DOI: https://doi.org/10.47687/snppvp.v7i1.2266  
Tautan artikel: https://jurnal.polbangtanmanokwari.ac.id/index.php/prosiding/article/view/2266

Artikel ini digunakan untuk mendukung penjelasan bahwa lama penyimpanan berkaitan dengan perubahan kualitas internal telur, terutama indeks kuning telur, indeks putih telur, dan Haugh Unit.

**Catatan penggunaan sumber:** S1 merupakan artikel informasi resmi pemerintah, sedangkan S2 merupakan artikel ilmiah pada prosiding. Aturan dalam proyek ini adalah penyederhanaan untuk demonstrasi sistem pakar, bukan kutipan lengkap seluruh persyaratan teknis SNI 3926:2023.

## 3. Fakta yang Ditanyakan kepada Pengguna
1. Kondisi cangkang: utuh atau retak.
2. Kekentalan putih telur: kental, sedikit encer, atau encer.
3. Bentuk kuning telur: bulat atau oval.
4. Posisi kuning telur: tengah, sedikit bergeser, atau pinggir.
5. Kedalaman kantung udara dalam cm.
6. Bau telur: khas atau tidak normal.

## 4. Aturan IF–THEN

| Aturan | IF (kondisi) | THEN (hasil) | Sumber |
|---|---|---|---|
| R1 | Cangkang utuh AND putih telur kental AND kuning telur bulat di tengah AND kantung udara < 0,5 cm | MUTU_I | S1 |
| R2 | Cangkang utuh AND putih telur sedikit encer AND kuning telur bulat sedikit bergeser AND kantung udara 0,5–0,9 cm | MUTU_II | S1 |
| R3 | Cangkang utuh AND putih telur encer AND kuning telur oval di pinggir AND kantung udara > 0,9 cm | MUTU_III | S1, S2 |
| R4 | Hasil R1 adalah MUTU_I AND bau khas | KUALITAS_FISIK_BAIK | S1 |
| R5 | Hasil R2 adalah MUTU_II AND bau khas | KUALITAS_FISIK_CUKUP | S1, S2 |
| R6 | Hasil R3 adalah MUTU_III AND bau khas | KUALITAS_FISIK_RENDAH | S1, S2 |
| R7 | Cangkang retak | PERINGATAN_CANGKANG_RUSAK | S1 |
| R8 | Bau tidak normal | INDIKASI_BAU_TIDAK_NORMAL | S1 |

R4, R5, dan R6 menggunakan hasil aturan sebelumnya. Contohnya, R1 menghasilkan `MUTU_I`, lalu hasil tersebut digunakan oleh R4 bersama fakta bau khas. Ini merupakan rantai Forward Chaining.

Setiap aturan mempunyai atribut `mode`. Nilai `dan` berarti semua kondisi harus terpenuhi; nilai `atau` berarti minimal satu kondisi harus terpenuhi. Mesin program mendukung kedua mode tersebut.

## 5. Cara Kerja Forward Chaining
1. Program membaca fakta awal dari jawaban pengguna.
2. Program memeriksa kondisi setiap aturan dalam file `aturan_telur.json`.
3. Aturan yang cocok dijalankan dan hasilnya disimpan ke memori.
4. Hasil aturan dapat digunakan sebagai fakta oleh aturan berikutnya.
5. Aturan yang sudah dijalankan tidak dijalankan ulang.
6. Proses berulang sampai tidak ada aturan baru.
7. Program menampilkan kesimpulan, aturan yang digunakan, sumber, dan batas keberlakuan.

## 6. Struktur Folder
```text
Sistem_Pakar_Telur/
├── main.py
├── aturan_telur.json
├── README.md
└── screenshot/
    ├── pengujian_1_mutu_baik.png
    ├── pengujian_2_mutu_cukup.png
    ├── pengujian_3_mutu_rendah.png
    └── pengujian_4_tanpa_kesimpulan.png
```

Masukkan screenshot hasil pengujian milik sendiri ke folder `screenshot/`. Nama file dapat disesuaikan.

## 7. Cara Menjalankan Program
Persyaratan: Python 3.

1. Simpan `main.py` dan `aturan_telur.json` dalam folder yang sama.
2. Buka terminal pada folder proyek.
3. Jalankan:
```bash
python main.py
```
4. Jawab pertanyaan kondisi telur sesuai pilihan yang tersedia.

Program hanya menggunakan modul bawaan Python (`json` dan `pathlib`), sehingga tidak perlu memasang library tambahan.

## 8. Kasus Uji

| No. | Data masukan ringkas | Kesimpulan yang diharapkan |
|---|---|---|
| 1 | Utuh; putih kental; kuning bulat di tengah; kantung udara 0,3 cm; bau khas | KUALITAS_FISIK_BAIK |
| 2 | Utuh; putih sedikit encer; kuning bulat sedikit bergeser; kantung udara 0,7 cm; bau khas | KUALITAS_FISIK_CUKUP |
| 3 | Utuh; putih encer; kuning oval di pinggir; kantung udara 1,2 cm; bau khas | KUALITAS_FISIK_RENDAH |
| 4 | Utuh; putih kental; kuning oval di pinggir; kantung udara 1,2 cm; bau khas | Tidak ditemukan kesimpulan |

### Bukti Pengujian
Tambahkan empat screenshot hasil eksekusi program ke folder `screenshot/` dan tampilkan di bawah ini:

- Pengujian 1: `screenshot/pengujian_1_mutu_baik.png`
- Pengujian 2: `screenshot/pengujian_2_mutu_cukup.png`
- Pengujian 3: `screenshot/pengujian_3_mutu_rendah.png`
- Pengujian 4: `screenshot/pengujian_4_tanpa_kesimpulan.png`

## 9. Batas Keberlakuan
- Klasifikasi mutu I, II, dan III dalam proyek ini merujuk pada parameter yang dipilih dari sumber, bukan penetapan keamanan pangan.
- Sistem tidak melakukan uji mikrobiologi dan tidak dapat memastikan telur bebas Salmonella.
- Pemeriksaan visual, bau, dan input pengguna memiliki keterbatasan.
- Aturan merupakan penyederhanaan untuk demonstrasi sistem pakar; hasil bukan sertifikat mutu atau pengganti pengujian sesuai prosedur standar.

## 10. Penggunaan AI
AI digunakan sebagai alat bantu belajar untuk memahami konsep sistem pakar dan Forward Chaining, menyusun rancangan awal aturan, membantu penulisan dan pemeriksaan kode, serta merapikan dokumentasi. Penulis melakukan pemeriksaan dan pengujian program, serta bertanggung jawab memahami dan menjelaskan aturan dan kode yang digunakan.

## 11. Pengembangan
Proyek ini dibuat sebagai tugas pembelajaran mata kuliah Kecerdasan Buatan. Pengembangan selanjutnya dapat mencakup penambahan parameter pengujian, validasi data berdasarkan dokumen standar lengkap, dan antarmuka pengguna.
