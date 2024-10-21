# Erase
esptool.py --port /dev/cu.usbserial-0001 erase_flash

# Flash
esptool.py --port /dev/cu.usbserial-0001 --baud 460800 write_flash --flash_size=detect 0 ESP8266_GENERIC-20240602-v1.23.0.bin

# Serial
picocom /dev/cu.usbserial-0001 -b115200

#
```
CREATE TABLE sensor_reading (
    id SERIAL PRIMARY KEY,
    location text NOT NULL,
    timestamp timestamp NOT NULL,
    type text NOT NULL,
    value decimal NOT NULL
);