---
title: Silicon Data Sleuthing

---

# [Write up Silicon Data Sleuthing HTB CTF try out](https://ctf.hackthebox.com/event/1434)
## Dạng bài có mức độ easy trong chủ đề forensics 
### Writeup:
----
### Description:
- In the dust and sand surrounding the vault, you unearth a rusty PCB... You try to read the etched print, it says Open..W...RT, a router! You hand it over to the hardware gurus and to their surprise the ROM Chip is intact! They manage to read the data off the tarnished silicon and they give you back a firmware image. It's now your job to examine the firmware and maybe recover some useful information that will be important for unlocking and bypassing some of the vault's countermeasures!
---
#### Bước 1:
- Sử dụng wget để tải file về thư mục trong ubuntu.
#### Bước 2:
- Sau khi tải file, ta thấy file có định dạng file.bin (Tức là 1 file dữ liệu nhị phân thô)
- Kết hợp với đoạn mô tả thì ta biết đây là 1 file lưu dữ liệu firmware của 1 router có tên là OpenWRT ([firmware file](https://gist.github.com/lopestom/ce250f5de64a2764ee85092a2c01939e))
#### Bước 3: 
- Sử dụng lệnh binwalk + file.bin kể kiểm tra các phân vùng của của file
![image](https://hackmd.io/_uploads/H19yyioKWx.png)
- Ta nhận thấy file chứa khá nhiều phân vùng lạ, nhưng để ý thấy nó tồn tại 2 phân vùng chứa các tệp tin của hệ thống.
```
Squashfs
JFFS2
```
- Tìm hiểu thông tin về 2 phân vùng đó, ta thu được 1 số thông tin như sau:

| Squashfs | JFFS2 |
| -------- | -------- |
| - Là một phân vùng nén chỉ đọc (read-only) giúp cùng cấp khả năng lưu trữ tốt hơn JFF2.    | - là một tệp siêu dữ liệu nhằm lưu trữ thông tin của hệ thống trước khi sửa chữa để tránh các sự cố như mất điện trong quá trình cập nhật và xây dựng hệ thống nhúng( tệp nhật kí hệ thống)   | 

[filesystem](https://openwrt.org/docs/techref/filesystems)
- Cấu hình người dùng(overlay) thường được nén đầy đủ trong JFFS2.
- Những cấu hình tối thiểu để hệ thống hoạt động thì được lưu trong phân vùng Squashfs
#### Bước 4:
- Để có thể đọc và lấy dữ liệu từ phân vùng của JFFS2 thì ta cần công cụ jefferson( tải thông qua git).
- Sử dụng `binwalk -e file.bin` để trích xuất dữ liệu thô thành thư mục dữ liệu.
- Sử dụng netcat để chạy docker của thử thách.
### Câu hỏi 1: What version of OpenWRT runs on the router (ex: 21.02.0)
#### Ans: 23.05.0
- Truy cập vào thư mục Squashfs-root để kiểm tra các thư mục lưu cấu hình của hệ thống. Thông thường cấu hình hệ thống sẽ được lưu với tên gọi _release hoặc _version.
- Ta thấy trong đường dẫn: `_chal_router_dump.bin.extracted\squashfs-root\etc` chứa 2 file `openwrt_release và openwrt_version`. Kiểm tra 2 file ta sẽ thu được kết quả là: `23.05.0`.

### Câu hỏi 2: What is the Linux kernel version (ex: 5.4.143)
#### Ans: 5.15.134
- Có nhiều cách để kiểm tra phiên bản kernel của Linux được sử dụng trong phiên bản OpenWRT của câu hỏi.
- Cách nhanh nhất là lên trang chủ của OpenWRT để kiểm tra theo phiên bản OpenWRT đã trả lời ở câu hỏi trên.
![image](https://hackmd.io/_uploads/SJ-pwostWx.png)

### Câu hỏi 3: What's the hash of the root account's password, enter the whole line (ex: root:$2$JgiaOAai....)
#### Ans: `root:$1$YfuRJudo$cXCiIJXn9fWLIt8WY2Okp1:19804:0:99999:7:::`
-  Như đã tìm hiểu ở trên thì cấu hình và thống tin người dùng được lưu trữ và nén trong phân vùng JFFS2. Kiểm tra thư mục sau khi ta giải nén dữ liệu thô thì ta thấy phân vùng 7C0000.jffs2 chưa được trích xuất.
![image](https://hackmd.io/_uploads/rkLBtootWl.png)
- Do đó ta sẽ sử dụng công cụ jefferson để giải nén và trích xuất thông tin từ phân vùng này.
![image](https://hackmd.io/_uploads/HJT3tojtWl.png)
- Truy cập vào thư mục jffs2-root và dùng lệnh tree . để kiểm tra cây thư mục.
```
.
├── 1 -> 2
├── upper
│   └── sysupgrade.tgz
└── work
    └── work
        ├── #1
        ├── #11
        ├── #13
        ├── #14
        ├── #16
        ├── #18
        ├── #1a
        ├── #1c
        ├── #1e
        ├── #1f
        ├── #2
        ├── #21
        ├── #22
        ├── #24
        ├── #26
        ├── #27
        ├── #28
        ├── #2a
        ├── #2c
        ├── #2e
        ├── #3
        │   ├── board.json
        │   ├── uhttpd.crt
        │   ├── uhttpd.key
        │   └── urandom.seed
        ├── #30
        ├── #32
        ├── #34
        ├── #36
        ├── #38
        ├── #39
        ├── #4
        │   ├── network
        │   ├── system
        │   └── wireless
        ├── #48
        ├── #7
        ├── #9
        ├── #b
        ├── #d
        └── #f
```
- Ta thấy trong đường dẫn `jffs2-root\work\work` có cấu trúc trong giống với cấu trúc của folder`squashfs-root` tuy nhiên tên đã bị thay đổi nên việc tìm kiếm sẽ rất khó khăn, vậy nên ta chuyển hướng điều tra qua thư mục upper.
- Trong thư mục này chứa file nén .tgz. Sau khi giải nén file này, ta lại nhận được 1 file nén khác có dạng .tar . Tiếp tục giải nén, thì ta sẽ nhận được 1 thư mục cùng tên. Kiểm tra cấu trúc thì ta nhận được kết quả như sau:
```
.
├── etc
│   ├── config
│   │   ├── dhcp
│   │   ├── dropbear
│   │   ├── firewall
│   │   ├── luci
│   │   ├── network
│   │   ├── rpcd
│   │   ├── system
│   │   ├── ucitrack
│   │   ├── uhttpd
│   │   └── wireless
│   ├── dropbear
│   │   ├── dropbear_ed25519_host_key
│   │   └── dropbear_rsa_host_key
│   ├── group
│   ├── hosts
│   ├── inittab
│   ├── luci-uploads
│   ├── nftables.d
│   │   ├── 10-custom-filter-chains.nft
│   │   └── README
│   ├── opkg
│   │   └── keys
│   │       └── b5043e70f9a75cde
│   ├── passwd
│   ├── profile
│   ├── rc.local
│   ├── shadow
│   ├── shells
│   ├── shinit
│   ├── sysctl.conf
│   ├── uhttpd.crt
│   └── uhttpd.key
└── sysupgrade.tar
```
- Đây là cấu trúc chuẩn của filesystem. Điều tra trong đây thì ta thu được kết quả cần tìm trong file `shadow` trong thư mục `/ect`.
### Câu hỏi 4: What is the PPPoE username?
#### Ans: yohZ5ah

![image](https://hackmd.io/_uploads/HJLQEV3KZl.png)

- Như vậy ta chỉ cần kiểm tra trong các thư mục hoặc file có chứa thông tin về network. Câu trả lời nằm trong file `network` của thư mục config.

### Câu hỏi 5: What is the PPPoE password
#### Ans: ae-h+i$i^Ngohroorie!bieng6kee7oh
- Đáp án này nằm ngay bên dưới đáp án của câu hỏi 4

### Câu hỏi 6: What is the WiFi SSID
#### Ans: VLT-AP01
- Ta có thể suy đoán rằng thư mục config sẽ chứa các thông tin cấu hình của router. Vậy nên ta sẽ sử dụng lệnh `strings * | grep "ssid" ` để lấy toàn bộ nội dung ta cần tìm trong thư mục này.
- Hoặc ta có thể dùng lệnh `grep -rni "keywork" pathtofile`
- ![image](https://hackmd.io/_uploads/SkWBDE3KWe.png)

### Câu hỏi 7: What is the WiFi Password
#### Ans: french-halves-vehicular-favorable
- Ở câu này ta có thể dùng lệnh `grep -rni "ssid" pathtofile` để tìm đệ quy từ khóa này trong thư mục (vì ta nghi ngờ rằng passwork có thể được lưu trữ trong cùng 1 file với nội dung của thông tin ở câu 6).
![image](https://hackmd.io/_uploads/S1I3YV2Y-g.png)
- Như vậy từ khóa trên được lưu trong file wireless trong thư mục config.
![image](https://hackmd.io/_uploads/HkW-i42Kbg.png)

### Câu hỏi 8: What are the 3 WAN ports that redirect traffic from WAN -> LAN (numerically sorted, comma sperated: 1488,8441,19990)
#### Ans: 1778, 2289, 8088
- Việc chuyển lưu lượng đường truyền từ WAN -> LAN thường được lưu trữ trong tường lửa của router. Tiến hành kiểm tra thì ta thu được kết quả.
```
config redirect
	option dest 'lan'
	option target 'DNAT'
	option name 'DB'
	option src 'wan'
	option src_dport '1778'
	option dest_ip '192.168.1.184'
	option dest_port '5881'

config redirect
	option dest 'lan'
	option target 'DNAT'
	option name 'WEB'
	option src 'wan'
	option src_dport '2289'
	option dest_ip '192.168.1.119'
	option dest_port '9889'

config redirect
	option dest 'lan'
	option target 'DNAT'
	option name 'NAS'
	option src 'wan'
	option src_dport '8088'
	option dest_ip '192.168.1.166'
	option dest_port '4431'
```
- Ta có thể dùng lệnh tìm kiếm đệ quy như trên với 1 số từ khóa như: "lan", "wan", "redirect", ... thì cũng thu được kết quả tương ứng.


### Sau khi trả lời xong tất cả câu hỏi tên server sẽ trả về cho ta flag.





