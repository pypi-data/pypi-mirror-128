from CGPCLI.Commands import Server

if __name__ == '__main__':
  server = Server(input('hostname: '))
  server.connect()
  server.login(input('username: '), input('password: '))
  print(server.noop())
  print(server.get_account_info('*'))
  server.disconnect()