# 🛡️ CyberDump Triage Toolkit

> **Bộ công cụ giám định số & phân tích Memory Dump / File thực thi nhị phân hiệu năng cao, tối ưu hóa cho file lớn từ 10 - 30+ GB với Web UI Dashboard hiện đại, Desktop GUI, Trợ lý AI và triển khai Docker 1-Click.**

---

## 🌟 Giới thiệu

**CyberDump Triage Toolkit** là giải pháp phân tích và giám định bộ nhớ (Memory Forensics / Incident Response) chuyên nghiệp, được thiết kế tối ưu cho các chuyên gia an ninh mạng (SOC/DFIR) và người chơi CTF. 

Bộ công cụ giải quyết triệt để vấn đề **tràn RAM (Out-Of-Memory)** và **treo máy** khi xử lý các file memory dump dung lượng cực lớn (**10 GB đến 30+ GB**), đồng thời cung cấp giao diện người dùng trực quan, biểu đồ trực tiếp, trình phân tích mã nhị phân và xuất báo cáo giám định sự cố tự động kết hợp AI.

---

## ✨ Tính năng nổi bật

### ⚡ 1. Công nghệ Streaming Chunk Engine ($O(1)$ RAM)
- **Cố định mức RAM dưới 60 MB**: Xử lý dữ liệu tuần tự theo từng khối buffer 8 MB kết hợp vùng gối đầu (4 KB Overlap), đảm bảo không bao giờ bị đứt chuỗi hoặc bỏ sót dấu vết ở ranh giới giữa các khối.
- **Trích xuất On-The-Fly**: Nhận diện và phân loại ngay các dấu hiệu xâm phạm (IOCs) trong lúc stream, không lưu trữ hàng triệu chuỗi rác vào bộ nhớ.
- **Ước lượng Shannon Entropy tức thì**: Sử dụng kỹ thuật lấy mẫu phân tán đa khối (Sparse Multi-Block Sampling), tính toán độ hỗn loạn entropy của file 30 GB trong **$< 0.1$ giây**.
- **Theo dõi Tiến độ Thời gian thực (Live Progress Tracker)**: Hiển thị liên tục tốc độ đọc I/O (`MB/s`), thời gian ước tính hoàn thành (`ETA`), `% tiến độ` và `số lượng IOCs tìm thấy`.

---

### 🔍 2. Nhận diện Dấu hiệu Xâm phạm (IOCs) Toàn diện
- 🌐 **Network IOCs**: Tự động phát hiện URLs (`http/https`), địa chỉ IPv4 (phân loại Public IP vs Private IP), Tên miền (Domains), và Emails.
- 🚨 **Lệnh Thực thi Nguy hiểm**: Phát hiện các câu lệnh hay bị lạm dụng như `powershell -enc`, `cmd.exe /c`, `certutil -decode`, `bitsadmin`, `vssadmin delete shadows`, `wmic`, `mshta`, `schtasks`.
- 📦 **Giải mã Base64 Payloads**: Nhận diện các đoạn mã hóa Base64 dài và tự động giải mã nội dung preview xem trước.
- 🗝️ **Persistence & Registry**: Dò quét các khóa Registry khởi động (`HKLM\Software\...`, Run keys).
- 💰 **Ví Tiền điện tử**: Nhận diện địa chỉ ví Bitcoin (BTC) và Ethereum (ETH).
- 🧬 **Tiến trình & Module DLL**: Tự động dò vết hơn 100+ tiến trình hệ thống và công cụ tấn công nổi tiếng (Mimikatz, Cobalt Strike, PsExec, v.v.).

---

### ⚙️ 3. Phân tích Cấu trúc PE & Section Entropy
- Hỗ trợ đầy đủ định dạng thực thi **PE 32-bit (PE32)** và **64-bit (PE32+)**.
- Phân tích Shannon Entropy trên từng section (`.text`, `.data`, `.rsrc`...) nhằm cảnh báo nhị phân bị **nén hoặc mã hóa (Packed/Encrypted)** khi entropy $> 7.0$.
- Soi chiếu bảng Import Table để phát hiện các **Suspicious Windows APIs** thường dùng trong mã độc (`VirtualAlloc`, `WriteProcessMemory`, `CreateRemoteThread`, `InternetOpenA`...).
- Kiểm tra các cơ chế bảo vệ nhị phân: ASLR, DEP/NX, Control Flow Guard (CFG), High Entropy 64-bit VA.

