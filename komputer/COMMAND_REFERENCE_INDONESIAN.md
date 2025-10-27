# Referensi Lengkap Perintah Motor Board

## ⚠️ PENTING: Persyaratan Protokol Komunikasi

### 🔌 Komunikasi UART (Serial Port)

**PENGATURAN WAJIB:**
- **Baudrate:** 115200 bps (WAJIB)
- **Data Bits:** 8
- **Parity:** None (Tidak ada)
- **Stop Bits:** 1
- **Hardware Flow Control:** None (Tidak ada)

**Format Protokol:**
```
$perintah:parameter#
```
- **Delimiter awal:** `$`
- **Delimiter akhir:** `#`
- **Pemisah parameter:** `,`
- **Case insensitive:** Perintah bisa HURUF BESAR atau huruf kecil

**Koneksi:**
- Hubungkan via kabel USB Type-C ke PC
- Board akan muncul sebagai virtual COM port
- Gunakan software terminal serial (Arduino IDE Serial Monitor, PuTTY, minicom, dll.)

**Format Response:**
- Perintah konfigurasi mengembalikan: `command+OK`
- Perintah data mengembalikan format data spesifik (lihat setiap perintah)
- Tidak ada response berarti cek koneksi serial port

**Contoh Komunikasi:**
```
TX: $mtype:1#
RX: command+OK

TX: $spd:100,100,100,100#
(motor bergerak, tidak ada response)

TX: $read_vol#
RX: $Battery:11.50V#
```

---

### 🔗 Komunikasi I2C (Protokol IIC)

**PENGATURAN WAJIB:**
- **Alamat Device I2C:** 0x26 (alamat 7-bit)
- **Kecepatan Clock:** 100kHz (Standard) atau 400kHz (Fast mode)
- **Level Tegangan:** Kompatibel 3.3V atau 5V
- **Format Data:** Big-endian untuk nilai multi-byte

**Koneksi:**
- **SDA:** Line data (bidirectional dengan resistor pull-up)
- **SCL:** Line clock (dikontrol master dengan resistor pull-up)
- **GND:** Ground bersama (WAJIB)
- **VCC:** Suplai daya (3.3V atau 5V)

**Resistor Pull-up:**
- 4.7kΩ direkomendasikan untuk line SDA dan SCL
- Mungkin perlu penyesuaian berdasarkan kapasitansi bus dan kecepatan

**Catatan:** Lihat bagian Peta Register I2C di bawah untuk detail register lengkap

---

## 📋 Referensi Layout Motor

```
        DEPAN
    M1 -------- M3
     |          |
     |   ROBOT  |
     |          |
    M2 -------- M4
      BELAKANG
```

- **M1:** Motor kiri atas (roda depan kiri)
- **M2:** Motor kiri bawah (roda belakang kiri)
- **M3:** Motor kanan atas (roda depan kanan)
- **M4:** Motor kanan bawah (roda belakang kanan)

---

## 📡 Referensi Perintah UART

### 1. Konfigurasi Tipe Motor

```
$mtype:x#
```

**Parameter:**
- `x` = Tipe motor:
  - `1` = Motor 520 (dengan encoder)
  - `2` = Motor 310 (dengan encoder)
  - `3` = Motor TT (dengan encoder)
  - `4` = Motor TT (tanpa encoder)

**Contoh:**
```
$mtype:1#     → Motor 520
$mtype:4#     → Motor TT tanpa encoder
```

**Response:** `command+OK`

**Catatan:**
- **Default:** Motor 520 (tipe 1)
- **Tersimpan:** Ya (tetap tersimpan setelah mati)
- Jika encoder motor A→port A dan B→port B: gunakan motor 310
- Untuk motor tanpa encoder, HARUS gunakan tipe 4
- Untuk motor dengan encoder, pilih 1, 2, atau 3 berdasarkan spesifikasi motor

---

### 2. Konfigurasi Deadband Motor (Dead Zone)

```
$deadzone:xxxx#
```

