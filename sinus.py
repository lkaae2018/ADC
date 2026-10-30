"""Afspil en sinustone på computerens standardhøjttaler (Windows)."""

import argparse
import math
import tempfile
import wave
from pathlib import Path

import winsound


def make_tone(path: Path, frequency: float, seconds: float, volume: float) -> None:
    sample_rate = 44100
    sample_count = int(sample_rate * seconds)
    amplitude = int(32767 * volume)

    with wave.open(str(path), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)  # 16-bit lyd
        wav.setframerate(sample_rate)
        samples = bytearray()
        for i in range(sample_count):
            value = int(amplitude * math.sin(2 * math.pi * frequency * i / sample_rate))
            samples.extend(value.to_bytes(2, byteorder="little", signed=True))
        wav.writeframes(samples)


def main() -> None:
    parser = argparse.ArgumentParser(description="Afspil en sinustone via standardhøjttaleren.")
    parser.add_argument("--frequency", "-f", type=float, default=440, help="Frekvens i Hz (standard: 440)")
    parser.add_argument("--duration", "-d", type=float, default=2, help="Varighed i sekunder (standard: 2)")
    parser.add_argument("--volume", "-v", type=float, default=0.25, help="Lydstyrke fra 0 til 1 (standard: 0.25)")
    args = parser.parse_args()

    if not 20 <= args.frequency <= 20000:
        parser.error("frekvensen skal være mellem 20 og 20000 Hz")
    if not 0 < args.duration <= 60:
        parser.error("varigheden skal være større end 0 og højst 60 sekunder")
    if not 0 < args.volume <= 1:
        parser.error("lydstyrken skal være større end 0 og højst 1")

    with tempfile.TemporaryDirectory() as temp_dir:
        wav_path = Path(temp_dir) / "sinustone.wav"
        make_tone(wav_path, args.frequency, args.duration, args.volume)
        print(f"Afspiller {args.frequency:g} Hz i {args.duration:g} sekunder …")
        winsound.PlaySound(str(wav_path), winsound.SND_FILENAME)


if __name__ == "__main__":
    main()
