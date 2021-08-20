import os
import socket
import traceback
from ftplib import FTP, error_perm
from json import load

from utils.exception import ExecuteException


class FtpHelper(object):
    def __init__(self, host, port, username, password):
        self.ftp = FTP()
        # ftp.set_debuglevel(2)
        self.ftp.encoding = 'utf-8'
        try:
            self.ftp.connect(host, port)
            self.ftp.login(username, password)
        except(socket.error, socket.gaierror):
            raise ExecuteException('', 'can not connect ftp server.')
        except error_perm:
            raise ExecuteException('', 'can not connect ftp server.')

    def listdir(self, path):
        if not self.is_exist_dir(path):
            raise ExecuteException('', 'not exist path %s on ftp server.' % path)
        self.ftp.cwd(path)
        files = self.ftp.nlst()
        return files

    def mkdir(self, path):
        # Suppose you want upload file to dir thy38
        try:
            self.ftp.cwd(path)
        except error_perm:
            try:
                self.ftp.mkd(path)
            except error_perm:
                print('U have no authority to make dir')

    def makedirs(self, path):
        # Suppose you want upload file to dir thy38
        try:
            self.ftp.cwd(path)
        except error_perm:
            try:
                if os.path.dirname(path) != '/':
                    self.makedirs(os.path.dirname(path))
                self.ftp.cwd(os.path.dirname(path))
                self.ftp.mkd(os.path.basename(path))
            except error_perm:
                print('U have no authority to make dir')

    def rename(self, target, filename, newname):
        # Suppose you want upload file to dir thy38
        try:
            self.ftp.cwd(target)
            self.ftp.rename(filename, newname)
        except error_perm:
            return False
        return True

    def is_exist_dir(self, path):
        # Suppose you want upload file to dir thy38
        try:
            self.ftp.cwd(path)
        except error_perm:
            return False
        return True

    def is_exist_file(self, path):
        # Suppose you want upload file to dir thy38
        try:
            self.ftp.cwd(os.path.dirname(path))
            if os.path.basename(path) in self.ftp.nlst():
                return True
        except error_perm:
            return False
        return False

    def delete_file(self, path):
        # Suppose you want upload file to dir thy38
        try:
            self.ftp.cwd(os.path.dirname(path))
            self.ftp.delete(os.path.basename(path))
        except error_perm:
            return False
        return True

    def upload_files(self, files, target_path):
        try:
            if self.is_exist_dir(target_path):
                self.ftp.cwd(target_path)
            else:
                self.makedirs(target_path)
                self.ftp.cwd(target_path)

            for filename in files:
                bufsize = 1024
                file_handle = open(filename, "rb")
                self.ftp.storbinary("STOR %s" % os.path.basename(filename), file_handle, bufsize)
        except error_perm:
            raise ExecuteException('', 'error while upload file from ftp server. %s' % error_perm.message)

    def delete_dir(self, target):
        if not self.is_exist_dir(target):
            return
        self.ftp.cwd(target)
        for file in self.listdir(target):
            if self.is_exist_dir('%s/%s' % (target, file)):
                self.delete_dir('%s/%s' % (target, file))
            else:
                self.ftp.delete(file)
        self.ftp.cwd(os.path.dirname(target))
        self.ftp.rmd(target)

    def upload_file(self, file, target_dir):
        try:
            if self.is_exist_dir(target_dir):
                self.ftp.cwd(target_dir)
            else:
                self.makedirs(target_dir)
                self.ftp.cwd(target_dir)
            filename = os.path.basename(file)
            if filename in self.ftp.nlst():
                if '%s.bak' % filename in self.ftp.nlst():
                    self.ftp.delete('%s.bak' % filename)
                self.ftp.rename(filename, '%s.bak' % filename)
            bufsize = 1024
            file_handle = open(file, "rb")
            self.ftp.storbinary("STOR %s" % os.path.basename(file), file_handle, bufsize)
            if '%s.bak' % filename in self.ftp.nlst():
                self.ftp.delete('%s.bak' % filename)
        except error_perm:
            # traceback.print_exc()
            raise ExecuteException('', 'error while upload file from ftp server. %s' % error_perm.message)

    def upload_dir(self, source_file_dir, target):
        # print source_file_dir
        if not os.path.exists(source_file_dir):
            raise ExecuteException('', 'not exist source file dir.')

        if not self.is_exist_dir(target):
            self.makedirs(target)

        files = get_dir_files(source_file_dir)
        for file in files:
            if target != '/':
                target_path = file.replace(source_file_dir, target)
            else:
                target_path = file.replace(source_file_dir, '')
            if not self.is_exist_dir(os.path.dirname(target_path)):
                self.makedirs(os.path.dirname(target_path))
            self.upload_file(file, os.path.dirname(target_path))

    def download_dir(self, download_path, target_path):
        if not os.path.exists(target_path):  # create file dir to save
            os.mkdir(target_path)
        try:
            if not self.is_exist_dir(download_path):
                raise ExecuteException('', 'not exist file on ftp server which need to download ')
            self.ftp.cwd(download_path)
            files = self.listdir(download_path)
            for filename in files:
                self.download_file('%s/%s' % (download_path, filename), '%s/%s' % (target_path, filename))
        except error_perm:
            raise ExecuteException('', 'error while download file from ftp server. %s' % error_perm.message)

    def download_file(self, download_path, target_path):
        if not os.path.exists(os.path.dirname(target_path)):  # create file dir to save
            os.mkdir(os.path.dirname(target_path))
        try:
            if not self.is_exist_file(download_path):
                raise ExecuteException('', 'not exist file on ftp server which need to download ')
            self.ftp.cwd(os.path.dirname(download_path))
            filename = os.path.basename(download_path)
            bufsize = 1024
            with open(target_path, 'wb') as fp:
                self.ftp.retrbinary("RETR %s" % filename, fp.write, bufsize)
        except error_perm:
            raise ExecuteException('', 'error while download file from ftp server. %s' % error_perm.message)

    def get_json_file_data(self, file_path):
        data = None
        if self.is_exist_file(file_path):
            self.download_file(file_path, '/tmp/%s' % os.path.basename(file_path))
            with open('/tmp/%s' % os.path.basename(file_path), 'r') as f:
                data = load(f)
            os.remove('/tmp/%s' % os.path.basename(file_path))
        return data


