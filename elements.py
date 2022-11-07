from js import document, componentHandler
from pyodide.ffi.wrappers import add_event_listener
from pyodide.code import run_js
from dataclasses import dataclass


@dataclass
class SliderElement:
    docid: str
    min: float = 0
    max: float = 100
    value: float = 0
    step: float = 1


@dataclass
class RadioElement:
    docid: str
    options: list[str]
    child_elems: dict  # dict of int -> Elem
    selected: int = 0

def button():
    e = document.createElement("button")
    e.className = "mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--accent"
    e.appendChild(document.createTextNode("Build"))
    componentHandler.upgradeElement(e)
    add_event_listener(e, "click", f)
    return e

def make_cols(row_elems):
    """
    Args:
        row_elems: list[tuple[Element, int]]
    """
    container = document.createElement("div")
    container.className = "container"
    re = document.createElement("div")
    re.className = "row"
    container.appendChild(re)
    for e, w in row_elems:
        ce = document.createElement("div")
        ce.className = f"col-{w}"
        ce.appendChild(e)
        re.appendChild(ce)
    return container


def set_attributes(e, **kwargs):
    for k, v in kwargs.items():
        e.setAttribute(k, v)


def slider(state: SliderElement):
    slider = document.createElement("div")
    e = document.createElement("input")
    e.className = "mdl-slider mdl-js-slider"
    slider_id = f"{state.docid}"
    set_attributes(
        e,
        id=slider_id,
        type="range",
        min=f"{state.min}",
        max=f"{state.max}",
        value=f"{state.value}",
        tabindex="0",
    )
    slider.appendChild(e)

    value_display = document.createElement("div")
    value_display.innerHTML = f"{state.value}"

    def update_value_display(_):
        e = document.getElementById(state.docid)
        value_display.innerHTML = e.value

    add_event_listener(e, "input", update_value_display)
    add_event_listener(e, "change", build)
    componentHandler.upgradeElement(e)
    return make_cols([(slider, 11), (value_display, 1)])

def radio(state: RadioElement):
    container = document.createElement("div")
    container.className = "container"
    for ix, option in enumerate(state.options):
        radio_id = f"{state.docid}_{option}"
        label = document.createElement("label")
        label.className = "mdl-radio mdl-js-radio mdl-js-ripple-effect"
        label.setAttribute("for", radio_id)
        inputelem = document.createElement("input")
        inputelem.className = "mdl-radio__button"
        inputelem.setAttribute("id", radio_id)
        # inputelem.setAttribute("name", )
        label.appendChild(inputelem)
        inputelem.setAttribute("type", "radio")
        inputelem.setAttribute("name", f"{state.docid}_{option}")
        span = document.createElement("span")
        span.className = "mdl-radio__label"
        span.appendChild(document.createTextNode(option))
        label.appendChild(span)
        if ix == state.selected:
            inputelem.setAttribute("checked", "checked")
        add_event_listener(inputelem, "click", build)
        container.appendChild(label)
    # componentHandler.upgradeElement(container)
    return container