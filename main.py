import time
import keyboard

def interval_timer(duration: int):
    """
    インターバルタイマーを指定秒数で開始。
    スペースキーを押すとリセットして再スタート。
    """
    while True:
        print(f"タイマー開始: {duration}秒")
        start_time = time.time()
        elapsed_time = 0

        while elapsed_time < duration:
            # タイマーの進行状況を表示
            remaining_time = duration - elapsed_time
            print(f"残り時間: {remaining_time:.1f}秒", end="\r")

            # スペースキーが押されたらリセットして再スタート
            if keyboard.is_pressed('space'):
                print("\nタイマーを再スタートします。")
                break
            
            time.sleep(0.01)  # 進行状況を更新する間隔
            elapsed_time = time.time() - start_time
        else:
            print("\nタイマー終了！")
            while not keyboard.is_pressed('q'):
                time.sleep(0.01)

if __name__ == "__main__":
    try:
        # ユーザーに秒数を入力させる
        duration = int(input("インターバルタイマーの時間を秒単位で入力してください: "))
        print("スペースキーを押すとタイマーをリセットします。\n")
        interval_timer(duration)
    except KeyboardInterrupt:
        print("\nプログラムを終了します。")
    except ValueError:
        print("\n無効な入力です。整数を入力してください。")