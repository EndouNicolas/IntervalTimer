import flet as ft

class Setting(ft.Control):
    def __init__(self):
        super().__init__()
        self.selected_file = None


    def settingUI(page: ft.Page):
        text = ft.Text("設定", size=30, weight=ft.FontWeight.W_900, selectable=True)

        def full_screen(e):
            page.window_full_screen = not page.window_full_screen
            set_fullscreen.text = "ウィンドウモード" if page.window_full_screen else "フルスクリーン"
            set_fullscreen.icon = ft.Icons.WINDOW if page.window_full_screen else ft.Icons.FULLSCREEN
            page.update()


        set_fullscreen = ft.ElevatedButton(
            "フルスクリーン", icon=ft.Icons.FULLSCREEN, on_click=full_screen)
        
        def set_audio_file(e: ft.FilePickerResultEvent):
            selected_file = e.files[0].path if e.files else "No file selected"

        pick_files_dialog = ft.FilePicker(on_result=set_audio_file)
        page.overlay.append(pick_files_dialog)


        #ボタンを宣言

        pick_file_button = ft.ElevatedButton(
            "Pick files",
            icon=ft.Icons.UPLOAD_FILE,
            on_click=lambda _: pick_files_dialog.pick_files(
                allow_multiple=True,
                allowed_extensions=["mp3", "wav"],
                file_type="audio",
            )
        )
        save_settings = ft.ElevatedButton("設定を保存", on_click=lambda _: page.go("/"))

        setting_ui = ft.Column(
            controls=[
                ft.Container(content=text, alignment=ft.alignment.center),
                ft.Container(content=pick_file_button, alignment=ft.alignment.center),
                ft.Container(content=set_fullscreen, alignment=ft.alignment.center),

            ]
        )
        return setting_ui
