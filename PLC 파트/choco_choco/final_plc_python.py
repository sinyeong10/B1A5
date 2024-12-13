import serial
import time

# 1. 시리얼 포트 설정 (PLC와 아두이노 연결)
plc_ser = serial.Serial(
    port='COM6',  # PLC와 연결된 포트
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=2
)

arduino_ser = serial.Serial(
    port='COM7',  # 아두이노와 연결된 포트
    baudrate=9600,
    timeout=1
)

time.sleep(2)  # 아두이노 초기화 대기

print("PLC 및 아두이노와 연결되었습니다.")

# 2. 송신 프레임 정의 (Modbus RTU 프레임 예제)
tx_frame = b'\x01\x06\x00\x01\x12\x34\xE1\xC7'

# 특정 값을 수신했을 때 송신할 펄스 신호
response_trigger_value = b':0101000'
pulse_signal = b'\x01'  # 펄스 신호
pulse_duration = 0.1    # 펄스 지속 시간 (초)

# 과일 크기를 저장할 변수 초기화
fruit_size = ""

# 3. 데이터 송신
plc_ser.write(tx_frame)
print("송신 완료:", tx_frame)

# 데이터 수신 및 처리 루프
try:
    # 데이터 수신 및 처리 루프
    while True:
        print("데이터 수신 대기 중...")
        response = plc_ser.read(5)  # PLC에서 예상되는 데이터 길이 (5바이트)

        if response:
            print("수신된 데이터:", response)

            # 특정 값 수신 시 처리
            if response == response_trigger_value:
                print("특정 값을 수신했습니다:", response)
                
                # 펄스 신호 송신
                plc_ser.write(pulse_signal)
                print("펄스 신호 송신 완료:", pulse_signal)
                
                # 펄스 지속 시간 유지
                time.sleep(pulse_duration)
                
                # 펄스 신호 종료
                plc_ser.write(b'\x00')
                print("펄스 신호 종료")

            # b':1\r\n' 수신 시 fruit_size에 'big' 저장
            elif response == b':1\r\n':
                fruit_size = 'big'
                print("과일 크기 업데이트: big")

            # b':2\r\n' 수신 시 fruit_size에 'small' 저장
            elif response == b':2\r\n':
                fruit_size = 'small'
                print("과일 크기 업데이트: small")

              

        # 사용자 입력 처리 (2,3번 기능 포함)


        # 디버터 작동 코드.
        user_command = input("아두이노로 보낼 명령 (3 또는 'exit' 입력): ").strip()
        if user_command == '2':
            arduino_ser.write(user_command.encode())  # 명령어 전송
            print(f"'{user_command}' 명령어를 아두이노로 보냈습니다.")
            
            # 아두이노 응답 읽기
            while arduino_ser.in_waiting > 0:
                arduino_response = arduino_ser.readline().decode().strip()
                print(f"아두이노 응답: {arduino_response}")
                
       
        
        elif user_command.lower() == 'exit':  # 종료 명령
            print("프로그램을 종료합니다.")
            break
except KeyboardInterrupt:
    print("사용자가 프로그램을 중단했습니다.")
except Exception as e:
    print("오류 발생:", e)
finally:
    plc_ser.close()
    arduino_ser.close()
    print("PLC 및 아두이노 시리얼 포트를 닫았습니다.")
