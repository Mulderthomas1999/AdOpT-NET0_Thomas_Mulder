import os

import h5py
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from matplotlib.colors import to_rgba
from matplotlib.ticker import PercentFormatter
from adopt_net0 import extract_datasets_from_h5group

# Define the data path
resultfolder = "Z:/PyHub/PyHub_results/CM/Flexibility"
data_to_excel_path = 'C:/EHubversions/AdOpT-NET0_Julia/Plotting/result_data_flex.xlsx'

# select the type of plot from ['costs_spec', 'costs_spec_cor', 'emissions_spec', 'emissions_spec_cor', 'size']
plot_type = 'costs_spec_cor'

get_data = 0

if get_data == 1:
    # Define the multi-level index for rows
    columns = pd.MultiIndex.from_product(
        [
            ["Chemelot"],
            ["slow", "slowCracker", "slowSMR"],
            ["minC_ref", "minC_high"]
        ],
        names=["Location", "Type", "Scenario"]
    )

    # Define the columns
    index = ["path", "costs_tot", "emissions_tot", 'size_NaphthaCracker', 'size_NaphthaCracker_CC',
             'size_NaphthaCracker_Electric', 'size_KBRreformer', 'size_KBRreformer_CC', 'size_eSMR', 'size_AEC',
             'costs_spec', 'costs_spec_cor']

    # Create the DataFrame with NaN values
    result_data = pd.DataFrame(np.nan, index=index, columns=columns)

    # Fill the path column using a loop
    for location in result_data.columns.levels[0]:
        for typ in result_data.columns.levels[1]:
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
                                tecs = ['NaphthaCracker', 'NaphthaCracker_CC', 'NaphthaCracker_Electric', 'KBRreformer', 'KBRreformer_CC', 'eSMR', 'AEC']
                                for tec in tecs:
                                    output_name = 'size_' + tec
                                    if ('period1', location, tec, 'size') in df.columns:
                                        result_data.loc[output_name, (location, typ, scenario)] = df[('period1', location, tec, 'size')].iloc[0]
                                    else:
                                        result_data.loc[output_name, (location, typ, scenario)] = 0


    # calculate total product
    products = {
        "Chemelot": {
            "ammonia": 135 * 8760,
            "ethylene": 150 * 8760,
            "cracker_tot": None,
            "total_product": None,
            "total_product_cor": None
        },
        "Zeeland": {
                "ammonia": 208 * 8760,
                "ethylene": 208 * 8760,
                "cracker_tot": None,
                "total_product": None,
                "total_product_cor": None
        }
    }

    ethylene_yield = 0.3025

    for location in products:
        products[location]['total_product'] = products[location]['ammonia'] + products[location]['ethylene']
        products[location]['cracker_tot'] = products[location]['ethylene'] / ethylene_yield
        products[location]['total_product_cor'] = products[location]['ammonia'] + products[location]['cracker_tot']

    multipliers = {
        'NaphthaCracker': 0.3025,
        'KBR': 0.127848,
        'eSMR': 0.155736,
        'AEC': 0.105672
    }

    # Make calculations with results
    for key, multiplier in multipliers.items():
        mask = result_data.index.to_series().str.contains(key)
        result_data.loc[mask] *= multiplier

    for location in result_data.columns.levels[0]:
        for type in result_data.columns.levels[1]:
            for scenario in result_data.columns.levels[2]:

                # get specific costs and emissions
                result_data.loc['costs_spec', (location, type, scenario)] = result_data.loc['costs_tot', (
                    location, type, scenario)] / products[location]['total_product']
                result_data.loc['costs_spec_cor', (location, type, scenario)] = result_data.loc['costs_tot', (
                    location, type, scenario)] / products[location]['total_product_cor']
                result_data.loc['emissions_spec', (location, type, scenario)] = result_data.loc['emissions_tot', (
                    location, type, scenario)] / products[location]['total_product']
                result_data.loc['emissions_spec_cor', (location, type, scenario)] = result_data.loc['emissions_tot', (
                    location, type, scenario)] / products[location]['total_product_cor']

    result_data.to_excel(data_to_excel_path)


if get_data == 0:
    result_data = pd.read_excel(data_to_excel_path, index_col=0, header=[0, 1, 2])

# Configure Matplotlib to use LaTeX for text rendering and set font
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Computer Modern Roman"],
    "axes.labelsize": 12,
    "font.size": 12,
    "legend.fontsize": 10,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
})

# Select data to plot
locations = ['Chemelot']
types = ['Reference', 'slow', 'slowCracker', 'slowSMR']
scenarios = ['minC_ref', 'minC_high']

