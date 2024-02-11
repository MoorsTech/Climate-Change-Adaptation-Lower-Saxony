"""
Python model 'Uelzen.py'
Translated using PySD
"""

from pathlib import Path

from pysd.py_backend.functions import if_then_else
from pysd.py_backend.statefuls import Integ

__pysd_version__ = "2.2.4"

__data = {"scope": None, "time": lambda: 0}

_root = Path(__file__).parent

_subscript_dict = {}

_namespace = {
    "TIME": "time",
    "Time": "time",
    "Monthly irrigation": "monthly_irrigation",
    "Agricultural water": "agricultural_water",
    "River Inflow": "river_inflow",
    "return flow": "return_flow",
    "River flow": "river_flow",
    "Recharge": "recharge",
    "months": "months",
    "Groundwater": "groundwater",
    "Extraction": "extraction",
    "Infiltration": "infiltration",
    "Generated": "generated",
    "Allowed amount": "allowed_amount",
    "Aquifer yield": "aquifer_yield",
    "Irrigated area": "irrigated_area",
    "Emissions": "emissions",
    "BAU": "bau",
    "CO2": "co2",
    "Condition": "condition",
    "Consumption": "consumption",
    "Past": "past",
    "Costs": "costs",
    "Covered": "covered",
    "Diesel consumption": "diesel_consumption",
    "Diesel price": "diesel_price",
    "Drinking water": "drinking_water",
    "Emissions per kWh": "emissions_per_kwh",
    "Emissions per liter of fuel": "emissions_per_liter_of_fuel",
    "Emitted": "emitted",
    "Energy": "energy",
    "Total area": "total_area",
    "ETP": "etp",
    "Work cost": "work_cost",
    "Industrial water": "industrial_water",
    "NetoNull": "netonull",
    "Outflow": "outflow",
    "Repairs cost": "repairs_cost",
    "kWh price": "kwh_price",
    "Energy per m3": "energy_per_m3",
    "Water Balance": "water_balance",
    "Pe": "pe",
    "Volume": "volume",
    "Artificial Recharge": "artificial_recharge",
    "Kc": "kc",
    "Correction": "correction",
    "Base flow": "base_flow",
    "Thickness": "thickness",
    "ActualET": "actualet",
    "n": "n",
    "Runoff": "runoff",
    "CN": "cn",
    "Recesion time": "recesion_time",
    "Porosity": "porosity",
    "Pp": "pp",
    "S max retention": "s_max_retention",
    "Soil water": "soil_water",
    "FINAL TIME": "final_time",
    "INITIAL TIME": "initial_time",
    "SAVEPER": "saveper",
    "TIME STEP": "time_step",
}

