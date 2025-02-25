import machine
import time
import network
import dht
import urequests
from machine import ADC

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("SIC","12345678")

while not wlan.isconnected():
    print(".",end="")
    time.sleep(1)

print("WLAN is connected")
UBIDOTS_ENDPOINT = "https://industrial.api.ubidots.com/api/v1.6/devices/esp32-sic6/"
FLASK_ENDPOINT = "http://192.168.114.21:5000/save"

ldr = ADC(machine.Pin(32))  # Pindah ke ADC1 (GPIO 32)
ldr.atten(ADC.ATTN_11DB)    # Konfigurasi agar bisa membaca 0-3.3V

sensor = dht.DHT11(machine.Pin(14))
while True:
    nilaiCahaya = ldr.read()  # Baca nilai ADC (0-1023)
    intensitas_cahaya = (1 - (nilaiCahaya / 4095)) * 100  # Untuk ESP32 dengan ADC 12-bit
  # Konversi ke persen (opsional)
    sensor.measure()
    suhu = sensor.temperature()
    kelembaban = sensor.humidity()
    print(f"Suhu = {suhu} C, kelembaban = {kelembaban} %")
    print("Nilai ADC:", nilaiCahaya, "intensitas Cahaya:", intensitas_cahaya, "%")
    data = {"suhu":suhu,
            "kelembaban":kelembaban,
            "intensitas_cahaya":intensitas_cahaya}
    headers = {"Content-Type":"application/json","X-Auth-Token":"BBUS-3wz43JETA7AxoTXGRj6vk1nJ8ITvi8"}
    response = urequests.post(UBIDOTS_ENDPOINT,json=data,headers=headers)
    
    print(f"response ubidots: {response.status_code}")
    response.close()
    
    
    headers = {"Content-Type":"application/json"}
    response = urequests.post(FLASK_ENDPOINT,json=data,headers=headers)
    
    print(f"response flask: {response.status_code}")
    response.close()
    
    time.sleep(6)