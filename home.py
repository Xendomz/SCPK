import streamlit as st

def home():
    st.title('Welcome to Stroke Prediction App')
    st.write('This app helps you to predict whether you are at risk of having a stroke or not')
    st.image('https://d1vbn70lmn1nqe.cloudfront.net/prod/wp-content/uploads/2022/07/06032532/Stroke-pada-Lansia-Waspada-Faktor-Risikonya.jpg', width=600)
    st.write('Stroke is one of the most dangerous diseases and causes many deaths. Stroke is a disease that can result in loss of ability and loss of life. Stroke is a disease that can result in loss of ability and loss of life. Stroke is a disease that can result in loss of ability and loss of life. This application will help you to find out the potential for stroke in yourself and find out the risk factors associated with the possibility of someone having a stroke.')

if __name__ == "__main__":
    home()
