import flet as ft
import signal
import asyncio
import time
import playsound3 as playsound


class Timer(ft.Control):
    signal.signal(signal.SIGINT, signal.SIG_IGN)

    @staticmethod
    def Sliders():
        def update_text_value():
            text_input_m.value = str(int(slider_value_m.value))
            text_input_s.value = str(int(slider_value_s.value))
            text_input_m.update()
            text_input_s.update()

        def update_slider_value():
            try:
                slider_value_m.value = int(text_input_m.value)
                slider_value_s.value = int(text_input_s.value)
                slider_value_m.update()
                slider_value_s.update()
            except ValueError:
                pass

        async def reset_and_start_timer(e):
            await reset_timer(e)
            await start_timer(e)

        slider_value_m = ft.Slider(min=0, max=59, divisions=59, label="{value}M",
                                on_change=lambda e: update_text_value())
        text_input_m = ft.TextField(value="0", width=100, label="分を入力",
                                    on_change=lambda e: update_slider_value())

        slider_value_s = ft.Slider(min=0, max=59, divisions=59, label="{value}S",
                                on_change=lambda e: update_text_value())
        text_input_s = ft.TextField(value="0", width=100, label="秒を入力",
                                    on_change=lambda e: update_slider_value())

        status_text = ft.Text("設定時間: 0分 0秒")
        time_display = ft.Text("残り時間: 0分 0秒00", size=50, weight=ft.FontWeight.BOLD)

        is_started = False
        is_stopped = False
        remaining_time = 0.0
        started_time = 0.0
        initial_duration = 0.0
        start_time_perf = 0.0

        async def count_down(page: ft.Page):
            nonlocal is_started, is_stopped, remaining_time, start_time_perf, initial_duration
            start_time_perf = time.perf_counter()
            while is_started and remaining_time > 0:
                if is_stopped:
                    await asyncio.sleep(0.01)
                    start_time_perf += 0.01
                    continue
                elapsed = time.perf_counter() - start_time_perf
                remaining_time = max(0.0, initial_duration - elapsed)
                minutes = int(remaining_time // 60)
                seconds = int(remaining_time % 60)
                milliseconds = int((remaining_time % 1) * 100)
                time_display.value = f"残り時間: {minutes}分 {seconds}秒{milliseconds:02d}"
                page.update()
                await asyncio.sleep(0.01)
            is_started = False
            if remaining_time <= 0:
                time_display.value = "終了"
                page.update()

        async def start_timer(e):
            nonlocal is_started, is_stopped, remaining_time, started_time, initial_duration
            if is_started:
                return
            is_started = True
            is_stopped = False
            m, s = int(slider_value_m.value), int(slider_value_s.value)
            started_time = float(m * 60 + s)
            remaining_time = started_time
            initial_duration = started_time
            status_text.value = f"タイマー開始: {m}分 {s}秒"
            page = e.control.page
            page.update()
            await count_down(page)

        async def stop_timer(e):
            nonlocal is_started, is_stopped, initial_duration, start_time_perf
            if not is_started:
                await start_timer(e)
            else:
                is_stopped = not is_stopped
                if not is_stopped:
                    # 再開時に現在の状態から再計算
                    initial_duration = remaining_time
                    start_time_perf = time.perf_counter()
                e.control.page.update()

        async def reset_timer(e):
            nonlocal is_started, is_stopped, remaining_time, started_time, initial_duration
            is_started = False
            is_stopped = True
            await asyncio.sleep(0.1)
            remaining_time = started_time
            initial_duration = started_time
            minutes = int(remaining_time // 60)
            seconds = int(remaining_time % 60)
            milliseconds = int((remaining_time % 1) * 100)
            time_display.value = f"{minutes}分 {seconds}秒{milliseconds:02d}"
            e.control.page.update()

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

                ft.Container(content=status_text, padding=10, alignment=ft.alignment.center),
                ft.Container(content=time_display, padding=10, alignment=ft.alignment.center, border_radius=10),

                ft.Row(
                    controls=[
                        ft.ElevatedButton("開始", on_click=start_timer, width=100),
                        ft.ElevatedButton("停止/再開", on_click=stop_timer, width=100),
                        ft.ElevatedButton("リセット", on_click=reset_timer, width=100),
                        ft.ElevatedButton("リセットして開始", on_click=reset_and_start_timer, width=140),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20
                )
            ],
            spacing=20,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

        return slider_ui, reset_and_start_timer
