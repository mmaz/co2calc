from js import document, componentHandler

# https://jeff.glass/post/whats-new-pyscript-2022-09-1/
from pyodide.ffi.wrappers import add_event_listener
from pyodide.code import run_js
from dataclasses import dataclass
import elements as e


state = dict(
    a=e.SliderElement("a"),
    b=e.SliderElement("b"),
    c=e.SliderElement("c"),
    d=e.RadioElement(
        docid="d",
        options=["disabled", "enabled"],
        child_elems={1: e.SliderElement("i", max=50)},
    ),
)


def f(event):
    print("f", event)

def update_state(state):
    for k, v in state.items():
        if isinstance(v, dict):
            update_state(v)
        elif isinstance(v, e.SliderElement):
            e = document.getElementById(f"{v.docid}")
            v = int(e.value)
            state[k].value = v
        elif isinstance(v, e.RadioElement):
            for ix,option in enumerate(v.options):
                e = document.getElementById(f"{v.docid}_{option}")
                if e.checked:
                    v.selected = ix
                    print("selected", option)


def render(app, state):
    for k, v in state.items():
        if isinstance(v, e.SliderElement):
            app.appendChild(e.slider(v))
        elif isinstance(v, e.RadioElement):
            app.appendChild(e.radio(v))


def build(event):
    # if event is not None:
    #     update_state(state)

    app = document.getElementById("app")
    app.innerHTML = ""
    render(app, state)
    app.appendChild(e.button())



def main():
    build(None)


main()
