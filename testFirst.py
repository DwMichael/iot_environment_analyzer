import os
import time
import adafruit_dht
import board
import requests
from dotenv import load_dotenv
from pmv_ppd_calculate import pmv_ppd_calc


THINGSPEAK_URL = "https://api.thingspeak.com/update"
PIN_CZUJNIKA = board.D4
INTERVAL_READ_SEC = 60.0
SEND_OPTIONALS = False # Send PMV and PPD

# Klucz API
THINGSPEAK_WRITE_API_KEY = None


def load_config():
    global THINGSPEAK_WRITE_API_KEY
    load_dotenv()

    THINGSPEAK_WRITE_API_KEY = os.getenv("THINGSPEAK_API_KEY")

    if not THINGSPEAK_WRITE_API_KEY:
        print("Nie znaleziono albo niepoprawny klucz API ThingSpeak w pliku .env")
        return False

    print("Klucz API poprawny!")
    return True


def dht_init(pin):
    try:
        dhtDevice = adafruit_dht.DHT22(pin)
        print(f"Poprawnie zainicjowano czujnik DHT22 na pinie {pin}")
        return dhtDevice
    except Exception as err:
        print(f"Nie można zainicjować czujnika na pinie {pin}: {err}")
        return None


def read_data_from_dht(dht):
    try:
        temperature = dht.temperature
        humidity = dht.humidity

        if humidity is None or temperature is None:
            print("Odczyt z DHT nie powiódł się. Próbuję ponownie...")
            return None, None

        print(f"Temperatura: {temperature:.1f}°C  |  Wilgotność: {humidity:.1f}%")

        return temperature, humidity
    except RuntimeError as error:
        print(f"Błąd odczytu DHT: {error.args[0]}. Próbuję ponownie...")
        return None, None
    except Exception as e:
        print(f"Nieoczekiwany błąd podczas odczytu czujnika: {e}")
        return None, None


def send_to_thingspeak(temperature, humidity, pmv, ppd, send_optionals=False):
    payload = {}

    if not send_optionals:
        payload = {
            'api_key': THINGSPEAK_WRITE_API_KEY,
            'field1': temperature,
            'field2': humidity,
        }
    else:
        payload = {
            'api_key': THINGSPEAK_WRITE_API_KEY,
            'field1': temperature,
            'field2': humidity,
            'field3': pmv,
            'field4': ppd
        }

    try:
        response = requests.post(THINGSPEAK_URL, data=payload)

        if response.status_code == 200:
            print(f"Poprawnie wysłano do ThingSpeak (ID wpisu: {response.text.strip()})")
        else:
            print(f"Błąd ThingSpeak. Status: {response.status_code}, Treść: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Błąd połączenia z ThingSpeak: {e}")


def main():
    if not load_config():
        return

    dht_device = dht_init(PIN_CZUJNIKA)
    if not dht_device:
        return

    print("Rozpoczynanie odczytu z DHT22 i wysyłanie do ThingSpeak (CTRL+C aby zakończyć)")
    print("=" * 40)

    try:
        while True:

            # Odczyt danych z DHT
            temperature, humidity = read_data_from_dht(dht_device)

            if temperature is None and humidity is None:
                continue

            # Obliczanie wskaźników
            pmv, ppd = pmv_ppd_calc(temperature, humidity) if SEND_OPTIONALS else (None, None)

            # Wysyłanie danych do Thingspeak
            send_to_thingspeak(temperature, humidity, pmv, ppd, SEND_OPTIONALS)

            print(f"--- Czekam {INTERVAL_READ_SEC}s ---")
            print("=" * 40)
            time.sleep(INTERVAL_READ_SEC)

    except KeyboardInterrupt:
        print("\nPrzerwano przez użytkownika (CTRL+C)")
    except Exception as e:
        print(f"Wystąpił nieoczekiwany błąd: {e}")
    finally:
        if dht_device:
            dht_device.exit()
        print("Program zakończony")


if __name__ == "__main__":
    main()
