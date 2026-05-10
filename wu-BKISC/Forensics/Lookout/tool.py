import re

def decrypt_specula_payload(hex_str, key):
    # Loại bỏ dấu ngoặc kép thừa nếu có
    hex_str = hex_str.strip('"').strip()
    decrypted = ""
    position = 0
    
    # Duyệt qua từng cặp 2 ký tự Hex (1 byte)
    for i in range(0, len(hex_str), 2):
        hex_byte = hex_str[i:i+2]
        
        if len(hex_byte) < 2:
            break
            
        try:
            cptx = int(hex_byte, 16)
        except ValueError:
            continue
            
        # Lấy ký tự tương ứng trong khóa giải mã
        key_char = key[position % len(key)]
        keyx = ord(key_char)
        
        # Giải mã XOR
        orgx = cptx ^ keyx
        decrypted += chr(orgx)
        position += 1
        
    return decrypted

def main():
    # ==============================================================================
    # BẠN CẦN THAY THẾ CHUỖI NÀY BẰNG KEY LẤY TỪ FILE NTUSER.DAT CỦA NẠN NHÂN
    # ==============================================================================
    SECRET_KEY = "o4WlfbKbx1xik1TgTQGeOQ" 
    
    if SECRET_KEY == "o4WlfbKbx1xik1TgTQGeOQ":
        print("[!] CẢNH BÁO: Bạn chưa nhập SECRET_KEY. Kết quả giải mã sẽ là rác.")
        print("[!] Hãy mở file NTUSER.DAT trong FTK Imager, tìm value KEY và thay vào script.\n")
    
    # Đọc nội dung file cấu trúc HTTP Stream
    try:
        with open("malware.txt", "r", encoding="utf-8") as f:
            log_data = f.read()
    except FileNotFoundError:
        print("[Lỗi] Không tìm thấy file malware.txt. Hãy đặt file cùng thư mục với script.")
        return

    # Regex trích xuất nội dung POST: Các chuỗi Hex viết hoa, dài >= 6 ký tự, nằm trong ngoặc kép
    pattern = r'"([A-F0-9]{6,})"'
    payloads = re.findall(pattern, log_data)
    
    print(f"[*] Đã tìm thấy {len(payloads)} payloads dữ liệu bị đánh cắp.\n")
    
    for i, payload in enumerate(payloads):
        print(f"--- Payload {i+1} (Chiều dài: {len(payload)} ký tự Hex) ---")
        
        # Tiến hành giải mã
        decrypted_text = decrypt_specula_payload(payload, SECRET_KEY)
        
        # Bộ lọc in an toàn: Biến các ký tự điều khiển/rác thành dấu chấm để không hỏng terminal
        safe_print = ''.join(c if c.isprintable() or c in ['\n', '\r', '\t'] else '.' for c in decrypted_text)
        
        print(f"Raw Hex (rút gọn) : {payload[:60]}...")
        print("Dữ liệu giải mã   :\n" + safe_print + "\n" + "-"*50)

if __name__ == "__main__":
    main()