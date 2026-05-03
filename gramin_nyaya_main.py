from stt_service import record_and_transcribe
from rag_logic import ask_gramin_nyaya

def start_system():
    print("\n" + "="*45)
    print("GRAMIN-NYAYA: AI LEGAL ASSISTANT (UPGRADED)")
    print("="*45)
    
    while True:
        choice = input("\nप्रेस करें 'Enter' और अपना सवाल बोलें (या 'exit' लिखें): ")
        if choice.lower() == 'exit':
            break
        
        # user_text = record_and_transcribe() # Comment this out for now
        user_text = input("\nType your question (e.g., 'रजिस्ट्री क्या है?'): ")
        print(f"\nआपका सवाल: {user_text}")
        
        if len(user_text.strip()) < 3:
            print("आवाज़ स्पष्ट नहीं थी, कृपया थोड़ा और विस्तार से बोलें।")
            continue
            
        answer = ask_gramin_nyaya(user_text)
        
        print("\n" + "-"*30)
        print("कानूनी परामर्श (Legal Advice):")
        print(answer)
        print("-"*30)

if __name__ == "__main__":
    start_system()