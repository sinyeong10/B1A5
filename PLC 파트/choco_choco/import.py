import sys
sys.path.append(r"C:\Users\gwonh\Desktop\final_plc")
from modbus_frame import create_modbus_frame, setup_serial

import time

class PLCControl:
    def __init__(self):
        # 시리얼 포트를 설정합니다.
        self.ser_plc = setup_serial(port='COM7', baudrate=9600)
        self.x_position = 0

    def plc_motor_ctrl(self, vec):
        """
        PLC 모터 제어 함수
        :param vec: 명령어 (예: "05" - 정회전, "10" - 역회전, "03" - 정지)
        """
        # PLC로 모터 제어 명령 전송
        frame = create_modbus_frame([0x3A, '01', vec, "00010008", 0x0D, 0x0A], 'lrc')
        self.ser_plc.write(frame)
        time.sleep(1)
        self.ser_plc.write(frame)

        print(f"모터 제어 명령 '{vec}' 전송 완료.")

        # 캡처 및 정렬 과정 (vec 값에 따라 동작 수행)
        self.capture_center(vec)


    def capture_center(self, vec):
        """
        모터 정렬 작업 (예제 코드, 필요 시 구현)
        :param vec: 모터 방향
        """
        print(f"모터 방향 '{vec}'에 따라 캡처 작업 수행 중...")
        time.sleep(1)  # 임의의 대기 시간 (실제 센서나 카메라 작업 수행 시 구현)
        print("캡처 작업 완료.")

if __name__ == "__main__":
    # PLCControl 객체 생성
    plc = PLCControl()

    plc.plc_motor_ctrl("11")  # "05"는 정회전을 의미

