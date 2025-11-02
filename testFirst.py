import time
import board
import adafruit_dht
import requests
import os
from dotenv import load_dotenv

load_dotenv()

THINGSPEAK_WRITE_API_KEY = os.getenv("THINGSPEAK_API_KEY")
THINGSPEAK_URL = "https://api.thingspeak.com/update"

if THINGSPEAK_WRITE_API_KEY is None:
    print("BŁĄD KRYTYCZNY: Nie znaleziono 'THINGSPEAK_API_KEY' w pliku .env")
    print("Upewnij się, że plik .env istnieje i zawiera poprawny klucz.")
    exit()

PIN_CZUJNIKA = board.D4

try:
    dhtDevice = adafruit_dht.DHT22(PIN_CZUJNIKA)
except Exception as e:
    print(f"Nie można zainicjować czujnika na pinie {PIN_CZUJNIKA}: {e}")
    print("Sprawdź podłączenie i czy skrypt ma uprawnienia.")
    exit()

print("Rozpoczynanie odczytu z DHT22 i wysyłanie do ThingSpeak (CTRL+C aby zakończyć)")
print("=" * 40)

while True:
    try:
        temperatura_c = dhtDevice.temperature
        wilgotnosc = dhtDevice.humidity

        if wilgotnosc is not None and temperatura_c is not None:
            print(f"Odczyt: Temperatura: {temperatura_c:.1f}°C | Wilgotność: {wilgotnosc:.1f}%")

            try:
                payload = {
                    'api_key': THINGSPEAK_WRITE_API_KEY,
                    'field1': temperatura_c,
                    'field2': wilgotnosc
                }

                response = requests.post(THINGSPEAK_URL, data=payload)

                if response.status_code == 200:
                    print(f"Wysłano do ThingSpeak (ID wpisu: {response.text})")
                else:
                    print(f"Błąd ThingSpeak. Status: {response.status_code}, Treść: {response.text}")

            except requests.exceptions.RequestException as e:
                print(f"Błąd połączenia z ThingSpeak: {e}")

        else:
            print("Odczyt z DHT nie powiódł się (zwrócono None). Próbuję ponownie...")

    except RuntimeError as error:
        print(f"Błąd odczytu DHT: {error.args[0]}. Próbuję ponownie...")
    except Exception as error:
        dhtDevice.exit()
        raise error

    print("--- Czekam 10 sekund na kolejny odczyt i wysłanie ---")
    time.sleep(10.0)