import io
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Audit SI - Access by KAI", page_icon="🚆", layout="wide")

KOMP = [
    ("Lingkungan Pengendalian (Control Environment)", "Sikap, kesadaran, dan tindakan manajemen: kebijakan, struktur, tanggung jawab, kompetensi, vendor, anggaran."),
    ("Penilaian Risiko (Risk Assessment)", "Identifikasi, analisis, evaluasi, dan penanganan risiko TI, keamanan, kontinuitas, dan pihak ketiga."),
    ("Aktivitas Pengendalian (Control Activities)", "Pengelolaan akses, keamanan data dan infrastruktur, perubahan, backup dan pemulihan, kontrol aplikasi."),
    ("Informasi dan Komunikasi (Information and Communication)", "Kualitas, dokumentasi, dan pertukaran informasi, insiden, komunikasi, pelindungan data, pelaporan."),
    ("Aktivitas Pemantauan (Monitoring Activities)", "KPI/SLA, monitoring, kapasitas, audit, kepatuhan, dan tindak lanjut kelemahan."),
]
# No | Pertanyaan audit | Ref. COBIT 2019 | Bukti yang diperiksa
RAW = """
1.1|Apakah PT KAI memiliki kebijakan dan pedoman tata kelola/manajemen TI tertulis untuk pengelolaan Access by KAI dan sistem pemesanan tiket pendukungnya?|EDM01, APO01|SK/kebijakan TI; SOP tata kelola TI; riwayat revisi dokumen
1.2|Apakah struktur organisasi serta peran dan tanggung jawab (pemilik sistem, pengembang, operator, keamanan) dalam pengelolaan Access by KAI telah ditetapkan dan didokumentasikan?|APO01|Struktur organisasi; uraian jabatan; matriks RACI; SK penunjukan
1.3|Apakah direksi atau manajemen puncak mengawasi kinerja dan risiko TI melalui forum atau mekanisme pelaporan yang terjadwal?|EDM01, EDM05|Notulen rapat; laporan kepada direksi; SK komite/forum
1.4|Apakah rencana strategis/roadmap TI selaras dengan tujuan bisnis perusahaan dan memuat pengembangan sistem pemesanan tiket?|APO02, EDM02|Renstra/roadmap TI; dokumen rencana kerja dan anggaran; dokumen KPI
1.5|Apakah kebijakan keamanan informasi, kode etik, dan perjanjian kerahasiaan telah disosialisasikan serta dipatuhi pegawai dan pihak ketiga yang mengakses sistem?|APO01, APO13|Kebijakan keamanan informasi; sampel NDA; daftar hadir/materi sosialisasi
1.6|Apakah tersedia SDM TI dengan kompetensi memadai beserta program pengembangan kompetensi untuk mengelola dan mengamankan Access by KAI?|APO07|Data SDM TI; rencana dan realisasi pelatihan; sertifikat kompetensi
1.7|Apakah hubungan dengan vendor dan mitra (pengembang, hosting, penyedia pembayaran, kanal penjualan eksternal) diatur dalam kontrak yang memuat tingkat layanan dan klausul keamanan?|APO09, APO10|Kontrak/PKS; dokumen SLA; daftar vendor dan penanggung jawab
1.8|Apakah anggaran dan sumber daya TI untuk operasional, keamanan, dan pengembangan sistem telah ditetapkan dan realisasinya dipantau?|APO06, EDM04|Dokumen anggaran TI; laporan realisasi anggaran; usulan/prioritas investasi
2.1|Apakah terdapat kebijakan dan metodologi manajemen risiko tertulis yang mencakup risiko TI, kriteria penilaian, serta selera/toleransi risiko?|EDM03, APO12|Kebijakan manajemen risiko; dokumen selera dan toleransi risiko; SK penanggung jawab risiko
2.2|Apakah risiko terkait Access by KAI (ketersediaan saat lonjakan, kebocoran data, kecurangan pembayaran, ketergantungan vendor) telah diidentifikasi dan dicatat?|APO12|Risk register; profil risiko unit TI; riwayat pembaruan risk register
2.3|Apakah risiko dianalisis dan dievaluasi dengan metode konsisten sehingga prioritas penanganan dapat ditetapkan?|APO12|Lembar penilaian risiko; peta risiko (risk map)
2.4|Apakah rencana penanganan risiko prioritas memiliki penanggung jawab, tenggat waktu, dan pemantauan progres?|APO12, EDM03|Rencana penanganan risiko; laporan progres mitigasi
2.5|Apakah penilaian kerentanan atau uji penetrasi pada aplikasi dan infrastruktur dilakukan berkala dan hasilnya ditindaklanjuti?|APO12, APO13, DSS05|Jadwal dan laporan asesmen kerentanan/uji penetrasi; tracker remediasi
2.6|Apakah analisis dampak bisnis (BIA) telah dilakukan untuk layanan pemesanan tiket, termasuk penetapan RTO dan RPO?|DSS04, APO12|Dokumen BIA; dokumen penetapan RTO/RPO
2.7|Apakah risiko dinilai sebelum perubahan besar pada sistem dan sebelum melibatkan mitra/vendor baru?|APO12, APO10, BAI06|Sampel formulir permintaan perubahan; hasil due diligence vendor; prosedur pengadaan
2.8|Apakah profil risiko TI dilaporkan berkala kepada manajemen dan ditinjau ulang berdasarkan insiden serta hasil audit?|EDM03, APO12|Laporan profil risiko; notulen rapat manajemen risiko
3.1|Apakah terdapat prosedur formal untuk pemberian, perubahan, dan pencabutan hak akses ke aplikasi, basis data, dan infrastruktur pendukung Access by KAI?|DSS05, APO13|SOP manajemen akses; sampel tiket/formulir akses; daftar pengguna vs data kepegawaian
3.2|Apakah akun berhak istimewa (administrator sistem dan basis data) dibatasi, aktivitasnya dicatat, dan dilindungi autentikasi yang kuat?|DSS05|Daftar akun istimewa; konfigurasi autentikasi; log dan hasil peninjauan
3.3|Apakah peninjauan hak akses dilakukan berkala dan kebijakan kata sandi/autentikasi diterapkan konsisten pada sistem?|DSS05|Laporan peninjauan hak akses; dokumen kebijakan kata sandi; tampilan konfigurasi sistem
3.4|Apakah data pribadi pelanggan dan data transaksi dilindungi melalui klasifikasi data, enkripsi saat disimpan dan ditransmisikan, serta pembatasan akses?|APO13, APO14, DSS05|Kebijakan klasifikasi data; konfigurasi enkripsi/sertifikat; observasi basis data dan aplikasi
3.5|Apakah infrastruktur jaringan dan server diamankan (firewall, proteksi serangan, penambalan kerentanan) serta aset dan konfigurasinya terinventarisasi?|DSS05, BAI09, BAI10|Inventaris aset; laporan patch/konfigurasi; konfigurasi perangkat keamanan; observasi pusat data
3.6|Apakah perubahan aplikasi dan infrastruktur dikendalikan melalui pengajuan, persetujuan, pengujian, dan rencana pemulihan (rollback)?|BAI06, BAI07|SOP manajemen perubahan; sampel change request dan hasil uji; catatan rilis
3.7|Apakah backup data dan pemulihan sistem dilaksanakan sesuai jadwal, disimpan di lokasi terpisah, dan diuji keberhasilannya?|DSS04|Kebijakan backup; log backup; laporan uji restore/DRP
3.8|Apakah pengendalian aplikasi pada pemesanan, pembayaran, dan penerbitan tiket (validasi input, rekonsiliasi transaksi, jejak audit) telah dirancang dan berjalan?|DSS06|Dokumentasi fungsi aplikasi; laporan rekonsiliasi; sampel audit trail; observasi/pengujian fitur
4.1|Apakah kepemilikan data, standar data, dan kualitas data penumpang serta transaksi tiket telah ditetapkan dan dikelola?|APO14|Daftar data owner; kamus data/kebijakan data; prosedur koreksi data
4.2|Apakah dokumentasi sistem (arsitektur, diagram alir data, manual pengguna dan operasional) tersedia, lengkap, dan dimutakhirkan?|APO03, BAI08|Dokumen arsitektur; manual dan SOP; riwayat versi dokumen
4.3|Apakah insiden dan gangguan layanan dicatat, diklasifikasikan, dieskalasi, dan diselesaikan melalui prosedur baku?|DSS02|SOP insiden; log/tiket insiden; laporan insiden periodik
4.4|Apakah insiden berulang atau berdampak besar dianalisis akar penyebabnya dan didokumentasikan sebagai basis pengetahuan serta perbaikan?|DSS03, BAI08|Laporan RCA; basis pengetahuan; daftar masalah (problem log)
4.5|Apakah terdapat prosedur komunikasi kepada pengguna dan pemangku kepentingan saat terjadi gangguan atau lonjakan layanan?|DSS02, APO08, EDM05|SOP komunikasi krisis; contoh pengumuman publik; catatan penyampaian informasi
4.6|Apakah keluhan dan masukan pengguna dikelola, dianalisis, dan ditindaklanjuti secara terdokumentasi?|APO08, DSS02|Rekap keluhan; laporan analisis keluhan; bukti tindak lanjut
4.7|Apakah kebijakan pelindungan data pribadi (pemberitahuan privasi, hak pemilik data, penanganan kegagalan pelindungan data) telah ditetapkan dan dikomunikasikan?|APO14, MEA03|Kebijakan privasi; SOP penanganan kebocoran data; SK penanggung jawab
4.8|Apakah informasi kinerja TI (ketersediaan, insiden, keamanan, kepuasan pengguna) dilaporkan berkala kepada manajemen dan memadai untuk pengambilan keputusan?|MEA01, EDM05|Laporan kinerja TI; dashboard; notulen tanggapan manajemen
5.1|Apakah indikator kinerja dan target tingkat layanan Access by KAI (ketersediaan, waktu respons, tingkat kesalahan transaksi) ditetapkan dan diukur berkala?|MEA01|Dokumen KPI/SLA; laporan pengukuran; analisis penyimpangan
5.2|Apakah infrastruktur dan aplikasi dipantau berkelanjutan (monitoring, peringatan dini, peninjauan log keamanan) dan log dilindungi serta disimpan sesuai kebijakan?|DSS01, DSS05, MEA01|Dashboard/konfigurasi alert; kebijakan retensi log; sampel hasil peninjauan log
5.3|Apakah kesiapan kapasitas pada periode puncak pemesanan direncanakan, diuji, dan dievaluasi setelah periode berakhir?|BAI04, MEA01|Rencana kapasitas; laporan uji beban; laporan evaluasi pascamusim
5.4|Apakah audit/penjaminan independen atas TI direncanakan dan dilaksanakan berkala terhadap sistem pemesanan tiket?|MEA04, MEA02|Program kerja audit tahunan; laporan hasil audit; piagam audit internal
5.5|Apakah temuan dan rekomendasi dari audit atau pemeriksaan sebelumnya dipantau tindak lanjutnya sampai tuntas?|MEA02, MEA04|Tracker tindak lanjut; laporan status; bukti penutupan temuan
5.6|Apakah kepatuhan terhadap regulasi dan kebijakan internal yang relevan (pelindungan data pribadi, penyelenggaraan sistem elektronik) diidentifikasi dan dinilai berkala?|MEA03|Daftar regulasi; hasil penilaian kepatuhan; rencana tindak lanjut
5.7|Apakah efektivitas pengendalian internal TI dievaluasi berkala (penilaian mandiri/uji pengendalian) dan kelemahan pengendalian dilaporkan?|MEA02|Hasil penilaian mandiri pengendalian; laporan kelemahan pengendalian
5.8|Apakah kebijakan, prosedur, dan pengendalian ditinjau ulang berdasarkan hasil pemantauan, insiden, dan audit sehingga terjadi perbaikan berkelanjutan?|EDM01, MEA01|Notulen tinjauan manajemen; riwayat revisi kebijakan/SOP; rencana perbaikan
"""
Q = []
for l in RAW.strip().splitlines():
    no, q, ref, bk = l.split("|")
    Q.append({"no": no, "k": int(no[0]), "q": q, "ref": ref, "bukti": bk})

