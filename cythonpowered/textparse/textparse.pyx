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
from cpython.unicode cimport (
    PyUnicode_KIND,
    PyUnicode_DATA,
    PyUnicode_READ
)

cpdef inline str get_attr(str tag, str attr):
    cdef:
        Py_ssize_t n = len(tag)
        Py_ssize_t m = len(attr)
        Py_ssize_t i = 0          # Current scan position
        Py_ssize_t j              # Loop variable
        Py_ssize_t start          # Start of current token

        # Cache Unicode internals once.
        # This avoids repeated Python-level indexing.
        int kind_tag = PyUnicode_KIND(tag)
        int kind_attr = PyUnicode_KIND(attr)

        void* data_tag = PyUnicode_DATA(tag)
        void* data_attr = PyUnicode_DATA(attr)

        Py_UCS4 c
        Py_UCS4 quote

    # ----------------------------------------------------------
    # Skip the opening tag name.
    #
    # Example:
    #     <a href="x">
    #      ^
    #      i starts here
    #
    # We stop once we reach the whitespace after "a".
    # ----------------------------------------------------------
    while i < n:
        c = PyUnicode_READ(kind_tag, data_tag, i)
        if c == ' ' or c == '\t' or c == '\n' or c == '\r':
            break
        i += 1

    # ----------------------------------------------------------
    # Scan each attribute exactly once.
    # ----------------------------------------------------------
    while i < n:

        # Skip whitespace between attributes.
        while i < n:
            c = PyUnicode_READ(kind_tag, data_tag, i)
            if c > ' ':
                break
            i += 1

        if i >= n:
            break

        # Stop at end of tag.
        if PyUnicode_READ(kind_tag, data_tag, i) == '>':
            break

        # Beginning of current attribute name.
        start = i

        # Read until '=', whitespace or '>'.
        while i < n:
            c = PyUnicode_READ(kind_tag, data_tag, i)
            if c == '=' or c <= ' ' or c == '>':
                break
            i += 1

        # ------------------------------------------------------
        # Compare attribute name.
        #
        # This performs an in-place character comparison.
        # No temporary substring is ever created.
        # ------------------------------------------------------
        if i - start == m:

            for j in range(m):
                if (
                    PyUnicode_READ(kind_tag, data_tag, start + j)
                    !=
                    PyUnicode_READ(kind_attr, data_attr, j)
                ):
                    break
            else:
                # ==================================================
                # Attribute name matched.
                # Parse and return its value.
                # ==================================================

                # Skip spaces before '='
                while i < n and PyUnicode_READ(kind_tag, data_tag, i) <= ' ':
                    i += 1

                if i >= n or PyUnicode_READ(kind_tag, data_tag, i) != '=':
                    return ""

                i += 1

                # Skip spaces after '='
                while i < n and PyUnicode_READ(kind_tag, data_tag, i) <= ' ':
                    i += 1

                if i >= n:
                    return ""

                quote = PyUnicode_READ(kind_tag, data_tag, i)

                # -----------------------------
                # Quoted attribute
                # href="..."
                # -----------------------------
                if quote == '"' or quote == "'":
                    i += 1
                    start = i

                    while i < n and PyUnicode_READ(kind_tag, data_tag, i) != quote:
                        i += 1

                    # This is the ONLY string allocation.
                    return tag[start:i]

                # -----------------------------
                # Unquoted attribute
                # value=123
                # -----------------------------
                start = i

                while i < n:
                    c = PyUnicode_READ(kind_tag, data_tag, i)
                    if c <= ' ' or c == '>':
                        break
                    i += 1

                return tag[start:i]

        # ------------------------------------------------------
        # Attribute name didn't match.
        #
        # Skip over the entire attribute value so that scanning
        # resumes at the next attribute.
        # ------------------------------------------------------
        while i < n:

            c = PyUnicode_READ(kind_tag, data_tag, i)

            if c == '>':
                return ""

            if c == '=':

                i += 1

                while i < n and PyUnicode_READ(kind_tag, data_tag, i) <= ' ':
                    i += 1

                if i >= n:
                    return ""

                quote = PyUnicode_READ(kind_tag, data_tag, i)

                # Skip quoted value.
                if quote == '"' or quote == "'":

                    i += 1

                    while i < n and PyUnicode_READ(kind_tag, data_tag, i) != quote:
                        i += 1

                    if i < n:
                        i += 1

                # Skip unquoted value.
                else:

                    while i < n:
                        c = PyUnicode_READ(kind_tag, data_tag, i)
                        if c <= ' ' or c == '>':
                            break
                        i += 1

                break

            i += 1

    # Attribute not found.
    return None
