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
resultfolder = "Z:/PyHub/PyHub_results/CM/Cluster_integration"
data_to_excel_path = 'C:/EHubversions/AdOpT-NET0_Julia/Plotting/result_data.xlsx'

# select the type of plot from ['costs_spec', 'costs_spec_cor', 'emissions_spec', 'emissions_spec_cor', 'size']
plot_type = 'emissions_spec_cor'

get_data = 0

if get_data == 1:
    # Define the multi-level index for rows
    columns = pd.MultiIndex.from_product(
        [
            ["Chemelot", "Zeeland"],
            ["cluster", "ethylene", "ammonia", "standalone"],
            ["minC_ref", "minC_high", "minE"]
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
        for scenario in result_data.columns.levels[2]:
            for row in result_data.index:
                if row != 'path':
                    result_data.loc[row, (location, 'standalone', scenario)] = result_data.loc[row, (
                    location, 'ethylene', scenario)] + result_data.loc[row, (location, 'ammonia', scenario)]
                else:
                    result_data.loc[row, (location, 'standalone', scenario)] = None

            # get specific costs and emissions
            result_data.loc['costs_spec', (location, 'cluster', scenario)] = result_data.loc['costs_tot', (
                location, 'cluster', scenario)] / products[location]['total_product']
            result_data.loc['costs_spec_cor', (location, 'cluster', scenario)] = result_data.loc['costs_tot', (
                location, 'cluster', scenario)] / products[location]['total_product_cor']
            result_data.loc['emissions_spec', (location, 'cluster', scenario)] = result_data.loc['emissions_tot', (
                location, 'cluster', scenario)] / products[location]['total_product']
            result_data.loc['emissions_spec_cor', (location, 'cluster', scenario)] = result_data.loc['emissions_tot', (
                location, 'cluster', scenario)] / products[location]['total_product_cor']

            result_data.loc['costs_spec', (location, 'ethylene', scenario)] = result_data.loc['costs_tot', (
                location, 'ethylene', scenario)] / products[location]['ethylene']
            result_data.loc['costs_spec_cor', (location, 'ethylene', scenario)] = result_data.loc['costs_tot', (
                location, 'ethylene', scenario)] / products[location]['cracker_tot']
            result_data.loc['emissions_spec', (location, 'ethylene', scenario)] = result_data.loc['emissions_tot', (
                location, 'ethylene', scenario)] / products[location]['ethylene']
            result_data.loc['emissions_spec_cor', (location, 'ethylene', scenario)] = result_data.loc['emissions_tot', (
                location, 'ethylene', scenario)] / products[location]['cracker_tot']

            result_data.loc['costs_spec', (location, 'ammonia', scenario)] = result_data.loc['costs_tot', (
                location, 'ammonia', scenario)] / products[location]['ammonia']
            result_data.loc['emissions_spec', (location, 'ammonia', scenario)] = result_data.loc['emissions_tot', (
                location, 'ammonia', scenario)] / products[location]['ammonia']

            result_data.loc['costs_spec', (location, 'standalone', scenario)] = result_data.loc['costs_tot', (
                location, 'standalone', scenario)] / products[location]['total_product']
            result_data.loc['costs_spec_cor', (location, 'standalone', scenario)] = result_data.loc['costs_tot', (
                location, 'standalone', scenario)] / products[location]['total_product_cor']
            result_data.loc['emissions_spec', (location, 'standalone', scenario)] = result_data.loc['emissions_tot', (
                location, 'standalone', scenario)] / products[location]['total_product']
            result_data.loc['emissions_spec_cor', (location, 'standalone', scenario)] = result_data.loc['emissions_tot', (
                location, 'standalone', scenario)] / products[location]['total_product_cor']

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
    "xtick.labelsize": 12,
    "ytick.labelsize": 12,
})

# Select data to plot
locations = ['Chemelot', 'Zeeland']
types = ['cluster', 'standalone']
scenarios = ['minC_ref', 'minC_high']

