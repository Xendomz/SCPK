import streamlit as st
from user import register, login, create_connection
import home, daftar, ranking, prediksi, konsultasi, criteria


def main():
    st.title('SPK Penerima Bantuan KIP-K')

    if 'register_in' not in st.session_state:
        st.session_state.register_in = False

    if not st.session_state.register_in:
        register_successful = register()
        if register_successful:
            st.session_state.register_in = True
        else:
            st.warning('Silakan login apabila sudah memiliki akun')
            return


    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        login_successful = login()
        if login_successful:
            st.session_state.logged_in = True
        else:
            st.warning('Silakan login terlebih dahulu!')
            return

    st.sidebar.title('Menu')
    menu_selection = st.sidebar.radio('Pilih Menu:', ('Home', 'Criteria', 'Daftar', 'Ranking', 'Prediksi', 'Konsultasi'))

    if menu_selection == 'Home':
        home.home()
    elif menu_selection == 'Criteria':
        criteria.criteria()
    elif menu_selection == 'Daftar':
        daftar.daftar()
    elif menu_selection == 'Ranking':
        ranking.show_ranking()
    elif menu_selection == 'Prediksi':
        prediksi.prediksi()
    elif menu_selection == 'Konsultasi':
        konsultasi.chatbot()


if __name__ == "__main__":
    main()
