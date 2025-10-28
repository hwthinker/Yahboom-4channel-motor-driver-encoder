# Welcome to 4-Channel Motor Drive Module repository

## 1.1 Pengenalan Board Driver Motor 4-Channel

![image-20251028052746916](C:/Users/hardware/Documents/Yahboom 4channel-motor-driver-encoder/assets/image-20251028052746916.png)

### Pengenalan Produk:

Modul driver motor encoder 4-channel mengintegrasikan koprosesor chip tunggal berkinerja tinggi, yang dapat terhubung dengan mulus dengan berbagai kontroler seperti MSPM0, STM32, Raspberry Pi dan Jetson melalui komunikasi port serial atau IIC, menyederhanakan proses penggerak.

Hanya membutuhkan empat kabel penghubung untuk mencapai komunikasi efisien dengan unit kontrol utama untuk dengan mudah mengontrol motor dan mendapatkan data encoder, mengurangi jumlah kabel dan mengurangi kesulitan operasi.

Pada saat yang sama, mendukung penggerak sebagian besar motor TT encoder Hall, motor reduksi DC 520/310 dan lainnya di pasaran.

### Tabel Parameter:

| Spesifikasi Teknis                         |             Parameter             |
| :----------------------------------------- | :-------------------------------: |
| Tegangan Input yang Direkomendasikan       |               5-12v               |
| Arus DC untuk Pin 5v                       |               0.7A                |
| Arus DC untuk Pin 3.3v                     |               500ma               |
| Arus penggerak berkelanjutan motor tunggal | Default 4A (output maksimum 5.5A) |
| Panjang * Lebar * Tinggi                   |         56 * 65 * 13.4mm          |
| Interface motor encoder                    |  PH2.0-6PIN、soket kabel Dupont   |
| Interface motor DC                         |            XH2.54-2PIN            |

## 4 interface motor pada modul sesuai dengan motor pada mobil robot, seperti ditunjukkan di bawah ini

M1 -> Motor kiri atas (roda depan kiri mobil) M2 -> Motor kiri bawah (roda belakang kiri mobil) M3 -> Motor kanan atas (roda depan kanan mobil) M4 -> Motor kanan bawah (roda belakang kanan mobil)

## Konfigurasi Port Serial

**Baud rate 115200, tanpa paritas, tanpa kontrol aliran perangkat keras, 1 stop bit**

 

### 1.Konfigurasi Tipe Motor

| Perintah  | Penjelasan  |  Contoh   |          Keterangan          | Default Firmware | Simpan saat mati |
| :-------: | :---------: | :-------: | :--------------------------: | :--------------: | :--------------: |
| $mtype:x# | Model motor | $mtype:1# | Model motor adalah motor 520 |    Motor 520     |        Y         |
|  Catatan  |             |           |                              |                  |                  |

1. Pemilihan tipe motor. Jika encoder motor A terhubung ke port A board, maka B terhubung ke B. Anda perlu memilih model motor 310. Jika tidak, Anda perlu memilih motor 520 atau motor TT.
2. Perintah dapat dikirim dalam huruf besar atau kecil semua.
3. Jika perintah di atas berhasil, akan mengembalikan pesan **perintah+OK**. Jika tidak ada pesan yang dikembalikan, periksa koneksi port serial.
4. x: adalah tipe motor. Tipe motor yang diwakili oleh nilai yang berbeda adalah sebagai berikut: 1: motor 520 2: motor 310 3: motor TT (dengan encoder) 4: motor TT (tanpa encoder)

Catatan: Jika Anda menggunakan motor tanpa encoder, Anda dapat memilih tipe 4, yaitu perintahnya adalah: $mtype:4# Jika Anda menggunakan motor dengan encoder, Anda dapat memilih salah satu dari 1, 2, dan 3.

### 2.Konfigurasi Deadband Motor

|    Perintah     |              Penjelasan               |     Contoh      |                          Keterangan                          | Default Firmware | Simpan saat mati |
| :-------------: | :-----------------------------------: | :-------------: | :----------------------------------------------------------: | :--------------: | :--------------: |
| $deadzone:xxxx# | Konfigurasi zona mati pulsa pwm motor | $deadzone:1650# | Saat mengontrol PWM, nilai zona mati akan ditambahkan secara default sehingga motor tidak akan memiliki area osilasi. |       1600       |        Y         |
|     Catatan     |                                       |                 |                                                              |                  |                  |

1. Perintah dapat dikirim dalam huruf besar atau kecil semua
2. Jika perintah di atas berhasil, akan mengembalikan pesan **perintah+OK**. Jika tidak ada pesan yang dikembalikan, periksa koneksi port serial
3. xxxx: adalah nilai zona mati, yang perlu diukur. Dengan mengubah nilai ini, getaran minimum motor dapat dihilangkan
4. Rentang nilai zona mati (0-3600)

### 3.Konfigurasi Garis Fase Motor

|  Perintah  |          Penjelasan          |   Contoh   |                      Keterangan                      | Default Firmware | Simpan saat mati |
| :--------: | :--------------------------: | :--------: | :--------------------------------------------------: | :--------------: | :--------------: |
| $mline:xx# | Konfigurasi garis fase motor | $mline:13# | Konfigurasi fase encoder Hall motor menjadi 13 garis |        11        |        Y         |
|  Catatan   |                              |            |                                                      |                  |                  |

