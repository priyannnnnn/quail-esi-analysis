"""
Modul 2: Agregasi data sensor menjadi ringkasan harian.
"""
import pandas as pd


def aggregate_daily(sensor_df):
    """Ringkas data sensor menjadi 1 baris per hari."""
    
    sensor_df['date'] = sensor_df['timestamp'].dt.normalize()
    
    daily = sensor_df.groupby('date').agg(
        suhu_rata     =('temperature', 'mean'),
        suhu_max      =('temperature', 'max'),
        suhu_min      =('temperature', 'min'),
        lembap_rata   =('humidity',    'mean'),
        lembap_max    =('humidity',    'max'),
        amonia_rata   =('nh3_ppm',     'mean'),
        amonia_max    =('nh3_ppm',     'max'),
        cahaya_rata   =('lux',         'mean'),
        cahaya_max    =('lux',         'max'),
        jumlah_baris  =('temperature', 'count'),
    ).reset_index()
    
    # Bulatkan 2 desimal
    numeric_cols = [
        'suhu_rata', 'suhu_max', 'suhu_min',
        'lembap_rata', 'lembap_max',
        'amonia_rata', 'amonia_max',
        'cahaya_rata', 'cahaya_max',
    ]
    daily[numeric_cols] = daily[numeric_cols].round(2)
    
    return daily