import flet as ft
from datetime import datetime
import time
import requests

api_url ="https://3fe5a5f690efc790d4764f1c528a4ebb89fa4168.nict.go.jp/cgi-bin/json"
response = requests.get(api_url)

class Clock(ft.UserControl):
    
    
    def test(page:ft.Page):
        page.add(ft.Text(response))
        page.update()