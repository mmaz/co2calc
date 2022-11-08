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

def button(cb):
    evt_handler = """(event) => {Pyscript.globals.get('f')(event)};"""
    e = document.createElement("button")
    e.className = "mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--accent"
    e.appendChild(document.createTextNode("Build"))
    componentHandler.upgradeElement(e)
    #add_event_listener(e, "click", "Pyscript.globals.get('f')();")
    # e.setAttribute("onclick", evt_handler)
    def modify_state(_):
        cb()
    # e.setAttribute("onclick", "Pyscript.globals.get('f')();")
    # e.setAttribute("onclick", "Pyscript.globals.get('f')();")
    add_event_listener(e, "click", modify_state)
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

def checkbox(state, cb):
    # <label class="mdl-checkbox mdl-js-checkbox mdl-js-ripple-effect" for="checkbox-1">
    #   <input type="checkbox" id="checkbox-1" class="mdl-checkbox__input" checked>
    #   <span class="mdl-checkbox__label">Checkbox</span>
    # </label>
    label_el = document.createElement("label")
    label_el.className = "mdl-checkbox mdl-js-checkbox mdl-js-ripple-effect"
    label_el.setAttribute("for", state["docid"])
    input_el = document.createElement("input")
    input_el.setAttribute("type", "checkbox")
    input_el.className = "mdl-checkbox__input"
    input_el.setAttribute("id", state["docid"])
    if state["enabled"]:
        input_el.setAttribute("checked", "checked")
    label_el.appendChild(input_el)
    span_el = document.createElement("span")
    span_el.className = "mdl-checkbox__label"
    span_el.appendChild(document.createTextNode(state["heading"]))
    label_el.appendChild(span_el)
    componentHandler.upgradeElement(label_el)
    def toggle(_):
        state["enabled"] = not state["enabled"]
        cb(None)
    add_event_listener(input_el, "change", toggle)
    return label_el

def block_option(ix, state, cb):
    card_el = document.createElement("div")
    if ix == state["selected"]:
        shadow = "mdl-card-active mdl-shadow--4dp"
    else:
        shadow = "mdl-card-inactive mdl-shadow--2dp"
    card_el.className = f"mdl-card mdl-card-mini {shadow}"
    supporting_el = document.createElement("div")
    supporting_el.className = "mdl-card__supporting-text"
    supporting_el.appendChild(document.createTextNode(state["options"][ix]))
    card_el.appendChild(supporting_el)
    def new_selection(_):
        state["selected"] = ix
        cb(None)
    add_event_listener(card_el, "click", new_selection)
    return card_el


def render_block(state, cb):
    block_el = document.createElement("div")
    block_el.className = "block-el"
    block_title = document.createElement("div")
    block_title.className = "block-title"
    block_title.appendChild(checkbox(state, cb))
    block_el.appendChild(block_title)

    row_els = []
    for ix, _ in enumerate(state["options"]):
        row_els.append((block_option(ix, state, cb), 3))
    block_el.appendChild(make_cols(row_els))
    return block_el

def slider(state: SliderElement, cb):
    slider_el = document.createElement("div")
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
    slider_el.appendChild(e)

    value_display = document.createElement("div")
    value_display.innerHTML = f"{state.value}"

    def update_value_display(_):
        e = document.getElementById(state.docid)
        value_display.innerHTML = e.value

    add_event_listener(e, "input", update_value_display)
    add_event_listener(e, "change", cb)
    componentHandler.upgradeElement(e)
    return make_cols([(slider_el, 11), (value_display, 1)])

def radio(state: RadioElement, cb):
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
        add_event_listener(inputelem, "click", cb)
        container.appendChild(label)
    # componentHandler.upgradeElement(container)
    return container


class App:
    def __init__(self, state):
        self.state = state
    

    def render(self):
        app = document.getElementById("app")
        app.innerHTML = ""
        for k, v in self.state.items():
            app.appendChild(render_block(v, self.build))
        #     if isinstance(v, SliderElement):
        #         app.appendChild(slider(v, self.build))
        #     elif isinstance(v, RadioElement):
        #         app.appendChild(radio(v, self.build))
        def mycb():
            print(self.state)
            self.state["ml_training"]["enabled"] = not self.state["ml_training"]["enabled"]
            self.build(None)
        # app.appendChild(button(mycb))
        app.appendChild(document.createTextNode(f"{self.state}"))

    def build(self, event):
        # if event is not None:
        #     self.update_state()

        self.render()