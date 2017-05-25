import pytest
import paramiko
import binascii
import os
import re


def test_ssh1():

    host = '192.168.101.3'
    user = 'root'
    secret = 'iskratel'

    try:

        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username=user, password=secret)
        stdin, stdout, stderr = client.exec_command('ls -l /opt/jboss-as/standalone/deployments/eha*')
        data = stdout.read() + stderr.read()
        data_eha = data.decode('utf-8').splitlines()
        client.close()
        return ''.join(["{}\n".format(x) for x in data_eha])
    except paramiko.ssh_exception.AuthenticationException:
        print("Authentication failed.")
    except TimeoutError:
        print("TimeoutError")


# print(test_ssh1())

def test_update_eha():
    sorce_dir = 'Z:\Downloaded packages\AA6410AX(EHA)\EHA'
    packet = 'eha-install-0.4.4.1-SNAPSHOT.tar.gz'
    ff = 'Z:\Downloaded packages\AA6410AX(EHA)\EHA\eha-install-0.4.4.1-SNAPSHOT.tar.gz'
    dest_host = "192.168.101.3"
    user = 'root'
    secret = 'iskratel'

    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(dest_host,\
                       username=user,\
                       password=secret)
        ftp = client.open_sftp()
        ftp.put(ff, packet)
        ftpdir = ftp.listdir()
        ftp.close()
        for i in ftpdir:
            if re.search(packet, i):
                print("Succes put to ftp {}".format(ftpdir))
                stdin, stdout, stderr = client.exec_command('java -jar eha-setup-0.4.4.1*')
                data = stdout.read() + stderr.read()
                break
            # else:
            #     print("Wrong put to ftp file: {}, ftpdir: {}".format(packet, ftpdir))
        client.close()
        return "ftp!!!"
    except paramiko.ssh_exception.AuthenticationException:
        return("Authentication failed.")
    except TimeoutError:
        return("TimeoutError")
    except PermissionError:
        return("Permission denied")
    # except:
    #     raise("Unckoun failed.")


# test_update_eha()


def chk_active_side_eha():

        def chk_side(ipside, user, passwd):

            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(ipside, username=user, password=passwd)
            stdin, stdout, stderr = client.exec_command('uptime')
            data = stdout.read() + stderr.read()
            uptime = data.decode('utf-8').splitlines()

            stdin, stdout, stderr = client.exec_command('cat /proc/drbd')
            data = stdout.read() + stderr.read()
            data_eha = data.decode('utf-8').splitlines()
            for active in data_eha:
                if re.search("Secondary/Primary", active):
                    return False
                    break
                if re.search("Primary/Secondary", active):
                    return True
                    break
                if re.search("No such file or directory", active):
                    return False
                
            #print(data_eha)
            client.close()

        return chk_side("192.168.101.3", "root", "iskratel")

print(chk_active_side_eha())
