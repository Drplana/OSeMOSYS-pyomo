#%%
from pyomo.environ import AbstractModel,DataPortal,Set,Param,Var,NonNegativeReals,NonNegativeIntegers,Objective,\
    Constraint
from .readXlsData import read_defaults
from pyomo.opt import SolverFactory
import json

def define_model(input_file):
    # from Data import *
    model = AbstractModel()
    data = DataPortal()
    model.YEAR = Set()               # y
    model.TECHNOLOGY = Set()           # t
    model.TIMESLICE = Set()            # l
    model.FUEL = Set()                 # f
    model.EMISSION = Set()             # e
    model.MODE_OF_OPERATION = Set()    # m
    model.REGION = Set()               # r
    model.SEASON = Set()               # ls
    model.DAYTYPE = Set()              # ld
    model.DAILYTIMEBRACKET = Set()     # lh
    model.STORAGE = Set()

    #%%
    """Reading excel Default parameter values  """
    Default = read_defaults(input_file)
    discountrate = Default.loc['DiscountRate', 'Defaul value']
    daysplit = Default.loc['DaySplit', 'Defaul value']
    conversionls = Default.loc['Conversionls', 'Defaul value']
    conversionld = Default.loc['Conversionld', 'Defaul value']
    conversionlh = Default.loc['Conversionlh', 'Defaul value']
    daysindaytype = Default.loc['DaysInDayType', 'Defaul value']
    traderoute = Default.loc['TradeRoute', 'Defaul value']
    depreciation = Default.loc['DepreciationMethod', 'Defaul value']
    sad = Default.loc['SpecifiedAnnualDemand', 'Defaul value']
    sdp = Default.loc['SpecifiedDemandProfile', 'Defaul value']
    acd = Default.loc['AccumulatedAnnualDemand', 'Defaul value']
    c2au = Default.loc['CapacityToActivityUnit', 'Defaul value']
    cf = Default.loc['CapacityFactor', 'Defaul value']
    af = Default.loc['AvailabilityFactor', 'Defaul value']
    ol = Default.loc['OperationalLife', 'Defaul value']
    rc = Default.loc['ResidualCapacity', 'Defaul value']
    iar = Default.loc['InputActivityRatio', 'Defaul value']
    oar = Default.loc['OutputActivityRatio', 'Defaul value']
    cc = Default.loc['CapitalCost', 'Defaul value']
    vc = Default.loc['VariableCost', 'Defaul value']
    fc = Default.loc['FixedCost', 'Defaul value']
    t2s = Default.loc['TechnologyToStorage', 'Defaul value']
    tfs = Default.loc['TechnologyFromStorage', 'Defaul value']
    sls = Default.loc['StorageLevelStart', 'Defaul value']
    smcr = Default.loc['StorageMaxChargeRate', 'Defaul value']
    smdr = Default.loc['StorageMaxDischargeRate', 'Defaul value']
    msc = Default.loc['MinStorageCharge', 'Defaul value']
    ols = Default.loc['OperationalLifeStorage', 'Defaul value']
    ccs = Default.loc['CapitalCostStorage', 'Defaul value']
    rsc = Default.loc['ResidualStorageCapacity', 'Defaul value']
    co1tu = Default.loc['CapacityOfOneTechnologyUnit', 'Defaul value']
    tamaxc = Default.loc['TotalAnnualMaxCapacity', 'Defaul value']
    taminc = Default.loc['TotalAnnualMinCapacity', 'Defaul value']
    tamaxci = Default.loc['TotalAnnualMaxCapacityInvestment', 'Defaul value']
    taminci = Default.loc['TotalAnnualMinCapacityInvestment', 'Defaul value']
    ttaaul = Default.loc['TotalTechnologyAnnualActivityUpperLimit', 'Defaul value']
    ttaall = Default.loc['TotalTechnologyAnnualActivityLowerLimit', 'Defaul value']
    ttmpaul = Default.loc['TotalTechnologyModelPeriodActivityUpperLimit', 'Defaul value']
    ttmpall = Default.loc['TotalTechnologyModelPeriodActivityLowerLimit', 'Defaul value']
    rmtt = Default.loc['ReserveMarginTagTechnology', 'Defaul value']
    rmtf = Default.loc['ReserveMarginTagFuel', 'Defaul value']
    rm = Default.loc['ReserveMargin', 'Defaul value']
    rtt = Default.loc['RETagTechnology', 'Defaul value']
    rtf = Default.loc['RETagFuel', 'Defaul value']
    rmpt = Default.loc['REMinProductionTarget', 'Defaul value']
    ear = Default.loc['EmissionActivityRatio', 'Defaul value']
    ep = Default.loc['EmissionsPenalty', 'Defaul value']
    aee = Default.loc['AnnualExogenousEmission', 'Defaul value']
    ael = Default.loc['AnnualEmissionLimit', 'Defaul value']
    mpee = Default.loc['ModelPeriodExogenousEmission', 'Defaul value']
    mpel = Default.loc['ModelPeriodEmissionLimit', 'Defaul value']
    #%%

    ###### Global Parameters ####
    """Parameters are defined with a p in front 
    of the name of each parameter"""

    model.p_YearSplit = Param(model.TIMESLICE, model.YEAR) #[l,y] Duration of a modelled time slice, expressed as a fraction of the year. The sum of each entry over one modelled year should equal 1.
    model.p_DiscountRate = Param(model.REGION,default = discountrate) # [r] Region specific value for the discount rate, expressed in decimals (e.g. 0.05)
    model.p_DaySplit = Param(model.DAILYTIMEBRACKET, model.YEAR, default =daysplit) # [lh,y] Length of one DailyTimeBracket in one specific day as a fraction of the year (e.g., when distinguishing between days and night: 12h/(24h*365d)).
    model.p_Conversionls = Param(model.TIMESLICE,model.SEASON, default = conversionls ) #[ls,l] Binary parameter linking one TimeSlice to a certain Season. It has value 0 if the TimeSlice does not pertain to the specific season, 1 if it does.
    model.p_Conversionld = Param(model.TIMESLICE,model.DAYTYPE, default = conversionld) #[ld,l] Binary parameter linking one TimeSlice to a certain DayType. It has value 0 if the TimeSlice does not pertain to the specific DayType, 1 if it does.
    model.p_Conversionlh = Param(model.TIMESLICE,model.DAILYTIMEBRACKET, default = conversionlh) #[lh,l]Binary parameter linking one TimeSlice to a certain DaylyTimeBracket. It has value 0 if the TimeSlice does not pertain to the specific DaylyTimeBracket, 1 if it does.
    model.p_DaysInDayType = Param(model.SEASON,model.DAYTYPE,model.YEAR, default = daysindaytype) # [ls,ld,y]Number of days for each day type, within one week (natural number, ranging from 1 to 7)
    model.p_TradeRoute = Param(model.REGION,model.REGION,model.FUEL,model.YEAR, default = traderoute)  #[r,rr,f,y] Binary parameter defining the links between region r and region rr, to enable or disable trading of a specific commodity. It has value 1 when two regions are linked, 0 otherwise
    model.p_DepreciationMethod = Param(model.REGION, default=depreciation) # [r] Binary parameter defining the type of depreciation to be applied. It has value 1 for sinking fund depreciation, value 2 for straight-line depreciation.

    ###### Demands in (PJ) 1GWh - 0.0036 PJ ###########
    """SpecifiedAnnualDemand[r,f,y] - Total specified demand for the year, 
    linked to a specific ‘time of use’ during the year."""
    model.p_SpecifiedAnnualDemand = Param(model.REGION,model.FUEL,model.YEAR, default = sad)

    """SpecifiedDemandProfile[r,f,l,y] - Annual fraction of energy-service or commodity demand
     that is required in each time slice. For each year, all the defined SpecifiedDemandProfile 
     input values should sum up to 1."""
    model.p_SpecifiedDemandProfile = Param(model.REGION,model.FUEL,model.TIMESLICE,model.YEAR, default = sdp)

    """AccumulatedAnnualDemand[r,f,y] - Accumulated Demand for a certain commodity in one specific year. 
    It cannot be defined for a commodity if its SpecifiedAnnualDemand for the same year is already defined and vice versa. """
    model.p_AccumulatedAnnualDemand = Param(model.REGION,model.FUEL,model.YEAR, default = acd)

    ######## Performance ########
    """ CapacityToActivityUnit[r,t] - Conversion factor relating the energy that would be produced 
    when one unit of capacity is fully used in one year."""
    model.p_CapacityToActivityUnit = Param(model.REGION, model.TECHNOLOGY, default = c2au)

    """CapacityFactor[r,t,l,y] - Capacity available per each TimeSlice expressed as
     a fraction of the total installed capacity, with values ranging from 0 to 1. 
     It gives the possibility to account for forced outages."""
    model.p_CapacityFactor = Param(model.REGION,model.TECHNOLOGY,model.TIMESLICE,model.YEAR, default = cf )

    """AvailabilityFactor[r,t,y] - Maximum time a technology can run in the whole year, 
    as a fraction of the year ranging from 0 to 1. It gives the possibility to account for planned outages."""
    model.p_AvailabilityFactor = Param(model.REGION,model.TECHNOLOGY,model.YEAR, default = af)

    """OperationalLife[r,t] - Useful lifetime of a technology, expressed in years."""
    model.p_OperationalLife = Param(model.REGION,model.TECHNOLOGY, default =ol)

    """ResidualCapacity[r,t,y]- Remained capacity available from before the modelling period."""
    model.p_ResidualCapacity  = Param(model.REGION,model.TECHNOLOGY,model.YEAR, default= rc)

    """InputActivityRatio[r,t,f,m,y] - Rate of use of a commodity by a technology, 
    as a ratio of the rate of activity. """
    model.p_InputActivityRatio = Param(model.REGION,model.TECHNOLOGY,model.FUEL,
                                       model.MODE_OF_OPERATION,model.YEAR, default = iar)
    """OutputActivityRatio[r,t,f,m,y] - Rate of commodity output from a technology, 
    as a ratio of the rate of activity.	"""
    model.p_OutputActivityRatio = Param(model.REGION,model.TECHNOLOGY,model.FUEL,
                                        model.MODE_OF_OPERATION,model.YEAR, default = oar)

    ######## Technology Costs #########
    """CapitalCost[r,t,y]-Capital investment cost of a technology, per unit of capacity. $/kW"""
    model.p_CapitalCost = Param(model.REGION,model.TECHNOLOGY,model.YEAR, default = cc )
    """VariableCost[r,t,m,y] - Cost of a technology for a given mode of operation (Variable O&M cost), 
    per unit of activity.$/GJ"""
    model.p_VariableCost = Param(model.REGION,model.TECHNOLOGY,model.MODE_OF_OPERATION,model.YEAR, default = vc )
    """FixedCost[r,t,y] - Fixed O&M cost of a technology, per unit of capacity.$/kW/yr"""
    model.p_FixedCost = Param(model.REGION,model.TECHNOLOGY,model.YEAR, default = fc )




    ######### Storage ######
    """TechnologyToStorage[r,t,s,m] - Binary parameter linking a technology to the storage facility it charges. 
    It has value 1 if the technology and the storage facility are linked, 0 otherwise."""
    model.p_TechnologyToStorage = Param(model.REGION,model.TECHNOLOGY,model.STORAGE,model.MODE_OF_OPERATION, default = t2s)

    """TechnologyFromStorage[r,t,s,m] - Binary parameter linking a storage facility to the technology it feeds. 
    It has value 1 if the technology and the storage facility are linked, 0 otherwise."""
    model.p_TechnologyFromStorage =  Param(model.REGION,model.TECHNOLOGY,model.STORAGE,model.MODE_OF_OPERATION, default = tfs)

    """StorageLevelStart[r,s] - Level of storage at the beginning of first modelled year, in units of activity."""
    model.p_StorageLevelStart = Param(model.REGION,model.STORAGE, default = sls )

    """StorageMaxChargeRate[r,s]-Maximum charging rate for the storage, in units of activity per year."""
    model.p_StorageMaxChargeRate = Param(model.REGION,model.STORAGE, default = smcr)

    """StorageMaxDischargeRate[r,s] - Maximum discharging rate for the storage, in units of activity per year."""
    model.p_StorageMaxDischargeRate =  Param(model.REGION,model.STORAGE, default= smdr)

    """MinStorageCharge[r,s,y] - It sets a lower bound to the amount of energy stored, 
    as a fraction of the maximum, with a number reanging between 0 and 1. The storage 
    facility cannot be emptied below this level."""
    model.p_MinStorageCharge = Param(model.REGION,model.STORAGE,model.YEAR, default = msc)

    """OperationalLifeStorage[r,s] - Useful lifetime of the storage facility."""
    model.p_OperationalLifeStorage = Param(model.REGION,model.STORAGE, default = ols)
    """CapitalCostStorage[r,s,y] - Investment costs of storage additions, defined per unit of storage capacity."""
    model.p_CapitalCostStorage  = Param(model.REGION,model.STORAGE,model.YEAR, default = ccs)
    """ResidualStorageCapacity[r,s,y] - Exogenously defined storage capacities."""
    model.p_ResidualStorageCapacity = Param(model.REGION,model.STORAGE,model.YEAR, default = rsc)

    ######## Capacity constraints #########"
    """CapacityOfOneTechnologyUnit[r,t,y] - Capacity of one new unit of a technology. 
    In case the user sets this parameter, the related technology will be installed only 
    in batches of the specified capacity and the problem will turn into a Mixed Integer Linear Problem."""
    model.p_CapacityOfOneTechnologyUnit = Param(model.REGION,model.TECHNOLOGY,model.YEAR, default = co1tu)

    """TotalAnnualMaxCapacity[r,t,y] - Total maximum existing (residual plus cumulatively installed) 
    capacity allowed for a technology in a specified year."""
    model.p_TotalAnnualMaxCapacity = Param(model.REGION,model.TECHNOLOGY,model.YEAR, default = tamaxc)

    """TotalAnnualMinCapacity[r,t,y]  - Total minimum existing (residual plus cumulatively installed) 
    capacity allowed for a technology in a specified year."""
    model.p_TotalAnnualMinCapacity = Param(model.REGION,model.TECHNOLOGY,model.YEAR, default = taminc)

    """TotalAnnualMaxCapacityInvestment[r,t,y]-Maximum capacity of a technology, expressed in power units."""
    model.p_TotalAnnualMaxCapacityInvestment = Param(model.REGION,model.TECHNOLOGY,model.YEAR, default = tamaxci)
    """TotalAnnualMinCapacityInvestment[r,t,y]-Minimum capacity of a technology, expressed in power units."""
    model.p_TotalAnnualMinCapacityInvestment = Param(model.REGION,model.TECHNOLOGY,model.YEAR, default = taminci )

    ########### Activity constraints PJ #########
    """TotalTechnologyAnnualActivityUpperLimit[r,t,y]-Total maximum level of activity allowed for a technology in one year."""
    model.p_TotalTechnologyAnnualActivityUpperLimit = Param(model.REGION,model.TECHNOLOGY,model.YEAR, default = ttaaul)
    """TotalTechnologyAnnualActivityLowerLimit[r,t,y] - Total minimum level of activity allowed for a technology in one year."""
    model.p_TotalTechnologyAnnualActivityLowerLimit = Param(model.REGION,model.TECHNOLOGY,model.YEAR, default = ttaall)
    """TotalTechnologyModelPeriodActivityUpperLimit[r,t]-Total maximum level of activity 
    allowed for a technology in the entire modelled period."""
    model.p_TotalTechnologyModelPeriodActivityUpperLimit = Param(model.REGION,model.TECHNOLOGY, default = ttmpaul)
    """TotalTechnologyModelPeriodActivityLowerLimit[r,t]-Total minimum level of activity 
    allowed for a technology in the entire modelled period."""
    model.p_TotalTechnologyModelPeriodActivityLowerLimit  = Param(model.REGION,model.TECHNOLOGY, default = ttmpall)

    ######## Reserve margin #########
    """ReserveMarginTagTechnology[r,t,y] - Binary parameter tagging the technologies that are allowed 
    to contribute to the reserve margin. It has value 1 for the technologies allowed, 0 otherwise."""
    model.p_ReserveMarginTagTechnology = Param(model.REGION,model.TECHNOLOGY,model.YEAR, default = int(rmtt))

    """ReserveMarginTagFuel[r,f,y]	Binary parameter tagging the fuels to which the reserve margin applies. 
    It has value 1 if the reserve margin applies to the fuel, 0 otherwise."""
    model.p_ReserveMarginTagFuel = Param(model.REGION,model.FUEL,model.YEAR, default = rmtf)

    """ReserveMargin[r,y]	Minimum level of the reserve margin required to be provided for all the tagged 
    commodities, by the tagged technologies. If no reserve margin is required, the parameter will have value 1; 
    if, for instance, 20% reserve margin is required, the parameter will have value 1.2."""
    model.p_ReserveMargin = Param(model.REGION,model.YEAR, default = rm )
    #######################################################################
    ######                   RE Generation target                     #####
    """RETagTechnology[r,t,y] -	Binary parameter tagging the renewable technologies
     that must contribute to reaching the indicated minimum renewable production target. 
     It has value 1 for thetechnologies contributing, 0 otherwise."""
    model.p_RETagTechnology = Param(model.REGION,model.TECHNOLOGY,model.YEAR, default = rtt)

    """RETagFuel[r,f,y] - Binary parameter tagging the fuels to which the renewable 
    target applies to. It has value 1 if the target applies, 0 otherwise."""
    model.p_RETagFuel = Param(model.REGION,model.FUEL,model.YEAR, default = rtf)

    """REMinProductionTarget[r,y] - Minimum ratio of all renewable commodities tagged 
    in the RETagCommodity parameter, to be produced by the technologies tagged with the RETechnology parameter."""
    model.p_REMinProductionTarget = Param(model.REGION,model.YEAR, default = rmpt)
    ########################################################################
    ######                        Emissions                         ########
    """EmissionActivityRatio[r,t,e,m,y] - Emission factor of a technology per unit of activity, per mode of operation."""
    model.p_EmissionActivityRatio = Param(model.REGION, model.TECHNOLOGY,model.EMISSION,
                                          model.MODE_OF_OPERATION,model.YEAR, default = ear)

    """EmissionsPenalty[r,e,y] - Penalty per unit of emission."""
    model.p_EmissionsPenalty = Param(model.REGION,model.EMISSION,model.YEAR, default = ep)

    """AnnualExogenousEmission[r,e,y]	It allows the user to account for additional annual emissions, 
    on top of those computed endogenously by the model (e.g. emissions generated outside the region)."""
    model.p_AnnualExogenousEmission = Param(model.REGION,model.EMISSION,model.YEAR, default= aee)

    """AnnualEmissionLimit[r,e,y] - Annual upper limit for a specific emission generated in the whole modelled region."""
    model.p_AnnualEmissionLimit = Param(model.REGION,model.EMISSION,model.YEAR, default = ael)

    """ModelPeriodExogenousEmission[r,e] - It allows the user to account for additional 
    emissions over the entire modelled period, on top of those computed endogenously by the model 
    (e.g. generated outside the region)."""
    model.p_ModelPeriodExogenousEmission = Param(model.REGION,model.EMISSION, default = mpee)

    """ModelPeriodEmissionLimit[r,e]	Annual upper limit for a specific emission generated
     in the whole modelled region, over the entire modelled period."""
    model.p_ModelPeriodEmissionLimit = Param(model.REGION,model.EMISSION, default = mpel)





                         ###########################
                         ######## Variables ########
                         ###########################
    """ Variables are defined with a v in front of the name of each variable"""
    #########################################################################
    #########                      Demands                             ######
    """RateOfDemand[r,l,f,y]>=0 Intermediate variable. It represents the energy that would 
    be demanded in one time slice l if the latter lasted the whole year. It is a function 
    of the parameters SpecifiedAnnualDemand and SpecifiedDemandProfile. | Energy (per year)"""
    model.v_RateOfDemand = Var(model.REGION,
                               model.TIMESLICE,
                               model.FUEL,model.YEAR,
                               within = NonNegativeReals,
                               )

    """Demand[r,l,f,y]>=0 -	Demand for one fuel in one time slice.	Energy"""
    model.v_Demand = Var(model.REGION,
                         model.TIMESLICE,
                         model.FUEL,model.YEAR,
                         domain = NonNegativeReals,
                         )
    #########################################################################
    ##########                 Storage Variables                      #######
    """RateOfStorageCharge[r,s,ls,ld,lh,y]	Intermediate variable. It represents the 
    commodity that would be charged to the storage facility s in one time slice if the 
    latter lasted the whole year. It is a function of the RateOfActivity and the parameter 
    TechnologyToStorage. | Energy (per year)"""
    model.v_RateOfStorageCharge = Var(model.REGION,
                                      model.STORAGE,
                                      model.SEASON,
                                      model.DAYTYPE,
                                      model.DAILYTIMEBRACKET,
                                      model.YEAR,
                                      )
    """RateOfStorageDischarge[r,s,ls,ld,lh,y]	Intermediate variable. It represents 
    the commodity that would be discharged from storage facility s in one time slice 
    if the latter lasted the whole year. It is a function of the RateOfActivity and 
    the parameter TechnologyFromStorage.	Energy (per year)"""
    model.v_RateOfStorageDischarge = Var(model.REGION,
                                         model.STORAGE,
                                         model.SEASON,
                                         model.DAYTYPE,
                                         model.DAILYTIMEBRACKET,
                                         model.YEAR,
                                         )

    """NetChargeWithinYear[r,s,ls,ld,lh,y]	Net quantity of commodity charged to storage 
    facility s in year y. It is a function of the RateOfStorageCharge and the RateOfStorageDischarge
     and it can be negative.	Energy"""
    model.v_NetChargeWithinYear = Var(model.REGION,
                                      model.STORAGE,
                                      model.SEASON,
                                      model.DAYTYPE,
                                      model.DAILYTIMEBRACKET,
                                      model.YEAR,
                                      )

    """NetChargeWithinDay[r,s,ls,ld,lh,y]	Net quantity of commodity charged to storage 
    facility s in daytype ld. It is a function of the RateOfStorageCharge and the 
    RateOfStorageDischarge and can be negative.	Energy"""
    model.v_NetChargeWithinDay = Var(model.REGION,model.STORAGE,model.SEASON,
                                      model.DAYTYPE,model.DAILYTIMEBRACKET,model.YEAR)
    """StorageLevelYearStart[r,s,y]>=0	Level of stored commodity in storage facility s 
    in the first time step of year y.	Energy"""
    model.v_StorageLevelYearStart = Var(model.REGION,model.STORAGE,model.YEAR,
                                        domain = NonNegativeReals)
    """StorageLevelYearFinish[r,s,y]>=0	Level of stored commodity in storage 
    facility s in the last time step of year y.	Energy"""
    model.v_StorageLevelYearFinish = Var(model.REGION,model.STORAGE,model.YEAR,
                                         domain = NonNegativeReals)
    """StorageLevelSeasonStart[r,s,ls,y]>=0	Level of stored commodity in storage
     facility s in the first time step of season ls.	Energy"""
    model.v_StorageLevelSeasonStart = Var(model.REGION,model.STORAGE,model.SEASON,model.YEAR,
                                         domain = NonNegativeReals)
    """StorageLevelDayTypeStart[r,s,ls,ld,y]>=0	Level of stored commodity in storage 
    facility s in the first time step of daytype ld.	Energy"""
    model.v_StorageLevelDayTypeStart = Var(model.REGION,model.STORAGE,model.SEASON,
                                   model.DAYTYPE,model.YEAR, domain = NonNegativeReals)
    """StorageLevelDayTypeFinish[r,s,ls,ld,y]>=0	Level of stored commodity in storage 
    facility s in the last time step of daytype ld.	Energy"""
    model.v_StorageLevelDayTypeFinish =  Var(model.REGION,model.STORAGE,model.SEASON,
                                   model.DAYTYPE,model.YEAR, domain = NonNegativeReals)
    """StorageLowerLimit[r,s,y]>=0	Minimum allowed level of stored commodity in 
    storage facility s, as a function of the storage capacity and the user-defined 
    MinStorageCharge ratio.	Energy"""
    model.v_StorageLowerLimit = Var(model.REGION, model.STORAGE, model.YEAR,
                                    domain = NonNegativeReals)
    """StorageUpperLimit[r,s,y]>=0	Maximum allowed level of stored commodity in storage
     facility s. It corresponds to the total existing capacity of storage facility s 
     (summing newly installed and pre-existing capacities).	Energy"""
    model.v_StorageUpperLimit = Var(model.REGION, model.STORAGE, model.YEAR,
                                    domain = NonNegativeReals)
    """AccumulatedNewStorageCapacity[r,s,y]>=0	Cumulative capacity of newly installed 
    storage from the beginning of the time domain to year y.	Energy"""
    model.v_AccumulatedNewStorageCapacity = Var(model.REGION, model.STORAGE, model.YEAR,
                                    domain = NonNegativeReals)
    """NewStorageCapacity[r,s,y]>=0	Capacity of newly installed storage in year y.	Energy"""
    model.v_NewStorageCapacity = Var(model.REGION, model.STORAGE, model.YEAR,
                                    domain = NonNegativeReals)
    """CapitalInvestmentStorage[r,s,y]>=0	Undiscounted investment in new capacity 
    for storage facility s. Derived from the NewStorageCapacity and the parameter 
    CapitalCostStorage.Monetary units"""
    model.v_CapitalInvestmentStorage = Var(model.REGION, model.STORAGE, model.YEAR,
                                    domain = NonNegativeReals)
    """DiscountedCapitalInvestmentStorage[r,s,y]>=0	Investment in new capacity for 
    storage facility s, discounted through the parameter DiscountRate.	Monetary units"""
    model.v_DiscountedCapitalInvestmentStorage = Var(model.REGION, model.STORAGE, model.YEAR,
                                    domain = NonNegativeReals)
    """SalvageValueStorage[r,s,y]>=0	Salvage value of storage facility s in year y, 
    as a function of the parameters OperationalLifeStorage and DepreciationMethod.	Monetary units"""
    model.v_SalvageValueStorage = Var(model.REGION, model.STORAGE, model.YEAR,
                                    domain = NonNegativeReals)
    """DiscountedSalvageValueStorage[r,s,y]>=0	Salvage value of storage facility s, 
    discounted through the parameter DiscountRate.	Monetary units"""
    model.v_DiscountedSalvageValueStorage = Var(model.REGION, model.STORAGE, model.YEAR,
                                    domain = NonNegativeReals)
    """TotalDiscountedStorageCost[r,s,y]>=0	Difference between the discounted capital 
    investment in new storage facilities and the salvage value in year y. Monetary units"""
    model.v_TotalDiscountedStorageCost = Var(model.REGION, model.STORAGE, model.YEAR,
                                    domain = NonNegativeReals)
    ############################################################################
    #######                      CAPACITY VARIABLES                      #######
    """NumberOfNewTechnologyUnits[r,t,y]>=0, integer	Number of newly installed units 
    of technology t in year y, as a function of the parameter CapacityOfOneTechnologyUnit. | No unit"""
    model.v_NumberOfNewTechnologyUnits = Var(model.REGION, model.TECHNOLOGY, model.YEAR,
                                             domain= NonNegativeIntegers, initialize=0.0)
    """NewCapacity[r,t,y]>=0 Newly installed capacity of technology t in year y. Power"""
    model.v_NewCapacity = Var(model.REGION, model.TECHNOLOGY, model.YEAR,
                              domain = NonNegativeReals)
    """AccumulatedNewCapacity[r,t,y]>=0	Cumulative newly installed capacity of technology t 
    from the beginning of the time domain to year y. Power"""
    model.v_AccumulatedNewCapacity =  Var(model.REGION, model.TECHNOLOGY, model.YEAR,
                              domain = NonNegativeReals)
    """TotalCapacityAnnual[r,t,y]>=0 - Total existing capacity of technology t in 
    year y (sum of cumulative newly installed and pre-existing capacity). Power"""
    model.v_TotalCapacityAnnual = Var(model.REGION, model.TECHNOLOGY, model.YEAR,
                              domain = NonNegativeReals, initialize = 0.0)
    #############################################################################
    ######                      Activity variables                        #######
    """RateOfActivity[r,l,t,m,y] >=0	Intermediate variable. It represents the 
    activity of technology t in one mode of operation and in time slice l, if the 
    latter lasted the whole year. | Energy (per year)"""
    model.v_RateOfActivity = Var(model.REGION, model.TIMESLICE, model.TECHNOLOGY,
                                 model.MODE_OF_OPERATION,model.YEAR, domain = NonNegativeReals )
    """RateOfTotalActivity[r,t,l,y] >=0	Sum of the RateOfActivity of a technology 
    over the modes of operation.	Energy (per year)"""
    model.v_RateOfTotalActivity =  Var(model.REGION, model.TECHNOLOGY, model.TIMESLICE,
                                 model.YEAR, domain = NonNegativeReals  )
    """TotalTechnologyAnnualActivity[r,t,y] >=0	Total annual activity of technology t.	Energy"""
    model.v_TotalTechnologyAnnualActivity = Var(model.REGION, model.TECHNOLOGY,
                                 model.YEAR, domain = NonNegativeReals  )
    """TotalAnnualTechnologyActivityByMode[r,t,m,y] >=0	Annual activity of technology 
    t in mode of operation m.	Energy"""
    model.v_TotalAnnualTechnologyActivityByMode = Var(model.REGION, model.TECHNOLOGY, model.MODE_OF_OPERATION,
                                 model.YEAR, domain = NonNegativeReals  )
    """TotalTechnologyModelPeriodActivity[r,t]	Sum of the TotalTechnologyAnnualActivity 
    over the years of the modelled period.	Energy"""
    model.v_TotalTechnologyModelPeriodActivity = Var(model.REGION,model.TECHNOLOGY, domain = NonNegativeReals )
    """RateOfProductionByTechnologyByMode[r,l,t,m,f,y] >=0	Intermediate variable. 
    It represents the quantity of fuel f that technology t would produce in one mode
     of operation and in time slice l, if the latter lasted the whole year. 
     It is a function of the variable RateOfActivity and the parameter OutputActivityRatio.	
     Energy (per year)"""
    model.v_RateOfProductionByTechnologyByMode = Var(model.REGION, model.TIMESLICE, model.TECHNOLOGY,
                                                     model.MODE_OF_OPERATION, model.FUEL, model.YEAR,
                                                     domain = NonNegativeReals, initialize = 0.0 )
    """RateOfProductionByTechnology[r,l,t,f,y] >=0	Sum of the RateOfProductionByTechnologyByMode 
    over the modes of operation.	Energy (per year)"""
    model.v_RateOfProductionByTechnology = Var (model.REGION, model.TIMESLICE, model.TECHNOLOGY,
                                                 model.FUEL,model.YEAR, domain = NonNegativeReals )
    """ProductionByTechnology[r,l,t,f,y] >=0	Production of fuel f by technology t in time slice l. Energy"""
    model.v_ProductionByTechnology  = Var( model.REGION,model.TIMESLICE, model.TECHNOLOGY, model.FUEL,
                                        model.YEAR, domain = NonNegativeReals )

    """ProductionByTechnologyAnnual[r,t,f,y] >=0	Annual production of fuel f by technology t. Energy"""
    model.v_ProductionByTechnologyAnnual = Var(model.REGION, model.TECHNOLOGY, model.FUEL, model.YEAR,
                                                domain = NonNegativeReals )
    """RateOfProduction[r,l,f,y] >=0 Sum of the RateOfProductionByTechnology over all the technologies.	Energy (per year)"""
    model.v_RateOfProduction  = Var(model.REGION, model.TIMESLICE, model.FUEL,
                                    model.YEAR, domain = NonNegativeReals )
    """Production[r,l,f,y] >=0	Total production of fuel f in time slice l. It is the 
    sum of the ProductionByTechnology over all technologies. Energy"""
    model.v_Production = Var(model.REGION, model.TIMESLICE, model.FUEL, model.YEAR, domain = NonNegativeReals )

    """RateOfUseByTechnologyByMode[r,l,t,m,f,y] >=0	Intermediate variable. It represents the quantity of fuel f 
    that technology t would use in one mode of operation and in time slice l, if the latter lasted the whole year. 
    It is the function of the variable RateOfActivity and the parameter InputActivityRatio.	Energy (per year)"""
    model.v_RateOfUseByTechnologyByMode  = Var(model.REGION,model.TIMESLICE, model.TECHNOLOGY,
                        model.MODE_OF_OPERATION, model.FUEL,model.YEAR, domain = NonNegativeReals, initialize = 0.0 )
    """RateOfUseByTechnology[r,l,t,f,y] >=0	Sum of the RateOfUseByTechnologyByMode over the modes of operation.	Energy (per year)"""
    model.v_RateOfUseByTechnology =  Var(model.REGION,model.TIMESLICE, model.TECHNOLOGY,
                                                model.FUEL,model.YEAR, domain = NonNegativeReals )

    model.v_RateOfUse = Var(model.REGION, model. TIMESLICE, model.FUEL, model.YEAR, domain = NonNegativeReals)
    """UseByTechnologyAnnual[r,t,f,y] >=0 Annual use of fuel f by technology t. Energy"""
    model.v_UseByTechnologyAnnual =  Var(model.REGION, model.TECHNOLOGY,
                                        model.FUEL,model.YEAR, domain = NonNegativeReals )
    """ UseByTechnology[r,l,t,f,y] >=0	Use of fuel f by technology t in time slice l. Energy"""
    model.v_UseByTechnology = Var(model.REGION,model.TIMESLICE, model.TECHNOLOGY,
                                model.FUEL,model.YEAR, domain = NonNegativeReals )
    """Use[r,l,f,y] >=0	Total use of fuel f in time slice l. It is the sum of the UseByTechnology over all technologies. Energy"""
    model.v_Use = Var(model.REGION,model.TIMESLICE, model.FUEL,model.YEAR, domain = NonNegativeReals )

    """Trade[r,rr,l,f,y] Quantity of fuel f traded be@tween region r and rr in time slice l. Energy"""
    model.v_Trade = Var(model.REGION, model.REGION, model.TIMESLICE,model.FUEL,model.YEAR )

    """TradeAnnual[r,rr,f,y] Annual quantity of fuel f traded between region r and rr. 
    It is the sum of the variable Trade over all the time slices.	Energy"""
    model.v_TradeAnnual = Var(model.REGION, model.REGION, model.FUEL,model.YEAR )

    """ProductionAnnual[r,f,y] >=0	Total annual production of fuel f. It is the sum of 
    the variable Production over all technologies. Energy"""
    model.v_ProductionAnnual = Var(model.REGION, model.FUEL, model.YEAR, domain = NonNegativeReals )

    """UseAnnual[r,f,y] >=0	Total annual use of fuel f. It is the sum of the variable Use over all technologies. Energy"""
    model.v_UseAnnual = Var(model.REGION, model.FUEL, model.YEAR, domain = NonNegativeReals )
    ##########################################################################################
    ###############                   Costing Variables           ############################
    """CapitalInvestment[r,t,y] >=0	Undiscounted investment in new capacity of technology t. 
    It is a function of the NewCapacity and the parameter CapitalCost. | Monetary units"""
    model.v_CapitalInvestment = Var(model.REGION, model.TECHNOLOGY, model.YEAR, domain = NonNegativeReals )
    """DiscountedCapitalInvestment[r,t,y] >=0	Investment in new capacity of technology t, 
    discounted through the parameter DiscountRate.	Monetary units"""
    model.v_DiscountedCapitalInvestment = Var(model.REGION, model.TECHNOLOGY, model.YEAR, domain = NonNegativeReals )
    """SalvageValue[r,t,y] >=0	Salvage value of technology t in year y, as a function of the parameters 
    OperationalLife and DepreciationMethod. Monetary units"""
    model.v_SalvageValue = Var(model.REGION, model.TECHNOLOGY, model.YEAR, domain = NonNegativeReals )
    """DiscountedSalvageValue[r,t,y] >=0 Salvage value of technology t, discounted through the parameter DiscountRate. Monetary units"""
    model.v_DiscountedSalvageValue  = Var(model.REGION, model.TECHNOLOGY, model.YEAR, domain = NonNegativeReals )
    """OperatingCost[r,t,y] >=0	Undiscounted sum of the annual variable and fixed operating costs of technology t.	Monetary units"""
    model.v_OperatingCost =  Var(model.REGION, model.TECHNOLOGY, model.YEAR, domain = NonNegativeReals )
    """DiscountedOperatingCost[r,t,y] >=0 Annual OperatingCost of technology t, discounted through the parameter DiscountRate. Monetary units"""
    model.v_DiscountedOperatingCost = Var(model.REGION, model.TECHNOLOGY, model.YEAR, domain = NonNegativeReals )
    """AnnualVariableOperatingCost[r,t,y] >=0	Annual variable operating cost of technology t. Derived from the 
    TotalAnnualTechnologyActivityByMode and the parameter VariableCost. Monetary units"""
    model.v_AnnualVariableOperatingCost = Var(model.REGION, model.TECHNOLOGY, model.YEAR, domain = NonNegativeReals )
    """AnnualFixedOperatingCost[r,t,y] >=0	Annual fixed operating cost of technology t. 
    Derived from the TotalCapacityAnnual and the parameter FixedCost.	Monetary units"""
    model.v_AnnualFixedOperatingCost = Var(model.REGION, model.TECHNOLOGY, model.YEAR, domain = NonNegativeReals )
    """TotalDiscountedCostByTechnology[r,t,y] >=0 Difference between the sum of discounted operating 
    cost / capital cost / emission penalties and the salvage value. Monetary units"""
    model.v_TotalDiscountedCostByTechnology = Var(model.REGION, model.TECHNOLOGY, model.YEAR, domain = NonNegativeReals )
    """TotalDiscountedCost[r,y] >=0	Sum of the TotalDiscountedCostByTechnology over all the technologies. Monetary units"""
    model.v_TotalDiscountedCost = Var(model.REGION, model.YEAR, domain = NonNegativeReals )
    """ModelPeriodCostByRegion[r] >=0 Sum of the TotalDiscountedCost over all modelled years. Monetary units"""
    model.v_ModelPeriodCostByRegion = Var(model.REGION, domain = NonNegativeReals )
    ################################################################################################
    ##################                      Reserve Margin               ###########################
    """TotalCapacityInReserveMargin[r,y] >=0 Total available capacity of the technologies required to provide reserve margin. 
    It is derived from the TotalCapacityAnnual and the parameter ReserveMarginTagTechnology. | Energy"""
    model.v_TotalCapacityInReserveMargin = Var(model.REGION, model.YEAR, domain = NonNegativeReals, initialize = 0.0 )
    """DemandNeedingReserveMargin[r,l,y] >=0 Quantity of fuel produced that is assigned to a target of reserve margin. 
    Derived from the RateOfProduction and the parameter ReserveMarginTagFuel. Energy (per year)"""
    model.v_DemandNeedingReserveMargin = Var(model.REGION,model.TIMESLICE, model.YEAR, domain = NonNegativeReals )
    ################################################################################################
    #################                  Renewable Generation Target        ##########################
    """TotalREProductionAnnual[r,y]	Annual production by all technologies tagged as renewable in the model. 
    Derived from the ProductionByTechnologyAnnual and the parameter RETagTechnology. Energy"""
    model.v_TotalREProductionAnnual = Var(model.REGION, model.YEAR )
    """RETotalProductionOfTargetFuelAnnual[r,y]	Annual production of fuels tagged as renewable in the model. 
    Derived from the RateOfProduction and the parameter RETagFuel.	Energy"""
    model.v_RETotalProductionOfTargetFuelAnnual = Var(model.REGION, model.YEAR )
    #################################################################################################
    ##################                    Emissions                     #############################
    """AnnualTechnologyEmissionByMode[r,t,e,m,y] >=0 Annual emission of agent e by technology t in mode of operation m. 
    Derived from the RateOfActivity and the parameter EmissionActivityRatio. Quantity of emission"""
    model.v_AnnualTechnologyEmissionByMode = Var(model.REGION,model.TECHNOLOGY,model.EMISSION,
                                            model.MODE_OF_OPERATION,model.YEAR, domain = NonNegativeReals )
    """AnnualTechnologyEmission[r,t,e,y] >=0 Sum of the AnnualTechnologyEmissionByMode over the modes of operation. Quantity of emission"""
    model.v_AnnualTechnologyEmission = Var(model.REGION,model.TECHNOLOGY,model.EMISSION,model.YEAR,
                                            domain = NonNegativeReals )
    """AnnualTechnologyEmissionPenaltyByEmission[r,t,e,y] >=0 Undiscounted annual cost of emission e by technology t. 
    It is a function of the AnnualTechnologyEmission and the parameter EmissionPenalty.	Monetary units"""
    model.v_AnnualTechnologyEmissionPenaltyByEmission  = Var(model.REGION,model.TECHNOLOGY,model.EMISSION,
                                                            model.YEAR, domain = NonNegativeReals )
    """AnnualTechnologyEmissionsPenalty[r,t,y] >=0 Total undiscounted annual cost of all emissions generated by technology t. 
    Sum of the AnnualTechnologyEmissionPenaltyByEmission over all the emitted agents. Monetary units"""
    model.v_AnnualTechnologyEmissionsPenalty = Var(model.REGION,model.TECHNOLOGY, model.YEAR, domain = NonNegativeReals )
    """DiscountedTechnologyEmissionsPenalty[r,t,y] >=0	Annual cost of emissions by technology t, 
    discounted through the DiscountRate. Monetary units"""
    model.v_DiscountedTechnologyEmissionsPenalty = Var(model.REGION,model.TECHNOLOGY, model.YEAR, domain = NonNegativeReals )
    """AnnualEmissions[r,e,y] >=0 Sum of the AnnualTechnologyEmission over all technologies. Quantity of emission"""
    model.v_AnnualEmissions = Var(model.REGION,model.EMISSION,model.YEAR, domain = NonNegativeReals )
    """ModelPeriodEmissions[r,e] >=0	Total system emissions of agent e in the model period, accounting for both 
    the emissions by technologies and the user defined ModelPeriodExogenousEmission. Quantity of emission"""
    model.v_ModelPeriodEmissions = Var(model.REGION,model.EMISSION, domain = NonNegativeReals )

    ###############################################################
    """ New parameters and variables added to the original model"""
    ###############################################################

    """Variables"""
    """ConnectedUnits[r,t,l,y] - Number of Conected Units in each TimeSlice"""
    model.v_ConnectedUnits = Var(model.REGION, model.TECHNOLOGY, model.SEASON, model.YEAR,
                                 domain=NonNegativeIntegers, initialize=0.0)
    """"probando nueva capacidad residual"""
    model.v_ResidualCapacity  = Var(model.REGION,model.TECHNOLOGY,model.YEAR)
    # model.v_RecuperadasAcumuladas = Var(model.REGION, model.TECHNOLOGY, model.YEAR, domain = NonNegativeReals, initialize=0.0)
    # model.v_Recuperadas = Var(model.REGION, model.TECHNOLOGY, model.YEAR, domain = NonNegativeReals, initialize=0.0)
    model.v_NumeroUnidadesRecuperadas = Var(model.REGION, model.TECHNOLOGY, model.YEAR, domain=NonNegativeIntegers, initialize=0.0)
    #model.v_UnidadesFinVida = Var(model.REGION, model.TECHNOLOGY, model.YEAR, domain=NonNegativeIntegers, initialize=0.0)

    """Parameters"""

    ''' Costo no asociado a la generacion'''
    model.p_CostoNoAsociado = Param(model.REGION, model.TECHNOLOGY, model.YEAR, default = 0)
    """MinimunOperatingLoad[r,t,y] - Minimum load could operate a technology"""
    model.p_MinimumOperatingLoad = Param(model.REGION, model.TECHNOLOGY, model.YEAR, default = 0)
    #### Disponibilidad de adquirir una tecnologia, disponibilidad en el mercado en un momento dado, capacidad de la region de instalarla.
    """De las unidades existentes cuales estan disponibles para instalar"""
    model.p_Availability = Param(model.REGION, model.TECHNOLOGY,model.YEAR, default=1)
    """Unidades que estan operando"""
    model.p_NumberOfExistingUnits  = Param(model.REGION, model.TECHNOLOGY, model.YEAR, default = 0)
    """Costo de re-invertir en una tecnologia"""
    model.p_CostoRecuperacion = Param(model.REGION, model.TECHNOLOGY, model.YEAR, default = 0.0001)
    """Vida Util despues de recuperadas"""
    model.p_VidaUtilRecuperada = Param(model.REGION, model.TECHNOLOGY, default = 1)
    '''Período de mantenimiento en años'''
    model.p_Mantenimiento = Param(model.REGION, model.TECHNOLOGY,model.TIMESLICE, model.YEAR)










    # data.load(filename='Data.json')

    from .constraints.ObjectiveFunction import ObjectiveFunction
    model.objectivefunction = Objective(rule = ObjectiveFunction)
    #%%
    def SpecifiedDemand_EQ (model, r, l, f, y ):
        return (model.v_RateOfDemand[r,l,f,y] ==
        model.p_SpecifiedAnnualDemand[r,f,y]*model.p_SpecifiedDemandProfile[r,f,l,y]/model.p_YearSplit[l,y])
    model.SpecifiedDemand_EQ = Constraint(model.REGION,model.TIMESLICE,model.FUEL,model.YEAR, rule = SpecifiedDemand_EQ)
    #%%
    from .constraints.CapacityAdequacyAB import CAa1_TotalNewCapacity,CAa1n_TotalResidualCapacity,CAa2_TotalAnnualCapacity, \
        CAa3_TotalActivityOfEachTechnology, CAa4_ConstraintCapacity, CAa5_TotalNewCapacity, CAb1_PlannedMaintenance
    model.CAa1_TotalNewCapacity = Constraint(
        model.REGION,
        model.TECHNOLOGY,
        model.YEAR,
        rule = CAa1_TotalNewCapacity
        )
    model.CAa1n_TotalResidualCapacity = Constraint(
        model.REGION,
        model.TECHNOLOGY,
        model.YEAR,
        rule = CAa1n_TotalResidualCapacity
    )


    model.CAa2_TotalAnnualCapacity = Constraint(
        model.REGION,
        model.TECHNOLOGY,
        model.YEAR,
        rule = CAa2_TotalAnnualCapacity
        )
    model.CAa3_TotalActivityOfEachTechnology = Constraint(
        model.REGION,
        model.TECHNOLOGY,
        model.TIMESLICE,
        model.YEAR,
        rule = CAa3_TotalActivityOfEachTechnology
        )
    model.CAa4_ConstraintCapacity = Constraint(
        model.REGION,
        model.TECHNOLOGY,
        model.TIMESLICE,
        model.YEAR,
        rule = CAa4_ConstraintCapacity
        )
    # # # # # model.CAa4b_ConstraintCapacity = Constraint(
    # # # # #     model.REGION,
    # # # # #     model.TECHNOLOGY,
    # # # # #     model.TIMESLICE,
    # # # # #     model.YEAR,
    # # # # #     rule = CAa4b_ConstraintCapacity
    # # # # #     )
    model.CAa5_TotalNewCapacity = Constraint(
        model.REGION,
        model.TECHNOLOGY,
        model.YEAR,
        rule  = CAa5_TotalNewCapacity
        )
    # # # model.CAa6_MinimumOperatingLoad = Constraint(
    # # #     model.REGION,
    # # #     model.TECHNOLOGY,
    # # #     model.SEASON,
    # # #     model.TIMESLICE,
    # # #     model.YEAR,
    # # #     rule = CAa6_MinimumOperatingLoad
    # # #     )
    # # # model.CAa7_ConnectedUnits = Constraint(
    # # #     model.REGION,
    # # #     model.TECHNOLOGY,
    # # #     model.SEASON,
    # # #     model.TIMESLICE,
    # # #     model.YEAR,
    # # #     rule = CAa7_ConnectedUnits
    # # #     )
    # model.CAa8_NumberOfConnectedUnits = Constraint(
    #     model.REGION,
    #     model.TECHNOLOGY,
    #     model.TIMESLICE,
    #     model.YEAR,
    #     rule = CAa8_NumberOfConnectedUnits
    # )
    """ Mantenimiento """
    model.CAb1_PlannedMaintenance = Constraint(
        model.REGION,
        model.TECHNOLOGY,
        model.YEAR,
        rule = CAb1_PlannedMaintenance
        )
    # model.CAb1_PlannedMaintenance.Skip()
    """ Recuperadas """
    # model.CAa1R_RecuperadasAcumuladas = Constraint(
    #     model.REGION,
    #     model.TECHNOLOGY,
    #     model.YEAR,
    #     rule = CAa1R_RecuperadasAcumuladas
    # )
    # model.CAa1R_RecuperadasAcumuladas.Skip()
    # model.CAa1R_Recuperadas = Constraint(
    #     model.REGION,
    #     model.TECHNOLOGY,
    #     model.YEAR,
    #     rule = CAa1R_Recuperadas
    # )


    #%%
    from .constraints.EnergyBalance import EBa1_RateOfFuelProduction1,EBa2_RateOfFuelProduction2, EBa3_RateOfFuelProduction3, \
        EBa4_RateOfFuelUse1, EBa5_RateOfFuelUse2, EBa6_RateOfFuelUse3, EBa7_EnergyBalanceEachTS1, EBa8_EnergyBalanceEachTS2, \
        EBa9_EnergyBalanceEachTS3, EBa10_EnergyBalanceEachTS4, EBa11_EnergyBalanceEachTS5, EBb1_EnergyBalanceEachYear1, \
        EBb2_EnergyBalanceEachYear2, EBb3_EnergyBalanceEachYear3, EBb4_EnergyBalanceEachYear4
    model.EBa1_RateOfFuelProduction1 = Constraint(
        model.REGION,
        model.TIMESLICE,
        model.FUEL,
        model.TECHNOLOGY,
        model.MODE_OF_OPERATION,
        model.YEAR,
        rule = EBa1_RateOfFuelProduction1
        )
    model.EBa2_RateOfFuelProduction2 = Constraint(
        model.REGION,
        model.TIMESLICE,
        model.FUEL,
        model.TECHNOLOGY,
        model.YEAR,
        rule = EBa2_RateOfFuelProduction2
        )
    model.EBa3_RateOfFuelProduction3 = Constraint(
        model.REGION,
        model.TIMESLICE,
        model.FUEL,
        model.YEAR,
        rule = EBa3_RateOfFuelProduction3
        )
    model.EBa4_RateOfFuelUse1 = Constraint(
        model.REGION,
        model.TIMESLICE,
        model.FUEL,
        model.TECHNOLOGY,
        model.MODE_OF_OPERATION,
        model.YEAR,
        rule = EBa4_RateOfFuelUse1
        )
    model.EBa5_RateOfFuelUse2  = Constraint(
        model.REGION,
        model.TIMESLICE,
        model.FUEL,
        model.TECHNOLOGY,
        model.YEAR,
        rule = EBa5_RateOfFuelUse2
        )
    model.EBa6_RateOfFuelUse3 = Constraint(
        model.REGION,
        model.TIMESLICE,
        model.FUEL,
        model.YEAR,
        rule= EBa6_RateOfFuelUse3
        )
    model.EBa7_EnergyBalanceEachTS1 = Constraint(
        model.REGION,
        model.TIMESLICE,
        model.FUEL,
        model.YEAR,
        rule = EBa7_EnergyBalanceEachTS1
        )
    model.EBa8_EnergyBalanceEachTS2 = Constraint(
        model.REGION,
        model.TIMESLICE,
        model.FUEL,
        model.YEAR,
        rule = EBa8_EnergyBalanceEachTS2    )
    model.EBa9_EnergyBalanceEachTS3 = Constraint(
        model.REGION,
        model.TIMESLICE,
        model.FUEL,
        model.YEAR,
        rule = EBa9_EnergyBalanceEachTS3    )
    model.EBa10_EnergyBalanceEachTS4 = Constraint(
        model.REGION,
        model.REGION,
        model.TIMESLICE,
        model.FUEL,
        model.YEAR,
        rule = EBa10_EnergyBalanceEachTS4    )
    model.EBa11_EnergyBalanceEachTS5 = Constraint(
        model.REGION,
        model.TIMESLICE,
        model.FUEL,
        model.YEAR,
        rule = EBa11_EnergyBalanceEachTS5)
    model.EBb1_EnergyBalanceEachYear1 = Constraint(
        model.REGION,
        model.FUEL,
        model.YEAR,
        rule = EBb1_EnergyBalanceEachYear1)
    model.EBb2_EnergyBalanceEachYear2 = Constraint(
        model.REGION,
        model.FUEL,
        model.YEAR,
        rule = EBb2_EnergyBalanceEachYear2)
    model.EBb3_EnergyBalanceEachYear3 = Constraint(
        model.REGION,
        model.REGION,
        model.FUEL,
        model.YEAR,
        rule = EBb3_EnergyBalanceEachYear3)
    model.EBb4_EnergyBalanceEachYear4 = Constraint(
        model.REGION,
        model.FUEL,
        model.YEAR,
        rule = EBb4_EnergyBalanceEachYear4)
    #%%
    from .constraints.AccountingTechnologyProductionUse import Acc1_FuelProductionByTechnology, Acc2_FuelUseByTechnology, \
        Acc3_AverageAnnualRateOfActivity, Acc4_ModelPeriodCostByRegion
    model.Acc1_FuelProductionByTechnology = Constraint(
        model.REGION,
        model.TIMESLICE,
        model.TECHNOLOGY,
        model.FUEL,
        model.YEAR,
        rule = Acc1_FuelProductionByTechnology)
    model.Acc2_FuelUseByTechnology = Constraint(
        model.REGION,
        model.TIMESLICE,
        model.TECHNOLOGY,
        model.FUEL,
        model.YEAR,
        rule = Acc2_FuelUseByTechnology)
    model.Acc3_AverageAnnualRateOfActivity = Constraint(
        model.REGION,
        model.TECHNOLOGY,
        model.MODE_OF_OPERATION,
        model.YEAR,
        rule = Acc3_AverageAnnualRateOfActivity)
    model.Acc4_ModelPeriodCostByRegion= Constraint(
        model.REGION,
        rule = Acc4_ModelPeriodCostByRegion)
    #%%
    from .constraints.StorageEq import S1_RateOfStorageCharge, S2_RateOfStorageDischarge, S3_NetChargeWithinYear, \
        S4_NetChargeWithinDay, S5_and_S6_StorageLevelYearStart, S7_and_S8_StorageLevelYearFinish, S9_and_S10_StorageLevelSeasonStart, \
        S11_and_S12_StorageLevelDayTypeStart, S13_and_S14_and_S15_StorageLevelDayTypeFinish
    model.S1_RateOfStorageCharge = Constraint(
            model.REGION,
            model.STORAGE,
            model.SEASON,
            model.DAYTYPE,
            model.DAILYTIMEBRACKET,
            model.YEAR,
            rule= S1_RateOfStorageCharge
            )
    model.S2_RateOfStorageDischarge = Constraint(
            model.REGION,
            model.STORAGE,
            model.SEASON,
            model.DAYTYPE,
            model.DAILYTIMEBRACKET,
            model.YEAR,
            rule= S2_RateOfStorageDischarge
            )
    model.S3_NetChargeWithinYear = Constraint(
            model.REGION,
            model.STORAGE,
            model.SEASON,
            model.DAYTYPE,
            model.DAILYTIMEBRACKET,
            model.YEAR,
            rule= S3_NetChargeWithinYear
            )
    model.S4_NetChargeWithinDay = Constraint(
            model.REGION,
            model.STORAGE,
            model.SEASON,
            model.DAYTYPE,
            model.DAILYTIMEBRACKET,
            model.YEAR,
            rule= S4_NetChargeWithinDay
            )
    model.S5_and_S6_StorageLevelYearStart =  Constraint(
            model.REGION,
            model.STORAGE,
            model.YEAR,
            rule= S5_and_S6_StorageLevelYearStart
            )
    model.S7_and_S8_StorageLevelYearFinish =  Constraint(
            model.REGION,
            model.STORAGE,
            model.YEAR,
            rule= S7_and_S8_StorageLevelYearFinish
            )
    model.S9_and_S10_StorageLevelSeasonStart = Constraint(
            model.REGION,
            model.STORAGE,
            model.SEASON,
            model.YEAR,
            rule= S9_and_S10_StorageLevelSeasonStart
            )
    model.S11_and_S12_StorageLevelDayTypeStart = Constraint(
            model.REGION,
            model.STORAGE,
            model.SEASON,
            model.DAYTYPE,
            model.YEAR,
            rule= S11_and_S12_StorageLevelDayTypeStart
            )
    model.S13_and_S14_and_S15_StorageLevelDayTypeFinish = Constraint(
            model.REGION,
            model.STORAGE,
            model.SEASON,
            model.DAYTYPE,
            model.YEAR,
            rule= S13_and_S14_and_S15_StorageLevelDayTypeFinish
            )
    #%%
    from .constraints.StorageConst import (
        SC1_LowerLimit_BeginningOfDailyTimeBracketOfFirstInstanceOfDayTypeInFirstWeekConstraint,
        SC1_UpperLimit_BeginningOfDailyTimeBracketOfFirstInstanceOfDayTypeInFirstWeekConstraint,
        SC2_LowerLimit_EndOfDailyTimeBracketOfLastInstanceOfDayTypeInFirstWeekConstraint,
        SC2_UpperLimit_EndOfDailyTimeBracketOfLastInstanceOfDayTypeInFirstWeekConstraint,
        SC3_LowerLimit_EndOfDailyTimeBracketOfLastInstanceOfDayTypeInLastWeekConstraint,
        SC3_UpperLimit_EndOfDailyTimeBracketOfLastInstanceOfDayTypeInLastWeekConstraint,
        SC4_LowerLimit_BeginningOfDailyTimeBracketOfFirstInstanceOfDayTypeInLastWeekConstraint,
        SC4_UpperLimit_BeginningOfDailyTimeBracketOfFirstInstanceOfDayTypeInLastWeekConstraint,
        SC5_MaxChargeConstraint,
        SC6_MaxDischargeConstraint
    )
    model.SC1_LowerLimit_BeginningOfDailyTimeBracketOfFirstInstanceOfDayTypeInFirstWeekConstraint = Constraint(
        model.REGION,
        model.STORAGE,
        model.SEASON,
        model.DAYTYPE,
        model.DAILYTIMEBRACKET,
        model.YEAR,
        rule = SC1_LowerLimit_BeginningOfDailyTimeBracketOfFirstInstanceOfDayTypeInFirstWeekConstraint
    )
    model.SC1_UpperLimit_BeginningOfDailyTimeBracketOfFirstInstanceOfDayTypeInFirstWeekConstraint = Constraint(
        model.REGION,
        model.STORAGE,
        model.SEASON,
        model.DAYTYPE,
        model.DAILYTIMEBRACKET,
        model.YEAR,
        rule = SC1_UpperLimit_BeginningOfDailyTimeBracketOfFirstInstanceOfDayTypeInFirstWeekConstraint
    )
    model.SC2_LowerLimit_EndOfDailyTimeBracketOfLastInstanceOfDayTypeInFirstWeekConstraint = Constraint(
        model.REGION,
        model.STORAGE,
        model.SEASON,
        model.DAYTYPE,
        model.DAILYTIMEBRACKET,
        model.YEAR,
        rule = SC2_LowerLimit_EndOfDailyTimeBracketOfLastInstanceOfDayTypeInFirstWeekConstraint
    )
    model.SC2_UpperLimit_EndOfDailyTimeBracketOfLastInstanceOfDayTypeInFirstWeekConstraint = Constraint(
        model.REGION,
        model.STORAGE,
        model.SEASON,
        model.DAYTYPE,
        model.DAILYTIMEBRACKET,
        model.YEAR,
        rule = SC2_UpperLimit_EndOfDailyTimeBracketOfLastInstanceOfDayTypeInFirstWeekConstraint
    )
    model.SC3_LowerLimit_EndOfDailyTimeBracketOfLastInstanceOfDayTypeInLastWeekConstraint = Constraint(
        model.REGION,
        model.STORAGE,
        model.SEASON,
        model.DAYTYPE,
        model.DAILYTIMEBRACKET,
        model.YEAR,
        rule = SC3_LowerLimit_EndOfDailyTimeBracketOfLastInstanceOfDayTypeInLastWeekConstraint
    )
    model.SC3_UpperLimit_EndOfDailyTimeBracketOfLastInstanceOfDayTypeInLastWeekConstraint = Constraint(
        model.REGION,
        model.STORAGE,
        model.SEASON,
        model.DAYTYPE,
        model.DAILYTIMEBRACKET,
        model.YEAR,
        rule = SC3_UpperLimit_EndOfDailyTimeBracketOfLastInstanceOfDayTypeInLastWeekConstraint
    )
    model.SC4_LowerLimit_BeginningOfDailyTimeBracketOfFirstInstanceOfDayTypeInLastWeekConstraint = Constraint(
        model.REGION,
        model.STORAGE,
        model.SEASON,
        model.DAYTYPE,
        model.DAILYTIMEBRACKET,
        model.YEAR,
        rule = SC4_LowerLimit_BeginningOfDailyTimeBracketOfFirstInstanceOfDayTypeInLastWeekConstraint
    )
    model.SC4_UpperLimit_BeginningOfDailyTimeBracketOfFirstInstanceOfDayTypeInLastWeekConstraint = Constraint(
        model.REGION,
        model.STORAGE,
        model.SEASON,
        model.DAYTYPE,
        model.DAILYTIMEBRACKET,
        model.YEAR,
        rule = SC4_UpperLimit_BeginningOfDailyTimeBracketOfFirstInstanceOfDayTypeInLastWeekConstraint
    )
    model.SC5_MaxChargeConstraint = Constraint(
        model.REGION,
        model.STORAGE,
        model.SEASON,
        model.DAYTYPE,
        model.DAILYTIMEBRACKET,
        model.YEAR,
        rule = SC5_MaxChargeConstraint
    )
    model.SC6_MaxDischargeConstraint = Constraint(
        model.REGION,
        model.STORAGE,
        model.SEASON,
        model.DAYTYPE,
        model.DAILYTIMEBRACKET,
        model.YEAR,
        rule = SC6_MaxDischargeConstraint
    )
    #%%
    from .constraints.StorageInv import (
        SI1_StorageUpperLimit,
        SI2_StorageLowerLimit,
        SI3_TotalNewStorage,
        SI4_UndiscountedCapitalInvestmentStorage,
        SI5_DiscountingCapitalInvestmentStorage,
        SI6_SalvageValueStorageAtEndOfPeriod1,
        SI7_SalvageValueStorageAtEndOfPeriod2,
        SI8_SalvageValueStorageAtEndOfPeriod3,
        SI9_SalvageValueStorageDiscountedToStartYear,
        SI10_TotalDiscountedCostByStorage
    )
    model.SI1_StorageUpperLimit = Constraint(
        model.REGION,
        model.STORAGE,
        model.YEAR,
        rule = SI1_StorageUpperLimit
    )

    model.SI2_StorageLowerLimit = Constraint(
        model.REGION,
        model.STORAGE,
        model.YEAR,
        rule = SI2_StorageLowerLimit
    )
    model.SI3_TotalNewStorage = Constraint(
        model.REGION,
        model.STORAGE,
        model.YEAR,
        rule = SI3_TotalNewStorage
    )
    model.SI4_UndiscountedCapitalInvestmentStorage = Constraint(
        model.REGION,
        model.STORAGE,
        model.YEAR,
        rule = SI4_UndiscountedCapitalInvestmentStorage
    )
    model.SI5_DiscountingCapitalInvestmentStorage = Constraint(
        model.REGION,
        model.STORAGE,
        model.YEAR,
        rule = SI5_DiscountingCapitalInvestmentStorage
    )
    model.SI6_SalvageValueStorageAtEndOfPeriod1 = Constraint(
        model.REGION,
        model.STORAGE,
        model.YEAR,
        rule = SI6_SalvageValueStorageAtEndOfPeriod1
    )
    model.SI7_SalvageValueStorageAtEndOfPeriod2 = Constraint(
        model.REGION,
        model.STORAGE,
        model.YEAR,
        rule = SI7_SalvageValueStorageAtEndOfPeriod2
    )
    model.SI8_SalvageValueStorageAtEndOfPeriod3 = Constraint(
        model.REGION,
        model.STORAGE,
        model.YEAR,
        rule = SI8_SalvageValueStorageAtEndOfPeriod3
    )
    model.SI9_SalvageValueStorageDiscountedToStartYear = Constraint(
        model.REGION,
        model.STORAGE,
        model.YEAR,
        rule = SI9_SalvageValueStorageDiscountedToStartYear
    )
    model.SI10_TotalDiscountedCostByStorage = Constraint(
        model.REGION,
        model.STORAGE,
        model.YEAR,
        rule = SI10_TotalDiscountedCostByStorage
    )



    #%%
    from .constraints.CapitalCost import (
        CC1_UndiscountedCapitalInvestment,
        CC2_DiscountingCapitalInvestment
    )
    model.CC1_UndiscountedCapitalInvestment = Constraint(
        model.REGION,
        model.TECHNOLOGY,
        model.YEAR,
        rule = CC1_UndiscountedCapitalInvestment)
    model.CC2_DiscountingCapitalInvestment = Constraint(
        model.REGION,
        model.TECHNOLOGY,
        model.YEAR,
        rule = CC2_DiscountingCapitalInvestment)
    #%%
    from .constraints.SalvageValue import (
        SV123_SalvageValueAtEndOfPeriod1,
        SV4_SalvageValueDiscountedToStarYear
    )
    model.SV123_SalvageValueAtEndOfPeriod1 = Constraint(
        model.REGION,
        model.TECHNOLOGY,
        model.YEAR,
        rule = SV123_SalvageValueAtEndOfPeriod1)
    model.SV4_SalvageValueDiscountedToStarYear = Constraint(
        model.REGION,
        model.TECHNOLOGY,
        model.YEAR,
        rule = SV4_SalvageValueDiscountedToStarYear)
    #%%
    from .constraints.OperatingCosts import (
        OC1_OperatingCostVariable,
        OC2_OperatingCostsFixedAnnual,
        OC3_OperatingCostsTotalAnnual,
        OC4_DiscountedOperatingCostsTotalAnnual
    )
    model.OC1_OperatingCostVariable = Constraint(
        model.REGION,
        model.TECHNOLOGY,
        model.YEAR,
        rule = OC1_OperatingCostVariable)
    model.OC2_OperatingCostsFixedAnnual = Constraint(
        model.REGION,
        model.TECHNOLOGY,
        model.YEAR,
        rule = OC2_OperatingCostsFixedAnnual)
    model.OC3_OperatingCostsTotalAnnual = Constraint(
        model.REGION,
        model.TECHNOLOGY,
        model.YEAR,
        rule = OC3_OperatingCostsTotalAnnual)
    model.OC4_DiscountedOperatingCostsTotalAnnual = Constraint(
        model.REGION,
        model.TECHNOLOGY,
        model.YEAR,
        rule = OC4_DiscountedOperatingCostsTotalAnnual)
    #%%
    from .constraints.TotalDiscountedCosts import (
        TDC1_TotalDiscountedCostByTechnology,
        TDC2_TotalDiscountedCost
    )
    model.TDC1_TotalDiscountedCostByTechnology = Constraint(
        model.REGION,
        model.TECHNOLOGY,
        model.YEAR,
        rule = TDC1_TotalDiscountedCostByTechnology)
    model.TDC2_TotalDiscountedCost = Constraint(
        model.REGION,
        model.YEAR,
        rule = TDC2_TotalDiscountedCost)
    #%%
    from .constraints.MinMaxCapacity import (
        TCC1_TotalAnnualMaxCapacityConstraint,
        TCC2_TotalAnnualMinCapacityConstraint,
        NCC1_TotalAnnualMaxNewCapacityConstraint,
        NCC2_TotalAnnualMinNewCapacityConstraint
    )
    model.TCC1_TotalAnnualMaxCapacityConstraint = Constraint(
        model.REGION,
        model.TECHNOLOGY,
        model.YEAR,
        rule = TCC1_TotalAnnualMaxCapacityConstraint)
    model.TCC2_TotalAnnualMinCapacityConstraint = Constraint(
        model.REGION,
        model.TECHNOLOGY,
        model.YEAR,
        rule = TCC2_TotalAnnualMinCapacityConstraint)
    model.NCC1_TotalAnnualMaxNewCapacityConstraint = Constraint(
        model.REGION,
        model.TECHNOLOGY,
        model.YEAR,
        rule = NCC1_TotalAnnualMaxNewCapacityConstraint)
    model.NCC2_TotalAnnualMinNewCapacityConstraint = Constraint(
        model.REGION,
        model.TECHNOLOGY,
        model.YEAR,
        rule = NCC2_TotalAnnualMinNewCapacityConstraint)
    #%%
    from .constraints.ActivityConstrains import (
        AAC1_TotalAnnualTechnologyActivity,
        AAC2_TotalAnnualTechnologyActivityUpperLimit,
        AAC3_TotalAnnualTechnologyActivityLowerLimit,
        TAC1_TotalModelHorizonTechnologyActivity,
        TAC2_TotalModelHorizonTechnologyActivityUpperLimit,
        TAC3_TotalModelHorizenTechnologyActivityLowerLimit
    )
    model.AAC1_TotalAnnualTechnologyActivity = Constraint(
        model.REGION,
        model.TECHNOLOGY,
        model.YEAR,
        rule= AAC1_TotalAnnualTechnologyActivity)
    model.AAC2_TotalAnnualTechnologyActivityUpperLimit = Constraint(
        model.REGION,
        model.TECHNOLOGY,
        model.YEAR,
        rule = AAC2_TotalAnnualTechnologyActivityUpperLimit)
    model.AAC3_TotalAnnualTechnologyActivityLowerLimit = Constraint(
        model.REGION,
        model.TECHNOLOGY,
        model.YEAR,
        rule = AAC3_TotalAnnualTechnologyActivityLowerLimit)
    model.TAC1_TotalModelHorizonTechnologyActivity = Constraint(
        model.REGION,
        model.TECHNOLOGY,
        rule = TAC1_TotalModelHorizonTechnologyActivity)
    model.TAC2_TotalModelHorizonTechnologyActivityUpperLimit =Constraint(
        model.REGION,
        model.TECHNOLOGY,
        rule = TAC2_TotalModelHorizonTechnologyActivityUpperLimit)
    model.TAC3_TotalModelHorizenTechnologyActivityLowerLimit = Constraint(
        model.REGION,
        model.TECHNOLOGY,
        rule = TAC3_TotalModelHorizenTechnologyActivityLowerLimit)
    #%%
    from .constraints.ReserveMargin import (
        RM1_ReserveMargin_TechnologiesIncluded_In_Activity_Units,
        RM2_ReserveMargin_FuelsIncluded,
        RM3_ReserveMargin_Constraint
    )
    model.RM1_ReserveMargin_TechnologiesIncluded_In_Activity_Units = Constraint(
        model.REGION,
        # model.TIMESLICE,
        model.YEAR,
        rule = RM1_ReserveMargin_TechnologiesIncluded_In_Activity_Units
        )
    model.RM2_ReserveMargin_FuelsIncluded = Constraint(
        model.REGION,
        model.TIMESLICE,
        model.YEAR,
        rule = RM2_ReserveMargin_FuelsIncluded)
    model.RM3_ReserveMargin_Constraint = Constraint(
        model.REGION,
        model.TIMESLICE,
        model.YEAR,
        rule = RM3_ReserveMargin_Constraint)
    #%%
    from .constraints.ReTagTech import (
        RE1_FuelProductionByTechnologyAnnual,
        RE2_TechIncluded,
        RE3_FuelIncluded,
        RE4_EnergyConstraint,
        RE5_FuelUseByTechnologyAnnual
    )
    model.RE1_FuelProductionByTechnologyAnnual = Constraint(
        model.REGION,
        model.TECHNOLOGY,
        model.FUEL,
        model.YEAR,
        rule = RE1_FuelProductionByTechnologyAnnual
        )
    model.RE2_TechIncluded = Constraint(
        model.REGION,
        model.YEAR,
        rule = RE2_TechIncluded
        )
    model.RE3_FuelIncluded =Constraint(
        model.REGION,
        model.YEAR,
        rule = RE3_FuelIncluded
        )
    model.RE4_EnergyConstraint = Constraint(
        model.REGION,
        model.YEAR,
        rule = RE4_EnergyConstraint
        )
    model.RE5_FuelUseByTechnologyAnnual = Constraint(
        model.REGION,
        model.TECHNOLOGY,
        model.FUEL,
        model.YEAR,
        rule = RE5_FuelUseByTechnologyAnnual
        )

    #%%
    from .constraints.Emission import (
        E1_AnnualEmissionProductionByMode,
        E2_AnnualEmissionProduction,
        E3_EmissionsPenaltyByTechAndEmission,
        E4_EmissionsPenaltyByTechnology,
        E5_DiscountedEmissionsPenaltyByTechnology,
        E6_EmissionsAccounting1,
        E7_EmissionsAccounting2,
        E8_AnnualEmissionsLimit,
        E9_ModelPeriodEmissionsLimit
    )
    model.E1_AnnualEmissionProductionByMode = Constraint(
        model.REGION,
        model.TECHNOLOGY,
        model.EMISSION,
        model.MODE_OF_OPERATION,
        model.YEAR,
        rule = E1_AnnualEmissionProductionByMode
    )
    model.E2_AnnualEmissionProduction = Constraint(
        model.REGION,
        model.TECHNOLOGY,
        model.EMISSION,
        model.YEAR,
        rule = E2_AnnualEmissionProduction
    )
    model.E3_EmissionsPenaltyByTechAndEmission = Constraint(
        model.REGION,
        model.TECHNOLOGY,
        model.EMISSION,
        model.YEAR,
        rule = E3_EmissionsPenaltyByTechAndEmission
    )
    model.E4_EmissionsPenaltyByTechnology= Constraint(
        model.REGION,
        model.TECHNOLOGY,
        model.YEAR,
        rule = E4_EmissionsPenaltyByTechnology
    )
    model.E5_DiscountedEmissionsPenaltyByTechnology= Constraint(
        model.REGION,
        model.TECHNOLOGY,
        model.YEAR,
        rule = E5_DiscountedEmissionsPenaltyByTechnology
    )
    model.E6_EmissionsAccounting1= Constraint(
        model.REGION,
        model.EMISSION,
        model.YEAR,
        rule = E6_EmissionsAccounting1
    )
    model.E7_EmissionsAccounting2= Constraint(
        model.REGION,
        model.EMISSION,
        rule = E7_EmissionsAccounting2
    )
    model.E8_AnnualEmissionsLimit= Constraint(
        model.REGION,
        model.EMISSION,
        model.YEAR,
        rule = E8_AnnualEmissionsLimit
    )
    model.E9_ModelPeriodEmissionsLimit= Constraint(
        model.REGION,
        model.EMISSION,
        rule = E9_ModelPeriodEmissionsLimit
    )
    return model

if __name__ =='__main__':
    results_folder = '../results'
    input_file = '../data/OsemosysNew.xlsx'
    m=define_model(input_file)



# %%
