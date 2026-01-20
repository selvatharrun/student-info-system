# 🎓 Student Info System

A Streamlit app to query student data using natural language.

## Quick Start (Without Docker)

1. **Install Python 3.9+** from https://python.org
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the app:**
   ```bash
   streamlit run app.py
   ```
4. Open http://localhost:8501 in your browser

---

## Run with Docker

### Prerequisites
- Install [Docker Desktop](https://www.docker.com/products/docker-desktop/)

### Build and Run

```bash
# Build the image
docker build -t student-info-system .

# Run the container
docker run -p 8501:8501 student-info-system
```

Open http://localhost:8501 in your browser.

### Save as Portable Image

To share with another computer:

```bash
# Save the image to a file
docker save -o student-info-system.tar student-info-system

# On the other computer, load the image
docker load -i student-info-system.tar

# Then run it
docker run -p 8501:8501 student-info-system
```

---

## Configuration

- Enter your **OpenRouter API Key** in the sidebar
- Default model: `xiaomi/mimo-v2-flash:free`
- You can change the model in `config.yaml` or in the sidebar

## Example Queries

- "Show students from Chennai"
- "Count students by gender"
- "List parents names for students in Grade 10"