if plot_type in ['costs_spec', 'costs_spec_cor', 'emissions_spec', 'emissions_spec_cor']:
    metric = plot_type

    # Extract the relevant data from the DataFrame and prepare data
    plot_data = result_data.loc[metric, locations[0]]
    plot_data = plot_data.loc[types, scenarios]

    # Plotting
    fig, ax = plt.subplots(figsize=(5.5, 3))

    # Define custom colors and layout
    colors = ['#F1DAC4', '#474973']
    bar_width = 0.1
    n_types = len(types)
    n_scenarios = len(scenarios)
    n_locations = len(locations)
    total_bars = n_types * n_scenarios

    # Set positions of the bars
    index = np.arange(n_locations) * (total_bars + 1) * bar_width

    # Create custom patches for the legend
    legend_elements = [
        plt.Line2D([0], [0], color=colors[0], lw=4, alpha=0.5, label='cluster (R-CO$_2$P)'),
        plt.Line2D([0], [0], color=colors[0], lw=4, label='cluster (H-CO$_2$P)'),
        plt.Line2D([0], [0], color=colors[1], lw=4, alpha=0.5, label='standalone (R-CO$_2$P)'),
        plt.Line2D([0], [0], color=colors[1], lw=4,  label='standalone (H-CO$_2$P)')
    ]

    # Plot each location
    for loc_idx, location in enumerate(locations):
        plot_data = result_data.loc[metric, location].loc[types, scenarios]

        # Plot each scenario for each type
        for j, scenario in enumerate(scenarios):
            for i, typ in enumerate(types):
                position = index[loc_idx] + (i * n_scenarios + j) * bar_width
                if scenario == 'minC_ref':
                    plt.bar(position, plot_data.loc[typ, scenario], bar_width,
                            label=None, color=colors[i], alpha=0.5)
                elif scenario == 'minC_high':
                    plt.bar(position, plot_data.loc[typ, scenario], bar_width,
                            label=None, color=colors[i])

    if metric in ['emissions_spec', 'emissions_spec_cor']:
        line_styles = ['--', ':']  # Different line styles for different locations
        for loc_idx, location in enumerate(locations):
            for i, typ in enumerate(types):
                minE_value = result_data.loc[metric, location].loc[typ, 'minE']
                plt.axhline(y=minE_value, color=colors[i], linestyle=line_styles[loc_idx],
                            label=f'{typ} (minE, {location})')

    # Adding labels and title
    plt.xticks(index + bar_width * (total_bars - 1) / 2, locations)
    if 'emission' in metric:
        plt.legend(handles=legend_elements + [
            plt.Line2D([0], [0], color=colors[0], linestyle='--', label='cluster min. (Chemelot)'),
            plt.Line2D([0], [0], color=colors[0], linestyle=':', label='cluster min. (Zeeland)'),
            plt.Line2D([0], [0], color=colors[1], linestyle='--', label='standalone min. (Chemelot)'),
            plt.Line2D([0], [0], color=colors[1], linestyle=':', label='standalone min. (Zeeland)')
        ], loc='upper center', ncol=2)
    else:
        plt.legend(handles=legend_elements, loc='upper center', ncol=2)

    # define filename
    if 'cost' in metric:
        plt.ylabel('Specific costs [€/tonne product]')
        filename = 'integration_costs'
        ax.set_ylim(0, 2500)
        if 'cor' in metric:
            filename = filename + '_cor'
            ax.set_ylim(0, 1400)
    elif 'emission' in metric:
        plt.ylabel(r'Specific emissions \\[0.1em] [kg CO$_2$/tonne product]')
        filename = 'integration_emissions'
        ax.set_ylim(0, 1.4)
        if 'cor' in metric:
            filename = filename + '_cor'
            ax.set_ylim(0, 0.8)

    # Adjust layout
    plt.tight_layout()

    #save the file
    saveas = 'both'

    if saveas == 'svg':
        savepath = f'C:/Users/5637635/Documents/OneDrive - Universiteit Utrecht/Images and graphs/Collection CM/PaperFinal/{filename}.svg'
        plt.savefig(savepath, format='svg')
    elif saveas == 'pdf':
        savepath = f'C:/Users/5637635/Documents/OneDrive - Universiteit Utrecht/Images and graphs/Collection CM/PaperFinal/{filename}.pdf'
        plt.savefig(savepath, format='pdf')
    elif saveas == 'both':
        savepath = f'C:/Users/5637635/Documents/OneDrive - Universiteit Utrecht/Images and graphs/Collection CM/PaperFinal/{filename}.pdf'
        plt.savefig(savepath, format='pdf')
        savepath = f'C:/Users/5637635/Documents/OneDrive - Universiteit Utrecht/Images and graphs/Collection CM/PaperFinal/{filename}.svg'
        plt.savefig(savepath, format='svg')


