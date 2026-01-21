# 🎓 Student Info System

A Streamlit app to query student data using natural language.

## Creating a Portable Version (No Installation Required)

Run this **once on your own PC** to create a portable package:

```bash
python create_portable.py
```

This creates a `portable` folder (~500MB) containing:
- Embedded Python (no installation needed)
- All dependencies pre-installed
- Your app files

### Using on College PC

1. Copy the `portable` folder to a USB drive
2. On the college PC, open the folder
3. Double-click **`START_APP.bat`**
4. Browser opens automatically at http://localhost:8501

**No Python installation or admin rights required!**

---

## Development Setup (Your Own PC)

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Configuration

- Enter your **OpenRouter API Key** in the sidebar
- Default model: `xiaomi/mimo-v2-flash:free`

## Example Queries

- "Show students from Chennai"
- "Count students by gender"  
- "List parents names for students in Grade 10"

