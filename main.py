import flet as ft
from timer import Timer as tm
from clock import Clock as ck
from stopwatch import StopWatch as st
from setting import Setting as stg

# ダミーのイベントオブジェクトを作成するクラス
class DummyEvent:
    def __init__(self, page):
        self.control = self
        self.page = page

def main(page: ft.Page):
    # 初期設定
    page.title = "インターバルタイマー"
    current_index = 1
    # ウィンドウアイコンの設定
    page.window.icon = "rect1.ico"

    # ウィンドウイベントの処理
    def on_window_event(e: ft.WindowEvent):
        if e.event_type == "close":
            print("Close is clicked")

    # スライダーのUIを構築
    slider_ui, reset_and_start_timer = tm.Sliders()
    clock_object = ck.Time(page)

    # ストップウォッチのUIを構築
    stopwatch_ui = st.stopwatch(page)

    setting_ui = stg.settingUI(page)

    # スペースキーが押されたときに `reset_and_start_timer` を呼び出す
    async def on_keyboard(e: ft.KeyboardEvent):
        if e.key == " ":
            await reset_and_start_timer(DummyEvent(page))

    # キーボードイベントを登録
    page.on_keyboard_event = on_keyboard

    # タブを構築
    k = ft.Tabs(
        selected_index=1,
        animation_duration=300,
        on_change=lambda e: update_tab_index(e),
        tabs=[
            ft.Tab(
                text="時計",
                content=ft.Container(
                    content=clock_object, alignment=ft.alignment.center,
                ),
            ),
            ft.Tab(
                text="タイマー",
                content=ft.Container(content=slider_ui, alignment=ft.alignment.center),
            ),
            ft.Tab(
                text="ストップウォッチ",
                content=ft.Container(content=stopwatch_ui, alignment=ft.alignment.center),
            ),
        ],
        expand=1,
    )

    # タブの更新
    def update_tab_index(e):
        nonlocal current_index
        current_index = e.control.selected_index

    def detect_key_event(e):
        nonlocal current_index
        if current_index == 1:
            page.add(ft.Text(f"Current tab index: {current_index}"))
            page.update()

    def setting_popup(e):
        setting_popup =ft.BottomSheet(content=setting_ui, open=True)
        page.open(setting_popup)
        page.update()

    # UI要素を追加
    page.add(k)

    # 設定ボタン
    setting = ft.IconButton(icon=ft.Icons.SETTINGS, icon_size=20,on_click=setting_popup, tooltip="設定",)
    page.add(setting)



# アプリケーションを開始
ft.app(target=main)
