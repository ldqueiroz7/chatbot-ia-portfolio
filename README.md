# Clinical Research Assistant v1.0

![Status](https://img.shields.io/badge/status-stable_version-brightgreen)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)
![Kivy](https://img.shields.io/badge/Kivy-MD-purple?logo=kivy)
![Cohere](https://img.shields.io/badge/AI-Cohere-red?logo=cohere)

A sophisticated desktop chatbot designed to act as a research assistant for medical students and healthcare professionals. This application leverages a powerful Generative AI (Cohere) combined with a local, curated knowledge base to provide reliable, context-aware, and cited answers to complex clinical questions.

This project was developed with the assistance of the Gemini Pro AI.

## 🎯 The Problem

Medical students and professionals need quick access to vast amounts of reliable information from trusted sources (textbooks, articles). Standard search engines can provide links, but not synthesized, direct answers. Generative AIs can "hallucinate" or provide information without citing sources, making them unreliable for clinical study.

## 💡 The Solution: Cloud-Processed RAG Architecture

This project implements a **Retrieval-Augmented Generation (RAG)** architecture to solve the problem. It combines the reasoning and language capabilities of a Large Language Model (LLM) with the factual accuracy of a specific knowledge base, built from large documents like medical textbooks.

To handle the immense computational task of processing and vectorizing entire books, this project uses a hybrid cloud/local workflow.

## 🏗️ Architecture & Workflow

The project is structured with a clear separation of concerns, reflecting a modern data science and software engineering pipeline.

### Part 1: Knowledge Base Creation (in Google Colab)

The heavy lifting of processing large source documents (PDFs, etc.) is offloaded to a **Google Colab notebook**, which provides free access to powerful GPUs.

1.  **Data Ingestion:** Large documents (e.g., medical textbooks in PDF format) are uploaded.
2.  **Text Extraction & Chunking:** The `PyMuPDF` library extracts text, which is then segmented into meaningful paragraphs (chunks).
3.  **Vectorization (Embedding):** Each chunk is converted into a numerical vector using a state-of-the-art multilingual model from the `sentence-transformers` library.
4.  **Vector Database Creation:** The vectors and their corresponding text are stored in a local, persistent **ChromaDB** vector database.
5.  **Export:** The resulting database is compressed and downloaded.

### Part 2: The Local Application

The final user-facing application runs locally and is lightweight.

-   **The "Brain" (`cerebro_chatbot.py`):** A pure Python module containing the logic to:
    -   Connect to the local ChromaDB vector database.
    -   Query the database to retrieve the most relevant context for a user's question.
    -   Communicate with the **Cohere API** to generate a final answer based on the retrieved context (RAG).
-   **The "Face" (`app_gui.py` & `chatbot.kv`):** The KivyMD application responsible for all visual aspects and user interaction.

## ✨ Key Features

-   **Modern GUI:** A user-friendly and responsive chat interface built with KivyMD.
-   **Generative AI Core:** Powered by the **Cohere API** for state-of-the-art language understanding and generation in a RAG context.
-   **Scalable Knowledge Base:** Can ingest and process entire books and articles using a cloud-based GPU workflow, creating a rich and reliable vector database.
-   **High-Fidelity Retrieval:** Uses a multilingual sentence-transformer model for accurate, semantic searching across documents in different languages.
-   **Secure API Key Management:** Uses a `.env` file and `.gitignore` to keep credentials safe.
-   **Asynchronous Processing:** Long-running tasks (API calls) are handled in separate threads to keep the UI from freezing.
-   **History Logging:** All conversations are logged for auditing and analysis.

## 🚀 How to Run the Project

This project has a two-stage setup: first building the knowledge base in the cloud, then running the application locally.

### Stage 1: Build the Knowledge Base (Google Colab)

1.  Follow the instructions in the `processador_de_dados.py` file, which has been adapted to run as a Google Colab notebook.
2.  Upload your source documents (PDFs, TXTs) to your Google Drive.
3.  Run the notebook in a **GPU-enabled Colab environment**.
4.  At the end of the process, download the generated `biblioteca_clinica_db.zip` file.
5.  Unzip it and place the `biblioteca_clinica_db` folder in the root of this project directory.

### Stage 2: Run the Local Application

1.  **Clone the Repository:**
    ```bash
    git clone [YOUR_GITHUB_REPOSITORY_URL]
    cd [YOUR_PROJECT_FOLDER]
    ```

2.  **Create and Activate the Virtual Environment:**
    ```bash
    py -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set Up API Key:**
    -   Create a file named `.env` in the root directory.
    -   Add your Cohere API Key: `COHERE_API_KEY='YourApiKeyHere'`

5.  **Run the Application:**
    ```bash
    py app_gui.py
    ```