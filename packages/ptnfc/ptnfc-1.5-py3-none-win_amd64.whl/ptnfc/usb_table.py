import usb
from enum import Enum
from typing import Callable, Dict, List, Sequence
from . import ComAddressDict


class Device:
    vendor_id = 0
    product_id = 0

    def __init__(self, bus: int, port_numbers: Sequence[int]) -> None:
        self._bus = bus
        self._port_numbers = port_numbers
        # addr is a series of ports from root to leaf in the usb device tree
        self._addr = str(self._bus) + '-' + '.'.join([str(p) for p in port_numbers])
        self._name = ''
        self._id = ''

    @classmethod
    def search_devices(cls) -> Sequence['Device']:
        if cls.product_id:
            devices = usb.core.find(find_all=all, idVendor=cls.vendor_id, idProduct=cls.product_id)
        else:
            devices = usb.core.find(find_all=all, idVendor=cls.vendor_id)
        return [cls.create(d.bus, d.port_numbers) for d in devices]

    @classmethod
    def create(cls, bus: int, port_numbers: Sequence[int]) -> 'Device':
        return Device(bus, port_numbers)

    def is_offspring_of(self, dev: 'Device') -> bool:
        return self._addr.startswith(dev._addr)

    def name(self) -> str:
        return self._name

    def my_port(self) -> int:
        return self._port_numbers[0]

    def id(self) -> str:
        return self._id

    # If a device is directly connected to a FE217 hub port, device id is the same as port id;
    # If a device is connected to a hub port through an external hub, device id is port id plus the diff of device
    # address and port address
    def set_id(self, port_id: str, port_addr: str) -> None:
        if self._addr == port_addr:
            self._id = port_id
        else:
            self._id = port_id + self._addr[len(port_addr):]


class Port:
    def __init__(self, id: str, addr: str):
        # id is a user-friendly name that helps to identify a hub port
        self._id = id
        # addr is a series of ports from root to leaf in the usb device tree
        self._addr = addr
        # There may be multiple devices when the port is connected to another hub
        self._devices: List[Device] = []

    def address(self) -> str:
        return self._addr

    def id(self) -> str:
        return self._id

    def add_device(self, dev: Device) -> None:
        self._devices.append(dev)

    def devices(self) -> List[Device]:
        return self._devices


class HubCatetory(Enum):
    UNKNOWN = 0
    PT = 1
    SP20 = 2
    SP32 = 3


class Hub(Device):
    @classmethod
    def create(cls, bus: int, port_numbers: Sequence[int]) -> 'Hub':
        return Hub(bus, port_numbers)

    def __init__(self, bus: int, port_numbers: Sequence[int]) -> None:
        super().__init__(bus, port_numbers)
        # key is hub port id
        self._ports: Dict[str, Port] = {}
        self._category = HubCatetory.UNKNOWN

    def catetory(self) -> HubCatetory:
        return self._category

    def add_device(self, dev: Device) -> None:
        for port in self._ports.values():
            if dev._addr.startswith(port.address()):
                    port.add_device(dev)
                    dev.set_id(port.id(), port.address())
                    break

    def has_subdevice(self) -> bool:
        for l in self._ports.values():
            if l: return True
        return False

    def dev_mapping(self, filter: Callable[[Device], bool]) -> Dict[str, str]:
        ret = {}
        for port in self._ports.values():
            for dev in port.devices():
                if filter(dev):
                    ret[dev.id()] = dev.name()
        return ret


class Terminus4(Hub):
    vendor_id = 0x1a40
    product_id = 0x0101

    @classmethod
    def create(cls, bus: int, port_numbers: Sequence[int]) -> 'Terminus4':
        return Terminus4(bus, port_numbers)


