import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import os

# 1. CONFIGURAÇÕES DA PÁGINA
st.set_page_config(page_title="Gerador Fireng", page_icon="🔥", layout="centered")

st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        background-color: #FF4B2B;
        color: white;
        font-weight: bold;
        border-radius: 5px;
        border: none;
        height: 3em;
    }
    .stButton>button:hover { background-color: #E63E1C; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🔥 Gerador de Assinaturas")
st.subheader("Preencha os dados abaixo:")

# 2. FORMULÁRIO
nome = st.text_input("Nome e Sobrenome:")
setor = st.text_input("Setor:")
col_tel, col_mail = st.columns(2)
with col_tel:
    telefone = st.text_input("Telefone:", placeholder="(71) 98183-5539")
with col_mail:
    email = st.text_input("E-mail Corporativo:", placeholder="vendas@fireng.com.br")

SITE_FIXO = "www.fireng.com.br"
TEMPLATE_PATH = "template_limpo.png" 
FONT_DIR = "fontes"

if st.button("GERAR MINHA ASSINATURA"):
    if nome and setor and telefone and email:
        try:
            img = Image.open(TEMPLATE_PATH)
            draw = ImageDraw.Draw(img)
            
            f_bold = os.path.join(FONT_DIR, "GoogleSans-Bold.ttf")
            f_reg = os.path.join(FONT_DIR, "GoogleSans-Regular.ttf")
            
            # Ajustei os tamanhos para caberem melhor
            font_nome = ImageFont.truetype(f_bold, 32)
            font_info = ImageFont.truetype(f_reg, 18)
            
            # --- NOVA MIRA (COORDENADAS) ---
            # Aumentei o x_pos para o texto começar depois da logo
            x_pos = 380 
            y_start = 100 # Desci um pouco para alinhar
            y_offset = 30 # Espaço entre linhas
            
            # Nome
            draw.text((x_pos, y_start), nome.upper(), font=font_nome, fill=(30, 30, 30))
            
            # Informações (Setor, Fone, Email, Site)
            current_y = y_start + 45
            infos = [setor, f"Fone: {telefone}", f"E-mail: {email}", f"Site: {SITE_FIXO}"]
            
            for info in infos:
                draw.text((x_pos, current_y), info, font=font_info, fill=(100, 100, 100))
                current_y += y_offset
            
            st.markdown("---")
            st.image(img, caption="Agora sim! Verifique o alinhamento.", use_column_width=True)
            
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            st.download_button(
                label="💾 BAIXAR ASSINATURA",
                data=buf.getvalue(),
                file_name=f"Assinatura_{nome.replace(' ', '_')}.png",
                mime="image/png"
            )
        except Exception as e:
            st.error(f"Erro: {e}")
    else:
        st.warning("Preencha todos os campos.")
