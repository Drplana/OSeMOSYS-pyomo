"""Capital Costs
Calculates the total discounted capital cost 
expenditure for each technology in each year."""


def CC1_UndiscountedCapitalInvestment(model, r,t,y):
    return (
        model.v_NewCapacity[r,t,y]*model.p_CapitalCost[r,t,y] 
        == model.v_CapitalInvestment[r,t,y]
    )
def CC2_DiscountingCapitalInvestment(model, r,t,y):
    return (
        model.v_CapitalInvestment[r,t,y]
        /((1 + model.p_DiscountRate[r])**(y-min(model.YEAR)))
        == model.v_DiscountedCapitalInvestment[r,t,y]
    )
    

