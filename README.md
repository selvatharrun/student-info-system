# Student Info System

A Streamlit app to query student data using natural language powered by AI.


![ezgif-63415258511be5b6](https://github.com/user-attachments/assets/928e49d5-fda5-491a-b840-6c108995ca73)


## Portable Version (No Installation Required)

### Step 1: Create the Portable Package (One-Time Setup)

On your own PC with Python installed, run:

```bash
python create_portable.py
```

This creates a `portable` folder (~600MB) containing:
- Embedded Python
- All dependencies pre-installed  
- Your app files
- `START_APP.bat` launcher

### Step 2: Use on Any PC

1. Copy the `portable` folder to a **USB drive**
2. On the target PC, open the `portable` folder
3. Double-click **`START_APP.bat`**
4. Browser opens automatically at **http://localhost:8501**

 **No Python installation or admin rights required!**


## Development Setup (Your Own PC)

If you want to run directly without the portable package:

```bash
# Create virtual environment (optional)
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

## Configuration

1. Get an API key from [OpenRouter](https://openrouter.ai/)
2. Enter your **OpenRouter API Key** in the sidebar
3. Default model: `xiaomi/mimo-v2-flash:free` (free tier)

---

## Example Queries

- "Show students from Chennai"
- "Count students by gender"
- "List parents names for students in Grade 10"
- "What is the average age of students?"
- "Show me students whose father's name starts with R"

---

## Project Structure

```
student-info-system/
├── app.py                 # Main Streamlit app
├── config.yaml            # Default configuration
├── requirements.txt       # Python dependencies
├── create_portable.py     # Script to build portable version
├── portable/              # Generated portable package (copy this!)
│   ├── python/            # Embedded Python
│   ├── app.py
│   ├── config.yaml
│   └── START_APP.bat      # Double-click to run
└── README.md
```


