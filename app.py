import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import os

# 1. CONFIGURAÇÕES DA PÁGINA
st.set_page_config(page_title="Gerador Fireng", page_icon="🔥", layout="centered")

# Customização do botão para o padrão laranja Fireng
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        background-color: #F37021;
        color: white;
        font-weight: bold;
        border-radius: 5px;
        border: none;
        height: 3em;
    }
    .stButton>button:hover { background-color: #D65A10; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- CONFIGURAÇÕES DE LAYOUT (ORIGINAIS DO SEU EXE) ---
TAMANHO_NOME = 65           
TAMANHO_DADOS = 38          
TAMANHO_ICON = (38, 38)     
COORDENADA_X = 885          
Y_NOME = 65                 
Y_CARGO = 145               
Y_LINHA_HORIZONTAL = 200    
Y_CONTATOS_INICIAL = 250    
ESPACAMENTO_LINHAS = 65     
LARGURA_LINHA = 500        
RECUO_TEXTO = 55            
# Links para o site
SITE_URL = "https://www.fireng.com.br"
SITE_DISPLAY = "www.fireng.com.br"
TEMPLATE_PATH = "template_limpo.png" 
FONT_DIR = "fontes"

# --- SEU AJUSTE MÁGICO DE ALINHAMENTO ---
ADJUST_Y_TEXT = -6

st.title("🔥 Gerador de Assinaturas")

# LINK CLICÁVEL NO TOPO
st.markdown(f"Acesse o site oficial: [{SITE_DISPLAY}]({SITE_URL})")
st.subheader("Dados da Assinatura")

# 2. CAMPOS DE ENTRADA
nome = st.text_input("Nome e Sobrenome:")
cargo = st.text_input("Cargo/Setor:")
col_tel, col_mail = st.columns(2)
with col_tel:
    telefone = st.text_input("Telefone:", value="(71) 3026-0721")
with col_mail:
    email = st.text_input("E-mail Corporativo:")

# 3. LÓGICA DE GERAÇÃO
if st.button("GERAR"):
    if nome and cargo and email:
        try:
            # Carrega Template
            img = Image.open(TEMPLATE_PATH).convert("RGBA")
            draw = ImageDraw.Draw(img)
            
            # Fontes
            f_bold = os.path.join(FONT_DIR, "GoogleSans-Bold.ttf")
            f_reg = os.path.join(FONT_DIR, "GoogleSans-Regular.ttf")
            font_n = ImageFont.truetype(f_bold, TAMANHO_NOME)
            font_d = ImageFont.truetype(f_reg, TAMANHO_DADOS)

            # Cores originais
            cor_nome = (26, 26, 26, 255)     
            cor_cargo = (102, 102, 102, 255) 

            # Desenha Nome, Cargo e Linha Horizontal
            draw.text((COORDENADA_X, Y_NOME), nome, font=font_n, fill=cor_nome)
            draw.text((COORDENADA_X, Y_CARGO), cargo, font=font_d, fill=cor_cargo)
            draw.line((COORDENADA_X, Y_LINHA_HORIZONTAL, COORDENADA_X + LARGURA_LINHA, Y_LINHA_HORIZONTAL), fill=cor_cargo, width=3)

            # Ícones e Contatos
            icons_info = [
                ('tel', telefone, Y_CONTATOS_INICIAL, 'telefone.png'),
                ('email', email, Y_CONTATOS_INICIAL + ESPACAMENTO_LINHAS, 'cartinha.png'),
                ('site', SITE_DISPLAY, Y_CONTATOS_INICIAL + (ESPACAMENTO_LINHAS * 2), 'mundo.png')
            ]

            for key, texto, y, icon_name in icons_info:
                icon_path = os.path.join(FONT_DIR, icon_name)
                if os.path.exists(icon_path):
                    icon_img = Image.open(icon_path).convert("RGBA")
                    icon_img = icon_img.resize(TAMANHO_ICON, Image.Resampling.LANCZOS)
                    # Cola o ícone na posição Y padrão
                    img.paste(icon_img, (COORDENADA_X, y), icon_img)
                
                # Desenha o texto com o ajuste vertical para centralizar com o ícone
                draw.text((COORDENADA_X + RECUO_TEXTO, y + ADJUST_Y_TEXT), texto, font=font_d, fill=cor_nome)

            # Exibição no Streamlit
            st.markdown("---")
            st.image(img, caption="PRÉVIA", use_column_width=True)
            
            # Preparar Download
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            st.download_button(
                label="💾 BAIXAR ASSINATURA",
                data=buf.getvalue(),
                file_name=f"Assinatura_{nome.replace(' ', '_')}.png",
                mime="image/png"
            )
            
        except Exception as e:
            st.error(f"Erro ao gerar: {e}")
    else:
        st.warning("⚠️ Preencha Nome, Cargo e E-mail.")

st.markdown("---")
# LINK CLICÁVEL NO RODAPÉ
st.markdown(f"© 2026 [FIRENG ENGENHARIA DE INCÊNDIO]({SITE_URL})")
