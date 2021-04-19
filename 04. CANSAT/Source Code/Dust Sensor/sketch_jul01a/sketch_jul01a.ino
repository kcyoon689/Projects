int measurePin = A0;
int ledPower = 5;
 
int samplingTime = 280;
int deltaTime = 40;
int sleepTime = 9680;
 
float voMeasured = 0;
float calcVoltage = 0;
float dustDensity = 0;
 
void setup(){
  Serial.begin(9600);
  pinMode(A0,INPUT);
  pinMode(ledPower,OUTPUT);
}
 
void loop(){
  digitalWrite(ledPower,LOW); // power on the LED
  delayMicroseconds(samplingTime);
 
  voMeasured = analogRead(measurePin); // read the dust value
 
  delayMicroseconds(deltaTime);
  digitalWrite(ledPower,HIGH); // turn the LED off
  delayMicroseconds(sleepTime);
 
  calcVoltage = voMeasured * (5.0 / 1023);
  //calcVoltage = voMeasured * (3.3 / 1023); // sensing test 해보기..
 
  dustDensity = 0.167 * calcVoltage - 0.1;
 
 // Serial.print("Raw Signal Value (0-1023): ");
 // Serial.print(voMeasured);
 
 // Serial.print(" - Voltage: ");
 // Serial.print(calcVoltage);
 
  Serial.print(" - Dust Density: ");
  Serial.println(dustDensity); // unit: mg/m^3
 
  delay(1000);
}
