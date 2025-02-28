import flet as ft
import signal
import asyncio

class Timer(ft.UserControl):
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    
    @staticmethod
    def Sliders():
        slider_value_m = ft.Slider(
            min=0, max=59, divisions=59, label="{value}M", on_change=lambda e: update_status(e)
        )
        text_input_m = ft.TextField(value=0, width=300, label="分を入力", on_change=lambda e: update_slider_value(e))
        slider_value_s = ft.Slider(
            min=0, max=59, divisions=59, label="{value}S", on_change=lambda e: update_status(e)
        )
        text_input_s = ft.TextField(value=0, width=300, label="秒を入力", on_change=lambda e: update_slider_value(e))
        status_text = ft.Text("設定時間: 0分 0秒")
        time_display = ft.Text("残り時間: 0分 0秒00", size=20, weight=ft.FontWeight.BOLD)
        
        is_started = False
        is_stopped = False
        remaining_time = 0
        started_time = 0
        
        async def count_down(page: ft.Page):
            nonlocal is_started, is_stopped, remaining_time
            while is_started and remaining_time > 0:
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
                remaining_time = started_time
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
                e.control.page.update()

        async def reset_timer(e):
            nonlocal is_started, is_stopped, remaining_time, started_time
            is_started = False
            is_stopped = True
            await asyncio.sleep(0.1)
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
                ft.Text("タイマー設定", size=24, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                ft.Row([
                    ft.Column([
                        ft.Text("分", size=16),
                        slider_value_m,
                        text_input_m
                    ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    ft.Column([
                        ft.Text("秒", size=16),
                        slider_value_s,
                        text_input_s
                    ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
                
                ft.Container(
                    content=status_text,
                    padding=10,
                    alignment=ft.alignment.center,
                ),
                
                ft.Container(
                    content=time_display,
                    padding=10,
                    alignment=ft.alignment.center,
                    bgcolor=ft.colors.BLACK,
                    border_radius=10
                ),
                
                ft.Row(
                    controls=[
                        ft.ElevatedButton("開始", on_click=start_timer, width=100),
                        ft.ElevatedButton("停止/再開", on_click=stop_timer, width=100),
                        ft.ElevatedButton("リセット", on_click=reset_timer, width=100),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20
                )
            ],
            spacing=20,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

        def get_slider_values():
            return slider_value_m.value, slider_value_s.value
        
        return slider_ui, get_slider_values
