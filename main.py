import json
from pathlib import Path


def baca_basis_pengetahuan(nama_file="aturan_telur.json"):
    """Membaca basis pengetahuan dari file JSON."""
    lokasi = Path(__file__).resolve().parent / nama_file
    with lokasi.open("r", encoding="utf-8") as file:
        return json.load(file)


def minta_fakta(basis):
    """Menanyakan fakta awal yang diperlukan kepada pengguna."""
    fakta = {}
    print("\n=== INPUT KONDISI TELUR ===")

    for nama, detail in basis["fakta_input"].items():
        pertanyaan = detail["pertanyaan"]

        if detail["tipe"] == "pilihan":
            pilihan = detail["pilihan"]
            while True:
                jawaban = input(
                    f"{pertanyaan} ({' / '.join(pilihan)}): "
                ).strip().lower()

                if jawaban in pilihan:
                    fakta[nama] = jawaban
                    break

                print("Jawaban tidak tersedia. Pilih salah satu:", ", ".join(pilihan))

        elif detail["tipe"] == "angka":
            while True:
                try:
                    jawaban = float(input(f"{pertanyaan}: ").strip().replace(",", "."))
                    if jawaban < detail.get("minimum", 0):
                        print("Nilai tidak boleh kurang dari", detail.get("minimum", 0))
                        continue
                    fakta[nama] = jawaban
                    break
                except ValueError:
                    print("Masukkan angka yang benar, contoh: 0.3")

    return fakta


def evaluasi_kondisi(kondisi, fakta_awal, memori):
    """Memeriksa satu kondisi berdasarkan fakta awal atau fakta hasil aturan."""
    nama_fakta = kondisi["fakta"]
    operator = kondisi["operator"]
    nilai_syarat = kondisi["nilai"]

    if nama_fakta == "hasil":
        nilai_aktual = nilai_syarat in memori
        return nilai_aktual if operator == "ada" else False

    if nama_fakta not in fakta_awal:
        return False

    nilai_aktual = fakta_awal[nama_fakta]

    if operator == "=":
        return nilai_aktual == nilai_syarat
    if operator == "<":
        return nilai_aktual < nilai_syarat
    if operator == ">":
        return nilai_aktual > nilai_syarat
    if operator == "rentang_inklusif":
        batas_bawah, batas_atas = nilai_syarat
        return batas_bawah <= nilai_aktual <= batas_atas

    raise ValueError(f"Operator tidak dikenal: {operator}")


def aturan_terpenuhi(aturan, fakta_awal, memori):
    """Mengevaluasi mode 'dan' atau 'atau' yang ditulis di file JSON."""
    hasil_kondisi = [
        evaluasi_kondisi(kondisi, fakta_awal, memori)
        for kondisi in aturan["jika"]
    ]

    mode = aturan["mode"].lower()
    if mode == "dan":
        return all(hasil_kondisi)
    if mode == "atau":
        return any(hasil_kondisi)

    raise ValueError(f"Mode aturan {aturan['id']} harus 'dan' atau 'atau'.")


def forward_chaining(basis, fakta_awal):
    """
    Mesin Forward Chaining buatan sendiri:
    fakta awal -> aturan cocok -> hasil masuk memori -> ulangi sampai stabil.
    """
    memori = set()
    aturan_terpakai = []
    aturan_sudah_dijalankan = set()
    nomor_siklus = 0

    print("\n=== PROSES FORWARD CHAINING ===")
    print("Fakta awal:", fakta_awal)

    while True:
        nomor_siklus += 1
        aturan_baru = []

        for aturan in basis["aturan"]:
            if aturan["id"] in aturan_sudah_dijalankan:
                continue

            if aturan_terpenuhi(aturan, fakta_awal, memori):
                aturan_baru.append(aturan)

        if not aturan_baru:
            print(f"Siklus {nomor_siklus}: tidak ada aturan baru, proses berhenti.")
            break

        for aturan in aturan_baru:
            hasil = aturan["maka"]

            memori.add(hasil)
            aturan_terpakai.append(aturan)
            aturan_sudah_dijalankan.add(aturan["id"])

            print(
                f"Siklus {nomor_siklus}: {aturan['id']} aktif "
                f"-> menghasilkan {hasil}"
            )

    return memori, aturan_terpakai


