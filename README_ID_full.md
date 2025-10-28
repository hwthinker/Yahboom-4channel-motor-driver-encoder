# Selamat Datang di Repositori Modul Penggerak Motor 4-Channel

## 1.1 Pengantar Papan Penggerak Motor 4-Channel

![image-20251028052746916](./assets/image-20251028052746916.png)

### Pengantar Produk

Modul driver motor 4-channel dengan encoder ini mengintegrasikan koprosesor single-chip berperforma tinggi, dan dapat terhubung tanpa hambatan ke berbagai kontroler seperti **MSPM0, STM32, Raspberry Pi,** dan **Jetson** melalui komunikasi **serial (USART)** atau **I2C**. Tujuannya adalah menyederhanakan proses penggerakan motor.

Hanya dengan **empat kabel** penghubung, modul dapat berkomunikasi efisien dengan unit kendali utama (MCU) untuk **mengontrol motor** dan **membaca data encoder**, sehingga **mengurangi jumlah kabel** dan **menyederhanakan operasi**.

Modul mendukung mayoritas motor DC reduction populer di pasaran seperti **TT dengan Hall encoder**, **520**, **310**, dan kompatibelnya.

### Tabel Parameter
| Spesifikasi Teknis                 | Parameter                     |
| :--------------------------------- | :---------------------------: |
| Rekomendasi Tegangan Masuk         | 5–12V                         |
| Arus DC pin 5V                     | 0.7A                          |
| Arus DC pin 3.3V                   | 500mA                         |
| Arus drive kontinu per motor       | Default 4A (maks. 5.5A)       |
| Dimensi (P × L × T)                | 56 × 65 × 13.4 mm             |
| Antarmuka motor encoder            | PH2.0-6PIN, socket kabel Dupont |
| Antarmuka motor DC                 | XH2.54-2PIN                   |

## Pemetaan 4 Antarmuka Motor pada Modul ke Roda Robot
- **M1** → Motor kiri atas (roda kiri depan)  
- **M2** → Motor kiri bawah (roda kiri belakang)  
- **M3** → Motor kanan atas (roda kanan depan)  
- **M4** → Motor kanan bawah (roda kanan belakang)

## Konfigurasi Serial
**Baud rate 115200, no parity, tanpa hardware flow control, 1 stop bit.**

---

## 1. Konfigurasi Tipe Motor
| Perintah    | Penjelasan    | Contoh       | Keterangan                                     | Bawaan Firmware | Tersimpan saat mati |
| :---------: | :-----------: | :----------: | :--------------------------------------------: | :--------------: | :-----------------: |
| `$mtype:x#` | Model motor   | `$mtype:1#`  | Model motor adalah 520 motor                   | 520 motor        | Y                   |

**Catatan:**
1. Pilih tipe motor sesuai **arah koneksi fase encoder** (A ke A dan B ke B). Jika encoder motor **A ke A, B ke B**, pilih model **310**; selain itu pilih **520** atau **TT** sesuai jenisnya.  
2. Perintah tidak peka huruf besar/kecil.  
3. Jika sukses, modul mengirim balasan **`command+OK`**. Jika tidak ada balasan, periksa koneksi serial.  
4. Nilai `x`:
   - `1` = 520 motor  
   - `2` = 310 motor  
   - `3` = TT motor (dengan encoder)  
   - `4` = TT motor (tanpa encoder)

Untuk motor tanpa encoder gunakan `4` → `$mtype:4#`. Untuk motor ber-encoder gunakan salah satu dari `1/2/3`.

## 2. Konfigurasi Deadband Motor (PWM Deadzone)
| Perintah           | Penjelasan                                   | Contoh              | Keterangan                                                                 | Bawaan | Simpan saat mati |
| :----------------: | :------------------------------------------: | :-----------------: | :------------------------------------------------------------------------: | :----: | :--------------: |
| `$deadzone:xxxx#`  | Set dead zone pulsa PWM                      | `$deadzone:1650#`   | Saat kontrol PWM, nilai dead zone ditambahkan agar menghindari osilasi     | 1600   | Y                |

**Catatan:**
1. Tidak peka huruf besar/kecil.  
2. Jika sukses, akan ada balasan **`command+OK`**; jika tidak ada, periksa koneksi serial.  
3. `xxxx` diukur secara eksperimen untuk meminimalkan getaran minimum.  
4. Rentang nilai: **0–3600**.

## 3. Konfigurasi Jumlah Garis Fase Encoder (Magnetic Ring Lines)
| Perintah     | Penjelasan                                | Contoh        | Keterangan                                             | Bawaan | Simpan saat mati |
| :----------: | :---------------------------------------: | :-----------: | :----------------------------------------------------: | :----: | :--------------: |
| `$mline:xx#` | Jumlah garis fase Hall encoder per putaran| `$mline:13#`  | Jumlah garis fase encoder Hall                         | 11     | Y                |

