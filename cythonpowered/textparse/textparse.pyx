# -----------------------------------------------------------------------------
# textparse — Fast text extraction functions powered by Cython
# Single-pass C scanning, no regex compilation, no backtracking
# -----------------------------------------------------------------------------

class html:

    @staticmethod
    def get_text(html:str, strip:bool=False):
        return html_get_text(html, strip=strip)

    @staticmethod
    def find(html: str, tag: str, recursive: bool=True):
        return find_tag(html=html, tag=tag, find_all=False, recursive=recursive)

    @staticmethod
    def find_all(html: str, tag: str, recursive: bool=True):
        return find_tag(html=html, tag=tag, find_all=True, recursive=recursive)


# -----------------------------------------------------------------------------
cdef inline list _html_strip_tags(str html, bint strip=False):
    """
    Removes all HTML tags from a string and returns a list of strings,
    corresponding to the text content of each tag.
    Handles nested tags, self-closing tags, quoted attributes,
    HTML comments, and <script>/<style> blocks.
    Helper function for get_text().
    """
    cdef unsigned int i = 0
    cdef unsigned int n = len(html)
    cdef unsigned int text_start = 0
    cdef list parts = []
    cdef bint in_tag = 0
    cdef bint in_comment = 0
    cdef bint in_script = 0
    cdef bint in_style = 0
    cdef unsigned char ch
    cdef str tag_lower


    while i < n:
        ch = <unsigned char>ord(html[i])

        if in_comment:
            if ch == ord('>') and i >= 2 and html[i-2:i] == '--':
                in_comment = 0
                i += 1
                text_start = i
            else:
                i += 1
            continue

        if in_script or in_style:
            tag_lower = html[i:min(i+9, n)].lower()
            #tag_lower_bytes = tag_lower.encode('ascii')
            if in_script and tag_lower[:8] == '</script':
                i += 9
                in_script = 0
                text_start = i
            elif in_style and tag_lower[:7] == '</style':
                i += 8
                in_style = 0
                text_start = i
            else:
                i += 1
            continue

        if ch == ord('<'):
            # Check for comment <!--
            if i + 3 < n and ord(html[i+1]) == ord('!') and html[i+2:i+4] == '--':
                if text_start < i:
                    parts.append(html[text_start:i])
                in_comment = 1
                i += 4
                continue

            # Check for script/style opening
            if not in_tag:
                tag_lower = html[i+1:min(i+11, n)].lower()

                if tag_lower.startswith('script'):
                    in_script = 1
                    i += 1
                    continue
                
                if tag_lower.startswith('style'):
                    in_style = 1
                    i += 1
                    continue

            # Opening tag
            if text_start < i:
                parts.append(html[text_start:i])
            in_tag = 1
            i += 1
        elif ch == ord('>') and in_tag:
            in_tag = 0
            text_start = i + 1
            i += 1
        elif (ch == ord('"') or ch == ord("'")) and in_tag:
            # Skip quoted attribute value
            quote = ch
            i += 1
            while i < n and ord(html[i]) != quote:
                i += 1
            if i < n:
                i += 1
        else:
            i += 1

    if not in_tag and text_start < n:
        parts.append(html[text_start:])

    if strip:
        return [p.strip() for p in parts]
    
    return parts
# -----------------------------------------------------------------------------



# -----------------------------------------------------------------------------
cpdef inline str html_get_text(str html, bint strip=False):
    """
    Extract text from HTML, optionally stripping whitespace per line.
    Replacement for: BeautifulSoup(html).get_text().
    """
    cdef list text = _html_strip_tags(html, strip=strip)
    cdef str part
    if strip:
        return ''.join([part.strip() for part in text])
    
    return ''.join(text)
# -----------------------------------------------------------------------------



