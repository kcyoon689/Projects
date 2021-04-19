#include <SoftwareSerial.h>
SoftwareSerial GPS(2,3); //TX - D2, RX - D3

void setup() {
  GPS.begin(19200);
  Serial.begin(9600);
  
}

void loop() {
  if(Serial.available()){
    GPS.write(Serial.read());
  }
  if(GPS.available()){
    Serial.write(GPS.read());
  }
}
