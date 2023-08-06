from pyftpdlib.handlers import FTPHandler, FilesystemError, _strerror, FileProducer
from omnitools import FTPESS, FTPS, FTP_ThrottledDTPHandler, TLS_FTPHandler
from .utils import FTPRelayFO
import threading
import os


class FTPFCS_ThrottledDTPHandler(FTP_ThrottledDTPHandler):
    uploading = False
    downloading = False
    homebase = None
    relay_upload_remote_root = None

    def relay_upload_worker(self):
        raise NotImplementedError

    def alter_recv2(self, chunk, flags):
        return chunk

    def alter_recv(self, chunk):
        if self.transfer_limit:
            self.read_limit = int(self.transfer_limit/len(self.clients_transferring))
        uploading = self.uploading
        if not self.uploading:
            self.uploading = True
            username = self.cmd_channel.username
            name = self.file_obj.name
            self.file_obj.close()
            os.remove(name)
            self.file_obj = FTPRelayFO()
            self.file_obj.name = os.path.basename(name)
            if not self.relay_upload_remote_root:
                homedir = os.path.join(self.homebase, username)
                remote_name = name.replace(homedir, "")[1:].replace("\\", "/")
                remote_root = "/{}".format(username)
                dirname = os.path.dirname(remote_name)
                if dirname:
                    remote_root += "/"+dirname
                self.relay_upload_remote_root = remote_root
            p = threading.Thread(target=self.relay_upload_worker)
            p.daemon = True
            p.start()
        return self.alter_recv2(chunk, [uploading])

    def alter_send2(self, data, flags):
        return data

    def alter_send(self, data, flags=[-1]):
        ff = flags[0]
        if ff <= 1:
            ff += 1
            flags.clear()
            flags.append(ff)
        if self.transfer_limit:
            self.write_limit = int(self.transfer_limit/len(self.clients_transferring))
        if not self.downloading:
            self.downloading = True
        return self.alter_send2(data, flags)


class FTPFCSS_ThrottledDTPHandler(FTPFCS_ThrottledDTPHandler, TLS_FTPHandler):
    pass


class FTPFCS_FTPHandler(FTPHandler):
    file_obj = None
    homebase = None

    def relay_download_worker(self, remote_file):
        raise NotImplementedError

    def ftp_RETR(self, file):
        rest_pos = self._restart_position
        self._restart_position = 0
        try:
            if not file.startswith(os.path.join(self.homebase, self.username)):
                raise FilesystemError("Directory traversal attack detected.")
            file = "/"+file.replace(self.homebase, "")[1:].replace("\\", "/")
            fd = FTPRelayFO()
            self.file_obj = fd
            self.file_obj.name = os.path.basename(file)
            p = threading.Thread(target=self.relay_download_worker, args=(file,))
            p.daemon = True
            p.start()
        except (EnvironmentError, FilesystemError) as err:
            why = _strerror(err)
            self.respond('550 %s.' % why)
            return
        try:
            if rest_pos:
                why = "Invalid REST parameter"
                fd.close()
                self.respond('554 %s' % why)
                return
            producer = FileProducer(fd, self._current_type)
            self.push_dtp_data(producer, isproducer=True, file=fd, cmd="RETR")
            return file
        except Exception:
            fd.close()
            raise


class FTPFCSS_Base:
    def init(self, *args, **kwargs):
        self.handler.dtp_handler.homebase = self.homebase
        self.handler.dtp_handler.uploading = FTPFCSS_ThrottledDTPHandler.uploading
        self.handler.dtp_handler.relay_upload_remote_root = FTPFCSS_ThrottledDTPHandler.relay_upload_remote_root
        self.handler.dtp_handler.relay_upload_worker = FTPFCSS_ThrottledDTPHandler.relay_upload_worker
        self.handler.dtp_handler.alter_recv2 = FTPFCSS_ThrottledDTPHandler.alter_recv2
        self.handler.dtp_handler.alter_recv = FTPFCSS_ThrottledDTPHandler.alter_recv
        self.handler.homebase = self.homebase
        self.handler.dtp_handler.downloading = FTPFCSS_ThrottledDTPHandler.downloading
        self.handler.ftp_RETR = FTPFCS_FTPHandler.ftp_RETR
        self.handler.file_obj = FTPFCS_FTPHandler.file_obj
        self.handler.relay_download_worker = FTPFCS_FTPHandler.relay_download_worker
        self.handler.dtp_handler.alter_send2 = FTPFCSS_ThrottledDTPHandler.alter_send2
        self.handler.dtp_handler.alter_send = FTPFCSS_ThrottledDTPHandler.alter_send

    def generate_users(self):
        for i in range(1, 10):
            user = "foxe"+str(i)
            homedir = os.path.join(self.homebase, user)
            os.makedirs(homedir, exist_ok=True)
            self.handler.authorizer.add_user(user, user, homedir, "elradfmwMT")


class FTPFCSS(FTPS, FTPFCSS_Base):
    def __init__(self, *args, homebase: str, relay_timeout: int = 30, **kwargs):
        super().__init__(*args, **kwargs)
        self.homebase = homebase
        FTPRelayFO.timeout = relay_timeout
        self.timeout = relay_timeout
        self.init(*args, **kwargs)


class FTPFCSESS(FTPESS, FTPFCSS_Base):
    def __init__(self, *args, homebase: str, relay_timeout: int = 30, **kwargs):
        super().__init__(*args, **kwargs)
        self.handler.tls_control_required = True
        self.handler.tls_data_required = True
        self.homebase = homebase
        FTPRelayFO.timeout = relay_timeout
        self.timeout = relay_timeout
        self.init(*args, **kwargs)


