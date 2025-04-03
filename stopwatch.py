import flet as ft
import asyncio
import time

class StopWatch(ft.UserControl):
    def stopwatch(page: ft.Page):
        time_text = ft.Text("00:00.0", size=80, weight=ft.FontWeight.W_900, selectable=True)
        is_started = False
        start_time = None  
        elapsed_time = 0.0  
        task = None  

        async def run_stopwatch():
            nonlocal elapsed_time, start_time
            start_time = time.perf_counter() - elapsed_time  # 再開時に時間を維持
            while is_started:
                now = time.perf_counter()
                elapsed_time = now - start_time
                minutes = int(elapsed_time // 60)
                seconds = int(elapsed_time % 60)
                milliseconds = int((elapsed_time - int(elapsed_time)) * 10)
                time_text.value = f"{minutes:02}:{seconds:02}.{milliseconds}"
                page.update()
                await asyncio.sleep(0.05)  

        async def start_and_stop(e):
            nonlocal is_started, task
            if is_started:
                start_and_stop_button.text = "スタート"
                is_started = False
            else:
                start_and_stop_button.text = "ストップ"
                is_started = True
                task = asyncio.create_task(run_stopwatch())
            page.update()

        def reset(e):
            nonlocal elapsed_time, is_started, task
            is_started = False
            if task:
                task.cancel()
            elapsed_time = 0.0
            time_text.value = "00:00.0"
            start_and_stop_button.text = "スタート"
            page.update()

        start_and_stop_button = ft.ElevatedButton(text="スタート", width=100, height=50, on_click=start_and_stop)
        reset_button = ft.ElevatedButton(text="リセット", width=100, height=50, on_click=reset)

        stopwatch_ui = ft.Column(
            controls=[
                ft.Container(content=time_text, padding=20, alignment=ft.alignment.center, border_radius=10),
                ft.Row(
                    controls=[
                        ft.Container(content=start_and_stop_button),
                        ft.Container(content=reset_button)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )

        return stopwatch_ui