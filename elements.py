from typing import Optional
from dataclasses import dataclass
import json
from functools import partial

import plotly
import plotly.express as px
import pandas as pd

from js import document, componentHandler, plotly_render
from pyodide.ffi.wrappers import add_event_listener
from pyodide.code import run_js

import ACT_model as ACT_model


@dataclass
class BlockOption:
    desc: str
    footprint: float
    act_desc: Optional[str] = None
    act_param: Optional = None


def render_block_option(o):
    supporting_el_html = document.createElement("span")
    desc_el = document.createElement("span")
    desc_el.appendChild(document.createTextNode(o.desc))
    br_el = document.createElement("br")
    if o.act_desc is not None:
        footnote_desc = document.createTextNode(f"{o.act_desc}")
    else:
        footnote_desc = document.createTextNode(f"{o.footprint:.2f} kg CO2e")
    footprint_el = document.createElement("span")
    footprint_el.className = "footprint"
    footprint_el.appendChild(footnote_desc)

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
    # add_event_listener(e, "click", "Pyscript.globals.get('f')();")
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
    card_el.className = f"mdl-card mdl-card-mmaz {shadow}"
    supporting_el = document.createElement("div")
    supporting_el.className = "mdl-card__supporting-text mdl-card__supporting-text-mmaz"
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


def totalCO2(state, scale_factor: int = 1):
    sum_co2 = 0
    for k, v in state.items():
        if v["enabled"]:
            if k == "scale":
                continue
            sum_co2 += v["options"][v["selected"]].footprint * scale_factor
    sum_el = document.createElement("div")
    sum_el.appendChild(document.createTextNode(f"TinyML Total: {sum_co2:0.2f} kg CO2e"))
    return sum_el


def plot_inferences(state, elem_id: str, scale_tinyml: int = 1):
    inference_type = "FPS"
    inferences = {}
    inferences["system"] = ["TinyML", "Traditional"]
    inferences[inference_type] = [10, 20]
    df = pd.DataFrame(inferences)
    fig = px.bar(
        df, y="system", x=inference_type, orientation="h", title="Inferences/sec"
    )
    fig.update_layout(autosize=False, width=400, height=300)
    # max_footprint = max(1.5, sum_co2)
    # fig.update_yaxes(range=[0, 160])
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    plotly_render(graphJSON, elem_id)


def plot_co2(state, act_footprint, elem_id: str, scale_tinyml: int = 1):
    # footprint = {"system": [], "component": [], co2: []}
    footprint = {}
    footprint.update(act_footprint)
    co2 = "kg CO2"
    sum_co2 = 0
    for k, v in state["tinyml"].items():
        if v["enabled"]:
            if k == "scale":
                continue
            footprint["system"].append("TinyML")
            footprint["component"].append(v["heading"])
            co2e = v["options"][v["selected"]].footprint
            co2e = co2e * scale_tinyml
            footprint[co2].append(co2e)
            sum_co2 += co2e
    df = pd.DataFrame(footprint)
    fig = px.bar(
        df,
        x="system",
        y=co2,
        color="component",
        title="Embodied and Operational CO2 Footprint",
    )
    fig.update_layout(autosize=False, width=400, height=700)
    # max_footprint = max(1.5, sum_co2)
    # fig.update_yaxes(range=[0, 160])
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    plotly_render(graphJSON, elem_id)


def collapse_icon(elemid: str):
    icon_container = document.createElement("span")
    icon_container.setAttribute("style", "margin-left: 4px;")
    icon = document.createElement("span")
    icon.className = "icon material-icons mdl-color-text--grey-600"
    icon.setAttribute("id", elemid)
    icon.appendChild(document.createTextNode("settings"))
    # tooltip = document.createElement("span")
    # tooltip.className = "mdl-tooltip--right"
    # tooltip.setAttribute("for", elemid)
    # tooltip.appendChild(document.createTextNode("Collapse"))
    icon_container.appendChild(icon)
    # icon_container.appendChild(tooltip)
    componentHandler.upgradeElement(icon)
    # componentHandler.upgradeElement(tooltip)
    return icon_container


