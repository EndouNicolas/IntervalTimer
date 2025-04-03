import flet as ft

class Setting(ft.UserControl):
    def settingUI(page:ft.Page):
        text =ft.Text("設定", size=30, weight=ft.FontWeight.W_900, selectable=True)

        setting_ui = ft.Column(
            controls=[ft.Container(
                content=text,
                alignment=ft.alignment.center,
            )]
        )
        return setting_ui