# -----------------------------------------------------------------------------



# -----------------------------------------------------------------------------
# Fast HTML tag search
# -----------------------------------------------------------------------------

from libc.string cimport memcmp
from cpython.unicode cimport PyUnicode_AsUTF8AndSize


# -----------------------------------------------------------------------------
# Helpers
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
    cdef Py_ssize_t length = end - start

    if length != target_len:
        return False

    return memcmp(
        html + start,
        target,
        target_len
    ) == 0


cdef inline bint is_void_tag(
    const char* tag_ptr,
    Py_ssize_t tag_len
):
    """
    HTML5 void elements.

    These elements do not have closing tags:

        <area>
        <base>
        <br>
        <col>
        <embed>
        <hr>
        <img>
        <input>
        <link>
        <meta>
        <param>
        <source>
        <track>
        <wbr>
    """

    if tag_len == 2:
        return (
            memcmp(tag_ptr, b"br", 2) == 0 or
            memcmp(tag_ptr, b"hr", 2) == 0
        )

    if tag_len == 3:
        return (
            memcmp(tag_ptr, b"img", 3) == 0 or
            memcmp(tag_ptr, b"col", 3) == 0
        )

    if tag_len == 4:
        return (
            memcmp(tag_ptr, b"area", 4) == 0 or
            memcmp(tag_ptr, b"base", 4) == 0 or
            memcmp(tag_ptr, b"link", 4) == 0 or
            memcmp(tag_ptr, b"meta", 4) == 0
        )

    if tag_len == 5:
        return (
            memcmp(tag_ptr, b"input", 5) == 0 or
            memcmp(tag_ptr, b"embed", 5) == 0 or
            memcmp(tag_ptr, b"param", 5) == 0 or
            memcmp(tag_ptr, b"track", 5) == 0
        )

    if tag_len == 6:
        return (
            memcmp(tag_ptr, b"source", 6) == 0
        )

    if tag_len == 3:
        return (
            memcmp(tag_ptr, b"wbr", 3) == 0
        )

    return False


# -----------------------------------------------------------------------------
# Find the end of an opening tag.
#
# This correctly handles:
#
#     <input type="text">
#     <input title="1 > 0">
#
# so that '>' inside quotes isn't treated as the end of the tag.
# -----------------------------------------------------------------------------

cdef inline Py_ssize_t find_tag_end(
    const char* buf,
    Py_ssize_t start,
    Py_ssize_t n
):
    cdef:
        Py_ssize_t i = start
        char quote = 0

    while i < n:

        if quote != 0:
            if buf[i] == quote:
                quote = 0

        else:
            if buf[i] == '"' or buf[i] == "'":
                quote = buf[i]

            elif buf[i] == '>':
                return i

        i += 1

    return n


# -----------------------------------------------------------------------------
# Determine whether an opening tag is explicitly self-closing:
#
#     <foo />
#     <foo/>
# -----------------------------------------------------------------------------

cdef inline bint is_self_closing(
    const char* buf,
    Py_ssize_t start,
    Py_ssize_t end
):
    cdef Py_ssize_t i = end

    while i > start and is_space(buf[i - 1]):
        i -= 1

    return (
        i > start and
        buf[i - 1] == '/'
    )


