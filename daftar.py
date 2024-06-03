import streamlit as st
import mysql.connector

def create_connection():
    conn = mysql.connector.connect(
        host="sql12.freemysqlhosting.net",
        user="sql12710637",
        password="hpWBInA8cr",
        database="sql12710637"
    )
    return conn

def save_application(conn, username, jenjang_pendidikan, afirmasi, akreditasi_pt, akreditasi_prodi, ukt, nilai_ipk):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO applications (username, jenjang_pendidikan, afirmasi, akreditasi_pt, akreditasi_prodi, ukt, nilai_ipk) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                   (username, jenjang_pendidikan, afirmasi, akreditasi_pt, akreditasi_prodi, ukt, nilai_ipk))
    conn.commit()
    cursor.close()

def validate_data(jenjang_pendidikan, afirmasi, akreditasi_pt, akreditasi_prodi, ukt, nilai_ipk):
    if not jenjang_pendidikan or not afirmasi or not akreditasi_pt or not akreditasi_prodi:
        return False
    if ukt is None or nilai_ipk is None:
        return False
    if nilai_ipk > 4.00:
        return False
    return True

def daftar():
    st.title('Menu Daftar Beasiswa')

    with st.form(key='registration_form'):
        username = st.text_input('Nama')
        jenjang_pendidikan = st.selectbox('Jenjang Pendidikan', ('D1', 'D2', 'D3', 'D4', 'S1', 'S2'))
        afirmasi = st.radio('Termasuk Keluarga Afirmasi?', ('Ya', 'Tidak'))
        akreditasi_pt = st.selectbox('Akreditasi Perguruan Tinggi', ('A', 'B'))
        akreditasi_prodi = st.selectbox('Akreditasi Program Studi', ('A', 'B', 'C'))
        ukt = st.number_input('UKT', min_value=0.0, step=0.01)
        nilai_ipk = st.number_input('Nilai IPK Semester Terakhir', min_value=0.0, max_value=4.0, step=0.01)

        submitted = st.form_submit_button('Daftar')

        if submitted:
            if validate_data(jenjang_pendidikan, afirmasi, akreditasi_pt, akreditasi_prodi, ukt, nilai_ipk):
                conn = create_connection()
                save_application(conn, username, jenjang_pendidikan, afirmasi, akreditasi_pt, akreditasi_prodi, ukt, nilai_ipk)
                st.success('Data Anda telah berhasil disimpan!')
                conn.close()
            else:
                st.error('Harap lengkapi semua kolom dengan benar!')

if __name__ == "__main__":
    daftar()
