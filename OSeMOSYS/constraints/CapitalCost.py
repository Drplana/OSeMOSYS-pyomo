"""Capital Costs
Calculates the total discounted capital cost 
expenditure for each technology in each year."""


def CC1_UndiscountedCapitalInvestment(model, r,t,y):
    """
s.t. CC1_UndiscountedCapitalInvestment{r in REGION, t in TECHNOLOGY, y in YEAR}: 
CapitalCost[r,t,y] * NewCapacity[r,t,y] = CapitalInvestment[r,t,y];
    """    
    return (
        model.v_NewCapacity[r,t,y]*model.p_CapitalCost[r,t,y] 
        + model.v_RecoveredExistingUnits[r,t,y]*model.p_CostoRecuperacion[r,t,y]*model.p_CapacityOfOneTechnologyUnit[r,t,min(model.YEAR)]
        + model.v_RecoveredCapacity[r,t,y]*model.p_CostoRecuperacion[r,t,y]
        == model.v_CapitalInvestment[r,t,y]
    )
def CC2_DiscountingCapitalInvestment(model, r,t,y):
    """
s.t. CC2_DiscountingCapitalInvestment{r in REGION, t in TECHNOLOGY, y in YEAR}: 
CapitalInvestment[r,t,y]/((1+DiscountRate[r])^(y-min{yy in YEAR} min(yy))) = 
DiscountedCapitalInvestment[r,t,y];
    """    
    return (
        model.v_CapitalInvestment[r,t,y]
        /((1 + model.p_DiscountRate[r])**(y-min(model.YEAR)))
        == model.v_DiscountedCapitalInvestment[r,t,y]
    )
    

