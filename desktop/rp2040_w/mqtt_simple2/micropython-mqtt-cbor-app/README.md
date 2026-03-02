# MicroPython MQTT CBOR Application

This project implements an asynchronous MQTT application using MicroPython, which supports keep-alive functionality and CBOR serialization for message formatting. The application allows two devices to publish and subscribe to messages on the topic "test/topic_rp2040_w".

## Project Structure

```
micropython-mqtt-cbor-app
├── src
│   ├── main.py          # Main entry point of the application
│   ├── simple2.py       # MQTT client implementation
│   ├── cbor.py          # CBOR serialization logic
│   └── config.py        # Configuration settings
└── README.md            # Project documentation
```

## Setup Instructions

1. **Clone the repository**:
   ```
   git clone <repository-url>
   cd micropython-mqtt-cbor-app
   ```

2. **Install MicroPython** on your device if not already installed.

3. **Upload the files** in the `src` directory to your MicroPython device.

4. **Modify the `config.py`** file to set your MQTT broker address, client ID, and other parameters as needed.

## Usage

1. **Run the application**:
   - Execute the `main.py` file on your MicroPython device:
     ```
     python main.py
     ```

2. **Publishing Messages**:
   - The application will publish messages to the topic "test/topic_rp2040_w" using CBOR serialization.

3. **Subscribing to Messages**:
   - The application will also subscribe to the same topic and handle incoming messages.

## Functionality Overview

- **Asynchronous MQTT Client**: The application uses the `simple2.py` library to manage MQTT connections and message handling.
- **Keep-Alive Support**: The MQTT client maintains a keep-alive connection to the broker.
- **CBOR Serialization**: Messages are serialized using CBOR format for efficient transmission.

## Example

- To publish a message, modify the `main.py` file to include your desired payload and call the publish method of the MQTT client.
- To receive messages, implement a callback function in `main.py` that processes incoming messages.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.