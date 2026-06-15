from utils.benchmark._base import (
    BaseFunctionBenchmark,
    BaseModuleBenchmark,
)
from utils.definitions._textparse import (
    PythonGetTextDefBs4,
    PythonGetTextDefLxml,
    CythonGetTextDef,
    PythonGetAttrDef,
    CythonGetAttrDef,
    PythonExtractIpsDef,
    CythonExtractIpsDef,
    PythonExtractEmailsDef,
    CythonExtractEmailsDef,
    PythonExtractMacAddrsDef,
    CythonExtractMacAddrsDef,
)

HTML = (
    "<div class='container'><h1>Title</h1>"
    "<p>Paragraph with <a href='#'>link</a></p>"
    "<!-- comment -->"
    "<script>alert('xss')</script>"
    "<style>.hidden { display: none; }</style>"
    "<p>More content <b>bold</b> and <i>italic</i></p>"
    '<img src="image.jpg" alt="An image" class="responsive"/>'
    "<ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul>"
    "<table><tr><td>Cell 1</td><td>Cell 2</td></tr></table>"
    "<p>Final paragraph with <span class='highlight'>highlighted</span> text</p>"
    "<div class='test-class' data-id='12345' data-value='hello'>content</div>"
)

IP_TEXTS = " ".join(
    [
        f"Server {i}.{i+1}.{i+2}.{i+3} found at position {i} in the log data"
        for i in range(100)
    ]
)

EMAIL_TEXTS = " ".join(
    [
        f"Contact user{i}@domain{i}.com or admin@test{i}.org for support with issue #{i}"
        for i in range(100)
    ]
)

MAC_TEXTS = " ".join(
    [
        f"MAC: 00:1A:2B:{i:02X}:{i+1:02X}:{i+2:02X} registered on switch port {i} at time {i}"
        for i in range(100)
    ]
)


class GetTextBenchmarkDefinitionBs4(BaseFunctionBenchmark):
    python_function = PythonGetTextDefBs4
    cython_function = CythonGetTextDef
    python_args = [HTML]
    cython_args = [HTML]
    kwargs = {"strip": False}
    runs = [100, 1000, 10000]


class GetTextBenchmarkDefinitionLxml(BaseFunctionBenchmark):
    python_function = PythonGetTextDefLxml
    cython_function = CythonGetTextDef
    python_args = [HTML]
    cython_args = [HTML]
    runs = [100, 1000, 10000]


class GetAttrBenchmarkDefinition(BaseFunctionBenchmark):
    python_function = PythonGetAttrDef
    cython_function = CythonGetAttrDef
    python_args = [HTML, "div", "class"]
    cython_args = [HTML, "div", "class"]
    runs = [100, 1000, 10000]


class ExtractIpsBenchmarkDefinition(BaseFunctionBenchmark):
    python_function = PythonExtractIpsDef
    cython_function = CythonExtractIpsDef
    python_args = [IP_TEXTS]
    cython_args = [IP_TEXTS]
    runs = [100, 1000, 10000]


class ExtractEmailsBenchmarkDefinition(BaseFunctionBenchmark):
    python_function = PythonExtractEmailsDef
    cython_function = CythonExtractEmailsDef
    python_args = [EMAIL_TEXTS]
    cython_args = [EMAIL_TEXTS]
    runs = [100, 1000, 10000]


class ExtractMacAddrsBenchmarkDefinition(BaseFunctionBenchmark):
    python_function = PythonExtractMacAddrsDef
    cython_function = CythonExtractMacAddrsDef
    python_args = [MAC_TEXTS]
    cython_args = [MAC_TEXTS]
    runs = [100, 1000, 10000]


class TextparseBenchmark(BaseModuleBenchmark):
    MODULE = "textparse"
    BENCHMARKS = [
        GetTextBenchmarkDefinitionBs4,
        GetTextBenchmarkDefinitionLxml,
        GetAttrBenchmarkDefinition,
        ExtractIpsBenchmarkDefinition,
        ExtractEmailsBenchmarkDefinition,
        ExtractMacAddrsBenchmarkDefinition,
    ]