# -----------------------------------------------------------------------------
# Find the next tag name.
#
# Returns:
#
#     0  = not a normal opening/closing tag
#     1  = opening tag
#     2  = closing tag
#
# name_start/name_end contain the tag name.
# tag_end contains the position of '>'.
# -----------------------------------------------------------------------------

cdef inline int parse_tag(
    const char* buf,
    Py_ssize_t start,
    Py_ssize_t n,
    Py_ssize_t* name_start,
    Py_ssize_t* name_end,
    Py_ssize_t* tag_end
):
    cdef:
        Py_ssize_t i = start + 1
        Py_ssize_t ns
        Py_ssize_t ne
        bint closing = False

    if i >= n:
        return 0

    # Closing tag
    if buf[i] == '/':
        closing = True
        i += 1

    # Comments, declarations, processing instructions, etc.
    if i >= n:
        return 0

    if (
        buf[i] == '!' or
        buf[i] == '?' 
    ):
        return 0

    # Skip whitespace after '<' or '</'
    while i < n and is_space(buf[i]):
        i += 1

    ns = i

    # Tag name
    while (
        i < n and
        not is_space(buf[i]) and
        buf[i] != '>' and
        buf[i] != '/'
    ):
        i += 1

    ne = i

    if ne == ns:
        return 0

    # Find the end of the complete tag.
    i = find_tag_end(buf, i, n)

    if i >= n:
        return 0

    name_start[0] = ns
    name_end[0] = ne
    tag_end[0] = i

    if closing:
        return 2

    return 1


# -----------------------------------------------------------------------------
# Main function
# -----------------------------------------------------------------------------