1. Perintah dapat dikirim dalam huruf besar atau kecil semua
2. Perintah di atas akan mengembalikan informasi **perintah+OK** jika berhasil. Jika tidak ada informasi yang dikembalikan, periksa koneksi port serial
3. xx: Ini adalah fase encoder Hall untuk satu putaran. Nilai ini perlu diperoleh dengan memeriksa tabel parameter motor dari pedagang
4. Untuk motor dengan encoder: Nilai ini memainkan **peran utama** dalam mengontrol kecepatan. Nilai ini harus benar
5. Motor tanpa encoder: Konfigurasi nilai ini dapat diabaikan

### 4.Konfigurasi Rasio Reduksi Motor

|  Perintah   |           Penjelasan            |   Contoh    |                 Keterangan                 | Default Firmware | Simpan saat mati |
| :---------: | :-----------------------------: | :---------: | :----------------------------------------: | :--------------: | :--------------: |
| $mphase:xx# | Konfigurasi rasio reduksi motor | $mphase:40# | Konfigurasi rasio reduksi motor menjadi 40 |        30        |        Y         |
| **Catatan** |                                 |             |                                            |                  |                  |

1. Perintah dapat dikirim dalam huruf besar atau kecil semua
2. Perintah di atas akan mengembalikan informasi **perintah+OK** jika berhasil. Jika tidak ada informasi yang dikembalikan, periksa koneksi port serial
3. xx: Ini adalah parameter rasio reduksi motor. Nilai ini perlu diperoleh dengan memeriksa tabel parameter motor dari pedagang
4. Untuk motor dengan encoder: Nilai ini memainkan **peran utama** dalam mengontrol kecepatan. Nilai ini harus benar
5. Motor tanpa encoder: Konfigurasi nilai ini dapat diabaikan

### 5.Konfigurasi Diameter Roda (Opsional)

|    Perintah    |        Penjelasan         |     Contoh     |        Keterangan         | Default Firmware | Simpan saat mati |
| :------------: | :-----------------------: | :------------: | :-----------------------: | :--------------: | :--------------: |
| $wdiameter:xx# | Konfigurasi diameter roda | $wdiameter:50# | Diameter roda adalah 50mm |      67 mm       |        Y         |
|  **Catatan**   |                           |                |                           |                  |                  |

1. Perintah dapat dikirim dalam huruf besar atau kecil semua
2. Perintah di atas akan mengembalikan informasi **perintah+OK** jika berhasil. Jika tidak ada informasi yang dikembalikan, periksa koneksi port serial
3. xx: Ini adalah diameter roda. Nilai ini dapat diukur atau diperoleh menggunakan informasi pedagang
4. Untuk motor dengan encoder: Nilai ini memainkan **peran utama** dalam mengontrol kecepatan. Nilai ini harus benar dalam milimeter (mm); jika nilai ini salah, hanya akan mempengaruhi data kecepatan yang tidak akurat, dan tidak akan mempengaruhi data encoder
5. Motor tanpa encoder: Konfigurasi nilai ini dapat diabaikan

### 6.Konfigurasi Parameter PID untuk Kontrol Motor

|       Perintah        |        Penjelasan         |       Contoh        |                          Keterangan                          |  Default Firmware  | Simpan saat mati |
| :-------------------: | :-----------------------: | :-----------------: | :----------------------------------------------------------: | :----------------: | :--------------: |
| $MPID:x.xx,x.xx,x.xx# | Konfigurasi parameter PID | $MPID:1.5,0.03,0.1# | Konfigurasi kontrol kecepatan adalah P: 1.5, I: 0.03, D: 0.1 | P:0.8 I:0.06 D:0.5 |        Y         |
|      **Catatan**      |                           |                     |                                                              |                    |                  |

1. Perintah dapat dikirim dalam huruf besar atau kecil semua
2. Perintah di atas akan mengembalikan **perintah+OK** jika berhasil. Jika tidak ada informasi yang dikembalikan, periksa koneksi port serial
3. x.xx, x.xx, x.xx: Ini adalah parameter untuk mengontrol motor p, i, d masing-masing. **Setiap kali nilai diubah, chip akan restart dan menghentikan motor yang bergerak. Ini adalah situasi normal**
4. Untuk motor dengan encoder: parameter pid valid, dan nilai ini harus benar. **Umumnya, tidak perlu memodifikasi pid, dan nilai default dapat digunakan**
5. Motor tanpa encoder: parameter pid tidak valid, dan konfigurasi nilai ini dapat diabaikan

### 7.Reset Semua Variabel ke Nilai Default

|   Perintah    |           Penjelasan            | Contoh | Keterangan | Default Firmware | Simpan saat mati |
| :-----------: | :-----------------------------: | :----: | :--------: | :--------------: | :--------------: |
| $flash_reset# | Kembalikan nilai default pabrik |   -    |     -      |        -         |        -         |
|  **Catatan**  |                                 |        |            |                  |                  |

