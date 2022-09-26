# **Penggunaan Scheduler Untuk Melakukan Prediksi**

Penggunaan *scheduler* untuk melakukan prediksi secara otomatis pada data dalam satu tabel yang kemudian hasinya disimpan dalam tabel lain.

## **Requirements**

Berikut adalah kebutuhan yang diperlukan untuk menjalan program ini:

+ Sistem Operasi (Di rekomendasikan `Ubuntu` atau `Windows + WSL Ubuntu`)
+ Python versi 3.8 (Di rekomendasikan untuk menggunakan `virtual environtment`)
+ Pip
+ Make
+ Docker Engine dan Docker Compose
+ Apache Airflow (Sudah tersedia dalam bentuk `docker-compose.yml` pada direktori `airflow`)
+ PostgreSQL (Sudah tersedia dalam bentuk `docker-compose.yml` yang terbundel dengan Apache Airflow pada direktori `airflow`)

## **Cara Penggunaan**

Langkah penggunaan dibagi memnjadi beberapa bagian penting, berikut adalah setiap bagian dan langkhanya.

### **Model Preparation**

Langkah untuk melakukan *training* model yang akan di *deploy*.

+ Jika `Python versi 3.8` sudah terinstall, `virtual environment` sudah dibuat dan diaktifkan maka silahkan lanjutkan ke tahap selanjutnya. Jika belum maka lakukan proses tersebut.

