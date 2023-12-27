#########################################################
########  AccountingTechnologyProductionUse    ##########
def Acc1_FuelProductionByTechnology(model, r,l,t,f,y):
    return(
        model.v_RateOfProductionByTechnology[r,l,t,f,y]
        *model.p_YearSplit[l,y]
        == model.v_ProductionByTechnology[r,l,t,f,y]
    )
def Acc2_FuelUseByTechnology(model, r,l,t,f,y):
    return(
        model.v_RateOfUseByTechnology[r,l,t,f,y]
        *model.p_YearSplit[l,y]
        == model.v_UseByTechnology[r,l,t,f,y]
    )
def Acc3_AverageAnnualRateOfActivity(model, r,t,m,y):
    return (
            sum(model.v_RateOfActivity[r,l,t,m,y]*model.p_YearSplit[l,y] 
                for l in model.TIMESLICE)
            == model.v_TotalAnnualTechnologyActivityByMode[r,t,m,y]
    )
def Acc4_ModelPeriodCostByRegion(model,r):
    return (
            sum(model.v_TotalDiscountedCost[r,y] 
                for y in model.YEAR)
            ==model.v_ModelPeriodCostByRegion[r]
        )



