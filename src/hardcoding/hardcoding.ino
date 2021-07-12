#include <ArduinoBLE.h>
#include <Arduino_LSM9DS1.h>
#include <Adafruit_NeoPixel.h>

#define LED_PIN 2
#define LED_COUNT 93
Adafruit_NeoPixel strip(LED_COUNT, LED_PIN, NEO_GRB + NEO_KHZ800);

BLEService Service("00000000-0000-0000-0000-000000000000");

BLEByteCharacteristic Write1("00000000-0000-0000-0000-000000000021", BLERead | BLEWrite);

float accel_x, accel_y, accel_z;
float gyro_x, gyro_y, gyro_z;

unsigned int serial_prev_time, led_prev_time;

void colorWipe(uint32_t color, int wait);
void colorAll(uint32_t color);

void setup()
{
    Serial.begin(115200);
    Serial1.begin(9600);

    if (!IMU.begin())
    { //LSM9DSI센서 시작
        Serial.println("LSM9DSI센서 오류!");
    }
    if (!BLE.begin())
    {
        Serial.println("starting BLE failed!");
    }

    strip.begin();
    strip.show();
    strip.setBrightness(255);

    BLE.setLocalName("NEO_Player");
    BLE.setAdvertisedService(Service);

    Service.addCharacteristic(Write1);
    BLE.addService(Service);

    BLE.advertise();

    delay(100);
    colorWipe(strip.Color(0, 0, 255), 1);
}

void loop()
{
    BLEDevice central = BLE.central();
    if (central)
    {
        while (central.connected())
        {
            if (IMU.accelerationAvailable())
                IMU.readAcceleration(accel_x, accel_y, accel_z);
            if (IMU.gyroscopeAvailable())
                IMU.readGyroscope(gyro_x, gyro_y, gyro_z);
            if (millis() - led_prev_time > 2000){
                Write1.writeValue(0);
                colorAll(strip.Color(0, 0, 255));
            }
            // GY가 몇초안에 200 이상
            if (gyro_y<-200){
                Write1.writeValue(1);
                colorAll(strip.Color(255, 255, 0));
                led_prev_time = millis();
            }
            if (abs(accel_x) >= 2)
            {
                Write1.writeValue(2);
                colorAll(strip.Color(255, 0, 0));
                led_prev_time = millis();
            }
        }
    }
    else{
      if (IMU.accelerationAvailable())
        IMU.readAcceleration(accel_x, accel_y, accel_z);
      if (IMU.gyroscopeAvailable())
          IMU.readGyroscope(gyro_x, gyro_y, gyro_z);
      if (millis() - led_prev_time > 2000){
          colorAll(strip.Color(0, 0, 255));
      }
      // GY가 몇초안에 200 이상
      if (gyro_y<-200){
          colorAll(strip.Color(255, 255, 0));
          led_prev_time = millis();
      }
      if (abs(accel_x) >= 2)
      {
          colorAll(strip.Color(255, 0, 0));
          led_prev_time = millis();
      }  
    }
}
void colorWipe(uint32_t color, int wait)
{
    for (int i = 0; i < strip.numPixels(); i++)
    {                                  // For each pixel in strip...
        strip.setPixelColor(i, color); //  Set pixel's color (in RAM)
        strip.show();                  //  Update strip to match
        delay(wait);                   //  Pause for a moment
    }
}
void colorAll(uint32_t color)
{
    for (int i = 0; i < strip.numPixels(); i++)
    {
        strip.setPixelColor(i, color);
    }
    strip.show();
}
