""""Total Discounted Costs:
Calculates the total discounted system cost over 
the entire model period to give the TotalDiscountedCost. 
This is the variable that is minimized in the model’s 
objective function."""

def TDC1_TotalDiscountedCostByTechnology(model,r,t,y):
    return (
        model.v_DiscountedOperatingCost[r,t,y]
        +model.v_DiscountedCapitalInvestment[r,t,y]
        +model.v_DiscountedTechnologyEmissionsPenalty[r,t,y]
        -model.v_DiscountedSalvageValue[r,t,y]
        == model.v_TotalDiscountedCostByTechnology [r,t,y]
    )
def TDC2_TotalDiscountedCost(model,r,y):
    return (
                sum(model.v_TotalDiscountedCostByTechnology[r,t,y]
                for t in model.TECHNOLOGY)
                +sum(model.v_TotalDiscountedStorageCost [r,s,y] 
                for s in model.STORAGE)
                ==model.v_TotalDiscountedCost[r,y]
            )
