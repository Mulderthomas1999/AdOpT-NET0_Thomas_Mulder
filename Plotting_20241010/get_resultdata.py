import os

import h5py
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from matplotlib.colors import to_rgba
from matplotlib.ticker import PercentFormatter
from adopt_net0 import extract_datasets_from_h5group

result_type = 'Infrastructure'

# Define the data path
resultfolder = "Z:/PyHub/PyHub_results/CM/" + result_type
data_to_excel_path = 'C:/EHubversions/AdOpT-NET0_Julia/Plotting/result_data_long3.xlsx'

get_data = 1

if get_data == 1:
    # Define the multi-level index for rows
    if result_type == 'Infrastructure':
        columns = pd.MultiIndex.from_product(
            [
                ["Chemelot", "Zeeland"],
                ["CO2lim0", "CO2limHigh", "eleclim",],
                ["minC_ref", "minC_high"]
            ],
            names=["Location", "Type", "Scenario"]
        )
    elif result_type == 'Cluster_integration':
        columns = pd.MultiIndex.from_product(
            [
                ["Chemelot", "Zeeland"],
                ["cluster", "ethylene", "ammonia", "standalone"],
                ["minC_ref", "minC_high", "minE"]
            ],
            names=["Location", "Type", "Scenario"]
        )

    # Define the columns
    index = ["path", "costs_tot", "emissions_tot"]

    # Create the DataFrame with NaN values
    result_data = pd.DataFrame(np.nan, index=index, columns=columns)

    # Fill the path column using a loop
    for location in result_data.columns.levels[0]:
        for typ in result_data.columns.levels[1]:
            if typ not in ['standalone']:
                folder_name = f"{location}_{typ}"
                summarypath = os.path.join(resultfolder, folder_name, "Summary.xlsx")
                summary_results = pd.read_excel(summarypath)

                for scenario in result_data.columns.levels[2]:
                    for case in summary_results['case']:
                        if pd.notna(case) and scenario in case:
                            h5_path = Path(summary_results[summary_results['case'] == case].iloc[0]['time_stamp']) / "optimization_results.h5"
                            result_data.loc["path", (location, typ, scenario)] = h5_path
                            result_data.loc["costs_tot", (location, typ, scenario)] = summary_results[summary_results['case'] == case].iloc[0]['total_npv']
                            result_data.loc["emissions_tot", (location, typ, scenario)] = summary_results[summary_results['case'] == case].iloc[0]['emissions_pos']

                            if h5_path.exists():
                                with h5py.File(h5_path, "r") as hdf_file:
                                    df = extract_datasets_from_h5group(hdf_file["design/nodes"])
                                    # tecs = ['NaphthaCracker', 'NaphthaCracker_CC', 'NaphthaCracker_Electric', 'KBRreformer', 'KBRreformer_CC', 'eSMR', 'AEC']
                                    for tec in df.columns.levels[2]:
                                        output_name = 'size_' + tec
                                        if ('period1', location, tec, 'size') in df.columns:
                                            result_data.loc[output_name, (location, typ, scenario)] = df[('period1', location, tec, 'size')].iloc[0]
                                        else:
                                            result_data.loc[output_name, (location, typ, scenario)] = 0

                                    df1 = extract_datasets_from_h5group(hdf_file["operation/energy_balance"])
                                    cars_at_node = (
                                        df1['period1', location].columns.droplevel([1]).unique()
                                    )
                                    for car in cars_at_node:
                                        parameters = ["import", "export"]
                                        for para in parameters:
                                            output_name = (
                                                f"{car}/{para}_max"
                                            )
                                            if ('period1', location, car, para) in df1.columns:
                                                car_output = df1['period1', location, car, para]
                                                result_data.loc[output_name, (location, typ, scenario)] = max(car_output)
                                            else:
                                                result_data.loc[output_name, (location, typ, scenario)] = 0

    result_data.to_excel(data_to_excel_path)


if get_data == 0:
    result_data = pd.read_excel(data_to_excel_path, index_col=0, header=[0, 1, 2])