**Parameter:**
- `xxxx` = Nilai dead zone (0-3600)

**Contoh:**
```
$deadzone:1650#    → Set deadzone ke 1650
$deadzone:1300#    → Set deadzone ke 1300
```

**Response:** `command+OK`

**Catatan:**
- **Default:** 1600
- **Tersimpan:** Ya (tetap tersimpan setelah mati)
- Dead zone menghilangkan osilasi motor pada PWM rendah
- Nilai harus diukur/disetel untuk motor spesifik Anda
- Ditambahkan otomatis ke perintah kontrol PWM

---

### 3. Konfigurasi Jalur Fase Motor

```
$mline:xx#
```

**Parameter:**
- `xx` = Jumlah jalur fase encoder per revolusi (1-99)

**Contoh:**
```
$mline:11#     → 11 jalur (motor 520)
$mline:13#     → 13 jalur (motor 310, motor TT)
```

**Response:** `command+OK`

**Catatan:**
- **Default:** 11
- **Tersimpan:** Ya (tetap tersimpan setelah mati)
- **KRITIKAL untuk kontrol kecepatan** - harus benar!
- Cek datasheet motor untuk nilai yang benar
- Hanya relevan untuk motor dengan encoder
- Diabaikan untuk motor tanpa encoder (tipe 4)

---

### 4. Konfigurasi Rasio Reduksi Motor

```
$mphase:xx#
```

**Parameter:**
- `xx` = Rasio reduksi (gear ratio)

**Contoh:**
```
$mphase:30#    → Rasio 30 (motor 520)
$mphase:40#    → Rasio 40 (L-type 520)
$mphase:45#    → Rasio 45 (motor TT)
```

**Response:** `command+OK`

**Catatan:**
- **Default:** 30
- **Tersimpan:** Ya (tetap tersimpan setelah mati)
- **KRITIKAL untuk kontrol kecepatan** - harus sesuai spesifikasi motor!
- Cek datasheet motor untuk nilai yang benar
- Hanya relevan untuk motor dengan encoder
- Diabaikan untuk motor tanpa encoder (tipe 4)

---

### 5. Konfigurasi Diameter Roda (Opsional)

```
$wdiameter:xx.xx#
```

**Parameter:**
- `xx.xx` = Diameter roda dalam milimeter (float)

**Contoh:**
```
$wdiameter:67.00#    → Roda 67mm
$wdiameter:48.00#    → Roda 48mm
$wdiameter:50#       → Roda 50mm (integer juga ok)
```

**Response:** `command+OK`

**Catatan:**
- **Default:** 67mm
- **Tersimpan:** Ya (tetap tersimpan setelah mati)
- Digunakan untuk kalkulasi kecepatan dalam mm/s
- Bisa diukur atau didapat dari spesifikasi roda
- Hanya mempengaruhi akurasi pelaporan kecepatan

---

### 6. Konfigurasi Parameter PID

```
$pid:motor,P,I,D#
```

**Parameter:**
- `motor` = Nomor motor (1-4)
- `P` = Proportional gain (float)
- `I` = Integral gain (float)
- `D` = Derivative gain (float)

**Contoh:**
```
$pid:1,0.5,0.1,0.05#    → Set PID M1
$pid:2,0.8,0.15,0.1#    → Set PID M2
```

**Response:** `command+OK`

**Catatan:**
- **Tersimpan:** Ya (tetap tersimpan setelah mati)
- Hanya untuk motor dengan encoder
- Memerlukan tuning untuk performa optimal
- P lebih tinggi = respons lebih cepat tapi bisa berosilasi
- I lebih tinggi = menghilangkan error steady-state
- D lebih tinggi = mengurangi overshoot

---

### 7. Reset ke Default Pabrik

```
$reset#
```

**Parameter:** Tidak ada

**Contoh:**
```
$reset#
```

**Response:** `command+OK`

