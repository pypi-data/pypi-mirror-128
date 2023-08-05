from ftplib import FTP


def connect_to_ftp():
    HOST = "localhost"
    PORT = 15988                        # Set your desired port number
    ftp = FTP()
    ftp.connect(HOST, PORT)

    usr = 'ftp_test'
    pwd = 'ftp_pwd'
    ftp.login(usr, pwd)

if __name__ == '__main__':
    connect_to_ftp()
