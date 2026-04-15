---
title: Write up Sleuthkit Apprentice picoCTF2022

---

# [Write up Sleuthkit Apprentice picoCTF2022](https://play.picoctf.org/practice/challenge/300?category=4&difficulty=2&page=2)
## Dạng bài có mức độ medium trong chủ đề forensics 
### Writeup:
----
#### Bước 1:
- Sử dụng wget để tải file về thư mục trong ubuntu.
#### Bước 2:
- Sau khi tải về ta nhận được file có định dạng .img.gz. Đây là định dạng phổ biến của 1 file bị nén bằng gunzip.
```
disk.flag.img.gz
```
- Sử dụng gzip để giải nén lớp .gz của file. Sau ta nhận được một file system .img
![image](https://hackmd.io/_uploads/rkObyCtxbe.png)
#### Bước 3: 
- Sử dụng các lệnh như: fdish, mmls, ...
-- ***Mục đích***: kiểm tra xem file chứa những tệp bị nén nào, kiểm tra phân vùng, offset, định dạng, metadata
![image](https://hackmd.io/_uploads/rk8rxAKlWg.png)
    - **LƯU Ý** : file có offset = 206848 không thể truy cập bình thường bằng binwalk hay fls do có dạng Linux Swap,..
#### Bước 4:
- Sử dụng lệnh binwalk -e filename để tạo 1 thư mục extracted
``` 
binwalk -e disk.flag.img
```
![image](https://hackmd.io/_uploads/BkorZ0tgZx.png)
- Ta sẽ nhận được 1 thư mục như sau:
![image](https://hackmd.io/_uploads/Bk1U-AKebl.png)

#### Bước 5: 
- Các file chứa flag sẽ thường được giấu dưới dạng file.txt và giấu trong 1 thư mục hoặc 1 file bị encrypt. Như vậy mục tiêu của ta sẽ tìm các file có dạng .txt trong thư mục đã được extracted
- Ở đây ta sẽ sử dụng lệnh find /path_to_folder -iname "*.txt"
```
find /path_to_folder -iname "*.txt"
```
![image](https://hackmd.io/_uploads/SygdmCYlWg.png)

- Ta sẽ nhận được một đường dẫn để vào được thư mục cần tìm

#### Bước 6: 
- Truy cập vào đường dẫn nhận được và lấy flag
```
cd path_t_file
cat file.txt
```
![image](https://hackmd.io/_uploads/SkdtNRKgWl.png)
