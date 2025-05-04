import netifaces as ni
import qrcode

def get_local_ip():
    interfaces = ni.interfaces()
    for iface in interfaces:
        if iface != 'lo' and ni.AF_INET in ni.ifaddresses(iface):
            addr = ni.ifaddresses(iface)[ni.AF_INET][0]['addr']
            if addr.startswith(('192.', '10.', '172.')):
                return addr
    return '127.0.0.1'

def show_qr(ip, port):
    url = f'http://{ip}:{port}/'
    qr = qrcode.QRCode()
    qr.add_data(url)
    qr.make(fit=True)
    print(f"\n📶 Upload page URL: {url}\n")
    qr.print_ascii(invert=True)
