# **Stinky Slim**

> This write-up documents a deliberately vulnerable lab / CTF-style service.  
> All techniques are presented for educational purposes only.

------

## Overview

- **Category**: Steganography (Audio)
- **Difficulty**: Easy
- **Key Concept**: Audio Spectrogram Analysis
- **Goal**: Extract hidden flag from audio file visualization

------

## Challenge Description

​	I don't trust Patapim; I think he is hiding something from me.

## 1. Solution

**Tool Used:**

- Audacity

**Steps:**

1. Open the provided audio file:
   
   - Load `pieno-di-slim.wav` into Audacity.
2. Convert waveform view into spectrogram view:
   - Click the track dropdown menu.
   
   - Select **Spectrogram**.
   
     ![](image/image1.png)
3. Adjust spectrogram settings (if needed):
   
   - Increase frequency range or resolution for clearer visualization.
4. Inspect the spectrogram:
   - The hidden text appears visually in the frequency display.
   - The visible text reveals the flag.

## Key Takeaways

- Audio files can hide information using frequency visualization techniques.
- Spectrogram analysis is a common steganography method in CTF challenges.
- Tools like Audacity allow visual inspection of audio signals beyond playback.



#### References

- Audacity Documentation
- Audio Steganography Techniques