**Catatan:**
- Me-reset SEMUA parameter ke default pabrik
- Gunakan ketika konfigurasi menjadi corrupt
- Memerlukan konfigurasi ulang setelah reset

---

### 8. Kontrol Kecepatan Motor (Closed-Loop)

```
$spd:M1,M2,M3,M4#
```

**Parameter:**
- `M1, M2, M3, M4` = Kecepatan dalam mm/s (-1000 sampai 1000)
- Nilai negatif = arah mundur
- Nol = berhenti

**Contoh:**
```
$spd:100,100,100,100#      → Semua maju pada 100mm/s
$spd:-100,-100,-100,-100#  → Semua mundur pada 100mm/s
$spd:100,-100,100,-100#    → Putar searah jarum jam
$spd:0,0,0,0#              → Berhenti semua motor
```

**Response:** Tidak ada (motor bergerak segera)

**Catatan:**
- **Range:** -1000 sampai 1000 mm/s
- **HANYA untuk motor DENGAN encoder** (tipe 1, 2, 3)
- Menggunakan kontrol PID untuk kecepatan akurat
- Kecepatan dipengaruhi oleh konfigurasi diameter roda
- Nilai tidak valid di luar range diabaikan

---

### 9. Kontrol PWM Langsung (Open-Loop)

```
$pwm:M1,M2,M3,M4#
```

**Parameter:**
- `M1, M2, M3, M4` = Nilai PWM (-3600 sampai 3600)
- Nilai negatif = arah mundur
- Nol = berhenti

**Contoh:**
```
$pwm:2000,2000,2000,2000#    → Semua maju PWM 2000
$pwm:-1500,-1500,-1500,-1500#→ Semua mundur PWM 1500
$pwm:0,0,0,0#                → Berhenti semua motor
```

**Response:** Tidak ada (motor bergerak segera)

**Catatan:**
- **Range:** -3600 sampai 3600
- Bekerja dengan SEMUA tipe motor (dengan atau tanpa encoder)
- **Direkomendasikan untuk motor TANPA encoder** (tipe 4)
- Tidak ada kontrol feedback - output PWM langsung
- Dead zone ditambahkan otomatis ke output
- Nilai tidak valid di luar range diabaikan

---

### 10. Laporan Data Encoder

```
$upload:A,B,C#
```

**Parameter:**
- `A` = Enable laporan total encoder (0 atau 1)
- `B` = Enable laporan encoder real-time (0 atau 1)
- `C` = Enable laporan kecepatan (0 atau 1)

**Hanya SATU yang bisa diaktifkan pada satu waktu**

**Contoh:**
```
$upload:1,0,0#    → Enable total encoder
$upload:0,1,0#    → Enable encoder real-time (10ms)
$upload:0,0,1#    → Enable kecepatan (mm/s)
$upload:0,0,0#    → Nonaktifkan semua laporan
```

**Response:** Stream data kontinu (lihat di bawah)

**Format Data:**

**Total Encoder:**
```
$MAll:M1,M2,M3,M4#
```
- Melaporkan hitungan encoder kumulatif sejak startup
- Contoh: `$MAll:1520,1503,-245,1498#`

**Encoder Real-Time (interval 10ms):**
```
$MTEP:M1,M2,M3,M4#
```
- Melaporkan hitungan encoder dalam 10ms terakhir
- Contoh: `$MTEP:5,5,-2,5#`

**Kecepatan Motor (mm/s):**
```
$MSPD:M1,M2,M3,M4#
```
- Melaporkan kecepatan aktual dalam mm/s
- Contoh: `$MSPD:99.8,100.2,100.1,99.9#`

**Catatan:**
- **HANYA untuk motor DENGAN encoder** (tipe 1, 2, 3)
- Data streaming kontinu ketika diaktifkan
- Nonaktifkan sebelum mengubah mode
- Beberapa laporan tidak bisa aktif bersamaan

---

### 11. Query Variabel Flash

```
$read_flash#
```

**Parameter:** Tidak ada

