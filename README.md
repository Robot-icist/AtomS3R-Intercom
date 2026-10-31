# AtomS3R Intercom (base station)

ESP-NOW intercom firmware for the **M5Stack AtomS3R + Atomic Voice Base
(K147)**. Pair it with the `StickS3-Intercom` project running on a StickS3.

## Features

- Live push-to-talk audio between the two boards (16 kHz mono, IMA ADPCM).
- Clip mode: record up to 15 s, then transmit it at 1x real time.
- Automatic peer discovery and online/offline indication.
- Compact 128x128 UI with peer name, mode, state, VU meter and battery.
- Audio buffers live in PSRAM; the UI sprite uses internal RAM.

## Hardware

| Item | Detail |
| --- | --- |
| Board | M5Stack AtomS3R + Atomic Voice Base (K147) |
| MCU | ESP32-S3-PICO-1-N8R8, 8 MB flash, 8 MB PSRAM |
| Codec | ES8311 (I2C `0x18`, I2S) |
| IO expander | PI4IOE (`0x43`) |
| I2C | SDA 38, SCL 39 |
| I2S | DIN 7, WS 6, DOUT 5, BCK 8 |
| Button | GPIO 41 (front button) |

M5Unified config used by the firmware:

```cpp
cfg.internal_mic = true;
cfg.internal_spk = false;
cfg.external_speaker.atomic_echo = true;
```

The Atomic Voice Base shares one I2S port between mic and speaker, so the
firmware stops playback while capturing. Incoming audio is buffered and played
after the button is released.

## Build and flash

From this directory:

```powershell
C:\Users\Gille\.platformio\penv\Scripts\pio.exe run
C:\Users\Gille\.platformio\penv\Scripts\pio.exe run -t upload
```

Then build and flash `..\StickS3-Intercom` the same way.

## Controls

| Action | Result |
| --- | --- |
| Hold **BtnA** (Live mode) | Transmit while held; incoming audio plays on release. |
| Click **BtnA** (Clip mode) | Start recording; click again to stop and send. |
| Double-click **BtnA** | Toggle Live / Clip mode (cancels an active recording). |

## UI

- Header: device name and peer name (or `SEARCH`).
- Large state: `READY`, `RX`, `TALK`, `REC`, `SEND`, `ERROR`.
- Two VU bars: microphone and received audio.
- Footer: mode, battery, RSSI and a short hint.

## Troubleshooting

- **Peer stays `SEARCH`**: both boards must be on channel 1 and within range.
  Flash both projects; they use the same protocol version.
- **No sound on the AtomS3R**: check the Atomic Voice Base is seated and the
  ES8311 is detected at `0x18`.
- **Audio stutters**: keep the boards close; ESP-NOW throughput drops with
  distance. The jitter buffer tolerates short gaps.
- **Feedback/echo**: use Live mode as push-to-talk; do not place the two boards
  next to each other while both speakers are active.
