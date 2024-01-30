from pyomo.environ import *
# """Reserve Margin Constraints
# Ensures that sufficient reserve capacity of specific technologies 
# (ReserveMarginTagTechnology = 1) is installed such that the user-defined 
# ReserveMargin is maintained. RM1 has an error in the documentation """
# def RM1_ReserveMargin_TechnologiesIncluded_In_Activity_Units(model,r,y):
#     """
#  s.t. RM1_ReserveMargin_TechnologiesIncluded_In_Activity_Units{r in REGION, l in TIMESLICE, y in YEAR}: 
#  sum {t in TECHNOLOGY} TotalCapacityAnnual[r,t,y] * ReserveMarginTagTechnology[r,t,y] * CapacityToActivityUnit[r,t]	 = 	TotalCapacityInReserveMargin[r,y];
#     """    
#     return (
#             sum(
#                 model.v_TotalCapacityAnnual[r, t, y]
#                 * model.p_ReserveMarginTagTechnology[r, t, y]
#                 * model.p_CapacityToActivityUnit[r, t]
            
#             for t in model.TECHNOLOGY if model.p_ReserveMarginTagTechnology[r, t, y] != 0)
            
        
#         == model.v_TotalCapacityInReserveMargin[r, y]
#         )

# def RM2_ReserveMargin_FuelsIncluded(model, r,l,y):
#     """
# s.t. RM2_ReserveMargin_FuelsIncluded{r in REGION, l in TIMESLICE, y in YEAR}: 
# sum {f in FUEL} RateOfProduction[r,l,f,y] * ReserveMarginTagFuel[r,f,y] = DemandNeedingReserveMargin[r,l,y];
#     """
#     return (
#             sum(model.v_RateOfProduction[r,l,f,y]
#             *model.p_ReserveMarginTagFuel[r,f,y] for f in model.FUEL)
#             == model.v_DemandNeedingReserveMargin[r,l,y]
#         )
# def RM3_ReserveMargin_Constraint(model, r, l, y):
#     """
# s.t. RM3_ReserveMargin_Constraint{r in REGION, l in TIMESLICE, y in YEAR}: 
# DemandNeedingReserveMargin[r,l,y] * ReserveMargin[r,y] <= TotalCapacityInReserveMargin[r,y];       
#     """
#     return ( 
#             model.v_DemandNeedingReserveMargin[r,l,y]
#             *model.p_ReserveMargin[r,y] 
#             <= model.v_TotalCapacityInReserveMargin[r,y]
#         )

""""Short Code equation"""
def RM3_ReserveMargin_Constraint(model, r, l, y):
     if model.p_OutputActivityRatio !=0 :
        return (
            sum(model.v_RateOfActivity [r, l, t, m, y] * model.p_OutputActivityRatio [r, t, f, m, y] * model.p_ReserveMarginTagFuel [r, f, y] * model.p_ReserveMargin [r, y] 
                for t in model.TECHNOLOGY for m in model.MODE_OF_OPERATION for f in model.FUEL)
        <= sum((sum(model.v_NewCapacity[r, t, yy] for yy in model.YEAR if y - yy < model.p_OperationalLife[r, t] and y - yy >= 0) + model.p_ResidualCapacity[r, t, y]) * model.p_ReserveMarginTagTechnology[r, t, y] * model.p_CapacityToActivityUnit[r, t] for t in model.TECHNOLOGY)
        )


