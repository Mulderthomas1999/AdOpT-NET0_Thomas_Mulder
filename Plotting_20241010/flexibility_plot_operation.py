import os
import h5py
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from matplotlib.colors import to_rgba
from adopt_net0 import extract_datasets_from_h5group, extract_dataset_from_h5

# Define the data paths
RESULT_FOLDER = "Z:/PyHub/PyHub_results/CM/Cluster_integration"
DATA_TO_EXCEL_PATH = 'C:/EHubversions/AdOpT-NET0_Julia/Plotting/operation_flex_import.xlsx'
DATA_TO_EXCEL_PATH1 = 'C:/EHubversions/AdOpT-NET0_Julia/Plotting/operation_flex.xlsx'
DATAPATH = "C:/EHubversions/AdOpT-NET0_Julia/Plotting"
EL_LOAD_PATH = Path(DATAPATH) / 'Electricity_data_CM.csv'

def fetch_and_process_data_import(resultfolder, data_to_excel_path):
    """
    Fetch data from HDF5 files, process it, and save the results to an Excel file.
    """
    columns = pd.MultiIndex.from_product(
        [
            ["Chemelot", "Zeeland"],
            ["cluster"],
            ["minC_ref", "minC_high"]
        ],
        names=["Location", "Type", "Scenario"]
    )

    result_data = pd.DataFrame(np.nan, index=range(8760), columns=columns)

    for location in result_data.columns.levels[0]:
        for typ in result_data.columns.levels[1]:
            folder_name = f"{location}_{typ}"
            summarypath = os.path.join(resultfolder, folder_name, "Summary.xlsx")
            summary_results = pd.read_excel(summarypath)

            for scenario in result_data.columns.levels[2]:
                for case in summary_results['case']:
                    if pd.notna(case) and scenario in case:
                        h5_path = Path(summary_results[summary_results['case'] == case].iloc[0][
                                           'time_stamp']) / "optimization_results.h5"
                        if h5_path.exists():
                            with h5py.File(h5_path, "r") as hdf_file:
                                df = extract_datasets_from_h5group(hdf_file["operation/energy_balance"])
                                car = "electricity"
                                para = "import"
                                if ('period1', location, car, para) in df.columns:
                                    car_output = df['period1', location, car, para]
                                    result_data.loc[:, (location, typ, scenario)] = car_output
                                else:
                                    result_data.loc[:, (location, typ, scenario)] = 0

    result_data.to_excel(data_to_excel_path)


def fetch_and_process_data_operation(resultfolder, data_to_excel_path):
    """
    Fetch data from HDF5 files, process it, and save the results to an Excel file.
    """
    columns = pd.MultiIndex.from_product(
        [
            ["Chemelot", "Zeeland"],
            ["cluster"],
            ["minC_ref", "minC_high"],
            ["NaphthaCracker_Electric", "eSMR", "AEC", "Boiler_El", "Storage_Battery"]
        ],
        names=["Location", "Type", "Scenario", "Tecs"]
    )

    result_data = pd.DataFrame(np.nan, index=range(8760), columns=columns)

    for location in result_data.columns.levels[0]:
        for typ in result_data.columns.levels[1]:
            folder_name = f"{location}_{typ}"
            summarypath = os.path.join(resultfolder, folder_name, "Summary.xlsx")
            summary_results = pd.read_excel(summarypath)

            for scenario in result_data.columns.levels[2]:
                for case in summary_results['case']:
                    if pd.notna(case) and scenario in case:
                        h5_path = Path(summary_results[summary_results['case'] == case].iloc[0][
                                           'time_stamp']) / "optimization_results.h5"
                        if h5_path.exists():
                            with h5py.File(h5_path, "r") as hdf_file:
                                df1 = extract_datasets_from_h5group(hdf_file["operation/technology_operation"], tec_ope=True)
                                for tec in result_data.columns.levels[3]:
                                    para = "electricity_input"
                                    if ('period1', location, tec, para) in df1:
                                        car_output = df1['period1', location, tec, para]
                                        result_data.loc[:, (location, typ, scenario, tec)] = car_output
                                    else:
                                        result_data.loc[:, (location, typ, scenario, tec)] = 0

    result_data.to_excel(data_to_excel_path)


def configure_matplotlib():
    """
    Configure Matplotlib to use LaTeX for text rendering and set font.
    """
    plt.rcParams.update({
        "text.usetex": True,
        "font.family": "serif",
        "font.serif": ["Computer Modern Roman"],
        "axes.labelsize": 12,
        "font.size": 12,
        "legend.fontsize": 11,
        "xtick.labelsize": 12,
        "ytick.labelsize": 12,
    })


