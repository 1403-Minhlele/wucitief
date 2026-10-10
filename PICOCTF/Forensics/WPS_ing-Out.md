# WU - Gone_Surfing

## 1. Thông tin challenge

-   **Tên/đề:** WPA / Wireless
-   **File PCAP:** `wpa-ing_out.pcap`
-   **ESSID:** `Gone_Surfing`
-   **BSSID:** `00:5F:67:4F:6A:1A`
-   **Mã hóa:** WPA
-   **Flag format:** `academy{XXXXXX}`

## 2. Ý tưởng tổng quát

Challenge cung cấp một file PCAP chứa traffic Wi-Fi và mô tả cho biết
mật khẩu của mạng nằm trong `rockyou.txt`.

Hai hint của challenge lần lượt hướng tới:

1.  Xác định traffic IEEE 802.11 bằng Wireshark.
2.  Sử dụng Aircrack-ng để xử lý PCAP và crack mật khẩu.

Flow giải:

``` text
PCAP
 │
 ├── Phân tích Wireshark
 │       │
 │       └── lọc EAPOL
 │              │
 │              └── phát hiện WPA 4-way handshake
 │
 ├── Aircrack-ng
 │       │
 │       └── xác định ESSID/BSSID
 │              │
 │              └── WPA (1 handshake)
 │
 └── RockYou
         │
         └── brute-force offline
                │
                └── KEY FOUND
                       │
                       └── academy{password}
```

Điểm quan trọng: RockYou không được truyền qua Wi-Fi. Aircrack-ng sử
dụng wordlist ở máy local để thử các mật khẩu trên handshake đã thu được
trong PCAP.

------------------------------------------------------------------------

# 3. Phân tích PCAP bằng Wireshark

Mở file:

``` bash
wireshark wpa-ing_out.pcap
```

Challenge nói về wireless traffic nên bước đầu tiên là kiểm tra các
packet 802.11.

Có thể lọc EAPOL bằng display filter:

``` text
eapol
```

## 3.1. EAPOL là gì?

EAPOL (Extensible Authentication Protocol over LAN) được sử dụng trong
quá trình xác thực WPA/WPA2.

Đối với WPA/WPA2-PSK, quá trình xác thực có 4 message chính:

``` text
Message 1 of 4
Message 2 of 4
Message 3 of 4
Message 4 of 4
```

Nếu PCAP chứa đủ các message này, ta có một WPA 4-way handshake có thể
sử dụng cho việc kiểm tra mật khẩu offline.

------------------------------------------------------------------------

# 4. Phát hiện WPA 4-way handshake

Sau khi filter:

``` text
eapol
```

Wireshark hiển thị nhiều packet EAPOL.

Một chuỗi đáng chú ý:

``` text
No. 50  → Key (Message 1 of 4)
No. 51  → Key (Message 2 of 4)
No. 52  → Key (Message 3 of 4)
No. 53  → Key (Message 4 of 4)
```

Ngoài ra còn có các chuỗi handshake khác, ví dụ:

``` text
1360 → Message 1 of 4
1362 → Message 2 of 4
1363 → Message 3 of 4
1364 → Message 4 of 4
```

và các chuỗi xuất hiện ở khoảng packet 22791 và 23020.

Như vậy PCAP không chỉ chứa EAPOL đơn lẻ mà có các bộ:

``` text
M1 → M2 → M3 → M4
```

Đây là bằng chứng PCAP đã capture WPA 4-way handshake.

------------------------------------------------------------------------

# 5. Liên hệ với Deauthentication

Trong quá trình phân tích wireless PCAP, có thể kiểm tra thêm các packet
Deauthentication bằng filter:

``` text
wlan.fc.type_subtype == 0x0c
```

Nếu thấy pattern:

``` text
Deauthentication
      ↓
Authentication
      ↓
Association Request
      ↓
Association Response
      ↓
EAPOL Message 1
      ↓
EAPOL Message 2
      ↓
EAPOL Message 3
      ↓
EAPOL Message 4
```