# -----------------------------------------------------------------------------
cpdef inline object get_attr(str html, str tag, str attr):
    """
    Finds the first <tag ...> in HTML and extract the attr value.
    Handles attr="value", attr='value', attr=value.
    Returns None if tag or attribute not found.
    Replacement for: BeautifulSoup(html).find(tag).get(attr).
    """
    cdef unsigned int i = 0
    cdef unsigned int n = len(html)
    cdef str tag_lower = tag.lower()
    cdef str attr_lower = attr.lower()
    cdef unsigned int j
    cdef str current_tag
    cdef str attr_name
    cdef str attr_value
    cdef unsigned char qc

    while i < n:
        if html[i] != '<':
            i += 1
            continue

        # Skip comments
        if i + 3 < n and html[i+1:i+4] == '<!--':
            j = html.find('-->', i + 4)
            i = (j + 3) if j != -1 else n
            continue

        # Parse tag name
        j = i + 1
        while j < n and html[j] not in (' ', '\t', '\n', '\r', '>'):
            j += 1
        current_tag = html[i+1:j].lower()

        if current_tag != tag_lower:
            # Not our tag, skip to end
            j = html.find('>', i)
            i = (j + 1) if j != -1 else n
            continue

        # Found target tag — scan for attribute
        j += 1
        while j < n and html[j] != '>':
            # Skip whitespace
            while j < n and html[j] in (' ', '\t', '\n', '\r'):
                j += 1
            if j >= n or html[j] == '>':
                break

            # Read attribute name
            attr_name = ""
            while j < n and html[j] not in (' ', '=', '\t', '\n', '\r', '>'):
                attr_name += html[j]
                j += 1

            attr_name = attr_name.lower()

            if attr_name == attr_lower:
                # Found target attribute — read value
                if j < n and html[j] == '=':
                    j += 1
                    # Skip whitespace
                    while j < n and html[j] in (' ', '\t', '\n', '\r'):
                        j += 1
                    if j < n:
                        qc = ord(html[j])
                        if qc == ord('"') or qc == ord("'"):
                            j += 1
                            attr_value = ""
                            while j < n and ord(html[j]) != qc:
                                attr_value += html[j]
                                j += 1
                            if j < n:
                                j += 1
                            return attr_value
                        else:
                            attr_value = ""
                            while j < n and html[j] not in (' ', '\t', '\n', '\r', '>'):
                                attr_value += html[j]
                                j += 1
                            return attr_value
                # Boolean attribute (no value)
                return ""

            # Skip to next attribute or closing >
            if j < n and html[j] == '=':
                j += 1
                if j < n:
                    qc = ord(html[j])
                    if qc == ord('"') or qc == ord("'"):
                        j += 1
                        while j < n and ord(html[j]) != qc:
                            j += 1
                        if j < n:
                            j += 1
                    else:
                        while j < n and html[j] not in (' ', '\t', '\n', '\r', '>'):
                            j += 1
            
        return None
        # i = j + 1 if j < n else n

    return None
# -----------------------------------------------------------------------------



# -----------------------------------------------------------------------------
cdef inline bint is_space(char c):
    return (
        c == ' ' or
        c == '\t' or
        c == '\n' or
        c == '\r'
    )


cdef inline bint tag_equals(
    const char* html,
    Py_ssize_t start,
    Py_ssize_t end,
    const char* target,
    Py_ssize_t target_len
):
    cdef Py_ssize_t n

    n = end - start

    if n != target_len:
        return False

    return (
        html[start:start+n] ==
        target[:target_len]
    )


cdef bint id_matches(
    const char* html,
    Py_ssize_t attr_start,
    Py_ssize_t attr_end,
    const char* wanted_id,
    Py_ssize_t wanted_len
):
    cdef Py_ssize_t i = attr_start
    cdef Py_ssize_t value_start
    cdef Py_ssize_t value_end
    cdef char quote

    while i < attr_end - 2:

        if (
            html[i] == 'i' and
            html[i+1] == 'd'
        ):
            i += 2

            while i < attr_end and is_space(html[i]):
                i += 1

            if i >= attr_end or html[i] != '=':
                continue

            i += 1

            while i < attr_end and is_space(html[i]):
                i += 1

            quote = html[i]

            if quote not in (b'"'[0], b"'"[0]):
                continue

            value_start = i + 1

            i += 1

            while i < attr_end and html[i] != quote:
                i += 1

            value_end = i

            if (
                value_end - value_start ==
                wanted_len
            ):
                if (
                    html[value_start:value_end] ==
                    wanted_id[:wanted_len]
                ):
                    return True

        i += 1

    return False


from libc.string cimport memcmp
from cpython.unicode cimport PyUnicode_AsUTF8AndSize