_dependencies = {
    "monthly_irrigation": {"agricultural_water": 1},
    "agricultural_water": {"kc": 2, "etp": 2, "pe": 2, "correction": 2, "n": 2},
    "river_inflow": {},
    "return_flow": {},
    "river_flow": {"groundwater": 1, "river_inflow": 1},
    "recharge": {
        "soil_water": 2,
        "time_step": 2,
        "s_max_retention": 2,
        "artificial_recharge": 1,
    },
    "months": {},
    "groundwater": {"_integ_groundwater": 1},
    "extraction": {
        "agricultural_water": 1,
        "irrigated_area": 1,
        "total_area": 3,
        "industrial_water": 1,
        "drinking_water": 1,
    },
    "infiltration": {"pp": 2, "runoff": 2},
    "generated": {
        "diesel_consumption": 1,
        "diesel_price": 1,
        "consumption": 1,
        "kwh_price": 1,
        "monthly_irrigation": 2,
        "work_cost": 1,
        "repairs_cost": 1,
    },
    "allowed_amount": {},
    "aquifer_yield": {},
    "irrigated_area": {},
    "emissions": {
        "emissions_per_kwh": 1,
        "consumption": 1,
        "diesel_consumption": 1,
        "emissions_per_liter_of_fuel": 1,
    },
    "bau": {},
    "co2": {"_integ_co2": 1},
    "condition": {},
    "consumption": {"monthly_irrigation": 1, "energy_per_m3": 1},
    "past": {"energy": 1},
    "costs": {"_integ_costs": 1},
    "covered": {"costs": 1},
    "diesel_consumption": {"kc": 1},
    "diesel_price": {},
    "drinking_water": {},
    "emissions_per_kwh": {"condition": 1, "bau": 1, "netonull": 1},
    "emissions_per_liter_of_fuel": {},
    "emitted": {"co2": 1},
    "energy": {"_integ_energy": 1},
    "total_area": {},
    "etp": {},
    "work_cost": {},
    "industrial_water": {},
    "netonull": {},
    "outflow": {"soil_water": 3, "time_step": 3, "etp": 3},
    "repairs_cost": {},
    "kwh_price": {},
    "energy_per_m3": {},
    "water_balance": {"pp": 1, "runoff": 1, "infiltration": 1},
    "pe": {"pp": 3},
    "volume": {"thickness": 1, "groundwater": 1},
    "artificial_recharge": {},
    "kc": {},
    "correction": {},
    "base_flow": {"groundwater": 1, "recesion_time": 1},
    "thickness": {},
    "actualet": {"outflow": 1, "agricultural_water": 1},
    "n": {},
    "runoff": {"pp": 3, "s_max_retention": 3},
    "cn": {},
    "recesion_time": {},
    "porosity": {},
    "pp": {},
    "s_max_retention": {"cn": 1},
    "soil_water": {"_integ_soil_water": 1},
    "final_time": {},
    "initial_time": {},
    "saveper": {"time_step": 1},
    "time_step": {},
    "_integ_groundwater": {
        "initial": {},
        "step": {
            "recharge": 1,
            "extraction": 1,
            "base_flow": 1,
            "river_flow": 1,
            "porosity": 1,
        },
    },
    "_integ_co2": {"initial": {}, "step": {"emissions": 1}},
    "_integ_costs": {"initial": {}, "step": {"generated": 1}},
    "_integ_energy": {"initial": {}, "step": {"consumption": 1}},
    "_integ_soil_water": {
        "initial": {},
        "step": {"infiltration": 1, "outflow": 1, "recharge": 1},
    },
}

##########################################################################
#                            CONTROL VARIABLES                           #
##########################################################################

_control_vars = {
    "initial_time": lambda: 1,
    "final_time": lambda: 1140,
    "time_step": lambda: 1,
    "saveper": lambda: time_step(),
}


def _init_outer_references(data):
    for key in data:
        __data[key] = data[key]


def time():
    return __data["time"]()


def final_time():
    """
    Real Name: FINAL TIME
    Original Eqn: 1140
    Units: Month
    Limits: (None, None)
    Type: constant
    Subs: None

    The final time for the simulation.
    """
    return __data["time"].final_time()


def initial_time():
    """
    Real Name: INITIAL TIME
    Original Eqn: 1
    Units: Month
    Limits: (None, None)
    Type: constant
    Subs: None

    The initial time for the simulation.
    """
    return __data["time"].initial_time()


def saveper():
    """
    Real Name: SAVEPER
    Original Eqn: TIME STEP
    Units: Month
    Limits: (0.0, None)
    Type: component
    Subs: None

    The frequency with which output is stored.
    """
    return __data["time"].saveper()


def time_step():
    """
    Real Name: TIME STEP
    Original Eqn: 1
    Units: Month
    Limits: (0.0, None)
    Type: constant
    Subs: None

    The time step for the simulation.
    """
    return __data["time"].time_step()


##########################################################################
#                             MODEL VARIABLES                            #
##########################################################################


def monthly_irrigation():
    """
    Real Name: Monthly irrigation
    Original Eqn: Agricultural water*10
    Units: m3/Month
    Limits: (None, None)
    Type: component
    Subs: None

    Para cualcular el total de toda el area = Agricultural water*Irrigated
        area*1000
    """
    return agricultural_water() * 10


def agricultural_water():
    """
    Real Name: Agricultural water
    Original Eqn: IF THEN ELSE((((Kc*ETP)-Pe)/(Correction*n))>=0, ((Kc*ETP)-Pe)/(Correction*n), 0)
    Units: mm/Month
    Limits: (None, None)
    Type: component
    Subs: None

    La formula está calculando el agua extraida basada en el area de 600 km2
        pero se tiene que transformat a 1454 para contar el area total y cuantos
        mm le substrae al aquífero
    """
    return if_then_else(
        (((kc() * etp()) - pe()) / (correction() * n())) >= 0,
        lambda: ((kc() * etp()) - pe()) / (correction() * n()),
        lambda: 0,
    )


