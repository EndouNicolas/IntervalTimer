import flet as ft

class Timer(ft.UserControl):
#スライダーを作成
    def Sliders():
        slider_value_m = ft.Ref[ft.Slider]()  # 分のスライダー値を保持
        slider_value_s = ft.Ref[ft.Slider]()  # 秒のスライダー値を保持
        t = ft.Text()
        k = ft.Text()
        
        def get_curretn_value(e):
            m, s = get_slider_values()
            k.value=f"Current slider values: {m}M {s}S"
            k.update()

        def slider_changed(e):
            t.value = f"Slider changed to {slider_value_m.current.value}M {slider_value_s.current.value}S"
            t.update()

        slider_ui = ft.Column(
            controls=[
                ft.Slider(ref=slider_value_m, min=0, max=59, divisions=59, label="{value}M", on_change=slider_changed),
                ft.Slider(ref=slider_value_s, min=1, max=12, divisions=11, label="{value}S", on_change=slider_changed),
                t,
                ft.ElevatedButton("設定", on_click=get_curretn_value),
                k,
            ]
        )
    
        def get_slider_values():
            return slider_value_m.current.value, slider_value_s.current.value

        return slider_ui, get_slider_values