---

### 📊 4. Đánh giá Mức độ Rủi ro (Threat Scoring & Verdict)
- Tự động tổng hợp dữ liệu, chấm điểm rủi ro động từ **0 đến 100** và đưa ra kết luận phân loại mức độ:
  - 🟢 **CLEAN** (0 - 15): Dữ liệu sạch / hoạt động bình thường.
  - 🟡 **LOW / MEDIUM** (16 - 45): Có một số bất thường nhẹ cần lưu ý.
  - 🟠 **HIGH** (46 - 70): Dấu hiệu nghi vấn rõ rệt, cần phân tích sâu.
  - 🔴 **CRITICAL** (71 - 100): Phát hiện mã độc, payload tấn công hoặc công cụ nguy hiểm.

---

### 🖥️ 5. Hệ sinh thái Giao diện 3 Tầng
- 🌐 **Modern Web UI Dashboard**: Single Page Application với giao diện Dark Cyberpunk, kéo-thả file, thanh đo speedometer trực tiếp, tìm kiếm chuỗi tức thì (filter-as-you-type), xem mã Hex tương tác và tích hợp AI.
- 💻 **Native Desktop GUI**: Ứng dụng Tkinter đa luồng mượt mà, phân loại tab khoa học, không đơ giao diện khi quét file lớn.
- 📟 **Terminal CLI chuyên nghiệp**: Hiển thị màu ANSI với thanh tiến độ động trực tiếp trên terminal.

---

### 🤖 6. AI Forensic Studio (Trợ lý Giám định AI)
- Hỗ trợ đa nền tảng: **Ollama** (chạy offline nội bộ, bảo mật 100%), **Google Gemini API**, và **OpenAI/DeepSeek**.
- Tự động lập bảng ma trận kỹ thuật theo khung **MITRE ATT&CK** và đề xuất phương án ứng cứu sự cố.

---

### 📑 7. Xuất Báo cáo Đa định dạng
- 📄 **Interactive HTML Report**: Báo cáo HTML độc lập, giao diện đẹp mắt, dễ dàng đính kèm gửi khách hàng/đội ngũ.
- 📝 **Markdown Incident Report**: Báo cáo Markdown chuẩn cho tài liệu kỹ thuật.
- 💾 **Structured JSON**: Dữ liệu cấu trúc hóa cho các hệ thống SIEM/SOAR.

---

## 🐳 Triển khai nhanh với Docker (Khuyên dùng)

### 1. Triển khai 1-Click tự động:

```bash
# Trên Linux / macOS / WSL:
chmod +x deploy.sh
./deploy.sh

# Trên Windows (PowerShell):
.\deploy.ps1
```

### 2. Sử dụng Docker Compose:

```bash
# Khởi động Web Dashboard ở chế độ chạy nền
docker compose up -d

# Xem logs hoạt động
docker compose logs -f

# Dừng dịch vụ
docker compose down
```

Truy cập Web Dashboard tại: **`http://localhost:8080`**.

> **💡 Cách phân tích file lớn 10 - 30 GB với Docker**:
> Chỉ cần copy file dump vào thư mục `./dumps` trên máy của bạn. File sẽ tự động được ánh xạ vào container tại đường dẫn `/dumps/<tên_file>`. Bạn có thể nhập đường dẫn này trên Web UI hoặc chạy qua CLI:
> ```bash
> docker compose run --rm cyberdump --dump /dumps/challenge.mem
> ```

---

## 🚀 Khởi chạy Trực tiếp bằng Python (Không cần Docker)

Toàn bộ hệ thống core và Web UI đều chạy thuần túy trên **Python 3.8+** tiêu chuẩn với **100% Zero Dependency** (không bắt buộc cài thư viện ngoài).

