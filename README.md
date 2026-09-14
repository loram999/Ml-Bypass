# ML Checker Pro

Premium MLBB Device ID Checker with F CHECK and ALL CHECK modes.

## Features

- **F CHECK** - Login-only check using generated Device IDs. Saves hits on successful login.
- **ALL CHECK** - Full info pull: login + game server + player data (nickname, level, skins, heroes, rank, V2L, Moonton, 3rd party, offline time, collector level).
- **Live Terminal** - Real-time device checking logs with rank/collector status.
- **Auto Save** - All hits automatically saved to categorized folders.
- **Bot / File Management** - Upload, browse, and manage device ID files.
- **Device Generator** - Generate device IDs with OEM A/B/C/D/MIX modes (8 real formats).

## Requirements

```bash
pip install -r requirements.txt
```

## Usage

```bash
python3 main.py
```

## Menu

```
[1] F CHECK       - Login only → Save on HIT
[2] ALL CHECK     - Full info → Auto Save
[3] GENERATOR     - Device ID generator
[4] HITS BROWSER  - View/Send hits
[5] BOT / FILES   - Upload & manage
[0] EXIT
```

## Output

All results saved in `ML_CHECKER_OUTPUT/`:
- `01_F_Check_Hits/` - F Check results
- `02_All_Check/` - All Check full info
- `04-10_Rank_*/` - Rank categorized hits
- `11_V2L_Active/`, `12_V2L_Inactive/`
- `13_Sultan/` - 200+ skin accounts
- `14_Collector/` - Collector level accounts

## Note

This tool is for educational purposes only. Use responsibly.
