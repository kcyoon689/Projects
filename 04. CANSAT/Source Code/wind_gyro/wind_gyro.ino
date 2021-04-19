#include <Wire.h>
#include <Servo.h>
#define SerialPort Serial
#include <SparkFunMPU9250-DMP.h>

#define analogPinForTMP1   8    // change to pins you the analog pins are using
#define analogPinForRV1    9 
  
#define analogPinForTMP2   10
#define analogPinForRV2    11
   
#define analogPinForTMP3   12
#define analogPinForRV3    13

MPU9250_DMP imu;
double roll , pitch, yaw;
long int pre_ts=0;

const float zeroWindAdjustment1 =  .2; // negative numbers yield smaller wind speeds and vice versa.
const float zeroWindAdjustment2 =  .2;
const float zeroWindAdjustment3 =  .2;

int TMP_Therm_ADunits1;  //temp termistor value from wind sensor
float RV_Wind_ADunits1;    //RV output from wind sensor 
float RV_Wind_Volts1;

int TMP_Therm_ADunits2;
float RV_Wind_ADunits2;
float RV_Wind_Volts2;

int TMP_Therm_ADunits3;
float RV_Wind_ADunits3;
float RV_Wind_Volts3;

unsigned long lastMillis;

int TempCtimes100;
int TempCtimes200;
int TempCtimes300;

float zeroWind_ADunits1;
float zeroWind_volts1;
float WindSpeed_MPH1;

float zeroWind_ADunits2;
float zeroWind_volts2;
float WindSpeed_MPH2;

float zeroWind_ADunits3;
float zeroWind_volts3;
float WindSpeed_MPH3;

void setup() {
{
  SerialPort.begin(9600);
  Serial.println("start");
  Serial.println("CLEARDATA"); //엑셀 리셋.
  Serial.println("LABEL,Time,pitch, roll, yaw, WS 01, WS 02, WS 03"); // 라벨 설정(PLX-DAQ) 연동..
  
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
    if (millis() - lastMillis > 200){      // read every 200 ms - printing slows this down further

    TMP_Therm_ADunits1 = analogRead(analogPinForTMP1);
    RV_Wind_ADunits1 = analogRead(analogPinForRV1);
    RV_Wind_Volts1 = (RV_Wind_ADunits1 *  0.0048828125);

    TMP_Therm_ADunits2 = analogRead(analogPinForTMP2);
    RV_Wind_ADunits2 = analogRead(analogPinForRV2);
    RV_Wind_Volts2 = (RV_Wind_ADunits2 *  0.0048828125);
    
    TMP_Therm_ADunits3 = analogRead(analogPinForTMP3);
    RV_Wind_ADunits3 = analogRead(analogPinForRV3);
    RV_Wind_Volts3 = (RV_Wind_ADunits3 *  0.0048828125);

    // these are all derived from regressions from raw data as such they depend on a lot of experimental factors
    // such as accuracy of temp sensors, and voltage at the actual wind sensor, (wire losses) which were unaccouted for.

    TempCtimes100 = (0.005 *((float)TMP_Therm_ADunits1 * (float)TMP_Therm_ADunits1)) - (16.862 * (float)TMP_Therm_ADunits1) + 9075.4;  
    zeroWind_ADunits1 = -0.0006*((float)TMP_Therm_ADunits1 * (float)TMP_Therm_ADunits1) + 1.0727 * (float)TMP_Therm_ADunits1 + 47.172;  //  13.0C  553  482.39
    zeroWind_volts1 = (zeroWind_ADunits1 * 0.0048828125) - zeroWindAdjustment1;  

    TempCtimes200 = (0.005 *((float)TMP_Therm_ADunits2 * (float)TMP_Therm_ADunits2)) - (16.862 * (float)TMP_Therm_ADunits2) + 9075.4;  
    zeroWind_ADunits2 = -0.0006*((float)TMP_Therm_ADunits2 * (float)TMP_Therm_ADunits2) + 1.0727 * (float)TMP_Therm_ADunits2 + 47.172;  //  13.0C  553  482.39
    zeroWind_volts2 = (zeroWind_ADunits2 * 0.0048828125) - zeroWindAdjustment2;  
 
    TempCtimes300 = (0.005 *((float)TMP_Therm_ADunits3 * (float)TMP_Therm_ADunits3)) - (16.862 * (float)TMP_Therm_ADunits3) + 9075.4;  
    zeroWind_ADunits3 = -0.0006*((float)TMP_Therm_ADunits3 * (float)TMP_Therm_ADunits3) + 1.0727 * (float)TMP_Therm_ADunits3 + 47.172;  //  13.0C  553  482.39
    zeroWind_volts3 = (zeroWind_ADunits3 * 0.0048828125) - zeroWindAdjustment3;  
 

    // This from a regression from data in the form of 
    // Vraw = V0 + b * WindSpeed ^ c
    // V0 is zero wind at a particular temperature
    // The constants b and c were determined by some Excel wrangling with the solver.

   WindSpeed_MPH1 =  pow(((RV_Wind_Volts1 - zeroWind_volts1) /.2300) , 2.7265);   
   WindSpeed_MPH2 =  pow(((RV_Wind_Volts2 - zeroWind_volts2) /.2300) , 2.7265);   
   WindSpeed_MPH3 =  pow(((RV_Wind_Volts3 - zeroWind_volts3) /.2300) , 2.7265);
    }
    
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
 
  //SerialPort.println("Accel: " + String(accelX) + '\t' + String(accelY) + '\t' + String(accelZ) + " g");
  //SerialPort.println("Gyro: " + String(gyroX) + '\t' + String(gyroY) + '\t' + String(gyroZ) + " dps");
  //SerialPort.println("Mag: " + String(magX) + '\t' + String(magY) + '\t' + String(magZ) + " uT");
  //SerialPort.println("Time: " + String(imu.time) + " ms");
 
  
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
   Serial.print((float)WindSpeed_MPH1);
   Serial.print(",");
   Serial.print((float)WindSpeed_MPH2);
   Serial.print(",");
   Serial.println((float)WindSpeed_MPH3);

   
    lastMillis = millis();    
   
 delay(1000);
 }

