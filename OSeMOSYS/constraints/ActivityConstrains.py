from pyomo.environ import * 
"""ActivityConstrains
Annual Activity Constraints:
Ensures that the total activity of each technology over each year is
greater than and less than the user-defined parameters 
TotalTechnologyAnnualActivityLowerLimit and 
TotalTechnologyAnnualActivityUpperLimit respectively. """

def AAC1_TotalAnnualTechnologyActivity(model,r,t,y):
    """
s.t. AAC1_TotalAnnualTechnologyActivity{r in REGION, t in TECHNOLOGY, y in YEAR}: 
sum{l in TIMESLICE} RateOfTotalActivity[r,t,l,y]*YearSplit[l,y] = TotalTechnologyAnnualActivity[r,t,y];    
    """    
    return (
            sum(model.v_RateOfTotalActivity[r,t,l,y]
            *model.p_YearSplit[l,y] for l in model.TIMESLICE)
            ==model.v_TotalTechnologyAnnualActivity[r,t,y]
        )
def AAC2_TotalAnnualTechnologyActivityUpperLimit(model, r,t,y):
    """
s.t. AAC2_TotalAnnualTechnologyActivityUpperLimit{r in REGION, t in TECHNOLOGY, y in YEAR}: 
TotalTechnologyAnnualActivity[r,t,y] <= TotalTechnologyAnnualActivityUpperLimit[r,t,y] ;
    """    
    return(
        model.v_TotalTechnologyAnnualActivity[r,t,y]
        <=model.p_TotalTechnologyAnnualActivityUpperLimit[r,t,y]
    )
def AAC3_TotalAnnualTechnologyActivityLowerLimit(model, r,t,y):
    """
s.t. AAC3_TotalAnnualTechnologyActivityLowerLimit{r in REGION, t in TECHNOLOGY, y in YEAR: 
    TotalTechnologyAnnualActivityLowerLimit[r,t,y]>0}: 
        TotalTechnologyAnnualActivity[r,t,y] >= TotalTechnologyAnnualActivityLowerLimit[r,t,y] ;
    """    
    if model.p_TotalTechnologyAnnualActivityLowerLimit[r,t,y]>0:
        return (
            model.v_TotalTechnologyAnnualActivity[r,t,y] 
            >=  model.p_TotalTechnologyAnnualActivityLowerLimit[r,t,y]
        )
    else: return Constraint.Skip
"""Total Activity Constraints":
Ensures that the total activity of each technology over the entire model 
period is greater than and less than the user-defined parameters 
TotalTechnologyModelPeriodActivityLowerLimit and 
TotalTechnologyModelPeriodActivityUpperLimit respectively.
"""
def TAC1_TotalModelHorizonTechnologyActivity(model, r,t):
    """
s.t. TAC1_TotalModelHorizonTechnologyActivity{r in REGION, t in TECHNOLOGY}: 
sum{y in YEAR} TotalTechnologyAnnualActivity[r,t,y] = TotalTechnologyModelPeriodActivity[r,t];
    """    
    return (
            sum(model.v_TotalTechnologyAnnualActivity[r,t,y] for y in model.YEAR)
            == model.v_TotalTechnologyModelPeriodActivity[r,t]
        )
def TAC2_TotalModelHorizonTechnologyActivityUpperLimit(model, r,t):
    """
s.t. TAC2_TotalModelHorizonTechnologyActivityUpperLimit{r in REGION, t in TECHNOLOGY: 
    TotalTechnologyModelPeriodActivityUpperLimit[r,t]>0}: 
        TotalTechnologyModelPeriodActivity[r,t] <= TotalTechnologyModelPeriodActivityUpperLimit[r,t] ;
    """    
    if model.p_TotalTechnologyModelPeriodActivityUpperLimit[r,t]>0:
        return(
        model.v_TotalTechnologyModelPeriodActivity[r,t]
        <= model.p_TotalTechnologyModelPeriodActivityUpperLimit[r,t]
    )
    else: 
        return Constraint.Skip

def TAC3_TotalModelHorizenTechnologyActivityLowerLimit(model, r, t):
    """
s.t. TAC3_TotalModelHorizenTechnologyActivityLowerLimit{r in REGION, t in TECHNOLOGY: 
    TotalTechnologyModelPeriodActivityLowerLimit[r,t]>0}: 
        TotalTechnologyModelPeriodActivity[r,t] >= TotalTechnologyModelPeriodActivityLowerLimit[r,t] ;
    """    
    if model.p_TotalTechnologyModelPeriodActivityLowerLimit[r,t] > 0:
        return (
            model.v_TotalTechnologyModelPeriodActivity[r,t]
            >= model.p_TotalTechnologyModelPeriodActivityLowerLimit[r,t]
        )
    else:
        return Constraint.Skip


