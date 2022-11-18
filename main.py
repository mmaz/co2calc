import elements as e

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

tinyml_state = dict(
    ml_training=dict(
        enabled=True,
        heading="ML Training",
        docid="tr",
        options=[
            e.BlockOption(desc="DenseNet", footprint=0.1),
            e.BlockOption(desc="MobileNetV1", footprint=0.1),
        ],
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
    processor_type=dict(
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
    scale=dict(
        enabled=True,
        heading="Scale Factor",
        docid="scale_factor",
        options=[
            e.BlockOption(desc="Individual", footprint=0, act_desc="1x"),
            e.BlockOption(desc="Small Scale", footprint=0, act_desc="10x"),
            e.BlockOption(desc="Medium Scale", footprint=0, act_desc="100x"),
            e.BlockOption(desc="Large Scale", footprint=0, act_desc="1,000x"),
        ],
        selected=3,
    ),
)


def main():
    app = e.App(dict(act=act_state, tinyml=tinyml_state))
    app.build(None)


main()
