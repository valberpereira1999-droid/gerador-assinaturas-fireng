import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import os

# 1. CONFIGURAÇÕES DA PÁGINA
st.set_page_config(page_title="Gerador Fireng", page_icon="🔥", layout="centered")

# CSS para customização visual
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
    .stButton>button:hover {
        background-color: #E63E1C;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. CABEÇALHO (Removida a imagem grande para melhor visualização)
st.title("🔥 Gerador de Assinaturas")
st.subheader("Preencha os dados abaixo:")

# 3. FORMULÁRIO
with st.container():
    nome = st.text_input("Nome e Sobrenome:")
    setor = st.text_input("Setor:")
    
    col_tel, col_mail = st.columns(2)
    with col_tel:
        telefone = st.text_input("Telefone:", placeholder="(71) 98183-5539")
    with col_mail:
        email = st.text_input("E-mail Corporativo:", placeholder="vendas@fireng.com.br")

SITE_FIXO = "www.fireng.com.br"

# 4. CONFIGURAÇÃO DE ARQUIVOS (Ajustado para o que está no seu GitHub)
FONT_DIR = "fontes"
# Mudamos para .png para bater com o arquivo que você subiu
TEMPLATE_PATH = "template_limpo.png" 

if st.button("GERAR MINHA ASSINATURA"):
    if nome and setor and telefone and email:
        try:
            with st.spinner('Construindo sua assinatura...'):
                img = Image.open(TEMPLATE_PATH)
                draw = ImageDraw.Draw(img)
                
                f_bold = os.path.join(FONT_DIR, "GoogleSans-Bold.ttf")
                f_reg = os.path.join(FONT_DIR, "GoogleSans-Regular.ttf")
                
                font_nome = ImageFont.truetype(f_bold, 38)
                font_info = ImageFont.truetype(f_reg, 22)
                
                # Coordenadas de desenho
                x_pos = 450
                y_start = 80
                y_offset = 40
                
                # Nome
                draw.text((x_pos, y_start), nome.upper(), font=font_nome, fill=(0, 0, 0))
                
                # Dados
                current_y = y_start + 55
                draw.text((x_pos, current_y), setor, font=font_info, fill=(80, 80, 80))
                current_y += y_offset
                draw.text((x_pos, current_y), f"Fone: {telefone}", font=font_info, fill=(80, 80, 80))
                current_y += y_offset
                draw.text((x_pos, current_y), f"E-mail: {email}", font=font_info, fill=(80, 80, 80))
                current_y += y_offset
                draw.text((x_pos, current_y), f"Site: {SITE_FIXO}", font=font_info, fill=(80, 80, 80))
                
                st.markdown("---")
                st.image(img, caption="Sua assinatura pronta!", use_column_width=True)
                
                buf = io.BytesIO()
                img.save(buf, format="PNG")
                st.download_button(
                    label="💾 BAIXAR ASSINATURA",
                    data=buf.getvalue(),
                    file_name=f"Assinatura_{nome.replace(' ', '_')}.png",
                    mime="image/png"
                )
        except Exception as e:
            st.error(f"Erro: Verifique se o arquivo 'template_limpo.png' e as fontes estão na pasta. Detalhe: {e}")
    else:
        st.warning("⚠️ Preencha todos os campos.")

st.markdown("---")
st.caption("© 2026 Fireng Engenharia")
