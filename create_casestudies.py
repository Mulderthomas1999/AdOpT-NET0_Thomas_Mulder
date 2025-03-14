from pathlib import Path
import adopt_net0.data_preprocessing as dp
from adopt_net0.modelhub import ModelHub
from adopt_net0.result_management.read_results import add_values_to_summary
import pandas as pd


#Create data Chemelot cluster
execute = 0

if execute == 1:
    # Specify the path to your input data
    casepath = "Z:/PyHub/PyHub_casestudies/CM/Chemelot_cluster"
    datapath = "Z:/PyHub/PyHub_data/CM/240624_CM"

    firsttime = 0
    if firsttime == 1:
        # Create template files
        dp.create_optimization_templates(casepath)
        dp.create_montecarlo_template_csv(casepath)

        # Create folder structure
        dp.create_input_data_folder_template(casepath)

        # # Copy technology and network data into folder
        dp.copy_technology_data(casepath, datapath)

        # Read climate data and fill carried data
        dp.load_climate_data_from_api(casepath)
        dp.fill_carrier_data(casepath, value_or_data=0)

        # Demand data
        dp.fill_carrier_data(casepath, value_or_data=135, columns=['Demand'], carriers=['ammonia'])
        dp.fill_carrier_data(casepath, value_or_data=45, columns=['Demand'], carriers=['CO2'])
        dp.fill_carrier_data(casepath, value_or_data=150, columns=['Demand'], carriers=['ethylene'])
        dp.fill_carrier_data(casepath, value_or_data=27.8, columns=['Demand'], carriers=['steam'])
        dp.fill_carrier_data(casepath, value_or_data=86.4, columns=['Demand'], carriers=['electricity'])
        dp.fill_carrier_data(casepath, value_or_data=6.9, columns=['Demand'], carriers=['crackergas'])

        # No import limit
        dp.fill_carrier_data(casepath, value_or_data=2000, columns=['Import limit'], carriers=['electricity', 'methane', 'naphtha', "CO2"])

        # No export limit
        dp.fill_carrier_data(casepath, value_or_data=2000, columns=['Export limit'], carriers=['nitrogen', 'oxygen', 'heatlowT', 'steam', 'crackergas'])
        dp.fill_carrier_data(casepath, value_or_data=0.203, columns=['Export emission factor'],
                             carriers=['crackergas'])

        # CO2 export
        dp.fill_carrier_data(casepath, value_or_data=115, columns=['Export limit'], carriers=['CO2'])
    dp.fill_carrier_data(casepath, value_or_data=-62.74, columns=['Export price'], carriers=['CO2'])

        # # Constant prices
        # dp.fill_carrier_data(casepath, value_or_data=100, columns=['Import price'], carriers=['methane'])
        # dp.fill_carrier_data(casepath, value_or_data=732, columns=['Import price'], carriers=['naphtha'])
        #
        # # Electricity price from file
        # el_load_path = Path(datapath) / 'import_data' / 'Electricity_data_CM.csv'
        # el_importdata = pd.read_csv(el_load_path, sep=';', header=0, nrows=8760)
        # el_price = el_importdata.iloc[:, 0]
        # el_emissionrate = el_importdata.iloc[:, 3]
        #
        # dp.fill_carrier_data(casepath, value_or_data=el_price, columns=['Import price'], carriers=['electricity'])
        # dp.fill_carrier_data(casepath, value_or_data=el_emissionrate, columns=['Import emission factor'], carriers=['electricity'])
        #
        #
        # #carbon tax
        # file_path = Path(casepath) / 'period1' / "node_data" / 'Chemelot' / 'CarbonCost.csv'
        # data = pd.read_csv(file_path, delimiter=';')
        #
        # # Set the price to 150.31 and subsidy to 0 for all rows
        # data['price'] = 150.31
        # data['subsidy'] = 0
        #
        # # Save the modified CSV file
        # data.to_csv(file_path, index=False, sep=';')


#Create data Chemelot standalone
execute = 0

