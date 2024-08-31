import requests
from django.shortcuts import render
from .forms import PublicForm


def index(request):
    files = []
    error = None

    if request.method == 'POST':
        form = PublicForm(request.POST)
        if form.is_valid():
            public_key = form.cleaned_data['public_key']
            type = form.cleaned_data['type']
            url = f'https://cloud-api.yandex.net/v1/disk/public/resources?public_key={public_key}'
            
            try:
                response = requests.get(url)
                response.raise_for_status()

                data = response.json()
                try:
                    files = data['_embedded']['items']

                    if type != 'all':
                        if type == 'image':
                            files = [ f for f in files if f['mime_type'].startswith('image/')]
                    elif type == 'doc':
                            document_mime_types = [
                                'application/pdf',
                                'application/msword',
                                'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                                'application/vnd.ms-excel',
                                'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                                'text/plain'
                            ]
                            files = [f for f in files if f['mime_type'] in document_mime_types]
                    else:
                        files = files
                
                except KeyError:
                    error = "Файлы не найдены, попробуйте еще раз"
                
            except requests.exceptions.HTTPError:
                if 'error' in data:
                    error = f"Ошибка: {data['message']}"
                else:
                    error = f"Ошибка сети: {response.status_code}"
            except requests.exceptions.RequestException:
                error = "Ошибка сети: не удалось подключиться к серверу"

        else:
            error = "Не удалось получить данные с диска, проверьте ссылку"
    else:
        form = PublicForm()
    
    return render(request, 'disk/index.html', {'form': form, 'files': files, 'error': error})