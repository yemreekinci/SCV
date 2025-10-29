import streamlit as st
from cvTemplate import create_cv
import base64

st.set_page_config(page_title="SCV", layout="centered")
st.title("SCV")
st.write("Dakikalar içinde profesyonel, sade ve etkileyici bir özgeçmiş oluşturun.")

def to_upper_tr(text):
    translation_table = str.maketrans("iığüşöç", "İIĞÜŞÖÇ")
    return text.translate(translation_table).upper()

with st.form("cv_form"):
    name = to_upper_tr(st.text_input("Ad Soyad"))
    title = to_upper_tr(st.text_input("Meslek Ünvanı"))
    telephone = st.text_input("Telefon")
    email = st.text_input("E-posta").lower()
    web = st.text_input("Web Sitesi").lower()
    address = st.text_input("Konum Bilgisi")
    linkedin = st.text_input("LinkedIn")
    github = st.text_input("GitHub")
    skills = st.text_area("Yetenekler")
    languages = st.text_area("Yabancı Dil(ler)")
    references = st.text_area("Referanslar")
    about = st.text_area("Hakkımda")
    experience = st.text_area("Deneyim")
    education = st.text_area("Eğitim")
    certificates = st.text_area("Sertifika & Başarılar")
    projects = st.text_area("Projeler")
    submitted = st.form_submit_button("CV Oluştur")

if submitted:
    data = {
        "name": name,
        "title": title,
        "email": email,
        "telephone": telephone,
        "web": web,
        "address": address,
        "linkedin": linkedin,
        "github": github,
        "languages": languages,
        "about": about,
        "experience": experience,
        "education": education,
        "skills": skills,
        "certificates": certificates,
        "projects": projects,
        "references": references
    }

    pdf_bytesio = create_cv(data)
    pdf_bytes = pdf_bytesio.getvalue()

    st.download_button(
        "CV İndir",
        pdf_bytes,
        file_name=f"{name}.pdf",
        mime="application/pdf"
    )

    st.subheader("CV Önizleme")
    base64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
    pdf_display = f'''
        <iframe 
            src="data:application/pdf;base64,{base64_pdf}" 
            width="700" 
            height="900" 
            type="application/pdf">
        </iframe>
    '''
    st.markdown(pdf_display, unsafe_allow_html=True)

