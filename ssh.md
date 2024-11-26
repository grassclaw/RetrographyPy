# Ensure the SSH Service (sshd) is Running

Run the following command in PowerShell to check the status of the `sshd` service:

    Get-Service sshd

If it is not running, start it:

    Start-Service sshd

### Example Outputs

    PS C:\Users\Administrator> Start-Service sshd
    PS C:\Users\Administrator> Get-Service sshd

    Status   Name               DisplayName
    ------   ----               -----------
    Running  sshd               OpenSSH SSH Server

---

# Confirm the SSH Port (22) is Listening

Use the following command to check if SSH is listening on port 22:

    netstat -an | findstr :22

### Example Outputs

    TCP    0.0.0.0:22             0.0.0.0:0              LISTENING
    TCP    [::]:22                [::]:0                 LISTENING

---

# Test Local SSH Connectivity (optional)

From within your Windows VM, test SSH locally to verify the server is responding:

    ssh Administrator@127.0.0.1

Enter the password when prompted.

> **Note**: `127.0.0.1` is a special IP address known as the localhost or loopback address. It always refers to the device you're currently using, regardless of its actual IP address on the network.
