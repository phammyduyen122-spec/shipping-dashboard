import pandas as pd
import json
import os
import glob
import sys
import time
from datetime import datetime, timedelta
import unicodedata

def get_best_file_for_date(directory, prefix, date_obj):
    fmt1 = date_obj.strftime("%Y-%m-%d")
    fmt2 = date_obj.strftime("%d%m%Y")
    
    candidates = []
    files = glob.glob(os.path.join(directory, f"{prefix}*.xlsx"))
    for f in files:
        basename = os.path.basename(f)
        if fmt1 in basename or fmt2 in basename:
            candidates.append(f)
            
    if not candidates:
        return None
        
    def get_priority(filename):
        basename = os.path.basename(filename)
        name_without_ext = os.path.splitext(basename)[0]
        parts = name_without_ext.split('-')
        if len(parts) > 1:
            suffix = parts[-1]
            if len(suffix) == 6 and suffix.isdigit():
                return 2
        return 1
        
    candidates.sort(key=lambda c: (get_priority(c), os.path.getmtime(c)), reverse=True)
    return candidates[0]

def get_date_from_filename(filename):
    import re
    basename = os.path.basename(filename)
    
    # Try YYYY-MM-DD
    m_ymd = re.search(r'(\d{4})-(\d{2})-(\d{2})', basename)
    if m_ymd:
        try:
            return datetime.strptime(m_ymd.group(0), "%Y-%m-%d")
        except ValueError:
            pass
            
    # Try DDMMYYYY
    m_dmy = re.search(r'(\d{2})(\d{2})(\d{4})', basename)
    if m_dmy:
        try:
            return datetime.strptime(m_dmy.group(0), "%d%m%Y")
        except ValueError:
            pass
            
    return None

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

def load_existing_data(filepath="data.js"):
    if not os.path.exists(filepath):
        print(f"Không tìm thấy file {filepath} để đọc dữ liệu cũ.")
        return [], []
    try:
        print(f"Đang đọc dữ liệu cũ từ {filepath}...")
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
        def extract_json(var_name):
            start_str = f"window.{var_name} = "
            idx = content.find(start_str)
            if idx == -1:
                return None
            start_idx = idx + len(start_str)
            end_idx = content.find(";", start_idx)
            if end_idx == -1:
                return None
            return json.loads(content[start_idx:end_idx])
            
        catalog = extract_json("itemCatalog")
        branches = extract_json("branchesList")
        users = extract_json("usersList")
        compressed_trans = extract_json("compressedTransfers")
        compressed_perf = extract_json("compressedPerformance")
        
        if not all([catalog is not None, branches is not None, users is not None, compressed_trans is not None, compressed_perf is not None]):
            print("Lỗi: Không thể giải nén một số biến từ data.js")
            return [], []
            
        # Decompress transfers
        existing_trans = []
        for row in compressed_trans:
            toBranch = branches[row[3]] if 0 <= row[3] < len(branches) else ""
            itemInfo = catalog.get(row[4], ["", "", ""])
            fromBranch = "KHO RAU CỦ XỬ LÝ CHÊNH LỆCH CHUYỂN HÀNG" if row[2] == "XL" else "KHO RAU CỦ"
            nguoiChia = users[row[10]] if 0 <= row[10] < len(users) else ""
            existing_trans.append({
                'date': row[1],
                'fromBranch': fromBranch,
                'toBranch': toBranch,
                'itemCode': row[4],
                'itemName': itemInfo[0],
                'unit': itemInfo[2],
                'qtyShipped': row[5],
                'qtyReceived': row[6],
                'transferCode': row[7],
                'originalDoc': "",
                'generatedDoc': row[8],
                'supplementQty': 0,
                'docStatus': row[9],
                'nguoiChia': nguoiChia
            })
            
        # Decompress performance
        existing_perf = []
        for row in compressed_perf:
            noiNhan = branches[row[4]] if 0 <= row[4] < len(branches) else ""
            itemInfo = catalog.get(row[3], ["", "", ""])
            nguoiChia = users[row[23]] if 0 <= row[23] < len(users) else ""
            existing_perf.append({
                'maYeuCau': row[1],
                'maPhieu': row[2],
                'barcode': row[3],
                'tenSanPham': itemInfo[0],
                'donVi': itemInfo[2],
                'noiNhan': noiNhan,
                'noiNhanVietTat': "",
                'qtyYcBanDau': row[5],
                'qtyHeThong': row[6],
                'qtyThucChia': row[7],
                'trangThai': row[8],
                'trangThaiPR': row[9],
                'trangThaiChuyen': row[10],
                'canChia': row[11],
                'chotNhan': row[12],
                'ngayChuyen': row[13],
                'ngayGiaoDuKien': row[14],
                'noiChuyen': row[15],
                'maPhieuChuyen': row[16],
                'ngayCapNhat': row[17],
                'nguoiCapNhat': row[18],
                'batDauChia': row[19],
                'hoanTatChia': row[20],
                'slRo': row[21],
                'slKien': row[22],
                'nguoiChia': nguoiChia
            })
            
        print(f"Đã giải nén thành công {len(existing_trans)} transfers và {len(existing_perf)} performance records từ data.js")
        return existing_trans, existing_perf
    except Exception as e:
        print(f"Lỗi giải nén data.js: {e}")
        return [], []

