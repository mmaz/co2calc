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


def render_presets(state, callbacks):
    assert len(callbacks) == len(state["options"])
    block_el = document.createElement("div")
    block_el.className = "block-el"
    block_el.setAttribute("style", "margin-left: 10px; margin-right: 10px;")
    block_title = document.createElement("div")
    block_title.className = "block-title"
    block_title.appendChild(document.createTextNode(state["heading"]))
    block_el.appendChild(block_title)

    row_els = []
    for ix, _ in enumerate(state["options"]):
        row_els.append((block_option(ix, state, callbacks[ix]), 3))
    block_el.appendChild(make_cols(row_els))
    return block_el


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


def inference_emerging(
    state: dict, inferences: dict, inference_key: str, emerging_fps: dict
):
    if state["emerging"]["flexic"]["enabled"]:
        inferences["system"].append("FlexICs")
        flexic_scale_factor_key = state["emerging"]["flexic"]["selected"]
        scale_flexic = {0: 1, 1: 10, 2: 100, 3: 1000}[flexic_scale_factor_key]
        one_device_fps = emerging_fps["flexic"]
        fps_flexic = one_device_fps * scale_flexic
        inferences[inference_key].append(fps_flexic)


def plot_inferences(state, elem_id: str, scale_tinyml: int = 1):
    if state["presets"]["selected"] == 0:
        inference_type = "FPS (Vision)"
        # TODO(mmaz)
        emerging_1device_fps = dict(flexic=0.0001, cnt=0.01)
        act_1cpu_fps = 1000
        tinyml_1cpu_fps = 0.9
    else:
        inference_type = "FPS (Audio)"
        # TODO(mmaz)
        emerging_1device_fps = dict(flexic=0.001, cnt=0.1)
        act_1cpu_fps = 10_000
        # 10ms, source: https://docs.edgeimpulse.com/experts/machine-learning-prototype-projects/brushless-dc-motor-anomaly-detection
        tinyml_1cpu_fps = 100
    # inferences = {"system": [], "inference_type": []}
    inferences = {}
    inferences["system"] = ["TinyML", "Traditional"]
    # TODO(mmaz)
    inferences[inference_type] = [10, 20]
    inference_emerging(state, inferences, inference_type, emerging_1device_fps)
    df = pd.DataFrame(inferences)
    fig = px.bar(
        df, y="system", x=inference_type, orientation="h", title="Inferences/sec"
    )
    fig.update_layout(autosize=False, width=400, height=300)
    # max_footprint = max(1.5, sum_co2)
    # fig.update_yaxes(range=[0, 160])
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    plotly_render(graphJSON, elem_id)


def add_emerging_and_refs(state: dict, footprint: dict, co2key: str, tinyml_unscaled: dict):
    flexic_carbon_reduction_factor = 1000
    if state["emerging"]["flexic"]["enabled"]:
        flexic_scale_factor_key = state["emerging"]["flexic"]["selected"]
        scale_flexic = {0: 1, 1: 10, 2: 100, 3: 1000}[flexic_scale_factor_key]
        for tinyml_k, (heading, tinyml_co2e) in tinyml_unscaled.items():
            footprint["system"].append("FlexICs")
            footprint["component"].append(heading)
            if tinyml_k == "ml_training":
                # ml training is done once, and not scaled down
                co2e = tinyml_co2e
            elif tinyml_k in ["processor_type", "pcb"]:
                # these are the only embodied cabon reductions for flexics
                co2e = tinyml_co2e / flexic_carbon_reduction_factor * scale_flexic
            else:
                co2e = tinyml_co2e * scale_flexic
            footprint[co2key].append(co2e)
    # static reference points
    footprint["system"].append("MacBook Pro (x1)")
    footprint["component"].append("reference")
    footprint[co2key].append(349)
    footprint["system"].append("Apple Watch S7 (x1)")
    footprint["component"].append("reference")
    footprint[co2key].append(34)


def plot_co2(state, act_footprint, elem_id: str, scale_tinyml: int = 1):
    # footprint = {"system": [], "component": [], co2: []}
    footprint = {}
    footprint.update(act_footprint)
    co2 = "kg CO2"
    sum_co2 = 0
    tinyml_unscaled = {}
    for k, v in state["tinyml"].items():
        if v["enabled"]:
            if k == "scale":
                continue
            footprint["system"].append("TinyML")
            footprint["component"].append(v["heading"])
            co2e = v["options"][v["selected"]].footprint
            tinyml_unscaled[k] = (v["heading"], co2e)
            if k != "ml_training":
                # ml_training is done once, not for each device
                co2e = co2e * scale_tinyml
            footprint[co2].append(co2e)
            sum_co2 += co2e
    add_emerging_and_refs(state, footprint, co2key=co2, tinyml_unscaled=tinyml_unscaled)
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

def collapse_note():
    note = document.createElement("span")
    note.className = "mdl-color-text--grey-600"
    note.appendChild(document.createTextNode("Note: click the gear icons to hide or expand configuration sections for TinyML and ACT"))
    return note

def text_node(text: str):
    el = document.createElement("div")
    el.appendChild(document.createTextNode(text))
    return el