1. Perintah dapat dikirim dalam huruf besar atau kecil semua
2. Jika perintah di atas berhasil, akan mengembalikan pesan **perintah+OK**. Jika tidak ada pesan yang dikembalikan, periksa koneksi port serial
3. Eksekusi perintah ini dan modul akan restart sekali

### 8.Perintah Kontrol Kecepatan

|   Perintah    |        Penjelasan         |       Contoh        |                     Keterangan                      | Default Firmware | Simpan saat mati |
| :-----------: | :-----------------------: | :-----------------: | :-------------------------------------------------: | :--------------: | :--------------: |
| $spd:0,0,0,0# | Kontrol kecepatan 4 motor | $spd:100,-100,0,50# | Kontrol kecepatan 4 motor M1:100 M2:-100 M3:0 M4:50 |        -         |        N         |
|  **Catatan**  |                           |                     |                                                     |                  |                  |

1. Perintah dapat dikirim dalam huruf besar atau kecil semua
2. Jika perintah di atas berhasil, akan mengembalikan pesan **perintah+OK**. Jika tidak ada pesan yang dikembalikan, periksa koneksi port serial
3. Untuk motor dengan encoder: perintah ini berfungsi untuk mengontrol kecepatan motor
4. Motor tanpa encoder: perintah ini tidak valid
5. Perintah kontrol motor tidak perlu dikirim berulang kali; cukup kirim sekali, dan modul akan mengontrol motor menurut kecepatan yang ditetapkan, hingga perintah kontrol kecepatan baru diterima atau perintah berhenti dikirim.

Catatan: Setelah perintah ini dikirim, encoder atau data kecepatan akan secara otomatis dikirim balik menurut perintah yang telah dikonfigurasi sebelumnya.

### 9.Instruksi Kontrol PWM Langsung

|   Perintah    |            Penjelasan             |        Contoh        |                         Keterangan                         | Default Firmware | Simpan saat mati |
| :-----------: | :-------------------------------: | :------------------: | :--------------------------------------------------------: | :--------------: | :--------------: |
| $pwm:0,0,0,0# | Kontrol 4 motor dengan output PWM | $spd:0,-520,300,800# | Kontrol output PWM dari 4 motor M1:0 M2:-520 M3:300 M4:800 |        -         |        N         |
|  **Catatan**  |                                   |                      |                                                            |                  |                  |

1. Perintah dapat dikirim dalam huruf besar atau kecil semua
2. Jika perintah di atas berhasil, motor akan bergerak, dan tidak ada yang akan dikembalikan dari port serial
3. Rentang kecepatan adalah (-3600~3600) dan tidak valid jika melebihi rentang
4. Untuk kontrol motor tanpa encoder, **Anda dapat mengontrolnya melalui perintah ini**
5. 0,0,0,0: mewakili M1,M2,M3,M4 pada layar board

### 10.Laporan Data Encoder (Perintah ini hanya valid untuk motor dengan encoder)

|    Perintah    |     Penjelasan      |     Contoh     |                          Keterangan                          | Default Firmware | Simpan saat mati |
| :------------: | :-----------------: | :------------: | :----------------------------------------------------------: | :--------------: | :--------------: |
| $upload:0,0,0# | Terima data encoder | $upload:1,0,0# | Terima data encoder total dari putaran roda 1: buka, 0: tidak menerima |        -         |        N         |
|  **Catatan**   |                     |                |                                                              |                  |                  |

1. Perintah dapat dikirim dalam huruf besar atau kecil semua
2. $upload:0,0,0#: 0 pertama mewakili: data encoder total dari putaran roda. 0 kedua mewakili: data encoder real-time dari putaran roda (10ms). 0 ketiga mewakili: kecepatan roda
3. Informasi yang sesuai dapat diterima pada saat yang sama

- Data encoder total dari putaran roda mengembalikan informasi: "$MAll:M1,M2,M3,M4#"
- Data encoder real-time dari putaran roda mengembalikan informasi: "$MTEP:M1,M2,M3,M4#"
- Kecepatan roda mengembalikan informasi: "$MSPD:M1,M2,M3,M4#"

### 11.Query Variabel Flash

|   Perintah   |      Penjelasan      | Contoh | Keterangan | Default Firmware | Simpan saat mati |
| :----------: | :------------------: | :----: | :--------: | :--------------: | :--------------: |
| $read_flash# | Query variabel flash |   -    |     -      |        -         |        N         |
|   Catatan    |                      |        |            |                  |                  |

1. Perintah dapat dikirim dalam huruf besar atau kecil semua
2. Jika perintah di atas berhasil, akan mengembalikan pesan **perintah+OK**. Jika tidak ada pesan yang dikembalikan, periksa koneksi port serial

### 12.Cek Level Baterai

|  Perintah  |    Penjelasan     | Contoh | Keterangan | Default Firmware | Simpan saat mati |
| :--------: | :---------------: | :----: | :--------: | :--------------: | :--------------: |
| $read_vol# | Cek level baterai |   -    |     -      |        -         |        N         |
|  Catatan   |                   |        |            |                  |                  |

