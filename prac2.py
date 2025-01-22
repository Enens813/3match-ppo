import subprocess

# def get_current_activity():
#     # 현재 활성화된 액티비티를 얻기 위해 dumpsys activity 명령어 사용
#     command = ['adb', 'shell', 'dumpsys', 'activity', 'activities']
#     result = subprocess.run(command, capture_output=True, text=True)
#     output = result.stdout

#     # 활성화된 액티비티 정보 추출
#     for line in output.splitlines():
#         if "mResumedActivity" in line:
#             print(f"Current activity: {line}")

# if __name__ == "__main__":
#     get_current_activity()

import subprocess

def monitor_logcat():
    # Logcat을 실행하여 실시간 로그를 모니터링합니다
    command = ['adb', 'logcat']
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    while True:
        log = process.stdout.readline()
        if log:
            log_str = log.decode('utf-8').strip()
            print(log_str)
            if "Activity" in log_str and "paused" in log_str:
                print("Screen transitioned to paused state.")
            if "Activity" in log_str and "started" in log_str:
                print("Screen transitioned to started state.")
        else:
            break

if __name__ == "__main__":
    monitor_logcat()