def uraikan_kondisi(kondisi, fakta_awal):
    """Mengubah kondisi aturan menjadi kalimat alasan yang mudah dibaca."""
    nama = kondisi["fakta"]
    operator = kondisi["operator"]
    syarat = kondisi["nilai"]

    label = {
        "cangkang": "kondisi cangkang",
        "putih_telur": "kekentalan putih telur",
        "kuning_telur_bentuk": "bentuk kuning telur",
        "kuning_telur_posisi": "posisi kuning telur",
        "kantung_udara_cm": "kedalaman kantung udara",
        "bau": "bau telur"
    }

    if nama == "hasil":
        return f"hasil aturan sebelumnya memuat {syarat}"

    nama_label = label.get(nama, nama)
    if operator == "=":
        return f"{nama_label} = {syarat}"
    if operator == "<":
        return f"{nama_label} < {syarat} cm"
    if operator == ">":
        return f"{nama_label} > {syarat} cm"
    if operator == "rentang_inklusif":
        return f"{nama_label} berada pada {syarat[0]} sampai {syarat[1]} cm"

    return f"{nama_label} memenuhi kondisi {operator} {syarat}"


def tampilkan_hasil(basis, memori, aturan_terpakai):
    """Menampilkan kesimpulan, alasan aturan, sumber, dan batas keberlakuan."""
    print("\n========== HASIL SISTEM PAKAR ==========")

    if not memori:
        print("Kesimpulan: BELUM DITEMUKAN")
        print("Alasan: tidak ada aturan yang seluruh/ salah satu kondisinya cocok.")
    else:
        kode_akhir = [
            kode for kode in memori
            if kode.startswith("KUALITAS_")
            or kode.startswith("PERINGATAN_")
            or kode.startswith("INDIKASI_")
        ]

        print("KESIMPULAN:")
        for kode in sorted(kode_akhir or memori):
            print(f"- {kode}: {basis['kesimpulan'].get(kode, '')}")

        print("\nALASAN / ATURAN YANG DIGUNAKAN:")
        for aturan in aturan_terpakai:
            kondisi_teks = [
                uraikan_kondisi(kondisi, {})
                for kondisi in aturan["jika"]
            ]
            penghubung = " DAN " if aturan["mode"] == "dan" else " ATAU "
            print(f"\n{aturan['id']}:")
            print("  JIKA " + penghubung.join(kondisi_teks))
            print(f"  MAKA {aturan['maka']}")

            for kode_sumber in aturan.get("sumber", []):
                sumber = basis["sumber"].get(kode_sumber, {})
                print(
                    f"  Sumber {kode_sumber}: {sumber.get('lembaga', '')} — "
                    f"{sumber.get('judul', '')}"
                )

    print("\nCATATAN BATAS KEBERLAKUAN:")
    for catatan in basis["catatan_batas"]:
        print(f"- {catatan}")


def main():
    try:
        basis = baca_basis_pengetahuan()
    except FileNotFoundError:
        print("File aturan_telur.json tidak ditemukan.")
        print("Pastikan file JSON berada satu folder dengan main.py.")
        return
    except json.JSONDecodeError as error:
        print("Format JSON tidak valid:", error)
        return

    print("=" * 62)
    print(basis["judul"])
    print("Metode penalaran:", basis["metode"])
    print("=" * 62)

    fakta_awal = minta_fakta(basis)
    memori, aturan_terpakai = forward_chaining(basis, fakta_awal)
    tampilkan_hasil(basis, memori, aturan_terpakai)


if __name__ == "__main__":
    main()