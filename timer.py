import flet as ft
import signal
import asyncio

class Timer(ft.UserControl):
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    @staticmethod
    def Sliders():
        slider_value_m = ft.Slider(min=0, max=59, divisions=59, label="{value}M")
        slider_value_s = ft.Slider(min=0, max=59, divisions=59, label="{value}S")
        is_started = False
        is_stopped = False
        time_display = ft.Text()
        status_text = ft.Text()
        remaining_time = 0
        started_time = 0

        async def count_down(page: ft.Page):
            nonlocal is_started, is_stopped, remaining_time
            while remaining_time > 0:
                if is_stopped:
                    await asyncio.sleep(0.01)
                    continue 
                time_display.value = f"残り時間: {remaining_time:.2f}秒"
                page.update()
                await asyncio.sleep(0.01)
                remaining_time -= 0.01
            is_started = False
            time_display.value = "終了"
            page.update()

        async def start_timer(e):
            nonlocal is_started, is_stopped, remaining_time, started_time
            if is_started:
                return
            is_started = True
            is_stopped = False
            if remaining_time <= 0:
                m, s = slider_value_m.value, slider_value_s.value
                started_time = remaining_time = float(m * 60 + s)
            
            else:
                m, s = slider_value_m.value, slider_value_s.value
                if started_time != float(m * 60 + s):
                    started_time=remaining_time = float(m * 60 + s)
                else:
                    remaining_time = started_time  # リセット後も正しい時間で開始
            status_text.value = f"タイマー開始: {remaining_time:.2f}秒"
            page = e.control.page 
            page.update()
            await count_down(page)

        async def stop_timer(e):
            nonlocal is_started, is_stopped
            if not is_started:
                await start_timer(e)
            else:
                is_stopped = not is_stopped
                if is_stopped:
                    time_display.value = f"停止: {remaining_time:.2f}秒"
                else:
                    time_display.value = "再開"
                e.control.page.update()
        
        def reset_timer(e):
            nonlocal is_started, is_stopped, remaining_time, started_time
            is_stopped = True
            is_started = False
            #スタート時の時間を復元
            remaining_time = started_time 
            time_display.value = f"{remaining_time:.2f}秒"
            e.control.page.update()

        def slider_changed(e):
            status_text.value = f"設定時間: {slider_value_m.value}分 {slider_value_s.value}秒"
            e.control.page.update()

        slider_ui = ft.Column(
            controls=[
                slider_value_m,
                slider_value_s,
                ft.ElevatedButton("開始", on_click=start_timer),
                ft.ElevatedButton("停止/再開", on_click=stop_timer),
                ft.ElevatedButton("リセット", on_click=reset_timer),
                status_text,
                time_display,
            ]
        )

        def get_slider_values():
            return slider_value_m.value, slider_value_s.value

        return slider_ui, get_slider_values
