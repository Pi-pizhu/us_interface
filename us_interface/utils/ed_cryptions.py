import base64


def ed_cryptions(data, data_type="base64", action_type="ec"):
    if action_type == "ec":
        return _encryptions(data, data_type)
    elif action_type == "dc":
        return _decryption(data, data_type)


def _encryptions(data, data_type="base64"):
    # 加密
    if data_type == "baset64":
        return _ec_base64(data)
    elif data_type == "xx":
        pass


def _decryption(data, data_type="base64"):
    # 解密
    if data_type == "base64":
        pass


def _ec_base64(data):
    return base64.b32encode(data)