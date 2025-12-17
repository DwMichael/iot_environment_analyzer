# IoT System monitorowania temperatury i wilgotności z obliczeniem współczynnika komfortu mikroklimatycznego

Projekt IoT w Pythonie, który monitoruje temperaturę i wilgotność za pomocą czujnika DHT22, wysyła dane do ThingSpeak i oblicza wskaźniki komfortu cieplnego (PMV/PPD).

## Instalacja

1. Klonowanie repozytorium
2. Wirtualne środowisko:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
3. Wymagane biblioteki:
   ```bash
   pip install -r requirements.txt
   ```
4. Stworzenie pliku `.env` z kluczem API do ThingSpeaka:
   ```ini
   THINGSPEAK_API_KEY = your_api_key
   ```
