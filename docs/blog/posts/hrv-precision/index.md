---
date: 2026-07-16
title: "HRV Precision"
tags:
  - blog
categories:
  - Blog
draft: true
---

# HRV Precision

## Overview
I recently bought a smartwatch that provides heart rate variability (HRV) measurements, and also a chest-strap that does the same.

I was curious how each one works:

- Smartwatch: Uses photoplethysmography (PPG) to measure the pulse wave and derive HRV from it.
- Chest strap: Uses electrocardiography (ECG) to measure the electrical activity of the heart and derive HRV from it.

It is known that ECG is more accurate than PPG, but I wanted to see how much difference there is in practice, and how does the smartwatch actually manages to derive accurate HRV from measurements overnight.


## Choosing a dataset

We need a dataset that contains both PPG and ECG data, ideally recorded simultaneously.

Options:

1. [Aalborg University Wearable Sleep Study (AAUWSS)](https://zenodo.org/records/16919071) / [GitHub - sdjanian/sf_sleep](https://github.com/sdjanian/sf_sleep) - Chosen
    - publicly available dataset for sleep studies.
    - contains both PPG and ECG data.
    - during sleep, which is what we need to compare with the smartwatch.

2. [PPG-DaLiA dataset](https://archive.ics.uci.edu/dataset/495/ppg+dalia)
    - publicly available dataset for PPG-based heart rate estimation.
    - contains both PPG and ECG data.
    - download directly or using the `ucimlrepo` package ([GitHub](https://github.com/uci-ml-repo/ucimlrepo)) - which provides a convenient way to download datasets from the UCI Machine Learning Repository.
    - **cons:** The measurements are during many active states, we need during sleep to compare with the smartwatch.

## Exploring the dataset

TODO
