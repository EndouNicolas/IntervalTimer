import flet as ft

class StopWatch(ft.UserControl):
    def stopwatch(page: ft.Page):
        time = ft.Text("00:00.0", size=80, weight=ft.FontWeight.W_900, selectable=True)
        is_started = False

        def start_and_stop(e):
            nonlocal is_started
            if is_started:
                start_and_stop_button.text = "スタート"
                is_started = False
            else:
                start_and_stop_button.text = "ストップ"
                is_started = True
            page.update()

        start_and_stop_button = ft.ElevatedButton(text="スタート", width=100, height=50, on_click=start_and_stop)
        reset_button = ft.ElevatedButton(text="リセット", width=100, height=50, on_click=None)

        stopwatch_ui = ft.Column(
            controls=[
                ft.Container(content=time, padding=20, alignment=ft.alignment.center, border_radius=10),
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
