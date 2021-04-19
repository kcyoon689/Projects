#include <Wire.h>
#include <Servo.h>
#define SerialPort Serial
#include <SparkFunMPU9250-DMP.h>
MPU9250_DMP imu;
double roll , pitch, yaw;
long int pre_ts=0;

//휨센서
const int FLEX1=A0;
const int FLEX2=A1;
const int FLEX3=A2;

const float Vcc=4.98;
const float R_DIV=47500.0;

const float STRAIGHT_R=37300.0;
const float BEND_R=90000.0;

//int flexsensor1 = 0;
//int flexsensor2 = 0;
//int flexsensor3 = 0;

 
void setup() 
{
 
    {
  SerialPort.begin(9600);
  Serial.println("CLEARDATA"); //엑셀 리셋.
  Serial.println("LABEL,Time,pitch, roll, yaw, Flex 01, Flex 02, Flex 03"); // 라벨 설정(PLX-DAQ) 연동..
  pinMode(FLEX1,INPUT);
  pinMode(FLEX2,INPUT);
  pinMode(FLEX3,INPUT);
  
 if (imu.begin() != INV_SUCCESS)
  {
    while (1)
    {
      SerialPort.println("Unable to communicate with MPU-9250");
      SerialPort.println("Check connections, and try again.");
      SerialPort.println();
      delay(3000);
    }
  }
 
  
  imu.setSensors(INV_XYZ_GYRO | INV_XYZ_ACCEL | INV_XYZ_COMPASS);
 
  
  imu.setGyroFSR(250);
  imu.setAccelFSR(2); 
  imu.setLPF(10); 
  imu.setSampleRate(10); 
  imu.setCompassSampleRate(50); 
}
 
  pre_ts=millis();
}
 
void loop() 
{
  int flexADC1 = analogRead(FLEX1);
  int flexADC2 = analogRead(FLEX2);
  int flexADC3 = analogRead(FLEX3);
  
  float flexV1 = flexADC1 * Vcc / 1023.0;
  float flexR1 = R_DIV * (Vcc /flexV1 - 1.0);
  
  float flexV2 = flexADC2 * Vcc / 1023.0;
  float flexR2 = R_DIV * (Vcc /flexV2 - 1.0);
  
  float flexV3 = flexADC3 * Vcc / 1023.0;
  float flexR3 = R_DIV * (Vcc /flexV3 - 1.0);

   Serial.print(flexR1);
   Serial.print(",");
   Serial.print(flexR2);
   Serial.print(",");
   Serial.println(flexR3); 
  
    if ( imu.dataReady() )
  {
    imu.update(UPDATE_ACCEL | UPDATE_GYRO | UPDATE_COMPASS);
    printIMUData(millis()-pre_ts);
    pre_ts=millis();
  }
}
 
void printIMUData(long int dt)
{  
   
  float accelX = imu.calcAccel(imu.ax);
  float accelY = imu.calcAccel(imu.ay);
  float accelZ = imu.calcAccel(imu.az);
  float gyroX = imu.calcGyro(imu.gx)/57.3;
  float gyroY = imu.calcGyro(imu.gy)/57.3;
  float gyroZ = imu.calcGyro(imu.gz)/57.3;
  float magX = imu.calcMag(imu.mx); 
  float magY = imu.calcMag(imu.my);
  float magZ = imu.calcMag(imu.mz);
 
 // SerialPort.println("Accel: " + String(accelX) + ", " + String(accelY) + ", " + String(accelZ) + " g");
 // SerialPort.println("Gyro: " + String(gyroX) + ", " + String(gyroY) + ", " + String(gyroZ) + " dps");
 // SerialPort.println("Mag: " + String(magX) + ", " + String(magY) + ", " + String(magZ) + " uT");
 // SerialPort.println("Time: " + String(imu.time) + " ms");
 
  
   pitch = atan2 (accelY ,( sqrt ((accelX * accelX) + (accelZ * accelZ))));
   roll = atan2(-accelX ,( sqrt((accelY * accelY) + (accelZ * accelZ))));
 
   // yaw - 지자계 이용 
   float Yh = (magY * cos(roll)) - (magZ * sin(roll));
   float Xh = (magX * cos(pitch))+(magY * sin(roll)*sin(pitch)) + (magZ * cos(roll) * sin(pitch));
 
   yaw =  atan2(Yh, Xh);
 
    roll = roll*57.3;
    pitch = pitch*57.3;
    yaw = yaw*57.3;

   Serial.print("DATA,TIME,"); //현재 시간 출력(프로그램 연동)
   Serial.print(pitch);
   Serial.print(",");
   Serial.print(roll);
   Serial.print(",");
   Serial.print(yaw);
   Serial.print(",");
   
 delay(1000);
}
