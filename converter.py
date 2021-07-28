import cloudconvert
import os
import ssl
import subprocess
from colorama import Fore, Back, Style
from colorama import init

init()

ssl._create_default_https_context = ssl._create_unverified_context

def convert(imported_file):
	f = open("API_KEY.json", "r")
	pdf_to_emf = f.read()

	cloudconvert.configure(api_key = pdf_to_emf, sandbox = False)

	job = cloudconvert.Job.create(payload={
		'tag': 'convert_to_emf',
		'tasks': {
			'import-it': {
				'operation': 'import/upload'
			},
			'convert-it': {
				'operation': 'convert',
                'input_format': 'pdf',
                'output_format': 'emf',
                'engine': 'inkscape',
                'input': ['import-it']
			},
			'export-it': {
				'input': ['convert-it'],
				'operation': 'export/url'
			}
		}
	})

	import_task = None

	for task in job["tasks"]:
		task_name = task.get("name")

		if task_name == "import-it":
			import_task = task

		if task_name == "export-it":
			export_task = task

	import_task_id = import_task.get("id")
	export_task_id = export_task.get("id")

	import_task = cloudconvert.Task.find(id = import_task_id)
	uploaded = cloudconvert.Task.upload(file_name = imported_file, task = import_task)

	if uploaded:
		print("Успешно!")
		print("Конвертирование...")

		exported_task = cloudconvert.Task.wait(id=export_task_id)
		exported_url = exported_task.get("result").get("files")[0].get("url")

		print("Успешно!")
		print("Скачивание...")

		imported_file = exported_task.get("result").get("files")[0].get("filename")
		exported_task = cloudconvert.download(url = exported_url, filename = "out/" + imported_file)
		os.system(os.path.join(os.path.abspath(os.path.dirname(__file__)), "out/" + imported_file))

if __name__ == '__main__':
	print(Back.WHITE)
	print(Fore.BLACK)
	print("-----------Убедитесь, что у вас скачан Microsoft Visio!!!-----------")
	print("-----------Файлы для конвертации располагаются в папке /in-----------")
	print("-----------Сконвертированные файлы располагаются в папке /out-----------")
	print(Back.BLACK)
	print(Fore.GREEN)

	file_name = input("Введите имя файла: ")

	file_name = "in/" + file_name

	print("Загрузка файла...")

	convert(file_name)

	print("Успешно!")