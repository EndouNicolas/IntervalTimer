import flet as ft

class Setting(ft.UserControl):
    def settingUI(page:ft.Page):
        text =ft.Text("設定", size=30, weight=ft.FontWeight.W_900, selectable=True)
        pick_files_dialog = ft.FilePicker()
        page.overlay.append(pick_files_dialog)
        pick_file_button=ft.ElevatedButton(
                    "Pick files",
                    icon=ft.Icons.UPLOAD_FILE,
                    on_click=lambda _: pick_files_dialog.pick_files(
                        allow_multiple=True
                    )
                )
        
        def set_audio_file(e):
            page.dialog = pick_files_dialog
            pick_files_dialog.pick_files(allow_multiple=False, file_types=[".mp3"])
            page.dialog.open = True
            page.update()

        setting_ui = ft.Column(
            controls=[ft.Container(
                content=text,
                alignment=ft.alignment.center,
            ),
            ft.Container(content=pick_file_button,
                alignment=ft.alignment.center,
            ),]
        )
        return setting_ui