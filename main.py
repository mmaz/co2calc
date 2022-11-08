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

state = dict(
    ml_training=dict(
        enabled=True,
        heading="ML Training",
        docid="tr",
        options=[e.BlockOption(desc="DenseNet", footprint=0.1)],
        selected=0,
    ),
    casing=dict(
        enabled=True,
        heading="Casing",
        docid="casing",
        options=[
            e.BlockOption(desc="small", footprint=0.04),
            e.BlockOption(desc="medium", footprint=0.27),
            e.BlockOption(desc="large", footprint=0.63),
        ],
        selected=0,
    ),
    connectivity=dict(
        enabled=True,
        heading="Processing",
        docid="processing",
        options=[
            e.BlockOption(desc="ARM Coretex M4", footprint=0.08),
            e.BlockOption(desc="Broadcom XYZ", footprint=0.17),
            e.BlockOption(desc="SnapDragon ABC", footprint=0.29),
        ],
        selected=0,
    ),
)


def main():
    app = e.App(state)
    app.build(None)


main()