if execute == 1:
    # Specify the path to your input data
    casepath = "Z:/PyHub/PyHub_casestudies/CM/Chemelot_ethylene"
    datapath = "Z:/PyHub/PyHub_data/CM/240624_CM"

    carrier = 'ethylene'

    dp.fill_carrier_data(casepath, value_or_data=0)

    if carrier == 'ammonia':
        # Demand data
        dp.fill_carrier_data(casepath, value_or_data=135, columns=['Demand'], carriers=['ammonia'])
        dp.fill_carrier_data(casepath, value_or_data=45, columns=['Demand'], carriers=['CO2'])
        dp.fill_carrier_data(casepath, value_or_data=5, columns=['Demand'], carriers=['electricity'])

        # No import limit
        dp.fill_carrier_data(casepath, value_or_data=2000/2, columns=['Import limit'],
                             carriers=['electricity'])
        dp.fill_carrier_data(casepath, value_or_data=2000, columns=['Import limit'],
                             carriers=['methane', "CO2"])

        # No export limit
        dp.fill_carrier_data(casepath, value_or_data=2000, columns=['Export limit'],
                             carriers=['nitrogen', 'oxygen', 'heatlowT', 'steam'])

    elif carrier == 'ethylene':
        # Demand data
        dp.fill_carrier_data(casepath, value_or_data=150, columns=['Demand'], carriers=['ethylene'])
        dp.fill_carrier_data(casepath, value_or_data=64.6, columns=['Demand'], carriers=['steam'])
        dp.fill_carrier_data(casepath, value_or_data=81.4, columns=['Demand'], carriers=['electricity'])
        dp.fill_carrier_data(casepath, value_or_data=6.9, columns=['Demand'], carriers=['crackergas'])

        # No import limit
        dp.fill_carrier_data(casepath, value_or_data=2000/2, columns=['Import limit'],
                             carriers=['electricity'])
        dp.fill_carrier_data(casepath, value_or_data=2000, columns=['Import limit'],
                             carriers=['methane', 'naphtha', "CO2"])

        # No export limit
        dp.fill_carrier_data(casepath, value_or_data=2000, columns=['Export limit'], carriers=['heatlowT', 'steam', 'crackergas'])
        dp.fill_carrier_data(casepath, value_or_data=0.203, columns=['Export emission factor'],
                             carriers=['crackergas'])

    # CO2 export
    dp.fill_carrier_data(casepath, value_or_data=115/2, columns=['Export limit'], carriers=['CO2'])
    dp.fill_carrier_data(casepath, value_or_data=-62.74, columns=['Export price'], carriers=['CO2'])

    # Constant prices
    dp.fill_carrier_data(casepath, value_or_data=100, columns=['Import price'], carriers=['methane'])
    if carrier == 'ethylene':
        dp.fill_carrier_data(casepath, value_or_data=732, columns=['Import price'], carriers=['naphtha'])

    # Electricity price from file
    el_load_path = Path(datapath) / 'import_data' / 'Electricity_data_CM.csv'
    el_importdata = pd.read_csv(el_load_path, sep=';', header=0, nrows=8760)
    el_price = el_importdata.iloc[:, 0]
    el_emissionrate = el_importdata.iloc[:, 3]

    dp.fill_carrier_data(casepath, value_or_data=el_price, columns=['Import price'], carriers=['electricity'])
    dp.fill_carrier_data(casepath, value_or_data=el_emissionrate, columns=['Import emission factor'], carriers=['electricity'])


    #carbon tax
    file_path = Path(casepath) / 'period1' / "node_data" / 'Chemelot' / 'CarbonCost.csv'
    data = pd.read_csv(file_path, delimiter=';')

    # Set the price to 150.31 and subsidy to 0 for all rows
    data['price'] = 150.31
    data['subsidy'] = 0

    # Save the modified CSV file
    data.to_csv(file_path, index=False, sep=';')



#Create data Zeeland cluster
execute = 0

if execute == 1:
    # Specify the path to your input data
    casepath = "Z:/PyHub/PyHub_casestudies/CM/Zeeland_cluster"
    datapath = "Z:/PyHub/PyHub_data/CM/240624_CM"

    firsttime = 0
    if firsttime == 1:
        # Create template files
        dp.create_optimization_templates(casepath)
        dp.create_montecarlo_template_csv(casepath)

        # Create folder structure
        dp.create_input_data_folder_template(casepath)

        # # Copy technology and network data into folder
        dp.copy_technology_data(casepath, datapath)

        # Read climate data and fill carried data
        dp.load_climate_data_from_api(casepath)
        dp.fill_carrier_data(casepath, value_or_data=0)

        # Demand data
        dp.fill_carrier_data(casepath, value_or_data=208, columns=['Demand'], carriers=['ammonia'])
        dp.fill_carrier_data(casepath, value_or_data=111, columns=['Demand'], carriers=['CO2'])
        dp.fill_carrier_data(casepath, value_or_data=208, columns=['Demand'], carriers=['ethylene'])
        dp.fill_carrier_data(casepath, value_or_data=546.7, columns=['Demand'], carriers=['steam'])
        dp.fill_carrier_data(casepath, value_or_data=93.2, columns=['Demand'], carriers=['electricity'])

        # No import limit
        dp.fill_carrier_data(casepath, value_or_data=3000, columns=['Import limit'], carriers=['electricity', 'methane', 'naphtha', "CO2"])

        # No export limit
        dp.fill_carrier_data(casepath, value_or_data=2000, columns=['Export limit'], carriers=['nitrogen', 'oxygen', 'heatlowT', 'steam', 'crackergas'])
        dp.fill_carrier_data(casepath, value_or_data=0.203, columns=['Export emission factor'],
                             carriers=['crackergas'])

    # CO2 export
    dp.fill_carrier_data(casepath, value_or_data=171, columns=['Export limit'], carriers=['CO2'])
    dp.fill_carrier_data(casepath, value_or_data=-54.56, columns=['Export price'], carriers=['CO2'])

        # # Constant prices
        # dp.fill_carrier_data(casepath, value_or_data=100, columns=['Import price'], carriers=['methane'])
        # dp.fill_carrier_data(casepath, value_or_data=732, columns=['Import price'], carriers=['naphtha'])
        #
        # # Electricity price from file
        # el_load_path = Path(datapath) / 'import_data' / 'Electricity_data_CM.csv'
        # el_importdata = pd.read_csv(el_load_path, sep=';', header=0, nrows=8760)
        # el_price = el_importdata.iloc[:, 1]
        # el_emissionrate = el_importdata.iloc[:, 3]
        #
        # dp.fill_carrier_data(casepath, value_or_data=el_price, columns=['Import price'], carriers=['electricity'])
        # dp.fill_carrier_data(casepath, value_or_data=el_emissionrate, columns=['Import emission factor'], carriers=['electricity'])
        #
        #
        # #carbon tax
        # file_path = Path(casepath) / 'period1' / "node_data" / 'Zeeland' / 'CarbonCost.csv'
        # data = pd.read_csv(file_path, delimiter=';')
        #
        # # Set the price to 150.31 and subsidy to 0 for all rows
        # data['price'] = 150.31
        # data['subsidy'] = 0
        #
        # # Save the modified CSV file
        # data.to_csv(file_path, index=False, sep=';')


