# Selamat Datang di Repositori Modul Driver Motor 4-Channel

## 1.1 Pengenalan Board Driver Motor 4-Channel

# Pengenalan Board Driver Motor 4-Channel

![image-20251028052746916](./assets/image-20251028052746916.png)

### Pengenalan Produk:

Modul driver motor encoder 4-channel mengintegrasikan koprosesor chip tunggal berkinerja tinggi, yang dapat terhubung dengan mulus dengan berbagai kontroler seperti MSPM0, STM32, Raspberry Pi dan Jetson melalui komunikasi port serial atau IIC, menyederhanakan proses penggerak.

Hanya membutuhkan empat kabel penghubung untuk mencapai komunikasi efisien dengan unit kontrol utama untuk dengan mudah mengontrol motor dan mendapatkan data encoder, mengurangi jumlah kabel dan mengurangi kesulitan operasi.

Pada saat yang sama, mendukung penggerak sebagian besar motor TT encoder Hall, motor reduksi DC 520/310 dan lainnya di pasaran.

### Tabel Parameter:

| Spesifikasi Teknis                    |            Parameter             |
| :------------------------------------ | :------------------------------: |
| Tegangan Input yang Direkomendasikan  |              5-12v               |
| Arus DC untuk Pin 5v                  |               0.7A               |
| Arus DC untuk Pin 3.3v                |              500ma               |
| Arus penggerak berkelanjutan motor tunggal | Default 4A (output maksimum 5.5A) |
| Panjang * Lebar * Tinggi              |         56 * 65 * 13.4mm         |
| Interface motor encoder               |  PH2.0-6PIN、soket kabel Dupont  |
| Interface motor DC                    |           XH2.54-2PIN            |

## 4 interface motor pada modul sesuai dengan motor pada mobil robot, seperti ditunjukkan di bawah ini

M1 -> Motor kiri atas (roda depan kiri mobil) M2 -> Motor kiri bawah (roda belakang kiri mobil) M3 -> Motor kanan atas (roda depan kanan mobil) M4 -> Motor kanan bawah (roda belakang kanan mobil)

## Konfigurasi Port Serial

**Baud rate 115200, tanpa paritas, tanpa kontrol aliran perangkat keras, 1 stop bit**

 

### 1.Konfigurasi Tipe Motor

|  Perintah  | Penjelasan  |  Contoh   |            Keterangan            | Default Firmware | Simpan saat mati |
| :-------: | :---------: | :-------: | :--------------------------: | :---------------: | :------------: |
| $mtype:x# | Model motor | $mtype:1# | Model motor adalah motor 520 |     Motor 520     |       Y        |
|   Catatan    |             |           |                              |                   |                |

1. Pemilihan tipe motor. Jika encoder motor A terhubung ke port A board, maka B terhubung ke B. Anda perlu memilih model motor 310. Jika tidak, Anda perlu memilih motor 520 atau motor TT.
2. Perintah dapat dikirim dalam huruf besar atau kecil semua.
3. Jika perintah di atas berhasil, akan mengembalikan pesan **perintah+OK**. Jika tidak ada pesan yang dikembalikan, periksa koneksi port serial.
4. x: adalah tipe motor. Tipe motor yang diwakili oleh nilai yang berbeda adalah sebagai berikut: 1: motor 520 2: motor 310 3: motor TT (dengan encoder) 4: motor TT (tanpa encoder)

Catatan: Jika Anda menggunakan motor tanpa encoder, Anda dapat memilih tipe 4, yaitu perintahnya adalah: $mtype:4# Jika Anda menggunakan motor dengan encoder, Anda dapat memilih salah satu dari 1, 2, dan 3.

### 2.Konfigurasi Deadband Motor

|     Perintah     |               Penjelasan               |     Contoh     |                            Keterangan                            | Default Firmware | Simpan saat mati |
| :-------------: | :-------------------------------------: | :-------------: | :----------------------------------------------------------: | :---------------: | :------------: |
| $deadzone:xxxx# | Konfigurasi zona mati pulsa pwm motor | $deadzone:1650# | Saat mengontrol PWM, nilai zona mati akan ditambahkan secara default sehingga motor tidak akan memiliki area osilasi. |       1600        |       Y        |
|      Catatan       |                                         |                 |                                                              |                   |                |

1. Perintah dapat dikirim dalam huruf besar atau kecil semua
2. Jika perintah di atas berhasil, akan mengembalikan pesan **perintah+OK**. Jika tidak ada pesan yang dikembalikan, periksa koneksi port serial
3. xxxx: adalah nilai zona mati, yang perlu diukur. Dengan mengubah nilai ini, getaran minimum motor dapat dihilangkan
4. Rentang nilai zona mati (0-3600)

### 3.Konfigurasi Garis Fase Motor

|  Perintah   |           Penjelasan           |  Contoh   |                          Keterangan                           | Default Firmware | Simpan saat mati |
| :--------: | :-----------------------------: | :--------: | :-------------------------------------------------------: | :---------------: | :------------: |
| $mline:xx# | Konfigurasi garis fase motor | $mline:13# | Konfigurasi fase encoder Hall motor menjadi 13 garis |        11         |       Y        |
|    Catatan    |                                 |            |                                                           |                   |                |