**Contoh:**
```
$read_flash#
```

**Response:** `command+OK` (diikuti dengan data konfigurasi)

**Catatan:**
- Membaca semua konfigurasi yang tersimpan dari flash memory
- Berguna untuk debugging masalah konfigurasi
- Format response bervariasi berdasarkan versi firmware

---

### 12. Cek Tegangan Baterai

```
$read_vol#
```

**Parameter:** Tidak ada

**Contoh:**
```
$read_vol#
```

**Response:**
```
$Battery:7.40V#
$Battery:11.85V#
$Battery:12.60V#
```

**Catatan:**
- Mengembalikan tegangan baterai aktual
- Format: `$Battery:XX.XXV#`
- Gunakan untuk peringatan baterai lemah
- Tegangan tergantung tipe baterai (1S, 2S, 3S LiPo, dll.)

---

## 🔗 Referensi Peta Register I2C

**Alamat Device I2C:** 0x26 (alamat 7-bit)

### Register Konfigurasi (Write Only / Tulis Saja)

| Register | Tipe     | Range       | Deskripsi                             |
|----------|----------|-------------|---------------------------------------|
| 0x01     | uint8_t  | 1-4         | Tipe motor (sama dengan UART $mtype)  |
| 0x02     | uint16_t | 0-3600      | Deadband motor                        |
| 0x03     | uint16_t | 0-65535     | Jalur fase motor                      |
| 0x04     | uint16_t | 0-65535     | Rasio reduksi motor                   |
| 0x05     | float    | -           | Diameter roda (mm), little-endian     |

### Register Kontrol (Write Only / Tulis Saja)

| Register | Tipe     | Range         | Deskripsi                                |
|----------|----------|---------------|------------------------------------------|
| 0x06     | int16_t  | -1000 s/d 1000| Kontrol kecepatan (mm/s) - 8 bytes total |
| 0x07     | int16_t  | -3600 s/d 3600| Kontrol PWM - 8 bytes total              |

**Format Register Kontrol (0x06 dan 0x07):**
- 8 bytes total: 2 bytes per motor (M1, M2, M3, M4)
- **Format big-endian**
- Contoh: M1=200, M2=-200, M3=0, M4=500
  ```
  [0x00 0xC8] [0xFF 0x38] [0x00 0x00] [0x01 0xF4]
  ```

### Register Status (Read Only / Baca Saja)

| Register | Tipe     | Deskripsi           | Kalkulasi                           |
|----------|----------|---------------------|-------------------------------------|
| 0x08     | uint16_t | Tegangan baterai    | voltage = (buf[0]<<8 \| buf[1])/10.0 |

### Register Encoder Real-Time (Read Only / Baca Saja)

| Register | Tipe    | Deskripsi                     | Kalkulasi                |
|----------|---------|-------------------------------|--------------------------|
| 0x10     | int16_t | M1 encoder real-time (10ms)   | data = buf[0]<<8\|buf[1] |
| 0x11     | int16_t | M2 encoder real-time (10ms)   | data = buf[0]<<8\|buf[1] |
| 0x12     | int16_t | M3 encoder real-time (10ms)   | data = buf[0]<<8\|buf[1] |
| 0x13     | int16_t | M4 encoder real-time (10ms)   | data = buf[0]<<8\|buf[1] |

### Register Total Encoder (Read Only / Baca Saja)

| Register | Tipe    | Deskripsi                          | Catatan                            |
|----------|---------|------------------------------------|------------------------------------|
| 0x20     | int16_t | M1 total encoder (16 bit tinggi)   | Gunakan 0x20 dan 0x21 bersamaan    |
| 0x21     | int16_t | M1 total encoder (16 bit rendah)   | Lihat kalkulasi di bawah           |
| 0x22     | int16_t | M2 total encoder (16 bit tinggi)   | Gunakan 0x22 dan 0x23 bersamaan    |
| 0x23     | int16_t | M2 total encoder (16 bit rendah)   | Sama dengan M1                     |
| 0x24     | int16_t | M3 total encoder (16 bit tinggi)   | Gunakan 0x24 dan 0x25 bersamaan    |
| 0x25     | int16_t | M3 total encoder (16 bit rendah)   | Sama dengan M1                     |
| 0x26     | int16_t | M4 total encoder (16 bit tinggi)   | Gunakan 0x26 dan 0x27 bersamaan    |
| 0x27     | int16_t | M4 total encoder (16 bit rendah)   | Sama dengan M1                     |