cpdef inline find_tag(
    str html,
    str tag,
    bint find_all=False,
    bint recursive=True
):
    """
    Fast HTML tag search.

    Examples:

        find_tag(html, "div")

            -> "<div>...</div>"

        find_tag(html, "input")

            -> '<input type="text">'

        find_tag(html, "input", find_all=True)

            -> [
                   '<input type="text">',
                   '<input type="email">'
               ]

    Args:
        html:
            HTML string to search.

        tag:
            Tag name, e.g. "div", "input", "img".

        find_all:
            Return all matching tags instead of the first one.

        recursive:
            If True, matching tags may occur inside other elements.

            If False, only top-level matching tags are returned.

    Returns:
        str
            First matching tag.

        list[str]
            All matching tags when find_all=True.

        None
            If no matching tag exists.
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

        Py_ssize_t close_name_start
        Py_ssize_t close_name_end
        Py_ssize_t close_end

        Py_ssize_t depth = 0
        Py_ssize_t local_depth

        int tag_type
        int inner_type

        bint self_closing

        list results = []

        bytes tag_bytes
        bytes lower_tag

    # -------------------------------------------------------------------------
    # Convert strings to UTF-8.
    # -------------------------------------------------------------------------

    buf = PyUnicode_AsUTF8AndSize(html, &n)

    # Make tag comparison case-insensitive.
    #
    # HTML tag names are ASCII case-insensitive.
    lower_tag = tag.lower().encode("ascii")
    tag_ptr = lower_tag
    tag_len = len(lower_tag)

    # -------------------------------------------------------------------------
    # Main scan
    # -------------------------------------------------------------------------

    while i < n:

        # Find next '<'
        if buf[i] != '<':
            i += 1
            continue

        open_start = i

        # ---------------------------------------------------------------------
        # Parse this tag.
        # ---------------------------------------------------------------------

        tag_type = parse_tag(
            buf,
            i,
            n,
            &name_start,
            &name_end,
            &open_end
        )

        # Not a normal tag.
        if tag_type == 0:
            i += 1
            continue

        # ---------------------------------------------------------------------
        # Closing tags don't start a search.
        #
        # We don't use them to blindly manipulate global depth because
        # unrelated closing tags should not affect whether our requested
        # tag is nested.
        # ---------------------------------------------------------------------

        if tag_type == 2:
            i = open_end + 1

            if depth > 0:
                depth -= 1

            continue

        # ---------------------------------------------------------------------
        # Opening tag.
        # ---------------------------------------------------------------------

        # Is this the tag we're looking for?
        if tag_equals(
            buf,
            name_start,
            name_end,
            tag_ptr,
            tag_len
        ):

            # -------------------------------------------------------------
            # Void HTML element.
            #
            # Examples:
            #
            #   <input>
            #   <input type="text">
            #   <img src="foo.jpg">
            #   <br>
            #
            # There is no closing tag to search for.
            # -------------------------------------------------------------

            if is_void_tag(
                tag_ptr,
                tag_len
            ):

                if recursive or depth == 0:

                    if not find_all:
                        return html[
                            open_start:open_end + 1
                        ]

                    results.append(
                        html[
                            open_start:open_end + 1
                        ]
                    )

                i = open_end + 1
                continue

            # -------------------------------------------------------------
            # Explicit self-closing element.
            #
            # Examples:
            #
            #   <foo />
            #   <custom/>
            #
            # -------------------------------------------------------------

            self_closing = is_self_closing(
                buf,
                open_start,
                open_end
            )

            if self_closing:

                if recursive or depth == 0:

                    if not find_all:
                        return html[
                            open_start:open_end + 1
                        ]

                    results.append(
                        html[
                            open_start:open_end + 1
                        ]
                    )

                i = open_end + 1
                continue

            # -------------------------------------------------------------
            # Normal opening/closing element.
            #
            # Search for the corresponding closing tag.
            # -------------------------------------------------------------

            if recursive or depth == 0:

                local_depth = 1
                j = open_end + 1

                while j < n:

                    # Find next '<'
                    while j < n and buf[j] != '<':
                        j += 1

                    if j >= n:
                        break

                    # -----------------------------------------------------
                    # Parse next tag.
                    # -----------------------------------------------------

                    inner_type = parse_tag(
                        buf,
                        j,
                        n,
                        &close_name_start,
                        &close_name_end,
                        &close_end
                    )

                    if inner_type == 0:
                        j += 1
                        continue

                    # -----------------------------------------------------
                    # Another opening tag with the same name.
                    # -----------------------------------------------------

                    if inner_type == 1:

                        # Ignore void elements.
                        if tag_equals(
                            buf,
                            close_name_start,
                            close_name_end,
                            tag_ptr,
                            tag_len
                        ):

                            if not is_void_tag(
                                buf + close_name_start,
                                close_name_end - close_name_start
                            ) and not is_self_closing(
                                buf,
                                j,
                                close_end
                            ):
                                local_depth += 1

                        j = close_end + 1
                        continue

                    # -----------------------------------------------------
                    # Closing tag.
                    # -----------------------------------------------------

                    if inner_type == 2:

                        if tag_equals(
                            buf,
                            close_name_start,
                            close_name_end,
                            tag_ptr,
                            tag_len
                        ):

                            local_depth -= 1

                            if local_depth == 0:

                                if not find_all:
                                    return html[
                                        open_start:close_end + 1
                                    ]

                                results.append(
                                    html[
                                        open_start:close_end + 1
                                    ]
                                )

                                break

                        j = close_end + 1
                        continue

                    j = close_end + 1

        # ---------------------------------------------------------------------
        # Move to the next opening tag.
        # ---------------------------------------------------------------------

        # Void/self-closing tags don't increase depth.
        if not is_void_tag(
            buf + name_start,
            name_end - name_start
        ) and not is_self_closing(
            buf,
            open_start,
            open_end
        ):
            depth += 1

        i = open_end + 1

    # -------------------------------------------------------------------------
    # Results
    # -------------------------------------------------------------------------

    if find_all:
        return results

    return None

# -----------------------------------------------------------------------------



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
