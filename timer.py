import flet as ft
import signal
import asyncio

class Timer(ft.UserControl):
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    
    @staticmethod
    def Sliders():
        #ここでスライダーの変数を作成(UI付き)
        slider_value_m = ft.Slider(
            min=0, max=59, divisions=59, label="{value}M", on_change=lambda e: update_status(e)
        )
        text_input_m = ft.TextField(value=0,width=300,label="分を入力", on_change=lambda e :update_slider_value(e))
        slider_value_s = ft.Slider(
            min=0, max=59, divisions=59, label="{value}S", on_change=lambda e: update_status(e)
        )
        text_input_s = ft.TextField(value=0,width=300,label="秒を入力", on_change=lambda e:update_slider_value(e))
        status_text = ft.Text("設定時間: 0分 0秒")
        time_display = ft.Text("残り時間: 0分 0秒00", size=20, weight=ft.FontWeight.BOLD)
        
        is_started = False
        is_stopped = False
        remaining_time = 0
        started_time = 0
        
        async def count_down(page: ft.Page):
            nonlocal is_started, is_stopped, remaining_time
            while remaining_time > 0:
                if is_stopped:
                    await asyncio.sleep(0.01)
                    continue 
                minutes = int(remaining_time // 60)
                seconds = int(remaining_time % 60)
                milliseconds = int((remaining_time % 1) * 100)
                time_display.value = f"残り時間: {minutes}分 {seconds}秒{milliseconds:02d}"
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
                    started_time = remaining_time = float(m * 60 + s)
                else:
                    remaining_time = started_time  # リセット後も正しい時間で開始
            status_text.value = f"タイマー開始: {int(remaining_time // 60)}分 {int(remaining_time % 60)}秒"
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
                    minutes = int(remaining_time // 60)
                    seconds = int(remaining_time % 60)
                    milliseconds = int((remaining_time % 1) * 100)
                    time_display.value = f"停止: {minutes}分 {seconds}秒{milliseconds:02d}"
                else:
                    time_display.value = "再開"
                e.control.page.update()
        
        def reset_timer(e):
            nonlocal is_started, is_stopped, remaining_time, started_time
            is_stopped = True
            is_started = False
            remaining_time = started_time 
            minutes = int(remaining_time // 60)
            seconds = int(remaining_time % 60)
            milliseconds = int((remaining_time % 1) * 100)
            time_display.value = f"{minutes}分 {seconds}秒{milliseconds:02d}"
            e.control.page.update()

        def update_status(e):
            status_text.value = f"設定時間: {slider_value_m.value}分 {slider_value_s.value}秒"
            update_text_value(e)
            e.control.page.update()
            
        #テキストの値をスライダーの値に合わせる
        def update_text_value(e):
            text_input_m.value = slider_value_m.value
            text_input_s.value = slider_value_s.value
            text_input_s.update()
            text_input_m.update()
            
        def update_slider_value(e):
            slider_value_m.value = text_input_m.value
            slider_value_s.value = text_input_s.value
            slider_value_m.update()
            slider_value_s.update()
            
        def test(e):
            nonlocal slider_value_m
            slider_value_m.value = 15
            slider_value_m.update()

        button_row = ft.Row(
            controls=[
                ft.ElevatedButton("開始", on_click=start_timer),
                ft.ElevatedButton("停止/再開", on_click=stop_timer),
                ft.ElevatedButton("リセット", on_click=reset_timer),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )

        slider_ui = ft.Column(
            controls=[
                slider_value_m,
                text_input_m,
                slider_value_s,
                text_input_s,
                status_text,
                time_display,
                button_row,
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.CENTER,
        )

        def get_slider_values():
            return slider_value_m.value, slider_value_s.value
        
        return slider_ui, get_slider_values
