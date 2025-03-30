class EthernetFrame:
    def __init__(
        self,
        destination_mac='empty',
        source_mac='empty',
        destination_ip='empty',
        source_ip='empty',
        destination_port=0,
        source_port=0,
        data='empty',
        is_encrypted=False,
        sequence_number=(0, 0)
    ):
        self.preamble = 'incoming'
        self.destination_mac = destination_mac
        self.source_mac = source_mac
        self.destination_ip = destination_ip
        self.source_ip = source_ip
        self.source_port = source_port
        self.destination_port = destination_port
        self.data = data
        self.is_encrypted = is_encrypted
        self.sequence_number = sequence_number
        
        print(f"[NIC] 📦 Frame #{self.sequence_number[0]+1}/{self.sequence_number[1]} CREATED")
        print(f"      From {self.source_ip} ({self.source_mac})")
        print(f"      To   {self.destination_ip} ({self.destination_mac})")
        print(f"      Ports: {self.source_port} -> {self.destination_port}")
        print(f"      Encrypted: {self.is_encrypted} | Data: {self.data}\n")

    def __repr__(self):
        return (f"<EthernetFrame #{self.sequence_number[0]+1}/{self.sequence_number[1]} "
                f"from {self.source_ip}:{self.source_port} to {self.destination_ip}:{self.destination_port} "
                f"| Data: {self.data} | Encrypted: {self.is_encrypted}>")


class Computer:
    def __init__(self, mac_address, ip_address, port):
        self.mac = mac_address
        self.ip = ip_address
        self.port = port
        self.received_frames = {}  # key: (src_ip, dest_ip), value: list of frames
        print(f"[BOOT] 💻 Computer initialized: {self.ip} ({self.mac}) on port {self.port}\n")

    def encrypt(self, data):
        print(f"[ENCRYPT] 🔐 Encrypting chunk: {data} -> {data[::-1]}")
        return data[::-1]

    def decrypt(self, data):
        print(f"[DECRYPT] 🔓 Decrypting chunk: {data} -> {data[::-1]}")
        return data[::-1]

    def send_data(self, destination_computer, data, encrypt=False):
        print(f"\n[SEND] 💬 Computer {self.ip} preparing to send data to {destination_computer.ip}")
        print(f"       Raw Data: '{data}'")
        print(f"       Encryption Enabled: {encrypt}")

        chunks = [data[i:i+2] for i in range(0, len(data), 2)]
        total_packets = len(chunks)
        print(f"[CHUNK] ✂️ Data split into {total_packets} chunks of 2 characters each\n")

        frames = []

        for i, chunk in enumerate(chunks):
            if encrypt:
                chunk = self.encrypt(chunk)

            frame = EthernetFrame(
                destination_mac=destination_computer.mac,
                source_mac=self.mac,
                destination_ip=destination_computer.ip,
                source_ip=self.ip,
                source_port=self.port,
                destination_port=destination_computer.port,
                data=chunk,
                is_encrypted=encrypt,
                sequence_number=(i, total_packets)
            )
            frames.append(frame)

        print(f"[TRANSMIT] 🚀 Sending {total_packets} frames to destination...\n")
        for frame in frames:
            destination_computer.receive_frame(frame)

        return frames

    def receive_frame(self, frame):
        print(f"[RECEIVE] 📥 Computer {self.ip} received a frame:")
        print(f"          To MAC: {frame.destination_mac} | My MAC: {self.mac}")
        print(f"          To IP:  {frame.destination_ip} | My IP:  {self.ip}")

        # Check if frame is for this device
        if frame.destination_mac != self.mac or frame.destination_ip != self.ip:
            print(f"❌ [DROP] This frame is NOT for me. Destroying: {frame}\n")
            return

        print(f"✅ [ACCEPT] Frame accepted. Processing data...\n")

        key = (frame.source_ip, frame.destination_ip)
        if key not in self.received_frames:
            self.received_frames[key] = [None] * frame.sequence_number[1]

        self.received_frames[key][frame.sequence_number[0]] = frame

        # Check if all frames are received
        if all(f is not None for f in self.received_frames[key]):
            print(f"[ASSEMBLE] 🔄 All {frame.sequence_number[1]} frames received from {frame.source_ip}")
            print(f"[ASSEMBLE] Reassembling data...\n")

            full_data = ''.join(
                self.decrypt(f.data) if f.is_encrypted else f.data
                for f in self.received_frames[key]
            )

            print(f"[OUTPUT] ✅ Final reassembled message at {self.ip}:")
            print(f"         📦 Message: '{full_data}'\n")

            del self.received_frames[key]  # Clear after reassembly
