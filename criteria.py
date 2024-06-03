import time
import streamlit as st
import mysql.connector
import pandas as pd
from user import create_connection
import criteria_add

# function to get all criteria data
def get_criteria_data():
    # initialize connection and get all data criteria
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM criteria")
    data = cursor.fetchall()
    
    cursor.close()
    conn.close()

    # set criteria data to dataframe
    columns = ['id', 'Nama Kriteria', 'Tipe',  'Bobot']

    return pd.DataFrame(data, columns=columns)
    

# function to get criteria data by id
def get_criteria_by_id(id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM criteria WHERE id = %s", [(id)])
    data = cursor.fetchone()
    cursor.close()
    conn.close()
    
    return data

# function to create criteria data
def create_criteria(data):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO criteria (id, name, type, weight) VALUES (%s, %s, %s, %s)", data)
    conn.commit()

    cursor.close()
    conn.close()

# function to update criteria data
def update_criteria(data):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE criteria SET id = %s,name = %s, type = %s, weight = %s WHERE id = %s", data)
    conn.commit()

    cursor.close()
    conn.close()

# function to delete criteria data
def delete_criteria(id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM criteria WHERE ID = %s", [(id)])
    conn.commit()

    cursor.close()
    conn.close()

# function to get criteria data by id
def get_sub_criteria_by_id(id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sub_criteria WHERE id = %s", [(id)])
    data = cursor.fetchone()
    cursor.close()
    conn.close()
    
    return data

# function to create criteria data
def create_sub_criteria(data):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO sub_criteria (id, criteria_id, name, weight) VALUES (%s, %s, %s, %s)", data)
    conn.commit()

    cursor.close()
    conn.close()
    
# function to update criteria data
def update_sub_criteria(data):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE sub_criteria SET id = %s, criteria_id = %s, name = %s, weight = %s WHERE id = %s", data)
    conn.commit()

    cursor.close()
    conn.close()
    
def delete_sub_criteria(id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM sub_criteria WHERE ID = %s", [(id)])
    conn.commit()

    cursor.close()
    conn.close()

def get_selection_criteria():
    # initialize connection and get all data criteria
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM criteria")
    data = cursor.fetchall()

    criteria_name = ()
    cols = st.columns(2, gap='large')
    with cols[0]:
        for i in range(len(data)):
            criteria_name += (data[i][0]+' | '+data[i][1],)
            cursor.execute("SELECT id, name, weight FROM sub_criteria where criteria_id = %s", [(data[i][0])])
            res = cursor.fetchall()
            st.write(f"Daftar Kriteria {data[i][1]}:")
            
            columns = ['id', 'Nama Sub Kriteria', 'Bobot']
            st.write(pd.DataFrame(res, columns=columns))
                    
    cursor.close()
    conn.close()

    with cols[1]:
        with st.form(key="sub_criteria_form", clear_on_submit=True):
            st.write("Tambah/Update Sub Kriteria")
            id = st.text_input('ID')
            criteria = st.selectbox('Kriteria', criteria_name)
            name = st.text_input('Name')
            weight = st.number_input('Weight')

            if st.form_submit_button('Simpan'):
                print(criteria.split(' | '))
                if not id or not name or not weight or not criteria:
                    st.error('Harap lengkapi kolom dengan benar!')
                else:
                    is_sub_criteria = get_sub_criteria_by_id(id)
                    if not is_sub_criteria:
                        create_sub_criteria((id, criteria.split(' | ')[0], name, weight))
                    else:
                        update_sub_criteria((id, criteria.split(' | ')[0], name, weight, id))
                        False
                    
                    # update dataframe
                    st.success('Data Anda telah berhasil disimpan!')
                    time.sleep(1)
                    st.experimental_rerun()


        with st.form(key="delete_sub_criteria_form", clear_on_submit=True):
            st.write("Hapus Sub Kriteria")
            id = st.text_input('ID')

            if st.form_submit_button('Hapus'):
                # Check if id input is empty
                if not id:
                    st.error('Harap lengkapi kolom dengan benar!')
                else:                
                    # Fetch one criteria data to check is data exists
                    is_sub_criteria = get_sub_criteria_by_id(id)
                    if not is_sub_criteria:
                        st.error('Data sub kriteria tidak ditemukan')
                    else:
                        delete_sub_criteria(id)
                        st.success('Data Anda telah berhasil dihapus!')
                        
                        # Reload Page
                        time.sleep(1)
                        st.experimental_rerun()
                        

def criteria_page():
    with st.form(key="criteria_form", clear_on_submit=True):
        st.write("Tambah/Update Kriteria")

        id = st.text_input('ID')
        name = st.text_input('Name')
        type = st.selectbox('Tipe', ('Cost', 'Benefit'))
        weight = st.number_input('Weight')


        if st.form_submit_button('Simpan'):
            if not id or not name or not weight:
                st.error('Harap lengkapi kolom dengan benar!')
            else:
                is_criteria = get_criteria_by_id(id)
                if not is_criteria:
                    create_criteria((id, name, type, weight))
                else:
                    update_criteria((id, name, type, weight, id))
                
                st.success('Data Anda telah berhasil disimpan!')
                
                # Reload Page
                time.sleep(1)
                st.experimental_rerun()


    with st.form(key="delete_criteria_form", clear_on_submit=True):
        st.write("Hapus Kriteria")
        id = st.text_input('ID')

        if st.form_submit_button('Hapus'):
            # Check if id input is empty
            if not id:
                st.error('Harap lengkapi kolom dengan benar!')
            else:                
                # Fetch one criteria data to check is data exists
                is_criteria = get_criteria_by_id(id)
                if not is_criteria:
                    st.error('Data kriteria tidak ditemukan')
                else:
                    delete_criteria(id)
                    st.success('Data Anda telah berhasil dihapus!')

                    # Reload Page
                    time.sleep(1)
                    st.experimental_rerun()
                
    # function to show criteria table
    st.title('Data Kriteria')
    st.write("Daftar Kriteria:")
    st.write(get_criteria_data())

    st.title('Data Pilihan Kriteria')
    st.write("Daftar Pilihan:")
    get_selection_criteria()


def criteria():
    criteria_page()

if __name__ == "__main__":
    criteria()