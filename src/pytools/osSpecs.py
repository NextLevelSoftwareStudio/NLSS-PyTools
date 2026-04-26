import platform
import os

def OperatingSystem(verbose=False):
    res = "Unknown System"
    stype = platform.system()
    
    if verbose:
        print(f"[Verbose] Plataforma detectada: {stype}")

    # --- WINDOWS (Formato: Windows 11 Pro) ---
    if stype == "Windows":
        try:
            import winreg
            path = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion"
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path, 0, winreg.KEY_READ) as k:
                prod_name, _ = winreg.QueryValueEx(k, "ProductName")
                build, _ = winreg.QueryValueEx(k, "CurrentBuild")
                try:
                    edition, _ = winreg.QueryValueEx(k, "EditionID")
                    # Padroniza "Professional" para "Pro"
                    edition = edition.replace("Professional", "Pro")
                except:
                    edition = ""

                if verbose:
                    print(f"[Verbose] Registro Windows - Nome: {prod_name}, Build: {build}, Edição: {edition}")

                # Lógica de correção para Windows 11
                if int(build) >= 22000:
                    if "Windows 10" in prod_name:
                        res = prod_name.replace("Windows 10", "Windows 11")
                    elif "Windows 11" not in prod_name:
                        res = f"Windows 11 {edition}".strip()
                    else:
                        res = prod_name
                else:
                    res = prod_name

                # Adiciona edição se não estiver presente na string
                if edition and edition.lower() not in res.lower():
                    res = f"{res} {edition}"
        except Exception as e:
            if verbose: print(f"[Verbose] Erro ao ler registro: {e}")
            res = f"Windows {platform.release()}"

    # --- LINUX (Sempre PRETTY_NAME) ---
    elif stype == "Linux":
        found_pretty = False
        for p in ('/etc/os-release', '/usr/lib/os-release'):
            if os.path.exists(p):
                if verbose: print(f"[Verbose] Lendo arquivo de sistema: {p}")
                try:
                    with open(p, "r", encoding="utf-8") as f:
                        for line in f:
                            if line.startswith("PRETTY_NAME="):
                                res = line.split("=", 1)[1].strip().strip('"')
                                found_pretty = True
                                break
                    if found_pretty: break
                except Exception as e:
                    if verbose: print(f"[Verbose] Erro ao ler {p}: {e}")
                    continue
        
        if not found_pretty:
            res = f"Linux {platform.release()}"

    # --- macOS (Formato: macOS <numero>) ---
    elif stype == "Darwin":
        version = platform.mac_ver()[0]
        if verbose: print(f"[Verbose] Versão Darwin detectada: {version}")
        res = f"macOS {version}" if version else "macOS"

    # --- SOLARIS ---
    elif stype == "SunOS":
        res = f"Solaris {platform.release()}"

    # --- OUTROS ---
    else:
        res = f"{stype} {platform.release()}"

    if verbose:
        print(f"[Verbose] Resultado final: {res}")
        
    return res