**Kalkulasi Total Encoder:**
```python
# Baca register High dan Low
high_data = i2c_read(0x20, 2)  # Mengembalikan [buf[0], buf[1]]
low_data = i2c_read(0x21, 2)   # Mengembalikan [bf[0], bf[1]]

# Kalkulasi total 32-bit
total = (high_data[0]<<24) | (high_data[1]<<16) | (low_data[0]<<8) | low_data[1]
```

---

## 📊 Konfigurasi Motor Preset

### Tipe 1: Motor 520 (Ber-encoder)
```
UART:
$mtype:1#
$mphase:30#
$mline:11#
$wdiameter:67.00#
$deadzone:1600#

I2C:
0x01 = 1
0x04 = 30
0x03 = 11
0x05 = 67.0 (float)
0x02 = 1600
```

### Tipe 2: Motor 310 (Ber-encoder)
```
UART:
$mtype:2#
$mphase:20#
$mline:13#
$wdiameter:48.00#
$deadzone:1300#

I2C:
0x01 = 2
0x04 = 20
0x03 = 13
0x05 = 48.0 (float)
0x02 = 1300
```

### Tipe 3: Motor TT dengan Encoder
```
UART:
$mtype:3#
$mphase:45#
$mline:13#
$wdiameter:68.00#
$deadzone:1250#

I2C:
0x01 = 3
0x04 = 45
0x03 = 13
0x05 = 68.0 (float)
0x02 = 1250
```

### Tipe 4: Motor TT tanpa Encoder
```
UART:
$mtype:4#
$deadzone:1000#
(Parameter lain tidak diperlukan)

I2C:
0x01 = 4
0x02 = 1000
```

---

## 🔄 Alur Kerja Tipikal

### Setup UART Pertama Kali:
```bash
# 1. Hubungkan ke serial port pada 115200 baud
# 2. Konfigurasi tipe motor dan parameter
$mtype:1#
$mphase:30#
$mline:11#
$wdiameter:67.00#
$deadzone:1600#

# 3. Test motor (opsional)
$pwm:1000,0,0,0#    # Test M1 saja
$pwm:0,0,0,0#       # Stop

# 4. Enable laporan kecepatan
$upload:0,0,1#

# 5. Kontrol motor
$spd:100,100,100,100#
```

### Setup I2C Pertama Kali:
```python
# 1. Konfigurasi tipe motor dan parameter
i2c_write(0x26, 0x01, [1])          # Tipe motor
i2c_write(0x26, 0x04, [0x00, 0x1E])  # Rasio reduksi (30)
i2c_write(0x26, 0x03, [0x00, 0x0B])  # Jalur fase (11)
# ... dll

# 2. Kontrol motor
speed_data = [0x00, 0x64, 0x00, 0x64, 0x00, 0x64, 0x00, 0x64]
i2c_write(0x26, 0x06, speed_data)  # Kontrol kecepatan

# 3. Baca feedback
voltage = i2c_read(0x26, 0x08, 2)
encoder = i2c_read(0x26, 0x10, 2)
```

---

## ⚡ Referensi Perintah Cepat

### Stop Darurat:
```
UART: $pwm:0,0,0,0#
I2C:  Tulis [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00] ke 0x06 atau 0x07
```

### Maju (Semua Motor):
```
UART: $spd:100,100,100,100#
I2C:  Tulis [0x00,0x64,0x00,0x64,0x00,0x64,0x00,0x64] ke 0x06
```

