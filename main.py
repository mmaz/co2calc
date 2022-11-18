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
    dram=dict(
        enabled=True,
        heading="DRAM",
        docid="dram_footprint",
        options=[
            e.BlockOption(
                desc="36 GB",
                footprint=0,
                act_desc="32 GB + 4 ECC GB x 1",
                act_param="1",
            ),
            e.BlockOption(
                desc="144 GB",
                footprint=0,
                act_desc="32 GB + 4 ECC GB x 4",
                act_param="4",
            ),
        ],
        selected=0,
    ),
)

tinyml_state = dict(
    ml_training=dict(
        enabled=True,
        heading="ML Training",
        docid="tr",
        options=[e.BlockOption(desc="DenseNet", footprint=0.1)],
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
    connectivity=dict(
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
)


def main():
    app = e.App(dict(act=act_state, tinyml=tinyml_state))
    app.build(None)


main()
