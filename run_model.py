# coding: utf-8

import os
import pickle
import sys
from concurrent.futures import ProcessPoolExecutor
from copy import deepcopy

import pandas as pd
import pysd

from logger import logger
from plot_data import plot_data

MODEL_F = "data/Uelzen.mdl"
CLIMATE_DATA_P = "data/BiasCorrection"
ADAPTATION_SPEED = "data/adaptation_speed.xlsx"
TARGET_LENGTH = 1140
"""
TODO:
- (Q) Average/Smooth or not?
    - Try smoothing without using monthly values
- can we figure out what pysd is doing when there's not enough data
    - Having mismatched input/output array lengths

TODO Rodrigo1:
- Copy paste plot data from here to rodrigo1
"""

adap_df = pd.read_excel(ADAPTATION_SPEED)
LOAD_CACHE = "--load-cache" in sys.argv
WRITE_CACHE = "--write-cache" in sys.argv

NO_ADAPTATIONS = ["Pp", "ETP"]
CASES = {
    # BAU case is used as the parameter base for all other cases
    # "BAU": {"n": 0.71, "Kc": adap_df.kc1, "Artificial Recharge": 0, "CN": 85.7, "BAU": adap_df.BAU, "NetoNull": adap_df.NetoNull, "Condition": 0},
    "BAU": {
        "n": 0.71,
        "Kc": adap_df.kc1,
        "Artificial Recharge": 0,
        "CN": 85.7,
        "BAU": adap_df.BAU,
        "NetoNull": adap_df.NetoNull,
        "Condition": 0,
        "Correction": 5.96,
    },
    "HUM": {"CN": adap_df.cn, "Correction": adap_df.correction},
    "ARC": {"Artificial Recharge": adap_df["artificial recharge"]},  # half of grey water goes into aquifer
    "PIR": {"n": adap_df.n},
    "CRP": {"Kc": adap_df.kc2},
    # "CRP+PIR+HUM": {"Kc": adap_df.kc2, "n": adap_df.n, "CN": adap_df.cn, "Correction": adap_df.correction},
}

Y_LABELS = {
    "Pp": "mean mm/month",
    "ETP": "mean mm/month",
    "Agricultural water": "Avg. monthly water demand [mm]",
    "Groundwater": "Groundwater level anomalies [mm]",
    "Consumption": "kWh / Hectar",
    "Generated": "€ / Hectar",
    "Emissions Current": "CO2 kg / Hectar",
    "Emissions Net": "CO2 kg / Hectar",
}
Y_SCALE = {
    "Pp": (58, 85),
    "ETP": (60, 75),
    "Groundwater": (-200, 600),
    "Agricultural water": (4, 10),
    "Consumption": (25, 60),
    "Emissions Current": (5, 45),
    "Emissions Net": (5, 45),
}

# read in Vensim model
MODEL = pysd.read_vensim(MODEL_F)
# RCP list and colors of RCPs
RCPS = ["rcp26", "rcp45", "rcp85"]

# add here the output variables with units
OUTPUT_VAR_LIST = [
    "Groundwater",
    "Pp",
    "ETP",
    "Agricultural water",
    "Consumption",  # energy
    "Generated",  # Costs
    "Emissions Current",  # CO2
    "Emissions Net",  # CO2
]  # Names in the model

region = "Seewinkel"


def prep_data(f, extra_params):
    df = pd.read_excel(f)
    # df["KC"] = df.Date.dt.month.apply(lambda x: KCS[kc].get(x, 0))
    extra_params = deepcopy(extra_params)
    # if "CN_target" in extra_params:
    #     cn_target = extra_params.pop("CN_target")
    #     base_cn = extra_params.pop("CN")
    #     monthly_change = (base_cn - cn_target) / TARGET_LENGTH
    #     extra_params["CN"] = pd.Series([base_cn - monthly_change * (i + 1) for i in df.index])
    return df, extra_params


