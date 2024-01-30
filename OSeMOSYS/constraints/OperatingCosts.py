"""Operating Cost"""

def OC1_OperatingCostVariable(model,r, t, y):
    """
s.t. OC1_OperatingCostsVariable{r in REGION, t in TECHNOLOGY, l in TIMESLICE, y in YEAR}: 
sum{m in MODE_OF_OPERATION} TotalAnnualTechnologyActivityByMode[r,t,m,y] * VariableCost[r,t,m,y] 
= AnnualVariableOperatingCost[r,t,y];

    """    
    return (
            sum(model.v_TotalAnnualTechnologyActivityByMode[r,t,m,y]
            *model.p_VariableCost[r,t,m,y] for m in model.MODE_OF_OPERATION)
            == model.v_AnnualVariableOperatingCost[r,t,y]
        )
def OC2_OperatingCostsFixedAnnual(model,r,t,y):
    """
s.t. OC2_OperatingCostsFixedAnnual{r in REGION, t in TECHNOLOGY, y in YEAR}: 
TotalCapacityAnnual[r,t,y]*FixedCost[r,t,y] = AnnualFixedOperatingCost[r,t,y];
    """    
    return (
        model.v_TotalCapacityAnnual[r,t,y]
        *model.p_FixedCost[r,t,y]
        ==model.v_AnnualFixedOperatingCost[r,t,y]
    )
def OC3_OperatingCostsTotalAnnual(model,r,t,y):
    """
s.t. OC3_OperatingCostsTotalAnnual{r in REGION, t in TECHNOLOGY, y in YEAR}: 
AnnualFixedOperatingCost[r,t,y]+AnnualVariableOperatingCost[r,t,y] = OperatingCost[r,t,y];
    """
    return (
         model.v_AnnualFixedOperatingCost[r,t,y]
        +model.v_AnnualVariableOperatingCost[r,t,y]
        ==model.v_OperatingCost[r,t,y]
    )
def OC4_DiscountedOperatingCostsTotalAnnual(model,r,t,y):
    """
s.t. OC4_DiscountedOperatingCostsTotalAnnual{r in REGION, t in TECHNOLOGY, y in YEAR}: 
OperatingCost[r,t,y]/((1+DiscountRate[r])^(y-min{yy in YEAR} min(yy)+0.5)) = DiscountedOperatingCost[r,t,y];
    """    
    return(
        model.v_OperatingCost[r,t,y]
        /((1+model.p_DiscountRate[r])**(y-min(model.YEAR)+0.5))
        == model.v_DiscountedOperatingCost[r,t,y]
    )



    
    