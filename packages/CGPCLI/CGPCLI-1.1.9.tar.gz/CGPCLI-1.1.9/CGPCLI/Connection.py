import socket
from CGPCLI.Parser import parse_to_python_object
from CGPCLI.Errors import FailedLogin, ConnectionTimeOut, CommandFailedError

class CGPConnector:
    def __init__(self, host, port=106):
        self.port = port
        self.host = host
    
    def connect(self):
        '''Create a connection with CGP server via socket'''
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.host, self.port))
            sock.settimeout(None)
            
            self.socket = sock
            self._read(get=False)
        except socket.error as e:
            raise e
        
    def _read(self, get=True, data=False):
        '''Metod that reads messages from server and returns dict containing server response
        if get parameter is set to True.
        
        :rtype dict

        Return examples:
        {"header": "200, "body": "OK"}
        {"header": "200", "body": "data follow"}
        
        '''
        
        message = {}
    
        if not data:
            msg = self.socket.recv(4).decode()
            message['header'] = msg.strip()
        
            msg_len = 1
        else:
            msg_len = 4096
            
        full = b''
            
        while True:
            try:
                msg = self.socket.recv(msg_len)
                full += msg
                
                if full.endswith('\r\n'.encode()):
                    message['body'] = full.decode('utf-8')[:-2]
                    break
    
            except ConnectionAbortedError:
                self.disconnect()
                raise ConnectionTimeOut()
        
        if get:
            return message

    def login(self, username, pwd):
        '''Log in CGP Account. Raises an Exception on failed login
        
        :sock socket
        :username str
        :pwd str
        
        '''
        
        check = '515'
        while check != '200':
            self.socket.send((f'USER {username}\n').encode())
            self._read(get=False)
    
            self.socket.send((f'PASS {pwd}\n').encode())
            check = self._read()['header'][:3]
            
            if check == '515':
                raise FailedLogin()
        
        self.socket.send(b'inline\n')
        self._read()

    def _operate(self, payload):  
        self.socket.send(payload.encode())

        result = self._read()

        if result['header'] in ('200', '201'):
            result['body'] = parse_to_python_object(result['body'])
            return result

        else:
            raise CommandFailedError(str(result))
        
    def disconnect(self):
        '''Close socket connection'''
        try:
            self.socket.send(('QUIT\n').encode())
            self.socket.close()
        except (ConnectionAbortedError, AttributeError):
            pass
        
        del self.socket
