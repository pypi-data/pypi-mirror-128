'''
Дескриптор
'''

import sys

import logging

from server.common.variables import DEFAULT_IP_ADDRESS


logger = logging.getLogger('server2')

# Инициализиция логера
# метод определения модуля, источника запуска.
if sys.argv[0].find('client') == -1:
    # если не клиент то сервер!
    logger = logging.getLogger('server2')
else:
    # ну, раз не сервер, то клиент
    logger = logging.getLogger('client')


class Port:
    '''
    Дескриптор для описания порта:
    '''

    def __set__(self, instance, value):
        if not 1023 < value < 65536:
            logger.critical(
                'Попытка запуска с указанием неподходящего '
                'порта %s', value, 'Допустимы адреса с 1024 до 65535.')
            sys.exit(1)
        instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        self.name = name


class Host:
    '''
    Дескриптор для описания хоста:
    '''

    def __set__(self, instance, value):
        value = DEFAULT_IP_ADDRESS
        host_addr_list = []
        _oct = 0
        while _oct < 4:
            host_addr = int(value.split('.')[_oct])
            host_addr_list.append(int(host_addr))
            _oct = _oct + 1
        for h in host_addr_list:
            if h > 254 or h < 0:
                logger.critical(
                    'Попытка запуска сервера с указанием неподходящего хоста %s',
                    value,
                    'Допустимы адреса с октетами не больше 254 и не меньше 0.')
                sys.exit(1)
        instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        self.name = name
