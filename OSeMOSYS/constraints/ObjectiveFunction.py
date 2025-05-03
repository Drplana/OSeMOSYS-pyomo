######### Objective Function #######
"""The default in OSeMOSYS is to minimise the 
total system cost, over the entire model period."""

def ObjectiveFunction(model):
    return (sum(model.v_TotalDiscountedCost[r, y] for r in model.REGION for y in model.YEAR) 
        # -   sum(model.v_Export[r,l,f,y]*model.p_ExportPrice[r,f,y]
        #         for r in model.REGION
        #         for l in model.TIMESLICE 
        #         for f in model.FUEL
        #         for y in model.YEAR)
)

 