1. Perintah dapat dikirim dalam huruf besar atau kecil semua
2. Perintah di atas akan mengembalikan informasi **perintah+OK** jika berhasil. Jika tidak ada informasi yang dikembalikan, periksa koneksi port serial
3. xx: Ini adalah fase encoder Hall untuk satu putaran. Nilai ini perlu diperoleh dengan memeriksa tabel parameter motor dari pedagang
4. Untuk motor dengan encoder: Nilai ini memainkan **peran utama** dalam mengontrol kecepatan. Nilai ini harus benar
5. Motor tanpa encoder: Konfigurasi nilai ini dapat diabaikan

### 4.Konfigurasi Rasio Reduksi Motor

|   Perintah   |             Penjelasan             |   Contoh   |                  Keterangan                   | Default Firmware | Simpan saat mati |
| :---------: | :---------------------------------: | :---------: | :---------------------------------------: | :---------------: | :------------: |
| $mphase:xx# | Konfigurasi rasio reduksi motor | $mphase:40# | Konfigurasi rasio reduksi motor menjadi 40 |        30         |       Y        |
|  **Catatan**   |                                     |             |                                           |                   |                |

1. Perintah dapat dikirim dalam huruf besar atau kecil semua
2. Perintah di atas akan mengembalikan informasi **perintah+OK** jika berhasil. Jika tidak ada informasi yang dikembalikan, periksa koneksi port serial
3. xx: Ini adalah parameter rasio reduksi motor. Nilai ini perlu diperoleh dengan memeriksa tabel parameter motor dari pedagang
4. Untuk motor dengan encoder: Nilai ini memainkan **peran utama** dalam mengontrol kecepatan. Nilai ini harus benar
5. Motor tanpa encoder: Konfigurasi nilai ini dapat diabaikan

### 5.Konfigurasi Diameter Roda (Opsional)

|    Perintah     |         Penjelasan          |    Contoh     |              Keterangan               | Default Firmware | Simpan saat mati |
| :------------: | :--------------------------: | :------------: | :-------------------------------: | :---------------: | :------------: |
| $wdiameter:xx# | Konfigurasi diameter roda | $wdiameter:50# | Diameter roda adalah 50mm |       67 mm       |       Y        |
|    **Catatan**    |                              |                |                                   |                   |                |

1. Perintah dapat dikirim dalam huruf besar atau kecil semua
2. Perintah di atas akan mengembalikan informasi **perintah+OK** jika berhasil. Jika tidak ada informasi yang dikembalikan, periksa koneksi port serial
3. xx: Ini adalah diameter roda. Nilai ini dapat diukur atau diperoleh menggunakan informasi pedagang
4. Untuk motor dengan encoder: Nilai ini memainkan **peran utama** dalam mengontrol kecepatan. Nilai ini harus benar dalam milimeter (mm); jika nilai ini salah, hanya akan mempengaruhi data kecepatan yang tidak akurat, dan tidak akan mempengaruhi data encoder
5. Motor tanpa encoder: Konfigurasi nilai ini dapat diabaikan

### 6.Konfigurasi Parameter PID untuk Kontrol Motor

|        Perintah        |       Penjelasan        |       Contoh       |                           Keterangan                           | Default Firmware  | Simpan saat mati |
| :-------------------: | :----------------------: | :-----------------: | :--------------------------------------------------------: | :----------------: | :------------: |
| $MPID:x.xx,x.xx,x.xx# | Konfigurasi parameter PID | $MPID:1.5,0.03,0.1# | Konfigurasi kontrol kecepatan adalah P: 1.5, I: 0.03, D: 0.1 | P:0.8 I:0.06 D:0.5 |       Y        |
|       **Catatan**        |                          |                     |                                                            |                    |                |

1. Perintah dapat dikirim dalam huruf besar atau kecil semua
2. Perintah di atas akan mengembalikan **perintah+OK** jika berhasil. Jika tidak ada informasi yang dikembalikan, periksa koneksi port serial
3. x.xx, x.xx, x.xx: Ini adalah parameter untuk mengontrol motor p, i, d masing-masing. **Setiap kali nilai diubah, chip akan restart dan menghentikan motor yang bergerak. Ini adalah situasi normal**
4. Untuk motor dengan encoder: parameter pid valid, dan nilai ini harus benar. **Umumnya, tidak perlu memodifikasi pid, dan nilai default dapat digunakan**
5. Motor tanpa encoder: parameter pid tidak valid, dan konfigurasi nilai ini dapat diabaikan

### 7.Reset Semua Variabel ke Nilai Default

|    Perintah    |          Penjelasan           | Contoh | Keterangan | Default Firmware | Simpan saat mati |
| :-----------: | :----------------------------: | :-----: | :----: | :---------------: | :------------: |
| $flash_reset# | Kembalikan nilai default pabrik |    -    |   -    |         -         |       -        |
|   **Catatan**    |                                |         |        |                   |                |

1. Perintah dapat dikirim dalam huruf besar atau kecil semua
2. Jika perintah di atas berhasil, akan mengembalikan pesan **perintah+OK**. Jika tidak ada pesan yang dikembalikan, periksa koneksi port serial
3. Eksekusi perintah ini dan modul akan restart sekali

### 8.Perintah Kontrol Kecepatan

