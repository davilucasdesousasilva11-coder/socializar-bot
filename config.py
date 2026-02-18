import os
import discord
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv("TOKEN")

# ===== IDS =====

OWNER_ID = 1330568796511014922
YUME_ID = 809826760241053737

# ===== IDENTIDADE =====
BOT_NAME = "Socializar"
BOT_VERSION = "0.0.2"
PREFIX = "$"

# ===== EMBED COLORS =====

EMBED_COLOR_BASE = 0x4A90E2
# padrão azul
EMBED_COLOR_SUCESS = 0x57F287
# sucesso verde
EMBED_COLOR_WARNING = 0XFEE75C
# aviso amarelo
EMBED_COLOR_ERROR = 0xED4245
# vermelho erro
EMBED_COLOR_INFO = 0xFF6FAE
# rosa info

# ===== HUMOR =====

HUMOR_NEUTRO_EMOJI = "😐"
HUMOR_FELIZ_EMOJI = "🥳"
HUMOR_REVOLTADO_EMOJI = "😤"
HUMOR_MOTIVADO_EMOJI = "🔥"
HUMOR_DESCONFIADO_EMOJI = "🤨"
HUMOR_ASSSUSTADO_EMOJI = "😱"
HUMOR_TRISTE_EMOJI = "😭"
HUMOR_AMOROSO_EMOJI = "😍"
HUMOR_PENSATIVO_EMOJI = "🤔"
HUMOR_CANSADO_EMOJI = "😴"
HUMOR_JOESTAR_EMOJI = "🌀"

# ===== TEMAS =====

TEMA_ATUAL = "ryo_joestar"

# ===== MENSAGENS PADRÃO =====

MSG_SEM_PERMISSAO = "🚫 Você não tem nível/permissões o suficiente para esta ação."
MSG_ERRO_PADRAO = "❌ Algo deu errado... Culpa da Kio-sama!"
MSG_SUCESSO_PADRAO = "✅ Funcionou! Mas não se acostume, erros são constantes aqui."

# ===== USOS =====

USE_JOJO_REFERENCES = True
USE_TYPING_EFFECT = True
USE_STATUS_SYSTEM = True

# ===== DELAYS =====

TYPING_DELAY = 1.5

INTENTS = discord.Intents.default()
INTENTS.message_content = True
INTENTS.members = True

SARCASM_LEVEL = 0.3