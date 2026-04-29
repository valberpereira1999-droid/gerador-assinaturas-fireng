if st.button("GERAR MINHA ASSINATURA"):
    if nome and setor and telefone and email:
        try:
            img = Image.open(TEMPLATE_PATH)
            draw = ImageDraw.Draw(img)
            
            f_bold = os.path.join(FONT_DIR, "GoogleSans-Bold.ttf")
            f_reg = os.path.join(FONT_DIR, "GoogleSans-Regular.ttf")
            
            # Fontes levemente maiores para aproveitar o espaço branco
            font_nome = ImageFont.truetype(f_bold, 35)
            font_info = ImageFont.truetype(f_reg, 20)
            
            # --- AJUSTE DE MIRA (X e Y) ---
            x_pos = 420 # Posição horizontal (mais para a direita)
            y_start = 65 # Posição vertical (mais para cima)
            y_offset = 35 # Espaço entre as linhas
            
            # Nome
            draw.text((x_pos, y_start), nome.upper(), font=font_nome, fill=(30, 30, 30))
            
            # Linhas de informação
            current_y = y_start + 50
            infos = [setor, f"Fone: {telefone}", f"E-mail: {email}", f"Site: {SITE_FIXO}"]
            
            for info in infos:
                draw.text((x_pos, current_y), info, font=font_info, fill=(80, 80, 80))
                current_y += y_offset
            
            st.markdown("---")
            st.image(img, caption="Verifique agora se o texto saiu da frente da logo!", use_column_width=True)
            
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
