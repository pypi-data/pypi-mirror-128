# FTP Forward Chaining Server

<badges>[![version](https://img.shields.io/pypi/v/ftpfcs.svg)](https://pypi.org/project/ftpfcs/)
[![license](https://img.shields.io/pypi/l/ftpfcs.svg)](https://pypi.org/project/ftpfcs/)
[![pyversions](https://img.shields.io/pypi/pyversions/ftpfcs.svg)](https://pypi.org/project/ftpfcs/)  
[![powered](https://img.shields.io/badge/Say-Thanks-ddddff.svg)](https://saythanks.io/to/foxe6)
[![donate](https://img.shields.io/badge/Donate-Paypal-0070ba.svg)](https://paypal.me/foxe6)
[![made](https://img.shields.io/badge/Made%20with-PyCharm-red.svg)](https://www.jetbrains.com/pycharm/)
</badges>

<i>Basically a FTP based MITM proxy that works as SFTP tunneling without SSH or an actual proxy to complete FTP traffic forward/relay. FTPFCS can be stacked to perform chaining using traditional FTP commands.</i>

# Hierarchy

```
ftpfcs
|---- FTPFCSS() # see http://pyftpdlib.readthedocs.io/ for class structure
'---- FTPFCSESS() # also see test for detailed example
```

# Example

## python
See `test`.