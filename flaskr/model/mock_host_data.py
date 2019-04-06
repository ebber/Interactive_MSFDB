Ports = [(22, "ssh", "sshd info", "OPEN"),
         (22, "ssh", "sshd info", "FILTERED"),
         (20, "telnet", "telnet info", "OPEN"),
         (53, "DNS", "DNS info", "OPEN"),
         (53, "DNS", "DNS info", "FILTERED"),
         (20, "telnet", "telnet info", "FILTERED"),
         (80, "HTTP", "HTTP info", "OPEN"),
         (80, "HTTP", "HTTP info", "FILTERED"),
         (443, "HTTPS", "HTTPS info", "OPEN"),
         (443, "HTTPS", "HTTPS info", "FILTERED")
        ]

OS = ["Linux", "Windows", "Cisco", "HP-UX"]


Purposes = ["Auth", "DB", "Switch", "Firewall"]

