"""
Modul 4: Korelasi Pearson antara ESI dan produksi telur.
"""
from scipy import stats


def calculate_correlation(esi_eggs_df):
    """Hitung korelasi Pearson dan interpretasinya."""
    
    r, p_value = stats.pearsonr(
        esi_eggs_df['ESI'],
        esi_eggs_df['total_eggs']
    )
    
    # Interpretasi arah
    arah = ("Negatif: semakin tinggi ESI → telur turun"
            if r < 0 else
            "Positif: semakin tinggi ESI → telur naik")
    
    # Kekuatan
    abs_r = abs(r)
    if abs_r >= 0.80:
        kekuatan = "Sangat Kuat"
    elif abs_r >= 0.60:
        kekuatan = "Kuat"
    elif abs_r >= 0.40:
        kekuatan = "Sedang"
    elif abs_r >= 0.20:
        kekuatan = "Lemah"
    else:
        kekuatan = "Sangat Lemah"
    
    # Signifikansi
    if p_value < 0.01:
        signif = "Sangat Signifikan (p < 0.01)"
    elif p_value < 0.05:
        signif = "Signifikan (p < 0.05)"
    else:
        signif = "Tidak Signifikan (p ≥ 0.05)"
    
    return {
        'r': r,
        'p_value': p_value,
        'arah': arah,
        'kekuatan': kekuatan,
        'signifikansi': signif,
    }