thì đây là pattern thường gặp khi một client bị disconnect rồi kết nối
lại, giúp attacker capture lại WPA handshake.

Tuy nhiên, cần phân biệt hai ý:

-   `Deauthentication` cho thấy có hoạt động disconnect/reconnect.
-   `EAPOL M1-M4` mới là bằng chứng trực tiếp cho việc đã capture 4-way
    handshake.

Không thể chỉ dựa vào một packet Deauthentication để kết luận có
password cracking.

------------------------------------------------------------------------

# 6. Kiểm tra handshake bằng Aircrack-ng

Sau khi xác định PCAP có EAPOL handshake, sử dụng Aircrack-ng để kiểm
tra:

``` bash
aircrack-ng wpa-ing_out.pcap
```

Aircrack-ng đọc PCAP và phân tích các handshake.

Kết quả:

``` text
#   BSSID              ESSID          Encryption
1   00:5F:67:4F:6A:1A  Gone_Surfing   WPA (1 handshake)
```

Các thông tin quan trọng:

``` text
BSSID       = 00:5F:67:4F:6A:1A
ESSID       = Gone_Surfing
Encryption  = WPA
Handshake   = 1
```

Dòng:

``` text
WPA (1 handshake)
```

xác nhận Aircrack-ng đã nhận diện được một handshake phù hợp trong PCAP.

------------------------------------------------------------------------

# 7. Tại sao Aircrack-ng biết handshake hợp lệ?

WPA-PSK không gửi password plaintext trong quá trình kết nối.

Thay vào đó, 4-way handshake chứa các giá trị mật mã được tạo dựa trên:

-   SSID
-   password/PSK
-   nonce
-   MAC address
-   các thông tin của quá trình handshake

Khi có handshake, attacker có thể lấy từng password ứng viên từ wordlist
và tính toán lại các giá trị cần thiết.

Nếu kết quả khớp với dữ liệu trong handshake:

``` text
candidate password
       ↓
cryptographic calculation
       ↓
match handshake
       ↓
password đúng
```

Do đó không cần kết nối lại với AP để thử từng password.

Đây là **offline password cracking**.

------------------------------------------------------------------------

# 8. Sử dụng RockYou

Challenge description đã cho biết:

> password xuất hiện trong `rockyou.txt`

Vì vậy cần cung cấp RockYou cho Aircrack-ng.

Trước tiên kiểm tra xem máy đã có wordlist chưa:

``` bash
find /usr/share/wordlists -iname 'rockyou*' 2>/dev/null
```

Nếu thấy:

``` text
/usr/share/wordlists/rockyou.txt
```

thì có thể sử dụng trực tiếp.

Nếu thấy:

``` text
/usr/share/wordlists/rockyou.txt.gz
```

thì giải nén:

``` bash
sudo gzip -dk /usr/share/wordlists/rockyou.txt.gz
```

Sau đó file sẽ có dạng:

``` text
/usr/share/wordlists/rockyou.txt
```

------------------------------------------------------------------------

# 9. Crack WPA password

Chạy:

``` bash
aircrack-ng wpa-ing_out.pcap -w /usr/share/wordlists/rockyou.txt
```

Trong đó:

``` text
aircrack-ng
    ↓
chương trình crack WPA

wpa-ing_out.pcap
    ↓
file chứa WPA handshake

-w
    ↓
chỉ định wordlist

rockyou.txt
    ↓
danh sách password ứng viên
```

Aircrack-ng sẽ lần lượt thử các password trong RockYou.

Có thể hình dung:

``` text
rockyou.txt

password1
123456
qwerty
...
candidate_password
...
```

Mỗi password được kiểm tra với handshake trong PCAP.

------------------------------------------------------------------------

# 10. Kết quả mong đợi

Nếu password nằm trong RockYou, Aircrack-ng sẽ báo:

``` text
KEY FOUND! [ <password> ]
```

Ví dụ nếu giả sử password tìm được là:

``` text
example_password
```

thì output sẽ có dạng:

``` text
KEY FOUND! [ example_password ]
```