def _common_presets(tinyml, act):
    tinyml["casing"]["selected"] = 0
    tinyml["processor_type"]["selected"] = 1
    tinyml["pcb"]["selected"] = 1
    tinyml["power_supply"]["selected"] = 0
    tinyml["others"]["selected"] = 1
    tinyml["transport"]["selected"] = 1
    tinyml["ui"]["selected"] = 1
    tinyml["use_stage"]["selected"] = 0
    tinyml["scale"]["selected"] = 2

    act["cpu_node"]["selected"] = 0
    act["energy_source"]["selected"] = 0
    act["dram"]["selected"] = 3
    act["ssd_main"]["selected"] = 2
    act["ssd_secondary"]["selected"] = 0
    return


class App:
    def __init__(self, state):
        assert "act" in state
        assert "tinyml" in state
        self.state = state

    def preset_vision(self, _):
        tinyml = self.state["tinyml"]
        tinyml["ml_training"]["selected"] = 1
        tinyml["sensing"]["selected"] = 1
        act = self.state["act"]
        act["cpu_count"]["selected"] = 1
        _common_presets(tinyml, act)
        return self.build(None)

    def preset_anomaly(self, _):
        tinyml = self.state["tinyml"]
        tinyml["ml_training"]["selected"] = 0
        tinyml["sensing"]["selected"] = 0
        act = self.state["act"]
        act["cpu_count"]["selected"] = 0
        _common_presets(tinyml, act)
        return self.build(None)
    
    def collapse(self, state, key, _):
        state[key] = not state[key]
        return self.build(None)

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

        # this doesnt need an inner container for collapsing
        preset_container = document.createElement("div")
        preset_container.className = "calcsection"
        # preset_container.appendChild(document.createTextNode("Presets"))
        preset_container.appendChild(
            render_presets(
                self.state["presets"], [self.preset_vision, self.preset_anomaly]
            )
        )
        config_container.appendChild(preset_container)

        tinyml_container = document.createElement("div")
        tinyml_container.className = "calcsection"
        tinyml_container.appendChild(document.createTextNode("TinyML (Pirson & Bol)"))

        ci_tiny = collapse_icon("tinyml_collapse")

        add_event_listener(
            ci_tiny, "click", partial(self.collapse, self.state["expanded"], "tinyml")
        )
        tinyml_container.appendChild(ci_tiny)
        config_container.appendChild(tinyml_container)

        tinyml_inner_container = document.createElement("div")
        tinyml_inner_container.setAttribute("id", "tinyml_configuration")
        if self.state["expanded"]["tinyml"]:
            tinyml_inner_container.style.display = "block"
        else:
            tinyml_inner_container.style.display = "none"
        tinyml_container.appendChild(tinyml_inner_container)

        act_container = document.createElement("div")
        act_container.className = "calcsection"
        act_container.appendChild(document.createTextNode("Traditional Server (ACT Dell R740 Server)"))

        ci_act = collapse_icon("act_collapse")
        add_event_listener(
            ci_act, "click", partial(self.collapse, self.state["expanded"], "act")
        )
        act_container.appendChild(ci_act)
        config_container.appendChild(act_container)

        act_inner_container = document.createElement("div")
        act_inner_container.setAttribute("id", "act_configuration")
        if self.state["expanded"]["act"]:
            act_inner_container.style.display = "block"
        else:
            act_inner_container.style.display = "none"
        act_container.appendChild(act_inner_container)

        for k, v in self.state["tinyml"].items():
            tinyml_inner_container.appendChild(render_block(v, self.build))

        for k, v in self.state["act"].items():
            act_inner_container.appendChild(render_block(v, self.build))

        emerging_container = document.createElement("div")
        emerging_container.className = "calcsection"
        emerging_container.appendChild(document.createTextNode("Emerging Technologies"))
        for k, v in self.state["emerging"].items():
            emerging_container.appendChild(render_block(v, self.build))
        config_container.appendChild(emerging_container)
        config_container.appendChild(collapse_note())

        # def mycb():
        #     print(self.state)
        #     self.state["ml_training"]["enabled"] = not self.state["ml_training"]["enabled"]
        #     self.build(None)
        # app.appendChild(button(mycb))
        # app.appendChild(document.createTextNode(f"{self.state}"))

        # graph_container.appendChild(text_node("TinyML vs. Traditional Server"))
        # graph_container.appendChild(text_node("Server Inferences/sec: 100 (placeholder)"))
        # graph_container.appendChild(text_node("TinyML Inferences/sec: 1 (placeholder)"))

        tinyml_scale_factor_key = self.state["tinyml"]["scale"]["selected"]
        scale_tinyml = {0: 1, 1: 10, 2: 100, 3: 1000}[tinyml_scale_factor_key]
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
            self.state, elem_id=inference_elem_id, scale_tinyml=scale_tinyml
        )

        graph_el = document.createElement("div")
        co2_elem_id = "co2_graph"
        graph_el.setAttribute("id", co2_elem_id)
        graph_container.appendChild(graph_el)

        plot_co2(
            self.state, act_footprint, elem_id=co2_elem_id, scale_tinyml=scale_tinyml
        )

    def build(self, event):
        # if event is not None:
        #     self.update_state()

        self.render()
