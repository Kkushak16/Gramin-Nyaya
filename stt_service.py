import pyaudio
import wave
from faster_whisper import WhisperModel

# 1. Initialize the UPGRADED STT Model
# 'small' is significantly more accurate for Hindi than 'base'
model_size = "small" 
print(f"--- Loading Professional STT Model ({model_size})... ---")

# Laptop: device="cpu" | Jetson Orin Nano: device="cuda"
stt_model = WhisperModel(model_size, device="cpu", compute_type="int8") 

def record_and_transcribe():
    CHUNK, FORMAT, CHANNELS, RATE = 1024, pyaudio.paInt16, 1, 16000
    RECORD_SECONDS = 7 
    WAVE_OUTPUT_FILENAME = "user_voice.wav"

    p = pyaudio.PyAudio()

    # 2. Record Audio
    print("\n🎤 बोलिए (Speak now)...")
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    frames = [stream.read(CHUNK) for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS))]

    print("🛑 रिकॉर्डिंग बंद (Recording stopped).")
    stream.stop_stream()
    stream.close()
    p.terminate()

    with wave.open(WAVE_OUTPUT_FILENAME, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

    # 3. Transcribe with Legal Context Bias
    print("--- Transcribing with Hindi Context... ---")
    segments, _ = stt_model.transcribe(
        WAVE_OUTPUT_FILENAME, 
        language="hi", 
        # Adding keywords helps the model recognize legal terms better
        initial_prompt="पंजीकरण अधिनियम, रजिस्ट्री, कानूनी दस्तावेज, धारा, नियम।" 
    )
    
    return "".join([segment.text for segment in segments])

if __name__ == "__main__":
    print(f"पहचाना गया: {record_and_transcribe()}")