STATUS = ["", "Ya", "Sebagian", "Tidak", "Tidak Dapat Diverifikasi"]
SKOR = ["", "0", "1", "2", "3", "4"]
TINGKAT = ["Tidak ada", "Awal / ad hoc", "Sebagian", "Diterapkan", "Terkelola dan dioptimalkan"]
IND = {"Ya": (3, 4), "Sebagian": (1, 3), "Tidak": (0, 1)}  # pedoman indikatif Bab III.E
IDENT = ["Nama auditor", "Periode/ruang waktu yang diaudit", "Tanggal pelaksanaan pemeriksaan", "Lokasi pemeriksaan",
         "Auditee / unit yang diperiksa", "Narasumber (nama dan jabatan)", "Dokumen surat tugas/izin (nomor)"]

st.markdown("""<style>
h1,h2,h3{color:#9a3412}
[data-testid="stVerticalBlockBorderWrapper"]{border-left:5px solid #ea580c;background:#fff}
[data-testid="stSidebar"]{border-right:2px solid #fed7aa}
</style>""", unsafe_allow_html=True)

ss = st.session_state
if "ans" not in ss:
    ss.ans = {q["no"]: {"status": "", "skor": "", "catatan": ""} for q in Q}
    ss.ident = {k: "" for k in IDENT}
    ss.temuan = pd.DataFrame({"Ringkasan Temuan": [""] * 8, "Ref. No. Pertanyaan": [""] * 8})
    ss.rek = pd.DataFrame({"Rekomendasi Perbaikan": [""] * 8, "Ref. No. Temuan": [""] * 8})
    ss.log = pd.DataFrame({"Kode Bukti": [""] * 15, "Jenis (D/W/O)": [""] * 15, "Deskripsi Bukti": [""] * 15,
                           "Sumber / Narasumber": [""] * 15, "Tanggal": [""] * 15, "Terkait No. Pertanyaan": [""] * 15})
    ss.kes, ss.tempat = "", ""


