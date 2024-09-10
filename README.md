# DocChat

Welcome to the DocChat project! This repository provides a chatbot interface for processing  documents using advanced machine learning techniques. Follow the instructions below to set up the project on your local machine.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Cloning the Project](#cloning-the-project)
3. [Setting Up the Virtual Environment](#setting-up-the-virtual-environment)
4. [Installing Dependencies](#installing-dependencies)
5. [Setting Up Environment Variables](#setting-up-environment-variables)
6. [Running the Application](#running-the-application)
7. [Database Setup (Optional)](#database-setup-optional)
8. [Testing and Validation](#testing-and-validation)
9. [Deactivating the Virtual Environment](#deactivating-the-virtual-environment)

## Prerequisites
Before setting up the project, ensure you have the following software and tools installed:

- **Python 3.8 or later**: Download Python from [python.org](https://www.python.org/).
- **Virtual Environment Tool**: Recommended tools are `venv` or `virtualenv` to manage project dependencies in an isolated environment.
- **Git**: Version control tool for cloning the repository.
- **pip**: Python package manager, typically bundled with Python.

## Cloning the Project
Start by cloning the project repository. Open a terminal window and run:

```bash
git clone https://github.com/SushainDevi/DocChat.git
```

## Setting Up the Virtual Environment
Once the project is cloned, create a virtual environment to manage dependencies:

```bash
cd DocChat
python3 -m venv .venv
```

After creating the virtual environment, activate it using the following commands:

- **On Windows**:
  ```bash
  .\.venv\Scripts\activate
  ```

- **On MacOS/Linux**:
  ```bash
  source .venv/bin/activate
  ```

## Installing Dependencies
With the virtual environment activated, install the required dependencies listed in the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

This will ensure that all necessary Python libraries, including `streamlit`, `PyPDF2`, `transformers`, and others, are installed correctly.

## Setting Up Environment Variables
The project uses environment variables for secure and flexible configurations, such as API keys and access tokens.

1. Open the `.env` file located in the project root directory.
2. Replace placeholders with the actual values (e.g., Hugging Face token, API keys). Example `.env` file format:
   ```bash
   HF_Token=<Your_Hugging_Face_Token>
   API_KEY=<Your_API_Key>
   ```
3. Save the `.env` file after updating the values.

## Running the Application
The core application is powered by Streamlit, which serves the chatbot interface. To run the chatbot, follow these steps:

1. Open the terminal.
2. Ensure the virtual environment is activated.
3. Run the Streamlit app:

```bash
streamlit run st-Qwen1.5–110B-Chat.py
```

This command will launch the Streamlit interface, accessible in your browser (typically at `http://localhost:8501/` by default).

## Database Setup (Optional)
The project uses SQLite for storing chatbot history (`chatbot_history.db`). No additional setup is required, as the database is automatically created and managed by the project scripts. However, if needed, you can inspect or modify the database using SQLite tools.

## Testing and Validation
After the setup, you can test the application by:

- Uploading documents (e.g., PDFs or DOCX files) to check the text extraction and summarization process.
- Interacting with the chatbot for document-related queries and responses.
- Requesting the generation of files (PDFs or DOCX) based on user prompts.

## Deactivating the Virtual Environment
Once you're done working on the project, you can deactivate the virtual environment by running:

```bash
deactivate
```

This ensures that your global Python environment remains unaffected by project-specific dependencies.

---

