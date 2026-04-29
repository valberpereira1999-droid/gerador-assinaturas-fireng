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

# 3. LÓGICA DE GERAÇÃO
if st.button("GERAR MINHA ASSINATURA"):
    if nome and setor and telefone and email:
        try:
            img = Image.open(TEMPLATE_PATH)
            draw = ImageDraw.Draw(img)
            
            f_bold = os.path.join(FONT_DIR, "GoogleSans-Bold.ttf")
            f_reg = os.path.join(FONT_DIR, "GoogleSans-Regular.ttf")
            
            font_nome = ImageFont.truetype(f_bold, 35)
            font_info = ImageFont.truetype(f_reg, 20)
            
            # --- AJUSTE FINAL DE POSIÇÃO ---
            x_pos = 450 # Texto bem à direita para fugir da logo
            y_start = 65 
            y_offset = 35 
            
            # Desenha o Nome
            draw.text((x_pos, y_start), nome.upper(), font=font_nome, fill=(30, 30, 30))
            
            # Desenha as demais informações
            current_y = y_start + 50
            infos = [setor, f"Fone: {telefone}", f"E-mail: {email}", f"Site: {SITE_FIXO}"]
            
            for info in infos:
                draw.text((x_pos, current_y), info, font=font_info, fill=(80, 80, 80))
                current_y += y_offset
            
            st.markdown("---")
            st.image(img, caption="Assinatura Gerada", use_column_width=True)
            
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            st.download_button(
                label="💾 BAIXAR ASSINATURA",
                data=buf.getvalue(),
                file_name=f"Assinatura_{nome.replace(' ', '_')}.png",
                mime="image/png"
            )
        except Exception as e:
            st.error(f"Erro técnico: {e}")
    else:
        st.warning("Preencha todos os campos.")
