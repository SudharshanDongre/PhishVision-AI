import re
import socket
import requests
import whois
from datetime import datetime
from urllib.parse import urlparse
from bs4 import BeautifulSoup

# 1. Check if URL uses an IP address
def have_ip(url):
    match = re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', url)
    return 1 if match else 0

# 2. Check if URL has @ symbol
def have_at(url):
    return 1 if "@" in url else 0

# 3. URL Length
def get_length(url):
    return 0 if len(url) < 54 else 1

# 4. URL Depth (number of / in path)
def get_depth(url):
    path = urlparse(url).path
    depth = path.count('/')
    return depth if depth > 0 else 1  # minimum depth of 1

# 5. Redirection using //
def redirection(url):
    path = urlparse(url).path
    return 1 if '//' in path else 0

# 6. https in domain name
def https_domain(url):
    domain = urlparse(url).netloc
    return 1 if 'https' in domain else 0

# 7. Tiny URL
shorteners = ['bit.ly','goo.gl','tinyurl.com','ow.ly','t.co','is.gd','buff.ly']
def tiny_url(url):
    for s in shorteners:
        if s in url:
            return 1
    return 0

# 8. Prefix or Suffix (- in domain)
def prefix_suffix(url):
    domain = urlparse(url).netloc
    return 1 if '-' in domain else 0

# 9. DNS Record
def dns_record(url):
    domain = urlparse(url).netloc
    try:
        socket.getaddrinfo(domain, None)
        return 0
    except:
        return 1

# 10. Web Traffic (simplified)
def web_traffic(url):
    try:
        domain = urlparse(url).netloc
        # If DNS resolves, assume it has traffic
        socket.getaddrinfo(domain, None)
        return 1
    except:
        return 0
    
# 11. Domain Age
def domain_age(url):
    try:
        domain = urlparse(url).netloc
        # Remove www. prefix
        if domain.startswith("www."):
            domain = domain[4:]
        w = whois.whois(domain)
        creation = w.creation_date
        if isinstance(creation, list):
            creation = creation[0]
        if creation is None:
            return 0
        age = (datetime.now() - creation).days
        return 1 if age >= 180 else 0
    except:
        return 1  # If whois fails, assume old domain (safe default)
    
# 12. Domain End (expiry)
def domain_end(url):
    try:
        domain = urlparse(url).netloc
        w = whois.whois(domain)
        expiry = w.expiration_date
        if isinstance(expiry, list): expiry = expiry[0]
        remaining = (expiry - datetime.now()).days
        return 0 if remaining < 180 else 1
    except:
        return 0

# 13. iFrame check
def iframe(response):
    try:
        return 1 if re.search(r"<iframe|<frameBorder", response.text, re.IGNORECASE) else 0
    except:
        return 0

# 14. Mouse Over check
def mouse_over(response):
    try:
        return 1 if re.search(r"onmouseover", response.text, re.IGNORECASE) else 0
    except:
        return 0

# 15. Right Click disabled
def right_click(response):
    try:
        return 1 if re.search(r"event.button==2", response.text) else 0
    except:
        return 0

# 16. Web Forwards
def forwarding(response):
    try:
        return 1 if len(response.history) > 2 else 0
    except:
        return 0

# ✅ MASTER FUNCTION — returns all 16 features
def featureExtraction(url):
    features = []
    features.append(have_ip(url))
    features.append(have_at(url))
    features.append(get_length(url))
    features.append(get_depth(url))
    features.append(redirection(url))
    features.append(https_domain(url))
    features.append(tiny_url(url))
    features.append(prefix_suffix(url))
    features.append(dns_record(url))
    features.append(web_traffic(url))
    features.append(domain_age(url))
    features.append(domain_end(url))

    try:
        response = requests.get(url, timeout=5)
    except:
        response = None

    features.append(iframe(response) if response else 0)
    features.append(mouse_over(response) if response else 0)
    features.append(right_click(response) if response else 0)
    features.append(forwarding(response) if response else 0)

    return features