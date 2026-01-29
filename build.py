from src.core.metadata import __version__
import PyInstaller.__main__

def build_executable():
    PyInstaller.__main__.run([
        '--add-data=src/assets;assets',
        '-i', 'src/assets/app_square.ico',
        '--noconsole',
        f'--name=SwiftTube_a{__version__}',
        '--onedir',
        '--clean',
        'src/main.py'
    ])

if __name__ == "__main__":
    build_executable()