```bash
# 1. Clone repository
git clone https://github.com/1403-Minhlele/wucitief.git
cd wucitief/toolkit/toolkit

# 2. Cài đặt các gói hỗ trợ phát triển (tuỳ chọn)
pip install -r requirements.txt
```

---

### 1. 🌐 Khởi động Web UI Dashboard

```bash
# Khởi động cổng mặc định (8080)
python src/main.py --web

# Hoặc chỉ định cổng tùy ý
python src/main.py --web --port 8080
```
Mở trình duyệt tại **`http://127.0.0.1:8080`**.

---

### 2. 💻 Khởi động Desktop GUI

```bash
python src/main.py --gui
```

---

### 3. 📟 Phân tích bằng dòng lệnh CLI

```bash
# Phân tích file dump mẫu
python src/main.py --dump samples/test_sample.dmp

# Phân tích file 10 - 30 GB và xuất tất cả báo cáo (HTML, Markdown, JSON)
python src/main.py --dump "D:\CTF\challenge.mem" --output reports/ --format all

# Phân tích kèm báo cáo tự động từ AI (Ollama Local)
python src/main.py --dump samples/test_sample.dmp --llm --provider ollama --model llama3.2

# Xuất dữ liệu JSON sạch cho pipeline tự động hóa
python src/main.py --dump samples/test_sample.dmp --json
```

---

## 📁 Cấu trúc Thư mục Dự án

```text
toolkit/
├── Dockerfile                   # Cấu hình container chuẩn production (bảo mật non-root)
├── docker-compose.yml           # File compose đa dịch vụ với volume mount file lớn
├── deploy.sh                    # Script triển khai tự động cho Linux/macOS/WSL
├── deploy.ps1                   # Script triển khai tự động cho Windows PowerShell
├── requirements.txt             # Danh sách dependencies
├── pyproject.toml               # Cấu hình dự án Python
├── src/
│   ├── main.py                  # Điểm khởi chạy trung tâm (CLI / Web / GUI)
│   ├── web.py                   # Máy chủ Web UI Dashboard bất đồng bộ (Zero-dependency)
│   ├── gui.py                   # Giao diện Desktop Native Tkinter đa luồng
│   ├── cli.py                   # Công cụ CLI hiệu năng cao kèm thanh đo tiến độ
│   ├── analyzers/
│   │   ├── dump_loader.py       # Nhận diện định dạng & Magic bytes (.mem, .raw, .dmp...)
│   │   ├── strings_scan.py      # Streaming Scanner $O(1)$ RAM & Trích xuất IOCs On-The-Fly
│   │   ├── process_scan.py      # Nhận diện dấu vết tiến trình & DLLs hệ thống
│   │   ├── pe_parser.py         # Phân tích PE Header, Section Entropy & Suspicious APIs
│   │   ├── llm_report_agent.py  # Trợ lý tạo báo cáo AI (Ollama, Gemini, OpenAI)
│   │   └── report_builder.py    # Bộ máy xuất báo cáo HTML, Markdown, JSON
│   ├── models/
│   │   └── dump_summary.py      # Cấu trúc dữ liệu giám định & Thuật toán chấm điểm rủi ro
│   └── utils/
│       ├── file_utils.py        # Đọc stream theo block, tính entropy phân tán đa khối
│       └── logger.py            # Hệ thống ghi log màu ANSI
├── samples/                     # File mẫu thử nghiệm & script benchmark
└── tests/                       # Bộ kiểm thử Unit Tests (12/12 passing)
```

---

## 🧪 Kiểm thử & Đo lường Hiệu năng (Benchmark)

Chạy bộ kiểm thử tiêu chuẩn:
```bash
python -m unittest discover tests -v
```

Chạy kịch bản Benchmark đo lường tốc độ I/O và mức tiêu thụ RAM đỉnh:
```bash
python samples/benchmark.py
```

---

## 📄 Giấy phép (License)

Dự án được phát hành theo giấy phép mã nguồn mở **MIT License**. Thiết kế phục vụ cộng đồng an toàn thông tin, nghiên cứu mã độc và các thí sinh tham gia các cuộc thi CTF.
