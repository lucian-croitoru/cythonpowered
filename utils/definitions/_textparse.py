from utils.definitions._base import BaseFunctionDefinition, REPLACEMENT
import re as py_re
import cythonpowered.textparse as cy_textparse
from bs4 import BeautifulSoup


# ------------------------------------------------------------------
def py_get_text(html: str, strip: bool = False):
    return BeautifulSoup(html, "lxml").get_text(strip=strip)


def py_get_attr(html: str, tag: str, attr: str):
    soup = BeautifulSoup(html, "lxml")
    element = soup.find(tag)
    if element:
        return element.get(attr)
    return None


def py_get_ips(text):
    pattern = r"(?<![.\d])(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})(?![.\d])"
    matches = py_re.findall(pattern, text)
    return [ip for ip in matches if all(0 <= int(o) <= 255 for o in ip.split("."))]


def py_get_emails(text):
    pattern = r"[\w.+-]+@[\w.-]+\.\w{2,}"
    return py_re.findall(pattern, text)


def py_get_mac_addrs(text):
    pattern = r"[0-9A-Fa-f]{2}[:-][0-9A-Fa-f]{2}[:-][0-9A-Fa-f]{2}[:-][0-9A-Fa-f]{2}[:-][0-9A-Fa-f]{2}[:-][0-9A-Fa-f]{2}"
    return py_re.findall(pattern, text)


# ------------------------------------------------------------------
class PythonGetTextDef(BaseFunctionDefinition):
    function = py_get_text
    reference = "BeautifulSoup().get_text()"


class CythonGetTextDef(BaseFunctionDefinition):
    function = cy_textparse.get_text
    reference = "cythonpowered.textparse.get_text()"
    usage = REPLACEMENT


# ------------------------------------------------------------------
class PythonGetAttrDef(BaseFunctionDefinition):
    function = py_get_attr
    reference = "BeautifulSoup().find().get()"


class CythonGetAttrDef(BaseFunctionDefinition):
    function = cy_textparse.get_attr
    reference = "cythonpowered.textparse.get_attr()"
    usage = REPLACEMENT


class PythonExtractIpsDef(BaseFunctionDefinition):
    function = py_get_ips
    reference = "re.findall(...) implementation to get IPs"


class CythonExtractIpsDef(BaseFunctionDefinition):
    function = cy_textparse.get_ips
    reference = "cythonpowered.textparse.get_ips()"
    usage = REPLACEMENT


class PythonExtractEmailsDef(BaseFunctionDefinition):
    function = py_get_emails
    reference = "re.findall(...) implementation to get emails"


class CythonExtractEmailsDef(BaseFunctionDefinition):
    function = cy_textparse.get_emails
    reference = "cythonpowered.textparse.get_emails()"
    usage = REPLACEMENT


class PythonExtractMacAddrsDef(BaseFunctionDefinition):
    function = py_get_mac_addrs
    reference = "re.findall(...) implementation to get MACs"


class CythonExtractMacAddrsDef(BaseFunctionDefinition):
    function = cy_textparse.get_mac_addrs
    reference = "cythonpowered.textparse.get_mac_addrs()"
    usage = REPLACEMENT


TEXTPARSE_DEFINITION_PAIRS = [
    [PythonGetTextDef, CythonGetTextDef],
    [PythonGetAttrDef, CythonGetAttrDef],
    [PythonExtractIpsDef, CythonExtractIpsDef],
    [PythonExtractEmailsDef, CythonExtractEmailsDef],
    [PythonExtractMacAddrsDef, CythonExtractMacAddrsDef],
]
