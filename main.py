"""
File utama — jalankan semua tahap pengolahan data ESI puyuh.

Cara pakai:
    python main.py
"""
import sys
import os
import pandas as pd

# Tambahkan folder src ke path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import modul kita
from importlib import import_module

clean_mod      = import_module('01_clean_data')
agg_mod        = import_module('02_aggregate_daily')
esi_mod        = import_module('03_calculate_esi')
corr_mod       = import_module('04_correlation')
viz_mod        = import_module('05_visualization')


def main():
    print("\n" + "="*55)
    print("  PENGOLAHAN DATA ESI — PENELITIAN PUYUH PETELUR")
    print("="*55)
    
    # ─── 1. Baca dan bersihkan data ──────────────────
    print("\n[1/5] Membersihkan data sensor & telur...")
    sensor = clean_mod.clean_sensor_data('data/data_sensor.csv')
    telur  = clean_mod.clean_egg_data('data/data_telur.csv')
    print(f"  → Sensor: {len(sensor)} baris siap diolah")
    print(f"  → Telur : {len(telur)} hari tercatat")
    
    # ─── 2. Agregasi harian ──────────────────────────
    print("\n[2/5] Agregasi data sensor per hari...")
    harian = agg_mod.aggregate_daily(sensor)
    print(f"  → {len(harian)} hari teragregasi")
    
    # ─── 3. Hitung THI dan ESI ───────────────────────
    print("\n[3/5] Menghitung THI dan ESI harian...")
    hasil = esi_mod.calculate_esi(harian)
    
    # Gabung dengan data telur
    gabung = pd.merge(hasil, telur, on='date', how='inner')
    print(f"  → {len(gabung)} hari berhasil dianalisis")
    
    # ─── 4. Korelasi ─────────────────────────────────
    print("\n[4/5] Menghitung korelasi Pearson...")
    korelasi = corr_mod.calculate_correlation(gabung)
    
    print("\n  ┌─────────────────────────────────────────")
    print(f"  │  r       : {korelasi['r']:.4f}")
    print(f"  │  p-value : {korelasi['p_value']:.4f}")
    print(f"  │  Arah    : {korelasi['arah']}")
    print(f"  │  Kuat    : {korelasi['kekuatan']}")
    print(f"  │  Signif  : {korelasi['signifikansi']}")
    print("  └─────────────────────────────────────────")
    
    # ─── 5. Visualisasi & ekspor ─────────────────────
    print("\n[5/5] Membuat grafik dan menyimpan hasil...")
    
    os.makedirs('output', exist_ok=True)
    
    # Simpan tabel hasil
    output_csv = 'output/hasil_ESI_lengkap.csv'
    gabung.to_csv(output_csv, index=False)
    print(f"  → Tabel hasil: {output_csv}")
    
    # Buat grafik
    viz_mod.buat_grafik(
        gabung, korelasi,
        output_path='output/grafik_ESI_puyuh.png'
    )
    
    # Ringkasan akhir
    print("\n" + "="*55)
    print("  RINGKASAN AKHIR")
    print("="*55)
    print(f"  Total hari dianalisis : {len(gabung)}")
    print(f"  ESI rata-rata         : {gabung['ESI'].mean():.4f}")
    print(f"  ESI tertinggi         : {gabung['ESI'].max():.4f}")
    print(f"  ESI terendah          : {gabung['ESI'].min():.4f}")
    print("\n  Distribusi Kategori ESI:")
    for kat, jml in gabung['Kategori_ESI'].value_counts().items():
        print(f"    {kat:20s}: {jml} hari")
    print("="*55)
    print("\n✅ Selesai. Cek folder 'output/' untuk hasilnya.\n")


if __name__ == '__main__':
    main()