erial Login: Ubuntu Host → Raspberry Pi Zero 2 W via CH340

Personal notes for getting a serial console working over a WCH CH340 USB-UART adapter.

## Hardware
- Host: Ubuntu machine
- Adapter: WCH CH340 USB-to-serial
- Target: Raspberry Pi Zero 2 W

## 1. Install the patched CH340 driver

The stock `ch341` driver in the kernel was broken for my adapter. Use the patched `ch34x` driver instead.

Download and unzip the patched driver repository, then:

```bash
# cd into the unzipped patched-driver directory
make clean
make
sudo make load

# Remove the broken stock driver
sudo rmmod ch341

# Confirm which ch34* modules are loaded
lsmod | grep ch34
```

Unplug and replug the CH340, then check the kernel log:

```bash
dmesg | tail
```

Expected output — note `ch34x` (not `ch341`):

```
[ xxx ] ch34x ttyUSB0: ch34x converter now attached to ttyUSB0
```

## 2. Grant serial-port access

Replace `$username` with your login (or just use `$USER`):

```bash
sudo usermod -a -G dialout $USER     # log out/in for this to take effect
sudo chmod a+rw /dev/ttyUSB0
```

If the device enumerates as something other than `ttyUSB0`, find it with:

```bash
ls /dev/ttyUSB*
```

## 3. Open the serial console

```bash
sudo screen /dev/ttyUSB0 115200
```

Exit `screen`: `Ctrl-A` then `K`, confirm with `y`.

## Troubleshooting

- **No `/dev/ttyUSB*` after plug-in** → run `sudo dmesg` to see what the kernel saw.
- **Stuck on the stock driver** → re-run `sudo rmmod ch341` and `sudo make load`.
- **Permission denied on the port** → re-check `dialout` group membership with `groups`, and the `chmod` on the device node.
- **Garbled output** → confirm the baud rate matches what the Pi expects (usually `115200`).

## Quick reference

| Step                | Command                             |
|---------------------|-------------------------------------|
| Verify port         | `ls /dev/ttyUSB*`                   |
| Inspect kernel log  | `sudo dmesg` / `dmesg \| tail`      |
| List loaded modules | `lsmod \| grep ch34`                |
| Open serial console | `sudo screen /dev/ttyUSB0 115200`   |
| Exit `screen`       | `Ctrl-A`, then `K`, then `y`        |