+ Lakukan installasi *library* yang akan digunakan yang tersimpan dalam file `project/requirements.txt` dengan perintah berikut:

    ```
    pip install -r requirements.txt
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

+ Kemudian deploy model tersebut dengan Docker Compose menggunakan perintah berikut.

    ```
    make deploy_model
    ```

### **Apache Airflow Preparation**

Langkah untuk installasi Airflow yang akan digunakan sebagai *scheduler* dan *pipeline*.

+ Jika Docker dan Docker Compose sudah terinstall. Maka lanjutkan installasi Apache Airflow dengan Docker Compose menggunakan perintah berikut.

    ```
    make deploy_airflow
    ```

+ Jika Apache Airflow berhasil terinstall, maka dengan mengakses alamat [http://localhost:8080](http://localhost:8080) pada browser akan tampil halaman login seperti gambar berikut.

    <img src="img/login_airflow.png" width="1000"/>

+ Lanjutkan dengan memasukan user *airflow* dan password *airflow* juga.
+ Lalu akan masuk ke tampilan panel Airflow, dengan *error* yang memunjukan kalau butuh masukan variabel seperti pada gambar berikut.

    <img src="img/dag_error_airflow.png" width="1000"/>

+ Unggah variabel Airflow dengan membuka menu **Admin > Variable** lalu pilih file yang berisi variabel dalam format `.json`. Kemudian lanjutkan dengan **Import Variable**. 

  + Berikut adalah file variabel yang akan digunakan:

      ```
      {
          "iris_ann_predict": {
              "pipeline_name": "iris_ann_predict_pipeline",
              "project": "Iris ANN Predict",
              "input_data": "/opt/airflow/data/new-iris-data.csv",
              "db_uri": "postgres://airflow:airflow@host.docker.internal:5432/db_iris",
              "conn_db": "conn_db_pipeline",
              "input_table": "tb_input",
              "input_column": [
                  "id", 
                  "sepal_length", 
                  "sepal_width", 
                  "petal_length", 
                  "petal_width"
              ],
              "output_table": "tb_output",
              "output_column": [
                  "executed_at",
                  "id",
                  "classes"
              ],
              "iris_ann_api": "http://host.docker.internal:5000/predict"
          }
      }
      ```

      *) *Copy* dan simpan variabel script diatas dalam format `.json` untuk diupload *upload*.
+ Kemudian lanjutkan dengan membahkan koneksi ke database PostgreSQL yang akan dipakai pada menu **Admin > Connection** dengan urutan sebagai berikut:
  
  + **Conn Id**: `conn_db_pipeline`
  + **Conn Type**: `Postgres`
  + **Description**: Kosongkan, isi jika ingin
  + **Host**: `host.docker.internal`
  + **Schema**: `db_iris`
  + **Login**: `airflow`
  + **Password**: `airflow`
  + **Port**: `5432`
  + **Extra**: Kosongkan


+ Pada akhirnya akan tampil *pipeline* dari Airflow seperti pada gambar berikut, yang mana *pipeline* tersebut dibuat menggukanan program yang tersimpan pada direktori `airflow/dags/iris_ann_predict_pipeline.py`.

    <img src="img/pipeline_airflow.png" width="1000"/>

    Dan bila dibuka maka akan muncul struktur *pipeline* tersebut dalam mode *tree*.

    <img src="img/pipeline_airflow_2.png" width="1000"/>

### **PosgreSQL Database Preparation**

Langkah untuk installasi Postgres yang akan digunakan sebagai database.

+ Masuk kedalam Database dengan menggunakan *command line* atau *tools* Database Client seperti [DBeaver](https://dbeaver.io/).

+ Masuk dengan credential dan alamat sebagai berikut:
  + **Address**: `localhost`
  + **Port**: `5432`
  + **User**: `airflow`
  + **Password**: `airflow`

+ Lanjutkan dengan pembuatan database dengan nama `db_iris`.

### **Proses Prediksi dari Tabel Input ke Tabel Output**

Langkah pengujian proses prediksi dengan input data pada Tabel Input dengan keluaran ke Tabel Output.

+ Tambahkan file `new-iris-data.csv` yang akan dijadikan sebagai input awal Tabel Input pada direktori `airflow/data`. Dengan format sebgain berikut (untuk nilai dan jumlah data dapat diubah sesuai dengan keinginan):

    ```
    sepal_length,sepal_width,petal_length,petal_width
    5.1,3.5,1.4,0.2
    4.9,3,1.4,0.2
    4.7,3.2,1.3,0.2
    4.6,3.1,1.5,0.2
    5,3.6,1.4,0.2
    7,3.2,4.7,1.4
    6.4,3.2,4.5,1.5
    6.9,3.1,4.9,1.5
    5.5,2.3,4,1.3
    6.5,2.8,4.6,1.5
    6.3,3.3,6,2.5
    5.8,2.7,5.1,1.9
    7.1,3,5.9,2.1
    6.3,2.9,5.6,1.8
    6.5,3,5.8,2.2
    ```
    *) Bisa juga dengan *Copy* dan simpan script diatas dengan nama `new-iris-data.csv` kemudian letakan dalam direktori `airflow/data`.

+ Tabel Input dan Tabel Output secara otomatis terbentuk dan terisi oleh masing-masing data *input* dengan nama `tb_input` dan data *output* dengan nama `tb_output` bila dilihat ke dalam Database langsung. Baik menggunakan command line atau tools DB Client seperti [DBeaver](https://dbeaver.io/).

+ Selanjutnya jika direktori `airflow/data` akan dikosongkan secara otomatis setelah proses prediksi selesai.

+ Meskipun direktori `airflow/data` kosong tanpa file `new-iris-data.csv` program tersebut akan terus berjalan setiap **10.00 AM WIB** tetapi dalam file `airflow/dags/iris_ann_predict_pipeline.py` menggunakan cron statement `"0 3 * * *"` yang menyatakan pipeline akan berjalan setiap jam 3 pagi, hal tersebut dikarenakan dalam Airflow digunakan konfigurasi waktu **UTC+0**.

+ Jika terdapat file atau ditambahkan file dengan nama `new-iris-data.csv` lagi. Maka file tersebut akan langsung ditambahkan ke dalam Tabel Input atau `tb_input` dengan `id` yang berlanjut berdasarkan data sebelumnya.

## **Reset Project**

Jika ingin menghapus model yang berjalan diatas Docker maka gunakan perintah berikut.

```
make clean_model
```

Untuk Airflow dan PostgreSQL yang berjalan diatas Docker maka dapat menggunakan perintah berikut.

```
make clean_airflow
```

Selanjutnya perintah berikut digunakan untuk menghapus seluruh direktori yang digunakan oleh Airflow dan Model untuk melakukan prediksi, yang mana pembuatannya diinisiasi dengan pemanggilan perintah `make build`.

```
make clean
```