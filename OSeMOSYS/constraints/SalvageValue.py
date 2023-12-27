"""Salvage Value:
Calculates the fraction of the initial capital cost that can 
be recouped at the end of a technologies operational life. 
The salvage value can be calculated using one of two depreciation methods:
 straight line and sinking fund."""

def SV123_SalvageValueAtEndOfPeriod1(model, r,t,y):
    if (
        model.p_DepreciationMethod[r]==1 
        and ((y + model.p_OperationalLife[r,t]-1) > max(model.YEAR))
        and model.p_DiscountRate[r] > 0
    ): return(
        model.v_SalvageValue[r,t,y]
        == model.v_NewCapacity[r,t,y]
        *  model.p_CapitalCost[r,t,y]
        *(1- (
            ((1+model.p_DiscountRate[r])**(max(model.YEAR)-y+1)-1)
            /((1+model.p_DiscountRate[r])**model.p_OperationalLife[r,t]-1))
             )
        )
    
    elif (
        model.p_DepreciationMethod[r] == 1
        and ((y+ model.p_OperationalLife[r,t] - 1) > max(model.YEAR))
        and model.p_DiscountRate[r] == 0
        or (model.p_DepreciationMethod[r] == 2
        and (y+model.p_OperationalLife[r,t]-1) > max(model.YEAR))
    ): return(
        model.v_SalvageValue[r,t,y]
        == model.v_NewCapacity[r,t,y]
        *  model.p_CapitalCost[r,t,y]
        *  (1-(max(model.YEAR)-y+1)/model.p_OperationalLife[r,t])            
            )
    else: 
        return(
        #if (y + Operationallife[r,t]-1)<= max(Year)
        model.v_SalvageValue[r,t,y] == 0
            )   
def SV4_SalvageValueDiscountedToStarYear(model, r,t,y):
    return (
        model.v_DiscountedSalvageValue[r,t,y]
        == model.v_SalvageValue[r,t,y]
        / (1+model.p_DiscountRate[r])**(1+max(model.YEAR)-min(model.YEAR))
    )


