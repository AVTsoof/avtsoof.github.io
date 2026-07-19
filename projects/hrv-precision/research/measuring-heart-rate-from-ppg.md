# Measuring Heart Rate (Frequency) from a PPG Sensor

> Author: AI Generated

Research notes for the HRV-Precision project. Focus: how to turn a raw
photoplethysmography (PPG) waveform into a heart-rate estimate, and the
trade-offs between the main approaches.

## 1. What the PPG signal actually is

A PPG sensor shines an LED into the skin and measures light reflected back to a
photodiode. Blood volume in the microvascular bed rises and falls with each
cardiac cycle, modulating the absorbed light. The recorded signal has two parts:

- **DC component** — slowly varying baseline from bulk tissue absorption,
  venous blood, respiration, and motion.
- **AC component** — the pulsatile part synchronized to the heartbeat. This is
  what carries heart-rate information.

Each cardiac cycle appears as one PPG pulse (a systolic upstroke, often with a
secondary dicrotic notch). **Heart rate = the fundamental frequency of the AC
pulse train.**

Typical physiological range:

- Resting / sleep: ~40–100 bpm → $0.67$–$1.67\ \text{Hz}$
- Exercise: up to ~200 bpm → $\approx 3.3\ \text{Hz}$

So valid heart-rate frequencies live roughly in the **0.5–4 Hz** band. This band
is the anchor for almost every method below.

## 2. Preprocessing (shared by all methods)

Raw PPG is noisy; every heart-rate method benefits from cleanup first.

1. **Detrend / remove DC** — subtract a moving average or high-pass filter to
   kill the baseline wander (respiration ≈ 0.15–0.4 Hz, slow drift below that).
2. **Band-pass filter** — keep only the plausible HR band. A common choice is a
   Butterworth band-pass of **0.5–4 Hz** (or 0.5–8 Hz if you want harmonics for
   waveform analysis).
3. **Normalize** — min-max or z-score per window so amplitude drift does not bias
   peak detection.
4. **(Optional) motion-artifact reduction** — if an accelerometer is available,
   adaptive filtering (e.g. LMS/RLS) can subtract motion components. This is the
   single biggest source of PPG error during activity; less critical during
   sleep.

> Sampling-rate note: HR estimation needs surprisingly little bandwidth. Even
> 25–64 Hz PPG resolves the pulse train well. Higher rates matter more for
> **beat-to-beat timing (HRV)** than for average HR.

## 3. Approach A — Time-domain peak detection

Find each systolic peak, then derive rate from the spacing between beats.

**Steps**

1. Band-pass filter the signal.
2. Detect systolic peaks (e.g. `scipy.signal.find_peaks` with a minimum
   `distance` set from the max plausible HR, plus a `prominence`/height threshold).
3. Compute peak-to-peak intervals — the **inter-beat intervals (IBI)**, analogous
   to ECG RR intervals:

$$
\text{IBI}_i = t_{\text{peak},\,i+1} - t_{\text{peak},\,i}
$$

4. Convert to instantaneous heart rate:

$$
\text{HR}_i = \frac{60}{\text{IBI}_i} \quad [\text{bpm}], \quad \text{IBI in seconds}
$$

5. Average (mean/median) over the window for a stable HR, or keep the IBI series
   for HRV.

**Pros**

- Gives beat-to-beat timing → required for **HRV** (RMSSD, SDNN, etc.).
- Intuitive and interpretable.

**Cons**

- Very sensitive to motion artifacts and misshapen pulses (missed or extra peaks
  wreck the IBI series).
- Needs careful threshold tuning; robustness depends on peak-detector quality.

## 4. Approach B — Frequency-domain (spectral) estimation

Instead of individual beats, find the dominant frequency of the whole window.

**Steps**

1. Band-pass filter and window the signal (e.g. 8–30 s window; a Hann window
   reduces spectral leakage).
2. Compute the power spectral density:
   - **FFT** magnitude spectrum, or
   - **Welch's method** (averaged periodograms) for a smoother, lower-variance
     PSD.
