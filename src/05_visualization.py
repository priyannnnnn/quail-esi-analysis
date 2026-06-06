"""
Modul 5: Buat grafik visualisasi untuk bab hasil skripsi.
"""
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import Patch
import numpy as np


WARNA_KATEGORI = {
    'Baik':            'green',
    'Perlu Perhatian': 'orange',
    'Kritis':          'red',
}


def buat_grafik(gabung_df, korelasi, output_path):
    """Buat 4 grafik utama dan simpan ke file."""
    
    r = korelasi['r']
    p = korelasi['p_value']
    
    fig, axs = plt.subplots(2, 2, figsize=(16, 11))
    fig.suptitle(
        'Analisis ESI dan Produksi Telur Puyuh — Musim Pancaroba',
        fontsize=14, fontweight='bold', y=1.01
    )
    
    # ─── Grafik 1: Fluktuasi Suhu & Amonia ────────
    ax1 = axs[0, 0]
    ax1.plot(gabung_df['date'], gabung_df['suhu_rata'],
             label='Suhu (°C)', color='tomato', marker='o', ms=3)
    ax1_t = ax1.twinx()
    ax1_t.plot(gabung_df['date'], gabung_df['amonia_rata'],
               label='Amonia (ppm)', color='purple',
               marker='s', ms=3, linestyle='--')
    ax1.set_title('Fluktuasi Suhu & Amonia Harian')
    ax1.set_xlabel('Tanggal')
    ax1.set_ylabel('Suhu (°C)', color='tomato')
    ax1_t.set_ylabel('Amonia (ppm)', color='purple')
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
    ax1.tick_params(axis='x', rotation=45)
    l1, lb1 = ax1.get_legend_handles_labels()
    l2, lb2 = ax1_t.get_legend_handles_labels()
    ax1.legend(l1 + l2, lb1 + lb2, loc='upper left', fontsize=8)
    
    # ─── Grafik 2: ESI Harian (warna per kategori) ───
    ax2 = axs[0, 1]
    for _, row in gabung_df.iterrows():
        ax2.bar(row['date'], row['ESI'],
                color=WARNA_KATEGORI.get(row['Kategori_ESI'], 'gray'),
                alpha=0.8, width=0.8)
    ax2.axhline(0.30, color='orange', linestyle='--', lw=1)
    ax2.axhline(0.60, color='red',    linestyle='--', lw=1)
    ax2.set_title('Nilai ESI Harian')
    ax2.set_xlabel('Tanggal'); ax2.set_ylabel('ESI')
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
    ax2.tick_params(axis='x', rotation=45)
    legend = [
        Patch(facecolor='green',  label='Baik'),
        Patch(facecolor='orange', label='Perhatian'),
        Patch(facecolor='red',    label='Kritis'),
    ]
    ax2.legend(handles=legend, fontsize=8)
    
    # ─── Grafik 3: Scatter ESI vs Telur ──────────
    ax3 = axs[1, 0]
    ax3.scatter(gabung_df['ESI'], gabung_df['total_eggs'],
                color='steelblue', s=60, zorder=5)
    z = np.polyfit(gabung_df['ESI'], gabung_df['total_eggs'], 1)
    garis = np.poly1d(z)
    x_line = np.linspace(gabung_df['ESI'].min(),
                          gabung_df['ESI'].max(), 100)
    ax3.plot(x_line, garis(x_line), color='red', lw=2, linestyle='--')
    ax3.set_title(f'Korelasi ESI vs Telur (r = {r:.3f}, p = {p:.3f})')
    ax3.set_xlabel('ESI'); ax3.set_ylabel('Total Telur')
    
    # ─── Grafik 4: Produksi Telur Harian ─────────
    ax4 = axs[1, 1]
    ax4.plot(gabung_df['date'], gabung_df['total_eggs'],
             color='steelblue', marker='o', ms=4, lw=2)
    ax4.fill_between(gabung_df['date'], gabung_df['total_eggs'],
                      alpha=0.15, color='steelblue')
    ax4.set_title('Produksi Telur Harian')
    ax4.set_xlabel('Tanggal'); ax4.set_ylabel('Total Telur')
    ax4.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
    ax4.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.show()
    print(f"  → Grafik disimpan ke {output_path}")