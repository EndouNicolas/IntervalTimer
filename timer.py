import flet as ft
import signal
import asyncio

class Timer(ft.UserControl):
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    @staticmethod
    def Sliders():
        # スライダー値を保持する変数
        slider_value_m = ft.Slider(min=0, max=59, divisions=59, label="{value}M")
        slider_value_s = ft.Slider(min=0, max=59, divisions=59, label="{value}S")
        is_started = False
        is_stopped = False
        time_display = ft.Text()
        status_text = ft.Text()
        remaining_time = 0
        started_time = 0 #以前スタートされた時間を保持する変数

        async def count_down(page: ft.Page):
            nonlocal is_started,is_stopped,remaining_time
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

            is_started = False
            time_display.value = "終了"
            page.update()

        async def start_timer(e):
            nonlocal is_started,is_stopped,remaining_time,started_time
            #もしタイマーがスタート状態なら何もしない
            if is_started:
                return
            is_started = True
            is_stopped = False
            if remaining_time <=0:
                m, s = slider_value_m.value, slider_value_s.value
                started_time=remaining_time = int(m * 60 + s)
            status_text.value = f"タイマー開始: {remaining_time}秒"
            page = e.control.page 
            page.update()
            await count_down(page)

        async def stop_timer(e):
            nonlocal is_started, is_stopped,remaining_time
            if not is_started:
                #停止しているなら再開する
                await start_timer(e)
            else:
                is_stopped = not is_stopped
                if is_stopped:
                    time_display.value = f"停止:{remaining_time:.2f}秒"
                else:
                    time_display.value = "再開"
                e.control.page.update()
        
        def reset_timer(e):
            nonlocal is_started, is_stopped,remaining_time,started_time
            if is_started and not is_stopped:
                is_stopped = True
                is_started = False
                remaining_time = float(started_time)  # 小数点を保持
            time_display.value = f"{remaining_time:.2f}秒"  # 表示もフォーマット
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