cpdef inline find_tag(
    str html,
    str tag,
    bint find_all=False,
    bint recursive=True
):
    """
    Fast HTML tag search.

    Returns:
        first matching tag string
        OR list[str] if find_all=True
        OR None
    """

    cdef:
        Py_ssize_t n
        const char* buf

        const char* tag_ptr
        Py_ssize_t tag_len

        Py_ssize_t i = 0
        Py_ssize_t j

        Py_ssize_t open_start
        Py_ssize_t open_end

        Py_ssize_t name_start
        Py_ssize_t name_end

        Py_ssize_t depth = 0

        bytes close_tag = b"</" + tag.encode() + b">"
        const char* close_ptr = close_tag
        Py_ssize_t close_len = len(close_tag)

        list results = []

    buf = PyUnicode_AsUTF8AndSize(html, &n)
    tag_ptr = PyUnicode_AsUTF8AndSize(tag, &tag_len)

    while i < n:

        if buf[i] != '<':
            i += 1
            continue

        # Closing tag
        if i + 1 < n and buf[i + 1] == '/':

            depth -= 1

            while i < n and buf[i] != '>':
                i += 1

            i += 1
            continue

        open_start = i
        i += 1

        name_start = i

        while (
            i < n and
            not is_space(buf[i]) and
            buf[i] != '>'
        ):
            i += 1

        name_end = i

        while i < n and buf[i] != '>':
            i += 1

        open_end = i

        if (
            tag_equals(
                buf,
                name_start,
                name_end,
                tag_ptr,
                tag_len
            )
            and
            (recursive or depth == 0)
        ):

            j = open_end

            while j + close_len <= n:

                # Skip until next '<'
                while j < n and buf[j] != '<':
                    j += 1

                if j + close_len > n:
                    break

                if memcmp(buf + j, close_ptr, close_len) == 0:

                    if not find_all:
                        return html[open_start:j + close_len]

                    results.append(html[open_start:j + close_len])
                    break

                j += 1

        depth += 1
        i += 1

    if find_all:
        return [] if results is None else results

    return None


# -----------------------------------------------------------------------------
cdef extern from "ctype.h":
    bint isxdigit(int c)
    bint isdigit(int c)
    bint isalpha(int c)

cdef inline bint _is_local_char(unsigned char c):
    """Returns True if character is valid in email local part."""
    return isalpha(c) or isdigit(c) or c in (ord('.'), ord('_'), ord('+'), ord('-'))

cdef inline bint _is_domain_char(unsigned char c):
    """Returns True if character is valid in email domain part."""
    return isalpha(c) or isdigit(c) or c in (ord('.'), ord('-'))
# -----------------------------------------------------------------------------



# -----------------------------------------------------------------------------
cpdef inline list get_ips(str text):
    """
    Extracts valid IPv4 addresses from text.
    Validates each octet is 0-255. Respects word boundaries.
    Replacement for: re.findall(r"(?<![.\d])(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})(?![.\d])", text)
    """
    cdef unsigned int i = 0
    cdef unsigned int n = len(text)
    cdef list result = []
    cdef unsigned int j, octet_start
    cdef str octet_str
    cdef unsigned short octet_val
    cdef unsigned int octets_found = 0

    while i < n:
        if not isdigit(<unsigned char>ord(text[i])):
            i += 1
            continue

        # Word boundary: no digit before
        if i > 0 and isdigit(<unsigned char>ord(text[i - 1])):
            i += 1
            continue

        j = i
        octets_found = 0

        while j < n and octets_found < 4:
            octet_start = j
            # Limit to 3 digits per octet (valid IPv4 octets: 0-255, max 3 digits)
            while j < n and (j - octet_start) < 3 and isdigit(<unsigned char>ord(text[j])):
                j += 1

            if j == octet_start:
                break

            octet_str = text[octet_start:j]
            octet_val = int(octet_str)

            if octet_val > 255:
                break

            octets_found += 1

            if octets_found < 4:
                if j >= n or text[j] != '.':
                    break
                j += 1

        if octets_found == 4:
            # Word boundary: no digit or dot adjacent
            if (i > 0 and (text[i - 1] in ('.',) or isdigit(<unsigned char>ord(text[i - 1])))):
                i += 1
                continue
            if (j < n and (text[j] in ('.',) or isdigit(<unsigned char>ord(text[j])))):
                i += 1
                continue

            result.append(text[i:j])
            i = j
        else:
            i += 1

    return result
