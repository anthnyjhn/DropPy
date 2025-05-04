from threading import Thread
from utils import get_local_ip, show_qr
from server import run, get_port

if __name__ == '__main__':
    ip = get_local_ip()
    thread = Thread(target=run)
    thread.start()
    show_qr(ip, get_port())