def run_sim(rcp, var, run_name, **extra_params):
    _files = sorted(filter(lambda x: x.startswith("met_0") and not x.endswith("_no_historical"), os.listdir(CLIMATE_DATA_P)))
    i_rcm = 0
    output_data = []
    output_index = None
    for data_dir in _files:
        # data_file = os.path.join(rcp_data_d, data_dir, "dr_reshape.xlsx")
        data_file = os.path.join(CLIMATE_DATA_P, data_dir, f"{rcp}biascorrected.xlsx")
        if not os.path.exists(data_file):
            continue

        # read in climate data from .xlsx file
        try:
            i_data, extra_params = prep_data(data_file, extra_params)
            if len(i_data) < TARGET_LENGTH:
                print(f"{data_file} has incorrect length of {len(i_data)}")
                continue
            if output_index is None:
                i_data["Date"] = i_data.Date.dt.normalize()
                output_index = i_data.set_index("Date").index
        except FileNotFoundError:
            logger.info(f"Could not find file at path {data_file}")

        # run Vensim model, provide input and ouput (return_columns)
        params = {"Pp": i_data["Pp"], "ETP": i_data["ETr"]}
        if extra_params:
            params.update(extra_params)
        # _df = pd.DataFrame(params)
        # _df.to_excel(f"input_params/{run_name}_{data_dir.replace('/','_')}.xlsx")
        data = MODEL.run(params=params, return_columns=[var])
        data = data.iloc[len(data) - len(output_index) :]
        data = data.rename({var: data_dir}, axis=1)
        data = data.set_index(output_index)
        output_data.append(data)
        i_rcm += 1
    output_data = pd.concat(output_data, axis=1)
    logger.info(f"Processed {i_rcm} files for {rcp=}, {var=}")
    return output_data


def annual_mean(df):
    df = df.melt(var_name="Case", value_name="value", id_vars="Date")
    df["Date"] = df["Date"].apply(lambda x: pd.Timestamp(year=x.year, month=1, day=1))
    df = pd.DataFrame({"value": df.groupby(["Date"]).mean().value}).reset_index()
    return df


def _load_cache(name):
    try:
        with open(f".cache/{name}", "rb") as f:
            args = pickle.load(f)
        return args
    except FileNotFoundError:
        return False


def _run_single(target_var, rcp, run_name):
    target_var_df = None
    for case_name, params in CASES.items():
        _params = params if case_name != "BAU" else None
        logger.info(f"Processing model for {target_var=}, {rcp=}, adapted_params='{list(_params.keys()) if _params is not None else None}'")
        if case_name != "BAU":
            params = CASES["BAU"] | params
        if target_var == "Emissions Current":
            target_var_name = "Emissions"
            params = deepcopy(params) | {"Condition": 0}
        elif target_var == "Emissions Net":
            target_var_name = "Emissions"
            params = deepcopy(params) | {"Condition": 1}
        else:
            target_var_name = target_var
        df = run_sim(rcp, target_var_name, case_name + "_" + run_name, **params).reset_index()
        df = annual_mean(df)
        df = df.rename({"value": f"{case_name}"}, axis=1)
        target_var_df = target_var_df.merge(df, on="Date") if target_var_df is not None else df

    return target_var_df


def run_single(target_var, rcp):
    run_name = f"{target_var} - {rcp.upper()}"

    df = _load_cache(run_name) if LOAD_CACHE else None
    if df is None:
        df = _run_single(target_var, rcp, run_name)
        if WRITE_CACHE:
            with open(f".cache/{target_var} - {rcp.upper()}", "wb") as f:
                pickle.dump(df, f)
            df.to_excel(f"output_data/{target_var} - {rcp.upper()}.xlsx", index=False)
    if target_var in NO_ADAPTATIONS:
        plot_data(df=df, cases=["BAU"], y_label=Y_LABELS[target_var], y_scale=Y_SCALE.get(target_var), name=run_name)
    else:
        plot_data(df=df, cases=list(CASES.keys()), y_label=Y_LABELS[target_var], y_scale=Y_SCALE.get(target_var), name=run_name)


def run_all(procs=0):
    if procs:
        pool = ProcessPoolExecutor(max_workers=procs)
    jobs = []
    for target_var in OUTPUT_VAR_LIST:
        for rcp in RCPS:
            if procs:
                jobs.append(pool.submit(run_single, target_var, rcp))
            else:
                run_single(target_var, rcp)
    if procs:
        while True:
            for job in list(jobs):
                if job.done():
                    if job.exception():
                        raise job.exception()
                    jobs.remove(job)
            if not jobs:
                break


if __name__ == "__main__":
    os.makedirs("plots", exist_ok=True)
    if WRITE_CACHE:
        os.makedirs(".cache", exist_ok=True)
    os.makedirs("output_data", exist_ok=True)
    os.makedirs("input_params", exist_ok=True)
    multi = int(sys.argv[1]) if (len(sys.argv) > 1 and not sys.argv[1].startswith("--")) else 0
    data = run_all(multi)
