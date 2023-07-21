import pyaudio
import wave
import time
import os, stat

form_1 = pyaudio.paInt16  # 16-bit resolution
chans = 1  # 1 channel
samp_rate = 44100  # 44.1kHz sampling rate
chunk = 4096  # 2^12 samples for buffer
record_secs = 60  # seconds to record
dev_index = 10  # device index found by p.get_device_info_by_index(ii)

output_dir = "/home/gtunano3/Desktop/beekeeping/recordings"  # directory to save audio files
hivename = "hive1"

# Creating the directory
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    os.chmod(output_dir, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)

audio = pyaudio.PyAudio()  # create pyaudio instantiation

while True:
    # name of the saved audio file (hivenumber-timestamp)
    wav_output_filename = hivename + "-" + str(time.time())

    # create pyaudio stream
    stream = audio.open(format=form_1, rate=samp_rate, channels=chans,
                        input_device_index=dev_index, input=True,
                        frames_per_buffer=chunk)
    print("Recording")
    frames = []

    # loop through stream and append audio chunks to frame array
    for _ in range(0, int((samp_rate / chunk) * record_secs)):
        data = stream.read(chunk, exception_on_overflow=False)
        frames.append(data)

    print("Finished recording")

    # stop the stream and close it
    stream.stop_stream()
    stream.close()

    # save the audio frames as .wav file
    wav_output_filepath = os.path.join(output_dir, f"{wav_output_filename}.wav")
    wavefile = wave.open(wav_output_filepath, 'wb')
    wavefile.setnchannels(chans)
    wavefile.setsampwidth(audio.get_sample_size(form_1))
    wavefile.setframerate(samp_rate)
    wavefile.writeframes(b''.join(frames))
    wavefile.close()

audio.terminate()
