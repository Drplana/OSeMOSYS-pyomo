from pyomo.environ import *
"""Reserve Margin Constraints
Ensures that sufficient reserve capacity of specific technologies 
(ReserveMarginTagTechnology = 1) is installed such that the user-defined 
ReserveMargin is maintained. RM1 has an error in the documentation """

def RM1_ReserveMargin_TechnologiesIncluded_In_Activity_Units(model,r,y):
    for t in model.TECHNOLOGY:
        if model.p_ReserveMarginTagTechnology[r, t, y] !=0 :
            return (
                    sum(
                        (
                model.v_TotalCapacityAnnual[r, t, y]
                * model.p_ReserveMarginTagTechnology[r, t, y]
                * model.p_CapacityToActivityUnit[r, t]
            )
            for t in model.TECHNOLOGY
        )
        == model.v_TotalCapacityInReserveMargin[r, y]
    )
        else:
            return model.v_TotalCapacityInReserveMargin[r, y] == 0
    # return (
    #     sum(model.v_TotalCapacityAnnual[r,t,y]
    #         *model.p_ReserveMarginTagTechnology[r,t,y]
    #         *model.p_CapacityToActivityUnit[r,t]
    #         for t in model.TECHNOLOGY
    #     )
    #     == model.v_TotalCapacityInReserveMargin[r,y]
    # )
def RM2_ReserveMargin_FuelsIncluded(model, r,l,y):
    return (
            sum(model.v_RateOfProduction[r,l,f,y]
            *model.p_ReserveMarginTagFuel[r,f,y] for f in model.FUEL)
            == model.v_DemandNeedingReserveMargin[r,l,y]
        )
def RM3_ReserveMargin_Constraint(model, r, l, y):
    # if model.p_ReserveMargin[r,y]!=0:
        return ( 
            model.v_DemandNeedingReserveMargin[r,l,y]
            *model.p_ReserveMargin[r,y] 
            <= model.v_TotalCapacityInReserveMargin[r,y]
        )
    # else: return Constraint.Skip
