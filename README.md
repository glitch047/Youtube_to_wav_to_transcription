## This tool-suit consis of multi-process transcription extraction

### youtube_to_WAV.py
- This uses yt_dlp and ffmpeg to download the audio from the youtube video and save it as a WAV file

### WAV_Convertor.py
- This Validate and convert audio to WAV (16kHz, mono) and save to output path

### extract_timestamps.py
- This uses pyannote.audio to extract the timestamps and distuinguish between the people speaking

### transciption.py
- This uses whisper model to extract the transctiption 


(hugging face is used for the models)


## Further Iterations
- Need to figureout how to match the transcription with timestamps(HF has a token limit :) )
