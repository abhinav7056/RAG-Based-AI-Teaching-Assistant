import whisper
import json
import os

# Load Whisper model
model = whisper.load_model("large-v2")

# Folder containing audio files
audios = os.listdir("audios")

# 🔥 ADD THIS: Mapping of lecture number → YouTube video ID
video_links = {
      
    "Lec-1": "https://www.youtube.com/watch?v=XslI8h7cGDs&list=PLxCzCOWd7aiFM9Lj5G9G_76adtyb4ef7i",
    "Lec-2": "https://www.youtube.com/watch?v=V19S3Mqfrzo&list=PLxCzCOWd7aiFM9Lj5G9G_76adtyb4ef7i&index=2",  
    "Lec-3": "https://www.youtube.com/watch?v=aoUEXRlvmxc&list=PLxCzCOWd7aiFM9Lj5G9G_76adtyb4ef7i&index=3",
    "Lec-4": "https://www.youtube.com/watch?v=4Q2rE6R31GU&list=PLxCzCOWd7aiFM9Lj5G9G_76adtyb4ef7i&index=4",  
    "Lec-5": "https://www.youtube.com/watch?v=5Jd54dxQ1_Q&list=PLxCzCOWd7aiFM9Lj5G9G_76adtyb4ef7i&index=5",
    "Lec-6": "https://www.youtube.com/watch?v=CiXJnosT0UE&list=PLxCzCOWd7aiFM9Lj5G9G_76adtyb4ef7i&index=6",  
    "Lec-7": "https://www.youtube.com/watch?v=vsEKN2f22bE&list=PLxCzCOWd7aiFM9Lj5G9G_76adtyb4ef7i&index=7",
    "Lec-8": "https://www.youtube.com/watch?v=cEX7V3c2CWc&list=PLxCzCOWd7aiFM9Lj5G9G_76adtyb4ef7i&index=8",  
    "Lec-9": "https://www.youtube.com/watch?v=v9IwDI0GtpE&list=PLxCzCOWd7aiFM9Lj5G9G_76adtyb4ef7i&index=9",
    "Lec-10": "https://www.youtube.com/watch?v=gUeh54lmlik&list=PLxCzCOWd7aiFM9Lj5G9G_76adtyb4ef7i&index=10"
}

# Create json folder if not exists
os.makedirs("jsons", exist_ok=True)

for audio in audios:
    if "_" in audio:
        try:
            # Split file name
            number, title = audio.split("_", 1)
            title = os.path.splitext(title)[0]

            print(f"Processing: {number} - {title}")

            # 🎤 Transcribe audio
            result = model.transcribe(
                audio=f"audios/{audio}",
                language="hi",
                task="translate",
                word_timestamps=False
            )

            chunks = []

            # 🔥 CREATE CHUNKS WITH VIDEO ID
            for segment in result["segments"]:
                chunk = {
                    "number": number,
                    "title": title,
                    "video_id": video_links.get(number, ""),  # 🔥 important
                    "start": segment["start"],
                    "end": segment["end"],
                    "text": segment["text"].strip()
                }
                chunks.append(chunk)

            # Final JSON structure
            chunks_with_metadata = {
                "chunks": chunks,
                "text": result["text"]
            }

            # Save JSON file
            output_path = f"jsons/{audio}.json"
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(chunks_with_metadata, f, ensure_ascii=False, indent=4)

            print(f"Saved: {output_path}")

        except Exception as e:
            print(f"Error processing {audio}: {e}")