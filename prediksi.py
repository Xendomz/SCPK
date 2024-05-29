import streamlit as st
import numpy as np
import joblib

decision_tree_model = joblib.load('decision_tree_model.pkl')
random_forest_model = joblib.load('random_forest_model.pkl')
scaler = joblib.load('scaler.pkl')

map_jenjang_pendidikan = {'S2': 5, 'S1': 4, 'D4': 4, 'D3': 3, 'D2': 2, 'D1': 1}
map_keluarga_afirmasi = {'Ya': 3, 'Tidak': 2}
map_akreditasi_pt = {'A': 3, 'B': 2, 'C': 1}
map_akreditasi_prodi = {'A': 4, 'B': 3, 'C': 2}

def predict_beasiswa(data):
    data_transformed = np.array(data).reshape(1, -1)
    data_transformed = scaler.transform(data_transformed)
    
    pred_dt = decision_tree_model.predict(data_transformed)
    pred_rf = random_forest_model.predict(data_transformed)
    
    return pred_dt[0], pred_rf[0]

def prediksi():
    st.title('Prediksi Kelayakan Beasiswa KIP-K')

    jenjang_pendidikan = st.selectbox('Jenjang Pendidikan', options=list(map_jenjang_pendidikan.keys()))
    keluarga_afirmasi = st.selectbox('Keluarga Afirmasi', options=list(map_keluarga_afirmasi.keys()))
    akreditasi_pt = st.selectbox('Akreditasi PT', options=list(map_akreditasi_pt.keys()))
    akreditasi_prodi = st.selectbox('Akreditasi Prodi', options=list(map_akreditasi_prodi.keys()))
    ukt = st.number_input('UKT', min_value=0, value=0, step=100000)
    nilai_ipk = st.number_input('Nilai IPK', min_value=0.0, max_value=4.0, value=0.0, step=0.01)

    if st.button('Prediksi'):
        data = [
            map_jenjang_pendidikan[jenjang_pendidikan],
            map_keluarga_afirmasi[keluarga_afirmasi],
            map_akreditasi_pt[akreditasi_pt],
            map_akreditasi_prodi[akreditasi_prodi],
            ukt,
            nilai_ipk
        ]
        pred_dt, pred_rf = predict_beasiswa(data)
        
        st.write('Hasil Prediksi:')
        st.write(f'Decision Tree: {"Layak" if pred_dt == 1 else "Tidak Layak"}')
        st.write(f'Random Forest: {"Layak" if pred_rf == 1 else "Tidak Layak"}')

if __name__ == '__main__':
    prediksi()