1. Perintah dapat dikirim dalam huruf besar atau kecil semua
2. Jika perintah di atas berhasil, akan mengembalikan informasi **daya baterai ($Battery:7.40V#)**. Jika tidak ada informasi yang dikembalikan, silakan periksa koneksi port serial

## Kontrol Protokol IIC

**Alamat perangkat IIC board driver motor 4-channel:** 0x26

| Alamat Register | R/W  |   Tipe   |                           Rentang                            |                          Penjelasan                          | Contoh                                                       |
| :-------------: | :--: | :------: | :----------------------------------------------------------: | :----------------------------------------------------------: | :----------------------------------------------------------- |
|      0x01       |  w   | uint8_t  | 1: motor 520 2: motor 310 3: motor TT (dengan encoder) 4: motor TT (tanpa encoder) |                       Tulis tipe motor                       | Alamat perangkat + alamat register + tipe motor              |
|      0x02       |  w   | uint16_t |                            0-3600                            |                  Konfigurasi deadband motor                  | Alamat perangkat + alamat register + nilai zona mati motor   |
|      0x03       |  w   | uint16_t |                           0-65535                            |        Konfigurasi jumlah garis cincin magnetik motor        | Alamat perangkat + alamat register + jumlah garis cincin magnetik motor |
|      0x04       |  w   | uint16_t |                           0-65535                            |               Konfigurasi rasio reduksi motor                | Alamat perangkat + alamat register + rasio reduksi motor     |
|      0x05       |  w   |  float   |                              -                               |              Masukkan diameter roda, satuan: mm              | Alamat perangkat + alamat register + diameter roda (perlu mengkonversi float ke bytes - little endian terlebih dahulu) |
|      0x06       |  w   | int16_t  |                          -1000~1000                          | Kontrol kecepatan, register ini hanya efektif untuk motor dengan encoder, satuan: mm | Alamat perangkat + alamat register + kecepatan (mentransmisikan data 4 motor setiap kali) **Mode big-endian** Setiap kecepatan menempati 2 bit Untuk uint8_t misalnya: kecepatan motor m1 200, kecepatan motor m2 -200, kecepatan motor m3 0, kecepatan motor m4 500 Yaitu: [0x00 0xC8 0xFF 0x38 0x00 0x00 0x01 0xf4] |
|      0x07       |  w   | int16_t  |                          -3600~3600                          | Kontrol PWM, kontrol ini tidak memerlukan data encoder dan dapat langsung mengontrol rotasi motor | Alamat perangkat + alamat register + kecepatan (mentransmisikan data 4 motor setiap kali) **Mode big-endian** Setiap kecepatan menempati 2 bit Untuk uint8_t misalnya: pwm motor m1 200, pwm motor m2 adalah -200, pwm motor m3 adalah 0, pwm motor m4 adalah 500 Yaitu: [0x00 0xC8 0xFF 0x38 0x00 0x00 0x01 0xf4] |
|      0x08       |  R   | uint16_t |                              -                               |                    Membaca level baterai                     | Data yang benar: data = (buf[0]<<8\|buf[1])/10.0             |
|      0x10       |  R   | int16_t  |                              -                               |      Baca data pulsa real-time encoder motor M1 - 10ms       | Data yang benar: data = buf[0]<<8\|buf[1]                    |
|      0x11       |  R   | int16_t  |                              -                               |      Baca data pulsa real-time encoder motor M2 - 10ms       | Data yang benar: data = buf[0]<<8\|buf[1]                    |
|      0x12       |  R   | int16_t  |                              -                               |      Baca data pulsa real-time encoder motor M3 - 10ms       | Data yang benar: data = buf[0]<<8\|buf[1]                    |
|      0x13       |  R   | int16_t  |                              -                               |      Baca data pulsa real-time encoder motor M4 - 10ms       | Data yang benar: data = buf[0]<<8\|buf[1]                    |
|      0x20       |  R   | int16_t  |                              -                               |     Baca data pulsa total encoder motor M1 (Bit tinggi)      | -                                                            |
|      0x21       |  R   | int16_t  |                              -                               |     Baca data pulsa total encoder motor M1 (Bit rendah)      | Data yang diperoleh perlu digeser untuk mendapatkan data yang benar. Bit tinggi mewakili: buf[0] buf[1] Bit rendah mewakili: bf[0] bf[1] (data = buf[0]<<24\|buf[1]<<16\|bf[0]<<8\|bf[1]) |
|      0x22       |  R   | int16_t  |                              -                               |     Baca data pulsa total encoder motor M2 (Bit tinggi)      | -                                                            |
|      0x23       |  R   | int16_t  |                              -                               |     Baca data pulsa total encoder motor M2 (Bit rendah)      | Metode perhitungan sama dengan M1                            |
|      0x24       |  R   | int16_t  |                              -                               |     Baca data pulsa total encoder motor M3 (Bit tinggi)      | -                                                            |
|      0x25       |  R   | int16_t  |                              -                               |     Baca data pulsa total encoder motor M3 (Bit rendah)      | Metode perhitungan sama dengan M1                            |
|      0x26       |  R   | int16_t  |                              -                               |     Baca data pulsa total encoder motor M4 (Bit tinggi)      | -                                                            |
|      0x27       |  R   | int16_t  |                              -                               |     Baca data pulsa total encoder motor M4 (Bit rendah)      | Metode perhitungan sama dengan M1                            |

# Cara Memperbarui Firmware

Buka software pembakaran FlyMcu yang disediakan dalam lampiran, hubungkan port typec dari board driver motor empat jalur ke komputer, kemudian klik Enumport di software tersebut. Dan pilih port serial yang digunakan oleh board driver Anda.

![image-20250611160834336](C:/Users/hardware/Documents/Yahboom 4channel-motor-driver-encoder/assets/image-20250611160834336.png)

Pada file program, pilih file firmware yang telah diunduh, kemudian perhatikan bahwa pengaturan lain dalam kotak merah harus sama dengan yang ada di gambar.

![image-20250611160857277](C:/Users/hardware/Documents/Yahboom 4channel-motor-driver-encoder/assets/image-20250611160857277.png)

Terakhir, cukup klik Start Programming. Tidak diperlukan operasi lain dan firmware akan mulai dibakar. Gambar berikut menunjukkan informasi yang ditampilkan setelah pembakaran berhasil:

![image-20250611160924015](C:/Users/hardware/Documents/Yahboom 4channel-motor-driver-encoder/assets/image-20250611160924015.png)

Terakhir, cabut dan colokkan kabel type-c lagi untuk me-restart board driver. Jika lampu merah selalu menyala dan lampu hijau berkedip dua kali setiap 3 detik, maka pembakaran berhasil.

# Pengenalan dan Penggunaan Motor

**Kursus ini digunakan untuk menjelaskan parameter motor, tegangan supply yang direkomendasikan, dan metode perkabelan yang direkomendasikan untuk menghubungkan motor ke board driver motor 4-channel.** 

## 1. Motor 520

![img](C:/Users/hardware/Documents/Yahboom 4channel-motor-driver-encoder/assets/1.png)

|         Parameter         |                         MD520Z19_12V                         |                         MD520Z30_12V                         |                         MD520Z56_12V                         |
| :-----------------------: | :----------------------------------------------------------: | :----------------------------------------------------------: | :----------------------------------------------------------: |
|      Tegangan rated       |                             12V                              |                             12V                              |                             12V                              |
|        Tipe motor         |                    Sikat magnet permanen                     |                    Sikat magnet permanen                     |                    Sikat magnet permanen                     |
|       Poros output        |             Poros eksentrik tipe-D diameter 6mm              |             Poros eksentrik tipe-D diameter 6mm              |             Poros eksentrik tipe-D diameter 6mm              |
|        Torsi stall        |                           3.1kg·cm                           |                           4.8kg·cm                           |                           8.3kg·cm                           |
|        Torsi rated        |                           2.2kg·cm                           |                           3.3kg·cm                           |                           6.5kg·cm                           |
| Kecepatan sebelum reduksi |                           11000rpm                           |                           11000rpm                           |                           12000rpm                           |
| Kecepatan setelah reduksi |                          550±10rpm                           |                          333±10rpm                           |                          205±10rpm                           |
|        Daya rated         |                             ≤4W                              |                             ≤4W                              |                             ≤4W                              |
|        Arus stall         |                              3A                              |                              3A                              |                              4A                              |
|        Arus rated         |                             0.3A                             |                             0.3A                             |                             0.3A                             |
|  Rasio reduksi gear set   |                             1:19                             |                             1:30                             |                             1:56                             |
|       Tipe encoder        |               Encoder Hall incremental fase AB               |               Encoder Hall incremental fase AB               |               Encoder Hall incremental fase AB               |
|  Tegangan supply encoder  |                            3.3-5V                            |                            3.3-5V                            |                            3.3-5V                            |
|   Jumlah loop magnetik    |                           11 garis                           |                           11 garis                           |                           11 garis                           |
|      Tipe interface       |                          PH2.0 6Pin                          |                          PH2.0 6Pin                          |                          PH2.0 6Pin                          |
|          Fungsi           | Dengan pembentukan pull-up built-in, MCU dapat langsung membaca pulsa sinyal | Dengan pembentukan pull-up built-in, MCU dapat langsung membaca pulsa sinyal | Dengan pembentukan pull-up built-in, MCU dapat langsung membaca pulsa sinyal |
|    Berat motor tunggal    |                           150g±1g                            |                           150g±1g                            |                           150g±1g                            |

Catu daya yang direkomendasikan: **12V**.

Ada tiga jenis motor 520, dan tegangan rated mereka adalah **12V**. Ketika kita menggerakkan motor 520, kita dapat menghubungkan tegangan antara 11 dan 16V, dan disarankan untuk menggunakan supply tegangan 12V**.

Jika Anda ingin membedakan model motor 520 yang Anda beli, Anda dapat langsung melihat label yang tercetak pada motor 520. Ada teks yang tercetak di atasnya bernama RPM, dan angka di depan RPM sesuai dengan angka **kecepatan setelah reduksi** dalam tabel parameter.

Misalnya, label motor 520 di tangan saya mengatakan 333RPM, jadi Anda harus memperhatikan parameter dalam kolom **MD520Z30_12V**. Khususnya, dua parameter **rasio reduksi dan jumlah garis cincin magnetik** mungkin perlu dimodifikasi saat menggunakan board driver motor 4-channel.

![img](C:/Users/hardware/Documents/Yahboom 4channel-motor-driver-encoder/assets/2.png)

Perkabelan yang direkomendasikan:

Motor 520 yang Anda beli akan dilengkapi dengan dua jenis kabel. Di sini kami merekomendasikan agar Anda memilih kabel double-ended PH2.0-6PIN hitam, satu ujung terhubung ke motor, dan ujung lainnya langsung terhubung ke interface motor encoder PH2.0-6PIN pada board driver motor empat jalur. Kita dapat menemukan bahwa A pada motor sesuai dengan fase B dari board driver motor empat jalur.

Jadi saat mengkonfigurasi tipe motor pada board driver motor empat jalur, Anda harus memilih `$mtype:1#`, model motor 520.

![img](C:/Users/hardware/Documents/Yahboom 4channel-motor-driver-encoder/assets/3.png)![img](https://www.yahboom.net/public/upload/upload-html/1740571311/4.png)

Instruksi perkabelan motor 520:

Jika Anda menggunakan koneksi PH2.0-6PIN ke kabel Dupont, Anda dapat menghubungkan sesuai dengan gambar di bawah ini. Dengan koneksi ini, fase A motor akan terhubung ke fase A board driver motor empat jalur, dan fase B akan terhubung ke fase B.

Namun, saat mengkonfigurasi tipe motor, Anda harus memilih `$mtype:2#`, model motor 310.

 

![img](C:/Users/hardware/Documents/Yahboom 4channel-motor-driver-encoder/assets/5.png)

 

## 2. Motor 310

![img](C:/Users/hardware/Documents/Yahboom 4channel-motor-driver-encoder/assets/6.png)

​	

| Parameter                 | Nilai/deskripsi                                              |
| ------------------------- | ------------------------------------------------------------ |
| Nama motor                | MD310Z20_7.4V                                                |
| Arus stall                | ≤1.4A                                                        |
| Tegangan rated motor      | 7.4V                                                         |
| Arus rated                | ≤0.65A                                                       |
| Tipe motor                | Sikat magnet permanen                                        |
| Rasio reduksi gear set    | 1:20                                                         |
| Poros output              | Poros eksentrik tipe-D diameter 3mm                          |
| Tipe encoder              | Encoder Hall incremental fase AB                             |
| Torsi stall               | ≥1.0kg·cm                                                    |
| Tegangan supply encoder   | 3.3-5V                                                       |
| Torsi rated               | 0.4kg·cm                                                     |
| Jumlah loop magnetik      | 13 garis                                                     |
| Kecepatan sebelum reduksi | 9000rpm                                                      |
| Tipe interface            | PH2.0 6Pin                                                   |
| Fungsi                    | Dengan pembentukan pull-up built-in, MCU dapat langsung membaca pulsa sinyal |
| Kecepatan setelah reduksi | 450±10rpm                                                    |
| Daya rated                | 4.8W                                                         |
| Berat motor tunggal       | 70g                                                          |

Catu daya yang direkomendasikan: **7.4V**. Dapat dihubungkan ke tegangan antara 4.2~8.4V, **direkomendasikan menggunakan tegangan 7.4V**.

Dua parameter **rasio reduksi dan jumlah garis cincin magnetik** dalam tabel parameter utama diperlukan. Dua parameter ini mungkin perlu dimodifikasi saat menggunakan board driver motor empat jalur.

Jika Anda membeli motor 310 sendiri, Anda akan menerima kabel PH2.0-6PIN ke DuPont. Saat menghubungkan board driver 4-channel, hubungkan ke soket IO-nya.

![img](C:/Users/hardware/Documents/Yahboom 4channel-motor-driver-encoder/assets/7.png)

![img](https://www.yahboom.net/public/upload/upload-html/1740571311/8.png)

Instruksi perkabelan motor 310:

Ketika fase A motor 310 terhubung ke fase A board driver motor 4-channel, dan fase B terhubung ke fase B, maka saat mengkonfigurasi tipe motor, Anda harus memilih `$mtype:2#`, model motor 310.

![img](C:/Users/hardware/Documents/Yahboom 4channel-motor-driver-encoder/assets/9.png)

 

Jika Anda membeli motor 310 dalam kit chassis, motor ini memiliki kabel double-ended PH2.0-6PIN. Anda dapat menghubungkan ujung hitam ke motor 310 dan ujung putih ke interface motor encoder PH2.0-6PIN pada board driver motor 4-channel.

Pada saat ini, pilih `$mtype:2#` untuk mengkonfigurasi tipe motor, yaitu model motor 310.

 

![img](C:/Users/hardware/Documents/Yahboom 4channel-motor-driver-encoder/assets/10.png)

![img](C:/Users/hardware/Documents/Yahboom 4channel-motor-driver-encoder/assets/10.1.png)

![img](C:/Users/hardware/Documents/Yahboom 4channel-motor-driver-encoder/assets/10.2.png)

## 3. Motor TT DC

![img](C:/Users/hardware/Documents/Yahboom 4channel-motor-driver-encoder/assets/11.png)

| Parameter                 | Nilai/Deskripsi |
| ------------------------- | --------------- |
| Model                     | Motor gear TT   |
| Material sikat            | Sikat karbon    |
| Rasio reduksi             | 1:48            |
| Tegangan rated            | 6V              |
| Arus idle                 | 200MA           |
| Arus stall                | 1.5A            |
| Torsi                     | 0.8N.m          |
| Kecepatan sebelum reduksi | 12000±10%rpm    |
| Kecepatan setelah reduksi | 245±10%rpm      |

Catu daya yang direkomendasikan: **7.4V**

Motor ini tidak memiliki encoder, jadi Anda hanya perlu memodifikasi **tipe motor** dan **rasio reduksi** di board driver motor empat jalur. Saat mengkonfigurasi tipe motor, pilih `$mtype:4#`, model motor TT tanpa encoder.

Perkabelan yang direkomendasikan: Hubungkan interface XH2.54-2PIN pada motor TT langsung ke soket XH2.54-2PIN pada board driver motor 4-channel.

![img](C:/Users/hardware/Documents/Yahboom 4channel-motor-driver-encoder/assets/12.png)

 

![img](C:/Users/hardware/Documents/Yahboom 4channel-motor-driver-encoder/assets/13.png)

 

 

## 4. Motor TT dengan pengukuran kecepatan encoder

![img](C:/Users/hardware/Documents/Yahboom 4channel-motor-driver-encoder/assets/14.png)

| Parameter                          | Nilai/Deskripsi                                              |
| ---------------------------------- | ------------------------------------------------------------ |
| Model                              | Motor TT poros tunggal logam 13-kawat                        |
| Tipe motor                         | Motor 130                                                    |
| Tipe motor/material sikat          | Sikat tembaga                                                |
| Rasio reduksi                      | 1:45                                                         |
| Tegangan rated                     | 6V                                                           |
| Arus tanpa beban                   | 0.08A                                                        |
| Arus rated                         | 0.3A                                                         |
| Arus stall                         | 1.1A                                                         |
| Torsi                              | 1.2N.m                                                       |
| Kecepatan sebelum reduksi          | 16000±5%rpm                                                  |
| Kecepatan setelah reduksi          | 355±5%rpm                                                    |
| Tipe encoder                       | Encoder fase AB Hall                                         |
| Catu daya encoder                  | 3.3-5V                                                       |
| Jumlah garis encoder               | 13 garis                                                     |
| Hitungan maksimum per putaran roda | 2340                                                         |
| Fitur                              | Dengan pembentukan pull-up built-in, MCU dapat membaca langsung |

Catu daya yang direkomendasikan: **7.4V**. Dapat dihubungkan ke 5~13V, **direkomendasikan menggunakan supply tegangan 7.4V**.

Dua parameter **rasio reduksi dan jumlah garis encoder** dalam tabel parameter utama diperlukan. Dua parameter ini mungkin perlu dimodifikasi saat menggunakan board driver motor 4-channel.

Perkabelan yang direkomendasikan: Gunakan kabel PH2.0-6PIN ke kabel Dupont dan hubungkan ke soket IO board driver motor 4-channel.

![img](C:/Users/hardware/Documents/Yahboom 4channel-motor-driver-encoder/assets/7-1761613091410-8.png)

![img](C:/Users/hardware/Documents/Yahboom 4channel-motor-driver-encoder/assets/8.png)

Instruksi perkabelan untuk motor TT pengukuran kecepatan encoder:

Ketika fase A motor TT encoder terhubung ke fase A board driver motor empat jalur, dan fase B terhubung ke fase B, maka saat mengkonfigurasi tipe motor, Anda harus memilih `$mtype:3#`, model motor TT dengan encoder.

![img](C:/Users/hardware/Documents/Yahboom 4channel-motor-driver-encoder/assets/15.png)

## 5. Motor 520 tipe-L

![img](C:/Users/hardware/Documents/Yahboom 4channel-motor-driver-encoder/assets/17.png)

| Parameter             | Nilai/Deskripsi  |
| --------------------- | ---------------- |
| Model                 | Motor 520 tipe-L |
| Tegangan starting     | 6V               |
| Tegangan rated        | 12V              |
| Rasio reduksi         | 1:40             |
| Jumlah loop magnetik  | 11线             |
| Arus tanpa beban      | ≥450mA           |
| Kecepatan tanpa beban | 300r/min±5%      |
| Torsi rated           | 4.4KG.CM         |
| Kecepatan rated       | 150r/min         |
| Torsi stall           | 10KG.CM          |
| Arus stall            | 4A               |

Catu daya yang direkomendasikan: **12V**.

Dua parameter **rasio reduksi dan jumlah garis encoder** dalam tabel parameter utama diperlukan. Dua parameter ini mungkin perlu dimodifikasi saat menggunakan board driver motor 4-channel.

Perkabelan yang direkomendasikan: Motor 520 tipe-L yang dibeli akan dilengkapi dengan dua jenis kabel. Di sini kami merekomendasikan agar Anda memilih kabel double-headed PH2.0-6PIN hitam, satu ujung terhubung ke motor, dan ujung lainnya langsung terhubung ke interface motor encoder PH2.0-6PIN pada board driver motor 4-channel. 

Perkabelan ini adalah yang paling nyaman, tetapi dapat ditemukan bahwa A pada motor sesuai dengan fase B board driver motor 4-channel. Oleh karena itu, saat mengkonfigurasi tipe motor pada board driver motor 4-channel, Anda harus memilih `$mtype:1#`, model motor 520.

![img](https://www.yahboom.net/public/upload/upload-html/1740571311/3.png)![img](C:/Users/hardware/Documents/Yahboom 4channel-motor-driver-encoder/assets/4.png)

Instruksi perkabelan motor 520 tipe-L:

Jika Anda menggunakan koneksi PH2.0-6PIN ke kabel Dupont, Anda dapat menghubungkan sesuai dengan gambar di bawah ini. Dengan koneksi ini, fase A motor akan terhubung ke fase A board driver motor 4-channel, dan fase B akan terhubung ke fase B. 

Namun, saat mengkonfigurasi tipe motor, Anda harus memilih `$mtype:2#`, model motor 310.

![img](C:/Users/hardware/Documents/Yahboom 4channel-motor-driver-encoder/assets/5-1761612922479-53.png)

## 1.PC host

# Komunikasi Serial

## 1.1 Penjelasan

**Harap baca 《0. Pengenalan dan penggunaan motor》 terlebih dahulu untuk memahami parameter motor, metode perkabelan, dan tegangan catu daya yang saat ini Anda gunakan. Untuk menghindari operasi yang tidak tepat dan kerusakan pada board driver atau motor.**

Hubungkan board driver ke komputer melalui port TYPE-C pada board driver, dan gunakan asisten port serial untuk mengirim perintah ke board driver untuk kontrol dan pembacaan data.

##### Perkabelan perangkat keras:

| **Motor** | **Board driver motor 4-channel**(Motor) |
| :-------: | :-------------------------------------: |
|    M2     |                   M-                    |
|     V     |                   3V3                   |
|     A     |                   H1A                   |
|     B     |                   H1B                   |
|     G     |                   GND                   |
|    M1     |                   M+                    |

 

## 1.2 Instruksi

Buka software asisten port serial di komputer. Di sini kita mengambil Uart Assistant sebagai contoh.

![image-20250218145905154](C:/Users/hardware/Documents/Yahboom 4channel-motor-driver-encoder/assets/1-1761604274918-25.png)

 

Konfigurasi port serial: **Baud rate 115200, tanpa pemeriksaan paritas, tanpa kontrol aliran perangkat keras, 1 stop bit**

Setelah konfigurasi, Anda dapat mengirim perintah di jendela kirim di bawah untuk mengontrol board driver. Semua perintah port serial dan penjelasan tercantum dalam kursus《1.2 Perintah kontrol》.

Selanjutnya, kami akan mendemonstrasikan cara memodifikasi parameter default untuk menggunakan **motor 310, ban diameter 48mm**.

![img](C:/Users/hardware/Documents/Yahboom 4channel-motor-driver-encoder/assets/2-1761604274919-26.png)

Pertama, keluarkan perintah `$read_flash#`, yang digunakan untuk query parameter penyimpanan power-off di flash. Ini dapat menyimpan tipe ban, zona mati motor, garis fase motor, rasio reduksi motor, diameter roda, dan parameter PID motor.

Kemudian, sesuai dengan parameter motor dan ban, masukkan perintah konfigurasi parameter kirim di kolom kirim di bawah.

![img](C:/Users/hardware/Documents/Yahboom 4channel-motor-driver-encoder/assets/3-1761604274919-27.png)

![img](C:/Users/hardware/Documents/Yahboom 4channel-motor-driver-encoder/assets/4-1761604274919-28.png)

Kita dapat melihat bahwa setelah setiap perintah konfigurasi dikeluarkan, board driver akan mengirim kembali pesan 'OK!', menunjukkan bahwa pengaturan berhasil. Terakhir, gunakan perintah untuk melihat flash untuk melihat bahwa parameter yang baru saja dimodifikasi telah berlaku. Metode modifikasi parameter PID sama dengan ini, tetapi umumnya tidak perlu dimodifikasi, jadi tidak akan didemonstrasikan di sini.

Jika Anda ingin mengontrol gerakan motor, kirim perintah `$spd:0,0,0,0#` atau `$pwm:0,0,0,0#`. Perintah spd mengontrol motor dengan encoder, dan perintah pwm dapat mengontrol motor dengan atau tanpa encoder. Misalkan saya ingin mengontrol motor 310 yang dicolokkan ke Motor1 pada board driver, yang memiliki encoder, maka kirim `$spd:100,0,0,0#` untuk mengontrolnya. Untuk mengontrol motor yang terhubung ke Motor2, modifikasi nilai kedua: `$spd:0,100,0,0#`.

## Referensi:

- https://www.yahboom.net/study/Quad-MD-Module

- https://github.com/YahboomTechnology/4-Channel-Motor-Drive-Module

  