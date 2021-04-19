///////////////////////////////////////
///////// Date: 2018. 06. 10  /////////
////////  Name: Kim ChaeYoon  /////////
/////////////////////////////////////// 

#include <Stepper.h>

#define but_1st 5
#define but_2nd 6
#define but_3rd 7

int stepsdeg = 2048;
// 서보 모터 회전 각도 설정

int i = 1; // 층 입력 변수

Stepper myStepper(stepsdeg, 11, 9, 10, 8);

void setup() {
  myStepper.setSpeed(10); //서보모터 속도
  pinMode(but_1st, INPUT);
  pinMode(but_2nd, INPUT);
  pinMode(but_3rd, INPUT);
  Serial.begin(9600);
}

void loop() {
 if (digitalRead(but_1st) == HIGH) { //1층 버튼 입력
    if (i == 1) { //현재 위치가 1층일 때
      delay(500); //가만히
    }
    
    if (i == 2) { // 현재 위치가 2층일 때
      myStepper.step(-stepsdeg); // CCW 회전
      delay(500);
    }
    
    if (i == 3) {  // 3층일 때,
      myStepper.step(-stepsdeg);
      myStepper.step(-stepsdeg);
      delay(500);
    }
    i=1;                     // 현재 위치 저장
 }
 
 if (digitalRead(but_2nd) == HIGH) { // 2층 버튼 입력
  if (i == 1) {                      // 현재 위치 1층일 때
    myStepper.step(stepsdeg);       // CW 회전
    delay(500);
  }
  
  if (i == 2) {                    // 2층일 때
    delay(500);                    // 가만히
  }
  
  if (i == 3) {
    myStepper.step(-stepsdeg);
    delay(500);
  }
  i = 2;  // 2층
 }
 
  if (digitalRead(but_3rd) == HIGH) {
  if (i == 1) {
    myStepper.step(stepsdeg);
    myStepper.step(stepsdeg);
    delay(500);
  }
  
  if (i == 2) {
    myStepper.step(stepsdeg);
    delay(500);
  }
  if(i == 3) {
    delay(500);
  }
  i = 3;
 }
}

