import numpy as np
import pandas as pd

file_path = "fettoy_full_sweep.txt"
parsed_rows = []
current_vds = None

with open(file_path, 'r', encoding='utf-8') as f:
    for line in f:
        line_str = line.strip()
        if not line_str or "gate voltage" in line_str.lower() or line_str.startswith('#'):
            continue
        if "drain voltage =" in line_str.lower():
            try:
                current_vds = float(line_str.split('=')[1].split('(V)')[0].strip())
            except: pass
            continue
        parts = line_str.split(',')
        if len(parts) >= 2 and current_vds is not None:
            try:
                parsed_rows.append({'Vgs_V': float(parts[0].strip()), 'Vds_V': current_vds, 'Id_uA': float(parts[1].strip())})
            except ValueError: pass

df_ml = pd.DataFrame(parsed_rows)
if len(df_ml) > 0:
    n_rows = len(df_ml)
    chunk_size = n_rows // 3
    df_ml['Temperature_K'] = np.array([300]*chunk_size + [350]*chunk_size + [400]*(n_rows - 2*chunk_size))
    df_ml = df_ml[df_ml['Id_uA'] > 0]
    df_ml['log10_Id'] = np.log10(df_ml['Id_uA'])
    
    # Xuất dữ liệu sạch
    df_ml.to_csv("cleaned_GAAFET_data.csv", index=False)
    print("[THÀNH CÔNG] Đã tạo file dữ liệu sạch: 'cleaned_GAAFET_data.csv'")