3. Restrict the search to the HR band (0.5–4 Hz).
4. The **peak frequency** $f_{\text{peak}}$ in that band is the fundamental:

$$
\text{HR} = 60 \cdot f_{\text{peak}} \quad [\text{bpm}]
$$

**Frequency resolution** is set by window length $T$:

$$
\Delta f = \frac{1}{T} \;\Rightarrow\; \Delta \text{HR} = \frac{60}{T}\ \text{bpm}
$$

So a 10 s window resolves ~6 bpm; a 30 s window ~2 bpm. Longer windows = finer
resolution but worse time localization (and they blur real HR changes).
**Zero-padding** the FFT interpolates the spectrum for a finer peak read, but does
not add true resolution.

**Pros**

- Robust to individual malformed beats — averages over many cycles.
- Handles noisy/low-amplitude signals better than peak detection.
- Naturally suited to a smartwatch's periodic HR updates.

**Cons**

- Gives an **average** HR over the window, not beat-to-beat timing → not enough
  on its own for HRV.
- Motion can create spurious spectral peaks (aliased into the HR band); harmonics
  can be mistaken for the fundamental.

## 5. Approach C — Autocorrelation

The PPG pulse train is quasi-periodic, so its autocorrelation function peaks at
the beat period.

**Steps**

1. Band-pass filter.
2. Compute the autocorrelation of the windowed signal.
3. Find the first dominant lag $\tau$ (within the HR band) after the zero lag.
4. Convert:

$$
\text{HR} = \frac{60}{\tau} \quad [\text{bpm}], \quad \tau \text{ in seconds}
$$

**Pros**: robust to noise, no explicit peak thresholds.
**Cons**: still a windowed average; can lock onto a harmonic/subharmonic.

## 6. Practical: how smartwatches actually do it

Production wearables rarely rely on a single method. A typical pipeline:

- Continuous band-pass + **adaptive motion cancellation** using the
  accelerometer.
- **Spectral tracking** (FFT/Welch) for the robust average HR, often with a
  Kalman filter or frequency tracker to smooth updates and reject jumps.
- **Peak detection** on clean segments (especially at rest / sleep) to recover
  beat-to-beat IBIs for HRV.
- Confidence gating: discard windows where motion or low perfusion make the
  estimate unreliable.

At night (low motion, good perfusion) PPG is at its best, which is why overnight
HRV from a watch can approach ECG quality — the hard artifacts are mostly absent.

## 7. Recommendation for this project

Because the goal is **comparing PPG-derived HRV against ECG**, not just average
HR:

1. Use **time-domain peak detection** to get PPG IBIs (needed for HRV metrics),
   with a robust detector (`neurokit2`'s PPG pipeline, or `scipy.find_peaks` with
   tuned prominence/distance).
2. Use **spectral estimation** as a cross-check / sanity bound on average HR per
   window, and to visualize where PPG's dominant frequency drifts from ECG.
3. Align both to real time (seconds) before comparing, since ECG (200 Hz) and PPG
   (64 Hz) are sampled differently.

## 8. Key libraries

- **`scipy.signal`** — `butter`/`filtfilt` (filtering), `find_peaks` (peaks),
  `welch`/`periodogram` (PSD), `correlate` (autocorrelation).
- **`neurokit2`** — `ppg_process`, `ppg_findpeaks`, and HRV metrics out of the
  box; good default for ECG + PPG comparison.
- **`numpy.fft`** — direct FFT if you want full control of the spectral method.

## References

- Allen J. (2007). *Photoplethysmography and its application in clinical
  physiological measurement.* Physiological Measurement, 28(3), R1–39.
- Charlton P.H. et al. (2022). *Wearable Photoplethysmography for Cardiovascular
  Monitoring.* Proceedings of the IEEE, 110(3), 355–381.
- Charlton P.H. et al. (2023). *The 2023 wearable photoplethysmography roadmap.*
  Physiological Measurement, 44(11), 111001.
- Wikipedia: [Photoplethysmogram](https://en.wikipedia.org/wiki/Photoplethysmogram).
