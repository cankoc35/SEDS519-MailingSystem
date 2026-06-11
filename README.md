# Interactive Mailing System

SEDS519 HW2 project for an interactive mailing system. The application will let users view mails, inspect attachments, update attachment data, and convert supported file attachments into an editable HTML table representation.

## Stack

- Python + FastAPI for the application logic and API
- React + TypeScript + Vite for the user interface
- PlantUML files for UML diagrams

## Design Patterns

- MVC: Python models and controllers with React views
- Adapter: CSV, Excel, and PDF adapters convert files into a common table format
- Composite: mails, text parts, and attachments are represented through a shared mail component structure

## Project Structure

```text
app/          Python application, models, controllers, adapters, composite code
ui/           React user interface
docs/         Homework PDF and UML diagrams
samples/      Sample attachment files
tests/        Project tests
```

## Development

Install Python dependencies:

```bash
pip install -r requirements.txt
```

Run the API:

```bash
uvicorn app.main:app --reload
```

Run the UI:

```bash
cd ui
npm install
npm run dev
```
