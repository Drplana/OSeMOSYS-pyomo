"""Salvage Value:
Calculates the fraction of the initial capital cost that can 
be recouped at the end of a technologies operational life. 
The salvage value can be calculated using one of two depreciation methods:
 straight line and sinking fund."""

def SV123_SalvageValueAtEndOfPeriod1(model, r,t,y):
    """
    s.t. SV1_SalvageValueAtEndOfPeriod1{r in REGION, t in TECHNOLOGY, y in YEAR: 
    DepreciationMethod[r]=1 && (y + OperationalLife[r,t]-1) > (max{yy in YEAR} max(yy)) && DiscountRate[r]>0}: 
        SalvageValue[r,t,y] =
        CapitalCost[r,t,y]*NewCapacity[r,t,y]*(1-(((1+DiscountRate[r])^(max{yy in YEAR} max(yy) - y+1)-1)/((1+DiscountRate[r])^OperationalLife[r,t]-1)));
    
    s.t. SV2_SalvageValueAtEndOfPeriod2{r in REGION, t in TECHNOLOGY, y in YEAR: 
        (DepreciationMethod[r]=1 && (y + OperationalLife[r,t]-1) > (max{yy in YEAR} max(yy)) && DiscountRate[r]=0) 
        || (DepreciationMethod[r]=2 && (y + OperationalLife[r,t]-1) > (max{yy in YEAR} max(yy)))}: 
            SalvageValue[r,t,y] = CapitalCost[r,t,y]*NewCapacity[r,t,y]*(1-(max{yy in YEAR} max(yy) - y+1)/OperationalLife[r,t]); 
    
    s.t. SV3_SalvageValueAtEndOfPeriod3{r in REGION, t in TECHNOLOGY, y in YEAR: 
        (y + OperationalLife[r,t]-1) <= (max{yy in YEAR} max(yy))}: SalvageValue[r,t,y] = 0;
    
    """
    if (model.p_DepreciationMethod[r]==1 and ((y + model.p_OperationalLife[r,t]-1) > max(model.YEAR)) and model.p_DiscountRate[r] > 0 ):
        return(
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
    """
s.t. SV4_SalvageValueDiscountedToStartYear{r in REGION, t in TECHNOLOGY, y in YEAR}: 
DiscountedSalvageValue[r,t,y] = SalvageValue[r,t,y]/((1+DiscountRate[r])^(1+max{yy in YEAR} max(yy)-min{yy in YEAR} min(yy)));
    """    
    return (
        model.v_DiscountedSalvageValue[r,t,y]
        == model.v_SalvageValue[r,t,y]
        / (1+model.p_DiscountRate[r])**(1+max(model.YEAR)-min(model.YEAR))
    )