### Mundur (Semua Motor):
```
UART: $spd:-100,-100,-100,-100#
I2C:  Tulis [0xFF,0x9C,0xFF,0x9C,0xFF,0x9C,0xFF,0x9C] ke 0x06
```

### Putar Searah Jarum Jam:
```
UART: $spd:100,-100,100,-100#
I2C:  Tulis [0x00,0x64,0xFF,0x9C,0x00,0x64,0xFF,0x9C] ke 0x06
```

### Putar Berlawanan Jarum Jam:
```
UART: $spd:-100,100,-100,100#
I2C:  Tulis [0xFF,0x9C,0x00,0x64,0xFF,0x9C,0x00,0x64] ke 0x06
```

---

## ⚠️ Catatan Penting

### Umum:
1. **Persistensi konfigurasi:** Semua config tersimpan di flash memory (non-volatile)
2. **Setup sekali jalan:** Konfigurasi sekali, pengaturan tetap setelah mati
3. **Kebutuhan encoder:** Kontrol kecepatan dan data encoder hanya untuk motor DENGAN encoder
4. **Mode upload tunggal:** Hanya satu mode laporan encoder yang bisa aktif pada satu waktu

### Spesifik UART:
5. **Format perintah:** Selalu gunakan format `$perintah:params#`
6. **Pengecekan response:** Cari `command+OK` untuk perintah konfigurasi
7. **Tidak ada echo:** Board tidak meng-echo perintah yang dikirim
8. **Line ending:** Gunakan `#` sebagai terminator, tidak perlu CR/LF

### Spesifik I2C:
9. **Endianness:** Register kontrol gunakan **big-endian**, float gunakan **little-endian**
10. **Penulisan multi-byte:** Kontrol kecepatan/PWM memerlukan 8 bytes (2 per motor)
11. **Pembacaan 32-bit:** Total encoder memerlukan pembacaan 2 register terpisah
12. **Resistor pull-up:** Diperlukan pada line SDA dan SCL (4.7kΩ direkomendasikan)

### Keamanan:
13. **Test dengan aman:** Selalu test dengan beban ringan atau tanpa beban terlebih dahulu
14. **Monitor baterai:** Cek tegangan secara teratur untuk mencegah over-discharge
15. **Stop darurat:** Siapkan perintah `$pwm:0,0,0,0#`
16. **Pemasangan kabel yang benar:** Cek polaritas motor sebelum menyalakan daya

---

## 🔍 Troubleshooting

### Masalah UART:
- **Tidak ada response:** Cek baudrate (harus 115200), cek kabel USB
- **Data kacau:** Verifikasi pengaturan serial port (8N1, no flow control)
- **Perintah diabaikan:** Cek format (`$perintah#`), cek case sensitivity
- **Motor tidak bergerak:** Cek suplai daya, cek koneksi motor

### Masalah I2C:
- **Tidak ada ACK:** Cek alamat I2C (0x26), cek resistor pull-up
- **Bus hang:** Cek koneksi SDA/SCL, cek level tegangan
- **Data salah:** Cek endianness (big-endian untuk kontrol, little-endian untuk float)
- **Response lambat:** Kurangi kecepatan clock I2C ke 100kHz

### Masalah Motor:
- **Motor berosilasi:** Tingkatkan nilai deadband
- **Kecepatan salah:** Cek pengaturan mphase, mline, wdiameter
- **Error encoder:** Verifikasi koneksi encoder (A→A, B→B)
- **Tidak ada gerakan:** Cek pengaturan tipe motor, coba kontrol PWM terlebih dahulu

---

**Versi Dokumen:** 3.0 (Referensi Lengkap UART + I2C)  
**Platform:** Universal (Windows/Linux/Mac/Embedded)  
**Kompatibel dengan:** Python GUI v2.0+  
**Board:** Yahboom 4-Channel Encoder Motor Drive Module  
**MCU:** STM32F103RCT6  
**Terakhir Diperbarui:** 2025
