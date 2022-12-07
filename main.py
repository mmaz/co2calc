import elements as e

preset_state = dict(
    enabled=True,
    heading="Application Presets",
    docid="preset_id",
    options=[
        e.BlockOption(
            desc="Vision",
            footprint=0,
            act_desc="Classifier/Features",
            act_param="",
        ),
        e.BlockOption(
            desc="Anomaly Detection", footprint=0, act_desc="Autoencoder", act_param=""
        ),
    ],
    selected=0,
)

act_state = dict(
    cpu_node=dict(
        enabled=True,
        heading="CPU Process Node",
        docid="cpu_process_node",
        options=[
            e.BlockOption(
                desc="Intel Xeon/Dell R740",
                footprint=0,
                act_desc="28nm",
                act_param="28nm",
            ),
            e.BlockOption(
                desc="Ivy Bridge", footprint=0, act_desc="14nm", act_param="14nm"
            ),
        ],
        selected=0,
    ),
    cpu_count=dict(
        enabled=True,
        heading="CPU Count",
        docid="cpu_count",
        options=[
            e.BlockOption(desc="1 CPU", footprint=0, act_desc="", act_param=1),
            e.BlockOption(desc="2 CPUs", footprint=0, act_desc="", act_param=2),
            e.BlockOption(desc="4 CPUs", footprint=0, act_desc="", act_param=4),
            e.BlockOption(desc="8 CPUs", footprint=0, act_desc="", act_param=8),
        ],
        selected=1,
    ),
    #   "coal"       : 820,
    #   "gas"        : 490,
    #   "biomass"    : 230,
    #   "solar"      : 41,
    #   "geothermal" : 38,
    #   "hydropower" : 24,
    #   "nuclear"    : 12,
    #   "wind"       : 11
    energy_source=dict(
        enabled=True,
        heading="Energy Source",
        docid="energy_source",
        options=[
            e.BlockOption(
                desc="Coal",
                footprint=0,
                act_desc="820",
                act_param="coal",
            ),
            e.BlockOption(
                desc="Natural Gas",
                footprint=0,
                act_desc="490",
                act_param="gas",
            ),
            e.BlockOption(
                desc="Solar",
                footprint=0,
                act_desc="41",
                act_param="solar",
            ),
            e.BlockOption(
                desc="Nuclear",
                footprint=0,
                act_desc="12",
                act_param="nuclear",
            ),
        ],
        selected=0,
    ),
    dram=dict(
        enabled=True,
        heading="DRAM",
        docid="dram_footprint",
        options=[
            e.BlockOption(
                desc="36 GB",
                footprint=0,
                act_desc="32 GB + 4 ECC GB x 1",
                act_param=1,
            ),
            e.BlockOption(
                desc="144 GB",
                footprint=0,
                act_desc="32 GB + 4 ECC GB x 4",
                act_param=4,
            ),
            e.BlockOption(
                desc="288 GB",
                footprint=0,
                act_desc="32 GB + 4 ECC GB x 8",
                act_param=8,
            ),
            e.BlockOption(
                desc="432 GB",
                footprint=0,
                act_desc="32 GB + 4 ECC GB x 12",
                act_param=12,
            ),
        ],
        selected=3,
    ),
)

emerging_tech = dict(
    flexic=dict(
        enabled=True,
        heading="Flexible Circuits",
        docid="flexics",
        options=[
            e.BlockOption(desc="Individual", footprint=0, act_desc="1x"),
            e.BlockOption(desc="Small Scale", footprint=0, act_desc="10x"),
            e.BlockOption(desc="Medium Scale", footprint=0, act_desc="100x"),
            e.BlockOption(desc="Large Scale", footprint=0, act_desc="1,000x"),
        ],
        selected=2,
    ),
)

