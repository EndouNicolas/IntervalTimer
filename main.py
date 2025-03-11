import time
import keyboard
import flet as ft
from timer import Timer as tm


def main(page: ft.Page):
    # 初期設定
    page.title = "インターバルタイマー"
    current_index = 1

    # ウィンドウイベントの処理
    def on_window_event(e: ft.WindowEvent):
        if e.event_type == "close":
            print("Close is clicked")


    #スライダーのUIを構築
    #slider_ui, get_values,reset_and_start_timer = tm.Timer.Sliders()
    slider_ui,reset_and_start_timer = tm.Sliders()
#タブを構築
    """
    1ページ目は時計､2ページ目はインターバルタイマー､3ページ目はストップウォッチ
    """
    k = ft.Tabs(
        selected_index=1,
        animation_duration=300,
        on_change=lambda e: update_tab_index(e),
        tabs=[
            ft.Tab(
                text="時計",
                content=ft.Container(
                    content=ft.Text("This is Tab 1"), alignment=ft.alignment.center
                ),
            ),
            ft.Tab(
                text="タイマー",
                content=ft.Container(content=slider_ui,alignment=ft.alignment.center),
            ),
            ft.Tab(
                text="ストップウォッチ",
                content=ft.Text("This is Tab 3"),
            ),
        ],
        expand=1,
    )

    def update_tab_index(e):
        nonlocal current_index
        current_index = e.control.selected_index
        detect_key_event(e)
        """
        page.add(ft.Text(f"Current tab index: {current_index}"))
        page.update()
        """

    def detect_key_event(e):
        nonlocal current_index
        if current_index == 1:
            page.add(ft.Text(f"Current tab index: {current_index}"))
            page.update()


    set_theme_button=ft.ElevatedButton(text="テーマ変更")
    #layout = ft.Row(controls=[k,set_theme_button],alignment=ft.MainAxisAlignment.SPACE_BETWEEN,vertical_alignment=ft.CrossAxisAlignment.CENTER,)
    #page.add(layout)
    page.add(k)


    # テキストインプットを取得する
    def on_keyboard(e: ft.KeyboardEvent):
        a = e.key
        if a == " ":
            """
            page.add(ft.Text("Space key"))
            page.update()
            """
            return "Space key"
        else:
            """
            page.add(ft.Text(a))
            page.update()
            """
            return a

    page.on_keyboard_event = lambda e: page.add(ft.Text(on_keyboard(e)))
    page.on_event = on_window_event

    """
    def get_curretn_value(e):
        m, s = get_values()
        page.add(ft.Text(f"Current slider values: {m}M {s}S"))
        
    page.add(ft.ElevatedButton("設定", on_click=get_curretn_value))
    """

    # 必要ならここでUI要素を追加

# アプリケーションを開始
ft.app(target=main)

"""

def interval_timer(duration: int):
    
    #インターバルタイマーを指定秒数で開始。
    #スペースキーを押すとリセットして再スタート。
    
    while True:
        print(f"タイマー開始: {duration}秒")
        start_time = time.time()
        elapsed_time = 0

        while elapsed_time < duration:
            # タイマーの進行状況を表示
            remaining_time = duration - elapsed_time
            print(f"残り時間: {remaining_time:.1f}秒", end="\r")

            # スペースキーが押されたらリセットして再スタート
            if keyboard.is_pressed("space"):
                print("\nタイマーを再スタートします。")
                break

            time.sleep(0.01)  # 進行状況を更新する間隔
            elapsed_time = time.time() - start_time
        else:
            print("\nタイマー終了！")
            while not keyboard.is_pressed("q"):
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
"""