**Catatan:**
1. Tidak peka huruf besar/kecil.  
2. Jika sukses, balasan **`command+OK`**.  
3. `xx` = jumlah garis magnetik per putaran (lihat datasheet motor).  
4. **Motor ber-encoder:** parameter ini **krusial** untuk kontrol kecepatan.  
5. **Motor tanpa encoder:** dapat diabaikan.

## 4. Konfigurasi Rasio Reduksi (Gear Reduction Ratio)
| Perintah       | Penjelasan                  | Contoh        | Keterangan                           | Bawaan | Simpan saat mati |
| :------------: | :-------------------------: | :-----------: | :----------------------------------: | :----: | :--------------: |
| `$mphase:xx#`  | Set rasio reduksi motor     | `$mphase:40#` | Set rasio reduksi motor menjadi 40   | 30     | Y                |

**Catatan:** sama seperti bagian sebelumnya; **wajib akurat** untuk motor ber-encoder.

## 5. Konfigurasi Diameter Roda (Opsional)
| Perintah            | Penjelasan                    | Contoh            | Keterangan                             | Bawaan | Simpan saat mati |
| :-----------------: | :---------------------------: | :---------------: | :------------------------------------: | :----: | :--------------: |
| `$wdiameter:xx#`    | Set diameter roda (mm)        | `$wdiameter:50#`  | Diameter roda 50 mm                    | 67 mm  | Y                |

**Catatan:**
- sama seperti bagian sebelumnya
- Untuk motor ber-encoder: memengaruhi **akurasi data kecepatan** (mm/s), tidak memengaruhi **data encoder** mentah.  
- Untuk motor tanpa encoder: dapat diabaikan.

## 6. Konfigurasi Parameter PID Kontrol Motor
| Perintah               | Penjelasan                 | Contoh                   | Keterangan                                  | Bawaan (P/I/D) | Simpan |
| :--------------------: | :------------------------: | :----------------------: | :-----------------------------------------: | :------------: | :----: |
| `$MPID:x.xx,x.xx,x.xx#`| Set parameter PID (P,I,D) | `$MPID:1.5,0.03,0.1#`    | Setelah ubah nilai, chip akan **restart**   | 0.8/0.06/0.5   | Y      |

**Catatan:** Umumnya **tidak perlu** diubah; gunakan nilai default kecuali perlu tuning.

## 7. Reset ke Pengaturan Pabrik
| Perintah         | Penjelasan                    | Contoh | Keterangan | Bawaan | Simpan |
| :--------------: | :---------------------------: | :----: | :--------: | :----: | :----: |
| `$flash_reset#`  | Kembalikan ke default pabrik |   -    |  Modul akan **restart** sekali |  - | - |

## 8. Perintah Kontrol Kecepatan (Encoder Wajib)
| Perintah         | Penjelasan                   | Contoh                 | Keterangan                                                    | Simpan |
| :--------------: | :--------------------------: | :--------------------: | :-----------------------------------------------------------: | :----: |
| `$spd:0,0,0,0#`  | Kontrol kecepatan 4 motor    | `$spd:100,-100,0,50#`  | Range **-1000 sampai 1000**, urutan **M1,M2,M3,M4**          | N      |

**Catatan:** Saat parameter `0`, PID tetap aktif → roda sulit diputar manual. Gunakan `pwm`=0 jika ingin bebas.

## 9. Perintah Kontrol PWM Langsung
| Perintah         | Penjelasan                     | Contoh                    | Keterangan                                                                    | Simpan |
| :--------------: | :----------------------------: | :-----------------------: | :----------------------------------------------------------------------------: | :----: |
| `$pwm:0,0,0,0#`  | Kontrol PWM 4 motor            | `$pwm:0,-520,300,800#`    | Range **-3600 sampai 3600**, cocok **motor tanpa encoder**                    | N      |

## 10. Laporan Data Encoder *(hanya motor ber-encoder)*
| Perintah          | Penjelasan                     | Contoh             | Keterangan                                                                    | Simpan |
| :---------------: | :----------------------------: | :----------------: | :----------------------------------------------------------------------------: | :----: |
| `$upload:0,0,0#`  | Mengatur data encoder yang diterima | `$upload:1,0,0#` | 1: total pulse, 2: real-time 10ms, 3: kecepatan roda                         | N      |

**Format data keluaran:**
- Total encoder roda: `"$MAll:M1,M2,M3,M4#"`  
- Encoder real-time 10ms: `"$MTEP:M1,M2,M3,M4#"`  
- Kecepatan roda: `"$MSPD:M1,M2,M3,M4#"`

