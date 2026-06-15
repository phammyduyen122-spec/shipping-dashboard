import pandas as pd
import glob
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

def parse_perf():
    perf_dir = "C:/Users/DUYEN/.gemini/antigravity/scratch/performance dashboard"
    perf_files = glob.glob(os.path.join(perf_dir, "*.xlsx"))
    if not perf_files:
        print("No perf files found.")
        return
    perf_file = max(perf_files, key=os.path.getmtime)
    print("Reading:", perf_file)
    
    df = pd.read_excel(perf_file, sheet_name="Sheet 1")
    print("Total rows read:", len(df))
    
    # Map columns
    mapping = {
        'Mã yêu cầu': 'maYeuCau',
        'Mã Phiếu': 'maPhieu',
        'Barcode': 'barcode',
        'Tên sản phẩm': 'tenSanPham',
        'Đơn vị': 'donVi',
        'Nơi nhận': 'noiNhan',
        'Nơi nhận (viết tắt)': 'noiNhanVietTat',
        'Số lượng y/c chuyển ban đầu': 'qtyYcBanDau',
        'Số lượng chuyển hệ thống tính': 'qtyHeThong',
        'Số lượng thực chia': 'qtyThucChia',
        'Trạng thái': 'trangThai',
        'Trạng thái nhận hàng (PR)': 'trangThaiPR',
        'Trạng thái chuyển hàng': 'trangThaiChuyen',
        'Cần chia': 'canChia',
        'Chốt số lượng nhận': 'chotNhan',
        'Ngày chuyển mong muốn': 'ngayChuyen',
        'Ngày giao hàng dự kiến': 'ngayGiaoDuKien',
        'Nơi chuyển': 'noiChuyen',
        'Mã phiếu chuyển': 'maPhieuChuyen',
        'Ngày cập nhật': 'ngayCapNhat',
        'Người cập nhật': 'nguoiCapNhat',
        'Bắt đầu chia hàng': 'batDauChia',
        'Hoàn tất chia hàng': 'hoanTatChia',
        'SL rổ': 'slRo',
        'SL kiện': 'slKien',
        'Người chia hàng': 'nguoiChia'
    }
    
    df_clean = pd.DataFrame()
    for col, prop in mapping.items():
        if col in df.columns:
            df_clean[prop] = df[col]
        else:
            df_clean[prop] = ""
            
    # Clean numeric columns
    for num_col in ['qtyYcBanDau', 'qtyHeThong', 'qtyThucChia', 'slRo', 'slKien']:
        df_clean[num_col] = pd.to_numeric(df_clean[num_col], errors='coerce').fillna(0).astype(int)
        
    # Date formatting
    def parse_dt(val):
        if pd.isna(val) or val == "":
            return "N/A"
        try:
            # Check if it is dd/mm/yyyy
            s = str(val).strip()
            # If it is like 04/06/2026
            parts = s.split("/")
            if len(parts) == 3 and len(parts[2]) == 4:
                return f"{parts[2]}-{parts[1]}-{parts[0]}"
            # Try general pandas datetime
            dt = pd.to_datetime(s, errors='coerce')
            if not pd.isna(dt):
                return dt.strftime('%Y-%m-%d')
            return s
        except:
            return str(val)
            
    df_clean['ngayChuyen'] = df_clean['ngayChuyen'].apply(parse_dt)
    
    # Filter cancelled
    df_clean = df_clean[~df_clean['trangThai'].str.lower().str.contains('hủy|huy', na=False)]
    df_clean = df_clean[~df_clean['barcode'].isin(['CC00360', 'CC00381'])]
    
    print("Clean rows:", len(df_clean))
    print(df_clean.head(3).to_string())

parse_perf()
