# Plagiarism Detection System

## Overview

This is a **Plagiarism Detection** system that leverages **Natural Language Processing (NLP)** and machine learning techniques to detect similarities between text pairs. It uses a **TF-IDF (Term Frequency-Inverse Document Frequency)** model for feature extraction and various classifiers like **SVM (Support Vector Machine)** for classification.

The project includes a **Flask API** for interaction, allowing users to check whether two given sentences are plagiarized based on a pre-trained model. The system also supports training a new model on a provided dataset.

## Key Features

- **Text Preprocessing**: Handles missing values, normalizes text (lowercasing, stripping whitespace), and tokenizes input.
- **Feature Extraction**: Uses **TF-IDF Vectorization** to convert text into numerical features suitable for machine learning models.
- **Model Training**: Supports **SVM** and **Logistic Regression** models for text classification. Additionally, **GridSearchCV** is used for hyperparameter tuning.
- **Flask API**: Provides endpoints to load data, make predictions, and check plagiarism between two given sentences.
- **Model Persistence**: Trains the model and saves it along with the TF-IDF vectorizer using **Joblib** for efficient loading in future use.

## Prerequisites

To run this project, you need the following tools installed:

- **Python 3.x**
- **pip** (Python's package installer)

Additionally, make sure to have the following Python libraries installed:

```
pip install -r requirements.txt
```

## Setup Instructions

To get started with the Plagiarism Detection project, follow the steps below:

### 1. Clone the repository

Clone the project repository to your local machine:

```bash
git clone https://github.com/yourusername/plagiarism_detector.git
cd plagiarism_detector

### 2. Install Python dependencies

Make sure you have **Python 3.x** installed. Then, install the required Python packages using **pip**:

```bash
pip install -r app/requirements.txt
```

### 3. Train the Model

```bash
python app/train.py
```

### 4. Run the Application

```bash
python app/main.py
```


