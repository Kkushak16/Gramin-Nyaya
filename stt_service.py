import wave
from faster_whisper import WhisperModel

# 'base' is used for speed; change to 'small' if you need higher accuracy
model_size = "base" 
stt_model = WhisperModel(model_size, device="cpu", compute_type="int8") 

def record_and_transcribe(file_path=None, language="hi"):
    WAVE_OUTPUT_FILENAME = file_path if file_path else "user_voice.wav"

    if not file_path:
        import pyaudio
        CHUNK, FORMAT, CHANNELS, RATE = 1024, pyaudio.paInt16, 1, 16000
        RECORD_SECONDS = 6 

        p = pyaudio.PyAudio()
        print("\n🎤 बोलिए (Speak now)...")
        
        stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
        frames = [stream.read(CHUNK) for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS))]

        print("🛑 रिकॉर्डिंग बंद।")
        stream.stop_stream()
        stream.close()
        p.terminate()

        with wave.open(WAVE_OUTPUT_FILENAME, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))

    # Determine standard Whisper language key (defaults to 'hi' for regional Devanagari dialects)
    whisper_lang = "hi"
    if language == "en":
        whisper_lang = "en"

    # Transcribe with legal context bias to help recognize words like 'Registry'
    segments, _ = stt_model.transcribe(
        WAVE_OUTPUT_FILENAME, 
        language=whisper_lang, 
        beam_size=5,
        initial_prompt="पंजीकरण अधिनियम, रजिस्ट्री, कानूनी दस्तावेज, धारा, नियम।" 
    )
    
    return "".join([segment.text for segment in segments])