**Không lấy `example_password` làm flag nếu nó chỉ là ví dụ.**

Phải lấy chính password mà Aircrack-ng tìm được trong challenge.

------------------------------------------------------------------------

# 11. Tạo flag

Challenge yêu cầu format:

``` text
academy{XXXXXX}
```

Do đó nếu Aircrack-ng trả về:

``` text
KEY FOUND! [ abc123 ]
```

thì flag sẽ là:

``` text
academy{abc123}
```

------------------------------------------------------------------------

# 12. Các dấu hiệu quan trọng trong bài

## Dấu hiệu 1: EAPOL

Wireshark filter:

``` text
eapol
```

Cho thấy quá trình WPA authentication.

## Dấu hiệu 2: Message 1-4

Các packet:

``` text
Message 1 of 4
Message 2 of 4
Message 3 of 4
Message 4 of 4
```

cho thấy một 4-way handshake hoàn chỉnh đã được capture.

## Dấu hiệu 3: Aircrack nhận diện handshake

``` text
WPA (1 handshake)
```

Đây là xác nhận trực tiếp từ Aircrack-ng rằng PCAP có handshake có thể
dùng để crack.

## Dấu hiệu 4: Challenge nói password nằm trong RockYou

Do đó không cần tự đoán password.

Ta chỉ cần:

``` text
PCAP + handshake + rockyou.txt
```

để thực hiện offline dictionary attack.

------------------------------------------------------------------------

# 13. Vì sao không thể thấy "RockYou" trong PCAP?

Đây là điểm quan trọng khi phân tích forensic.

PCAP chỉ ghi lại traffic giữa các thiết bị trên mạng Wi-Fi.

Trong khi đó quá trình:

``` text
Aircrack-ng
    ↓
đọc rockyou.txt
    ↓
thử password
    ↓
kiểm tra handshake
```

diễn ra trên máy attacker.

Vì vậy PCAP có thể chứng minh:

``` text
WPA handshake đã được capture
```

nhưng không thể tự nó chứng minh:

``` text
attacker đã sử dụng rockyou.txt
```

Trong challenge này, thông tin về RockYou được cung cấp bởi
description/hint.

------------------------------------------------------------------------

# 14. Các lệnh hoàn chỉnh

## Bước 1 - Kiểm tra PCAP

``` bash
aircrack-ng wpa-ing_out.pcap
```

## Bước 2 - Tìm RockYou

``` bash
find /usr/share/wordlists -iname 'rockyou*' 2>/dev/null
```

## Bước 3 - Nếu file bị nén

``` bash
sudo gzip -dk /usr/share/wordlists/rockyou.txt.gz
```

## Bước 4 - Crack

``` bash
aircrack-ng wpa-ing_out.pcap -w /usr/share/wordlists/rockyou.txt
```

## Bước 5 - Lấy password

Tìm dòng:

``` text
KEY FOUND! [ ... ]
```

## Bước 6 - Submit flag

``` text
academy{PASSWORD}
```

------------------------------------------------------------------------

# 15. Kết luận

PCAP `wpa-ing_out.pcap` chứa wireless traffic của mạng:

``` text
ESSID : Gone_Surfing
BSSID : 00:5F:67:4F:6A:1A
```

Phân tích bằng Wireshark với filter:

``` text
eapol
```

cho thấy nhiều WPA EAPOL 4-way handshake hoàn chỉnh với các message:

``` text
M1 → M2 → M3 → M4
```

Sau đó Aircrack-ng xác nhận:

``` text
Gone_Surfing
WPA (1 handshake)
```

Challenge cho biết password nằm trong `rockyou.txt`, vì vậy sử dụng:

``` bash
aircrack-ng wpa-ing_out.pcap -w /usr/share/wordlists/rockyou.txt
```

Aircrack-ng thực hiện dictionary attack offline trên handshake. Khi xuất
hiện:

``` text
KEY FOUND! [ PASSWORD ]
```

thì password đó được đưa vào format:

``` text
academy{PASSWORD}
```

Đây là toàn bộ hướng giải của challenge.
