import flet as ft
import time

class Timer(ft.UserControl):
#スライダーを作成
    def Sliders():
        slider_value_m = ft.Ref[ft.Slider]()  # 分のスライダー値を保持
        slider_value_s = ft.Ref[ft.Slider]()  # 秒のスライダー値を保持
        t = ft.Text()
        k = ft.Text()
        
        def start_timer(e):
            m, s = get_slider_values()
            start_time =time.time()
            elapsed_time = 0
            target_time = m * 60 + s
            while elapsed_time < target_time:
                remaining_time = target_time - elapsed_time
            k.value=f"s:{target_time}"
            k.update()
        

        def slider_changed(e):
            t.value = f"Slider changed to {slider_value_m.current.value}M {slider_value_s.current.value}S"
            t.update()

        slider_ui = ft.Column(
            controls=[
                ft.Slider(ref=slider_value_m, min=0, max=59, divisions=59, label="{value}M", on_change=slider_changed),
                ft.Slider(ref=slider_value_s, min=1, max=12, divisions=11, label="{value}S", on_change=slider_changed),
                t,
                ft.ElevatedButton("開始", on_click=start_timer),
                k,
            ]
        )
    
        def get_slider_values():
            return slider_value_m.current.value, slider_value_s.current.value

        return slider_ui, get_slider_values