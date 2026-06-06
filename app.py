import streamlit as st
from groq import Groq

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

# --- FUNÇÃO DE VOZ VIA JAVASCRIPT (O Segredo da Solução) ---
def falar_no_browser(texto):
    """Injeta JavaScript para forçar o Android a falar usando a voz nativa do sistema"""
    # Escapamos as aspas para não quebrar o JavaScript
    texto_escapado = texto.replace('"', '\\"').replace('\n', ' ')
    
    js_code = f"""
    <script>
    var msg = new SpeechSynthesisUtterance('{texto_escapado}');
    msg.lang = 'pt-PT';
    msg.rate = 0.9; // Velocidade ligeiramente mais lenta para soar madura
    msg.pitch = 1.0;
    window.speechSynthesis.speak(msg);
    </script>
    """
    st.markdown(js_code, unsafe_allow_html=True)

# --- ESTADO DA SESSÃO ---
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("🤖 Protocolo Sofia")
st.caption("Versão Suprema: Voz Nativa do Sistema (Web Speech API)")

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
            
            # A SOLUÇÃO SUPREMA: Comando direto ao sistema do Android
            falar_no_browser(resposta)
    
    st.session_state.messages.append({"role": "assistant", "content": resposta})
