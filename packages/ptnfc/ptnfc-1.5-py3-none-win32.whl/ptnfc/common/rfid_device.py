import time
from ctypes import CDLL, create_string_buffer
from . import Get_Com_Dict

MAX_BLOCK_NUMBER = 256
ONCE_READ_MAX_BLOCK_NUMBER = 15
FunctionReturnErrorCodes = {
        1: "波特率错误",
        2: "串口号错误或者连接断开",
        10: "通用错误",
        11: "不支持该命令",
        12: "指令参数错误",
        13: "无卡",
        20: "寻卡失败",
        21: "卡复位错误",
        22: "卡密钥验证错误",
        23: "读卡错误",
        24: "写卡错误",
        25: "写地址错误",
        26: "读地址错误"
    }


# 根据操作系统读取对应的DLL库
def Get_Reader_Dll() -> CDLL:
    import platform
    import os
    dir = os.path.dirname(os.path.abspath(__file__))
    os_bit, os_name = platform.architecture()
    if os_bit == '32bit':
        return CDLL(f'{dir}/32/MasterRD.dll')
    elif os_bit == '64bit':
        return CDLL(f'{dir}/64/MasterRD.dll')
    else:
        raise TypeError(f"Don't supported os-bit : {os_bit}")


class RFIDComPort:

    def __init__(self, comIndex, baudrate):
        self.dll = Get_Reader_Dll()
        self.comIndex = comIndex
        self.baudrate = baudrate

        r, msg = self.init_com()
        if not r:
            raise Exception(msg)

        # 初始化端口成功

    def init_com(self) -> (bool, str):
        """初始化对应的串口"""
        r = self.dll.rf_init_com(self.comIndex, self.baudrate)
        return r == 0, f"InitCom success: [COM{self.comIndex}], [Baudrate: {self.baudrate}]." if r == 0 else\
            f"InitCom failure: [COM{self.comIndex}], [Baudrate: {self.baudrate}], [Reason: {FunctionReturnErrorCodes.get(r)}]."

    def close_com(self) -> (bool, str):
        """关闭对应的串口"""
        r = self.dll.rf_ClosePort()
        return r == 0, f"CloseCom success: [COM{self.comIndex}]." if r == 0 else\
            f"CloseCom failure: [COM{self.comIndex}], [Reason: {FunctionReturnErrorCodes.get(r)}]."

    def init_type(self, rtype) -> (bool, str):
        """
        设置读写卡器非接触工作方式

        :param rtype: 读写卡器工作方式
                    ['A': 设置为TYPE_A方式,
                    'B': 设置为TYPE_B方式,
                    'r': 设置为AT88RF020方式,
                    '1': 设置为ISO15693方式]
        """
        r = self.dll.rf_init_type(0, rtype)
        return r == 0, f"Init_type success: [COM{self.comIndex}], [Type: {rtype}]." if r == 0 else\
            f"Init_type failure: [COM{self.comIndex}], [Type: {rtype}], [Reason: {FunctionReturnErrorCodes.get(r)}]."

    def beep(self, ms) -> None:
        """
        控制蜂鸣器响

        :param ms: 鸣响时长，单位：ms
        """
        t = ms / 10
        # 接口蜂鸣器时长单位为 10ms
        self.dll.rf_beep(0, int(t))

    def _light(self, color):
        self.dll.rf_light(0, color)

    def on_green_light(self):
        """LED打开绿灯"""
        self._light(0)
        self._light(2)

    def on_red_light(self):
        """LED打开红灯"""
        self._light(0)
        self._light(1)

    def off_light(self):
        """关闭LED指示灯"""
        self._light(0)

    def ISO15693_Inventory(self):
        pData = create_string_buffer(9)
        pLen = create_string_buffer(1)
        r = self.dll.ISO15693_Inventory(0, pData, pLen)
        return r == 0, pData.raw

    def ISO15693_Read(self, pUid, block, number) -> (bool, bytes):
        pData = create_string_buffer(number * 4)
        pLen = create_string_buffer(1)
        r = self.dll.ISO15693_Read(0, 2, pUid, block, number, pData, pLen)
        size = int(pLen.raw.hex(), 16)
        return r == 0, pData.raw[:size], size


class ISO15693ComPort(RFIDComPort):

    def __init__(self, comIndex, baudrate):
        RFIDComPort.__init__(self, comIndex, baudrate)
        r, msg = self.init_type(None)
        if not r:
            raise Exception(msg)

    def init_type(self, rtype) -> (bool, str):
        rtype = 0x31
        return RFIDComPort.init_type(self, rtype)

    def find_card(self):
        r, data = self.ISO15693_Inventory()
        if not r:
            raise Exception(FunctionReturnErrorCodes.get(r, "未知错误"))

        dsfid, uid = data[0], data[1:]
        return dsfid, uid

    def read(self, uid, block, number):
        pUid = _create_pUid(uid)
        return self.ISO15693_Read(pUid, block, number)

    def read_all(self, uid, timeout=10):
        pUid = _create_pUid(uid)
        block = 0
        data = b''
        time_start = time.time()

        while block < MAX_BLOCK_NUMBER:
            read_block_num = ONCE_READ_MAX_BLOCK_NUMBER if block + ONCE_READ_MAX_BLOCK_NUMBER <= MAX_BLOCK_NUMBER - 1 else MAX_BLOCK_NUMBER - block
            r, d, l = self.ISO15693_Read(pUid, block, read_block_num)
            if r:
                block = block + ONCE_READ_MAX_BLOCK_NUMBER
                data = data + d
                if l < read_block_num * 4:
                    break
            else:
                time.sleep(0.1)

            time_duration = time.time() - time_start
            if time_duration > timeout:
                raise TimeoutError(f"Read all already timeout.[Block: {block}], [Data: {data}")

        return data

    def big_recruit(self, timeout=10):
        """用于直接获取卡号及其全部信息"""
        # 记录开始时间
        start = time.time()
        # 防冲突读取卡号
        Readable = True
        dsfid = 0x00
        uid = 0
        while Readable and time.time() - start < timeout:
            r, data =self.ISO15693_Inventory()
            if r:
                self.beep(50)
                self.on_green_light()
                dsfid, uid = data[0], data[1:]
                self.on_red_light()
                Readable = False

        if Readable:
            raise TimeoutError("Big recruit already timeout.")

        # 根据卡号读取所有信息
        timeout = timeout - (time.time() - start)
        data = self.read_all(uid, timeout)
        return uid, data


def _create_pUid(uid):
    if isinstance(uid, bytes):
        if len(uid) != 8:
            raise TypeError(f"Uid must 8 bytes. {uid}")
        return create_string_buffer(uid)
    elif isinstance(uid, str):
        int(uid, 16)
        if len(uid) != 16:
            raise TypeError(f"Uid must 8 bytes. {uid}")
        return create_string_buffer(bytes.fromhex(uid))


def Find_usb_comport(usbIndex:str) -> ISO15693ComPort:
    com_dict = Get_Com_Dict()
    if usbIndex in com_dict:
        com = com_dict[usbIndex]
        comIndex = int(com.replace('COM', ''))
        return ISO15693ComPort(comIndex, 115200)
    else:
        raise Exception(f"The specified USB serial port was not found. [usbIndex: {usbIndex}]")

def Find_comport(comIndex) -> ISO15693ComPort:
    return ISO15693ComPort(int(comIndex), 115200)
