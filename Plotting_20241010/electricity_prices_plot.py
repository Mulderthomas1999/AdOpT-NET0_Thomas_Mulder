import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Define the data path
datapath = "Z:/PyHub/PyHub_data/CM/100624_CM"
el_load_path = Path(datapath) / 'import_data' / 'Electricity_data_CM.csv'

# Read the CSV file
el_importdata = pd.read_csv(el_load_path, sep=';', header=0, nrows=8760)

# Extract the relevant data
el_price = el_importdata.iloc[:, 0]
el_price2 = el_importdata.iloc[:, 1]
el_emissionrate = el_importdata.iloc[:, 3]

# Define the custom colors
color_price = '#315C5E'
color_price2 = '#B1BFB0'
color_emission = '#28316E'

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

# Create a new figure and axis with a grid of subplots
fig = plt.figure(figsize=(10, 5))
gs = fig.add_gridspec(2, 2, height_ratios=[1.3, 0.8], width_ratios=[2, 2])

# Plot the time series data on the main plot (top subplot spanning both columns)
ax_main = fig.add_subplot(gs[0, :])
ax_main.plot(el_price, color=color_price, label='Chemelot', linewidth=0.5)
ax_main.plot(el_price2, color=color_price2, label='Zeeland', linewidth=0.5)
ax_main.set_xlabel('Time (hours)')
ax_main.set_ylabel('Electricity Price [EUR/MWh]')
ax_main.tick_params(axis='y')
ax_main.set_xlim(0, 8759)
ax_main.set_ylim(0, 200)

# Create a second y-axis for the emissions on the main plot
ax_main2 = ax_main.twinx()
ax_main2.plot(el_emissionrate, color=color_emission, linestyle='--', label='Grid emissions', linewidth=0.5)
ax_main2.set_ylabel('Emission Rate [t CO$_2$/MWh]', color=color_emission)
ax_main2.tick_params(axis='y', labelcolor=color_emission)
ax_main2.set_ylim(0, 0.4)

# Add a legend to the main plot
lines, labels = ax_main.get_legend_handles_labels()
lines2, labels2 = ax_main2.get_legend_handles_labels()
legend = ax_main.legend(lines + lines2, labels + labels2, loc='upper center', ncol=3)
# legend.get_frame().set_facecolor('white')
# legend.get_frame().set_alpha(1)



# # Plot the histogram for electricity prices on the bottom left subplot
# ax_hist1 = fig.add_subplot(gs[1, 0])
# ax_hist1.hist(el_price, bins=50, color=color_price, alpha=0.5, label='Chemelot')
# ax_hist1.hist(el_price2, bins=50, color=color_price2, alpha=0.5, label='Zeeland')
# ax_hist1.set_xlabel('Electricity Price [EUR/MWh]')
# ax_hist1.set_ylabel('Frequency')
# ax_hist1.legend()

# Plot the histogram for electricity prices on the bottom left subplot
ax_hist1 = fig.add_subplot(gs[1, 0])
ax_hist1.ecdf(el_price, complementary=True, color=color_price, label='Chemelot')
ax_hist1.ecdf(el_price2, complementary=True, color=color_price2, label='Zeeland')
ax_hist1.set_xlabel('Electricity Price [EUR/MWh]')
ax_hist1.set_ylabel('Probability')
ax_hist1.legend()

# # Plot the histogram for CO₂ emissions on the bottom right subplot
# ax_hist2 = fig.add_subplot(gs[1, 1])
# ax_hist2.hist(el_emissionrate, bins=50, color=color_emission, alpha=0.5, label='Grid emissions')
# ax_hist2.set_xlabel('Emission Rate [t CO$_2$/MWh]')
# ax_hist2.set_ylabel('Probability')
# ax_hist2.legend()

# Plot the histogram for CO₂ emissions on the bottom right subplot
ax_hist2 = fig.add_subplot(gs[1, 1])
ax_hist2.ecdf(el_emissionrate, complementary=True, color=color_emission, label='Grid emissions')
ax_hist2.set_xlabel('Emission Rate [t CO$_2$/MWh]')
ax_hist2.set_ylabel('Probability')
ax_hist2.legend()

# Show the plot
plt.tight_layout()


saveas = 'pdf'

if saveas == 'svg':
    savepath = 'C:/Users/5637635/Documents/OneDrive - Universiteit Utrecht/Images and graphs/Collection CM/Paper/' + 'Fig_eprice_cum.svg'
    plt.savefig(savepath, format='svg')
if saveas == 'pdf':
    savepath = 'C:/Users/5637635/Documents/OneDrive - Universiteit Utrecht/Images and graphs/Collection CM/Paper/' + 'Fig_eprice_cum.pdf'
    plt.savefig(savepath, format='pdf')

#show plot
# plt.show()
