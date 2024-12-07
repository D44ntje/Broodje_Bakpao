import socket

PICO_IP = '192.168.137.132'  # Replace with the IP address of your Pico W
PICO_PORT = 12345          # The same port number used on the Pico W

def communicate_with_pico():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((PICO_IP, PICO_PORT))
        print(f"Connected to Pico W at {PICO_IP}:{PICO_PORT}")

        while True:
            message = input("Enter a message to send (or 'exit' to quit): ")
            if message.lower() == 'exit':
                break

            client.send(message.encode('utf-8'))  # Send the message to the Pico
            response = client.recv(1024).decode('utf-8')  # Receive the response
            print(f"Response from Pico: {response}")

    except Exception as e:
        print("Connection error:", e)
    finally:
        client.close()
        print("Disconnected from Pico W")

communicate_with_pico()
