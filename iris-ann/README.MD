# **Proses Traing untuk Membuat Model yang Siap Deploy**

Agar hasil *training* atau mudah di *deploy* maka yang harus dilakukan adalah membuat *dump* model hasi dari proses *training* tersebut. Dalam kasus ini karena menggunakan library `keras` maka model hasil *dump* keluaran dari program yang siap untuk di *deploy* berformat `*.h5`, yang nantinya akan disimpan dalam direktori `project/model`. Selain itu keluaran lain berupa `pickle` hasil dari `joblib` yang berisi data masukan untuk proses normaliasasi saat memprediksi data baru akan disimpan dalam direktori `project/output`.

## **Requirements**

Berikut adalah kebutuhan yang diperlukan untuk menjalan program ini:

+ Python versi 3.8 (Di rekomendasikan untuk menggunakan `virtual environtment`)
+ Pip
+ make
+ Sistem Operasi (Di rekomendasikan `Ubuntu` atau `Windows + WSL Ubuntu`)

## **Cara Penggunaaan**

Berikut cara penggunaan program ini:

+ Jika `Python versi 3.8` sudah terinstall dan virtual environment sudah dibuat maka silahkan lanjutkan ke tahap selanjutnya, jika belum maka lakukan proses tersebut.

+ Lakukan installasi library yang akan digunakan yang tersimpan dalam file `../requirements.txt` dengan perintah berikut:

    ```
    pip install -r requirements.txt
    ```

+ Lakukan installasi `make` untuk mengeksekusi `Makefile`.

    ```
    sudo apt install make
    ```

+ Lakukan eksekusi perintah untuk membuat direktori `project/model`, `project/output` dan merubah *permission* dari direktori `project`.

    ```
    sudo make build
    ```

+ Lakukan eksekusi perintah untuk menjalankan *training*.

    ```
    sudo make train
    ```