if plot_type in ['costs_spec', 'costs_spec_cor', 'emissions_spec', 'emissions_spec_cor']:
    metric = plot_type

    # Extract the relevant data from the DataFrame
    plot_data = result_data.loc[metric, locations[0]]
    plot_data = plot_data.loc[types, scenarios]

    # Initialize the plot
    fig, ax = plt.subplots(figsize=(7, 5))

    # Define custom colors and layout
    colors = ['#36151E', '#7B6D8D', '#8499B1', '#A5C4D4']
    bar_width = 0.2
    n_types = len(types)
    n_scenarios = len(scenarios)

    # Set positions of the bars
    index = np.arange(n_scenarios) * (n_types + 1) * bar_width

    legend_elements = [
        plt.Line2D([0], [0], color=colors[0], lw=4, label='Reference case'),
        plt.Line2D([0], [0], color=colors[1], lw=4, label='Limited grid capacity'),
        plt.Line2D([0], [0], color=colors[2], lw=4, label='Limited CO$_2$ T\&S capacity'),
        plt.Line2D([0], [0], color=colors[3], lw=4, label='Increased CO$_2$ T\&S capacity')
    ]

    for j, scenario in enumerate(scenarios):
        for i, typ in enumerate(types):
            position = index[j] + i * bar_width
            plt.bar(position, plot_data.loc[typ, scenario], bar_width, color=colors[i])

    # Configure x-axis and legend
    plt.xticks(index + bar_width * (n_types - 1) / 2, ['Reference CO$_2$ tax', 'High CO$_2$ tax'])
    plt.legend(handles=legend_elements, loc='upper center', ncol=2)

    # Set y-axis label and file name
    if 'cost' in metric:
        plt.ylabel('Specific costs [€/tonne product]')
        filename = locations[0] + '_flex_costs'
        ax.set_ylim(0, 2500)
        if 'cor' in metric:
            filename += '_cor'
            ax.set_ylim(0, 1000)
    elif 'emission' in metric:
        plt.ylabel('Specific emissions [kg CO$_2$/tonne product]')
        filename = locations[0] + '_flex_emissions'
        ax.set_ylim(0, 1.2)
        if 'cor' in metric:
            filename += '_cor'
            ax.set_ylim(0, 0.6)

    # Adjust layout
    plt.tight_layout()

    #save the file
    saveas = '0'

    if saveas == 'svg':
        savepath = f'C:/Users/5637635/Documents/OneDrive - Universiteit Utrecht/Images and graphs/Collection CM/Paper/{filename}.svg'
        plt.savefig(savepath, format='svg')
    elif saveas == 'pdf':
        savepath = f'C:/Users/5637635/Documents/OneDrive - Universiteit Utrecht/Images and graphs/Collection CM/Paper/{filename}.pdf'
        plt.savefig(savepath, format='pdf')


elif plot_type == 'size':
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(10, 5), sharey=True)

    tecs = {'ethylene': ['NaphthaCracker', 'NaphthaCracker_CC', 'NaphthaCracker_Electric'],
            'ammonia': ['KBRreformer', 'KBRreformer_CC', 'eSMR', 'AEC']}

    # Define custom colors for the tecs
    colors = ['#48525B', '#5277B7', '#FFBC47', '#639051']

    # Adjust bar width and gap between groups
    bar_width = 0.5  # Make the bars wider
    group_gap = 0.5  # Adjust the gap between groups
    bar_gap = 0.01

    # Preprocess tec labels
    def format_label(label):
        label = label.replace('_', ' ')
        if 'NaphthaCracker' in label:
            label = label.replace('NaphthaCracker', 'Naphtha Cracker')
        if 'KBRreformer' in label:
            label = label.replace('KBRreformer', 'KBR Reformer')
        if 'CC' in label:
            label = label.replace('CC', 'with CC')
        return label

    formatted_tecs = {product: [format_label(tec) for tec in tecs[product]] for product in tecs}

    for ax, product in zip(axes, tecs):
        n_scenarios = len(scenarios)
        n_types = len(types)

        # Calculate the total number of bars per scenario
        total_bars_per_scenario = n_types

        # Calculate the positions for each group, ensuring no extra space within groups
        index = np.arange(n_scenarios) * (total_bars_per_scenario * bar_width + group_gap)

        # Loop through each scenario
        for sc_idx, scenario in enumerate(scenarios):
            for typ_idx, typ in enumerate(types):
                position = index[sc_idx] + typ_idx * (bar_width + bar_gap)
                bottom = 0

                for tec_idx, tec in enumerate(tecs[product]):
                    metric = f'size_{tec}'
                    value = result_data.loc[metric, (locations[0], typ, scenario)]

                    color = colors[tec_idx]

                    # Plot each technology as a stacked horizontal bar
                    ax.barh(position, value, bar_width,
                            label=formatted_tecs[product][tec_idx] if sc_idx == 0 and typ_idx == 0 else "",
                            color=color, left=bottom)
                    bottom += value

        total_ticks = len(scenarios) * len(types)
        tick_positions = index + (total_bars_per_scenario - 1) * (bar_width + bar_gap) / 2
        ax.set_yticks(tick_positions)
        ax.set_yticklabels(['Reference CO$_2$ tax', 'High CO$_2$ tax'], rotation=0)

        ax.legend(loc='upper right')

        if product == 'ammonia':  # To avoid duplicate legends
            ax.set_xlabel('Size [t NH$_3$/h]')
        elif product == 'ethylene':
            ax.set_xlabel('Size [t C$_2$H$_4$/h]')

    axes[0].set_xlim(0, 225)

    # Adjust layout
    plt.tight_layout()

    # save the file
    saveas = '0'

    if saveas == 'svg':
        savepath = f'C:/Users/5637635/Documents/OneDrive - Universiteit Utrecht/Images and graphs/Collection CM/Paper/installed_capacities.svg'
        plt.savefig(savepath, format='svg')
    elif saveas == 'pdf':
        savepath = f'C:/Users/5637635/Documents/OneDrive - Universiteit Utrecht/Images and graphs/Collection CM/Paper/installed_capacities.pdf'
        plt.savefig(savepath, format='pdf')

#show plot
plt.show()