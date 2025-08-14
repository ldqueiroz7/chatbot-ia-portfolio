# Internal Support Assistant v1.0

![Status](https://img.shields.io/badge/status-stable_version-brightgreen)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)
![Kivy](https://img.shields.io/badge/Kivy-MD-purple?logo=kivy)

This project is a comprehensive internal support chatbot developed in Python, featuring a modern graphical user interface built with the Kivy framework and the KivyMD library. Its goal is to provide fast and reliable answers to frequently asked employee questions, optimizing internal processes and communication.

This project was developed with the assistance of the Gemini Pro AI.

![Application Showcase](showcase.png)

## 🎯 The Problem

In dynamic work environments, especially with operational teams, repetitive questions about processes, systems, and HR policies are constant. This consumes valuable time from both employees, who have to wait for an answer, and supervisors or HR staff, who are frequently interrupted to address the same issues.

## 💡 The Solution

This Virtual Assistant was created to be a central point of information, available 24/7. It serves as an instant training and support tool, allowing employees to quickly and accurately resolve queries about complex procedures, such as hospital sanitization processes based on ANVISA (Brazilian Health Regulatory Agency) standards. The solution is designed to be robust, reliable, and, above all, user-friendly.

## 🚀 The Development Journey

The project evolved significantly from its inception, reflecting an agile and continuous improvement-focused development cycle:

1.  **Command-Line Interface:** Started as a simple Python script in the terminal.
2.  **Knowledge Base:** Evolved to a keyword-matching logic within a dictionary.
3.  **Enhanced Intelligence:** Implemented a scoring system to find the "best match" instead of the first one, and added typo tolerance using `difflib`.
4.  **Contextual Logic:** The bot gained a "memory" to ask clarifying questions and understand subsequent answers.
5.  **Graphical User Interface (GUI):** Transitioned to a desktop application using the Kivy framework.
6.  **Modern Design:** The UI was refined with the KivyMD library, adhering to Material Design guidelines for a professional and user-friendly experience.

## ✨ Key Features

-   **Intuitive Graphical Interface:** A modern and responsive chat UI built with KivyMD.
-   **Robust Conversational Logic:**
    -   **Best-Match Search:** Utilizes a scoring system to analyze the user's entire sentence and determine the most relevant intent.
    -   **Typo Tolerance:** Uses `difflib` to correct common spelling mistakes in user queries.
    -   **Contextual Memory:** Manages multi-step conversations, asking clarifying questions when necessary.
-   **Centralized Knowledge Base:** All questions and answers are stored in a Python dictionary, making maintenance and the addition of new knowledge extremely simple.
-   **History Logging:** All conversations are saved to a `historico_conversas.txt` file with timestamps for analysis and auditing purposes.

## 🏗️ Architecture

The project is structured with a clear separation of concerns, a fundamental software engineering best practice:

-   **The "Brain" (`cerebro_chatbot.py`):** A pure Python module containing all the language processing logic, the knowledge base, and the decision-making rules. It is completely independent of the interface.
-   **The "Face" (`app_gui.py` & `chatbot.kv`):** The KivyMD application responsible for all visual aspects and user interaction. It acts as a client for the "brain," sending queries and displaying the results.

## 🚀 How to Run the Project

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/ldqueiroz7/chatbot-ia-portfolio.git](https://github.com/ldqueiroz7/chatbot-ia-portfolio.git)
    cd chatbot-ia-portfolio
    ```

2.  **Create and Activate the Virtual Environment:**
    ```bash
    # Create the environment (only once)
    py -m venv venv
    
    # Activate the environment (every time you work on the project)
    .\venv\Scripts\activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Application:**
    ```bash
    py app_gui.py
    ```

## 🔮 Future Roadmap & Vision

This project serves as a solid foundation for future enhancements, such as:

-   [ ] **Packaging for Android:** Using Buildozer to turn the application into an installable `.apk` file.
-   [ ] **Voice Recognition:** Implementing a Speech-to-Text library to enable voice-based interaction, increasing accessibility.
-   [ ] **Admin Mode:** Creating a secure interface for authorized users to update the knowledge base without editing the code.