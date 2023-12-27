from pyomo.environ import *
"""Total Capacity Constraints:
Ensures that the total capacity of each technology in each year 
is greater than and less than the user-defined parameters 
TotalAnnualMinCapacityInvestment and TotalAnnualMaxCapacityInvestment 
respectively."""

def TCC1_TotalAnnualMaxCapacityConstraint(model,r,t,y):
    return (
        model.v_TotalCapacityAnnual[r,t,y]
        <= model.p_TotalAnnualMaxCapacity[r,t,y]
    )
def TCC2_TotalAnnualMinCapacityConstraint(model,r ,t,y):
    if model.p_TotalAnnualMinCapacity[r,t,y]>0:
        return (
            model.v_TotalCapacityAnnual[r,t,y]
            >= model.p_TotalAnnualMinCapacity[r,t,y]
        )
    else: return Constraint.Skip    

"""New Capacity Constraints 
 Ensures that the new capacity of each technology installed in each year 
 is greater than and less than the user-defined parameters 
 TotalAnnualMinCapacityInvestment and TotalAnnualMaxCapacityInvestment 
 respectively."""
def NCC1_TotalAnnualMaxNewCapacityConstraint(model, r,t,y):
    return (
        model.v_NewCapacity[r,t,y]
        <=model.p_TotalAnnualMaxCapacityInvestment[r,t,y]
    )
def NCC2_TotalAnnualMinNewCapacityConstraint(model, r,t,y):
    if model.p_TotalAnnualMinCapacityInvestment[r,t,y]>0:
        return(
            model.v_NewCapacity[r,t,y]
            >= model.p_TotalAnnualMinCapacityInvestment[r,t,y]
        )
    else: return Constraint.Skip