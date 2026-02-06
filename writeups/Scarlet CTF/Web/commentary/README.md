# **Commentary**

> This write-up documents a deliberately vulnerable lab / CTF-style service.  
> All techniques are presented for educational purposes only.

------

## Overview

- **Category**: Web / Commentary  
- **Difficulty**: Easy  
- **Key Concept**: Reverse Proxy, OSI Layer separation, ICMP  
- **Goal**: Discover the real backend IP and access forgotten content

------

## Challenge Description

> You're currently speaking to my favorite host right now (ctf.rusec.club),  
> but who's to say you even had to speak with one?  
>
> Sometimes, the treasure to be found is just bloat that people forgot to remove.

---

### 1.Analysis

The challenge provides a public domain, `ctf.rusec.club`, which responds normally over HTTP.
The service appears to be a standard web application with no obvious input points or user interaction.

The challenge description repeatedly references the concept of a "host", suggesting that the
HTTP `Host` header may be significant.

Additionally, the phrase *"who's to say you even had to speak with one"* implies that interacting
with the service through HTTP may not be strictly required.

Since HTTP reverse proxies operate at the application layer (Layer 7), this suggests that
lower-layer protocols, such as ICMP, may behave differently and bypass the proxy entirely.

### 2. Exploitation

The `ping` command operates at **OSI Layer 3** using the **ICMP** protocol, while reverse proxies
operate at **Layer 7** and only handle HTTP traffic. As a result, ICMP traffic is not processed
by the reverse proxy.

To identify the real backend IP address, ICMP was used:

```shell
ping ctf.rusec.club
```

outcome:
	5.161.91.13

We connecting address.
The page displays the default Nginx welcome page.indicating that the backend server is accessible
and that the default configuration was left exposed.

![](image/img1.png)

Inspecting the page source of the default Nginx site reveals hidden HTML comments:

```html
<!-- you found me :3 -->
<!-- RUSEC{truly_the_hardest_ctf_challenge} -->
```

## Key Takeaways

- Reverse proxies only handle **application-layer protocols** such as HTTP
- ICMP traffic bypasses Layer 7 protections entirely
- Direct IP access may expose forgotten default configurations
- Understanding protocol layers is often more important than exploiting vulnerabilities



## References

- OSI Model
- ICMP (Internet Control Message Protocol)

- Nginx Reverse Proxy behavior

