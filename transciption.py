import os
from datetime import timedelta
import pandas as pd
import whisper

INPUT_DIR = "./Converted_WAV"
OUTPUT_DIR = "./Transcriptions"


def format_time(seconds: float) -> str:
    """Convert seconds to hh:mm:ss format."""
    return str(timedelta(seconds=int(seconds))).zfill(8)


def assign_speaker_ids(segments: list, gap_threshold: int = 2) -> list:
    """Assign dynamic speaker IDs based on gaps between segments."""
    speaker_counter = 0
    last_end_time = 0
    speaker_mapping = []

    for segment in segments:
        if segment["start"] >= last_end_time + gap_threshold:
            speaker_counter += 1
        last_end_time = segment["end"]
        speaker_mapping.append(f"speaker-{speaker_counter:02d}")

    return speaker_mapping


def transcribe_audio_file(audio_file: str, model, output_dir: str) -> None:
    """Transcribe a single audio file and save the results as an Excel file."""
    try:
        print(f"Transcribing: {os.path.basename(audio_file)}")
        result = model.transcribe(audio_file, verbose=False)
        segments = result.get("segments", [])

        if not segments:
            print(f"No transcription segments found for: {audio_file}")
            return

        # Assign speaker IDs and prepare transcription data
        speaker_ids = assign_speaker_ids(segments)
        transcription_data = [
            {
                "speaker_ID": speaker_ids[idx],
                "start_time": format_time(segment["start"]),
                "stop_time": format_time(segment["end"]),
                "transcription": segment["text"].strip(),
            }
            for idx, segment in enumerate(segments)
        ]

        # Save to Excel
        output_file = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(audio_file))[0]}-transcription.xlsx")
        pd.DataFrame(transcription_data).to_excel(output_file, index=False)
        print(f"Saved transcription to: {output_file}")
    except Exception as e:
        print(f"Error transcribing {audio_file}: {e}")


def process_audio_files(input_dir: str, output_dir: str, model_name: str = "large") -> None:
    """Process all audio files in the input directory and save results to the output directory."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    audio_files = [f for f in os.listdir(input_dir) if f.lower().endswith(".wav")]
    if not audio_files:
        print(f"No audio files found in {input_dir}.")
        return

    print(f"Found {len(audio_files)} audio file(s) in {input_dir}.")
    print(f"Loading Whisper model: {model_name}")
    model = whisper.load_model(model_name)

    for audio_file in audio_files:
        full_path = os.path.join(input_dir, audio_file)
        transcribe_audio_file(full_path, model, output_dir)

    print(f"All files processed. Transcriptions saved in {output_dir}.")


if __name__ == "__main__":
    print("Starting transcription process...")
    process_audio_files(INPUT_DIR, OUTPUT_DIR)
    print("Transcription process completed.")
