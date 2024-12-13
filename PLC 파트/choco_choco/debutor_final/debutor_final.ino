#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

// PCA9685 초기화
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

int servo_channel = 0; // 서보모터 채널 (PCA9685의 채널 번호)
int current = 160;     // 서보모터의 현재 각도
int motorPin1 = 9;     // L298N IN1 핀
int motorPin2 = 10;     // L298N IN2 핀

// 각도를 PWM 신호로 변환하는 함수
int angleToPulse(int angle) {
  int min_pulse = 122;  // 0도에 해당하는 펄스 길이
  int max_pulse = 615;  // 180도에 해당하는 펄스 길이
  return map(angle, 0, 180, min_pulse, max_pulse);
}

void setup() {
  Serial.begin(9600);        // 시리얼 통신 시작
  pwm.begin();               // PCA9685 시작
  pwm.setPWMFreq(50);        // 서보모터용 주파수 50Hz 설정
  pinMode(motorPin1, OUTPUT); // L298N IN1 핀 출력 모드 설정
  pinMode(motorPin2, OUTPUT); // L298N IN2 핀 출력 모드 설정

  Serial.println("1을 입력하면 0도, 2를 입력하면 180도로 회전합니다.");
  Serial.println("3을 입력하면 모터를 2초간 작동시킵니다.");
}

void loop() {
  if (Serial.available()) {  // 시리얼 입력이 있는 경우
    char input = Serial.read(); // 입력값 읽기
    if (input == '1') { // 1을 입력하면 0도로 회전
      for (int i = current; i <= 160; i += 2) {
        int pulse = angleToPulse(i); // 각도의 PWM 값 계산
        pwm.setPWM(servo_channel, 0, pulse); // 서보모터 제어
        Serial.print("서보모터를 ");
        Serial.print(i);
        Serial.println("도로 회전 중...");
        delay(50); // 부드럽게 이동
      }
      Serial.println("서보모터를 0도로 회전했습니다.");
      current = 80;
    } else if (input == '2') { // 2를 입력하면 180도로 회전
      for (int i = current; i >= 80; i -= 2) {
        int pulse = angleToPulse(i); // 각도의 PWM 값 계산
        pwm.setPWM(servo_channel, 0, pulse); // 서보모터 제어
        Serial.print("서보모터를 ");
        Serial.print(i);
        Serial.println("도로 회전 중...");
        delay(50); // 부드럽게 이동
      }
      for (int i = current; i <= 160; i += 2) {
        int pulse = angleToPulse(i); // 각도의 PWM 값 계산
        pwm.setPWM(servo_channel, 0, pulse); // 서보모터 제어
        Serial.print("서보모터를 ");
        Serial.print(i);
        Serial.println("도로 회전 중...");
        delay(50); // 부드럽게 이동
        // int pulse = angleToPulse(180); // 180도의 PWM 값 계산
        // pwm.setPWM(servo_channel, 0, pulse); // 서보모터 제어
        // Serial.println("서보모터를 180도로 회전했습니다.");
        // current = 180;
      }
      Serial.println("서보모터를 160도로 회전했습니다.");
      current = 160;
    }  else {
      Serial.println("유효하지 않은 입력입니다. 1, 2 또는 3을 입력하세요.");
    }
  }
}
