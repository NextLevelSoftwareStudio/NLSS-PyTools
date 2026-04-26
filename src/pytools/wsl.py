import subprocess, osSpecs
def check():
    if osSpecs.OperatingSystem().startswith("Windows"):
        try:
            if subprocess.check_output("powershell -c (Get-ComputerInfo).HypervisorPresent", shell=True).decode().strip() != "True":
                return False
            ps = "Get-WindowsOptionalFeature -Online|Where-Object {$_.FeatureName -match 'Microsoft-Windows-Subsystem-Linux|VirtualMachinePlatform'}|ForEach-Object {$_.State}"
            f = subprocess.run(["powershell", "-c", ps], capture_output=True, text=True).stdout.splitlines()
            if len([s for s in f if "Enabled" in s]) < 2:
                return False
            return subprocess.run("wsl --status", capture_output=True, shell=True).returncode == 0
        except:
            return False
    else:
        return False
def install():
    if osSpecs.OperatingSystem().startswith("Windows"):
        try:
            subprocess.run("powershell -c Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux -NoRestart", shell=True, check=True)
            subprocess.run("powershell -c Enable-WindowsOptionalFeature -Online -FeatureName VirtualMachinePlatform -NoRestart", shell=True, check=True)
            print("Please restart your computer to complete the WSL installation.")
        except subprocess.CalledProcessError as e:
            print(f"Error installing WSL: {e}")
    else:
        print("WSL is not supported on this operating system.")
def uninstall():
    if osSpecs.OperatingSystem().startswith("Windows"):
        try:
            command1 = "wsl --list --quiet | ForEach-Object { wsl --unregister $_.Trim() }"
            command2 = "Get-AppxPackage -allusers *WindowsSubsystemforLinux* | Remove-AppxPackage -AllUsers"
            command3 = "Disable-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux -NoRestart"
            command4 = "Disable-WindowsOptionalFeature -Online -FeatureName VirtualMachinePlatform -NoRestart"
            subprocess.run(["powershell", "-c", command1], shell=True, check=True)
            subprocess.run(["powershell", "-c", command2], shell=True, check=True)
            subprocess.run(["powershell", "-c", command3], shell=True, check=True)
            subprocess.run(["powershell", "-c", command4], shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error uninstalling WSL: {e}")
    else:
        print("WSL is not supported on this operating system.")