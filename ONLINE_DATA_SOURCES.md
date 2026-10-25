# Online Dataset Sources, Licenses, and Attribution

This repository downloads data at runtime. Data files are not committed to GitHub, and each source's ownership and terms remain with the dataset maintainers. Check the original source pages before commercial reuse or redistribution.

## UCI Wine Quality

- Dataset page: https://archive.ics.uci.edu/dataset/186/wine+quality
- DOI: https://doi.org/10.24432/C56S3T
- Authors cited by UCI: Paulo Cortez, A. Cerdeira, F. Almeida, T. Matos, and J. Reis
- License shown by UCI: Creative Commons Attribution 4.0 International (CC BY 4.0)
- Used by: wine-quality classifiers, regressors, PCA, GMM segmentation, and anomaly screening in the online model suite.
- Download: https://archive.ics.uci.edu/static/public/186/wine+quality.zip
- The generated report includes the source title, URL, and license metadata.

## UCI Bike Sharing

- Dataset page: https://archive.ics.uci.edu/dataset/275/bike+sharing+dataset
- DOI: https://doi.org/10.24432/C5W894
- Author cited by UCI: Hadi Fanaee-T
- License shown by UCI: Creative Commons Attribution 4.0 International (CC BY 4.0)
- Used by: Poisson count modeling, quantile-demand modeling, extreme-value tail illustration, and chronological demand forecasting.
- Download: https://archive.ics.uci.edu/static/public/275/bike+sharing+dataset.zip

## Beans leaf image dataset

- Hugging Face dataset: https://huggingface.co/datasets/AI-Lab-Makerere/beans
- Original collection repository linked by the card: https://github.com/AI-Lab-Makerere/ibean
- Dataset card metadata declares MIT. However, its licensing-information section says more information is needed about the original source. This implementation downloads from Hugging Face and does not redistribute images. Review the source repository and its terms before commercial adaptation or redistribution.
- Used by: vision_beans_cnn.py, a small convolutional network for three-way bean-leaf image classification.
- This educational model is not a validated plant-health diagnostic service.

## Free Spoken Digit Dataset (FSDD)

- Source repository: https://github.com/Jakobovski/free-spoken-digit-dataset
- Version tag fetched by code: v1.0.10
- Dataset description: 8 kHz WAV recordings of spoken English digits; the upstream repository states indices 0–4 are test and 5–49 are train.
- License stated by the repository: Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0).
- Used by: audio_fsdd_cnn.py.
- Audio files are not committed to this repository. The official split can include the same speakers in train and test, so speaker-independent performance is not claimed.

## Software dependencies

- NumPy: BSD-3-Clause — https://github.com/numpy/numpy/blob/main/LICENSE.txt
- pandas: BSD-3-Clause — https://github.com/pandas-dev/pandas/blob/main/LICENSE
- SciPy: BSD-3-Clause — https://github.com/scipy/scipy/blob/main/LICENSE.txt
- scikit-learn: BSD-3-Clause — https://github.com/scikit-learn/scikit-learn/blob/main/COPYING
- PyTorch: BSD-style — https://github.com/pytorch/pytorch/blob/main/LICENSE
- Pillow: HPND license — https://github.com/python-pillow/Pillow/blob/main/LICENSE
- Hugging Face Datasets: Apache-2.0 — https://github.com/huggingface/datasets/blob/main/LICENSE

The exact installed versions depend on the environment; see requirements-online.txt. Review all upstream notices before redistribution or commercial use. No API credentials, data archives, audio, or image files are stored in this repository.
