from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai
import os # <--- TAMBAHKAN INI

app = Flask(__name__)
CORS(app) 

# Kunci diambil dari brankas, bukan diketik langsung
api_key_rahasia = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key_rahasia)

# Konteks AI (Pindahkan dari JavaScript ke sini)
SYSTEM_CONTEXT = """
Kamu adalah asisten AI virtual yang ramah di website portofolio Kemal Almahdika. 
Keahlian Kemal: PHP, MySQL, Flutter, Tailwind, Video Editing (CapCut).
Proyek: Website Angel Brownies, Absensi PRO, Web Supplychain.
Jawab dengan singkat, ramah, dan gunakan bahasa Indonesia.
"""

@app.route('/chat', methods=['POST'])
def chat_with_gemini():
    data = request.json
    user_message = data.get("message", "")
    
    if not user_message:
        return jsonify({"error": "Pesan kosong"}), 400

    try:
        # Menggabungkan konteks sistem dengan pertanyaan user
        full_prompt = f"{SYSTEM_CONTEXT}\n\nPertanyaan pengunjung: {user_message}"
        
        # Logika dari kode Python Anda (disesuaikan dengan metode generate_content)
        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=full_prompt
        )
        
        return jsonify({"reply": response.text})
        
    except Exception as e:
        error_msg = str(e)
        print("Error System:", error_msg) # Tetap di-print agar tercatat di log Vercel
        
        # Mengubah pesan error 503 menjadi balasan chat yang ramah
        if "503" in error_msg or "UNAVAILABLE" in error_msg:
            return jsonify({"reply": "Waduh, server AI Google sedang kelebihan beban saat ini. Mohon tunggu beberapa detik dan coba kirim lagi, ya!"})
        else:
            return jsonify({"reply": "Maaf, sedang ada gangguan teknis pada sistem AI. Silakan coba lagi nanti."})

if __name__ == '__main__':
    # Server Python akan berjalan di port 5000
    app.run(debug=True, port=5000)