def rekap():
    rows = []
    for k, (nama, _) in enumerate(KOMP, 1):
        sk = [int(ss.ans[q["no"]]["skor"]) for q in Q if q["k"] == k and ss.ans[q["no"]]["skor"] != ""]
        n, tot = len(sk), sum(sk)
        rows.append({"No": k, "Komponen": nama.split(" (")[0], "Tersedia": 8, "Dinilai": n, "Total Skor": tot,
                     "Skor Maksimal": n * 4, "Persentase (%)": round(tot / (n * 4) * 100, 1) if n else None})
    d = pd.DataFrame(rows)
    n, tot = d["Dinilai"].sum(), d["Total Skor"].sum()
    d.loc[len(d)] = ["", "TOTAL", 40, n, tot, n * 4, round(tot / (n * 4) * 100, 1) if n else None]
    return d


def form_df():
    return pd.DataFrame([{"No": q["no"], "Komponen": KOMP[q["k"] - 1][0], "Pertanyaan": q["q"], "Ref. COBIT 2019": q["ref"],
                          "Bukti": q["bukti"], "Status": ss.ans[q["no"]]["status"], "Skor": ss.ans[q["no"]]["skor"],
                          "Catatan Auditor": ss.ans[q["no"]]["catatan"]} for q in Q])


