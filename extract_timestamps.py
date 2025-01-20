import os
import pandas as pd
from pyannote.audio import Pipeline
import torch
from datetime import timedelta

# Enable TensorFloat-32 for performance
torch.backends.cuda.matmul.allow_tf32 = True
torch.backends.cudnn.allow_tf32 = True

# Check if GPU is available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# Hugging Face token
HUGGING_FACE_TOKEN = os.getenv("HUGGING_FACE_TOKEN")
if not HUGGING_FACE_TOKEN:
    raise ValueError("Hugging Face token not found. Please set the 'HUGGING_FACE_TOKEN' environment variable.")

INPUT_DIR = "./Converted_WAV"
OUTPUT_DIR = "./Timestamps"

def format_time(seconds):
    """Convert seconds to HH:MM:SS format."""
    return str(timedelta(seconds=round(seconds)))

def initialize_diarization_pipeline(hugging_face_token, device):
    """Initialize the PyAnnote pipeline for speaker diarization."""
    if not hugging_face_token:
        raise ValueError("Hugging Face token is not set. Please set it directly in the code.")
    try:
        pipeline = Pipeline.from_pretrained(
            "pyannote/speaker-diarization@2.1",
            use_auth_token=hugging_face_token
        )
        pipeline.to(device)
        print("Pipeline initialized successfully.")
        return pipeline
    except Exception as e:
        raise ValueError(
            f"Error initializing the pipeline: {e}. Ensure your token is valid and you have accepted the model's terms at "
            f"https://hf.co/pyannote/speaker-diarization"
        )

def diarize_audio_to_excel(pipeline, audio_file, output_file):
    """Apply the diarization pipeline to an audio file and save results to an Excel file."""
    try:
        print(f"Processing file: {os.path.basename(audio_file)}")
        diarization = pipeline(audio_file)

        # Extract segments and create a DataFrame
        results = []
        for segment, track, speaker in diarization.itertracks(yield_label=True):
            results.append({
                "speaker_ID": speaker,
                "start_time": format_time(segment.start),
                "stop_time": format_time(segment.end)
            })

        # Save to Excel
        df = pd.DataFrame(results)
        df.to_excel(output_file, index=False)
        print(f"Saved results to: {output_file}")
    except Exception as e:
        print(f"Error processing {audio_file}: {e}")

def process_audio_files(input_dir, output_dir, pipeline):
    """Process all audio files in the input directory and save results to the output directory."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    audio_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.wav')]
    if not audio_files:
        print(f"No audio files found in: {input_dir}")
        return

    print(f"Found {len(audio_files)} audio file(s) in: {input_dir}")
    for audio_file in audio_files:
        input_path = os.path.join(input_dir, audio_file)
        output_path = os.path.join(output_dir, f"{os.path.splitext(audio_file)[0]}.xlsx")
        diarize_audio_to_excel(pipeline, input_path, output_path)

if __name__ == "__main__":
    try:
        # Initialize the diarization pipeline
        pipeline = initialize_diarization_pipeline(HUGGING_FACE_TOKEN, device)

        # Process all audio files
        print("Starting audio diarization...")
        process_audio_files(INPUT_DIR, OUTPUT_DIR, pipeline)

        print("Audio diarization completed successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
