import cythonpowered.textparse as tp
import pytest
from utils.definitions._textparse import (
    py_get_text,
    py_get_attr,
    py_get_ips,
    py_get_emails,
    py_get_mac_addrs,
)

# HTML tests
TEST_HTML = [
    "<p>Hello\n  world</p>",
    "<p>Hello world</p>",
    "<div class='container'>Nested <b>text</b> here</div>",
    "<!-- comment --><p>After comment</p>",
    '<a href="http://example.com?q=1&r=2">Link</a>',
    "<script>alert('xss')</script><p>Safe</p>",
    "<ul><li>Item 1</li><li>Item 2</li></ul>",
]


@pytest.mark.parametrize("html", TEST_HTML)
def test_html_get_text_vs_bs4_single(html):
    expected = py_get_text(html)
    actual = tp.get_text(html)
    assert actual == expected
    expected_stripped = py_get_text(html, strip=True)
    actual_stripped = tp.get_text(html, strip=True)
    assert actual_stripped == expected_stripped


def test_html_get_text_vs_bs4_full():
    html = "".join(TEST_HTML)
    expected = py_get_text(html)
    actual = tp.get_text(html)
    assert actual == expected
    expected_stripped = py_get_text(html, strip=True)
    actual_stripped = tp.get_text(html, strip=True)
    assert actual_stripped == expected_stripped


TEST_TAGS = [
    (
        '<div class="test" id="block1">content1</div><div class="test2" id="block2" style="somestyle: 2px; border: green;">content2</div>',
        "div",
        "style",
    ),
    (
        '<div class="test2" id="block2" style="somestyle: 2px; border: green;">content2</div>',
        "div",
        "style",
    ),
    ('<a href="http://example.com" title="Link">Click</a>', "a", "href"),
    ('<input type="text" name="username" value="john"/>', "input", "name"),
    ('<span style="color: red">text</span>', "span", "style"),
]


@pytest.mark.parametrize(["html", "tag", "attr"], TEST_TAGS)
def test_get_attr_vs_bs4(html, tag, attr):
    expected = py_get_attr(html, tag, attr)
    actual = tp.get_attr(html, tag, attr)
    assert actual == expected


# IP tests
TEST_IPS = [
    "192.168.1.1 and 10.0.0.1",
    "0.0.0.0 to 255.255.255.255",
    "textbeforeIP127.0.0.1",
    "127.0.0.2textafterIP",
    "256.1.1.1 invalid",
    "1.2.3.4.5 not an IP",
]


@pytest.mark.parametrize("text", TEST_IPS)
def test_get_ips_vs_regex(text):
    expected = py_get_ips(text)
    actual = tp.get_ips(text)
    assert actual == expected


def test_extract_all_ips():
    all_ips = " ".join(TEST_IPS)
    actual = tp.get_ips(all_ips)
    assert "192.168.1.1" in actual
    assert "10.0.0.1" in actual
    assert "127.0.0.1" in actual
    assert "127.0.0.2" in actual
    assert "256.1.1.1" not in actual
    assert "1.2.3.4.5" not in actual


# Email tests
TEST_EMAILS = [
    "Contact us at user@example.com or admin@test.org",
    "test.name+tag@domain.co.uk",
    "john-doe.someguy@test.com",
    "invalid#mail@123.com",
    "al$oinvalidmail@foobar.io",
]


@pytest.mark.parametrize("text", TEST_EMAILS)
def test_get_emails_vs_regex(text):
    expected = py_get_emails(text)
    actual = tp.get_emails(text)
    assert actual == expected


def test_extract_all_emails():
    all_emails = " ".join(TEST_EMAILS)
    actual = tp.get_emails(all_emails)
    assert "user@example.com" in actual
    assert "admin@test.org" in actual
    assert "test.name+tag@domain.co.uk" in actual
    assert "john-doe.someguy@test.com" in actual
    assert "invalid#mail@123.com" not in actual
    assert "al$oinvalidmail@foobar.io" not in actual


# MAC address tests
TEST_MAC_ADDRS = [
    "MAC: 00:1A:2B:3C:4D:5E and AA-BB-CC-DD-EE-FF",
    "00:1A:2B:3C:4D:5 and not-a-mac",
    "ZX-55-AB-78-A-FF-88 not a mac",
    "AB-F55-48-BD-78-AA also not a mac",
]


@pytest.mark.parametrize("text", TEST_MAC_ADDRS)
def test_get_mac_addrs_vs_regex(text):
    expected = py_get_mac_addrs(text)
    actual = tp.get_mac_addrs(text)
    assert actual == expected


def test_extract_all_mac_addrs():
    all_mac_addrs = " ".join(TEST_MAC_ADDRS)
    actual = tp.get_mac_addrs(all_mac_addrs)
    assert "00:1A:2B:3C:4D:5E" in actual
    assert "AA-BB-CC-DD-EE-FF" in actual
    assert "00:1A:2B:3C:4D:5" not in actual
    assert "ZX-55-AB-78-A-FF-88" not in actual
    assert "AB-F55-48-BD-78-AA" not in actual
