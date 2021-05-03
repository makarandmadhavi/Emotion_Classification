from converter import Converter
conv = Converter("ffmpeg/bin/ffmpeg.exe","ffmpeg/bin/ffprobe.exe")

info = conv.probe('static/processedvids/TestVideo.avi')

convert = conv.convert('static/processedvids/TestVideo.avi', 'static/processedvids/TestVideo11.mp4', {
    'format': 'mp4',
    'audio': {
        'codec': 'aac',
        'samplerate': 11025,
        'channels': 2
    },
    'video': {
        'codec': 'hevc',
        'width': 720,
        'height': 400,
        'fps': 25
    }})