def river_inflow():
    """
    Real Name: River Inflow
    Original Eqn: 0.0166
    Units:
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return 0.0166


def return_flow():
    """
    Real Name: return flow
    Original Eqn: 0.0108
    Units:
    Limits: (0.15, 0.37)
    Type: constant
    Subs: None


    """
    return 0.0108


def river_flow():
    """
    Real Name: River flow
    Original Eqn: Groundwater*River Inflow
    Units:
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return groundwater() * river_inflow()


def recharge():
    """
    Real Name: Recharge
    Original Eqn: IF THEN ELSE((Soil water/TIME STEP)>=S max retention, (Soil water/TIME STEP)-S max retention, 0 )+Artificial Recharge
    Units: mm/Month
    Limits: (None, None)
    Type: component
    Subs: None

    IF THEN ELSE((Soil water/TIME STEP)>=S max retention, (Soil water/TIME STEP)-S max
        retention, 0 )+ArtificialRecharge+DELAY1        (((Agricultural water/(Irrigated area/Total area))*return flow) , months )
    """
    return (
        if_then_else(
            (soil_water() / time_step()) >= s_max_retention(),
            lambda: (soil_water() / time_step()) - s_max_retention(),
            lambda: 0,
        )
        + artificial_recharge()
    )


def months():
    """
    Real Name: months
    Original Eqn: 2.12
    Units:
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return 2.12


def groundwater():
    """
    Real Name: Groundwater
    Original Eqn: INTEG ( ((Recharge-Extraction-Base flow-River flow)/Porosity), 0)
    Units: mm
    Limits: (None, None)
    Type: component
    Subs: None

    Blaschke and Gschöpf (2011) mention that the aquifer has a thickness of 5
        to 20 m
    """
    return _integ_groundwater()


def extraction():
    """
    Real Name: Extraction
    Original Eqn: (Agricultural water/(Irrigated area/Total area))+((Industrial water/Total area)*0.001)+((Drinking water/Total area)*0.001)
    Units: mm/Month
    Limits: (None, None)
    Type: component
    Subs: None

    (Agricultural water/(Total area/Irrigated area))+((Industrial water/Total
        area)*0.001)+((Drinking water/Total area)*0.001)
    """
    return (
        (agricultural_water() / (irrigated_area() / total_area()))
        + ((industrial_water() / total_area()) * 0.001)
        + ((drinking_water() / total_area()) * 0.001)
    )


def infiltration():
    """
    Real Name: Infiltration
    Original Eqn: IF THEN ELSE( Pp-Runoff>0 , Pp-Runoff , 0 )
    Units: mm/Month
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return if_then_else(pp() - runoff() > 0, lambda: pp() - runoff(), lambda: 0)


def generated():
    """
    Real Name: Generated
    Original Eqn: (Diesel consumption*Diesel price)+(Consumption*kWh price)+(Monthly irrigation*Work cost)+(Monthly irrigation *Repairs cost)
    Units: euro/Month
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (
        (diesel_consumption() * diesel_price())
        + (consumption() * kwh_price())
        + (monthly_irrigation() * work_cost())
        + (monthly_irrigation() * repairs_cost())
    )


def allowed_amount():
    """
    Real Name: Allowed amount
    Original Eqn: 70.34
    Units: mm/year
    Limits: (None, None)
    Type: constant
    Subs: None

    De los datos de Uelzen en promedio entre 2002 y 2008 se permitia extraer
        51,458,693.71 m3/año. Con area de 60,000 ha = 85.76 mm/año y con area de
        73,156 ha = 70.34 mm/año. Máximo permitido incluyendo agua de la
        industria y agua potable
    """
    return 70.34


def aquifer_yield():
    """
    Real Name: Aquifer yield
    Original Eqn: 91.95
    Units: mm/year
    Limits: (None, None)
    Type: constant
    Subs: None

    Los datos de Uelzen dicen que son 67,270,000 m3/año. Si usamos el area de
        60,000 ha entonces = 112.12 mm/año si usamos 73,156 ha entonces = 91.95
        mm/año
    """
    return 91.95


def irrigated_area():
    """
    Real Name: Irrigated area
    Original Eqn: 600
    Units: km2
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return 600


def emissions():
    """
    Real Name: Emissions
    Original Eqn: (Emissions per kWh*Consumption)+(Diesel consumption*Emissions per liter of fuel)
    Units: kg/Month
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (emissions_per_kwh() * consumption()) + (
        diesel_consumption() * emissions_per_liter_of_fuel()
    )


def bau():
    """
    Real Name: BAU
    Original Eqn: 1
    Units:
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return 1


