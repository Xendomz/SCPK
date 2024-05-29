import streamlit as st
import mysql.connector
import hashlib

def create_connection():
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="",
        database="spk_database"
    )
    return conn

def register_user(conn, username, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
    conn.commit()
    cursor.close()

def verify_login(conn, username, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, hashed_password))
    user = cursor.fetchone()
    cursor.close()
    return user

def is_registered():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return count > 0

def register():
    st.title('Registrasi Pengguna')
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')
    confirm_password = st.text_input('Confirm Password', type='password')

    if password != confirm_password:
        st.error('Password dan konfirmasi password tidak cocok!')
        return

    if st.button('Register'):
        conn = create_connection()
        register_user(conn, username, password)
        st.success('Registrasi berhasil! Silakan login.')
        st.info('Silakan login menggunakan akun yang telah Anda daftarkan.')

        login()

def login():
    st.title('Login Admin')
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')

    if st.button('Login'):
        conn = create_connection()
        user = verify_login(conn, username, password)
        if user:
            st.success(f'Login berhasil, Selamat datang, {username}!')
            return True
        else:
            st.error('Username atau password salah. Silakan coba lagi.')
    return False

def user():
    if not is_registered():
        register()
    else:
        login()

if __name__ == '__main__':
    user()
