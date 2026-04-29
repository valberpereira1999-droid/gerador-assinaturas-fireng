import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import os

# 1. CONFIGURAÇÕES DA PÁGINA
st.set_page_config(page_title="Gerador Fireng", page_icon="🔥", layout="centered")

# CSS para deixar o botão laranja e o visual profissional
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
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #E63E1C;
        border: none;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. EXIBIÇÃO DA LOGO NO TOPO
# Tenta carregar a logo. Se não existir, pula silenciosamente.
if os.path.exists("logo.png"):
    st.image("logo.png", width=220)
else:
    st.caption("🔥 Fireng Engenharia")

# 3. CABEÇALHO E FORMULÁRIO
st.title("Gerador de Assinaturas")
st.subheader("Preencha os dados abaixo:")

with st.container():
    nome = st.text_input("Nome e Sobrenome:")
    setor = st.text_input("Setor:")
    
    col_tel, col_mail = st.columns(2)
    with col_tel:
        telefone = st.text_input("Telefone:", placeholder="(71) 99999-9999")
    with col_mail:
        email = st.text_input("E-mail Corporativo:", placeholder="seu.nome@fireng.com.br")

# Site fixo que sairá na assinatura
SITE_FIXO = "www.fireng.com.br"

# 4. CONFIGURAÇÃO DE ARQUIVOS
FONT_DIR = "fontes"
TEMPLATE_PATH = "template_limpo.png"

if st.button("GERAR MINHA ASSINATURA"):
    if nome and setor and telefone and email:
        try:
            with st.spinner('Construindo sua assinatura...'):
                # Carregamento dos recursos
                img = Image.open(TEMPLATE_PATH)
                draw = ImageDraw.Draw(img)
                
                # Definindo caminhos das fontes
                f_bold = os.path.join(FONT_DIR, "GoogleSans-Bold.ttf")
                f_reg = os.path.join(FONT_DIR, "GoogleSans-Regular.ttf")
                
                # Tamanhos das fontes
                font_nome = ImageFont.truetype(f_bold, 38)
                font_info = ImageFont.truetype(f_reg, 22)
                
                # --- DESENHO NA IMAGEM ---
                # Coordenadas (Ajuste x_pos se precisar chegar mais para o lado)
                x_pos = 450
                y_start = 80
                y_offset = 40
                
                # Escreve o Nome em Maiúsculo
                draw.text((x_pos, y_start), nome.upper(), font=font_nome, fill=(0, 0, 0))
                
                # Escreve as demais informações abaixo
                current_y = y_start + 55
                
                # Setor/Cargo
                draw.text((x_pos, current_y), setor, font=font_info, fill=(80, 80, 80))
                current_y += y_offset
                
                # Telefone
                draw.text((x_pos, current_y), f"Fone: {telefone}", font=font_info, fill=(80, 80, 80))
                current_y += y_offset
                
                # E-mail
                draw.text((x_pos, current_y), f"E-mail: {email}", font=font_info, fill=(80, 80, 80))
                current_y += y_offset
                
                # Site (Fixo)
                draw.text((x_pos, current_y), f"Site: {SITE_FIXO}", font=font_info, fill=(80, 80, 80))
                
                # --- EXIBIÇÃO E DOWNLOAD ---
                st.markdown("---")
                st.image(img, caption="Prévia da Assinatura", use_column_width=True)
                
                # Preparar buffer para download
                buf = io.BytesIO()
                img.save(buf, format="PNG")
                
                st.download_button(
                    label="💾 BAIXAR ASSINATURA AGORA",
                    data=buf.getvalue(),
                    file_name=f"Assinatura_{nome.replace(' ', '_')}.png",
                    mime="image/png"
                )
                
        except Exception as e:
            st.error(f"Erro inesperado: {e}")
    else:
        st.warning("⚠️ Preencha todos os campos para continuar.")

# 5. RODAPÉ
st.markdown("---")
st.caption("© 2026 Fireng Engenharia - Sistema Interno de Padronização")
