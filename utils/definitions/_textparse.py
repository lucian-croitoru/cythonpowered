from utils.definitions._base import BaseFunctionDefinition, REPLACEMENT
import re as py_re
import cythonpowered.textparse as cy_textparse
from bs4 import BeautifulSoup
import lxml.html
from lxml import etree


# ------------------------------------------------------------------
def py_get_text_bs4(html: str, strip: bool = False):
    return BeautifulSoup(html, "lxml").get_text(strip=strip)


def py_get_text_lxml(html: str):
    doc = lxml.html.fromstring(html)
    etree.strip_elements(doc, "script", "style", with_tail=False)
    return doc.text_content()


def py_find_bs4(html: str, tag: str, recursive: bool = True):
    found = BeautifulSoup(html, "lxml").find(tag, recursive=recursive)
    if found is not None:
        return found.decode(formatter=None)
    return found


def py_findall_bs4(html: str, tag: str, recursive: bool = True):
    found = BeautifulSoup(html, "lxml").find_all(tag, recursive=recursive)
    if found:
        return [tg.decode(formatter=None) for tg in found]
    return found


def py_find_lxml(html: str, tag: str, recursive: bool = True):
    doc = lxml.html.fromstring(html)
    pattern = ".//"
    if recursive is False:
        pattern = "./"

    found = doc.find(f"{pattern}{tag}")
    if found is not None:
        return lxml.html.tostring(found, encoding="unicode")
    return None


def py_findall_lxml(html: str, tag: str, recursive: bool = True):
    doc = lxml.html.fromstring(html)
    pattern = ".//"
    if recursive is False:
        pattern = "./"

    found = doc.findall(f"{pattern}{tag}")
    if found:
        return [lxml.html.tostring(tg, encoding="unicode") for tg in found]
    return None


def py_get_attr_bs4(html: str, tag: str, attr: str):
    soup = BeautifulSoup(html, "lxml")
    element = soup.find(tag)
    if element:
        return element.get(attr)
    return None


def py_get_attr_lxml(html: str, tag: str, attr: str):
    doc = lxml.html.fromstring(html)
    # iter() includes the root element itself, which fromstring() returns
    # directly when parsing a fragment.
    element = next((el for el in doc.iter(tag)), None)
    if element is not None:
        return element.get(attr)
    return None


# Fair-comparison variants for get_attr: the element is already parsed, so
# only the attribute lookup is measured (no document re-parse, no tag re-find).
def py_get_attr_bs4_for_benchmark(element, attr: str):
    return element.get(attr)


def py_get_attr_lxml_for_benchmark(element, attr: str):
    return element.get(attr)


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
class PythonHTMLGetTextDefBs4(BaseFunctionDefinition):
    function = py_get_text_bs4
    reference = "BeautifulSoup().get_text()"


class PythonHTMLGetTextDefLxml(BaseFunctionDefinition):
    function = py_get_text_lxml
    reference = "lxml.html.fromstring().text_content()"


class CythonHTMLGetTextDef(BaseFunctionDefinition):
    function = cy_textparse.html.get_text
    reference = "cythonpowered.textparse.html.get_text()"
    usage = f"{REPLACEMENT}, no HTML entity decoding"


# ------------------------------------------------------------------
class PythonHTMLFindDefBs4(BaseFunctionDefinition):
    function = py_find_bs4
    reference = "BeautifulSoup().find()"


class PythonHTMLFindDefLxml(BaseFunctionDefinition):
    function = py_find_lxml
    reference = "lxml.html.fromstring().find()"


class CythonHTMLFindDef(BaseFunctionDefinition):
    function = cy_textparse.html.find
    reference = "cythonpowered.textparse.html.find()"
    usage = f"{REPLACEMENT}, raw substring"


# ------------------------------------------------------------------


# ------------------------------------------------------------------
class PythonHTMLFindallDefBs4(BaseFunctionDefinition):
    function = py_findall_bs4
    reference = "BeautifulSoup().find_all()"


class PythonHTMLFindallDefLxml(BaseFunctionDefinition):
    function = py_findall_lxml
    reference = "lxml.html.fromstring().findall()"


class CythonHTMLFindallDef(BaseFunctionDefinition):
    function = cy_textparse.html.find_all
    reference = "cythonpowered.textparse.html.find_all()"
    usage = f"{REPLACEMENT}, raw substrings"


# ------------------------------------------------------------------


class PythonGetAttrDefBs4(BaseFunctionDefinition):
    function = py_get_attr_bs4
    reference = "BeautifulSoup().find().get()"


class PythonGetAttrDefLxml(BaseFunctionDefinition):
    function = py_get_attr_lxml
    reference = "lxml.html.fromstring().find().get()"


class PythonGetAttrDefBs4ForBenchmark(BaseFunctionDefinition):
    function = py_get_attr_bs4_for_benchmark
    reference = "BeautifulSoup Tag.get()"


class PythonGetAttrDefLxmlForBenchmark(BaseFunctionDefinition):
    function = py_get_attr_lxml_for_benchmark
    reference = "lxml Element.get()"


class CythonGetAttrDef(BaseFunctionDefinition):
    function = cy_textparse.html.get_attr
    reference = "cythonpowered.textparse.html.get_attr()"
    usage = "Takes single tag string as input, not a document"


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
    usage = f"{REPLACEMENT}, ASCII only"


class PythonExtractMacAddrsDef(BaseFunctionDefinition):
    function = py_get_mac_addrs
    reference = "re.findall(...) implementation to get MACs"


class CythonExtractMacAddrsDef(BaseFunctionDefinition):
    function = cy_textparse.get_mac_addrs
    reference = "cythonpowered.textparse.get_mac_addrs()"
    usage = REPLACEMENT


TEXTPARSE_DEFINITION_PAIRS = [
    [PythonHTMLGetTextDefBs4, CythonHTMLGetTextDef],
    [PythonHTMLFindDefBs4, CythonHTMLFindDef],
    [PythonHTMLFindallDefBs4, CythonHTMLFindallDef],
    [PythonGetAttrDefBs4, CythonGetAttrDef],
    [PythonExtractIpsDef, CythonExtractIpsDef],
    [PythonExtractEmailsDef, CythonExtractEmailsDef],
    [PythonExtractMacAddrsDef, CythonExtractMacAddrsDef],
]
