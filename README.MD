# **IRIS ANN Classification**

Setelah mengevaluasi file proses *training* dan *testing* dalam direktori `notebook` selanjutnya dilakukan proses *serving* atau penyajian service *machine learning* dan *deployment*. Berikut adalah langkah-langkahnya yang terangkum dalam setiap direktori:

+ `iris-ann`: Proses pembuatan *pickle* dan *dump* model yang siap di *deploy*.
+ `iris-ann-with-schedule`: Proses pembuatan *scheduler* untuk proses prediksi secara otomatis dalam waktu tertentu. Dengan masukan data dari satu tabel database dengan nama `tb_input` dengan keluaran satu tabel dalam database yang sama dengan nama `tb_output`.
+ `iris-ann-api`: Penggunaan API agar dapat melakukan prediksi dengan memasukan data melalui protokol HTTP.