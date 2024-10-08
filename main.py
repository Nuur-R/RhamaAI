import asyncio
from dotenv import load_dotenv
from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli, llm
from livekit.agents.voice_assistant import VoiceAssistant
from livekit.plugins import openai, silero

load_dotenv()

async def entrypoint(ctx: JobContext):
    initial_ctx =  llm.ChatContext().append(
        role="system",
        text=(
            "You are a helpful voice assistant create by LiveKit. Your interface with users will be in the form of a voice assistant. "
            "You should respond to user questions in a friendly and helpful manner in short and to the point response."
        ),
    )
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    assistant = VoiceAssistant(
        vad=silero.VAD.load(),
        stt=openai.STT(),
        llm=openai.LLM.with_groq(api_key="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", model="llama3-8b-8192"),
        tts=openai.TTS(),
        chat_ctx=initial_ctx
    )
    assistant.start(ctx.room)

    await asyncio.sleep(1)
    await assistant.say("Hai... What up???", allow_interruption=True)

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))