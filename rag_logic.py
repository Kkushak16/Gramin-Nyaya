import ollama
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# 1. Process PDF
print("--- 1. Reading Legal PDF... ---")
loader = PyPDFLoader("./legal_docs/registrationActHindi.pdf") 
docs = loader.load()

# 2. Optimized Chunking for Search Accuracy
text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)
chunks = text_splitter.split_documents(docs)

# 3. Vector Database
print("--- 2. Connecting to Search Database... ---")
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
vector_db = Chroma.from_documents(
    documents=chunks, 
    embedding=embeddings, 
    persist_directory="./chroma_db"
)

def ask_gramin_nyaya(user_query):
    print("\n--- Searching Legal Context... ---")
    relevant_chunks = vector_db.similarity_search(user_query, k=3)
    context_text = "\n\n".join([chunk.page_content for chunk in relevant_chunks])
    
    print("--- Generating Professional Legal Response... ---")
    
    # 4. Strict Lawyer Persona
    response = ollama.chat(model='qwen2.5:1.5b', messages=[
        {
            'role': 'system', 
            'content': f'''आप 'ग्रामीण न्याय' परियोजना के एक वरिष्ठ भारतीय वकील हैं। 
            आपका काम ग्रामीणों को कानूनी जानकारी सरल और शुद्ध हिंदी में देना है।
            
            नियम:
            1. केवल नीचे दिए गए Context के आधार पर उत्तर दें।
            2. "क्षमा करतामुँ" जैसे टूटे-फूटे शब्दों का प्रयोग न करें। शुद्ध हिंदी का प्रयोग करें।
            3. यदि जानकारी उपलब्ध नहीं है, तो कहें: "क्षमा करें, मुझे इस दस्तावेज़ में इसकी जानकारी नहीं मिली।"
            
            Context:
            {context_text}'''
        },
        {'role': 'user', 'content': user_query},
    ], 
    options={
        "temperature": 0.1,    # High factual accuracy
        "repeat_penalty": 1.5, # Stops the AI from getting stuck in loops
        "top_k": 40,
        "top_p": 0.9
    })
    
    return response['message']['content']