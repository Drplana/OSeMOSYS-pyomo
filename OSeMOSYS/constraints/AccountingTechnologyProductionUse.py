#########################################################
########  AccountingTechnologyProductionUse    ##########

def Acc1_FuelProductionByTechnology(model, r,l,t,f,y):
    """
s.t. Acc1_FuelProductionByTechnology{r in REGION, l in TIMESLICE, t in TECHNOLOGY, f in FUEL, y in YEAR}:
RateOfProductionByTechnology[r,l,t,f,y] * YearSplit[l,y] = ProductionByTechnology[r,l,t,f,y];
    """    
    return(
        model.v_RateOfProductionByTechnology[r,l,t,f,y]
        *model.p_YearSplit[l,y]
        == model.v_ProductionByTechnology[r,l,t,f,y]
    )
def Acc2_FuelUseByTechnology(model, r,l,t,f,y):
    """
s.t. Acc2_FuelUseByTechnology{r in REGION, l in TIMESLICE, t in TECHNOLOGY, f in FUEL, y in YEAR}:
RateOfUseByTechnology[r,l,t,f,y] * YearSplit[l,y] = UseByTechnology[r,l,t,f,y]; 
    """    
    return(
        model.v_RateOfUseByTechnology[r,l,t,f,y]
        *model.p_YearSplit[l,y]
        == model.v_UseByTechnology[r,l,t,f,y]
    )

def Acc3_AverageAnnualRateOfActivity(model, r,t,m,y):
    """
s.t. Acc3_AverageAnnualRateOfActivity{r in REGION, t in TECHNOLOGY, m in MODE_OF_OPERATION, y in YEAR}: 
sum{l in TIMESLICE} RateOfActivity[r,l,t,m,y]*YearSplit[l,y] = TotalAnnualTechnologyActivityByMode[r,t,m,y];
    """    
    return (
            sum(model.v_RateOfActivity[r,l,t,m,y]*model.p_YearSplit[l,y] 
                for l in model.TIMESLICE)
            == model.v_TotalAnnualTechnologyActivityByMode[r,t,m,y]
    )
    
def Acc4_ModelPeriodCostByRegion(model,r):
    """
s.t. Acc4_ModelPeriodCostByRegion{r in REGION}:
sum{y in YEAR}TotalDiscountedCost[r,y] = ModelPeriodCostByRegion[r];
    """    
    return (
            sum(model.v_TotalDiscountedCost[r,y] 
                for y in model.YEAR)
            ==model.v_ModelPeriodCostByRegion[r]
        )
    









