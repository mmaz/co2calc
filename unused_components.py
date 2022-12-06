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