tinyml_state = dict(
    ml_training=dict(
        enabled=True,
        heading="ML Training",
        docid="tinyml_training",
        options=[
            e.BlockOption(desc="DenseNet", footprint=0.1),
            e.BlockOption(desc="MobileNetV1", footprint=0.1),
        ],
        selected=1,
    ),
    casing=dict(
        enabled=True,
        heading="Casing",
        docid="tinyml_casing",
        options=[
            e.BlockOption(desc="small", footprint=0.04),
            e.BlockOption(desc="medium", footprint=0.27),
            e.BlockOption(desc="large", footprint=0.63),
        ],
        selected=0,
    ),
    processor_type=dict(
        enabled=True,
        heading="Processing",
        docid="tinyml_processor_type",
        options=[
            e.BlockOption(desc="HSL-0 low", footprint=0.08),
            e.BlockOption(desc="HSL-0 typical", footprint=0.17),
            e.BlockOption(desc="HSL-0 high", footprint=0.29),
        ],
        selected=1,
    ),
    pcb=dict(
        enabled=True,
        heading="PCB",
        docid="tinyml_pcb",
        options=[
            e.BlockOption(desc="HSL-0 small", footprint=0.13),
            e.BlockOption(desc="HSL-0 typical", footprint=0.16),
            e.BlockOption(desc="HSL-0 large", footprint=0.24),
        ],
        selected=1,
    ),
    power_supply=dict(
        enabled=True,
        heading="Power Supply",
        docid="tinyml_power_supply",
        options=[
            e.BlockOption(desc="Mains powered", footprint=0.52),
            e.BlockOption(desc="Li-ion battery (typical)", footprint=1.36),
            e.BlockOption(desc="Li-ion battery (large)", footprint=2.71),
        ],
        selected=0,
    ),
    sensing=dict(
        enabled=True,
        heading="Sensing",
        docid="tinyml_sensing",
        options=[
            e.BlockOption(desc="Microphone", footprint=0.03),
            e.BlockOption(desc="Vision (Typical)", footprint=0.77),
            e.BlockOption(desc="Vision (Worst case)", footprint=1.47),
        ],
        selected=1,
    ),
    others=dict(
        enabled=True,
        heading="Others",
        docid="tinyml_others",
        options=[
            e.BlockOption(desc="HSL-0 Best case", footprint=0.06),
            e.BlockOption(desc="HSL-0 Typical", footprint=0.11),
            e.BlockOption(desc="HSL-0 Worst case", footprint=0.14),
        ],
        selected=1,
    ),
    transport=dict(
        enabled=True,
        heading="Transport",
        docid="tinyml_transport",
        options=[
            e.BlockOption(desc="HSL-1 Best case", footprint=0.18),
            e.BlockOption(desc="HSL-1 Typical", footprint=0.4),
            e.BlockOption(desc="HSL-1 Worst case", footprint=1.35),
        ],
        selected=1,
    ),
    ui=dict(
        enabled=True,
        heading="Indicator LED UI",
        docid="tinyml_ui",
        options=[
            e.BlockOption(desc="HSL-1 Best case", footprint=0.03),
            e.BlockOption(desc="HSL-1 Typical", footprint=0.06),
            e.BlockOption(desc="HSL-1 Worst case", footprint=0.12),
        ],
        selected=1,
    ),
    use_stage=dict(
        enabled=True,
        heading="Use-Stage",
        docid="tinyml_use_stage",
        options=[
            e.BlockOption(desc="Continuous 1mW", footprint=0.01),
        ],
        selected=0,
    ),
    scale=dict(
        enabled=True,
        heading="Scale Factor",
        docid="tinyml_scale_factor",
        options=[
            e.BlockOption(desc="Individual", footprint=0, act_desc="1x"),
            e.BlockOption(desc="Small Scale", footprint=0, act_desc="10x"),
            e.BlockOption(desc="Medium Scale", footprint=0, act_desc="100x"),
            e.BlockOption(desc="Large Scale", footprint=0, act_desc="1,000x"),
        ],
        selected=2,
    ),
)


def main():
    app = e.App(
        dict(
            presets=preset_state,
            act=act_state,
            tinyml=tinyml_state,
            emerging=emerging_tech,
            expanded=dict(tinyml=True, act=True),
        )
    )
    app.preset_vision(None)


main()