|    Perintah    |          Penjelasan          |       Contoh       |                         Keterangan                          | Default Firmware | Simpan saat mati |
| :-----------: | :---------------------------: | :-----------------: | :-----------------------------------------------------: | :---------------: | :------------: |
| $spd:0,0,0,0# | Kontrol kecepatan 4 motor | $spd:100,-100,0,50# | Kontrol kecepatan 4 motor M1:100 M2:-100 M3:0 M4:50 |         -         |       N        |
|   **Catatan**    |                               |                     |                                                         |                   |                |

1. Perintah dapat dikirim dalam huruf besar atau kecil semua
2. Jika perintah di atas berhasil, akan mengembalikan pesan **perintah+OK**. Jika tidak ada pesan yang dikembalikan, periksa koneksi port serial
3. Untuk motor dengan encoder: perintah ini berfungsi untuk mengontrol kecepatan motor
4. Motor tanpa encoder: perintah ini tidak valid
5. Perintah kontrol motor tidak perlu dikirim berulang kali; cukup kirim sekali, dan modul akan mengontrol motor menurut kecepatan yang ditetapkan, hingga perintah kontrol kecepatan baru diterima atau perintah berhenti dikirim.

Catatan: Setelah perintah ini dikirim, encoder atau data kecepatan akan secara otomatis dikirim balik menurut perintah yang telah dikonfigurasi sebelumnya.

### 9.Perintah Kontrol PWM

|    Perintah    |          Penjelasan          |       Contoh        |                         Keterangan                         | Default Firmware | Simpan saat mati |
| :-----------: | :---------------------------: | :------------------: | :----------------------------------------------------: | :---------------: | :------------: |
| $pwm:0,0,0,0# | Kontrol 4 motor dengan nilai PWM | $pwm:1000,-1000,0,500# | Kontrol 4 motor dengan nilai PWM M1:1000 M2:-1000 M3:0 M4:500 |         -         |       N        |
|   **Catatan**    |                               |                      |                                                        |                   |                |

1. Perintah dapat dikirim dalam huruf besar atau kecil semua
2. Jika perintah di atas berhasil, akan mengembalikan pesan **perintah+OK**. Jika tidak ada pesan yang dikembalikan, periksa koneksi port serial
3. Untuk motor dengan encoder: perintah ini berfungsi untuk mengontrol nilai PWM motor; karena adanya encoder, kecepatan motor dapat dibaca secara real time.
4. Motor tanpa encoder: perintah ini berfungsi untuk mengontrol nilai PWM motor; karena tidak ada encoder, kecepatan motor tidak dapat dibaca. Perlu dicatat bahwa motor dengan dan tanpa encoder menggunakan cara berbeda untuk mengontrol motor. Perintah kontrol motor tanpa encoder adalah PWM.
5. Perintah kontrol motor tidak perlu dikirim berulang kali; cukup kirim sekali, dan modul akan mengontrol motor menurut nilai pwm yang ditetapkan, hingga perintah kontrol pwm baru diterima atau perintah berhenti dikirim.

### 10.Perintah Berhenti

| Perintah |       Penjelasan       | Contoh | Keterangan | Default Firmware | Simpan saat mati |
| :------: | :--------------------: | :----: | :--------: | :---------------: | :------------: |
| $stop:x# | Berhentikan semua motor | $stop:1# |     -      |         -         |       N        |
| **Catatan** |                        |        |            |                   |                |

1. Perintah dapat dikirim dalam huruf besar atau kecil semua
2. Jika perintah di atas berhasil, akan mengembalikan pesan **perintah+OK**. Jika tidak ada pesan yang dikembalikan, periksa koneksi port serial
3. x: adalah angka acak apa pun, bisa bilangan desimal atau bilangan bulat

### 11.Perintah Baca Data Encoder

|   Perintah    |             Penjelasan             |   Contoh   |                          Keterangan                          | Default Firmware | Simpan saat mati |
| :----------: | :--------------------------------: | :--------: | :----------------------------------------------------------: | :---------------: | :------------: |
| $encoder:x:y# | Kontrol feedback encoder yang dikirim balik | $encoder:1:2# | Menyiapkan untuk mengembalikan kumulasi total encoder encoder setiap 100ms |         -         |       N        |
|  **Catatan**   |                                    |           |                                                              |                   |                |