#Create data Zeeland standalone
execute = 0

if execute == 1:
    # Specify the path to your input data
    casepath = "Z:/PyHub/PyHub_casestudies/CM/Zeeland_ethylene"
    datapath = "Z:/PyHub/PyHub_data/CM/240624_CM"

    carrier = 'ethylene'

    dp.fill_carrier_data(casepath, value_or_data=0)

    # Demand data
    dp.fill_carrier_data(casepath, value_or_data=208, columns=['Demand'], carriers=[carrier])

    if carrier == 'ammonia':
        dp.fill_carrier_data(casepath, value_or_data=111, columns=['Demand'], carriers=['CO2'])
        dp.fill_carrier_data(casepath, value_or_data=12.4, columns=['Demand'], carriers=['electricity'])

        # No import limit
        dp.fill_carrier_data(casepath, value_or_data=3000/2, columns=['Import limit'], carriers=['electricity'])
        dp.fill_carrier_data(casepath, value_or_data=3000, columns=['Import limit'],
                             carriers=['methane', "CO2"])

        # No export limit
        dp.fill_carrier_data(casepath, value_or_data=2000, columns=['Export limit'], carriers=['nitrogen', 'oxygen', 'heatlowT', 'steam', 'crackergas'])

    elif carrier == 'ethylene':
        dp.fill_carrier_data(casepath, value_or_data=570.2, columns=['Demand'], carriers=['steam'])
        dp.fill_carrier_data(casepath, value_or_data=80.9, columns=['Demand'], carriers=['electricity'])

        # No import limit
        dp.fill_carrier_data(casepath, value_or_data=3000/2, columns=['Import limit'], carriers=['electricity'])
        dp.fill_carrier_data(casepath, value_or_data=3000, columns=['Import limit'],
                             carriers=['methane','naphtha'])

        # No export limit
        dp.fill_carrier_data(casepath, value_or_data=2000, columns=['Export limit'],
                             carriers=['oxygen', 'heatlowT', 'steam', 'crackergas'])
        dp.fill_carrier_data(casepath, value_or_data=0.203, columns=['Export emission factor'],
                             carriers=['crackergas'])

    # CO2 export
    dp.fill_carrier_data(casepath, value_or_data=171/2, columns=['Export limit'], carriers=['CO2'])
    dp.fill_carrier_data(casepath, value_or_data=-54.56, columns=['Export price'], carriers=['CO2'])

    # Constant prices
    dp.fill_carrier_data(casepath, value_or_data=100, columns=['Import price'], carriers=['methane'])
    if carrier == 'ethylene':
        dp.fill_carrier_data(casepath, value_or_data=732, columns=['Import price'], carriers=['naphtha'])

    # Electricity price from file
    el_load_path = Path(datapath) / 'import_data' / 'Electricity_data_CM.csv'
    el_importdata = pd.read_csv(el_load_path, sep=';', header=0, nrows=8760)
    el_price = el_importdata.iloc[:, 1]
    el_emissionrate = el_importdata.iloc[:, 3]

    dp.fill_carrier_data(casepath, value_or_data=el_price, columns=['Import price'], carriers=['electricity'])
    dp.fill_carrier_data(casepath, value_or_data=el_emissionrate, columns=['Import emission factor'], carriers=['electricity'])


    #carbon tax
    file_path = Path(casepath) / 'period1' / "node_data" / 'Zeeland' / 'CarbonCost.csv'
    data = pd.read_csv(file_path, delimiter=';')

    # Set the price to 150.31 and subsidy to 0 for all rows
    data['price'] = 150.31
    data['subsidy'] = 0

    # Save the modified CSV file
    data.to_csv(file_path, index=False, sep=';')



#Create data infrastructure 2 nodes
execute = 0

if execute == 1:
    # Specify the path to your input data
    casepath = "Z:/PyHub/PyHub_casestudies/CM/Infra_2clusters"

    # Create template files
    dp.create_optimization_templates(casepath)
    dp.create_input_data_folder_template(casepath)
    #add network data
    dp.copy_network_data(casepath)


