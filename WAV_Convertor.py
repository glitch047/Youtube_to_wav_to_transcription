import os
import subprocess

def validate_and_convert_audio(input_path, output_path):
    """Validate and convert audio to WAV (16kHz, mono) and save to output path."""
    try:
        print(f"Now converting: {os.path.basename(input_path)}")
        subprocess.run(
            ["ffmpeg", "-y", "-i", input_path, "-ar", "16000", "-ac", "1", output_path],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        print(f"Completed: {os.path.basename(input_path)} -> {os.path.basename(output_path)}")
    except subprocess.CalledProcessError as e:
        print(f"Error converting {os.path.basename(input_path)}: {e.stderr.decode('utf-8')}")
    except Exception as ex:
        print(f"Unexpected error with {os.path.basename(input_path)}: {str(ex)}")

def process_all_audio_files(input_directory, output_directory):
    """Process all files in the input directory and save converted files to the output directory."""
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # List all files in the input directory
    audio_files = [f for f in os.listdir(input_directory) if f.lower().endswith('.wav')]

    if not audio_files:
        print("No WAV files found in the input directory.")
        return

    print(f"Found {len(audio_files)} files in '{input_directory}'. Starting conversion...")

    for audio_file in audio_files:
        input_path = os.path.join(input_directory, audio_file)
        output_path = os.path.join(output_directory, audio_file)
        validate_and_convert_audio(input_path, output_path)

    print(f"All files processed. Converted files saved in '{output_directory}'.")

if __name__ == "__main__":
    downloaded_dir = "./Downloaded_WAV"
    converted_dir = "./Converted_WAV"

    print("Starting the audio conversion process...")

    if not os.path.exists(downloaded_dir):
        print(f"Input directory not found: {downloaded_dir}")
    else:
        process_all_audio_files(downloaded_dir, converted_dir)

    print("Audio conversion process completed.")