PAGES = ["Informasi Audit"] + [f"Komponen {i}: {k[0].split(' (')[0]}" for i, k in enumerate(KOMP, 1)] + \
        ["Rekapitulasi", "Temuan dan Kesimpulan", "Log Bukti"]

with st.sidebar:
    st.markdown("## 🚆 Audit SI\n**Access by KAI**")
    halaman = st.radio("Langkah", PAGES, label_visibility="collapsed")
    dinilai = sum(1 for a in ss.ans.values() if a["skor"] != "")
    st.progress(dinilai / 40, text=f"{dinilai}/40 butir dinilai")
    st.divider()
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as xw:
        pd.DataFrame(list(ss.ident.items()), columns=["Keterangan", "Isian"]).to_excel(xw, sheet_name="Identitas", index=False)
        form_df().to_excel(xw, sheet_name="Form Audit", index=False)
        rekap().to_excel(xw, sheet_name="Rekapitulasi", index=False)
        ss.temuan.to_excel(xw, sheet_name="Temuan", index=False)
        ss.rek.to_excel(xw, sheet_name="Rekomendasi", index=False)
        pd.DataFrame({"Kesimpulan": [ss.kes], "Tempat, tanggal": [ss.tempat]}).to_excel(xw, sheet_name="Kesimpulan", index=False)
        ss.log.to_excel(xw, sheet_name="Log Bukti", index=False)
    st.download_button("⬇️ Unduh Excel", buf.getvalue(), "audit_access_by_kai.xlsx", width="stretch")
    st.download_button("⬇️ Unduh CSV form", form_df().to_csv(index=False).encode("utf-8-sig"), "form_audit.csv", "text/csv", width="stretch")
    st.caption("Data hilang jika halaman ditutup. Unduh berkala.")

if halaman == "Informasi Audit":
    st.title("Form Audit Sistem Informasi")
    st.subheader("Access by KAI · PT Kereta Api Indonesia (Persero)")
    st.write("Kerangka acuan: **COBIT 2019** dengan struktur **lima komponen COSO**. Isi identitas, lalu telusuri kelima komponen "
             "dari sidebar. Isi status, skor 0-4, dan catatan auditor berdasarkan bukti.")
    st.info("Pemetaan COSO ke COBIT bersifat konseptual. Aplikasi akademik, bukan hasil audit aktual perusahaan.")
    st.markdown("**Identitas pelaksanaan audit**")
    for k in IDENT:
        ss.ident[k] = st.text_input(k, ss.ident[k], key=f"id_{k}")
    st.markdown("**Skala skor**")
    st.table(pd.DataFrame({"Skor": range(5), "Tingkat": TINGKAT}).set_index("Skor"))