def extract_profiles(result_data):
    """
    Extract import profiles from the result data.
    """
    return {
        (location, typ, scenario): result_data.loc[:, (location, typ, scenario)]
        for location in ["Chemelot", "Zeeland"]
        for typ in ["cluster"]
        for scenario in ["minC_ref", "minC_high"]
    }


def extract_profiles_operation(result_data):
    """
    Extract import profiles from the result data.
    """
    return {
        (location, typ, scenario, tec): result_data.loc[:, (location, typ, scenario, tec)]
        for location in ["Chemelot", "Zeeland"]
        for typ in ["cluster"]
        for scenario in ["minC_ref", "minC_high"]
        for tec in ["NaphthaCracker_Electric", "eSMR", "AEC", "Boiler_El", "Storage_Battery"]
    }



def plot_import_profiles(import_profiles, el_price, el_price2, el_emissionrate, relative=False, overlay=None, colors=None):
    """
    Plot import profiles with optional overlays and custom colors.
    """
    weeks = {
        'Winter': range(0, 168),
        'Spring': range(168 * 12, 168 * 13),
        'Summer': range(168 * 25, 168 * 26),
        'Fall': range(168 * 38, 168 * 39)
    }

    plt.figure(figsize=(10, 5))

    color_cycle = plt.rcParams['axes.prop_cycle'].by_key()['color'] if colors is None else colors
    legend_handles = []  # To collect handles from the first subplot only

    for i, (season, week_range) in enumerate(weeks.items(), start=1):
        plt.subplot(2, 2, i)
        ax1 = plt.gca()

        # Plot import profiles
        for idx, ((location, typ, scenario), profile) in enumerate(import_profiles.items()):
            color = color_cycle[idx % len(color_cycle)]
            label = f"{location} - {'R-CO$_2$P' if scenario == 'minC_ref' else 'H-CO$_2$P'}"
            if relative:
                max_import = profile.max()
                line, = ax1.plot(list(week_range), profile.iloc[week_range] / max_import, label=label, linewidth=0.75,
                                 color=color)
            else:
                line, = ax1.plot(list(week_range), profile.iloc[week_range], label=label, linewidth=0.75, color=color)

            # Only collect legend handles from the first subplot
            if i == 1:
                legend_handles.append((line, label))

        # Overlay plot (for second y-axis)
        if overlay:
            ax2 = ax1.twinx()
            if overlay == "el_price":
                line1, = ax2.plot(list(week_range), el_price.iloc[week_range], color='grey', linestyle='dotted',
                                  linewidth=0.8, label='Chemelot Price')
                line2, = ax2.plot(list(week_range), el_price2.iloc[week_range], color='black', linestyle='dotted',
                                  linewidth=0.8, label='Zeeland Price')
                ax2.set_ylabel('Electricity Price [€/MWh]')
                ax2.set_ylim(0, 150)
            elif overlay == "emission":
                line1, = ax2.plot(list(week_range), el_emissionrate.iloc[week_range], color='black', linestyle='dotted',
                                  linewidth=0.8, label='Emission Rate')
                ax2.set_ylabel('Emission Rate [t CO$_2$/MWh]')
                ax2.set_ylim(0, 0.4)

            # Collect handles from right y-axis of the first subplot
            if i == 1:
                legend_handles.append((line1, line1.get_label()))
                if overlay == "el_price":
                    legend_handles.append((line2, line2.get_label()))

        # Set axis labels and title
        ax1.set_xlabel('Time (hours)')
        ax1.set_ylabel('Electricity import' + (' (Relative)' if relative else ' [MW]'))
        ax1.set_title(f'{season}')
        ax1.set_ylim(0, 3000)
        ax1.grid(True, alpha=0.5)

    # Create the figure-wide legend using only the first subplot's handles
    plt.subplots_adjust(bottom=0.2)
    handles, labels = zip(*legend_handles)
    plt.figlegend(handles, labels, loc='lower center', bbox_to_anchor=(0.5, 0), ncol=5)

    plt.tight_layout(rect=[0, 0.05, 1, 1])


