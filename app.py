import streamlit as st
import pandas as pd

# Cargar los datos con los nombres definitivos
df = pd.read_csv("comparacion_salmos_nueva_version_def.csv")

st.set_page_config(page_title="Text Comparision of Psalms editions (1553 vs 1554) / Comparador de versiones del Salterio")

st.title("📜 Text Comparision of Psalms editions (1553 vs 1554)/Comparador de versiones del Salterio Sefardí (1553 vs 1554)")

# Añadir pestañas para navegación
pestañas = st.tabs(["Search versicle / Buscar versículo", "Global differences / Diferencias globales"])

with pestañas[0]:
    # Buscador de palabra en los textos
    busqueda = st.text_input("🔎 Search word in both editions / Buscar palabra en cualquiera de las versiones")
    if busqueda:
        resultados = df[
            df["Text_V1"].str.contains(busqueda, case=False, na=False) |
            df["Text_V2"].str.contains(busqueda, case=False, na=False)
        ]
        if resultados.empty:
            st.warning(" No results /No se encontraron versículos que contengan esa palabra.")
        else:
            st.markdown(f"### Results / Resultados para '{busqueda}':")
            st.dataframe(resultados[["Chapter", "Verse", "Text_V1", "Text_V2"]].rename(columns={
                "Chapter": "Salmo", "Verse": "Versículo",
                "Text_V1": "Versión 1553", "Text_V2": "Versión 1554"
            }), use_container_width=True)
    else:
        # Selección de capítulo
        capitulos = df["Chapter"].unique()
        chapter_sel = st.selectbox("Select a chapter / Selecciona un capítulo (Salmo)", sorted(capitulos))

        # Selección de versículo
        versiculos = df[df["Chapter"] == chapter_sel]["Verse"].unique()
        verse_sel = st.selectbox("Select a verse /Selecciona un versículo", sorted(versiculos))

        # Fila correspondiente
        fila = df[(df["Chapter"] == chapter_sel) & (df["Verse"] == verse_sel)].iloc[0]

        # Mostrar texto completo
        st.markdown(f"### 📖 Salmo {chapter_sel}:{verse_sel}")
        st.markdown("**Versión 1553:**")
        st.markdown(f"`{fila['Text_V1']}`")
        st.markdown("**Versión 1554:**")
        st.markdown(f"`{fila['Text_V2']}`")

        # Mostrar diferencias
        if fila["Cambios_v1"] or fila["Cambios_v2"]:
            st.markdown("### 🔍 Differences between editions / Diferencias entre versiones:")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Only in ed.1553 / Solo en versión 1553:**")
                st.markdown(f"`{fila['Cambios_v1']}`")
            with col2:
                st.markdown("**Only in ed. 1554 / Solo en versión 1554:**")
                st.markdown(f"`{fila['Cambios_v2']}`")
        else:
            st.info("✔ No differences / No se encontraron diferencias en este versículo.")

with pestañas[1]:
    st.markdown("## 📑 Global visualization of differences / Vista global de diferencias")
    df_diferencias = df[(df["Cambios_v1"].str.strip() != '') | (df["Cambios_v2"].str.strip() != '')]

    if df_diferencias.empty:
        st.info("No differences/ No se encontraron diferencias entre las versiones.")
    else:
        df_mostrar = df_diferencias[["Chapter", "Verse", "Cambios_v1", "Cambios_v2"]].rename(columns={
            "Chapter": "Salmo",
            "Verse": "Versículo",
            "Cambios_v1": "Diferencias 1553",
            "Cambios_v2": "Diferencias 1554"
        })
        st.dataframe(df_mostrar, use_container_width=True)