## 11. Query Variabel Flash
| Perintah          | Penjelasan                  | Contoh | Keterangan                | Simpan |
| :---------------: | :-------------------------: | :----: | :-----------------------: | :----: |
| `$read_flash#`    | Tampilkan variabel di flash |   -    | Balasan **`command+OK`**  | N      |

## 12. Cek Tegangan Baterai
| Perintah        | Penjelasan             | Contoh | Keterangan                                      | Simpan |
| :-------------: | :--------------------: | :----: | :---------------------------------------------: | :----: |
| `$read_vol#`    | Membaca level baterai  |   -    | Contoh balasan: **`$Battery:7.40V#`**           | N      |

---

# Kontrol Melalui I2C (IIC)

**Alamat device I2C driver 4-channel:** `0x26`

| Alamat Reg | R/W | Tipe      | Rentang / Nilai                         | Penjelasan                                                                            | Contoh Penulisan Data |
| :--------: | :-: | :-------: | :-------------------------------------- | :------------------------------------------------------------------------------------ | :-------------------- |
| `0x01`     |  W  | `uint8_t` | 1:520, 2:310, 3:TT encoder, 4:TT no enc | Tulis tipe motor                                                                      | Device addr + reg + tipe |
| `0x02`     |  W  | `uint16_t`| 0–3600                                  | Set PWM deadzone                                                                      | Device addr + reg + nilai |
| `0x03`     |  W  | `uint16_t`| 0–65535                                 | Set jumlah garis magnetik encoder                                                     | Device addr + reg + nilai |
| `0x04`     |  W  | `uint16_t`| 0–65535                                 | Set rasio reduksi                                                                     | Device addr + reg + nilai |
| `0x05`     |  W  | `float`   | —                                       | Set diameter roda (mm), **little-endian** saat konversi byte                          | Device addr + reg + diameter |
| `0x06`     |  W  | `int16_t` | -1000~1000                              | Kontrol **kecepatan** (hanya motor ber-encoder), **big-endian**, 4 motor × 2 byte     | Contoh: `[0x00 0xC8 0xFF 0x38 0x00 0x00 0x01 0xF4]` utk 200,-200,0,500 |
| `0x07`     |  W  | `int16_t` | -3600~3600                              | Kontrol **PWM** (motor tanpa encoder/umum), **big-endian**, 4 motor × 2 byte          | Contoh serupa register 0x06 |
| `0x08`     |  R  | `uint16_t`| —                                       | Baca level baterai → `data = (buf[0]<<8 \| buf[1]) / 10.0`                            | — |
| `0x10`     |  R  | `int16_t` | —                                       | Baca data pulse encoder M1 real-time (10ms) → `data = buf[0]<<8 \| buf[1]`            | — |
| `0x11`     |  R  | `int16_t` | —                                       | Baca data pulse encoder M2 real-time (10ms)                                           | — |
| `0x12`     |  R  | `int16_t` | —                                       | Baca data pulse encoder M3 real-time (10ms)                                           | — |
| `0x13`     |  R  | `int16_t` | —                                       | Baca data pulse encoder M4 real-time (10ms)                                           | — |
| `0x20`     |  R  | `int16_t` | —                                       | Baca **total** pulse encoder M1 (High)                                                | — |
| `0x21`     |  R  | `int16_t` | —                                       | Baca **total** pulse encoder M1 (Low)  → gabung `buf` high/low: `data = buf[0]<<24 \| buf[1]<<16 \| bf[0]<<8 \| bf[1]` | — |
| `0x22`     |  R  | `int16_t` | —                                       | Baca **total** pulse encoder M2 (High)                                                | — |
| `0x23`     |  R  | `int16_t` | —                                       | Baca **total** pulse encoder M2 (Low)                                                 | — |
| `0x24`     |  R  | `int16_t` | —                                       | Baca **total** pulse encoder M3 (High)                                                | — |
| `0x25`     |  R  | `int16_t` | —                                       | Baca **total** pulse encoder M3 (Low)                                                 | — |
| `0x26`     |  R  | `int16_t` | —                                       | Baca **total** pulse encoder M4 (High)                                                | — |
| `0x27`     |  R  | `int16_t` | —                                       | Baca **total** pulse encoder M4 (Low)                                                 | — |

---

# Cara Memperbarui Firmware

1. Buka perangkat lunak **FlyMcu** (tersedia pada lampiran).  
2. Hubungkan port **Type‑C** papan driver motor 4-channel ke komputer.  
3. Klik **Enumport** pada FlyMcu dan pilih **port serial** papan driver Anda.  
4. Pada kolom **Program file**, pilih file firmware yang telah diunduh.  
5. Pastikan pengaturan lain (pada kotak merah di dokumentasi) **sesuai**.  
6. Klik **Start Programming** untuk memulai proses burning firmware.  
7. Setelah sukses, cabut dan pasang kembali kabel Type‑C untuk **restart** papan.  
8. Indikator sukses: **lampu merah selalu ON** dan **lampu hijau berkedip dua kali setiap 3 detik**.

