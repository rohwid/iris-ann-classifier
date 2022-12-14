# **Deploy Model Menjadi API Endpoint**

Penyajian atau *service* ML berbasis API yang dapat menerima permintaan atau *request* prediksi melalui protokol HTTP.

## **Requirements**

Berikut adalah kebutuhan yang diperlukan untuk menjalan program ini:

+ Sistem Operasi (Di rekomendasikan `Ubuntu` atau `Windows + WSL Ubuntu`)
+ Python versi 3.8 (Di rekomendasikan untuk menggunakan `virtual environtment`)
+ Pip
+ Make
+ Docker Engine dan Docker Compose
+ Postman

## **Cara Penggunaan**

Langkah penggunaan dibagi memnjadi beberapa bagian penting, berikut adalah setiap bagian dan langkhanya.

### **Model Preparation**

Langkah untuk melakukan training model yang akan di *deploy*.

+ Jika `Python versi 3.8` sudah terinstall, `virtual environment` sudah dibuat dan diaktifkan maka silahkan lanjutkan ke tahap selanjutnya. Jika belum maka lakukan proses tersebut.

+ Lakukan installasi library yang akan digunakan yang tersimpan dalam file `project/requirements.txt` dengan perintah berikut:

    ```
    pip install -r project/requirements.txt
    ```

+ Lakukan installasi `make` untuk mengeksekusi `Makefile`.

    ```
    sudo apt install make
    ```

+ Lakukan eksekusi perintah untuk membuat direktori `project/model` dan `project/output`. Kemudian juga akan merubah *permission* dari direktori `project`.

    ```
    make build
    ```

+ Lakukan eksekusi perintah untuk menjalankan *training* agar model dapat digunakan.

    ```
    make train
    ```
### **Deploy Model**

Berikut adalah beberapa langkah dan opsi dalam melakukan model *deployment*.

+ Untuk menguji proses prediksi secara langsung, lanjutkan dengan eksekusi perintah berikut.

    ```
    make serve
    ```

+ Gunakan Postman untuk melakukan `request` atau prediksi dengan data masukan yang dimasukan memaluli protokol HTTP dengan ketentuan sebagai berikut:
  + **Method**: `POST`
  + **Address**: `http://0.0.0.0:5000/predict`
  + Tambahkan **header** pada Postman:
    + **Key**: `Content-Type`
    + **Value**: `Application/json`
  + Kemudian pada `Body` pilih `raw`, dan berikut contoh *request body* yg digunakan:
    ```
    [
        {
            "sepal_length": 6.0,
            "sepal_width": 3.0,
            "petal_length": 4.0,
            "petal_width": 1.5
        },
        {
            "sepal_length": 6.1,
            "sepal_width": 3.2,
            "petal_length": 4.3,
            "petal_width": 1.1
        },
        {
            "sepal_length": 5.7,
            "sepal_width": 2.9,
            "petal_length": 4.1,
            "petal_width": 1.6
        }
    ]
    ```

+ Atau bisa juga menggukan file `*.json` yang bisa di import ke postman, file tersebut tersimpan pada direktori `postman/iris-ann.postman_collection.json`.

+ Kemudian deploy model tersebut juga dapat di *deploy* dengan Docker Compose menggunakan perintah berikut. Jika melakukan deployment menggunakan Docker maka tidak perlu melakukan langkah seperti installasi python, virtual environment dan installasi library.

    ```
    make deploy_model
    ```

+ Kemudian ulangi cara pengujian dengan menggunakan Postman diatas.

+ Untuk format keluaran dari program ini sendiri adalah sebagai berikut.

    ```
    {
        "response": [0, 2, 1]
    }
    ```

## **Reset Project**

Jika ingin menghapus model yang berjalan diatas Docker maka gunakan perintah berikut.

```
make clean_model
```

Selanjutnya perintah berikut digunakan untuk menghapus seluruh direktori yang digunakan oleh Model untuk melakukan prediksi, yang mana pembuatannya diinisiasi dengan pemanggilan perintah `make build`.

```
make clean
```