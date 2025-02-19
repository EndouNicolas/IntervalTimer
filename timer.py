import flet as ft
import asyncio

class Timer(ft.UserControl):
    @staticmethod
    def Sliders():
        # スライダー値を保持する変数
        slider_value_m = ft.Slider(min=0, max=59, divisions=59, label="{value}M")
        slider_value_s = ft.Slider(min=1, max=12, divisions=11, label="{value}S")
        time_display = ft.Text()
        status_text = ft.Text()

        async def count_down(page: ft.Page, total_seconds: int):
            while total_seconds > 0:
                time_display.value = f"残り時間: {total_seconds:.2f}秒"
                page.update()
                await asyncio.sleep(0.01)
                total_seconds -= 0.01

            time_display.value = "終了"
            page.update()

        async def start_timer(e):
            m, s = slider_value_m.value, slider_value_s.value
            total_seconds = int(m * 60 + s)
            status_text.value = f"タイマー開始: {total_seconds}秒"
            page = e.control.page  # `page` を取得
            page.update()
            await count_down(page, total_seconds)

        def slider_changed(e):
            status_text.value = f"設定時間: {slider_value_m.value}分 {slider_value_s.value}秒"
            e.control.page.update()

        slider_ui = ft.Column(
            controls=[
                slider_value_m,
                slider_value_s,
                ft.ElevatedButton("開始", on_click=start_timer),
                status_text,
                time_display,
            ]
        )

        def get_slider_values():
            return slider_value_m.value, slider_value_s.value

        return slider_ui, get_slider_values
