#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import base64
import ssl
import argparse
import urllib3
from threading import Thread
try:
    from urllib.parse import urlparse
except ImportError:
     from urlparse import urlparse
from socket import *
from threading import Thread
from time import sleep
import struct

# Constants
SOCKTIMEOUT = 5
RESENDTIMEOUT = 300
VER4 = b"\x04"
VER = b"\x05"
METHOD = b"\x00"
SUCCESS = b"\x00"
SOCKFAIL = b"\x01"
NETWORKFAIL = b"\x02"
HOSTFAIL = b"\x04"
REFUSED = b"\x05"
TTLEXPIRED = b"\x06"
UNSUPPORTCMD = b"\x07"
ADDRTYPEUNSPPORT = b"\x08"
UNASSIGNED = b"\x09"

BASICCHECKSTRING = b"Georg says, 'All seems fine'"
BASICAUTH=""

HTTP_TLS = False
CERT_REQS = ssl.CERT_REQUIRED

# Globals
READBUFSIZE = 1024

# Logging
RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[1;%dm"
BOLD_SEQ = "\033[1m"

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

LEVEL = {"INFO": logging.INFO, "DEBUG": logging.DEBUG, }

logLevel = "INFO"

COLORS = {
    'WARNING': YELLOW,
    'INFO': WHITE,
    'DEBUG': BLUE,
    'CRITICAL': YELLOW,
    'ERROR': RED,
    'RED': RED,
    'GREEN': GREEN,
    'YELLOW': YELLOW,
    'BLUE': BLUE,
    'MAGENTA': MAGENTA,
    'CYAN': CYAN,
    'WHITE': WHITE,
}


def formatter_message(message, use_color=True):
    if use_color:
        message = message.replace("$RESET", RESET_SEQ).replace("$BOLD", BOLD_SEQ)
    else:
        message = message.replace("$RESET", "").replace("$BOLD", "")
    return message


class ColoredFormatter(logging.Formatter):
    def __init__(self, msg, use_color=True):
        logging.Formatter.__init__(self, msg)
        self.use_color = use_color

    def format(self, record):
        levelname = record.levelname
        if self.use_color and levelname in COLORS:
            levelname_color = COLOR_SEQ % (30 + COLORS[levelname]) + levelname + RESET_SEQ
            record.levelname = levelname_color
        return logging.Formatter.format(self, record)


class ColoredLogger(logging.Logger):

    def __init__(self, name):
        FORMAT = "[$BOLD%(levelname)-18s$RESET]  %(message)s"
        COLOR_FORMAT = formatter_message(FORMAT, True)
        logging.Logger.__init__(self, name, logLevel)
        if (name == "transfer"):
            COLOR_FORMAT = "\x1b[80D\x1b[1A\x1b[K%s" % COLOR_FORMAT
        color_formatter = ColoredFormatter(COLOR_FORMAT)

        console = logging.StreamHandler()
        console.setFormatter(color_formatter)

        self.addHandler(console)
        return


logging.setLoggerClass(ColoredLogger)
log = logging.getLogger(__name__)
transferLog = logging.getLogger("transfer")


class SocksCmdNotImplemented(Exception):
    pass


class SocksProtocolNotImplemented(Exception):
    pass


class RemoteConnectionFailed(Exception):
    pass


class session(Thread):
    def __init__(self, pSocket, connectString):
        Thread.__init__(self)
        self.pSocket = pSocket
        self.connectString = connectString
        o = urlparse(connectString)
        try:
            self.httpPort = o.port
        except:
            if o.scheme == "https":
                self.httpPort = 443
            else:
                self.httpPort = 80
        self.httpScheme = o.scheme
        self.httpHost = o.netloc.split(":")[0]
        self.httpPath = o.path
        self.cookie = None
        if o.scheme == "http":
            self.httpScheme = urllib3.HTTPConnectionPool
            HTTP_TLS = False
        else:
            self.httpScheme = urllib3.HTTPSConnectionPool
            HTTP_TLS = True
        log.debug("finished init")

    def parseSocks5(self, sock):
        log.debug("SocksVersion5 detected")
        nmethods = sock.recv(1)
        methods = sock.recv(ord(nmethods))
        sock.sendall(VER + METHOD)
        ver = sock.recv(1)
        if ver == b"\x02":  # this is a hack for proxychains
            ver, cmd, rsv, atyp = (sock.recv(1), sock.recv(1), sock.recv(1), sock.recv(1))
        else:
            cmd, rsv, atyp = (sock.recv(1), sock.recv(1), sock.recv(1))
        target = None
        targetPort = None
        if atyp == b"\x01":  # IPv4
            # Reading 6 bytes for the IP and Port
            target = sock.recv(4)
            targetPort = sock.recv(2)
            target = inet_ntoa(target)
            # target = "." .join([str(ord(i)) for i in target])
        elif atyp == b"\x03":  # Hostname
            targetLen = ord(sock.recv(1))  # hostname length (1 byte)
            target = sock.recv(targetLen)
            targetPort = sock.recv(2)
            # target = "".join([unichr(ord(i)) for i in target])
            target = target.decode()
        elif atyp == b"\x04":  # IPv6
            target = sock.recv(16)
            targetPort = sock.recv(2)
            target = inet_ntop(AF_INET6, target)
            #tmp_addr = []
            #for i in xrange(len(target) / 2):
            #    tmp_addr.append(unichr(ord(target[2 * i]) * 256 + ord(target[2 * i + 1])))
            #target = ":".join(tmp_addr)
        if targetPort == None:
            return False
        # targetPort = ord(targetPort[0]) * 256 + ord(targetPort[1])
        targetPortNum = struct.unpack('>H', targetPort)[0]
        if cmd == b"\x02":  # BIND
            raise SocksCmdNotImplemented("Socks5 - BIND not implemented")
        elif cmd == b"\x03":  # UDP
            raise SocksCmdNotImplemented("Socks5 - UDP not implemented")
        elif cmd == b"\x01":  # CONNECT
            # serverIp = target
            serverIp = inet_aton(target)
            try:
                serverIp = gethostbyname(target)
            except:
                log.error("oeps")
            # serverIp = "".join([chr(int(i)) for i in serverIp.split(".")])
            self.cookie = self.setupRemoteSession(target, targetPortNum)
            # kst added below
            serverIp = inet_aton(target)
            if self.cookie:
                sock.sendall(VER + SUCCESS + b"\x00" + b"\x01" + serverIp + targetPort)
                return True
            else:
                sock.sendall(VER + REFUSED + b"\x00" + b"\x01" + serverIp + targetPort)
                raise RemoteConnectionFailed("[%s:%d] Remote failed" % (target, targetPortNum))

        raise SocksCmdNotImplemented("Socks5 - Unknown CMD")

    def parseSocks4(self, sock):
        log.debug("SocksVersion4 detected")
        cmd = sock.recv(1)
        if cmd == b"\x01":  # Connect
            targetPort = sock.recv(2)
            # targetPort = ord(targetPort[0]) * 256 + ord(targetPort[1])
            targetPortNum = struct.unpack('>H', targetPort)[0]
            targetPortOrd = struct.pack(">h", targetPortNum)
            target = sock.recv(4)
            sock.recv(1)
            # target = ".".join([str(ord(i)) for i in target])
            target = inet_ntoa(target)
            # target = inet_aton(str(target))
            serverIp = target
            log.debug("1 Connecting to %s:%s" % (target, serverIp))
            try:
                serverIp = gethostbyname(target)
            except:
                log.error("oeps")
            log.debug("1 Resolved %s to %s" % (target, serverIp))
            serverIp = inet_aton(str(serverIp))
            # log.debug("2 Connecting to %s:%s" % (target, serverIp))
            log.debug("3 Connecting to %s:%d" % (target, targetPortNum))
            self.cookie = self.setupRemoteSession(target, targetPortNum)
            if self.cookie:
                log.debug("[%s:%d] success of getting cookie" % (target, targetPortNum))
                barr=b"\x00" + b"\x5A" + serverIp + targetPortOrd
                sock.sendall(barr)
                return True
            else:
                log.debug("[%s:%d] not success of getting cookie" % (target, targetPortNum))
                barr=b"\x00" + b"\x5B" + serverIp + targetPortOrd
                sock.sendall(barr)
                raise RemoteConnectionFailed("Remote connection failed")
        else:
            raise SocksProtocolNotImplemented("Socks4 - Command [%d] Not implemented" % ord(cmd))

    def handleSocks(self, sock):
        # This is where we setup the socks connection
        log.debug("handleSocks()")
        ver = sock.recv(1)
        if ver == b"\x05":
            return self.parseSocks5(sock)
        elif ver == b"\x04":
            return self.parseSocks4(sock)

    def setupRemoteSession(self, target, port):
        log.debug("setupRemoteSession()")
        headers = {"X-CMD": "CONNECT", "X-TARGET": target, "X-PORT": str(port)}
        if BASICAUTH != "":
            headers['Authorization'] = ("Basic %s") % BASICAUTH
            log.debug("headers['Authorization']")
            log.debug(headers['Authorization'])
        self.target = target
        self.port = port
        cookie = None
        if HTTP_TLS:
            if CERT_REQS == ssl.CERT_NONE:
                conn = self.httpScheme(host=self.httpHost, port=self.httpPort, cert_reqs=CERT_REQS, assert_hostname=False)
            else:
                conn = self.httpScheme(host=self.httpHost, port=self.httpPort, cert_reqs=CERT_REQS)
        else:
            conn = self.httpScheme(host=self.httpHost, port=self.httpPort)
        # response = conn.request("POST", self.httpPath, params, headers)
        response = conn.urlopen('POST', self.connectString + "?cmd=connect&target=%s&port=%d" % (target, port), headers=headers, body="")
        if response.status == 200:
            status = response.getheader("x-status")
            if status == "OK":
                cookie = response.getheader("set-cookie")
                log.info("[%s:%d] HTTP [200]: cookie [%s]" % (self.target, self.port, cookie))
            else:
                if response.getheader("X-ERROR") is not None:
                    log.error(response.getheader("X-ERROR"))
        else:
            log.error("[%s:%d] HTTP [%d]: [%s]" % (self.target, self.port, response.status, response.getheader("X-ERROR")))
            log.error("[%s:%d] RemoteError: %s" % (self.target, self.port, response.data))
        conn.close()
        log.debug("setupRemoteSession()-end")
        return cookie

    def closeRemoteSession(self):
        headers = {"X-CMD": "DISCONNECT", "Cookie": self.cookie}
        if BASICAUTH != "":
            headers['Authorization'] = "Basic %s" % BASICAUTH
        params = ""
        if HTTP_TLS:
            if CERT_REQS == ssl.CERT_NONE:
                conn = self.httpScheme(host=self.httpHost, port=self.httpPort, cert_reqs=CERT_REQS, assert_hostname=False)
            else:
                conn = self.httpScheme(host=self.httpHost, port=self.httpPort, cert_reqs=CERT_REQS)
        else:
            conn = self.httpScheme(host=self.httpHost, port=self.httpPort)
        response = conn.request("POST", self.httpPath + "?cmd=disconnect", params, headers)
        if response.status == 200:
            log.info("[%s:%d] Connection Terminated" % (self.target, self.port))
        conn.close()

    def reader(self):
        if HTTP_TLS:
            conn = urllib3.PoolManager(cert_reqs = CERT_REQS)
        else:
            conn = urllib3.PoolManager()
        while True:
            try:
                if not self.pSocket:
                    break
                # data = b""
                headers = {"X-CMD": "READ", "Cookie": self.cookie, "Connection": "Keep-Alive"}
                if BASICAUTH != "":
                    headers['Authorization'] = "Basic %s" % BASICAUTH
                response = conn.urlopen('POST', self.connectString + "?cmd=read", headers=headers, body="")
                data = None
                if response.status == 200:
                    status = response.getheader("x-status")
                    if status == "OK":
                        if response.getheader("set-cookie") is not None:
                            cookie = response.getheader("set-cookie")
                        data = response.data
                        # Yes I know this is horrible, but its a quick fix to issues with tomcat 5.x bugs that have been reported, will find a propper fix laters
                        try:
                            if response.getheader("server").find("Apache-Coyote/1.1") > 0:
                                data = data[:len(data) - 1]
                        except:
                            pass
                        if data is None:
                            data = b""
                    else:
                        data = None
                        log.error("[%s:%d] HTTP [%d]: Status: [%s]: Message [%s] Shutting down" % (self.target, self.port, response.status, status, response.getheader("X-ERROR")))
                else:
                    log.error("[%s:%d] HTTP [%d]: Shutting down" % (self.target, self.port, response.status))
                if data is None:
                    log.debug("[%s:%d] data is None" % (self.target, self.port))
                    # Remote socket closed
                    break
                if len(data) == 0:
                    log.debug("[%s:%d] len(data)==0" % (self.target, self.port))
                    sleep(0.1)
                    continue
                transferLog.info("[%s:%d] <<<< [%d]" % (self.target, self.port, len(data)))
                self.pSocket.send(data)
            except Exception as ex:
                raise ex
        self.closeRemoteSession()
        log.debug("[%s:%d] Closing localsocket" % (self.target, self.port))
        try:
            self.pSocket.close()
        except:
            log.debug("[%s:%d] Localsocket already closed" % (self.target, self.port))

    def writer(self):
        global READBUFSIZE
        if HTTP_TLS:
            conn = urllib3.PoolManager(cert_reqs = CERT_REQS)
        else:
            conn = urllib3.PoolManager()
        while True:
            try:
                self.pSocket.settimeout(1)
                data = self.pSocket.recv(READBUFSIZE)
                if not data:
                    break

                headers = {"X-CMD": "FORWARD", "Cookie": self.cookie, "Content-Type": "application/octet-stream", "Connection": "Keep-Alive"}
                if BASICAUTH != "":
                    headers['Authorization'] = "Basic %s" % BASICAUTH
                response = conn.urlopen('POST', self.connectString + "?cmd=forward", headers=headers, body=data)
                if response.status == 200:
                    status = response.getheader("x-status")
                    if status == "OK":
                        if response.getheader("set-cookie") is not None:
                            self.cookie = response.getheader("set-cookie")
                    else:
                        log.error("[%s:%d] HTTP [%d]: Status: [%s]: Message [%s] Shutting down" % (self.target, self.port, response.status, status, response.getheader("x-error")))
                        break
                else:
                    log.error("[%s:%d] HTTP [%d]: Shutting down" % (self.target, self.port, response.status))
                    break
                transferLog.info("[%s:%d] >>>> [%d]" % (self.target, self.port, len(data)))
            except timeout:
                continue
            except Exception as ex:
                raise ex
                break
        self.closeRemoteSession()
        log.debug("Closing localsocket")
        try:
            self.pSocket.close()
        except:
            log.debug("Localsocket already closed")

    def run(self):
        log.debug("run()")
        try:
            if self.handleSocks(self.pSocket):
                log.debug("Staring reader")
                r = Thread(target=self.reader, args=())
                r.start()
                log.debug("Staring writer")
                w = Thread(target=self.writer, args=())
                w.start()
                r.join()
                w.join()
        except SocksCmdNotImplemented as si:
            log.error(si.message)
            self.pSocket.close()
        except SocksProtocolNotImplemented as spi:
            log.error(spi.message)
            self.pSocket.close()
        except Exception as e:
            log.error(e.message)
            self.closeRemoteSession()
            self.pSocket.close()


def askGeorg(connectString, creds):
    global BASICAUTH
    global HTTP_TLS
    connectString = connectString
    o = urlparse(connectString)
    try:
        httpPort = o.port
    except:
        if o.scheme == "https":
            httpPort = 443
        else:
            httpPort = 80
    httpScheme = o.scheme
    httpHost = o.netloc.split(":")[0]
    httpPath = o.path
    if o.scheme == "http":
        httpScheme = urllib3.HTTPConnectionPool
        HTTP_TLS = False
    else:
        httpScheme = urllib3.HTTPSConnectionPool
        HTTP_TLS = True

    if HTTP_TLS:
        if CERT_REQS == ssl.CERT_NONE:
            conn = httpScheme(host=httpHost, port=httpPort, cert_reqs=CERT_REQS, assert_hostname=False)
        else:
            conn = httpScheme(host=httpHost, port=httpPort, cert_reqs=CERT_REQS)
    else:
        conn = httpScheme(host=httpHost, port=httpPort)

    if creds != "":
        headers = urllib3.make_headers(basic_auth=creds)
        response = conn.request("GET", httpPath, headers=headers)
        BASICAUTH=base64.b64encode(creds.encode()).decode()
        log.debug(BASICAUTH)
    else:
        response = conn.request("GET", httpPath)
    print(response.data.strip())
    if response.status == 200:
        # print(response.data.strip())
        if BASICCHECKSTRING == response.data.strip():
            log.info(BASICCHECKSTRING)
            return True
    conn.close()
    return False

if __name__ == '__main__':
    print("""\033[1m
    \033[1;33m
                     _____
  _____   ______  __|___  |__  ______  _____  _____   ______
 |     | |   ___||   ___|    ||   ___|/     \|     | |   ___|
 |     \ |   ___||   |  |    ||   ___||     ||     \ |   |  |
 |__|\__\|______||______|  __||______|\_____/|__|\__\|______|
                    |_____|
                    ... every office needs a tool like Georg

  willem@sensepost.com / @_w_m__
  sam@sensepost.com / @trowalts
  etienne@sensepost.com / @kamp_staaldraad
  kost/ @k0st
  \033[0m
   """)
    log.setLevel(logging.DEBUG)
    parser = argparse.ArgumentParser(description='Socks server for reGeorg HTTP(s) tunneller')
    parser.add_argument("-c", "--creds", metavar="", help="Credentials for basic authentication as user:pass", default="")
    parser.add_argument("-l", "--listen-on", metavar="", help="The default listening socks address", default="127.0.0.1")
    parser.add_argument("-p", "--listen-port", metavar="", help="The default listening socks port", type=int, default="8888")
    parser.add_argument("-r", "--read-buff", metavar="", help="Local read buffer, max data to be sent per POST", type=int, default="1024")
    parser.add_argument("-s", "--ssl", metavar="", help="check TLS/SSL certificate", type=bool, default=False)
    parser.add_argument("-u", "--url", metavar="", required=True, help="The url containing the tunnel script")
    parser.add_argument("-v", "--verbose", metavar="", help="Verbose output[INFO|DEBUG]", default="INFO")
    args = parser.parse_args()
    if (args.verbose in LEVEL):
        log.setLevel(LEVEL[args.verbose])
        log.info("Log Level set to [%s]" % args.verbose)

    if (args.ssl):
        CERT_REQS = ssl.CERT_REQUIRED
    else:
        log.info("Disable SSL/TLS warnings")
        CERT_REQS = ssl.CERT_NONE
        ssl._create_default_https_context = ssl._create_unverified_context
        urllib3.disable_warnings()

    log.info("Starting socks server [%s:%d], tunnel at [%s]" % (args.listen_on, args.listen_port, args.url))
    log.info("Checking if Georg is ready")
    if not askGeorg(args.url, args.creds):
        log.info("Georg is not ready, please check url")
        exit()
    READBUFSIZE = args.read_buff
    servSock = socket(AF_INET, SOCK_STREAM)
    servSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    servSock.bind((args.listen_on, args.listen_port))
    servSock.listen(1000)
    while True:
        try:
            sock, addr_info = servSock.accept()
            sock.settimeout(SOCKTIMEOUT)
            log.debug("Incomming connection")
            session(sock, args.url).start()
        except KeyboardInterrupt as ex:
            break
        except Exception as e:
            log.error(e)
    servSock.close()
