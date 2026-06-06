"""
Modul 1: Membersihkan dan memperbaiki format data sensor.
"""
import pandas as pd


def clean_sensor_data(filepath):
    """Baca, bersihkan, dan kembalikan data sensor yang siap olah."""
    
    # Baca CSV — tangani separator titik koma dan desimal koma
    df = pd.read_csv(filepath, sep=';', decimal=',')

    # Normalisasi nama kolom: huruf kecil, spasi/karakter khusus → underscore
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(r'[^\w]', '_', regex=True)
        .str.replace(r'_+', '_', regex=True)
        .str.strip('_')
    )

    # Rename kolom waktu ke 'timestamp'
    for candidate in ('timestamp', 'created_at', 'time', 'date'):
        if candidate in df.columns:
            df = df.rename(columns={candidate: 'timestamp'})
            break

    # Rename kolom sensor ke nama standar
    rename_map = {}
    for col in df.columns:
        if 'temp' in col:
            rename_map[col] = 'temperature'
        elif 'humid' in col:
            rename_map[col] = 'humidity'
        elif 'nh3' in col or 'ammonia' in col:
            rename_map[col] = 'nh3_ppm'
        elif 'lux' in col or 'light' in col:
            rename_map[col] = 'lux'
    df = df.rename(columns=rename_map)

    # Paksa kolom numerik yang mungkin masih string karena koma desimal
    for col in ['temperature', 'humidity', 'nh3_ppm', 'lux']:
        if col in df.columns and not pd.api.types.is_float_dtype(df[col]):
            df[col] = pd.to_numeric(
                df[col].astype(str).str.replace(',', '.', regex=False),
                errors='coerce'
            )

    # Parse timestamp dengan format YY/MM/DD HH.MM (misal: 25/04/26 15.42)
    df['timestamp'] = pd.to_datetime(
        df['timestamp'], format='%y/%m/%d %H.%M', errors='coerce'
    )
    # Fallback ke parser otomatis jika format di atas gagal
    if df['timestamp'].isnull().all():
        df['timestamp'] = pd.to_datetime(
            df['timestamp'], errors='coerce', dayfirst=False
        )
    
    # Hapus baris yang waktunya gagal diparse
    before = len(df)
    df = df.dropna(subset=['timestamp'])
    print(f"  → {before - len(df)} baris terhapus karena format waktu salah")
    
    # Urutkan berdasarkan waktu
    df = df.sort_values('timestamp').reset_index(drop=True)
    
    # Tangani nilai kosong dengan interpolasi
    for col in ['temperature', 'humidity', 'nh3_ppm', 'lux']:
        kosong = df[col].isnull().sum()
        if kosong > 0:
            df[col] = df[col].interpolate(method='linear')
            df[col] = df[col].fillna(method='bfill').fillna(method='ffill')
            print(f"  → {kosong} nilai kosong pada '{col}' diisi dengan interpolasi")
    
    # Hapus outlier dengan IQR
    for col in ['temperature', 'humidity', 'nh3_ppm', 'lux']:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        before = len(df)
        df = df[
            (df[col] >= Q1 - 1.5 * IQR) &
            (df[col] <= Q3 + 1.5 * IQR)
        ]
        outliers = before - len(df)
        if outliers > 0:
            print(f"  → {outliers} outlier pada '{col}' dihapus")
    
    return df.reset_index(drop=True)


def clean_egg_data(filepath):
    """Baca dan bersihkan data produksi telur."""
    df = pd.read_csv(filepath)
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df = df.dropna(subset=['date']).sort_values('date').reset_index(drop=True)
    return df