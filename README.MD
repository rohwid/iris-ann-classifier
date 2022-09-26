# **IRIS ANN Classification**

Setelah mengevaluasi file proses *training* dan *testing* dalam direktori `notebook` selanjutnya dilakukan proses *serving* atau penyajian service *machine learning* dan *deployment*. Berikut adalah langkah-langkahnya yang terangkum dalam setiap direktori seusai urutan dari pertanyaan.

<ol type="a">
  <li><code>iris-ann</code>: Proses pembuatan <i>pickle</i> dan <i>dump</i> model yang siap di <i>deploy</i>.</li>
  <li><code>iris-ann-with-schedule</code>: Proses pembuatan <i>scheduler</i> untuk proses prediksi secara otomatis dalam waktu tertentu. Dengan masukan data dari satu tabel database dengan nama <code>tb_input</code> dengan keluaran satu tabel dalam database yang sama dengan nama <code>tb_output</code>.</li>
  <li><code>iris-ann-api</code>: Penggunaan API agar dapat melakukan prediksi dengan memasukan data melalui protokol HTTP.</li>
</ol>

