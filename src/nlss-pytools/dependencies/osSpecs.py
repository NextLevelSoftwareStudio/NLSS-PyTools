import platform, hashlib, os
from pathlib import Path
def OperatingSystem(completeVerification=True):
    base_path = Path.home() / "System" / "Registry"
    os_file = base_path / "OS Name.txt"
    sec_file = base_path / "OS Name Security File.txt"
    if not base_path.exists():
        base_path.mkdir(parents=True, exist_ok=True)
    if not completeVerification and os_file.exists() and sec_file.exists():
        try:
            sha = hashlib.sha256()
            with open(os_file, "rb") as f:
                while chunk := f.read(4096):
                    sha.update(chunk)
            with open(sec_file, "r", encoding="utf-8") as f:
                if sha.hexdigest() == f.read(64).strip():
                    with open(os_file, "r", encoding="utf-8") as f:
                        print(f"Sistema (Cache): {f.read().strip()}")
                    return
        except (IOError, OSError):
            pass
    res = ""
    stype = platform.system()
    if stype == "Windows":
        try:
            import winreg
            k = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion")
            prod, _ = winreg.QueryValueEx(k, "ProductName")
            bld, _ = winreg.QueryValueEx(k, "CurrentBuild")
            res = "Windows 11" if int(bld) >= 22000 and "Windows 10" in str(prod) else str(prod)
            k.Close()
        except Exception:
            res = f"Windows {platform.release()}"
    elif stype == "Linux":
        res = "Linux"
        for p in ('/etc/os-release', '/usr/lib/os-release'):
            if os.path.exists(p):
                with open(p, "r", encoding="utf-8") as f:
                    for line in f:
                        if line.startswith("PRETTY_NAME="):
                            res = line.split("=", 1)[1].strip().strip('"')
                            break
                break
    elif stype == "Darwin":
        v = platform.mac_ver()[0]
        res = f"macOS {v}" if v else "macOS"
    else:
        res = stype
    with open(os_file, "w", encoding="utf-8") as f:
        f.write(res)
    h_final = hashlib.sha256(res.encode('utf-8')).hexdigest()
    with open(sec_file, "w", encoding="utf-8") as f:
        f.write(h_final)