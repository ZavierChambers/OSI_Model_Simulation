# 🧠 Network Frame Simulator | NIC-to-NIC Packet Simulation

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux-lightgrey)

> A Python-based network simulation tool that breaks data into Ethernet frames, routes it from one computer to another, drops invalid packets, and reassembles messages – complete with encryption and full verbose logging.  
> Built by **IT Guy** for cybersecurity, OSI model education, and low-level network simulation fun.

---

## 🚀 Features

- 📦 Ethernet frame simulation with MAC/IP headers
- 🔐 Optional symmetric encryption (reversible)
- ✂️ Auto-splits data into 2-character chunks (frame fragmentation)
- 💻 Computer-to-Computer message sending
- ❌ Automatic packet filtering (wrong MAC/IP is rejected)
- 🔄 Reassembly of full message once all frames are received
- 🖨️ Super verbose logs for every action (create, send, drop, receive, decrypt)

---

## 🧰 Requirements

- Python 3.10+
- No external libraries needed — runs fully on built-in Python

---

## 🧠 How It Works

1. You create two or more `Computer` instances with their MAC, IP, and Port.
2. When `send_data()` is called:
   - The message is broken into 2-character chunks.
   - Each chunk is turned into an `EthernetFrame` with a sequence number.
   - Frames are "sent" to another computer (via direct method calls).
3. The receiving computer checks:
   - If the frame is for its MAC & IP.
   - If it is, it stores the frame.
   - Once all frames arrive, it reassembles the message and decrypts if needed.
   - If the frame is not for it, it drops the packet.

## 🧪 Example Usage

```python
from network_sim import Computer

# Create sender and receiver
computer_A = Computer(mac_address="11:22:33:44:55:66", ip_address="192.168.1.10", port=1234)
computer_B = Computer(mac_address="AA:BB:CC:DD:EE:FF", ip_address="192.168.1.20", port=80)

# Send encrypted data from A to B
computer_A.send_data(destination_computer=computer_B, data="This is top secret!", encrypt=True)
✅ Output (Example)
css
Copy
Edit
[NIC] 📦 Frame #1/10 CREATED
[TRANSMIT] 🚀 Sending 10 frames to destination...
[RECEIVE] 📥 Computer 192.168.1.20 received a frame...
✅ [ACCEPT] Frame accepted. Processing...
[ASSEMBLE] 🔄 All 10 frames received from 192.168.1.10
[OUTPUT] ✅ Final reassembled message: This is top secret!
🔐 Encryption Info
This simulator uses a basic symmetric encryption model (string reversal) for educational purposes:

Encrypt: "hi" → "ih"

Decrypt: "ih" → "hi"

🔍 Roadmap
 Basic frame simulation

 Fragmentation & sequencing

 Packet filtering logic

 Message reassembly

 Simple encryption & decryption

 GUI Interface with network visualization 🎛️

 Packet loss + retransmission 💥

 Switch/router simulation 🌐

 Support for broadcasting/multicast

📜 License
Licensed under the MIT License.
Feel free to fork, modify, and learn from it!

🧑‍💻 Author
Built by IT Guy
For learning how real NICs, Ethernet, and low-level data transmission work 🚀
Use it to practice cybersecurity, networking fundamentals, or build your own Wireshark-inspired toy.

yaml
Copy
Edit

---

Let me know if you want:
- A matching `LICENSE` file
- A `.gitignore` for Python
- A logo/banner to top off your repo

Let’s make this repo pop on GitHub, IT Guy 🚀🖥️