def co2():
    """
    Real Name: CO2
    Original Eqn: INTEG ( Emissions, 0)
    Units:
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return _integ_co2()


def condition():
    """
    Real Name: Condition
    Original Eqn: 0
    Units:
    Limits: (0.0, 1.0, 1.0)
    Type: constant
    Subs: None


    """
    return 0


def consumption():
    """
    Real Name: Consumption
    Original Eqn: Monthly irrigation*Energy per m3
    Units: kWh/Month
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return monthly_irrigation() * energy_per_m3()


def past():
    """
    Real Name: Past
    Original Eqn: Energy
    Units:
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return energy()


def costs():
    """
    Real Name: Costs
    Original Eqn: INTEG ( Generated, 0)
    Units:
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return _integ_costs()


def covered():
    """
    Real Name: Covered
    Original Eqn: Costs
    Units:
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return costs()


def diesel_consumption():
    """
    Real Name: Diesel consumption
    Original Eqn: IF THEN ELSE(Kc = 0, 0 , 9.17 )
    Units: liter/hectare
    Limits: (None, None)
    Type: component
    Subs: None

    Average tracktor diesel consumption per hectare (Fricke)
    """
    return if_then_else(kc() == 0, lambda: 0, lambda: 9.17)


def diesel_price():
    """
    Real Name: Diesel price
    Original Eqn: 1.25
    Units: euro/liter
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return 1.25


def drinking_water():
    """
    Real Name: Drinking water
    Original Eqn: 533638
    Units: m3/Month
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return 533638


def emissions_per_kwh():
    """
    Real Name: Emissions per kWh
    Original Eqn: IF THEN ELSE(Condition=0, BAU , NetoNull)
    Units: kg/kWh
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return if_then_else(condition() == 0, lambda: bau(), lambda: netonull())


def emissions_per_liter_of_fuel():
    """
    Real Name: Emissions per liter of fuel
    Original Eqn: 2.67
    Units: kg/liter
    Limits: (None, None)
    Type: constant
    Subs: None

    2.76 kg of CO2 per Liter of diesel
    """
    return 2.67


def emitted():
    """
    Real Name: Emitted
    Original Eqn: CO2
    Units:
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return co2()


def energy():
    """
    Real Name: Energy
    Original Eqn: INTEG ( Consumption, 0)
    Units:
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return _integ_energy()


def total_area():
    """
    Real Name: Total area
    Original Eqn: 1454
    Units: km2
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return 1454


def etp():
    """
    Real Name: ETP
    Original Eqn: 1
    Units:
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return 1


def work_cost():
    """
    Real Name: Work cost
    Original Eqn: 0.02
    Units: euro/m3
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return 0.02


def industrial_water():
    """
    Real Name: Industrial water
    Original Eqn: 61921.5
    Units: m3/Month
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return 61921.5


def netonull():
    """
    Real Name: NetoNull
    Original Eqn: 1
    Units:
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return 1


def outflow():
    """
    Real Name: Outflow
    Original Eqn: IF THEN ELSE((Soil water/TIME STEP)<=0, 0 ,IF THEN ELSE((Soil water/TIME STEP)<=ETP,(Soil water/TIME STEP)=ETP , ETP ))
    Units: mm/Month
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return if_then_else(
        (soil_water() / time_step()) <= 0,
        lambda: 0,
        lambda: if_then_else(
            (soil_water() / time_step()) <= etp(),
            lambda: (soil_water() / time_step()) == etp(),
            lambda: etp(),
        ),
    )


def repairs_cost():
    """
    Real Name: Repairs cost
    Original Eqn: 0.015
    Units: euro/m3
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return 0.015


def kwh_price():
    """
    Real Name: kWh price
    Original Eqn: 0.3
    Units: euro/kWh
    Limits: (None, None)
    Type: constant
    Subs: None

    €/kWh        https://bit.ly/2UU2VwR
    """
    return 0.3


def energy_per_m3():
    """
    Real Name: Energy per m3
    Original Eqn: 0.6
    Units: kWh/m3
    Limits: (None, None)
    Type: constant
    Subs: None

    Electricity = 0,6 kWh/m3        Diesel = 0,14 l/m3
    """
    return 0.6


def water_balance():
    """
    Real Name: Water Balance
    Original Eqn: Pp-Runoff-Infiltration
    Units: mm/Month
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return pp() - runoff() - infiltration()


