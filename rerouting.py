class Router:
    buffer = []
    servers = []

    @classmethod
    def link(cls, server):
        if server not in cls.servers:
            cls.servers.append(server)
            print(f'---Добавляю сервер {server.get_ip()}---')
            server.router_buffer = cls.buffer

    @classmethod
    def unlink(cls, server):
        if server in cls.servers:
            del cls.servers[cls.servers.index(server)]
            print(f'---Удаляю сервер {server.get_ip()}---')

    @classmethod
    def send_data(cls):
        for i in cls.buffer:
            for j in cls.servers:
                if i.ip == j.get_ip():
                    j.buffer.append(i)
                    print(f'---Отправляем данные по адресу {i.ip} серверу {j.get_ip()}---')
        print('---Очистка буфера---')
        cls.buffer.clear()


class Server:
    ip = 0
    buffer = []

    def __new__(cls, *args, **kwargs):
        cls.ip += 1
        return super().__new__(cls)

    def __init__(self):
        self.ip = self.ip
        self.buffer = []

    def get_ip(self):
        return self.ip

    def send_data(self, data):
        print(f'---Произвожу отправку данных из {self.ip} по адресу {data.ip}, передача в маршрутизатор---')
        self.router_buffer.append(data)



    def get_data(self):
        return self.buffer

class Data:
    def __init__(self, data, ip):
        self.data = data
        self.ip = ip

router = Router()
sv_from = Server()
router.link(sv_from)
router.link(Server())
router.link(Server())
sv_to = Server()
router.link(sv_to)
sv_from.send_data(Data("Hello", sv_to.get_ip()))
router.send_data()
sv_to.send_data(Data("Hi", sv_from.get_ip()))
router.send_data()
msg_lst_from = sv_from.get_data()
msg_lst_to = sv_to.get_data()

assert msg_lst_from[0].data == "Hi" and msg_lst_to[0].data == "Hello", "данные не прошли по сети, классы не функционируют должным образом"

print(msg_lst_to[0].data)
print(msg_lst_from[0].data)