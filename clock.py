import flet as ft
from datetime import datetime, timezone, timedelta
import asyncio
import requests

api_url = "https://3fe5a5f690efc790d4764f1c528a4ebb89fa4168.nict.go.jp/cgi-bin/json"

class Clock(ft.UserControl):


    def Time(page: ft.Page):
        now_time =ft.Text("00:00.0")

        async def set_time():
            nonlocal now_time
            while True:
                response = requests.get(api_url)
                if response.status_code == 200:
                    data = response.json()
                    unix_time = data.get("st")
                    jst_time = datetime.fromtimestamp(unix_time, tz=timezone.utc) + timedelta(hours=9)
                    now_time.value = jst_time.strftime("%Y/%m/%d %H:%M:%S")
                else:
                    now_time.value = "Error"
                page.update()
                await asyncio.sleep(1)

        
        page.run_task(set_time)

        clock_object =ft.Column(controls=[
            ft.Container(content=now_time),
        ])

        return clock_object