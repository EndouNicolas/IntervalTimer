import time
import keyboard
import flet as ft

#スライダーを作成
def Sliders():
    slider_value_m = ft.Ref[ft.Slider]()  # 分のスライダー値を保持
    slider_value_s = ft.Ref[ft.Slider]()  # 秒のスライダー値を保持
    t = ft.Text()

    def slider_changed(e):
        t.value = f"Slider changed to {slider_value_m.current.value}M {slider_value_s.current.value}S"
        t.update()

    slider_ui = ft.Column(
        controls=[
            ft.Slider(ref=slider_value_m, min=0, max=59, divisions=59, label="{value}M", on_change=slider_changed),
            ft.Slider(ref=slider_value_s, min=1, max=12, divisions=11, label="{value}S", on_change=slider_changed),
            t,
        ]
    )
    
    def get_slider_values():
        return slider_value_m.current.value, slider_value_s.current.value

    return slider_ui, get_slider_values

def main(page: ft.Page):
    # 初期設定
    page.title = "インターバルタイマー"

    # ウィンドウイベントの処理
    def on_window_event(e: ft.WindowEvent):
        if e.event_type == "close":
            print("Close is clicked")

#タブを構築
    k = ft.Tabs(
        selected_index=1,
        animation_duration=300,
        tabs=[
            ft.Tab(
                text="Tab 1",
                content=ft.Container(
                    content=ft.Text("This is Tab 1"), alignment=ft.alignment.center
                ),
            ),
            ft.Tab(
                tab_content=ft.Icon(ft.Icons.SEARCH),
                content=ft.Text("This is Tab 2"),
            ),
            ft.Tab(
                text="Tab 3",
                icon=ft.Icons.SETTINGS,
                content=ft.Text("This is Tab 3"),
            ),
        ],
        expand=1,
    )

    page.add(k)


    # テキストインプットを取得する
    def on_keyboard(e: ft.KeyboardEvent):
        a = e.key
        if a == " ":
            page.add(ft.Text("Space key"))
        else:
            page.add(ft.Text(a))

    page.on_keyboard_event = on_keyboard
    page.on_event = on_window_event

    #スライダーのUIを構築
    slider_ui, get_values = Sliders()

    def get_curretn_value(e):
        m, s = get_values()
        page.add(ft.Text(f"Current slider values: {m}M {s}S"))
        
    page.add(ft.ElevatedButton("設定", on_click=get_curretn_value))


    page.add(slider_ui)
    # 必要ならここでUI要素を追加
    k = ft.Text("")

    page.add(k)
    page.add(ft.Text())
    page.update()


# アプリケーションを開始
ft.app(target=main)


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