def get_dir_files(source_file_dir):
    files = []
    for source_file in os.listdir(source_file_dir):
        if os.path.isfile('%s/%s' % (source_file_dir, source_file)):
            files.append('%s/%s' % (source_file_dir, source_file))
        elif os.path.isdir('%s/%s' % (source_file_dir, source_file)):
            files.extend(get_dir_files('%s/%s' % (source_file_dir, source_file)))
    return files




if __name__ == '__main__':
    ftp = FtpHelper('133.133.135.30', '21', 'ftpuser', 'ftpuser')
    # ftp.set_debuglevel(2)
    # upload_file(ftp, '/tmp/123.json', '/vmbackuptest/clouddiskbackup/vmbackuptestdisk1')
    # print ftp.listdir('/vmbackuptest')
    # ftp.download_file('/vmbackuptest/clouddiskbackup/vmbackuptestdisk1/history.json', '/tmp/123.json')
    print((ftp.get_json_file_data('/cloudinitbackup4/history.json')))
    # ftp.makedirs('/test/test1/test2')
    # upload_dir(ftp, '/var/lib/libvirt/cstor/a639873f92a24a9ab840492f0e538f2b/a639873f92a24a9ab840492f0e538f2b/vmbackup', '/')
    # upload_file(ftp, ['/root/vmtest/vmtest.xml', '/root/vmtest/1.qcow2', '/root/vmtest/2.qcow2', '/root/vmtest/3.qcow2'], '/vmtest')
    # uploadFile(ftp, ['/root/vmtest/vmtest.xml', '/root/vmtest/1.qcow2', '/root/vmtest/2.qcow2', '/root/vmtest/3.qcow2'], '/uuid')
    # ftp.rmd('vmtest')
    # ftp.rename('uuid', 'vmtest')
    # downloadDir(ftp, '/vmtest', '/root/vmtest')
    # ftp.set_debuglevel(0)
    # print get_dir_files('/root/test1')