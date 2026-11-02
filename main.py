import base64
import os
import requests
from dotenv import load_dotenv
from google import genai


# carrega as variaveis do arquivo .env
load_dotenv()

spotify_client_id = os.getenv("SPOTIFY_CLIENT_ID")
spotify_client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
gemini_api_key = os.getenv("GEMINI_API_KEY")

# autenticação no spotify
credenciais = f"{spotify_client_id}:{spotify_client_secret}"
credenciais_base64 = base64.b64encode(credenciais.encode()).decode()

resposta_token = requests.post(
    "https://accounts.spotify.com/api/token",
    headers={
        "Authorization": f"Basic {credenciais_base64}",
        "Content-Type": "application/x-www-form-urlencoded",
    },
    data={"grant_type": "client_credentials"},
)
token = resposta_token.json()["access_token"]

# buscar artista no spotify
artista_busca = input("Digite o nome de um artista: ")
resposta_artista = requests.get(
    "https://api.spotify.com/v1/search",
    headers={"Authorization": f"Bearer {token}"},
    params={"q": artista_busca, "type": "artist", "limit": 1},
)
artista = resposta_artista.json()["artists"]["items"][0]
nome_artista = artista["name"]
generos = input("Digite o gênero musical do artista: ")

# envia os dados do artista para o gemini
prompt = (
    f"Sugira 3 músicas de outros artistas parecidas com {nome_artista}. "
    f"Os gêneros informados são: {generos}. Responda em português e justifique brevemente."
)

cliente = genai.Client(api_key=gemini_api_key)
resposta_gemini = cliente.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents=prompt,
)

print(resposta_gemini.text)
