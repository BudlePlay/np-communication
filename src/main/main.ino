#include <ArduinoBLE.h>
#include <Arduino_LSM9DS1.h>
#include "DFRobotDFPlayerMini.h"
#include <Adafruit_NeoPixel.h>

#define LED_PIN 2
#define LED_COUNT 93
Adafruit_NeoPixel strip(LED_COUNT, LED_PIN, NEO_GRB + NEO_KHZ800);

DFRobotDFPlayerMini myDFPlayer;

BLEService Service("00000000-0000-0000-0000-000000000000");

BLEByteCharacteristic Read1("00000000-0000-0000-0000-000000000011", BLEWrite);

BLEFloatCharacteristic Write1("00000000-0000-0000-0000-000000000021", BLERead);
BLEFloatCharacteristic Write2("00000000-0000-0000-0000-000000000022", BLERead);
BLEFloatCharacteristic Write3("00000000-0000-0000-0000-000000000023", BLERead);
BLEFloatCharacteristic Write4("00000000-0000-0000-0000-000000000024", BLERead);
BLEFloatCharacteristic Write5("00000000-0000-0000-0000-000000000025", BLERead);
BLEFloatCharacteristic Write6("00000000-0000-0000-0000-000000000026", BLERead);

float accel_x, accel_y, accel_z;
float gyro_x, gyro_y, gyro_z;

unsigned int serial_prev_time, led_prev_time;

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
  if (!myDFPlayer.begin(Serial1))
  { //Use softwareSerial to communicate with mp3.
    Serial.println(F("Unable to begin:"));
    Serial.println(F("1.Please recheck the connection!"));
    Serial.println(F("2.Please insert the SD card!"));
  }

  strip.begin();
  strip.show();
  strip.setBrightness(255);

  myDFPlayer.volume(30);

  BLE.setLocalName("NEO_Player");
  BLE.setAdvertisedService(Service);

  Service.addCharacteristic(Read1);
  Service.addCharacteristic(Write1);
  Service.addCharacteristic(Write2);
  Service.addCharacteristic(Write3);
  Service.addCharacteristic(Write4);
  Service.addCharacteristic(Write5);
  Service.addCharacteristic(Write6);
  BLE.addService(Service);

  BLE.advertise();

  delay(100);
  myDFPlayer.play(1);
  colorWipe(strip.Color(0, 0, 255), 1);
}

void loop()
{
  if (IMU.accelerationAvailable())
    IMU.readAcceleration(accel_x, accel_y, accel_z);
  if (IMU.gyroscopeAvailable())
    IMU.readGyroscope(gyro_x, gyro_y, gyro_z);

  if(millis()-serial_prev_time>100){
    Serial.print(accel_x); Serial.print(", "); Serial.print(accel_y); Serial.print(", "); Serial.print(accel_z); Serial.print(", ");
    Serial.print(gyro_x); Serial.print(", "); Serial.print(gyro_y); Serial.print(", "); Serial.println(gyro_z);
    serial_prev_time=millis();
  }
  if(millis()-led_prev_time>2000) colorAll(strip.Color(0, 0, 255));
  if(Serial.available()){
      int read_data=Serial.read();     
      if(read_data=='1'){
        colorAll(strip.Color(255, 255, 255));
        led_prev_time=millis();
      }
      else if(read_data=='2'){
        colorAll(strip.Color(255, 0, 0));
        led_prev_time=millis();
      }
  }
  
  
//  BLEDevice central = BLE.central();
//  if (central)
//  {
//    Serial.print("Connected to central: ");
//    Serial.println(central.address());
//    while (central.connected())
//    {
//      if (IMU.accelerationAvailable())
//        IMU.readAcceleration(accel_x, accel_y, accel_z);
//      if (IMU.gyroscopeAvailable())
//        IMU.readGyroscope(gyro_x, gyro_y, gyro_z);
//
//      Serial.print(accel_x); Serial.print(", "); Serial.print(accel_y); Serial.print(", "); Serial.print(accel_z); Serial.print(", ");
//      Serial.print(gyro_x); Serial.print(", "); Serial.print(gyro_y); Serial.print(", "); Serial.println(gyro_z);
//
//      Write1.writeValue(accel_x);
//      Write2.writeValue(accel_y);
//      Write3.writeValue(accel_z);
//      Write4.writeValue(gyro_x);
//      Write5.writeValue(gyro_y);
//      Write6.writeValue(gyro_z);
//      delay(100);
//    }
//    Serial.print(F("Disconnected from central: "));
//    Serial.println(central.address());
//  }
}
void colorWipe(uint32_t color, int wait)
{
  for (int i = 0; i < strip.numPixels(); i++)
  { // For each pixel in strip...
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