(Gambar/ilustrasi mengikuti berkas asli di folder `assets/`.)

---

**Catatan Umum:**  
- Perintah serial **case-insensitive** (boleh huruf besar/kecil).  
- Jika tidak ada balasan setelah mengirim perintah konfigurasi, **periksa koneksi** dan parameter serial.  
- Untuk tuning PID, lakukan **bertahap** dan catat nilai yang stabil.  
- Untuk motor tanpa encoder, gunakan kontrol **PWM** secara langsung.  
- Diameter roda memengaruhi **konversi** kecepatan (mm/s), bukan **pulses** encoder.



---

# Pengantar Motor dan Penggunaan

**Bagian ini menjelaskan parameter motor, rekomendasi tegangan suplai, serta metode wiring yang disarankan untuk koneksi ke papan driver motor 4-channel.**

Tautan referensi asli (dipertahankan):
- [Motor introduction and usage](https://www.yahboom.net/public/upload/upload-html/1740571311/0.%20Motor%20introduction%20and%20usage.html#motor-introduction-and-usage)
- [1. 520 motor](https://www.yahboom.net/public/upload/upload-html/1740571311/0.%20Motor%20introduction%20and%20usage.html#1-520-motor)
- [2. 310 motor](https://www.yahboom.net/public/upload/upload-html/1740571311/0.%20Motor%20introduction%20and%20usage.html#2-310-motor)
- [3. DC TT Motor](https://www.yahboom.net/public/upload/upload-html/1740571311/0.%20Motor%20introduction%20and%20usage.html#3-dc-tt-motor)
- [4. TT motor with encoder speed measurement](https://www.yahboom.net/public/upload/upload-html/1740571311/0.%20Motor%20introduction%20and%20usage.html#4-tt-motor-with-encoder-speed-measurement)
- [5. L-type 520 motor](https://www.yahboom.net/public/upload/upload-html/1740571311/0.%20Motor%20introduction%20and%20usage.html#5-l-type-520-motor)

## 1. 520 Motor

**Rekomendasi suplai:** 12V (dapat 11–16V; disarankan 12V).  
Tiga varian 520 memiliki **rated voltage 12V**. Untuk mengidentifikasi model, periksa label **RPM** pada bodi motor; cocokkan dengan **kecepatan setelah reduksi** pada tabel parameter.

**Parameter ringkas (contoh kolom):**
- Tipe motor: **Permanent magnet brush**  
- Encoder: **Hall incremental AB-phase**, **11 garis**  
- Rasio reduksi: 1:19 / 1:30 / 1:56 (tergantung model)  
- Arus stall: ±3–4A, arus rated: ±0.3A
- Output shaft: D-type 6 mm (eccentric)

**Wiring yang disarankan:**  
Gunakan kabel **PH2.0‑6PIN double-ended** (hitam) → satu ujung ke motor, ujung lain ke **port PH2.0‑6PIN encoder** pada driver. Pada wiring ini, fasa **A pada motor korespond ke fasa B** pada board. Maka **set tipe motor** dengan:  
```
$mtype:1#
```
Jika menggunakan **PH2.0‑6PIN → Dupont**, maka A motor → A board, B motor → B board. Pada wiring ini, **set tipe motor 310**:
```
$mtype:2#
```

## 2. 310 Motor

**Rekomendasi suplai:** 7.4V (boleh 4.2–8.4V; disarankan 7.4V).  
Parameter penting: **rasio reduksi** dan **jumlah garis encoder** (13 garis) — keduanya berpengaruh pada kontrol kecepatan.

**Wiring:**
- Jika motor 310 dibeli satuan: kabel **PH2.0‑6PIN → Dupont** ke **IO socket** di driver.
- Jika motor 310 dalam paket sasis: **PH2.0‑6PIN double-ended** (hitam ke motor; putih ke port encoder board).

**Set tipe motor 310:**
```
$mtype:2#
```

## 3. DC TT Motor (tanpa encoder)

**Rekomendasi suplai:** 7.4V.  
Parameter tipikal: **rasio 1:48**, **rated 6V**, idle current ±200 mA, stall ±1.5 A.

**Kontrol:** gunakan **PWM** (karena tanpa encoder).  
**Set tipe motor tanpa encoder:**
```
$mtype:4#
```
**Wiring:** port **XH2.54‑2PIN** motor → **XH2.54‑2PIN** pada driver.

## 4. TT Motor dengan Encoder

**Rekomendasi suplai:** 7.4V (boleh 5–13V).  
Encoder: **Hall AB‑phase**, **13 garis**, hitung maksimum per putaran roda **2340** (bergantung rasio).

**Wiring:** gunakan **PH2.0‑6PIN → Dupont** ke **IO socket** driver.  
Jika A motor → A board dan B motor → B board, set tipe berikut:
```
$mtype:3#
```

## 5. 520 Motor Tipe L (L-type 520)

**Rekomendasi suplai:** 12V.  
Parameter: rasio 1:40, 11 garis encoder, arus stall ±4 A.

**Wiring opsi 1 (disarankan):** **PH2.0‑6PIN double-headed (hitam)** → motor ↔ port encoder board. Pada wiring ini **A motor korespond ke B board**, maka set:
```
$mtype:1#
```
**Wiring opsi 2 (PH2.0‑6PIN → Dupont):** A motor → A board, B motor → B board, maka set:
```
$mtype:2#
```

**Catatan umum untuk semua motor ber‑encoder:** pastikan **`$mline`** (jumlah garis) dan **`$mphase`** (rasio reduksi) sesuai spesifikasi motor yang digunakan.


---

# Komunikasi Serial (PC Host)

## 1.1 Penjelasan
**Pastikan membaca “0. Motor introduction and usage”** untuk memahami parameter motor, metode wiring, dan tegangan suplai yang digunakan. Hal ini untuk menghindari kesalahan operasi serta potensi kerusakan pada driver atau motor.

Hubungkan papan driver ke komputer melalui **port Type‑C**, kemudian gunakan **serial port assistant** untuk mengirim perintah kontrol dan pembacaan data.

### Wiring Percontohan (Motor ↔ Driver)
| Motor | Driver Motor (Label) |
| :---: | :-------------------: |
| M2    | M‑                    |
| V     | 3V3                   |
| A     | H1A                   |
| B     | H1B                   |
| G     | GND                   |
| M1    | M+                    |

## 1.2 Instruksi
Buka software **Uart Assistant** (atau serupa).  
**Konfigurasi serial:** *Baud 115200, no parity, no hardware flow control, 1 stop bit.*

Kirim perintah sesuai daftar di bab **“Control command”** (lihat bagian sebelumnya). Contoh alur penggunaan:  
1) Jalankan `$read_flash#` untuk membaca parameter tersimpan (tipe ban/roda, deadzone, garis fase, rasio reduksi, diameter roda, PID).  
2) Ubah parameter sesuai motor/ban yang digunakan (tipe, reduksi, garis encoder, diameter, deadzone).  
3) Verifikasi kembali dengan `$read_flash#`.  
4) Kontrol gerak dengan `$spd:...#` (ber‑encoder) atau `$pwm:...#` (umum/tanpa encoder).

**Contoh:** kontrol motor 310 pada port Motor1:  
```
$spd:100,0,0,0#
```
Motor pada port Motor2:  
```
$spd:0,100,0,0#
```

---

# Catatan Tambahan Platform (Ringkas)

Bagian selanjutnya (Arduino, ESP32, Jetson, dsb.) pada README asli berisi:
- **Wiring spesifik** per board (UART Rx/Tx, VCC, GND).
- **Konfigurasi serial** (umumnya 115200 8N1).
- **Cuplikan kode** untuk: set parameter motor (`send_motor_type`, `send_pulse_phase`, `send_pulse_line`, `send_wheel_diameter`, `send_motor_deadzone`), dan **loop kontrol** yang meningkatkan kecepatan bertahap serta membaca data yang dikirim driver (`MAll`, `MTEP`, `MSPD`).

**Prinsip umum (lintas platform):**
- Jika pin **RX** pada board dipakai untuk komunikasi dengan driver, **lepas dulu** sebelum upload program, lalu sambungkan kembali setelah upload selesai (umum pada Arduino).  
- **I2C dan UART tidak digunakan bersamaan** pada saat yang sama untuk driver ini — pilih salah satu mode komunikasi.  
- Untuk debugging/printing, gunakan **serial terpisah** (mis. USB‑to‑TTL) agar tidak bentrok dengan UART yang terhubung ke driver.

**Tips validasi data:**
- Total pulse encoder: `MAll`
- Pulse real-time (10 ms): `MTEP`
- Kecepatan (mm/s): `MSPD`

Semua format dan protokol tetap **sama** seperti telah dijelaskan di bab perintah.


---

# Panduan Penggunaan dengan Arduino

## 1. Persiapan

### 1.1 Perangkat yang Diperlukan
- Papan **Arduino UNO / MEGA / Leonardo / Nano**
- **Modul Driver Motor 4-Channel Yahboom**
- Kabel **Type-C USB**
- Kabel **Dupont (female-to-female)** untuk koneksi UART
- **Motor DC 310** (atau jenis lain yang sesuai dengan konfigurasi `$mtype`)

### 1.2 Koneksi Hardware

| Arduino | Modul Driver Motor 4CH |
| :------: | :---------------------: |
| 5V       | 5V                     |
| GND      | GND                    |
| TX       | RX                     |
| RX       | TX                     |

**Catatan penting:**
- Lepas sambungan pin **RX/TX** dari modul sebelum proses **upload program** ke Arduino.
- Setelah upload selesai, **sambungkan kembali** kabel RX/TX agar komunikasi serial berjalan normal.
- Baud rate komunikasi ditetapkan pada **115200 bps**.

---

## 2. Contoh Kode Arduino (Serial Command)

Berikut contoh kode untuk menginisialisasi komunikasi dan mengirim perintah serial ke modul driver.

```cpp
#include <Arduino.h>

void setup() {
  Serial.begin(115200);   // Inisialisasi komunikasi serial
  delay(2000);
  
  Serial.println("$mtype:2#");        // Set tipe motor 310
  delay(200);
  Serial.println("$mphase:40#");      // Rasio reduksi 1:40
  delay(200);
  Serial.println("$mline:13#");       // Jumlah garis encoder 13
  delay(200);
  Serial.println("$wdiameter:66#");   // Diameter roda 66 mm
  delay(200);
  Serial.println("$deadzone:1600#");  // Dead zone PWM
  delay(200);
  Serial.println("$MPID:0.8,0.06,0.5#"); // Parameter PID default
  delay(200);
  Serial.println("$flash_reset#");    // Simpan konfigurasi dan restart modul
  delay(3000);
}

void loop() {
  // Perintah untuk menggerakkan kecepatan ke empat motor
  Serial.println("$spd:200,200,200,200#");  // Maju
  delay(2000);

  Serial.println("$spd:-200,-200,-200,-200#");  // Mundur
  delay(2000);

  Serial.println("$spd:0,0,0,0#");  // Berhenti
  delay(2000);
}
```

---

## 3. Monitoring Data Encoder

Untuk membaca data encoder yang dikirim modul, buka **Serial Monitor** pada Arduino IDE dengan baud rate 115200.

Contoh hasil keluaran:
```
$MAll:120,120,119,121#
$MTEP:13,13,12,13#
$MSPD:155,155,150,155#
```

**Penjelasan:**
- `$MAll` → Total jumlah pulse masing-masing motor.
- `$MTEP` → Pulse yang diterima setiap 10 ms.
- `$MSPD` → Kecepatan masing-masing roda dalam mm/s.

---

## 4. Troubleshooting Umum

| Masalah | Penyebab Kemungkinan | Solusi |
| :------ | :------------------- | :------ |
| Tidak ada respon dari modul | Salah baud rate / kabel TX-RX terbalik | Pastikan baud rate 115200 dan pin RX↔TX tertukar |
| Motor berputar tidak searah | Tipe motor salah atau wiring encoder terbalik | Ubah `$mtype` atau balik kabel A/B encoder |
| Gerak motor tidak stabil | Nilai PID tidak sesuai / deadzone terlalu kecil | Gunakan nilai default PID dan `$deadzone:1600#` |
| Data encoder tidak muncul | Motor tanpa encoder atau `$upload` belum diaktifkan | Gunakan `$upload:1,0,0#` untuk aktifkan kiriman data encoder |
| Kecepatan tidak sesuai nilai | Diameter roda atau rasio reduksi tidak akurat | Pastikan `$wdiameter` dan `$mphase` sesuai spesifikasi motor |

---

## 5. Tips Penggunaan Aman

1. **Gunakan catu daya stabil** sesuai spesifikasi motor (umumnya 7.4V–12V).
2. **Jangan ubah parameter PID secara ekstrem** tanpa uji bertahap.
3. **Gunakan `$flash_reset#`** hanya bila perlu mengembalikan ke pengaturan awal.
4. **Periksa suhu driver** jika motor bekerja pada arus tinggi (>4A) untuk waktu lama.
5. **Gunakan pendingin atau kipas kecil** bila driver dipasang dalam casing tertutup.


---

# Panduan Penggunaan dengan ESP32

## 1. Persiapan Perangkat

### 1.1 Perangkat yang Diperlukan
- Papan **ESP32 DevKit (DOIT, WROOM32, atau varian serupa)**
- **Modul Driver Motor 4-Channel Yahboom**
- **Motor DC 310** atau **TT ber-encoder**
- Kabel **Type-C USB**
- Kabel **Dupont female-to-female**

### 1.2 Konfigurasi UART

ESP32 memiliki beberapa port UART hardware. UART0 digunakan untuk komunikasi USB (upload & debug), sehingga untuk komunikasi dengan modul driver disarankan menggunakan **UART2**.

| ESP32 Pin | Fungsi | Keterangan |
| :--------: | :----: | :--------- |
| GPIO16     | RX2    | Terhubung ke TX modul driver |
| GPIO17     | TX2    | Terhubung ke RX modul driver |
| GND        | GND    | Ground bersama |
| 5V         | 5V     | Daya untuk modul driver |

**Catatan penting:**
- Gunakan **baud rate 115200 bps.**
- Pastikan kabel **RX dan TX tidak tertukar.**
- Gunakan **common ground (GND ke GND).**
- Lepaskan sambungan UART2 jika perlu upload ulang firmware ke ESP32.

---

## 2. Contoh Kode ESP32 (PlatformIO / Arduino Framework)

Berikut contoh program dasar menggunakan ESP32 untuk mengirim perintah konfigurasi dan kontrol motor ke modul driver.

```cpp
#include <Arduino.h>

#define RXD2 16
#define TXD2 17

void setup() {
  Serial.begin(115200);       // Debug monitor
  Serial2.begin(115200, SERIAL_8N1, RXD2, TXD2); // UART2 ke driver motor
  delay(2000);

  Serial2.println("$mtype:2#");        // Motor 310
  delay(200);
  Serial2.println("$mphase:40#");      // Rasio reduksi
  delay(200);
  Serial2.println("$mline:13#");       // Jumlah garis encoder
  delay(200);
  Serial2.println("$wdiameter:66#");   // Diameter roda (mm)
  delay(200);
  Serial2.println("$deadzone:1600#");  // Dead zone PWM
  delay(200);
  Serial2.println("$flash_reset#");    // Simpan dan restart modul
  delay(3000);
}

void loop() {
  // Jalankan maju selama 2 detik
  Serial2.println("$spd:200,200,200,200#");
  delay(2000);

  // Mundur selama 2 detik
  Serial2.println("$spd:-200,-200,-200,-200#");
  delay(2000);

  // Berhenti
  Serial2.println("$spd:0,0,0,0#");
  delay(2000);
}
```

---

## 3. Monitoring Data Encoder

Gunakan fungsi pembacaan serial untuk menerima data dari driver. Contoh implementasi sederhana:

```cpp
void loop() {
  if (Serial2.available()) {
    String data = Serial2.readStringUntil('#');
    Serial.println("Data dari driver: " + data);
  }
}
```

**Hasil tipikal di Serial Monitor:**
```
$MAll:1024,1024,1020,1023#
$MTEP:13,13,12,13#
$MSPD:160,160,159,161#
```

**Penjelasan:**
- `$MAll` → Total pulse masing-masing motor.
- `$MTEP` → Pulse yang diterima setiap 10 ms.
- `$MSPD` → Kecepatan roda dalam mm/s.

---

## 4. Troubleshooting Umum

| Masalah | Penyebab Kemungkinan | Solusi |
| :------ | :------------------- | :------ |
| Tidak ada komunikasi | RX/TX tertukar atau UART salah | Gunakan UART2 (GPIO16 & 17) dan pastikan kabel benar |
| Tidak ada data encoder | Motor tanpa encoder / `$upload` belum aktif | Aktifkan `$upload:1,0,0#` |
| Motor bergetar / tidak stabil | Deadzone atau PID tidak sesuai | Gunakan `$deadzone:1600#` dan PID bawaan |
| Data tidak terbaca di monitor | Baud rate berbeda | Pastikan 115200 di Serial2 dan Serial Monitor |

---

## 5. Tips Tambahan

1. Gunakan catu daya eksternal 12V jika beban motor berat.
2. Jangan hubungkan pin 5V dari ESP32 langsung ke motor besar (gunakan regulator terpisah jika perlu).
3. Gunakan **Serial.println()** untuk debug tambahan tanpa mengganggu UART2.
4. Simpan konfigurasi stabil menggunakan `$flash_reset#` setelah tuning parameter selesai.


---

# Panduan Penggunaan dengan Jetson Nano / Raspberry Pi

## 1. Persiapan Perangkat

### 1.1 Perangkat yang Diperlukan
- **Jetson Nano / Raspberry Pi 4 / 3B+**
- **Modul Driver Motor 4-Channel Yahboom**
- **Motor DC 310 / TT ber-encoder**
- Kabel **Type-C USB** atau **UART-to-USB converter (CP2102/CH340)**
- Kabel **Dupont female-to-female**

### 1.2 Mode Komunikasi

Driver dapat dihubungkan ke Jetson atau Raspberry Pi melalui dua cara:
1. **UART Serial** — menggunakan pin GPIO (TX, RX, GND).
2. **I2C** — menggunakan jalur SDA dan SCL.

#### Konfigurasi UART (Direkomendasikan)

| Jetson/RPi Pin | Fungsi | Keterangan |
| :-------------: | :----: | :---------- |
| Pin 6           | GND    | Ground bersama |
| Pin 8           | TXD    | Terhubung ke RX driver |
| Pin 10          | RXD    | Terhubung ke TX driver |
| Pin 2 / 4       | 5V     | Daya modul driver |

**Catatan penting:**
- Pastikan **login sebagai root** atau gunakan `sudo` untuk mengakses serial.  
- Gunakan **baud rate 115200**.  
- Tambahkan user ke grup `dialout` jika muncul error permission:
  ```bash
  sudo usermod -a -G dialout $USER
  ```
  Lalu logout dan login kembali.

---

## 2. Instalasi Dependensi (Python)

Untuk komunikasi serial menggunakan Python di Jetson/RPi, instal pustaka `pyserial`:

```bash
sudo apt update
sudo apt install python3-pip -y
pip3 install pyserial
```

---

## 3. Contoh Kode Python (UART Serial)

```python
import serial
import time

# Inisialisasi port serial (ubah sesuai perangkat, contoh: /dev/ttyTHS1 atau /dev/ttyS0)
ser = serial.Serial("/dev/ttyTHS1", 115200, timeout=1)

time.sleep(2)

def send_command(cmd):
    ser.write((cmd + "\r\n").encode())
    print("Kirim:", cmd)
    time.sleep(0.2)

# Konfigurasi awal
send_command("$mtype:2#")       # Motor 310
send_command("$mphase:40#")     # Rasio reduksi
send_command("$mline:13#")      # Garis encoder
send_command("$wdiameter:66#")  # Diameter roda
send_command("$deadzone:1600#") # Deadzone PWM
send_command("$flash_reset#")   # Simpan & restart

time.sleep(3)

# Loop kontrol
while True:
    send_command("$spd:200,200,200,200#")
    time.sleep(2)
    send_command("$spd:-200,-200,-200,-200#")
    time.sleep(2)
    send_command("$spd:0,0,0,0#")
    time.sleep(2)

    # Baca data encoder
    if ser.in_waiting > 0:
        data = ser.readline().decode().strip()
        print("Data dari driver:", data)
```

**Hasil tipikal:**
```
Kirim: $mtype:2#
Kirim: $spd:200,200,200,200#
Data dari driver: $MSPD:152,150,149,153#
```

---

## 4. Mode I2C (Alternatif)

Driver juga dapat dikontrol melalui antarmuka **I2C** dengan alamat `0x26`.  
Gunakan library Python seperti `smbus2`.

### Instalasi Library:
```bash
sudo apt install python3-smbus -y
pip3 install smbus2
```

### Contoh Kode Python (I2C):
```python
from smbus2 import SMBus
import time

ADDR = 0x26
bus = SMBus(1)

def write_word(register, value):
    high = (value >> 8) & 0xFF
    low = value & 0xFF
    bus.write_i2c_block_data(ADDR, register, [high, low])

# Set kecepatan PWM ke empat motor
write_word(0x07, 100)   # M1
write_word(0x07, 100)   # M2
write_word(0x07, 100)   # M3
write_word(0x07, 100)   # M4
time.sleep(1)

# Set motor berhenti
write_word(0x07, 0)
time.sleep(1)
bus.close()
```

**Catatan penting:**
- Pastikan alamat device I2C benar (`sudo i2cdetect -y 1`).  
- Jalankan dengan hak akses root bila perlu.  
- Hindari penggunaan UART dan I2C bersamaan.

---

## 5. Troubleshooting Umum

| Masalah | Penyebab | Solusi |
| :------ | :-------- | :------ |
| Modul tidak terdeteksi di `/dev/` | Izin akses atau kabel salah | Pastikan kabel RX/TX benar dan user ada di grup `dialout` |
| Tidak ada data dari modul | Timeout serial / baud rate salah | Pastikan `115200` dan gunakan `timeout=1` di objek Serial |
| I2C gagal menulis | Register atau tipe data salah | Gunakan format data 16-bit sesuai tabel register |
| Kecepatan tidak berubah | Perintah `$spd` tidak diterima | Tambahkan jeda antar-perintah `time.sleep(0.2)` |
| Motor bergetar saat berhenti | Deadzone tidak sesuai | Gunakan `$deadzone:1600#` untuk stabilisasi |

---

## 6. Tips Integrasi Jetson / Raspberry Pi

1. Jalankan komunikasi serial dalam **thread terpisah** untuk membaca dan menulis data tanpa delay.
2. Gunakan **filter data encoder** (moving average) untuk stabilitas kecepatan.
3. Pastikan **catu daya Jetson dan driver terpisah**, dengan **ground bersama**.
4. Gunakan **UPS atau regulator DC-DC** jika motor besar untuk menghindari reset Jetson/RPi akibat drop tegangan.
5. Backup konfigurasi motor ke flash modul menggunakan `$flash_reset#` setelah semua parameter stabil.


---

