from array import array
from multiprocessing.connection import Client

address = ('localhost', 6000)

with Client(address, authkey=b'password') as conn:
    print(conn.recv())  # => [2.25, None, 'junk', float]

    print(conn.recv_bytes())  # => 'hello'

    arr = array('i', [0, 0, 0, 0, 0])
    print(conn.recv_bytes_into(arr))  # => 8
    print(arr)  # => array('i', [42, 1729, 0, 0, 0])