def collapse_byid(elemid, _):
    config = document.getElementById(elemid)
    if config.style.display == "none":
        config.style.display = "block"
    else:
        config.style.display = "none"


def text_node(text: str):
    el = document.createElement("div")
    el.appendChild(document.createTextNode(text))
    return el


class App:
    def __init__(self, state):
        assert "act" in state
        assert "tinyml" in state
        self.state = state

    def render(self):
        app = document.getElementById("app")
        app.innerHTML = ""
        main_div = document.createElement("div")
        main_div.className = "container"
        app.appendChild(main_div)

        main_row = document.createElement("div")
        main_row.className = "row"
        main_div.appendChild(main_row)

        graph_container = document.createElement("div")
        graph_container.className = "col-lg-5"
        main_row.appendChild(graph_container)

        config_container = document.createElement("div")
        config_container.className = "col-lg-7"
        main_row.appendChild(config_container)

        tinyml_container = document.createElement("div")
        tinyml_container.className = "calcsection"
        tinyml_container.appendChild(document.createTextNode("TinyML (Pirson & Bol)"))

        ci_tiny = collapse_icon("tinyml_collapse")

        add_event_listener(
            ci_tiny, "click", partial(collapse_byid, "tinyml_configuration")
        )
        tinyml_container.appendChild(ci_tiny)
        config_container.appendChild(tinyml_container)

        tinyml_inner_container = document.createElement("div")
        tinyml_inner_container.setAttribute("id", "tinyml_configuration")
        tinyml_container.appendChild(tinyml_inner_container)

        act_container = document.createElement("div")
        act_container.className = "calcsection"
        act_container.appendChild(document.createTextNode("Traditional Server (ACT)"))

        ci_act = collapse_icon("act_collapse")
        add_event_listener(ci_act, "click", partial(collapse_byid, "act_configuration"))
        act_container.appendChild(ci_act)
        config_container.appendChild(act_container)

        act_inner_container = document.createElement("div")
        act_inner_container.setAttribute("id", "act_configuration")
        act_container.appendChild(act_inner_container)

        for k, v in self.state["tinyml"].items():
            tinyml_inner_container.appendChild(render_block(v, self.build))

        for k, v in self.state["act"].items():
            act_inner_container.appendChild(render_block(v, self.build))

        # def mycb():
        #     print(self.state)
        #     self.state["ml_training"]["enabled"] = not self.state["ml_training"]["enabled"]
        #     self.build(None)
        # app.appendChild(button(mycb))
        # app.appendChild(document.createTextNode(f"{self.state}"))

        # graph_container.appendChild(text_node("TinyML vs. Traditional Server"))
        # graph_container.appendChild(text_node("Server Inferences/sec: 100 (placeholder)"))
        # graph_container.appendChild(text_node("TinyML Inferences/sec: 1 (placeholder)"))

        scale_factor_key = self.state["tinyml"]["scale"]["selected"]
        scale_factor = {0: 1, 1: 10, 2: 100, 3: 1000}[scale_factor_key]
        # graph_container.appendChild(totalCO2(self.state["tinyml"], scale_factor))

        act_footprint = ACT_model.model(self.state["act"])
        # print(f"{jload=}")
        # je = document.createTextNode(f"{jload}")
        # rje = document.createElement("div")
        # rje.appendChild(je)
        # graph_container.appendChild(rje)

        inference_el = document.createElement("div")
        inference_elem_id = "inference_graph"
        inference_el.setAttribute("id", inference_elem_id)
        graph_container.appendChild(inference_el)
        plot_inferences(
            self.state, elem_id=inference_elem_id, scale_tinyml=scale_factor
        )

        graph_el = document.createElement("div")
        co2_elem_id = "co2_graph"
        graph_el.setAttribute("id", co2_elem_id)
        graph_container.appendChild(graph_el)

        plot_co2(
            self.state, act_footprint, elem_id=co2_elem_id, scale_tinyml=scale_factor
        )

    def build(self, event):
        # if event is not None:
        #     self.update_state()

        self.render()
