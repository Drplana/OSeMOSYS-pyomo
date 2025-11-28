from pyomo.environ import *

# # def Must_Run(model, r,l,m,t,f,y):
# #     if model.p_OutputActivityRatio[r,t,f,m,y] !=0 and model.p_MustRunTech[r,t,y] !=0:
# #     # if model.p_MustRunFuel[r,f,y]!=0:
# #         return( sum(model.v_RateOfActivity[r,l,t,m,y]*model.p_OutputActivityRatio[r,t,f,m,y]*model.p_MustRunTech[r,t,y] for m in model.MODE_OF_OPERATION for t in model.TECHNOLOGY ) 
# #                >= model.p_MustRun[r,y]*model.v_RateOfDemand[r,f,l,y])
# #             #    sum(model.v_RateOfDemand[r,l,f,y]*model.p_MustRun[r,y]*model.p_MustRunFuel[r,f,y])
# #     else: return Constraint.Skip

# def Must_Run(model, r,l,y):
#     # if model.p_OutputActivityRatio[r,t,f,m,y] !=0 and model.p_MustRunTech[r,t,y] !=0:
#     # if model.p_MustRunFuel[r,f,y]!=0:
#         return( sum( model.v_RateOfProductionByTechnology[r,l,t,f,y]*model.p_MustRunTech[r,t,y] for t in model.TECHNOLOGY for f in model.FUEL)
#                >= model.p_MustRun[r,y]*sum(model.v_RateOfDemand[r,l,f,y] for f in model.FUEL))
            #    sum(model.v_RateOfDemand[r,l,f,y]*model.p_MustRun[r,y]*model.p_MustRunFuel[r,f,y])
    # else: return Constraint.Skip
def Must_Run(model, r,t,l,y):
    return (model.v_RateOfTotalActivity[r,t,l,y] 
            >=
         model.p_MustRunTech[r,t,y]
        *model.v_TotalCapacityAnnual[r,t,y]
        *model.p_CapacityFactor[r,t,l,y]
        *model.p_CapacityToActivityUnit[r,t]
        *model.p_AvailabilityFactor[r,t,y]    
    )