def plot_operation_profiles(operation_profiles, el_price2, el_emissionrate, relative=False, overlay=None, colors=None):
    """
    Plot operation profiles with optional overlays and custom colors for all technologies in Zeeland under high CO2 tax.
    """
    weeks = {
        'Winter': range(0, 168),
        'Spring': range(168 * 12, 168 * 13),
        'Summer': range(168 * 25, 168 * 26),
        'Fall': range(168 * 38, 168 * 39)
    }

    import matplotlib.pyplot as plt

    plt.figure(figsize=(10, 5))

    color_cycle = plt.rcParams['axes.prop_cycle'].by_key()['color'] if colors is None else colors
    tech_labels = {
        "NaphthaCracker_Electric": "Electric cracker",
        "eSMR": "Electric SMR",
        "AEC": "",
        "Boiler_El": "Electric boiler",
        "Storage_Battery": "Battery storage"
    }

    legend_handles = []  # To collect handles from the first subplot

    for i, (season, week_range) in enumerate(weeks.items(), start=1):
        plt.subplot(2, 2, i)
        ax1 = plt.gca()

        for idx, ((location, typ, scenario, tec), profile) in enumerate(operation_profiles.items()):
            if location == "Zeeland" and scenario == "minC_high":
                color = color_cycle[idx % len(color_cycle)]
                label = tech_labels[tec]
                if label:
                    if relative:
                        max_import = profile.max()
                        line, = ax1.plot(list(week_range), profile.iloc[week_range] / max_import, label=label,
                                         linewidth=0.75, color=color)
                    else:
                        line, = ax1.plot(list(week_range), profile.iloc[week_range], label=label, linewidth=0.75,
                                         color=color)
                    # Collect legend handles from the first subplot only
                    if i == 1:
                        legend_handles.append((line, label))

        # Handle overlay
        if overlay:
            ax2 = ax1.twinx()
            if overlay == "el_price":
                line2, = ax2.plot(list(week_range), el_price2.iloc[week_range], color='black', linestyle='dotted',
                                  linewidth=0.8, label='Zeeland Price')
                ax2.set_ylabel('Electricity Price [€/MWh]')
                ax2.set_ylim(0, 150)
            elif overlay == "emission":
                line2, = ax2.plot(list(week_range), el_emissionrate.iloc[week_range], color='black',
                                  linestyle='dotted', linewidth=0.8, label='Emission Rate')
                ax2.set_ylabel('Emission Rate [t CO$_2$/MWh]')
                ax2.set_ylim(0, 0.4)

            # Collect right y-axis legend handles only for the first subplot
            if i == 1 and overlay in ["el_price", "emission"]:
                legend_handles.append((line2, line2.get_label()))

        # Set labels, title, and limits
        ax1.set_xlabel('Time (hours)')
        ax1.set_ylabel('Electricity consumption' + (' (Relative)' if relative else ' [MW]'))
        ax1.set_title(f'{season}')
        ax1.set_ylim(0, 2000)
        ax1.grid(True, alpha=0.5)

    # Create the figure-wide legend using only the first subplot's handles
    plt.subplots_adjust(bottom=0.2)
    handles, labels = zip(*legend_handles)
    plt.figlegend(handles, labels, loc='lower center', bbox_to_anchor=(0.5, 0), ncol=5)

    plt.tight_layout(rect=[0, 0.05, 1, 1])


def main():
    get_data = 0

    if get_data == 1:
        fetch_and_process_data_import(RESULT_FOLDER, DATA_TO_EXCEL_PATH)
        fetch_and_process_data_operation(RESULT_FOLDER, DATA_TO_EXCEL_PATH1)
        import_data = pd.read_excel(DATA_TO_EXCEL_PATH, index_col=0, header=[0, 1, 2])
        operation_data = pd.read_excel(DATA_TO_EXCEL_PATH1, index_col=0, header=[0, 1, 2, 3])
    else:
        import_data = pd.read_excel(DATA_TO_EXCEL_PATH, index_col=0, header=[0, 1, 2])
        operation_data = pd.read_excel(DATA_TO_EXCEL_PATH1, index_col=0, header=[0, 1, 2, 3])

    configure_matplotlib()
    el_importdata = pd.read_csv(EL_LOAD_PATH, sep=';', header=0, nrows=8760)
    el_price = el_importdata.iloc[:, 0]
    el_price2 = el_importdata.iloc[:, 1]
    el_emissionrate = el_importdata.iloc[:, 3]

    import_profiles = extract_profiles(import_data)
    operation_profiles = extract_profiles_operation(operation_data)

    # custom_colors_operation = ['#512500', '#7D1D3F', '#9467bd', '#33658A', '#F26419']
    # custom_colors_operation = ['#5D3250', '#94617B', '#A37BA2', '#A0B7BB', '#4A7787']
    custom_colors_operation = ['#422966', '#EEBD6D', '#EEEEFF', '#79AA74', '#28587B']
    custom_colors_import = ['#3F826D', '#E15F51', '#545E75', '#F2D0A4']
    overlay = "emission"
    plot = "import"

    if plot == "operation":
        plot_operation_profiles(operation_profiles, el_price2, el_emissionrate, overlay=overlay, colors=custom_colors_operation)
    elif plot == "import":
        plot_import_profiles(import_profiles, el_price, el_price2, el_emissionrate, relative=False, overlay=overlay, colors=custom_colors_import)

    filename = plot + '_' + overlay

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

    plt.show()


if __name__ == "__main__":
    main()


