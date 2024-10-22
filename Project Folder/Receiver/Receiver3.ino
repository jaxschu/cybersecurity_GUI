#include <SPI.h>
#include <RH_RF95.h>

// RC4 encryption functions
void RC4_init(uint8_t* key, uint8_t* S, uint8_t key_length) {
    for (int i = 0; i < 256; i++) {
        S[i] = i;
    }

    int j = 0;
    for (int i = 0; i < 256; i++) {
        j = (j + S[i] + key[i % key_length]) % 256;
        uint8_t temp = S[i];
        S[i] = S[j];
        S[j] = temp;
    }
}

void RC4_crypt(uint8_t* data, int data_length, uint8_t* S) {
    int i = 0, j = 0;
    for (int n = 0; n < data_length; n++) {
        i = (i + 1) % 256;
        j = (j + S[i]) % 256;

        uint8_t temp = S[i];
        S[i] = S[j];
        S[j] = temp;

        uint8_t K = S[(S[i] + S[j]) % 256];
        data[n] ^= K;
    }
}

// Define pins
#define RFM95_CS 10
#define RFM95_RST 9
#define RFM95_INT 2

// Define the RF95 object
RH_RF95 rf95(RFM95_CS, RFM95_INT);

// RC4 key and S-box array
uint8_t key[] = "Lora";  // Define your key here
uint8_t S[256];          // S-box for RC4

// Unique username
String username = "HostB";  // Default username

void setup() {
    Serial.begin(9600);
    while (!Serial);

    pinMode(RFM95_RST, OUTPUT);
    digitalWrite(RFM95_RST, HIGH);

    // Manual reset
    digitalWrite(RFM95_RST, LOW);
    delay(10);
    digitalWrite(RFM95_RST, HIGH);
    delay(10);

    if (!rf95.init()) {
        Serial.println("LoRa init failed!");
        while (1);
    }

    if (!rf95.setFrequency(915.0)) {
        Serial.println("setFrequency failed");
        while (1);
    }

    Serial.println("LoRa Transceiver ready");
    

    // Initialize RC4 with the key
    RC4_init(key, S, sizeof(key) - 1);
}

void loop() {
    // Check if a packet is received
    if (rf95.available()) {
        // Buffer to hold the incoming message
        uint8_t buf[RH_RF95_MAX_MESSAGE_LEN];
        uint8_t len = sizeof(buf);

        // Receive the message
        if (rf95.recv(buf, &len)) {
            //Serial.print("Received encrypted message: ");
            for (int i = 0; i < len; i++) {
                // Serial.print(buf[i], HEX);
                // Serial.print("");
            }
            // Serial.println();

            // Decrypt the message using RC4
            RC4_crypt(buf, len, S);

            // Print the decrypted message without the receiver's username
            // Serial.print("Decrypted message: ");
            for (uint8_t i = 0; i < len; i++) {
                Serial.print((char)buf[i]);
            }
            Serial.println();

            // Print RSSI (signal strength)
            // Serial.print("RSSI: ");
            // Serial.println(rf95.lastRssi(), DEC);
        } else {
            Serial.println("Receive failed");
        }
    }

    // Check if user entered something in Serial Monitor
    if (Serial.available()) {
        // Read the user input
        String message =  Serial.readStringUntil('\n');

        // Prompt user for username if it's not set
        if (username.length() == 0) {
            Serial.print("Enter your username: ");
            while (!Serial.available()) {}  // Wait for user input
            username = Serial.readStringUntil('\n');  // Read the username
            Serial.print("Username set to: ");
            Serial.println(username);
        }

        // Prepend username to the message
        String fullMessage = username + ": " + message;

        // Check message length
        int messageLength = fullMessage.length();
        if (messageLength > RH_RF95_MAX_MESSAGE_LEN) {
            Serial.println("Message too long!");
            return;
        }

        // Convert message to byte array
        uint8_t data[messageLength + 1];
        fullMessage.getBytes(data, sizeof(data));

        // Encrypt the data using RC4
        RC4_crypt(data, messageLength, S);

        // Send the encrypted message
        rf95.send(data, messageLength);
        rf95.waitPacketSent();

        // Serial.print("Encrypted message sent.");
    }

    delay(100);  // Small delay to avoid overwhelming the serial input
}
