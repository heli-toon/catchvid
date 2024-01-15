from django.shortcuts import render
from pytube.exceptions import RegexMatchError
from pytube import *
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import os
import platform
from jnius import autoclass

def on_progress(stream, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = bytes_downloaded / total_size * 100
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'progress_group',
        {
            'type': 'progress_update',
            'percentage_of_completion': percentage_of_completion
        }
    )
    return percentage_of_completion

def home(request):
    try:
        if request.method == 'POST':
            global link
            link = request.POST['link']
            video = YouTube(link)
            stream = video.streams.get_lowest_resolution()
            stream.download()

            return render(request, 'index.html')
        
        if platform.system() == 'Windows':
            output_path = os.path.join(os.path.expanduser('~'), 'Downloads')
        elif platform.system() == 'Linux':
            output_path = os.path.join(os.path.expanduser('~'), 'Downloads')
        elif platform.system() == 'Darwin':
            output_path = os.path.join(os.path.expanduser('~'), 'Downloads')
        elif platform.system() == 'Android':
            Environment = autoclass('android.os.Environment')
            output_path = os.path.join(Environment.getExternalStorageDirectory().getPath(), 'Download')

        else:
            raise Exception('Unsupported operating system')

        video = YouTube(link, on_progress_callback=on_progress)
        video.download(output_path=output_path)
        
    except RegexMatchError:
        error_message = "Sorry, we couldn't find a YouTube video that matches your link. Please try again."
        return render(request, 'index.html', {'error_message': error_message})
    return render(request, 'index.html')

def progress_update(event):
    percentage_of_completion = event['percentage_of_completion']
