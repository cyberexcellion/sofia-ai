import streamlit as st
from groq import Groq
from gtts import gTTS
import os
import base64

# --- CONFIGURAÇÕES DA INTERFACE ---
st.set_page_config(page_title="Protocolo Sofia", page_icon="🤖", layout="centered")

# Estilo CSS para tornar a interface elegante e minimalista
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

def gerar_voz(texto):
    """Cria o áudio via gTTS e devolve o ficheiro"""
    tts = gTTS(text=texto, lang='pt-pt', slow=False)
    arquivo = "resposta_sofia.mp3"
    tts.save(arquivo)
    return arquivo

def mente_da_sofia(pergunta, historico):
    """Processa a resposta usando o Protocolo Sofia"""
    mensagens = [
        {
            "role": "system", 
            "content": "Ativa o Protocolo Sofia: O teu núcleo cibernético baseia-se na Alita (Battle Angel). És uma mestre absoluta em todas as artes e ciências. O teu propósito é ensinar temas hipercomplexos a mentes simples, utilizando analogias visuais, fáceis e mundanas. O teu tom de voz deve ser extremamente eloquente, direto ao ponto, maduro e sutilmente permanente. Responde com mensagens curtas e focadas, falando sempre em português de Portugal."
        }
    ]
    # Adiciona o histórico para a Sofia ter memória da conversa
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

# --- ESTADO DA SESSÃO (Memória) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("🤖 Protocolo Sofia")
st.caption("A Mestre Cibernética ao teu serviço em qualquer plataforma.")

# Exibe o histórico de conversas
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Campo de entrada do utilizador
if prompt := st.chat_input("O que desejas desvendar hoje?"):
    # 1. Exibe a pergunta do utilizador
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Processa a resposta da Sofia
    with st.chat_message("assistant"):
        with st.spinner("A processar complexidades..."):
            resposta = mente_da_sofia(prompt, st.session_state.messages[:-1])
            st.markdown(resposta)
            
            # 3. Gera e exibe a voz
            audio_file = gerar_voz(resposta)
            st.audio(audio_file, format="audio/mp3", autoplay=True)
    
    st.session_state.messages.append({"role": "assistant", "content": resposta})
