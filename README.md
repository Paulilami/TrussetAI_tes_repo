
# **AI Protocol Interface - Testing Guide**

Welcome to the AI Protocol Interface testing guide. This document will walk you through setting up and testing the protocol quickly and efficiently.

## **Prerequisites**

Before you start, ensure you have the following:

- **Python 3.8+** installed on your machine.
- **Pip3** for managing Python packages.
- **OpenAI API Key**. Ensure you have it ready.

## **Setup Instructions**

### 1. **Clone the Repository**

If you have the project in a repository, clone it to your local machine:

```bash
git clone https://github.com/paulilami/trussetai_test_repo.git
cd trussetai_test_repo
```

### 2. **Install Dependencies**

Install the required Python packages using `pip3`:

```bash
pip3 install flask openai
```

### 3. **Set Up Environment Variables**

Set your OpenAI API key in your environment. Replace `your-openai-api-key` with your actual key.

- **Linux/macOS:**

  ```bash
  export OPENAI_API_KEY='your-openai-api-key'
  ```

- **Windows:**

  ```cmd
  set OPENAI_API_KEY=your-openai-api-key
  ```

### 4. **Run the Flask Application**

Start the Flask server by running:

```bash
python app.py
```

The server will start at `http://127.0.0.1:5001/`.

## **Testing the Protocol**

### 1. **Access the Interface**

Open your web browser and navigate to:

```
http://127.0.0.1:5001/
```

### 2. **Interact with the Interface**

- **Sending Inputs:**
  - Type your input in the provided text field and click "Send."
  - The input will appear in the left panel under "User Inputs."
  - The AI's response will be displayed in the right panel under "AI Output."

- **End Session:**
  - Click "End Session" to terminate the current session.
  - The session data will be displayed in the right panel.

### 3. **Observe the Output**

- **Loading Bar:** A loading bar will appear when processing your input.
- **Structured Output:** The AI's JSON output will be neatly structured and displayed.

## **Troubleshooting**

- **Can't See CSS Styles?** Ensure the CSS is embedded in the HTML or served correctly from the `/static` directory.
- **API Key Issues?** Double-check that your OpenAI API key is set correctly in the environment variables.

## **Conclusion**

This setup allows you to test the AI protocol interface easily. For further customization or troubleshooting, refer to the documentation or contact the project maintainer.

Enjoy testing! 🎉
