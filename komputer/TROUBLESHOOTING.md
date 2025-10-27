# Troubleshooting Guide - Motor Board GUI

## 🔧 Panduan Mengatasi Masalah

### 📍 KATEGORI MASALAH

1. [Koneksi Serial](#1-masalah-koneksi-serial)
2. [Motor Tidak Bergerak](#2-motor-tidak-bergerak)
3. [Data Tidak Muncul](#3-data-tidak-muncul)
4. [Kecepatan Tidak Akurat](#4-kecepatan-tidak-akurat)
5. [PID/Kontrol Tidak Stabil](#5-pid-kontrol-tidak-stabil)
6. [Error Messages](#6-error-messages)
7. [Performance Issues](#7-performance-issues)

---

## 1. Masalah Koneksi Serial

### ❌ Port Tidak Muncul di Dropdown

**Gejala:**
- Dropdown port kosong atau tidak ada pilihan
- Board sudah terhubung ke USB

**Penyebab & Solusi:**

#### A. Driver Belum Terinstall
**Windows:**
```
1. Buka Device Manager (Win+X → Device Manager)
2. Cek apakah ada "Unknown Device" atau tanda seru kuning
3. Download driver CH340 atau CP2102:
   - CH340: http://www.wch.cn/downloads/CH341SER_ZIP.html
   - CP2102: https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers
4. Install driver
5. Restart komputer
6. Klik "Refresh Ports" di GUI
```

**Linux:**
```bash
# Cek apakah device terdeteksi
lsusb
dmesg | grep tty

# Install driver (biasanya sudah built-in)
sudo apt-get install brltty
sudo apt-get remove brltty  # Jika conflict

# Tambahkan user ke group dialout
sudo usermod -a -G dialout $USER
# Logout dan login lagi

# Berikan permission
sudo chmod 666 /dev/ttyUSB0
```

**Mac:**
```bash
# Cek device
ls /dev/cu.*

# Install driver jika perlu (untuk CH340)
# Download dari: https://github.com/adrianmihalko/ch340g-ch34g-ch34x-mac-os-x-driver
```

#### B. Port Digunakan Program Lain
```
- Tutup Arduino IDE
- Tutup PuTTY / Terminal
- Tutup aplikasi serial monitor lain
- Unplug dan plug ulang USB
- Klik "Refresh Ports"
```

#### C. Kabel USB Rusak/Charging-Only
```
Coba:
1. Ganti kabel USB (pastikan bukan kabel charging-only)
2. Test dengan kabel data yang pasti bagus
3. Coba port USB berbeda di komputer
```

---

### ❌ Connection Failed / Timeout

**Gejala:**
- Error: "Failed to connect: [Error message]"
- Timeout saat connect

**Solusi:**

#### A. Port Sudah Terbuka
```python
# Windows: Task Manager → Details → cari python.exe
# Kill process yang pakai port

# Linux/Mac:
lsof | grep ttyUSB0
# Atau
sudo fuser -k /dev/ttyUSB0
```

#### B. Baudrate Tidak Match
```
1. Coba baudrate berbeda: 9600, 57600, 115200
2. Cek dokumentasi board untuk baudrate default
3. Biasanya: 115200 baud
```

#### C. Board Tidak Responding
```
1. Reset board (tekan reset button)
2. Unplug USB, tunggu 5 detik, plug lagi
3. Cek LED indikator di board (harus nyala)
4. Cek power supply board
```

---

## 2. Motor Tidak Bergerak

### ❌ Motor Diam Saat Diberi Command

**Penyebab & Solusi:**

#### A. Nilai Dalam Dead Zone
```
Gejala: Motor tidak bergerak dengan nilai kecil (< 500)

Solusi:
1. Tab Configuration → Configure Motor Deadband
2. Coba nilai deadzone lebih rendah (1000-1200)
3. Atau naikkan nilai speed/PWM di atas deadzone
   - Contoh: jika deadzone=1600, coba speed > 200
```

#### B. Konfigurasi Belum Di-Apply
```
Checklist:
☐ Motor type sudah di-set?
☐ Deadzone sudah di-set?
☐ Configuration sudah di-apply?
☐ Board sudah di-restart setelah config?

Cara fix:
1. Tab Configuration
2. Pilih motor type
3. Klik "Apply Preset Configuration"
4. Tunggu 1 detik
5. Test lagi
```

#### C. Wiring Salah atau Loose
```
Cek:
1. Kabel motor ke board:
   - M1+ M1- ke terminal M1
   - M2+ M2- ke terminal M2
   - dst...
2. Power supply:
   - VCC dan GND terhubung
   - Tegangan cukup (cek battery level)
3. Kencangkan semua terminal screw
```

#### D. Power Supply Tidak Cukup
```
Gejala: Motor bergerak sebentar lalu mati

Solusi:
1. Cek battery level: Tab Monitor → Check Battery Level
2. Minimum voltage: 7.4V untuk board ini
3. Gunakan power supply yang cukup:
   - 4 motor @ 2A = min 8A total
   - Recommended: 12V 10A
```

#### E. Motor Rusak
```
Test:
1. Test motor satu per satu
2. Swap motor yang rusak dengan yang baik
3. Test dengan PWM langsung (bukan speed control)
   $pwm:2000,0,0,0#
4. Jika tetap tidak gerak → motor/encoder rusak
```

---

### ❌ Motor Bergerak Terbalik

**Gejala:**
- Command maju, motor mundur
- Command positif, motor putar kiri (seharusnya kanan)

**Solusi:**

#### A. Swap Wiring Motor
```
Tukar polaritas motor:
M+ ↔ M-

Atau di software (lebih mudah):
- Jika command 100 → motor mundur
- Kirim command -100 → motor maju
- Update code Anda untuk invert nilai
```

#### B. Encoder Wiring Terbalik
```
Jika speed reporting terbalik:
1. Swap encoder A dan B channel
2. Atau update phase lines configuration
```

---

## 3. Data Tidak Muncul

### ❌ Tidak Ada Data di Log Monitor

**Solusi:**

#### A. Upload Mode Belum Di-Enable
```
Checklist:
1. Tab Connection → Upload Data Mode
2. Pilih mode yang diinginkan (1, 2, atau 3)
3. Klik "Apply Upload Mode"
4. Data akan mulai streaming

Catatan: Mode 0 = no data upload
```

#### B. Motor Tanpa Encoder
```
Jika motor type = 4 (TT DC Reduction):
- Tidak ada encoder
- Tidak bisa report encoder data
- Hanya bisa kirim command PWM
- Tidak ada feedback

Solusi: Gunakan motor dengan encoder (type 1,2,3,5)
```

#### C. Baudrate Mismatch
```
Gejala: Connected tapi data aneh/corrupted

Solusi:
1. Disconnect
2. Ganti baudrate (coba 115200)
3. Connect lagi
4. Re-apply upload mode
```

---

## 4. Kecepatan Tidak Akurat

### ❌ Speed Reporting Salah

**Penyebab & Solusi:**

#### A. Parameter Konfigurasi Salah
```
Cek parameter ini di Tab Configuration:

1. Phase Lines (Magnetic Ring)
   - Harus sesuai spec motor
   - 520 motor = 11 lines
   - 310 motor = 13 lines
   - Cek manual motor!

2. Reduction Ratio (mphase)
   - Harus sesuai gear ratio
   - 520 motor = 30:1
   - Salah ratio → speed salah

3. Wheel Diameter
   - Ukur diameter roda yang sebenarnya
   - Dalam milimeter
   - Pengaruh besar ke speed calculation

Formula:
Speed (mm/s) = (Encoder pulses × Wheel circumference) / (Lines × Ratio × Time)
```

#### B. Encoder Noise
```
Gejala: Speed jumping / unstable

Solusi:
1. Cek kabel encoder tidak terlalu panjang
2. Gunakan shielded cable
3. Ground yang baik
4. Jauhkan dari kabel power motor
```

---

## 5. PID Kontrol Tidak Stabil

### ❌ Motor Oscillating / Overshooting

**Gejala:**
- Motor tidak stabil di target speed
- Bergetar / berosilasi
- Overshoot lalu undershoot

**Solusi - PID Tuning:**

#### Step-by-Step Tuning:

```
1. Mulai dari NOL:
   P = 0, I = 0, D = 0

2. Tune P (Proportional):
   - Set P = 0.1
   - Test, naikkan P bertahap (0.2, 0.3, 0.5, ...)
   - Stop saat motor responsif TAPI masih stabil
   - Jika mulai oscillating → turunkan P sedikit
   - Target: Motor respond cepat, steady-state error masih ada

3. Tune I (Integral):
   - Set I = 0.01
   - Test, naikkan I bertahap
   - Stop saat steady-state error hilang
   - Jika oscillating → turunkan I
   - Target: Motor mencapai exact target speed

4. Tune D (Derivative):
   - Set D = 0.001
   - Test, naikkan D bertahap
   - Stop saat overshoot minimal
   - D untuk damping/smoothing
   - Target: No overshoot, smooth response

5. Fine-tuning:
   - Adjust ketiga parameter untuk balance
   - Test dengan berbagai speed
   - Test dengan load (robot bergerak)
```

#### Contoh Values:
```
Starting point (520 motor):
P = 0.5
I = 0.1
D = 0.05

If too aggressive:
P = 0.3
I = 0.05
D = 0.02

If too sluggish:
P = 0.8
I = 0.15
D = 0.08
```

---

## 6. Error Messages

### Common Errors:

#### "Not connected to serial port"
```
Solusi: Klik Connect dulu di tab Connection
```

#### "Failed to connect: [WinError 5] Access denied"
```
Solusi: Port digunakan program lain, tutup program tersebut
```

#### "Failed to connect: could not open port"
```
Solusi: 
1. Unplug dan plug USB
2. Cek driver
3. Coba port USB berbeda
```

#### GUI Freeze / Not Responding
```
Solusi:
1. Tutup GUI (force close jika perlu)
2. Unplug board
3. Restart GUI
4. Plug board
5. Connect lagi

Pencegahan:
- Jangan spam button terlalu cepat
- Tunggu response dari board
```

---

## 7. Performance Issues

### ❌ GUI Slow / Laggy

**Solusi:**

#### A. Too Much Data Logging
```
1. Disable upload mode saat tidak perlu
   $upload:0,0,0#
2. Clear log berkala (klik Clear Log)
3. Jangan biarkan log > 1000 lines
```

#### B. Komputer Lambat
```
1. Tutup program lain
2. Update Python ke versi terbaru
3. Reinstall pyserial
```

---

## 🆘 Emergency Procedures

### 🚨 Motor Ngamuk / Out of Control

```
1. DISCONNECT USB SECEPATNYA
   atau
2. KLIK STOP ALL MOTORS
   atau
3. MATIKAN POWER SUPPLY

Jangan panik, safety first!
```

### 🔥 Motor Overheat

```
1. Stop semua motor immediately
2. Biarkan dingin 5-10 menit
3. Cek:
   - Overload? (terlalu berat)
   - Stall? (motor mentok)
   - PWM terlalu tinggi terlalu lama
4. Kurangi load atau PWM
```

---

## 📝 Checklist Sebelum Lapor Bug

Jika semua troubleshooting di atas sudah dicoba dan masih error:

```
☐ Versi Python? (python --version)
☐ Versi pyserial? (pip show pyserial)
☐ OS? (Windows/Linux/Mac + version)
☐ Board type dan versi firmware?
☐ Motor type yang digunakan?
☐ Sudah coba dengan setting default?
☐ Error message lengkap (screenshot)?
☐ Log data (copy dari monitor)?
☐ Langkah-langkah reproduksi error?
```

Sertakan info di atas saat lapor bug untuk solusi lebih cepat!

---

## 💡 Tips Debugging

### Enable Debug Mode:
```python
# Tambahkan di awal motor_board_gui_full.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Test Serial Manual:
```python
import serial
ser = serial.Serial('COM3', 115200, timeout=1)
ser.write(b'$battery#')
print(ser.read(100))
ser.close()
```

### Test dengan Serial Monitor Lain:
```
- PuTTY (Windows)
- screen (Linux/Mac)
- Arduino Serial Monitor
- CoolTerm

Test command manual untuk isolate masalah GUI vs Board
```

---

**Good Luck & Happy Debugging! 🚀**

Jika masih stuck, jangan ragu untuk ask for help!
