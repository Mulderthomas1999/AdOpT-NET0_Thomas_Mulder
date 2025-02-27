import pytest
from pathlib import Path
import json
import numpy as np

from adopt_net0 import database as td


# WIND COST MODELS
def test_wind_cost_model(request):
    """
    tests wind cost model for IRENA, NREL
    """
    tec = "WindTurbine_Onshore_4000"
    td.help(component_name=tec)

    # IRENA
    for terrain in ["Onshore", "Offshore"]:
        options = {
            "currency_out": "EUR",
            "financial_year_out": 2020,
            "discount_rate": 0.1,
            "nameplate_capacity_MW": 4,
            "terrain": terrain,
            "source": "IRENA",
        }

        td.write_json(tec, request.config.result_folder_path, options)

    # NREL
    for terrain in ["Onshore", "Offshore"]:
        for mounting_type in ["fixed", "floating"]:
            options = {
                "currency_out": "EUR",
                "financial_year_out": 2020,
                "discount_rate": 0.1,
                "nameplate_capacity_MW": 4,
                "source": "NREL",
                "terrain": terrain,
                "projection_year": 2030,
                "projection_type": "Moderate",
                "mounting_type": mounting_type,
            }

            td.write_json(tec, request.config.result_folder_path, options)


# PV COST MODELS
def test_pv_cost_model(request):
    """
    tests PV cost model for IRENA, NREL
    """
    tec = "Photovoltaic"
    td.help(component_name=tec)

    # IRENA
    options = {
        "currency_out": "EUR",
        "financial_year_out": 2020,
        "discount_rate": 0.1,
        "region": "Germany",
        "source": "IRENA",
    }

    td.write_json(tec, request.config.result_folder_path, options)

    # NREL
    for pv_type in ["utility", "rooftop commercial", "rooftop residential"]:
        options = {
            "currency_out": "EUR",
            "financial_year_out": 2020,
            "discount_rate": 0.1,
            "source": "NREL",
            "projection_year": 2030,
            "projection_type": "Moderate",
            "pv_type": pv_type,
        }

        td.write_json(tec, request.config.result_folder_path, options)


# DAC
def test_dac_cost_model(request):
    """
    tests DAC cost model for Sievert
    """
    tec = "Photovoltaic"
    td.help(component_name=tec)

    # Sievert
    tec = "DAC_Adsorption"
    td.help(component_name=tec)

    options = {
        "currency_out": "EUR",
        "financial_year_out": 2020,
        "discount_rate": 0.1,
        "cumulative_capacity_installed_t_per_a": 1,
        "source": "Sievert",
    }

    td.write_json(tec, ".", options)


# CO2 PIPELINE
def test_co2_pipeline_cost_model(request):
    """
    tests CO2_Pipeline cost model for Oeuvray
    """
    tec = "CO2_Pipeline"
    td.help(component_name=tec)

    for terrain in ["Offshore", "Onshore"]:
        for p in [10, 80]:
            options = {
                "currency_out": "EUR",
                "financial_year_out": 2020,
                "discount_rate": 0.1,
                "length_km": 100,
                "m_kg_per_s_min": 10,
                "m_kg_per_s_max": 10,
                "m_kg_evaluation_points": 1,
                "p_inlet_bar": 1,
                "p_outlet_bar": p,
                "terrain": terrain,
            }

            td.write_json(tec, ".", options)


# CO2 Compressor
def test_co2_compressor_cost_model(request):
    """
    tests CO2_Pipeline cost model for Oeuvray
    """
    tec = "CO2_Compressor"
    td.help(component_name=tec)

    for capex_model in [1, 3]:
        for p in [10, 80]:
            options = {
                "currency_out": "EUR",
                "financial_year_out": 2020,
                "discount_rate": 0.1,
                "m_kg_per_s_min": 10,
                "m_kg_per_s_max": 10,
                "m_kg_evaluation_points": 1,
                "p_inlet_bar": 1,
                "p_outlet_bar": p,
                "capex_model": capex_model,
            }

            td.write_json(tec, ".", options)