elif halaman.startswith("Komponen"):
    k = PAGES.index(halaman)
    st.title(f"Komponen {k}")
    st.subheader(KOMP[k - 1][0])
    st.caption(KOMP[k - 1][1])
    for q in [x for x in Q if x["k"] == k]:
        a = ss.ans[q["no"]]
        with st.container(border=True):
            st.markdown(f"**{q['no']}**  {q['q']}")
            st.caption(f"Ref. COBIT 2019: {q['ref']}  ·  Bukti: {q['bukti']}")
            c1, c2, c3 = st.columns([1.3, 0.7, 2.6])
            a["status"] = c1.selectbox("Status", STATUS, STATUS.index(a["status"]), key=f"s{q['no']}", format_func=lambda x: x or "-")
            a["skor"] = c2.selectbox("Skor", SKOR, SKOR.index(a["skor"]), key=f"k{q['no']}", format_func=lambda x: x or "-")
            a["catatan"] = c3.text_input("Catatan auditor (kode bukti, jenis D/W/O, ringkasan)", a["catatan"], key=f"c{q['no']}")
            if a["status"] in IND and a["skor"] != "" and not IND[a["status"]][0] <= int(a["skor"]) <= IND[a["status"]][1]:
                lo, hi = IND[a["status"]]
                st.caption(f"⚠️ Di luar pedoman indikatif ({lo}-{hi}) untuk status {a['status']}. Pastikan didukung bukti.")
            if a["status"] == "Tidak Dapat Diverifikasi" and a["skor"] == "":
                st.caption("Skor dikosongkan: butir tidak dihitung dan dicatat sebagai pembatasan lingkup.")

elif halaman == "Rekapitulasi":
    st.title("Rekapitulasi Hasil Audit")
    r = rekap()
    tot = r.iloc[-1]
    c1, c2, c3 = st.columns(3)
    c1.metric("Butir dinilai", f"{int(tot['Dinilai'])} / 40")
    c2.metric("Total skor", f"{int(tot['Total Skor'])} / {int(tot['Skor Maksimal'])}")
    c3.metric("Persentase penerapan", "-" if pd.isna(tot["Persentase (%)"]) else f"{tot['Persentase (%)']}%")
    if tot["Dinilai"]:
        rata = tot["Total Skor"] / tot["Dinilai"]
        st.success(f"Rata-rata skor {rata:.2f} (mendekati tingkat **{TINGKAT[round(rata)]}**)")
    st.dataframe(r, hide_index=True, width="stretch")
    st.caption("Persentase penerapan = Total skor / (Jumlah pertanyaan dinilai × 4) × 100%")
    if tot["Dinilai"]:
        st.bar_chart(r.iloc[:5].set_index("Komponen")["Persentase (%)"].fillna(0))
    tdv = [n for n, a in ss.ans.items() if a["status"] == "Tidak Dapat Diverifikasi"]
    if tdv:
        st.warning("Butir berstatus Tidak Dapat Diverifikasi: " + ", ".join(tdv))

elif halaman == "Temuan dan Kesimpulan":
    st.title("Temuan, Rekomendasi, dan Kesimpulan")
    t1, t2, t3 = st.tabs(["Ringkasan temuan", "Rekomendasi", "Kesimpulan"])
    with t1:
        ss.temuan = st.data_editor(ss.temuan, key="ed_t", hide_index=True, width="stretch")
    with t2:
        ss.rek = st.data_editor(ss.rek, key="ed_r", hide_index=True, width="stretch")
    with t3:
        ss.kes = st.text_area("Kesimpulan audit", ss.kes, height=180, key="w_kes")
        ss.tempat = st.text_input("Tempat, tanggal", ss.tempat, key="w_tmp")
    yes_low = [f"{n}" for n, a in ss.ans.items() if a["skor"] in ("0", "1")]
    if yes_low:
        st.caption("Butir berskor 0-1 (kandidat temuan): " + ", ".join(yes_low))

else:
    st.title("Lampiran A. Log Bukti Audit")
    st.caption("Jenis: D = dokumen, W = wawancara, O = observasi.")
    ss.log = st.data_editor(ss.log, key="ed_l", hide_index=True, width="stretch")
