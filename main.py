import asyncio
from dotenv import load_dotenv
from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli, llm
from livekit.agents.voice_assistant import VoiceAssistant
from livekit.plugins import openai, silero, deepgram, elevenlabs, cartesia
from api import AssistantFnc

load_dotenv()

# Function to adjust load threshold for the worker
def set_worker_options():
    # Define custom worker load threshold (higher than the default of 0.75 in production)
    return WorkerOptions(
        load_threshold=0.95,  # Set to a higher threshold for better handling
        entrypoint_fnc=entrypoint
    )

async def entrypoint(ctx: JobContext):
    initial_ctx = llm.ChatContext().append(
        role="system",
        text=(
            "You are a voice assistant created by LiveKit. Your interface with users will be voice. "
            "You should use short and concise responses, avoiding usage of unpronounceable punctuation."
        ),
    )
    
    # Try connecting to the context and check if the worker is available
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)
    fnc_ctx = AssistantFnc()

    # assistant = VoiceAssistant(
    #     vad=silero.VAD.load(),
    #     stt=deepgram.STT(),
    #     llm=openai.LLM.with_groq(api_key="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", model="llama3-8b-8192"),
    #     tts=elevenlabs.TTS(model_id="eleven_turbo_v2"),
    #     chat_ctx=initial_ctx,
    #     fnc_ctx=fnc_ctx,
    # )

    assistant = VoiceAssistant(
        vad=silero.VAD.load(),
        stt=deepgram.STT(),
        llm=openai.LLM(model="gpt-4o-mini"),
        tts=cartesia.TTS(model="sonic-english"),
        chat_ctx=initial_ctx,
        fnc_ctx=fnc_ctx,
    )
    
    # Monitor the assistant's connection and load
    try:
        assistant.start(ctx.room)

        # Brief delay to ensure smooth connection
        await asyncio.sleep(0.5)  
        await assistant.say("Hey, how can I help you today!", allow_interruptions=True)
    except Exception as e:
        # Log any issues related to assistant start or load capacity
        print(f"Error starting assistant: {e}")

if __name__ == "__main__":
    # Set custom worker options with higher threshold and run the app
    cli.run_app(set_worker_options())
