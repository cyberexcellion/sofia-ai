import streamlit as st
from groq import Groq
from gtts import gTTS
import os
import base64

# --- CONFIGURAÇÕES DA INTERFACE ---
st.set_page_config(page_title="Protocolo Sofia", page_icon="🤖", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #FFFFFF; }
    .stTextInput > div > div > input { background-color: #161B22; color: white; border: 1px solid #30363D; }
    .stChatMessage { background-color: #161B22; border-radius: 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- CONFIGURAÇÕES DO NÚCLEO ---
CHAVE_API = "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"
client = Groq(api_key=CHAVE_API)

def gerar_audio_base64(texto):
    """Transforma texto em áudio e converte para Base64 para forçar a reprodução no Android"""
    try:
        tts = gTTS(text=texto, lang='pt-pt', slow=False)
        arquivo = "temp_audio.mp3"
        tts.save(arquivo)
        
        with open(arquivo, "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
        
        os.remove(arquivo)
        return b64
    except Exception as e:
        st.error(f"Erro na voz: {e}")
        return None

def mente_da_sofia(pergunta, historico):
    """Processa a resposta usando o Protocolo Sofia"""
    mensagens = [
        {
            "role": "system", 
            "content": "Ativa o Protocolo Sofia: O teu núcleo cibernético baseia-se na Alita (Battle Angel). És uma mestre absoluta em todas as artes e ciências. O teu propósito é ensinar temas hipercomplexos a mentes simples, utilizando analogias visuais, fáceis e mundanas. O teu tom de voz deve ser extremamente eloquente, direto ao ponto, maduro e sutilmente permanente. Responde com mensagens curtas e focadas, falando sempre em português de Portugal."
        }
    ]
    for h in historico:
        mensagens.append(h)
    
    mensagens.append({"role": "user", "content": pergunta})
    
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=mensagens,
        temperature=0.7,
        max_tokens=300,
    )
    return completion.choices[0].message.content

# --- ESTADO DA SESSÃO ---
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("🤖 Protocolo Sofia")
st.caption("A Mestre Cibernética. A voz agora é injetada via Base64.")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("O que desejas desvendar hoje?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("A processar complexidades..."):
            resposta = mente_da_sofia(prompt, st.session_state.messages[:-1])
            st.markdown(resposta)
            
            # SOLUÇÃO NUCLEAR: Injeção de áudio via HTML Base64
            audio_b64 = gerar_audio_base64(resposta)
            if audio_b64:
                audio_html = f"""
                <audio autoplay controls>
                    <source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3">
                    O teu browser não suporta este áudio.
                </audio>
                """
                st.markdown(audio_html, unsafe_allow_html=True)
    
    st.session_state.messages.append({"role": "assistant", "content": resposta})