1. Perintah dapat dikirim dalam huruf besar atau kecil semua
2. Jika perintah di atas berhasil, akan mengembalikan pesan **perintah+OK**. Jika tidak ada pesan yang dikembalikan, periksa koneksi port serial
3. x: adalah kontrol feedback dari encoder
   - 0: tidak mengembalikan
   - 1: mengembalikan kumulasi total encoder (mengembalikan: $MAll:xxx,xxx,xxx,xxx#)
   - 2: mengembalikan perubahan encoder real-time setiap 10ms (mengembalikan: $MTEP:xxx,xxx,xxx,xxx#)
4. y: adalah waktu pengembalian data (satuan milidetik ms)
   - 0: tidak mengembalikan
   - (1~2000): mengembalikan setiap 1~2000 milidetik. Misalnya: 2 mewakili pengembalian data setiap 2ms

Catatan: Perintah ini berlaku untuk motor dengan dan tanpa encoder. Jika motor tidak memiliki encoder, nilai yang dikembalikan akan selalu 0.

**Format pengembalian kumulasi total encoder adalah:** $MAll:xxx,xxx,xxx,xxx#

**Format pengembalian perubahan encoder real-time setiap 10ms adalah:** $MTEP:xxx,xxx,xxx,xxx#

**Prinsip pengembalian adalah:**

Misalnya, perintah yang Anda kirim adalah: $encoder:1:100#, maka arti pengembaliannya adalah: pengembalian kumulasi total encoder dilakukan setiap 100 milidetik, yaitu pengembalian dilakukan setiap 100ms, dan hanya memicu 10 kali dalam 1 detik.

Kumulasi total encoder pengembalian data:

Misalnya: $MAll:12,25,-10,50# M1: 12 M2: 25 M3: -10 M4: 50

Pengembalian data perubahan encoder real-time setiap 10ms:

Misalnya: $MTEP:12,25,-10,50# M1: 12 M2: 25 M3: -10 M4: 50

### 12.Perintah Membaca Data Kecepatan

|  Perintah   |              Penjelasan               |  Contoh   |                         Keterangan                         | Default Firmware | Simpan saat mati |
| :--------: | :------------------------------------: | :-------: | :--------------------------------------------------------: | :---------------: | :------------: |
| $speed:x:y# | Kontrol feedback kecepatan yang dikirim balik | $speed:1:100# | Menyiapkan untuk mengembalikan kecepatan motor real-time setiap 100ms |         -         |       N        |
| **Catatan**  |                                        |          |                                                            |                   |                |

1. Perintah dapat dikirim dalam huruf besar atau kecil semua
2. Jika perintah di atas berhasil, akan mengembalikan pesan **perintah+OK**. Jika tidak ada pesan yang dikembalikan, periksa koneksi port serial
3. x: adalah kontrol feedback dari kecepatan
   - 0: tidak mengembalikan
   - 1: mengembalikan kecepatan motor real-time (mengembalikan: $MSPD:xxx,xxx,xxx,xxx#)
4. y: adalah waktu pengembalian data (satuan milidetik ms)
   - 0: tidak mengembalikan
   - (1~2000): mengembalikan setiap 1~2000 milidetik. Misalnya: 2 mewakili pengembalian data setiap 2ms

**Format pengembalian kecepatan motor real-time adalah:** $MSPD:xxx,xxx,xxx,xxx#

Catatan:

1. Perintah ini berlaku untuk motor dengan encoder atau tanpa encoder. Untuk motor dengan encoder, kecepatan yang dikembalikan dapat dihitung oleh encoder. Untuk motor tanpa encoder, jika perintah kontrol PWM sebelumnya adalah $pwm:200,0,500,100#, maka pengembalian kecepatan juga akan sesuai dengan nilai pwm, yaitu $MSPD:200,0,500,100#
2. **Data yang dikembalikan mewakili mm/s, yang merupakan data kecepatan dalam satuan milimeter per detik**.

**Prinsip pengembalian adalah:**

Misalnya, perintah yang Anda kirim adalah: $speed:1:100#, maka arti pengembaliannya adalah: pengembalian data kecepatan dilakukan setiap 100 milidetik, yaitu pengembalian dilakukan setiap 100ms, dan hanya memicu 10 kali dalam 1 detik.

Pengembalian data kecepatan motor real-time:

Misalnya: $MSPD:100,250,0,180# M1: 100 mm/s M2: 250 mm/s M3: 0 mm/s M4: 180 mm/s

### 13.Mereset Encoder Kembali ke 0

|  Perintah   |          Penjelasan           | Contoh | Keterangan | Default Firmware | Simpan saat mati |
| :--------: | :----------------------------: | :----: | :--------: | :---------------: | :------------: |
| $encRst:x# | Mereset kumulasi encoder kembali ke 0 | $encRst:1# |     -      |         -         |       N        |
| **Catatan** |                                |        |            |                   |                |

1. Perintah dapat dikirim dalam huruf besar atau kecil semua
2. Jika perintah di atas berhasil, akan mengembalikan pesan **perintah+OK**. Jika tidak ada pesan yang dikembalikan, periksa koneksi port serial
3. x: adalah angka acak apa pun, bisa bilangan desimal atau bilangan bulat

### 14.Membaca Nilai Parameter Board

|  Perintah  |         Penjelasan          | Contoh | Keterangan | Default Firmware | Simpan saat mati |
| :-------: | :-------------------------: | :----: | :--------: | :---------------: | :------------: |
| $Rvalue:x# | Membaca berbagai nilai parameter | $Rvalue:1# |     -      |         -         |       N        |
| **Catatan** |                             |        |            |                   |                |

1. Perintah dapat dikirim dalam huruf besar atau kecil semua
2. Jika perintah di atas berhasil, akan mengembalikan pesan **perintah+OK**. Jika tidak ada pesan yang dikembalikan, periksa koneksi port serial
3. x: adalah angka acak apa pun, bisa bilangan desimal atau bilangan bulat

Format pengembalian: $mtype,deadzone,mline,mphase,wdiameter,Px.xx,Ix.xx,Dx.xx,batValue#

Contoh: $3,1650,11,30,67,P0.8,I0.06,D0.5,12.5#

$

mtype: tipe motor 3 (motor TT dengan encoder)

deadzone: zona mati motor 1650

mline: fase encoder Hall motor 11

mphase: rasio reduksi motor 30

wdiameter: diameter roda 67

Px.xx: parameter p 0.8 untuk kontrol pid

Ix.xx: parameter i 0.06 untuk kontrol pid

Dx.xx: parameter d 0.5 untuk kontrol pid

batValue: tegangan baterai 12.5V

#

Catatan: Setiap kali data dikembalikan, nilainya akan dimulai dengan $ dan diakhiri dengan #.

### 15.Membaca Nilai Tegangan Baterai

|   Perintah   |            Penjelasan             | Contoh | Keterangan | Default Firmware | Simpan saat mati |
| :---------: | :-------------------------------: | :----: | :--------: | :---------------: | :------------: |
| $batRead:x# | Membaca tegangan baterai board saat ini | $batRead:1# |     -      |         -         |       N        |
|  **Catatan**  |                                   |        |            |                   |                |

1. Perintah dapat dikirim dalam huruf besar atau kecil semua
2. Jika perintah di atas berhasil, akan mengembalikan pesan **perintah+OK**. Jika tidak ada pesan yang dikembalikan, periksa koneksi port serial
3. x: adalah angka acak apa pun, bisa bilangan desimal atau bilangan bulat

Format pengembalian: $bat:xx.x#

Contoh: $bat:11.2#

$

bat: tegangan baterai 11.2V

#

Catatan: Setiap kali data dikembalikan, nilainya akan dimulai dengan $ dan diakhiri dengan #.

## Konfigurasi IIC

Alamat IIC: 0x55

Jika modul driver motor telah dikonfigurasi dengan benar melalui komunikasi serial port (motor telah dikonfigurasi dengan benar), Anda dapat langsung menggunakan komunikasi IIC.

### Pengenalan Alamat Register IIC

**Konfigurasi PWM motor:**

| Alamat Register |     Nama Register      | Baca/Tulis | Panjang Data | Nilai Default |
| :-------------: | :--------------------: | :--------: | :----------: | :-----------: |
|      0x00       |  Nilai PWM motor M1    |     R/W    |      2       |       0       |
|      0x02       |  Nilai PWM motor M2    |     R/W    |      2       |       0       |
|      0x04       |  Nilai PWM motor M3    |     R/W    |      2       |       0       |
|      0x06       |  Nilai PWM motor M4    |     R/W    |      2       |       0       |

**Membaca encoder motor:**

| Alamat Register |          Nama Register           | Baca/Tulis | Panjang Data | Nilai Default |
| :-------------: | :------------------------------: | :--------: | :----------: | :-----------: |
|      0x20       | Data encoder motor kumulatif M1 |     R      |      4       |       0       |
|      0x24       | Data encoder motor kumulatif M2 |     R      |      4       |       0       |
|      0x28       | Data encoder motor kumulatif M3 |     R      |      4       |       0       |
|      0x2c       | Data encoder motor kumulatif M4 |     R      |      4       |       0       |

**Membaca kecepatan motor:**

| Alamat Register |   Nama Register    | Baca/Tulis | Panjang Data | Nilai Default |
| :-------------: | :----------------: | :--------: | :----------: | :-----------: |
|      0x30       | Data kecepatan motor M1 |     R      |      4       |       0       |
|      0x34       | Data kecepatan motor M2 |     R      |      4       |       0       |
|      0x38       | Data kecepatan motor M3 |     R      |      4       |       0       |
|      0x3c       | Data kecepatan motor M4 |     R      |      4       |       0       |

**Reset encoder:**

| Alamat Register |    Nama Register     | Baca/Tulis | Panjang Data | Nilai Default |
| :-------------: | :------------------: | :--------: | :----------: | :-----------: |
|      0x40       | Reset encoder kembali ke 0 |     W      |      1       |       0       |

**Konfigurasi kecepatan motor:**

| Alamat Register |    Nama Register     | Baca/Tulis | Panjang Data | Nilai Default |
| :-------------: | :------------------: | :--------: | :----------: | :-----------: |
|      0x50       | Nilai kecepatan motor M1 |     R/W    |      2       |       0       |
|      0x52       | Nilai kecepatan motor M2 |     R/W    |      2       |       0       |
|      0x54       | Nilai kecepatan motor M3 |     R/W    |      2       |       0       |
|      0x56       | Nilai kecepatan motor M4 |     R/W    |      2       |       0       |

**Berhentikan motor:**

| Alamat Register | Nama Register  | Baca/Tulis | Panjang Data | Nilai Default |
| :-------------: | :------------: | :--------: | :----------: | :-----------: |
|      0x60       | Berhentikan motor |     W      |      1       |       0       |

**Membaca tegangan baterai:**

| Alamat Register |   Nama Register    | Baca/Tulis | Panjang Data | Nilai Default |
| :-------------: | :----------------: | :--------: | :----------: | :-----------: |
|      0x70       | Tegangan baterai motor |     R      |      2       |       0       |

**Catatan:**

1. Register hanya dapat menulis data dengan alamat yang dapat ditulis (menunjukkan R/W dalam tabel di atas)
2. Register hanya dapat membaca data dengan alamat yang dapat dibaca (menunjukkan R atau R/W dalam tabel di atas)
3. Panjang data adalah jumlah byte data yang dapat dibaca atau ditulis
4. Karena enkoder total kumulatif diwakili oleh tipe int, encoder dapat negatif atau positif, dengan rentang data: -2147483648 hingga 2147483648
5. Encoder membaca dan menulis 4 byte, sehingga perlu ditulis dari byte rendah hingga tinggi, atau dibaca dari byte rendah hingga tinggi
6. Kecepatan motor membaca 4 byte, dan membaca dari byte rendah hingga tinggi

## 1.2 Demo Program

Hubungkan MSPM0L1306 dengan board driver motor, dan mainboard MSPM0L1306 dapat diperoleh dari repositori: https://github.com/johnsonqaq/yummy-robo

Jika Anda ingin mendapatkan boardnya, Anda dapat membeli dari tautan: https://www.tindie.com/products/35754/

### Kode Kontrol Motor

Program ini ditulis berdasarkan mainboard MSPM0L1306 (atau MSPM0G3507), Anda perlu menginstal perangkat lunak CCS sebelumnya untuk digunakan.

#### Folder program

Karena ada dukungan jaringan untuk repo github, di sini kami akan membuat tautan file jadi yang dapat Anda unduh.

Pada program di atas, perintah kontrol motor yang didukung untuk berkomunikasi dengan driver motor adalah sebagai berikut:

```
/*
Konfigurasi motor TT yang diuji digunakan:
$mtype:3# menginisialisasi tipe motor menjadi TT motor
$mline:11# mengatur fase encoder Hall menjadi 11
$mphase:30# mengatur rasio reduksi motor menjadi 30
$wdiameter:67# mengatur diameter roda menjadi 67mm
$deadzone:1650# mengatur deadzone motor menjadi 1650
$MPID:0.8,0.06,0.5# mengatur pid motor menjadi 0.8, 0.06, 0.5
$encoder:1:100# mengembalikan encoder total kumulatif, dengan siklus pengembalian 100ms
$encoder:2:10# mengembalikan perubahan encoder 10ms, dengan siklus pengembalian 10ms
$speed:1:100# mengembalikan kecepatan real-time, dengan siklus pengembalian 100ms
*/
void Init_motor(void)
{
    MY_UART_write("$mtype:3#");
    DELAY_ms(200);
    MY_UART_write("$mline:11#");
    DELAY_ms(200);
    MY_UART_write("$mphase:30#");
    DELAY_ms(200);
    MY_UART_write("$wdiameter:67#");
    DELAY_ms(200);
    MY_UART_write("$deadzone:1650#");
    DELAY_ms(200);
    MY_UART_write("$MPID:0.8,0.06,0.5#");
    DELAY_ms(500);
    MY_UART_write("$encoder:1:100#");
    DELAY_ms(200);
    MY_UART_write("$encoder:2:10#");
    DELAY_ms(200);
    MY_UART_write("$speed:1:100#");
    DELAY_ms(200);
}
```

Fungsi di atas adalah untuk menginisialisasi motor ke board driver motor, dan fungsi inisialisasi dapat disesuaikan sesuai kebutuhan. Catatan: jika Anda tidak ingin menginisialisasi setiap kali Anda menghidupkan, cukup ubah tipe motor dari driver motor, dan parameter lainnya akan secara otomatis disimpan.

Catatan khusus: untuk motor dengan tipe motor yang sama, Anda hanya perlu mengkonfigurasi sekali. Setelah konfigurasi berhasil, board driver motor akan menyimpan semua data secara otomatis dan masih valid setelah restart berikutnya. Untuk motor dengan tipe motor yang sama, tidak perlu mengkonfigurasi lagi.

Misalnya, beberapa catatan tentang perintah kontrol motor kecepatan adalah sebagai berikut:

```
/*
    Masuk: spd1, spd2, spd3, spd4 mewakili kecepatan 4 motor, masing-masing dalam satuan milimeter per detik (mm/s)
    spd1, spd2, spd3, spd4 adalah bilangan bulat, rentangnya adalah: -1000 ~ 1000
    Catatan: motor TT yang saya gunakan tidak memiliki kecepatan terlalu tinggi, jadi rentangnya dipilih dari -1000 hingga 1000; jika Anda menggunakan motor dengan kecepatan tinggi,
    Sesuaikan rentang nilai sesuai dengan kebutuhan Anda.
*/

void Control_motor_spd(int16_t spd1, int16_t spd2, int16_t spd3, int16_t spd4)
{
    static char buff[40] = {0};
    sprintf(buff, "$spd:%d,%d,%d,%d#", spd1, spd2, spd3, spd4);
    MY_UART_write(buff);
}
```

Misalnya, beberapa catatan tentang perintah kontrol motor PWM adalah sebagai berikut:

```
/*
    Masuk: pwm1, pwm2, pwm3, pwm4 mewakili nilai PWM dari 4 motor, yang berarti berapa nilai PWM
    pwm1, pwm2, pwm3, pwm4 adalah bilangan bulat, rentangnya adalah: -3600 ~ 3600
    Catatan: nilai nilai PWM yang didukung oleh driver motor adalah -3600 ~ 3600, jangan melebihi rentang nilai ini
*/
void Control_motor_pwm(int16_t pwm1, int16_t pwm2, int16_t pwm3, int16_t pwm4)
{
    static char buff[40] = {0};
    sprintf(buff, "$pwm:%d,%d,%d,%d#", pwm1, pwm2, pwm3, pwm4);
    MY_UART_write(buff);
}
```

Misalnya, pada program contoh ini, Anda dapat melihat fungsi beralih posisi mobil; ada dua jenis fungsi beralih posisi mobil: satu adalah fungsi beralih posisi mobil kecepatan; yang lain adalah fungsi beralih posisi mobil pwm:

```
//Fungsi kontrol posisi mobil yang berbeda dengan mode kontrol kecepatan
//Different car position control functions with speed control mode
void Motor_Control_State_Spd(uint8_t car_state)
{
    switch (car_state)
    {
        case STOP:
        {
            Control_motor_spd(0, 0, 0, 0);//berhenti  stop
            break;
        }
        case GO:
        {
            Control_motor_spd(300, 300, 300, 300);//maju Forward
            break;
        }
        case BACK:
        {
            Control_motor_spd(-300, -300, -300, -300);//mundur  Backward
            break;
        }
        case LEFT:
        {
            Control_motor_spd(-300, -300, 300, 300);//rotasi kiri Left rotation
            break;
        }
        case RIGHT:
        {
            Control_motor_spd(300, 300, -300, -300);//rotasi kanan  Right rotation
            break;
        }        
    }
}

//Fungsi kontrol posisi mobil yang berbeda dengan mode kontrol pwm
//Different car position control functions with PWM control mode
void Motor_Control_State_Pwm(uint8_t car_state)
{
    switch (car_state)
    {
        case STOP:
        {
            Control_motor_pwm(0, 0, 0, 0);//berhenti  stop
            break;
        }
        case GO:
        {
            Control_motor_pwm(2400, 2400, 2400, 2400);//maju Forward
            break;
        }
        case BACK:
        {
            Control_motor_pwm(-2400, -2400, -2400, -2400);//mundur  Backward
            break;
        }
        case LEFT:
        {
            Control_motor_pwm(-2400, -2400, 2400, 2400);//rotasi kiri Left rotation
            break;
        }
        case RIGHT:
        {
            Control_motor_pwm(2400, 2400, -2400, -2400);//rotasi kanan  Right rotation
            break;
        }        
    }
}
```

Program ini mendefinisikan 5 status mobil: berhenti, maju, mundur, rotasi kiri, dan rotasi kanan.

Dalam fungsi utama:

```
int main(void)
{
    SYSCFG_DL_init();
    NVIC_EnableIRQ(TIMER_0_INST_INT_IRQN);//Aktifkan interupsi timer untuk mengubah status mobil  Enable timer interrupt to change car status
    NVIC_EnableIRQ(UART_0_INST_INT_IRQN);//Aktifkan interrupsi port serial untuk menerima pesan dari driver motor  Enable serial port interrupt to receive messages from motor driver
    
    Delay_ms(2000);//Menunggu driver motor untuk menginisialisasi dengan benar  Wait for the motor driver to initialize correctly
    Init_motor();//Inisialisasi tipe motor driver motor, dan atur untuk mengubah data dari driver motor  Initialize the motor driver motor type and set up to change data from the motor driver

    
    while (1) 
    {
        //Jika tipe motor adalah 4, yaitu motor tanpa encoder, maka gunakan fungsi beralih status mobil versi pwm  If the motor type is 4, that is, the motor without encoder, then use the pwm version of the car state switching function
        if(g_motor_type == 4)
        {
            Motor_Control_State_Pwm(car_state);
        }
        //Jika motor memiliki encoder, gunakan fungsi beralih status mobil versi kecepatan  If the motor has an encoder, use the speed version of the car state switching function
        else
        {
            Motor_Control_State_Spd(car_state);
        }
        
        //Membaca data dari board driver motor dan mencetak  Read data from motor driver board and print
        if(g_recv_flag == 1)
        {
            g_recv_flag = 0;
            Deal_data_real();
            printf("$MAll:%d,%d,%d,%d# ",Encoder_Now[0],Encoder_Now[1],Encoder_Now[2],Encoder_Now[3]);
            printf("$MTEP:%d,%d,%d,%d# ",Encoder_Offset[0],Encoder_Offset[1],Encoder_Offset[2],Encoder_Offset[3]);
            printf("$MSPD:%.2f,%.2f,%.2f,%.2f# \r\n",g_Speed[0],g_Speed[1],g_Speed[2],g_Speed[3]);
        }
    }
}
```

Setelah memulai ulang mainboard, tunggu 2 detik untuk menginisialisasi chip driver motor, dan kemudian kirim perintah konfigurasi ke board driver motor.

```
//Timer 0: 100ms diaktifkan sekali  Timer 0: triggered once every 100ms
void TIMER_0_INST_IRQHandler(void)
{
    switch (DL_TimerG_getPendingInterrupt(TIMER_0_INST)) 
    {
        case DL_TIMER_IIDX_ZERO:
            times++;
            if(times >= 25)//2.5s
            {
                times = 0;
                car_state++;
                if(car_state > RIGHT)
                {
                    car_state = STOP;
                }
            }
            break;
        default:
            break;
    }
}
```

Timer 100ms diatur dalam program. Setiap kali interrupsi timer dipicu, variabel times akan bertambah satu. Ketika mencapai 25 kali, yaitu 2,5 detik, status gerakan mobil akan diubah.

Jika tipe motor adalah 4, yaitu motor tanpa encoder, maka fungsi beralih status mobil versi pwm digunakan. Pada saat yang sama, baca data yang dikirim oleh board driver dan cetak datanya sekaligus.

```
//Memeriksa data yang dikirim dari board driver, menyimpan data yang memenuhi protokol komunikasi
//Check the data sent from the driver board, and save the data that meets the communication protocol
void Deal_Control_Rxtemp(uint8_t rxtemp)
{
    static u16 step = 0;
    static u8 start_flag = 0;


    if(rxtemp == '$' &&     start_flag == 0)
    {
        start_flag = 1;
        memset(g_recv_buff,0,RXBUFF_LEN);//Bersihkan data Clear data
    }
    
    else if(start_flag == 1)
    {
            if(rxtemp == '#')
            {
                start_flag = 0;
                step = 0;
                g_recv_flag = 1;
                memcpy(g_recv_buff_deal,g_recv_buff,RXBUFF_LEN); //Hanya yang benar yang akan ditetapkan Only correct ones will be assigned
            }
            else
            {
                if(step > RXBUFF_LEN)
                {
                    start_flag = 0;
                    step = 0;
                    memset(g_recv_buff,0,RXBUFF_LEN);//Bersihkan data yang diterima   Clear received data
                }
                else
                {
                    g_recv_buff[step] = rxtemp;
                    step++;
                }
            }
    }
    
}


//Memformat data yang disimpan dari board driver, dan mempersiapkannya untuk dicetak
//Format the data saved from the driver board and prepare it for printing
void Deal_data_real(void)
{
    static uint8_t data[RXBUFF_LEN];
    uint8_t  length = 0;
    
    //Encoder keseluruhan    Overall encoder
     if ((strncmp("MAll",(char*)g_recv_buff_deal,4)==0))
    {
        length = strlen((char*)g_recv_buff_deal)-5;
        for (uint8_t i = 0; i < length; i++)
        {
            data[i] = g_recv_buff_deal[i+5]; //Hapus titik dua Remove the colon
        }  
                data[length] = '\0';    



                    
                char* strArray[10];//Array pointer Panjang didefinisikan oleh nomor pemisah char 1 byte char* 4 byte    Pointer array The length is defined by the split number char 1 byte char* 4 bytes
                char mystr_temp[4][10] = {'\0'}; 
                splitString(strArray,(char*)data, ", ");//Pisahkan dengan koma Split by comma
                for (int i = 0; i < 4; i++)
                {
                        strcpy(mystr_temp[i],strArray[i]);
                        Encoder_Now[i] = atoi(mystr_temp[i]);
                }
                
        }
        //Data encoder real-time 10ms  10ms real-time encoder data
        else if ((strncmp("MTEP",(char*)g_recv_buff_deal,4)==0))
    {
        length = strlen((char*)g_recv_buff_deal)-5;
        for (uint8_t i = 0; i < length; i++)
        {
            data[i] = g_recv_buff_deal[i+5]; //Hapus titik dua Remove the colon
        }  
                data[length] = '\0';        


                char* strArray[10];//Array pointer Panjang didefinisikan oleh nomor pemisah char 1 byte char* 4 byte       Pointer array The length is defined by the split number char 1 byte char* 4 bytes
                char mystr_temp[4][10] = {'\0'}; 
                splitString(strArray,(char*)data, ", ");//Pisahkan dengan koma Split by comma
                for (int i = 0; i < 4; i++)
                {
                        strcpy(mystr_temp[i],strArray[i]);
                        Encoder_Offset[i] = atoi(mystr_temp[i]);
                }
        }
        //Kecepatan    Speed
        else if ((strncmp("MSPD",(char*)g_recv_buff_deal,4)==0))
    {
        length = strlen((char*)g_recv_buff_deal)-5;
        for (uint8_t i = 0; i < length; i++)
        {
            data[i] = g_recv_buff_deal[i+5]; //Hapus titik dua Remove the colon
        }  
                data[length] = '\0';    
                
                char* strArray[10];//Array pointer Panjang didefinisikan oleh nomor pemisah char 1 byte char* 4 byte       Pointer array The length is defined by the split number char 1 byte char* 4 bytes
                char mystr_temp[4][10] = {'\0'}; 
                splitString(strArray,(char*)data, ", ");//Pisahkan dengan koma Split by comma
                for (int i = 0; i < 4; i++)
                {
                        strcpy(mystr_temp[i],strArray[i]);
                        g_Speed[i] = atof(mystr_temp[i]);
                }
        }
}


```

- Deal_Control_Rxtemp: Menyaring data yang diterima dan menyimpan yang memenuhi protokol komunikasi.
- Deal_data_real: Mengekstrak data asli yang disimpan dan merekonstruksi format cetak baru.

## 1.3 Fenomena Eksperimen

Setelah kabel terpasang dengan benar, tulis program ke mainboard. Setelah reset, Anda dapat melihat bahwa mobil akan bergerak maju selama 2.5S, bergerak mundur selama 2.5S, memutar kanan selama 2.5S, memutar kiri selama 2.5S, kemudian berhenti selama 2.5S, dan melanjutkan tindakan beralih status di atas.

Pada saat yang sama, Anda dapat melihat bahwa nilai motor yang dicetak terus berubah di asisten port serial.

![img](./assets/2-1761604788916-76.png)
