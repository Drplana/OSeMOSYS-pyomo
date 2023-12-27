"""Operating Cost"""

""""Hay un error en la definición de esta ecuación 
en la documentación de osemosys """
def OC1_OperatingCostVariable(model,r,t,y):
    return (
            sum(model.v_TotalAnnualTechnologyActivityByMode[r,t,m,y]
            *model.p_VariableCost[r,t,m,y] for m in model.MODE_OF_OPERATION)
            == model.v_AnnualVariableOperatingCost[r,t,y]
        )
def OC2_OperatingCostsFixedAnnual(model,r,t,y):
    return (
        model.v_TotalCapacityAnnual[r,t,y]
        *model.p_FixedCost[r,t,y]
        ==model.v_AnnualFixedOperatingCost[r,t,y]
    )
def OC3_OperatingCostsTotalAnnual(model,r,t,y):
    return (
         model.v_AnnualFixedOperatingCost[r,t,y]
        +model.v_AnnualVariableOperatingCost[r,t,y]
        ==model.v_OperatingCost[r,t,y]
    )
def OC4_DiscountedOperatingCostsTotalAnnual(model,r,t,y):
    return(
        model.v_OperatingCost[r,t,y]
        /((1+model.p_DiscountRate[r])**(y-min(model.YEAR)+0.5))
        == model.v_DiscountedOperatingCost[r,t,y]
    )