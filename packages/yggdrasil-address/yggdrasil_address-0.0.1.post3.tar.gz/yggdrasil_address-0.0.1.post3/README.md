# Yggdrasil address converter

Simple yggdrasil public key to IPv6 converter and vice versa.

# Quick start
```python
import yggdrasil_address as ygg_addr

key = ygg_addr.generate_sign_key()
pk = ygg_addr.pk2ip(key)
ip = ygg_addr.ip2pk(pk)

print('IPv6:', ip, 'public key:', pk)
```