class FE217(Hub):
    vendor_id = 0x1a40
    product_id = 0x0201

    # Perfectek new MCU chassis port suffix
    # key is port id, id n.m means the m-th usb port of the MCU on the n-th slot,
    # suffix is port address relative to the hub address
    pt_port_suffix = {
        '1':  '1.3.1', '1.1':  '1.3.4', '1.2':  '1.3.3', '1.3':  '1.3.2',
        '2':  '1.2.1', '2.1':  '1.2.4', '2.2':  '1.2.3', '2.3':  '1.3.2',
        '3':  '1.1.1', '3.1':  '1.1.4', '3.2':  '1.1.3', '3.3':  '1.1.2',
        '4':  '1.4.1', '4.1':  '1.4.4', '4.2':  '1.4.3', '4.3':  '1.4.2',
        '5':  '2.1.1', '5.1':  '2.1.4', '5.2':  '2.1.3', '5.3':  '2.1.2',
        '6':  '2.4.1', '6.1':  '2.4.4', '6.2':  '2.4.3', '6.3':  '2.4.2',
        '7':  '2.2.1', '7.1':  '2.2.4', '7.2':  '2.2.3', '7.3':  '2.2.2',
        '8':  '2.3.1', '8.1':  '2.3.4', '8.2':  '2.3.3', '8.3':  '2.3.2',
        '9':  '6.2.1', '9.1':  '6.2.4', '9.2':  '6.2.3', '9.3':  '6.2.2',
        '10': '6.1.1', '10.1': '6.1.4', '10.2': '6.1.3', '10.3': '6.1.2',
        '11': '6.4.1', '11.1': '6.4.4', '11.2': '6.4.3', '11.3': '6.4.2',
        '12': '6.3.1', '12.1': '6.3.4', '12.2': '6.3.3', '12.3': '2.3.2',
        '13': '5.4.1', '13.1': '5.4.4', '13.2': '5.4.3', '13.3': '5.4.2',
        '14': '5.2.1', '14.1': '5.2.4', '14.2': '5.2.3', '14.3': '5.2.2',
        '15': '5.3.1', '15.1': '5.3.4', '15.2': '5.3.3', '15.3': '5.3.2',
        '16': '5.1.1', '16.1': '5.1.4', '16.2': '5.1.3', '16.3': '5.1.2',
        'F1': '4',
        'F2': '3.4',   'F3':   '3.3',   'F4':   '3.2',   'F5': '3.1'
    }

    # 20-ports Hub, key is port id
    sp20_port_suffix = {
        '1':  '7.1', '2':  '7.2',  '3':  '7.3',  '4':  '3.2',
        '5':  '3.3', '6':  '3.4',  '7':  '4.1',  '8':  '4.2',
        '9':  '4.3', '10': '4.4',  '11': '6.1',  '12': '6.2',
        '13': '6.4', '14': '2.2',  '15': '2.3',  '16': '2.4',
        '17': '1.1', '18': '1.2',  '19': '1.3',  '20': '1.4'
    }

    # 32-ports Hub, key is port id
    sp32_port_suffix = {
        '1':  '7.1',   '2':  '7.2',   '3':  '7.3',   '4':  '7.4',
        '5':  '4.1',   '6':  '4.2',   '7':  '4.3',   '8':  '4.4',
        '9':  '3.1',   '10': '3.2',   '11': '3.3',   '12': '3.4',
        '13': '2.3.1', '14': '2.3.2', '15': '2.3.3', '16': '2.3.4',
        '17': '6.1',   '18': '6.2',   '19': '6.3',   '20': '6.4',
        '21': '5.1',   '22': '5.2',   '23': '5.3',   '24': '5.4',
        '25': '1.1',   '26': '1.2',   '27': '1.3',   '28': '1.4',
        '29': '2.1.1', '30': '2.1.2', '31': '2.1.3', '32': '2.1.4'
    }

    @classmethod
    def create(cls, bus: int, port_numbers: Sequence[int]) -> 'FE217':
        fe_hub = FE217(bus, port_numbers)
        tm_hubs = Terminus4.search_devices()
        tm_hub_cnt = 0
        for h in tm_hubs:
            if h.is_offspring_of(fe_hub):
                tm_hub_cnt = tm_hub_cnt + 1
        if tm_hub_cnt == 6:
            fe_hub._category = HubCatetory.SP20
        elif tm_hub_cnt == 9:
            fe_hub._category = HubCatetory.SP32
        fe_hub.init_ports()
        return fe_hub

    def __init__(self, bus: int, port_numbers: Sequence[int]) -> None:
        super().__init__(bus, port_numbers)
        self._category = HubCatetory.PT

    def init_ports(self) -> None:
        if self._category == HubCatetory.PT:
            port_suffix = self.pt_port_suffix
        elif self._category == HubCatetory.SP20:
            port_suffix = self.sp20_port_suffix
        else:
            port_suffix = self.sp32_port_suffix

        for id, suffix in port_suffix.items():
            self._ports[id] = Port(id, self._addr + '.' + suffix)

    def comports(self, coms) -> dict:
        ret = {}
        if len(coms) == 0:
            return ret
        for port in self._ports.values():
            _id = port.id()
            _add = port.address()
            if _add in coms:
                ret[_id] = coms[_add]
        return ret


def Get_Com_Dict() -> dict:
    ret = {}
    hubs = FE217.search_devices()
    _com_dict = ComAddressDict()
    if len(hubs) > 0:
        com_hub = hubs[0]
        ret = com_hub.comports(_com_dict)
    return ret



