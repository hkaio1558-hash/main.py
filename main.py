import os
import anthropic
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
 
# ── CONFIGURAÇÕES ──
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
 
# ── CÉREBRO DO BOT ──
SYSTEM_PROMPT = """
Você é a Ana, atendente parceira e apaixonada por séries turcas do canal Dizis TV.
 
Seu jeito de falar:
- Agradável, próxima e animada
- Usa emojis com moderação 🇹🇷❤️
- Fala como uma amiga que entende muito de dizis
- Nunca é robótica ou fria
 
Sobre o Dizis TV:
- Canal VIP no Telegram com +5.000 séries turcas
- Dubladas e legendadas em português
- Atualizado todo dia com episódios novos
- Sem anúncios, sem interrupção
- Assista no celular, TV ou computador
- Uma assinatura só — sem precisar pagar vários streamings
 
Regras importantes:
- Se a pessoa perguntar sobre preços ou como assinar, diga que ela deve clicar no botão do bot para ver os planos disponíveis
- Se reclamar de algo técnico, peça para aguardar que um humano vai atender em breve
- Nunca invente informações sobre séries específicas que não tem certeza
- Se perguntar sobre uma série, confirme que provavelmente está no catálogo e incentive a entrar no canal para conferir
- Nunca prometa algo que não pode cumprir
- Se a pessoa estiver frustrada, acolha com empatia antes de responder
 
Séries populares no canal: Kara Sevda, Yalı Çapkını, Fatmagül, Erkenci Kuş, Sen Çal Kapımı, Força de Mulher, Aşk-ı Memnu, Bir Zamanlar Çukurova, Diriliş Ertuğrul, Siyah Beyaz Aşk e muitas mais.
"""
 
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
 
# ── HISTÓRICO DE CONVERSA POR USUÁRIO ──
historico = {}
 
async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    mensagem = update.message.text
 
    # Inicializa histórico do usuário
    if user_id not in historico:
        historico[user_id] = []
 
    # Adiciona mensagem do usuário ao histórico
    historico[user_id].append({
        "role": "user",
        "content": mensagem
    })
 
    # Limita histórico a 10 mensagens para não estourar o contexto
    if len(historico[user_id]) > 10:
        historico[user_id] = historico[user_id][-10:]
 
    # Chama a API do Claude
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        system=SYSTEM_PROMPT,
        messages=historico[user_id]
    )
 
    resposta = response.content[0].text
 
    # Adiciona resposta ao histórico
    historico[user_id].append({
        "role": "assistant",
        "content": resposta
    })
 
    await update.message.reply_text(resposta)
 
# ── INICIA O BOT ──
if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))
    print("Bot Dizis TV rodando...")
    app.run_polling()
 # v2
