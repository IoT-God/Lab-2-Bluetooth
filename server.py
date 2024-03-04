import bluetooth
import picar_4wd as fc
import json
import threading
import time

def send_server_info():
    server_info = {
        "cpu_temperature": fc.cpu_temperature(),
        "power_level": fc.power_read()
    }
    return json.dumps(server_info).encode()

hostMACAddress = "dc:a6:32:92:06:d6"  # The address of Raspberry PI Bluetooth adapter on the server. The server might have multiple Bluetooth adapters.
port = 0
backlog = 1
size = 1024
s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
s.bind((hostMACAddress, port))
s.listen(backlog)
print("listening on port ", port)

try:
    client, clientInfo = s.accept()
    print("server recv from: ", clientInfo)

    while True:
        data = client.recv(size)
        if data:
            print(data)
            if "cpu" in str(data):
                cpu_tem = str(fc.cpu_temperature())
                message = "CPU temperature is " + cpu_tem + "Fahrenheit.\n"
                client.send(message.encode())
            elif "power" in str(data):
                cpu_tem = str(fc.power_read())
                message = "Power is at " + cpu_tem + "%.\n"
                client.send(message.encode())
            else:
                client.send(send_server_info() + "\n".encode())

            client.send("Your message is: ".encode() + data)


except Exception as e:
    print("Error:", e)
    print("Closing socket")
    client.close()
    s.close()