elif plot_type == 'size':
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(10, 5), sharey=True)

    tecs = {'ethylene': ['NaphthaCracker', 'NaphthaCracker_CC', 'NaphthaCracker_Electric'],
            'ammonia': ['KBRreformer', 'KBRreformer_CC', 'eSMR', 'AEC']}

    # Define custom colors for the tecs
    # colors = ['#3B252C', '#8F6593', '#AEA4BF', '#CDCDCD']
    # colors = ['#422439', '#BDA0BC', '#C3D2D5', '#C1F7DC']
    colors = ['#48525B', '#5277B7', '#FFBC47', '#639051']


    # Adjust bar width and gap between groups
    bar_width = 0.5  # Make the bars wider
    group_gap = 0.5  # Adjust the gap between groups
    bar_gap = 0.01
    opacity = 1

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
        n_locations = len(locations)
        n_scenarios = len(scenarios)
        n_types = len(types)

        # Calculate the total number of bars per location
        total_bars_per_loc = n_scenarios * n_types

        # Calculate the positions for each group, ensuring no extra space within groups
        index = np.arange(n_locations) * (total_bars_per_loc * bar_width + group_gap)

        # Loop through each location
        for loc_idx, location in enumerate(reversed(locations)):
            for typ_idx, typ in enumerate(reversed(types)):
                for sc_idx, scenario in enumerate(reversed(scenarios)):
                    position = index[loc_idx] + (sc_idx + typ_idx * n_scenarios) * (bar_width + bar_gap)
                    bottom = 0

                    for tec_idx, tec in enumerate(tecs[product]):
                        metric = f'size_{tec}'
                        value = result_data.loc[metric, (location, typ, scenario)]

                        if scenario == 'minC_ref':
                            opacity = 0.5
                        else:
                            opacity = 1

                        color = to_rgba(colors[tec_idx], alpha=opacity)

                        # Plot each technology as a stacked horizontal bar
                        ax.barh(position, value, bar_width,
                                label=formatted_tecs[product][tec_idx] if loc_idx == 0 and typ_idx == 0 and sc_idx == 0 else "",
                                color=color, left=bottom)
                        bottom += value

        # ax.set_title(f'{product.capitalize()} Production')
        # tick_positions = np.arange(n_locations) * (total_bars_per_loc * bar_width + group_gap) + (
        #         total_bars_per_loc * bar_width / 2) - 0.23
        # ax.set_yticks(tick_positions)
        # ax.set_yticklabels(reversed(locations), rotation=0)

        total_ticks = len(locations) * len(types)
        tick_positions = np.arange(total_ticks) * (total_bars_per_loc/2 * bar_width) + (total_bars_per_loc/2 * bar_width / 2) - 0.23
        tick_positions[2] = tick_positions[2] + group_gap
        tick_positions[3] = tick_positions[3] + group_gap
        ytick_labels = [f'{loc}-{typ}' for loc in reversed(locations) for typ in reversed(types)]
        ax.set_yticks(tick_positions)
        ax.set_yticklabels(ytick_labels, rotation=0)


        ax.legend(loc='upper right')

        if product == 'ammonia':  # To avoid duplicate legends
            ax.set_xlabel('Size [t NH$_3$/h]')
        elif product == 'ethylene':
            ax.set_xlabel('Size [t C$_2$H$_4$/h]')

    axes[0].set_xlim(0, 225)

    # Adjust layout
    plt.tight_layout()

    # save the file
    saveas = 'pdf'

    if saveas == 'svg':
        savepath = f'C:/Users/5637635/Documents/OneDrive - Universiteit Utrecht/Images and graphs/Collection CM/Paper/installed_capacities.svg'
        plt.savefig(savepath, format='svg')
    elif saveas == 'pdf':
        savepath = f'C:/Users/5637635/Documents/OneDrive - Universiteit Utrecht/Images and graphs/Collection CM/Paper/installed_capacities.pdf'
        plt.savefig(savepath, format='pdf')

#show plot
plt.show()