def parse_excel():
    print("--- BẮT ĐẦU XỬ LÝ PHÂN TÍCH EXCEL ---")
    
    # Find the maximum date across both performance and transfer files
    all_dates = []
    perf_files = glob.glob(os.path.join("performance dashboard", "chi-tiet-chia-qua-canh_*.xlsx"))
    for f in perf_files:
        d = get_date_from_filename(f)
        if d:
            all_dates.append(d)
    trans_files = glob.glob("transfer_*.xlsx")
    for f in trans_files:
        d = get_date_from_filename(f)
        if d:
            all_dates.append(d)
            
    if all_dates:
        global_max_date = max(all_dates)
    else:
        global_max_date = datetime(2026, 6, 17)
        
    allowed_dates = [(global_max_date - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(4)]
    print(f"Rolling 4 days for filtering: {allowed_dates}")
    
    # Load existing data
    existing_trans, existing_perf = load_existing_data("data.js")
    
    # 1. Read Performance Reports
    perf_records = []
    perf_map = {}
    try:
        perf_dir = "performance dashboard"
        target_perf_files = []
        recent_perf_files = [f for f in target_perf_files if os.path.exists(f)]
        if recent_perf_files:
            print(f"Bắt buộc dùng các file hiệu suất do người dùng chỉ định: {recent_perf_files}")
        else:
            recent_perf_files = glob.glob(os.path.join(perf_dir, "chi-tiet-chia-qua-canh_*.xlsx"))
            perf_dates = []
            for f in recent_perf_files:
                d = get_date_from_filename(f)
                if d:
                    perf_dates.append((f, d))
            if perf_dates:
                max_date = max(d for f, d in perf_dates)
                cutoff = max_date - timedelta(days=8)
                recent_perf_files = [f for f, d in perf_dates if d >= cutoff]
                recent_perf_files.sort()
                print(f"Lọc file hiệu suất (max date: {max_date.strftime('%Y-%m-%d')}): Giữ {len(recent_perf_files)} / {len(perf_dates)} files.")
        
        if recent_perf_files or len(existing_perf) > 0:
            perf_mapping = {
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
            
            def keep_user(name):
                if not name:
                    return False
                n = str(name).strip().lower()
                import unicodedata
                n_norm = unicodedata.normalize('NFC', n)
                excluded = ['nhan quang hiếu', 'nhân quang hiếu', 'nhan quang hieu', 'nhân quang hieu']
                if n_norm in excluded or not n_norm:
                    return False
                return True
                
            def parse_dt(val):
                if pd.isna(val) or val == "":
                    return "N/A"
                if isinstance(val, pd.Timestamp):
                    return val.strftime('%Y-%m-%d')
                try:
                    s = str(val).strip()
                    # If already YYYY-MM-DD, return as is
                    if len(s) == 10 and s[4] == '-' and s[7] == '-':
                        return s
                    parts = s.split("/")
                    if len(parts) == 3 and len(parts[2]) == 4:
                        return f"{parts[2]}-{parts[1]}-{parts[0]}"
                    dt = pd.to_datetime(s, dayfirst=True, errors='coerce')
                    if not pd.isna(dt):
                        return dt.strftime('%Y-%m-%d')
                    return s
                except:
                    return str(val)

            dfs_perf = []
            if len(existing_perf) > 0:
                df_existing_perf = pd.DataFrame(existing_perf)
                dfs_perf.append(df_existing_perf)
            for perf_file in recent_perf_files:
                print(f"Đang đọc file Excel hiệu suất chia hàng: {perf_file}")
                try:
                    df_p = pd.read_excel(perf_file, sheet_name=0)
                    
                    df_perf_clean = pd.DataFrame()
                    for col, prop in perf_mapping.items():
                        if col in df_p.columns:
                            df_perf_clean[prop] = df_p[col]
                        else:
                            df_perf_clean[prop] = ""
                    
                    # Normalizing string columns
                    for str_col in ['maYeuCau', 'maPhieu', 'barcode', 'tenSanPham', 'donVi', 'noiNhan', 'noiNhanVietTat', 'trangThai', 'trangThaiPR', 'trangThaiChuyen', 'canChia', 'chotNhan', 'noiChuyen', 'maPhieuChuyen', 'ngayCapNhat', 'nguoiCapNhat', 'batDauChia', 'hoanTatChia', 'nguoiChia']:
                        df_perf_clean[str_col] = df_perf_clean[str_col].fillna("").astype(str).str.strip()
                        unique_vals = {x: unicodedata.normalize('NFC', x) for x in df_perf_clean[str_col].unique()}
                        df_perf_clean[str_col] = df_perf_clean[str_col].map(unique_vals)
                    
                    # Clean numeric columns
                    for num_col in ['qtyYcBanDau', 'qtyHeThong', 'qtyThucChia']:
                        df_perf_clean[num_col] = pd.to_numeric(df_perf_clean[num_col], errors='coerce').fillna(0).astype(float)
                    for num_col in ['slRo', 'slKien']:
                        df_perf_clean[num_col] = pd.to_numeric(df_perf_clean[num_col], errors='coerce').fillna(0).astype(float).astype(int)
                        # Cap values > 1000 to 0 to prevent quintillion basket glitch
                        df_perf_clean.loc[df_perf_clean[num_col] > 1000, num_col] = 0
                        
                    # Filter: only keep CTV / F1 / F2 / HUYHOANG
                    df_perf_clean = df_perf_clean[df_perf_clean['nguoiChia'].apply(keep_user)]
                    
                    # Filter out canceled documents
                    df_perf_clean = df_perf_clean[~df_perf_clean['trangThai'].str.lower().str.strip().isin(['đã hủy', 'hủy', 'huy', 'da hủy'])]
                    df_perf_clean = df_perf_clean[~df_perf_clean['barcode'].isin(['CC00360', 'CC00381'])]
                    
                    dfs_perf.append(df_perf_clean)
                except Exception as e_file:
                    print(f"Lỗi khi đọc file {perf_file}: {e_file}")
            
            if dfs_perf:
                df_perf_all = pd.concat(dfs_perf, ignore_index=True)
                df_perf_all['ngayChuyen'] = df_perf_all['ngayChuyen'].apply(parse_dt)
                
                # Dynamic allowed_dates calculation based on the actual data
                valid_dates = df_perf_all[df_perf_all['ngayChuyen'] != 'N/A']['ngayChuyen']
                if not valid_dates.empty:
                    actual_max_date = valid_dates.max()
                    print(f"Max date found in performance data: {actual_max_date}")
                    global_max_date = datetime.strptime(actual_max_date, '%Y-%m-%d')
                    allowed_dates = [(global_max_date - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(4)]
                    print(f"Recomputed rolling 4 days: {allowed_dates}")
                
                # Filter strictly for the rolling 4 days
                df_perf_all = df_perf_all[df_perf_all['ngayChuyen'].isin(allowed_dates)]
                
                # Deduplicate performance records based on unique PO line
                df_perf_all.drop_duplicates(subset=['maPhieuChuyen', 'barcode', 'noiNhan'], keep='last', inplace=True)
                
                # Build mapping for Shipping transfers (transferCode, itemCode) -> nguoiChia
                for idx, row in df_perf_all.iterrows():
                    mpc = row['maPhieuChuyen']
                    bc = row['barcode']
                    nc = row['nguoiChia']
                    if mpc and bc and nc:
                        perf_map[(mpc, bc)] = nc
                print(f"Đã tạo bản đồ mapping hiệu suất: {len(perf_map)} khóa.")
                
                # Add ID
                df_perf_all.insert(0, 'id', range(1, len(df_perf_all) + 1))
                perf_records = df_perf_all.to_dict(orient='records')
                print(f"Đã xử lý xong {len(perf_records)} bản ghi hiệu suất chia hàng.")
        else:
            print("Không tìm thấy file Excel hiệu suất chia hàng.")
    except Exception as ex_perf:
        print(f"Lỗi khi xử lý file Excel hiệu suất: {ex_perf}")
        import traceback
        traceback.print_exc()

    # 2. Read Shipping transfers Excel
    target_excel_files = []
    recent_excel_files = [f for f in target_excel_files if os.path.exists(f)]
    if recent_excel_files:
        print(f"Bắt buộc dùng các file điều chuyển do người dùng chỉ định: {recent_excel_files}")
    else:
        recent_excel_files = glob.glob("transfer_*.xlsx")
        trans_dates = []
        for f in recent_excel_files:
            d = get_date_from_filename(f)
            if d:
                trans_dates.append((f, d))
        if trans_dates:
            max_date = max(d for f, d in trans_dates)
            cutoff = max_date - timedelta(days=8)
            recent_excel_files = [f for f, d in trans_dates if d >= cutoff]
            recent_excel_files.sort()
            print(f"Lọc file điều chuyển (max date: {max_date.strftime('%Y-%m-%d')}): Giữ {len(recent_excel_files)} / {len(trans_dates)} files.")
    
    if not recent_excel_files and len(existing_trans) == 0:
        print("Lỗi: Không tìm thấy file Excel transfer_*.xlsx nào và không có dữ liệu cũ.")
        return
        
    try:
        
        col_mapping = {
            'date': 'Ngày chuyển hàng',
            'fromBranch': 'Chi nhánh chuyển',
            'toBranch': 'Chi nhánh nhận',
            'itemCode': 'Mã hàng',
            'itemName': 'Tên hàng',
            'unit': 'Đơn vị tính',
            'qtyShipped': 'Số lượng chuyển',
            'qtyReceived': 'Số lượng nhận',
            'transferCode': 'Mã chuyển hàng',
            'originalDoc': 'Chứng từ gốc',
            'generatedDoc': 'Chứng từ phát sinh',
            'supplementQty': 'SL hoàn/bổ sung',
            'docStatus': 'Trạng thái',
            'daHauKiem': 'Đã hậu kiểm'
        }
        
        dfs_transfers = []
        if len(existing_trans) > 0:
            df_existing_trans = pd.DataFrame(existing_trans)
            dfs_transfers.append(df_existing_trans)
        for excel_file in recent_excel_files:
            print(f"Đang đọc file Excel điều chuyển: {excel_file}")
            try:
                # Load raw data first to find the header
                df_raw = pd.read_excel(excel_file, header=None, nrows=10)
                header_row = None
                for idx in range(len(df_raw)):
                    row_vals = [str(x).lower() for x in df_raw.iloc[idx].values]
                    if any('mã hàng' in x for x in row_vals) or any('tên hàng' in x for x in row_vals):
                        header_row = idx
                        break
                        
                if header_row is None:
                    header_row = 0
                    
                df = pd.read_excel(excel_file, header=header_row)
                
                df_clean_f = pd.DataFrame()
                df_cols = list(df.columns)
                cols_lower = [str(c).lower().strip() for c in df_cols]
                for key, col_name in col_mapping.items():
                    resolved_name = None
                    col_name_clean = str(col_name).lower().strip()
                    if col_name in df.columns:
                        resolved_name = col_name
                    elif col_name_clean in cols_lower:
                        resolved_name = df_cols[cols_lower.index(col_name_clean)]
                    elif key == 'toBranch' and len(df_cols) > 3:
                        resolved_name = df_cols[3]
                        
                    if resolved_name and resolved_name in df.columns:
                        df_clean_f[key] = df[resolved_name]
                    else:
                        df_clean_f[key] = ""
                
                # Normalize fromBranch immediately to filter rows accurately
                df_clean_f['fromBranch'] = df_clean_f['fromBranch'].fillna("").astype(str).str.strip()
                unique_vals = {x: unicodedata.normalize('NFC', x) for x in df_clean_f['fromBranch'].unique()}
                df_clean_f['fromBranch'] = df_clean_f['fromBranch'].map(unique_vals)
                
                # Filter rows immediately to save huge memory & CPU concat time
                df_clean_f = df_clean_f[df_clean_f['fromBranch'].isin(['KHO RAU CỦ', 'KHO RAU CỦ XỬ LÝ CHÊNH LỆCH CHUYỂN HÀNG'])]
                
                dfs_transfers.append(df_clean_f)
            except Exception as e_file:
                print(f"Lỗi khi đọc file {excel_file}: {e_file}")
                
        if dfs_transfers:
            df_clean = pd.concat(dfs_transfers, ignore_index=True)
        else:
            print("Lỗi: Không có dữ liệu điều chuyển nào được đọc thành công.")
            return
            
        # Clean data types
        df_clean['qtyShipped'] = pd.to_numeric(df_clean['qtyShipped'], errors='coerce').fillna(0).astype(float)
        df_clean['qtyReceived'] = pd.to_numeric(df_clean['qtyReceived'], errors='coerce').fillna(0).astype(float)
        df_clean['supplementQty'] = pd.to_numeric(df_clean['supplementQty'], errors='coerce').fillna(0).astype(float)
        
        # Format Date
        def format_date(val):
            try:
                if pd.isna(val):
                    return "N/A"
                if isinstance(val, pd.Timestamp):
                    return val.strftime('%Y-%m-%d')
                s = str(val).strip()
                # If already YYYY-MM-DD, return as is
                if len(s) == 10 and s[4] == '-' and s[7] == '-':
                    return s
                dt = pd.to_datetime(s, dayfirst=True, errors='coerce')
                if not pd.isna(dt):
                    return dt.strftime('%Y-%m-%d')
                return s
            except:
                return str(val)
                
        df_clean['date'] = df_clean['date'].apply(format_date)
        # Filter strictly for the rolling 4 days
        df_clean = df_clean[df_clean['date'].isin(allowed_dates)]
        
        # Clean strings and normalize Unicode to NFC format using fast unique values map
        for str_col in ['fromBranch', 'toBranch', 'itemCode', 'itemName', 'unit', 'transferCode', 'originalDoc', 'generatedDoc', 'docStatus', 'daHauKiem']:
            if str_col in df_clean.columns:
                df_clean[str_col] = df_clean[str_col].fillna("").astype(str).str.strip()
                unique_vals = {x: unicodedata.normalize('NFC', x) for x in df_clean[str_col].unique()}
                df_clean[str_col] = df_clean[str_col].map(unique_vals)
            
        # Filter: only keep KHO RAU CỦ and KHO RAU CỦ XỬ LÝ CHÊNH LỆCH CHUYỂN HÀNG
        df_clean = df_clean[df_clean['fromBranch'].isin(['KHO RAU CỦ', 'KHO RAU CỦ XỬ LÝ CHÊNH LỆCH CHUYỂN HÀNG'])]
        
        # Set supplementQty = qtyReceived (excluding -1) for corrective rows whose destination is a Supermarket (starts with KFM)
        is_corrective = df_clean['fromBranch'] == 'KHO RAU CỦ XỬ LÝ CHÊNH LỆCH CHUYỂN HÀNG'
        is_to_supermarket = df_clean['toBranch'].str.upper().str.startswith('KFM')
        
        # Cap original received qty: SL nhận <= SL chuyển từ kho rau củ
        is_orig = df_clean['fromBranch'] == 'KHO RAU CỦ'
        df_clean.loc[is_orig & (df_clean['qtyReceived'] > df_clean['qtyShipped']) & (df_clean['qtyReceived'] != -1), 'qtyReceived'] = df_clean.loc[is_orig & (df_clean['qtyReceived'] > df_clean['qtyShipped']) & (df_clean['qtyReceived'] != -1), 'qtyShipped']
        
        # Set supplementQty = qtyShipped for corrective rows
        df_clean.loc[is_corrective & is_to_supermarket, 'supplementQty'] = df_clean.loc[is_corrective & is_to_supermarket, 'qtyShipped']
        df_clean.loc[is_corrective & ~is_to_supermarket, 'supplementQty'] = 0

        # Map nguoiChia using perf_map
        def get_nguoi_chia(r):
            val = perf_map.get((r['transferCode'], r['itemCode']))
            if val:
                return val
            if 'nguoiChia' in r and pd.notna(r['nguoiChia']) and r['nguoiChia'] != "":
                return r['nguoiChia']
            return ""
        df_clean['nguoiChia'] = df_clean.apply(get_nguoi_chia, axis=1)

        # Inherit nguoiChia for corrective rows from original rows with matching itemCode, toBranch, and date proximity (within 3 days)
        is_orig = df_clean['fromBranch'] == 'KHO RAU CỦ'
        orig_lookup = {}
        for idx, row in df_clean[is_orig].iterrows():
            if not row['nguoiChia']:
                continue
            key = (row['toBranch'], row['itemCode'])
            if key not in orig_lookup:
                orig_lookup[key] = []
            try:
                d_obj = datetime.strptime(row['date'], '%Y-%m-%d')
                orig_lookup[key].append((d_obj, row['nguoiChia']))
            except:
                pass

        corr_indices = df_clean[is_corrective].index
        for idx in corr_indices:
            row = df_clean.loc[idx]
            key = (row['toBranch'], row['itemCode'])
            candidates = orig_lookup.get(key)
            if candidates:
                try:
                    c_date_obj = datetime.strptime(row['date'], '%Y-%m-%d')
                    best_nc = ""
                    min_diff = timedelta(days=4)
                    for o_date_obj, nc in candidates:
                        diff = abs(o_date_obj - c_date_obj)
                        if diff <= timedelta(days=3) and diff < min_diff:
                            min_diff = diff
                            best_nc = nc
                    if best_nc:
                        df_clean.at[idx, 'nguoiChia'] = best_nc
                except Exception as e_inherit:
                    pass
        
        # Filter out rows with all empty or invalid values
        df_clean = df_clean[df_clean['itemCode'] != 'nan']
        df_clean = df_clean[df_clean['itemCode'] != '']
        
        # Filter out canceled documents (docStatus contains 'hủy')
        df_clean = df_clean[~df_clean['docStatus'].str.lower().str.contains('hủy|huy', na=False)]
        
        # Filter out container items
        df_clean = df_clean[~df_clean['itemCode'].isin(['CC00360', 'CC00381'])]
        
        # Deduplicate shipping transfers based on unique transfer line
        df_clean.drop_duplicates(subset=['transferCode', 'itemCode', 'toBranch'], keep='last', inplace=True)
        
        # Drop temporary 'daHauKiem' column
        if 'daHauKiem' in df_clean.columns:
            df_clean = df_clean.drop(columns=['daHauKiem'])
        
        # Add ID index
        df_clean.insert(0, 'id', range(1, len(df_clean) + 1))
        
        # Convert to records list
        records = df_clean.to_dict(orient='records')
        
        # Load category mapping
        mapping = {}
        mapping_path = "scratch/category_mapping.json"
        if os.path.exists(mapping_path):
            try:
                with open(mapping_path, "r", encoding="utf-8") as f_map:
                    mapping = json.load(f_map)
                print(f"Đã tải thành công category mapping: {len(mapping)} keys.")
            except Exception as e_map:
                print(f"Lỗi khi tải category mapping: {e_map}")
        else:
            print("WARNING: category_mapping.json không tồn tại!")

        # Inject nganhHang field into shipping transfers
        for r in records:
            code = r.get("itemCode", "").strip()
            info = mapping.get(code)
            r["nganhHang"] = info["category"] if info else ""

        # Inject nganhHang field into performance transfers
        for r in perf_records:
            code = r.get("barcode", "").strip()
            info = mapping.get(code)
            r["nganhHang"] = info["category"] if info else ""

        print(f"Đã xử lý xong {len(records)} bản ghi điều chuyển hàng hợp lệ.")
        
        # Create a compressed data structure to keep data.js under GitHub's 100MB file limit
        # 1. Normalization: Item Catalog
        item_catalog = {}
        for r in records:
            code = r.get("itemCode", "")
            if code and code not in item_catalog:
                info = mapping.get(code)
                path = info.get("categoryPath", "") if info else ""
                level3 = ""
                if path:
                    parts = [p.strip() for p in path.split(">")]
                    if len(parts) > 2:
                        level3 = parts[2]
                item_catalog[code] = [r.get("itemName", ""), r.get("nganhHang", ""), r.get("unit", ""), level3]
        for r in perf_records:
            code = r.get("barcode", "")
            if code and code not in item_catalog:
                info = mapping.get(code)
                path = info.get("categoryPath", "") if info else ""
                level3 = ""
                if path:
                    parts = [p.strip() for p in path.split(">")]
                    if len(parts) > 2:
                        level3 = parts[2]
                item_catalog[code] = [r.get("tenSanPham", ""), r.get("nganhHang", ""), r.get("donVi", ""), level3]


        # 2. Index Mapping: Branches
        branches = []
        def get_branch_idx(name):
            if not name: return -1
            if name not in branches:
                branches.append(name)
            return branches.index(name)

        # 3. Index Mapping: Users
        users = []
        def get_user_idx(name):
            if not name: return -1
            if name not in users:
                users.append(name)
            return users.index(name)

        # 4. Compress transfers
        # Columns: [id, date, fromBranch, toBranchIdx, itemCode, qtyShipped, qtyReceived, transferCode, generatedDoc, docStatus, nguoiChiaIdx]
        compressed_trans = []
        for r in records:
            fb = "XL" if "XỬ LÝ" in r.get("fromBranch", "") else "RC"
            row = [
                r.get("id"),
                r.get("date"),
                fb,
                get_branch_idx(r.get("toBranch")),
                r.get("itemCode"),
                r.get("qtyShipped"),
                r.get("qtyReceived"),
                r.get("transferCode"),
                r.get("generatedDoc"),
                r.get("docStatus"),
                get_user_idx(r.get("nguoiChia"))
            ]
            compressed_trans.append(row)

        # 5. Compress performance
        # Columns: [id, maYeuCau, maPhieu, barcode, noiNhanIdx, qtyYcBanDau, qtyHeThong, qtyThucChia, trangThai, trangThaiPR, trangThaiChuyen, canChia, chotNhan, ngayChuyen, ngayGiaoDuKien, noiChuyen, maPhieuChuyen, ngayCapNhat, nguoiCapNhat, batDauChia, hoanTatChia, slRo, slKien, nguoiChiaIdx]
        compressed_perf = []
        for r in perf_records:
            row = [
                r.get("id"),
                r.get("maYeuCau"),
                r.get("maPhieu"),
                r.get("barcode"),
                get_branch_idx(r.get("noiNhan")),
                r.get("qtyYcBanDau"),
                r.get("qtyHeThong"),
                r.get("qtyThucChia"),
                r.get("trangThai"),
                r.get("trangThaiPR"),
                r.get("trangThaiChuyen"),
                r.get("canChia"),
                r.get("chotNhan"),
                r.get("ngayChuyen"),
                r.get("ngayGiaoDuKien"),
                r.get("noiChuyen"),
                r.get("maPhieuChuyen"),
                r.get("ngayCapNhat"),
                r.get("nguoiCapNhat"),
                r.get("batDauChia"),
                r.get("hoanTatChia"),
                r.get("slRo"),
                r.get("slKien"),
                get_user_idx(r.get("nguoiChia"))
            ]
            compressed_perf.append(row)

        # Write to data.js
        with open("data.js", "w", encoding="utf-8") as f:
            f.write("// Autogenerated compressed data\n")
            f.write("window.itemCatalog = ")
            json.dump(item_catalog, f, ensure_ascii=False)
            f.write(";\n\n")
            
            f.write("window.branchesList = ")
            json.dump(branches, f, ensure_ascii=False)
            f.write(";\n\n")
            
            f.write("window.usersList = ")
            json.dump(users, f, ensure_ascii=False)
            f.write(";\n\n")
            
            f.write("window.compressedTransfers = ")
            json.dump(compressed_trans, f, ensure_ascii=False)
            f.write(";\n\n")
            
            f.write("window.compressedPerformance = ")
            json.dump(compressed_perf, f, ensure_ascii=False)
            f.write(";\n\n")
            
            # Load price map and write it to data.js
            price_map = {}
            price_map_path = "scratch/price_map.json"
            if os.path.exists(price_map_path):
                try:
                    with open(price_map_path, "r", encoding="utf-8") as f_price:
                        raw_price_map = json.load(f_price)
                        price_map = {bc: details["price"] for bc, details in raw_price_map.items()}
                    print(f"Đã tải {len(price_map)} giá từ price_map.json")
                except Exception as e_price:
                    print(f"Lỗi khi tải price_map.json: {e_price}")
            
            f.write("window.productPrices = ")
            json.dump(price_map, f, ensure_ascii=False)
            f.write(";\n")
            
        print("✅ Thành công: Đã ghi dữ liệu vào data.js")
        
    except Exception as e:
        print(f"Lỗi khi xử lý file Excel điều chuyển: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    parse_excel()
