#include "WiFi.h"
#include <BLAKE2s.h>
#include <Preferences.h>

const unsigned int SLIZE_SIZE = 30;
const unsigned int MILLIS_PER_SECOND = 1000;
const size_t SSID_LEN = 32;
const size_t WIFI_KEY_LEN = 32;
const uint8_t HMAC_KEY1[] = { "WiFi-CnC" };
const uint8_t HMAC_KEY2[] = { "Midnight" };
const char CNC_SERVER_IP[] = "10.0.0.137";

Preferences preferences;

void setup_flag() {
    preferences.begin("midnight", false);
    Serial.println("Waiting for flag");
    for(int i = 0; i < 10 && Serial.available() <= 0; i++) {
        delay(500);
    }
    if(Serial.available() > 0) {
        String flag = Serial.readStringUntil('\n');
        preferences.putString("flag", flag);
        Serial.print("Storing flag: ");
    } else {
        Serial.print("No flag sent. Using stored flag: ");
    }
    Serial.println(preferences.getString("flag"));
    preferences.end();
}

void setup()
{
    Serial.begin(115200);
    setup_flag();

    // Set WiFi to station mode and disconnect from an AP if it was previously connected
    WiFi.mode(WIFI_STA);
    WiFi.disconnect();
    delay(100);

    Serial.println("Setup done");
}

unsigned int get_timeslice() {
    return millis() / MILLIS_PER_SECOND / SLIZE_SIZE;
}

// Generates an 8 byte long SSID based on the time since start
void generate_ssid(char *dst) {
    uint8_t hash[32];
    char timeslice[8+1];

    sprintf(timeslice, "%08x", get_timeslice());

    BLAKE2s blake;
    blake.resetHMAC(HMAC_KEY1, sizeof(HMAC_KEY1));
    blake.update(timeslice, 8);
    blake.finalizeHMAC(HMAC_KEY1, sizeof(HMAC_KEY1), hash, 32);

    sprintf(dst, "CnC_%02hhx%02hhx%02hhx%02hhx", hash[0], hash[1], hash[2], hash[3]);
}

void generate_wifi_key(char *dst) {
    uint8_t hash[32];
    char timeslice[8+1];
    char chipid[16+1];

    sprintf(timeslice, "%08x", get_timeslice());
    sprintf(chipid, "%016llx", ESP.getEfuseMac());

#ifdef DEBUG
    Serial.print("Chip: ");
    Serial.println(chipid);
#endif

    BLAKE2s blake;
    blake.resetHMAC(HMAC_KEY2, sizeof(HMAC_KEY2));
    blake.update(timeslice, 8);
    blake.finalizeHMAC(HMAC_KEY2, sizeof(HMAC_KEY2), hash, 32);

    sprintf(dst, "%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx", hash[0], hash[1], hash[2], hash[3], hash[4], hash[5], hash[6], hash[7]);
}

void process_command(WiFiClient &client, String &cmd) {
    Serial.print("Processing command: ");
    Serial.println(cmd);
    if(cmd == "help") {
        client.println("WiFi DGA System");
        client.println("Command:");
        client.println("help - print this help");
        client.println("flag - get the stored flag");
        client.println("store - store a message for other teams");
        client.println("read - read a message stored by other team");
    } else if(cmd == "flag") {
        preferences.begin("midnight", false);
        client.print("Flag: ");
        client.println(preferences.getString("flag"));
        preferences.end();
    } else if(cmd == "read") {
        preferences.begin("midnight", false);
        client.print("Message: ");
        client.println(preferences.getString("message"));
        preferences.end();
    } else if(cmd == "store") {
        String message = client.readStringUntil('\n');
        preferences.begin("midnight", false);
        preferences.putString("message", message);
        client.print("Storing message: ");
        client.println(preferences.getString("message"));
        preferences.end();
    }
}

void wifi_connected() {
    Serial.println("Connected to WiFi");
    Serial.print("IP: ");
    Serial.println(WiFi.localIP());

    WiFiClient client;
    if(client.connect(CNC_SERVER_IP, 31337)) {
        String line = client.readStringUntil('\n');
        Serial.print("Command: ");
        Serial.println(line);
        process_command(client, line);
        client.stop();
    }
}

void wifi_try_connect() {
    char ssid[SSID_LEN];
    char wifi_key[WIFI_KEY_LEN];

    generate_ssid(ssid);
    generate_wifi_key(wifi_key);

#ifdef DEBUG
    Serial.print("SSID: ");
    Serial.println(ssid);
    Serial.print("Key: ");
    Serial.println(wifi_key);
#endif

    WiFi.disconnect();
    for(int i = 0; i < 20 && WiFi.status() == WL_CONNECTED; i++) {
        delay(100);
    }
    WiFi.begin(ssid, wifi_key);

    // Try to connect to for 10 seconds
    for(int i = 0; i < 20 && WiFi.status() != WL_CONNECTED; i++) {
        delay(500);
    }

    if(WiFi.status() == WL_CONNECTED) {
        wifi_connected();
    } else {
        Serial.println("Failed to connect to WiFi");
    }
}

unsigned int current_slice = 0;
void loop()
{
    unsigned int new_slice = get_timeslice();
    if(new_slice != current_slice) {
#ifdef DEBUG
        Serial.print("Time slice: ");
        Serial.println(get_timeslice());
#endif

        current_slice = new_slice;
        wifi_try_connect();
    }

    delay(1000);
}
