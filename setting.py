import flet as ft
from playsound3 import playsound

class Setting(ft.UserControl):
    def settingUI(page: ft.Page):
        text = ft.Text("設定", size=30, weight=ft.FontWeight.W_900, selectable=True)
        selected_file = ft.Text()

        def set_audio_file(e: ft.FilePickerResultEvent):
            selected_file.value = e.files[0].path if e.files else "No file selected"
            page.update()

        def play_sound(e: ft.ControlEvent):
            if selected_file.value != "No file selected":
                playsound(selected_file.value)

        pick_files_dialog = ft.FilePicker(on_result=set_audio_file)
        page.overlay.append(pick_files_dialog)

        pick_file_button = ft.ElevatedButton(
            "Pick files",
            icon=ft.Icons.UPLOAD_FILE,
            on_click=lambda _: pick_files_dialog.pick_files(
                allow_multiple=True
            )
        )
        
        play_sound_test = ft.ElevatedButton("Play sound test",on_click=play_sound)

        setting_ui = ft.Column(
            controls=[
                ft.Container(content=text, alignment=ft.alignment.center),
                ft.Container(content=pick_file_button, alignment=ft.alignment.center),
                ft.Container(content=selected_file, alignment=ft.alignment.center),
                ft.Container(content=play_sound_test, alignment=ft.alignment.center),
            ]
        )
        return setting_ui
