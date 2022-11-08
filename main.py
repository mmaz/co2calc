from js import document, componentHandler

# https://jeff.glass/post/whats-new-pyscript-2022-09-1/
from pyodide.ffi.wrappers import add_event_listener
from pyodide.code import run_js
from dataclasses import dataclass
import elements as e


# state = dict(
#     a=e.SliderElement("a"),
#     b=e.SliderElement("b"),
#     c=e.SliderElement("c"),
#     d=e.RadioElement(
#         docid="d",
#         options=["disabled", "enabled"],
#         child_elems={1: e.SliderElement("i", max=50)},
#     ),
# )

state = dict(ml_training=dict(enabled=True, docid="tr", options=["a", "b"], selected=0))


def main():
    app = e.App(state)
    app.build(None)


main()
