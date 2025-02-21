# InfoSphere

InfoSphere ist eine moderne Desktop-Anwendung, die eine Electron-basierte Frontend-Anwendung mit einem Django-Backend kombiniert. Die Anwendung bietet eine nahtlose Integration zwischen einer benutzerfreundlichen Desktop-Oberfläche und einem leistungsstarken Python-Backend.

## Projektstruktur

Das Projekt besteht aus zwei Hauptkomponenten:

### Electron Frontend (`electron-app/`)
- Moderne Desktop-Anwendung mit React
- Webpack für Bundling
- Babel für moderne JavaScript-Features

### Django Backend (`django-app/`)
- RESTful API mit Django
- Nachrichtenverwaltung über `messages_api`
- Service-Layer für Geschäftslogik

## Technologie-Stack

- **Frontend:**
  - Electron
  - React
  - Webpack
  - Babel

- **Backend:**
  - Django
  - Django REST Framework
  - Python

## Installation und Setup

### Frontend Setup (Electron)

1. Navigiere in das electron-app Verzeichnis:
```bash
cd electron-app
```

2. Installiere die Abhängigkeiten:
```bash
npm install
```

3. Starte die Entwicklungsumgebung:
```bash
npm start
```

### Backend Setup (Django)

1. Navigiere in das django-app Verzeichnis:
```bash
cd django-app
```

2. Erstelle eine virtuelle Umgebung (empfohlen):
```bash
python -m venv venv
source venv/bin/activate  # Unter Windows: venv\Scripts\activate
```

3. Installiere die Python-Abhängigkeiten:
```bash
pip install -r requirements.txt
```

4. Führe die Datenbank-Migrationen aus:
```bash
python manage.py migrate
```

5. Starte den Django-Server:
```bash
python manage.py runserver
```

## Entwicklung

- Der Electron-Frontend-Code befindet sich in `electron-app/src/`
- Der Django-Backend-Code ist in `django-app/` organisiert
- API-Endpunkte sind über die Messages-API verfügbar

## Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert. 