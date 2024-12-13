import serial
import time

# 1. 시리얼 포트 설정
ser = serial.Serial(
    port='COM6',  # 사용 중인 시리얼 포트
    baudrate=9600,        # PLC와 동일한 보레이트
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=2   # 타임아웃
)

# 2. 송신 프레임 정의 (Modbus RTU 프레임 예제)
tx_frame = b'\x01\x06\x00\x01\x12\x34\xE1\xC7'

# 특정 값을 수신했을 때 송신할 펄스 신호
response_trigger_value = b':0101000'
pulse_signal = b'\x01'  # 펄스 신호
pulse_duration = 0.1    # 펄스 지속 시간 (초)

# 과일 크기를 저장할 변수 초기화
fruit_size = ""

# 3. 데이터 송신
ser.write(tx_frame)
print("송신 완료:", tx_frame)

# 데이터 수신 및 처리 루프
try:
    while True:
        print("데이터 수신 대기 중...")
        response = ser.read(5)  # PLC에서 예상되는 데이터 길이 (5바이트)

        if response:
            print("수신된 데이터:", response)

            # 특정 값 수신 시 처리
            if response == response_trigger_value:
                print("특정 값을 수신했습니다:", response)
                
                # 펄스 신호 송신
                ser.write(pulse_signal)
                print("펄스 신호 송신 완료:", pulse_signal)
                
                # 펄스 지속 시간 유지
                time.sleep(pulse_duration)
                
                # 펄스 신호 종료
                ser.write(b'\x00')
                print("펄스 신호 종료")

            # b':1\r\n' 수신 시 fruit_size에 'big' 저장
            elif response == b':1\r\n':
                fruit_size = 'big'
                print("과일 크기 업데이트: big")

            # b':2\r\n' 수신 시 fruit_size에 'small' 저장
            elif response == b':2\r\n':
                fruit_size = 'small'
                print("과일 크기 업데이트: small")
except KeyboardInterrupt:
    print("사용자가 프로그램을 중단했습니다.")
except Exception as e:
    print("수신 오류:", e)
finally:
    ser.close()
    print("시리얼 포트를 닫았습니다.")
