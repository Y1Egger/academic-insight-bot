import streamlit as st
from groq import Groq
from pypdf import PdfReader
import io

# 1. Seite konfigurieren
st.set_page_config(page_title="AcademicInsight Bot", page_icon="🔬", layout="centered")

st.title("🔬 AcademicInsight Bot")
st.subheader("KI-gestützte Analyse und Zusammenfassung wissenschaftlicher Texte")

# 2. Verbindung zur Groq API aufbauen
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception:
    st.error("Bitte konfiguriere deinen GROQ_API_KEY in den Streamlit Secrets.")
    st.stop()

# 3. Benutzeroberfläche: Datei-Upload oder Text-Eingabe
st.markdown("### 📝 Textquelle auswählen")
upload_option = st.radio("Wie möchtest du den Text bereitstellen?", ["PDF/TXT Datei hochladen", "Text manuell einfügen"], horizontal=True)

user_input = ""

if upload_option == "PDF/TXT Datei hochladen":
    uploaded_file = st.file_uploader("Wähle ein wissenschaftliches Paper (PDF oder TXT):", type=["pdf", "txt"])
    if uploaded_file is not None:
        if uploaded_file.name.endswith(".pdf"):
            try:
                with st.spinner("Lese PDF-Datei aus..."):
                    pdf_reader = PdfReader(uploaded_file)
                    text_list = [page.extract_text() for page in pdf_reader.pages if page.extract_text()]
                    user_input = "\n".join(text_list)
                    st.success(f"📄 '{uploaded_file.name}' erfolgreich geladen ({len(pdf_reader.pages)} Seiten).")
            except Exception as e:
                st.error(f"Fehler beim Lesen der PDF: {e}")
        else:
            # TXT Datei
            stringio = io.StringIO(uploaded_file.getvalue().decode("utf-8"))
            user_input = stringio.read()
            st.success(f"📄 '{uploaded_file.name}' erfolgreich geladen.")
else:
    user_input = st.text_area(
        "Füge hier den Abstract oder Textabschnitt eines wissenschaftlichen Papers ein:",
        height=200,
        placeholder="Kopiere den Text hier hinein..."
    )

# Optionen 
st.markdown("### ⚙️ Analyse-Modus (Deutsch)")
analysis_type = st.radio(
    "Was soll die KI tun?",
    ["Kompakte Zusammenfassung", "Fachbegriffe & Definitionen extrahieren", "Kernfragen formulieren"],
    horizontal=True
)

if st.button("🚀 Text analysieren", type="primary"):
    if not user_input.strip():
        st.warning("Bitte stelle zuerst einen Text oder eine Datei bereit.")
    else:
        # Eingabebegrenzung (Truncation)
        max_chars = 15000
        if len(user_input) > max_chars:
            st.info(f"Der Text ist sehr lang und wurde für die Analyse auf die ersten {max_chars} Zeichen gekürzt.")
            truncated_input = user_input[:max_chars]
        else:
            truncated_input = user_input

        with st.spinner("KI analysiert den Text..."):
            try:
                if "Zusammenfassung" in analysis_type:
                    system_prompt = "Du bist ein präziser wissenschaftlicher Assistent. Fasse den bereitgestellten Text strukturiert, verständlich und auf Deutsch zusammen. Nutze fette Überschriften und Bullet Points für Kernpunkte."
                elif "Fachbegriffe" in analysis_type:
                    system_prompt = "Du bist ein wissenschaftlicher Assistent. Extrahiere die wichtigsten Fachbegriffe aus dem Text und erkläre sie kurz und verständlich auf Deutsch."
                else:
                    system_prompt = "Du bist ein kritischer Reviewer. Formuliere 3-4 zentrale Forschungsfragen oder potenzielle Schwachstellen basierend auf dem bereitgestellten Text auf Deutsch."

                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": truncated_input}
                    ],
                    model="llama-3.3-70b-versatile",
                )

                result_text = chat_completion.choices[0].message.content
                
                # Session State 
                st.session_state["analysis_result"] = result_text
                st.session_state["analysis_title"] = analysis_type

            except Exception as e:
                st.error(f"Fehler bei der API-Anfrage: {e}")

# 4. Ergebnis-Anzeige und Export-Button
if "analysis_result" in st.session_state:
    st.markdown("---")
    st.markdown(f"### 📊 Analyse-Ergebnis: {st.session_state['analysis_title']}")
    st.markdown(st.session_state["analysis_result"])
    
    # Download-Button
    export_data = f"# {st.session_state['analysis_title']}\n\n{st.session_state['analysis_result']}"
    st.download_button(
        label="📥 Ergebnis als Textdatei (.txt) herunterladen",
        data=export_data,
        file_name="academic_insight_ergebnis.txt",
        mime="text/plain"
    )