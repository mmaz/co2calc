from dataclasses import dataclass
import json

import plotly
import plotly.express as px
import pandas as pd

from js import document, componentHandler, plotly_render
from pyodide.ffi.wrappers import add_event_listener
from pyodide.code import run_js

@dataclass
class BlockOption:
    desc: str
    footprint: float

def render_block_option(o):
    supporting_el_html = document.createElement("span")
    desc_el = document.createElement("span")
    desc_el.appendChild(document.createTextNode(o.desc))
    br_el = document.createElement("br")
    footprint_el = document.createElement("span")
    footprint_el.className = "footprint"
    footprint_el.appendChild(document.createTextNode(f"{o.footprint} kg CO2e"))

    for e in [desc_el, br_el, footprint_el]:
        supporting_el_html.appendChild(e)
    return supporting_el_html

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
        if state["enabled"]:
            shadow = "mdl-card-active mdl-shadow--4dp"
        else:
            shadow = "mdl-card-ignore mdl-shadow--4dp"
    else:
        shadow = "mdl-card-inactive mdl-shadow--2dp"
    card_el.className = f"mdl-card mdl-card-mini {shadow}"
    supporting_el = document.createElement("div")
    supporting_el.className = "mdl-card__supporting-text"
    supporting_el.appendChild(render_block_option(state["options"][ix]))
    card_el.appendChild(supporting_el)
    def new_selection(_):
        state["selected"] = ix
        cb(None)
    add_event_listener(card_el, "click", new_selection)
    return card_el


def render_block(state, cb):
    block_el = document.createElement("div")
    block_el.className = "block-el"
    block_el.setAttribute("style", "margin-left: 10px; margin-right: 10px;")
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

def totalCO2(state):
    sum_co2 = 0
    for k, v in state.items():
        if v["enabled"]:
            sum_co2 += v["options"][v["selected"]].footprint
    sum_el = document.createElement("div")
    sum_el.appendChild(document.createTextNode(f"Total: {sum_co2:0.2f} kg CO2e"))
    return sum_el   

def plot(state):
    # df = pd.DataFrame(
    # fig = px.bar(x=["a", "b", "c"], y=[1, 3, 2])
    co2 = "kg CO2"
    footprint = {"system": [], "component": [], co2: []}
    sum_co2 = 0
    for k, v in state.items():
        if v["enabled"]:
            footprint["system"].append("TinyML")
            footprint["component"].append(v["heading"])
            co2e = v["options"][v["selected"]].footprint
            footprint[co2].append(co2e)
            sum_co2 += co2e
    df = pd.DataFrame(footprint)
    fig = px.bar(df, x="system", y=co2, color="component")
    fig.update_layout(autosize=False, width=300, height=400)
    max_footprint = max(1.5, sum_co2)
    fig.update_yaxes(range=[0, max_footprint])
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    plotly_render(graphJSON,"graph")

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
        # app.appendChild(document.createTextNode(f"{self.state}"))
        app.appendChild(totalCO2(self.state))

        graph_el = document.createElement("div")
        graph_el.setAttribute("id", "graph")
        app.appendChild(graph_el)
        plot(self.state)

    def build(self, event):
        # if event is not None:
        #     self.update_state()

        self.render()