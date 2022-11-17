from dram_model import Fab_DRAM
import json
from pathlib import Path
# from pyodide.http import pyfetch

# async def request(url):
#     kwargs = {"method": "GET", "mode": "cors"}
#     response = await pyfetch(url, **kwargs)
#     return response



# async def foo():
#     res = await request("http://markmaz.com/co2calc/ACT/dram/dram_hynix.json")
#     print(res)

    # j = json.loads(Path("http://markmaz.com/co2calc/ACT/dram/dram_hynix.json").read_text())
    # return j["lpddr3_30nm"]
def foo():
    return Fab_DRAM().get_cpg()