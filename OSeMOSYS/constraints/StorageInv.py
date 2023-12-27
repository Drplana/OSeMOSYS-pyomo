"""Storage Investment"""
def SI1_StorageUpperLimit(model, r,s,y):
    return (
        model.v_AccumulatedNewStorageCapacity[r,s,y]
        +model.p_ResidualStorageCapacity[r,s,y]
        == model.v_StorageUpperLimit[r,s,y]
    )
def SI2_StorageLowerLimit(model, r,s,y):
    return (
        model.p_MinStorageCharge[r,s,y]
        *model.v_StorageUpperLimit[r,s,y]
        == model.v_StorageLowerLimit[r,s,y]
    )
def SI3_TotalNewStorage(model, r,s,y):
    return(
        sum(model.NewStorageCapacity[r,s,yy]
            for yy in model.YEAR
            if (y-yy<model.p_OperationalLifeStorage[r,s]) and y-yy>=0)
    == model.v_AccumulatedNewStorageCapacity[r,s,y]
    )
def SI4_UndiscountedCapitalInvestmentStorage(model,r,s,y):
    return (
        model.p_CapitalCostStorage[r,s,y]
        *model.v_NewStorageCapacity[r,s,y]
        == model.v_CapitalInvestmentStorage[r,s,y]
    )
def SI5_DiscountingCapitalInvestmentStorage(model,r,s,y):
    return(
        model.v_CapitalInvestmentStorage[r,s,y]
        /(1+model.p_DiscountRate[r])**(y-min(model.YEAR))
        ==model.v_DiscountedCapitalInvestmentStorage[r,s,y]    
    )
def SI6_SalvageValueStorageAtEndOfPeriod1(model,r,s,y):
    if (y + model.p_OperationalLifeStorage[r,s]-1)<= max(model.YEAR):
        return (      
                0 <= model.v_SalvageValueStorage[r,s,y]
        )
def SI7_SalvageValueStorageAtEndOfPeriod2(model, r,s,y):
    if (model.p_DepreciationMethod[r]==1 
        and (y+model.p_OperationalLifeStorage[r,s]-1)>max(model.YEAR)
        and model.DiscountRate[r]==0 
        or model.p_DepreciationMethod[r]==2 
        and (y+model.p_OperationalLifeStorage[r,s]-1)>max(model.YEAR) 
        ):
        return (
            model.v_CapitalInvestmentStorage[r,s,y]*(1-max(model.YEAR)-y+1)
            /model.p_OperationalLifeStorage[r,s]
            == model.v_SalvageValueStorage[r,s,y]
        )
def SI8_SalvageValueStorageAtEndOfPeriod3(model, r,s,y):
    if (model.p_DepreciationMethod[r]==1
    and (y+model.p_OperationalLifeStorage[r,s]-1)> max(model.YEAR)
    and model.p_DiscountRate[r]>0
    ):
        return (
            model.v_CapitalInvestmentStorage[r,s,y]*(1-(((1+model.p_DiscountRate[r])**max(model.YEAR - y+1)-1)/((1+model.p_DiscountRate[r])**model.p_OperationalLifeStorage[r,s]-1)))
            == model.v_SalvageValueStorage[r,s,y]
        )
def SI9_SalvageValueStorageDiscountedToStartYear(model, r,s,y):
    return (model.v_SalvageValueStorage[r,s,y]
            /(1+model.p_DiscountRate[r])**(max(model.YEAR)-min(model.YEAR)+1)
            ==model.v_DiscountedSalvageValueStorage[r,s,y]
            )
def SI10_TotalDiscountedCostByStorage(model,r,s,y):
    return (
        model.v_DiscountedCapitalInvestment[r,s,y]
        -model.v_DiscountedSalvageValueStorage[r,s,y]
        == model.v_TotalDiscountedStorageCost[r,s,y]
    )