def pe():
    """
    Real Name: Pe
    Original Eqn: IF THEN ELSE(Pp>75, (0.8*Pp)-25 , (0.6*Pp)-10 )
    Units:
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return if_then_else(pp() > 75, lambda: (0.8 * pp()) - 25, lambda: (0.6 * pp()) - 10)


def volume():
    """
    Real Name: Volume
    Original Eqn: Thickness+Groundwater
    Units:
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return thickness() + groundwater()


def artificial_recharge():
    """
    Real Name: Artificial Recharge
    Original Eqn: 0
    Units:
    Limits: (0.0, 6.54, 0.02)
    Type: constant
    Subs: None


    """
    return 0


def kc():
    """
    Real Name: Kc
    Original Eqn: 1
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return 1


def correction():
    """
    Real Name: Correction
    Original Eqn: 5.96
    Units:
    Limits: (None, None)
    Type: constant
    Subs: None

    6.69 si el areas es 60000 ha pero 18 o más si se normaliza todo con areas
        1454
    """
    return 5.96


def base_flow():
    """
    Real Name: Base flow
    Original Eqn: (Groundwater)*Recesion time
    Units: mm/Month
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (groundwater()) * recesion_time()


def thickness():
    """
    Real Name: Thickness
    Original Eqn: 10128
    Units: m
    Limits: (0.0, 150.0, 1.0)
    Type: constant
    Subs: None


    """
    return 10128


def actualet():
    """
    Real Name: ActualET
    Original Eqn: Outflow+(Agricultural water*0.35)
    Units: mm/Month
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return outflow() + (agricultural_water() * 0.35)


def n():
    """
    Real Name: n
    Original Eqn: 0.716
    Units: Dmnl
    Limits: (0.0, 1.0, 0.01)
    Type: constant
    Subs: None

    Irrigation Efficiency Howell Table 1 - Moving big gun n = 65
    """
    return 0.716


def runoff():
    """
    Real Name: Runoff
    Original Eqn: IF THEN ELSE (Pp>(0.2*S max retention), ((Pp-(0.2*S max retention))^2)/(Pp+(0.8*S max retention)) , 0 )
    Units: mm/Month
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return if_then_else(
        pp() > (0.2 * s_max_retention()),
        lambda: ((pp() - (0.2 * s_max_retention())) ** 2)
        / (pp() + (0.8 * s_max_retention())),
        lambda: 0,
    )


def cn():
    """
    Real Name: CN
    Original Eqn: 85.7
    Units: Dmnl
    Limits: (0.0, 100.0, 1.0)
    Type: constant
    Subs: None

    Curve Number Table 4.2 Row Crops Soil A or B
    """
    return 85.7


def recesion_time():
    """
    Real Name: Recesion time
    Original Eqn: 9e-07
    Units: 1/Month
    Limits: (1e-06, 0.5, 0.0001)
    Type: constant
    Subs: None

    1/recession time
    """
    return 9e-07


def porosity():
    """
    Real Name: Porosity
    Original Eqn: 0.3
    Units: Dmnl
    Limits: (0.0, 1.0, 0.01)
    Type: constant
    Subs: None


    """
    return 0.3


def pp():
    """
    Real Name: Pp
    Original Eqn: 1
    Units: mm/Month
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return 1


def s_max_retention():
    """
    Real Name: S max retention
    Original Eqn: (25400/CN)-254
    Units: mm/Month
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (25400 / cn()) - 254


def soil_water():
    """
    Real Name: Soil water
    Original Eqn: INTEG ( Infiltration-Outflow-Recharge, 160)
    Units: mm
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return _integ_soil_water()


_integ_groundwater = Integ(
    lambda: ((recharge() - extraction() - base_flow() - river_flow()) / porosity()),
    lambda: 0,
    "_integ_groundwater",
)


_integ_co2 = Integ(lambda: emissions(), lambda: 0, "_integ_co2")


_integ_costs = Integ(lambda: generated(), lambda: 0, "_integ_costs")


_integ_energy = Integ(lambda: consumption(), lambda: 0, "_integ_energy")


_integ_soil_water = Integ(
    lambda: infiltration() - outflow() - recharge(), lambda: 160, "_integ_soil_water"
)
