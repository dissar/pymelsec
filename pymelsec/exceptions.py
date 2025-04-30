"""
This file is a collection of MELSEC Communication error.
"""

# page 42 of developer guide https://dl.mitsubishielectric.com/dl/fa/document/manual/plc/sh080891eng/sh080891engs.pdf)
MC_ERROR_DETAILS = {
    # 0x4000 to 0x4FFF
    **dict.fromkeys(range(0x4000, 0x5000), {
        "description": "Errors detected by the CPU module (Errors occurred in other than MC protocol communication)",
        "action": [
            "Refer to the MELSEC-L CPU Module User's Manual (Hardware Design, Maintenance and Inspection)."
        ]
    }),
    0x0055: {
        "description": "Although online change is disabled, the connected device requested the RUN-state CPU module for data writing.",
        "action": [
            "Before enabling online change, write the data.",
            "Change the operating status of the CPU module to STOP and write the data."
        ]
    },
    0xC050: {
        "description": 'When "Communication Data Code" is set to ASCII Code, ASCII code data that cannot be converted to binary were received.',
        "action": [
            "Select Binary Code for 'Communication Data Code', and restart the CPU module.",
            "Correct the send data of the connected device and resend the data."
        ]
    },
    # 0xC051 to 0xC054
    **dict.fromkeys(range(0xC051, 0xC055), {
        "description": "The number of read or write points is outside the allowable range.",
        "action": [
            "Correct the number of read or write points.",
            "Resend the data to the CPU module."
        ]
    }),
    0xC055: {
        "description": "Although online change is disabled, the connected device requested data writing.",
        "action": [
            "Before enabling online change, write the data.",
            "Change the CPU module to STOP and write the data."
        ]
    },
    0xC056: {
        "description": "The read or write request exceeds the maximum address.",
        "action": [
            "Correct the start address or the number of read/write points.",
            "The maximum address must not be exceeded."
        ]
    },
    0xC058: {
        "description": "Request data length mismatch after ASCII-to-binary conversion.",
        "action": ["Check and correct the text or request data length."]
    },
    0xC059: {
        "description": "Command and/or subcommand are specified incorrectly.",
        "action": ["Check the request.", "Use supported command/subcommand."]
    },
    0xC05B: {
        "description": "The CPU module could not access the specified device.",
        "action": ["Check the device to be read or written."]
    },
    0xC05C: {
        "description": "The request data is incorrect (e.g. bit-to-word device mismatch).",
        "action": ["Correct the request data and resend it."]
    },
    0xC05D: {
        "description": "No monitor registration.",
        "action": ["Perform monitor registration before monitoring."]
    },
    0xC05F: {
        "description": "Request cannot be executed to the CPU module.",
        "action": [
            "Correct the network number, PC number, or module I/O/station number."
        ]
    },
    0xC060: {
        "description": "Incorrect specification of bit devices.",
        "action": ["Correct and resend the request data."]
    },
    0xC061: {
        "description": "Data length mismatch in character area.",
        "action": [
            "Check and correct the text data or request data length."
        ]
    },
    0xC06F: {
        "description": "Request sent in mismatched communication format (ASCII/Binary).",
        "action": [
            "Send request in format matching 'Communication Data Code'.",
            "Change the setting to match the request message."
        ]
    },
    0xC070: {
        "description": "Device memory extension not allowed for target station.",
        "action": [
            "Access device memory without specifying the extension."
        ]
    },
    0xC0B5: {
        "description": "The CPU module cannot handle the specified data.",
        "action": [
            "Correct the request data.",
            "Stop the current request."
        ]
    },
    0xC200: {
        "description": "The remote password is incorrect.",
        "action": [
            "Correct the remote password, then unlock and lock again."
        ]
    },
    0xC201: {
        "description": "Port is locked due to remote password.",
        "action": [
            "Unlock the remote password before communication."
        ]
    },
    0xC204: {
        "description": "Unlock request came from a different device.",
        "action": [
            "Retry lock processing from the original requesting device."
        ]
    }
}

class MCError(Exception):
    """
    Device code error

    Attributes:
        plc_type(str):      PLC type. "Q", "L" or "iQ"
        devicename(str):    devicename. (ex: "Q", "P", both of them does not support mcprotocol.)
    """

    def __init__(self, errorcode: int) -> None:
        # self.errorcode =  f'0x{str(errorcode).rjust(4, "0").upper()}'
        self.errorcode = errorcode

    def errorcode_as_hex(self) -> str:
        return f'0x{str(self.errorcode).rjust(4, "0").upper()}'

    def __str__(self):
        entry = MC_ERROR_DETAILS.get(self.errorcode, None)
        if entry is None:
            return f'Unknown error code: {self.errorcode_as_hex()}'
        else:
            description = entry["description"]
            action = "\n".join(entry["action"])
            return f'{self.errorcode_as_hex()}\nDescription: {description}\nAction: {action}'


class DataTypeError(Exception):
    """
    This data type is not supported by the module you connected.
    """
    def __init__(self, message:str):
        self.msg = message

    def __str__(self):
        return f'{self.msg}'


class DeviceCodeError(Exception):
    """
    Device code error: device does not exist.

    Attributes:
        plc_type(str):      PLC type. "Q", "L", "QnA", "iQ-L", "iQ-R", 
        devicename(str):    devicename. (ex: "Q", "P", both of them does not support mcprotocol.)

    """
    def __init__(self, plc_type:str, devicename:str):
        self.plc_type = plc_type
        self.devicename = devicename

    def __str__(self):
        error_txt = (f'devicename: "{self.devicename}" is not support "{self.plc_type}" series PLC. '
                    'If you enter hexadecimal device(X, Y, B, W, SB, SW, DX, DY, ZR) with only alphabet number '
                    '(such as XFFF, device name is "X", device number is "FFF"),'
                    'please insert 0 between device name and device number (e.g. XFFF → X0FFF)'
                    )
        return error_txt


class CommTypeError(Exception):
    """
    Communication type error. Communication type must be "binary" or "ascii"
    """
    def __init__(self):
        pass

    def __str__(self):
        return 'communication type must be "binary" or "ascii"'


class PLCTypeError(Exception):
    """
    PLC type error. PLC type must be"Q", "L", "QnA", "iQ-L", "iQ-R"
    """
    def __init__(self):
        pass

    def __str__(self):
        return 'PLC type must be "Q", "L", "QnA" "iQ-L" or "iQ-R"'
