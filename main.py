import time
import keyboard
import flet as ft
from timer import Timer as tm

# ダミーのイベントオブジェクトを作成するクラス
class DummyEvent:
    def __init__(self, page):
        self.control = self
        self.page = page

def main(page: ft.Page):
    # 初期設定
    page.title = "インターバルタイマー"
    current_index = 1

    # ウィンドウイベントの処理
    def on_window_event(e: ft.WindowEvent):
        if e.event_type == "close":
            print("Close is clicked")

    # スライダーのUIを構築
    slider_ui, reset_and_start_timer = tm.Sliders()

    # スペースキーが押されたときに `reset_and_start_timer` を呼び出す
    async def on_keyboard(e: ft.KeyboardEvent):
        if e.key == " ":
            await reset_and_start_timer(DummyEvent(page))  # ← await を追加

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
                    content=ft.Text("This is Tab 1"), alignment=ft.alignment.center
                ),
            ),
            ft.Tab(
                text="タイマー",
                content=ft.Container(content=slider_ui, alignment=ft.alignment.center),
            ),
            ft.Tab(
                text="ストップウォッチ",
                content=ft.Text("This is Tab 3"),
            ),
        ],
        expand=1,
    )

    # タブの更新
    def update_tab_index(e):
        nonlocal current_index
        current_index = e.control.selected_index
        detect_key_event(e)

    def detect_key_event(e):
        nonlocal current_index
        if current_index == 1:
            page.add(ft.Text(f"Current tab index: {current_index}"))
            page.update()

    # UI要素を追加
    page.add(k)

    # テーマ変更ボタン
    set_theme_button = ft.ElevatedButton(text="テーマ変更")
    page.add(set_theme_button)

# アプリケーションを開始
ft.app(target=main)
