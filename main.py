from js import document, componentHandler
# https://jeff.glass/post/whats-new-pyscript-2022-09-1/
from pyodide.ffi.wrappers import add_event_listener
from pyodide.code import run_js

state = {i : 25 for i in range(10)}

def f(event):
    print("f", event)

def button():
    e = document.createElement("button")
    e.className = "mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--accent"
    e.appendChild(document.createTextNode("Build"))
    componentHandler.upgradeElement(e)
    add_event_listener(e, "click", f)
    return e

def build(event):
    if event is not None:
        # print(event)
        for i in range(3):
            e = document.getElementById(f"state{i}")
            # v = str(e.getAttribute("value"))
            v = int(e.value)
            # print(v)
            state[i] = v

    app = document.getElementById("app")
    app.innerHTML = ""
    for i in range(3):
        app.appendChild(slider(state, i))
    app.appendChild(button())


# def q(event):
#     for i in range(3):
#         e = document.getElementById(f"state{i}")
#         # v = str(e.getAttribute("value"))
#         # v = str(e.getAttribute("value"))
#         print(e.value)

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

def slider(state, i):
    # <input class="mdl-slider mdl-js-slider" type="range"
    #   min="0" max="100" value="25" tabindex="0">
    slider = document.createElement("div")
    e = document.createElement("input")
    e.className = "mdl-slider mdl-js-slider"
    slider_id = f"state{i}"
    e.setAttribute("id", slider_id)
    e.setAttribute("type", "range")
    e.setAttribute("min", "0")
    e.setAttribute("max", "100")
    e.setAttribute("step", "1")
    e.setAttribute("value", f"{state[i]}")
    e.setAttribute("tabindex", "0")
    slider.appendChild(e)

    value_display = document.createElement("div")
    value_display.innerHTML = f"{state[i]}"
    def update_value_display(_):
        e = document.getElementById(slider_id)
        value_display.innerHTML = e.value
    add_event_listener(e, "input", update_value_display)
    add_event_listener(e, "change", build)
    componentHandler.upgradeElement(e)
    return make_cols([(slider, 11), (value_display, 1)])

def main():
    build(None)

main()