# -----------------------------------------------------------------------------



# -----------------------------------------------------------------------------
cpdef inline list get_emails(str text):
    """
    Extracts email addresses from text.
    Local part: alphanumeric + "._+-".
    Domain: alphanumeric + .- + . + 2+ alpha chars TLD.
    Replacement for: re.findall(r"[\w.+-]+@[\w.-]+\.\w{2,}", text)
    """
    cdef int i = 0
    cdef int n = len(text)
    cdef list result = []
    cdef int at_pos
    cdef int local_end
    cdef int local_start
    cdef int domain_end
    cdef int tld_start
    cdef str tld_part
    cdef bint has_dot = False

    while i < n:
        # Find @ symbol
        while i < n and text[i] != '@':
            i += 1
        if i >= n:
            break

        at_pos = i
        i += 1
        has_dot = False

        # Find local part end (from @ going backwards)
        local_end = at_pos - 1
        while local_end >= 0 and _is_local_char(<unsigned char>ord(text[local_end])):
            local_end -= 1
        local_start = local_end + 1

        if local_start > at_pos:
            # No valid local part
            continue

        # Parse domain from @
        domain_end = i
        while domain_end < n and _is_domain_char(<unsigned char>ord(text[domain_end])):
            if text[domain_end] == '.':
                has_dot = True
            domain_end += 1

        if not has_dot or domain_end <= i:
            i = domain_end
            continue

        # Find TLD (after last dot in domain)
        tld_start = domain_end
        while tld_start > i and text[tld_start - 1] != '.':
            tld_start -= 1

        tld_part = text[tld_start:domain_end]
        if len(tld_part) < 2:
            i = domain_end
            continue

        # Check TLD is all alpha
        all_alpha = True
        for c in tld_part:
            if not isalpha(<unsigned char>ord(c)):
                all_alpha = False
                break
        if not all_alpha:
            i = domain_end
            continue

        result.append(text[local_start:domain_end])
        i = domain_end

    return result
# -----------------------------------------------------------------------------



# -----------------------------------------------------------------------------
cpdef inline list get_mac_addrs(str text):
    """
    Extracts MAC addresses (XX:XX:XX:XX:XX:XX or XX-XX-XX-XX-XX-XX).
    Replacement for: re.findall(r"[0-9A-Fa-f]{2}[:-][0-9A-Fa-f]{2}[:-][0-9A-Fa-f]{2}[:-][0-9A-Fa-f]{2}[:-][0-9A-Fa-f]{2}[:-][0-9A-Fa-f]{2}", text).
    """
    cdef unsigned int i = 0
    cdef unsigned int n = len(text)
    cdef list result = []
    cdef unsigned int pos
    cdef str sep_char
    cdef unsigned int pair
    cdef bint sep_found = 0

    while i < n:
        if not isxdigit(<unsigned char>ord(text[i])):
            i += 1
            continue

        # Word boundary: no hex digit before
        if i > 0 and isxdigit(<unsigned char>ord(text[i - 1])):
            i += 1
            continue

        # Must be exactly 2 hex digits before separator
        if i + 2 >= n or not isxdigit(<unsigned char>ord(text[i + 1])):
            i += 1
            continue

        sep_char = text[i + 2]
        if sep_char not in (':', '-'):
            i += 1
            continue

        pos = i + 3
        sep_found = 1

        for pair in range(5):
            if pos + 1 >= n:
                sep_found = 0
                break
            if not (isxdigit(<unsigned char>ord(text[pos])) and isxdigit(<unsigned char>ord(text[pos + 1]))):
                sep_found = 0
                break
            pos += 2

            if pair < 4:
                if pos >= n or text[pos] != sep_char:
                    sep_found = 0
                    break
                pos += 1

        if sep_found:
            # Word boundary: no hex digit after
            if pos < n and isxdigit(<unsigned char>ord(text[pos])):
                i += 1
                continue
            result.append(text[i:pos])
            i = pos
        else:
            i += 1

    return result
# -----------------------------------------------------------------------------
