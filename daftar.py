import streamlit as st
import mysql.connector
import pandas as pd
from user import create_connection

def create_connection():
    conn = mysql.connector.connect(
        host="sql12.freemysqlhosting.net",
        user="sql12710637",
        password="hpWBInA8cr",
        database="sql12710637"
    )
    return conn

def get_select_criteria():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM criteria")
    criterias = cursor.fetchall()
    
    input_data = {}
    for i, criteria in enumerate(criterias):
        cursor.execute("SELECT id, name FROM sub_criteria WHERE criteria_id = %s", [(criteria[0])])
        sub_criterias = cursor.fetchall()
        filtered_sub_criteria = ()
        for sc in sub_criterias:
            filtered_sub_criteria += sc[0] + '|' + sc[1],
        input_data[i] = st.selectbox(criteria[1], filtered_sub_criteria)
        
    return input_data
            
def get_alter_by_username(username):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM applications WHERE username = %s", [(username)])
    data = cursor.fetchone()
    cursor.close()
    conn.close()
    
    return data

def create_alter_data(data):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO applications (username) VALUES (%s)", [(data[0])])
    alt = cursor.lastrowid
    for key, val in data[1].items():
        cursor.execute("INSERT INTO detail_criteria (alt_id, sub_id) VALUES (%s, %s)", (alt, val.split('|')[0]))
        
    conn.commit()

    cursor.close()
    conn.close()
    
def update_alter_data(data):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT (id) FROM applications WHERE username = %s", [(data[0])])
    alt = cursor.fetchone()[0]
    cursor.execute("DELETE FROM detail_criteria WHERE alt_id = %s", [(alt)])
    
    for key, val in data[1].items():
        cursor.execute("INSERT INTO detail_criteria (alt_id, sub_id) VALUES (%s, %s)", (alt, val.split('|')[0]))
        
    conn.commit()

    cursor.close()
    conn.close()
    
def calculate():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM criteria")
    criterias = cursor.fetchall()
    
    columns = ['id', 'Nama']
    for criteria in criterias:
        columns.append(criteria[1])
    
    cursor.execute("SELECT * FROM applications")
    appications = cursor.fetchall()
    res = []
    s_total = 0
    for key, alt in enumerate(appications):
        data = ()
        data += alt[0],
        data += alt[1],
        cursor.execute("SELECT alt_id, sub_id FROM detail_criteria WHERE alt_id = %s", ([alt[0]]))
        s = 1
        for k, d_criteria in enumerate(cursor.fetchall()):
            cursor.execute("SELECT sub_criteria.id, sub_criteria.name, sub_criteria.weight, criteria.id, criteria.weight, criteria.name FROM sub_criteria JOIN criteria ON criteria.id = sub_criteria.criteria_id WHERE sub_criteria.id = %s", ([d_criteria[1]]))
            sub_c = cursor.fetchone()
            s *= int(sub_c[2]) ** float(sub_c[4])
            data += sub_c[1],
            
        s_total += s
        data += s,
        res.append(data)
    
    vec_s_total = 0
    for key, alt in enumerate(res):
        vec_s = alt[-1] / s_total
        alt += vec_s,
        vec_s_total += vec_s
        res[key] = alt
        
    for key, alt in enumerate(res):
        alt += alt[-1] / vec_s_total,
        res[key] = alt
        
    res.sort(reverse= True, key= lambda t: t[-1])
    
    print(columns)
    columns.extend(['S', 'Vektor S', 'WP Score'])
    
    return pd.DataFrame(res, columns=columns)

def daftar():
    st.title('Menu Daftar Beasiswa')
    with st.form(key='registration_form', clear_on_submit=True):
        username = st.text_input('Nama')
        input_data = get_select_criteria()
    
        submitted = st.form_submit_button('Daftar')

        if submitted:
            if not id or not username:
                st.error('Harap lengkapi kolom dengan benar!')
            else:
                is_alter = get_alter_by_username(username)
                if not is_alter:
                    create_alter_data((username, input_data))
                else:
                    update_alter_data((username, input_data))
                    
                st.success('Data Anda telah berhasil disimpan!')
                    
            # if validate_data(jenjang_pendidikan, afirmasi, akreditasi_pt, akreditasi_prodi, ukt, nilai_ipk):
            #     conn = create_connection()
            #     save_application(username, jenjang_pendidikan, afirmasi, akreditasi_pt, akreditasi_prodi, ukt, nilai_ipk)
            #     st.success('Data Anda telah berhasil disimpan!')
            #     conn.close()
            # else:
            #     st.error('Harap lengkapi semua kolom dengan benar!')
            
    calculate_button = st.button('Kalkulasi')
    if calculate_button:
        st.write(calculate())

if __name__ == "__main__":
    daftar()
