# Simple-Wake-on-LAN
Wake up your hosts by sending a "magic packet" in Python!

# Usage
```
python3 wakeup.py -h
options:
  -h, --help            show this help message and exit
  -l, --list            list all hosts from config.yaml
  -n NAME, --name NAME  alias of the host (must be inserted into config.yaml before!)
  -m MAC, --mac MAC     mac address
```

# Examples
`python3 wakeup.py -n alias1`
`python3 wakeup.py -m "00.00.00.00.00.00"`
`python3 wakeup.py -l`

# config.yaml
In this file, you can define some aliases for an alias <-> mac-address translation... because it's easier to remember names instead of mac addresses ;)
You can also specify the outgoing interface by setting the corresponding ip address in config.yaml.

# General information
Don't forget, to activate wake-on-lan in your BIOS and/or operation system respectively. I can't provide information about this since it depends on your NIC, operation system and/or BIOS (and maybe more?). 

# IPv6 Support? 
Feel free to contribute and send pull requests! :)
