import flet as ft
from datetime import datetime, timezone, timedelta
import asyncio
import requests
import time

api_url = "https://3fe5a5f690efc790d4764f1c528a4ebb89fa4168.nict.go.jp/cgi-bin/json"

class Clock(ft.Control):


    def Time(page: ft.Page):
        now_time =ft.Text("00:00.0",size=80, weight=ft.FontWeight.W_900, selectable=True)
        time_source = ft.Text("取得中",size=20, weight=ft.FontWeight.W_900, selectable=True)

        async def set_time():
            nonlocal now_time
            while True:
                response = requests.get(api_url)
                if response.status_code == 200:
                    data = response.json()
                    unix_time = data.get("st")
                    jst_time = datetime.fromtimestamp(unix_time, tz=timezone.utc) + timedelta(hours=9)
                    now_time.value = jst_time.strftime("%Y/%m/%d %H:%M:%S")
                    time_source.value = "NICTから正確な時刻を取得中"
                else:
                    time_source.value = "コンピュータの時刻で表示中"
                    now_time.value = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
                page.update()
                await asyncio.sleep(1)

        
        page.run_task(set_time)

        clock_object =ft.Column(controls=[
            ft.Container(content=now_time,padding=20,
                alignment=ft.alignment.center,
                border_radius=10),ft.Container(content=time_source,padding=20,
                alignment=ft.alignment.center)
        ], alignment=ft.MainAxisAlignment.CENTER)

        return clock_object