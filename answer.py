import re

def is_valid_socket(socket_address):

  socket = socket_address.split(":", 1)
  port = int(socket[1])
  path = socket[0].split(".")

  if 1 > port or port > 65535:
      return False

  for num in path:
    regex = r'\d'
    if re.search(regex, num) is not None:
      if 0 > int(num) or int(num) > 255:
        return False
  return True

if __name__ == '__main__':
    for socket_address in ["127.12.23.43:5000",
                           "127.A:-12"]:
        print is_valid_socket(socket_address)
