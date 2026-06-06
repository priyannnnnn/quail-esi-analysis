"""
Modul 3: Hitung THI, skor stres, dan ESI harian.
"""

# ===== Bobot ESI =====
W_THI    = 0.45
W_AMONIA = 0.35
W_CAHAYA = 0.20


def hitung_thi(suhu, kelembapan):
    """Rumus baku Temperature-Humidity Index untuk unggas."""
    return (0.8 * suhu) + ((kelembapan / 100) * (suhu - 14.4)) + 46.4


def skor_thi(thi):
    """Skor stres dari THI. Zona nyaman puyuh: ≤68."""
    if thi <= 68:
        return 0.0
    elif thi >= 82:
        return 1.0
    else:
        return (thi - 68) / (82 - 68)


def skor_amonia(nh3):
    """Skor stres dari amonia. Aman ≤10 ppm, bahaya ≥25 ppm."""
    if nh3 <= 10:
        return 0.0
    elif nh3 >= 25:
        return 1.0
    else:
        return (nh3 - 10) / (25 - 10)


def skor_cahaya(lux):
    """Skor stres dari cahaya. Cukup ≥15 lux."""
    if lux >= 15:
        return 0.0
    else:
        return (15 - lux) / 15


def kategori_thi(thi):
    if thi < 68:
        return 'Nyaman'
    elif thi <= 76:
        return 'Perhatian'
    else:
        return 'Stres'


def kategori_esi(esi):
    if esi <= 0.30:
        return 'Baik'
    elif esi <= 0.60:
        return 'Perlu Perhatian'
    else:
        return 'Kritis'


def calculate_esi(daily_df):
    """Hitung THI, skor stres komponen, dan ESI per hari."""
    
    df = daily_df.copy()
    
    # Hitung THI
    df['THI'] = hitung_thi(df['suhu_rata'], df['lembap_rata']).round(2)
    df['Kategori_THI'] = df['THI'].apply(kategori_thi)
    
    # Skor stres komponen
    df['S_THI']    = df['THI'].apply(skor_thi).round(4)
    df['S_amonia'] = df['amonia_rata'].apply(skor_amonia).round(4)
    df['S_cahaya'] = df['cahaya_rata'].apply(skor_cahaya).round(4)
    
    # ESI gabungan
    df['ESI'] = (
        W_THI    * df['S_THI']    +
        W_AMONIA * df['S_amonia'] +
        W_CAHAYA * df['S_cahaya']
    ).round(4)
    
    df['Kategori_ESI'] = df['ESI'].apply(kategori_esi)
    
    return df