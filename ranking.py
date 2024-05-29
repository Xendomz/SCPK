import streamlit as st
import pandas as pd
from user import create_connection

def calculate_wp(data):
    weights = {
        'C1': 0.25,
        'C2': 0.15,
        'C3': 0.15,
        'C4': 0.15,
        'C5': -0.10,
        'C6': 0.20
    }

    def calculate_s(row):
        s = 1
        s *= row['C1'] ** weights['C1']
        s *= row['C2'] ** weights['C2']
        s *= row['C3'] ** weights['C3']
        s *= row['C4'] ** weights['C4']
        s *= row['C5'] ** weights['C5']
        s *= row['C6'] ** weights['C6']
        return s

    data['Vektor S'] = data.apply(calculate_s, axis=1)

    total_s = data['Vektor S'].sum()

    data['WP Score'] = data['Vektor S'] / total_s

    sorted_data = data.sort_values(by='WP Score', ascending=False).reset_index(drop=True)
    sorted_data['Ranking'] = sorted_data.index + 1
    
    return sorted_data

def show_ranking():
    st.title('Ranking Penerima KIP-K')

    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM applications")
    data = cursor.fetchall()
    conn.close()

    columns = ['id', 'username', 'jenjang_pendidikan', 'afirmasi', 'akreditasi_pt', 'akreditasi_prodi', 'ukt', 'nilai_ipk']
    df = pd.DataFrame(data, columns=columns)

    df['C1'] = df['jenjang_pendidikan'].map({'S2': 5, 'S1': 4, 'D4': 4, 'D3': 3, 'D2': 2, 'D1': 1})
    df['C2'] = df['afirmasi'].map({'Ya': 3, 'Tidak': 2})
    df['C3'] = df['akreditasi_pt'].map({'A': 3, 'B': 2})
    df['C4'] = df['akreditasi_prodi'].map({'A': 3, 'B': 2, 'C': 1})
    df['C5'] = df['ukt'].apply(lambda x: 5 if x < 1000000 else (4 if x < 3000000 else (3 if x < 5000000 else (2 if x < 10000000 else 1))))
    df['C6'] = df['nilai_ipk'].apply(lambda x: 5 if x >= 3.75 else (4 if x >= 3.50 else (3 if x >= 3.00 else (2 if x >= 2.50 else 1))))

    sorted_df = calculate_wp(df)

    st.write("Ranking Penerima KIP-K:")
    st.write(sorted_df)

if __name__ == "__main__":
    show_ranking()
