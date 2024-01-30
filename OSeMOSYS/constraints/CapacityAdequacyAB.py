#################################
#########Capacity Adequacy A ####
from pyomo.environ import *

def CAa1_TotalNewCapacity(model, r, t, y ):
    """=
s.t. CAa1_TotalNewCapacity{r in REGION, t in TECHNOLOGY, y in YEAR}:
AccumulatedNewCapacity[r,t,y] = sum{yy in YEAR: y-yy < OperationalLife[r,t] && y-yy>=0} NewCapacity[r,t,yy];
    """    
    return (
        model.v_AccumulatedNewCapacity [r,t,y] 
    == sum(model.v_NewCapacity [r,t,yy]
    for yy in model.YEAR 
    if ((y-yy < model.p_OperationalLife[r,t]) and (y-yy>=0) ))
    )
    
def CAa2_TotalAnnualCapacity(model, r, t, y):
    """
s.t. CAa2_TotalAnnualCapacity{r in REGION, t in TECHNOLOGY, y in YEAR}: 
AccumulatedNewCapacity[r,t,y]+ ResidualCapacity[r,t,y] = TotalCapacityAnnual[r,t,y];
    """    
    return (model.v_AccumulatedNewCapacity[r,t,y] 
            + model.p_ResidualCapacity[r,t,y]
            == model.v_TotalCapacityAnnual[r,t,y]
            )
  
def CAa3_TotalActivityOfEachTechnology(model, r, t, l, y):
    """
s.t. CAa3_TotalActivityOfEachTechnology{r in REGION, t in TECHNOLOGY, l in TIMESLICE, y in YEAR}: 
sum{m in MODE_OF_OPERATION} RateOfActivity[r,l,t,m,y] = RateOfTotalActivity[r,t,l,y]; 
    """    
    return (
        sum(model.v_RateOfActivity [r,l,t,m,y] 
        for m in model.MODE_OF_OPERATION) 
        == model.v_RateOfTotalActivity [r,t,l,y]
    )

def CAa4_ConstraintCapacity(model, r,t,l,y):
    """
s.t. CAa4_Constraint_Capacity{r in REGION, l in TIMESLICE, t in TECHNOLOGY, y in YEAR}:
RateOfTotalActivity[r,t,l,y] <= TotalCapacityAnnual[r,t,y] * CapacityFactor[r,t,l,y]*CapacityToActivityUnit[r,t];
    """    
    return (
        model.v_RateOfTotalActivity [r,t,l,y] 
        <= model.v_TotalCapacityAnnual [r,t,y]
        *model.p_CapacityFactor[r,t,l,y]
        *model.p_CapacityToActivityUnit[r,t]
        
    )

def CAa5_TotalNewCapacity(model, r, t, y):
    """
    s.t. CAa5_TotalNewCapacity{r in REGION, t in TECHNOLOGY, y in YEAR: CapacityOfOneTechnologyUnit[r,t,y]<>0}: 
    CapacityOfOneTechnologyUnit[r,t,y]*NumberOfNewTechnologyUnits[r,t,y] = NewCapacity[r,t,y];    
    """
    if model.p_CapacityOfOneTechnologyUnit[ r, t, y] != 0:
        return (
            model.p_CapacityOfOneTechnologyUnit [r,t,y] 
            *model.v_NumberOfNewTechnologyUnits[r,t,y]
            == model.v_NewCapacity[r,t,y]
        )
    else: return Constraint.Skip
    

###############################
###### Capacity Adecuacy B ####
"""Revisar"""

def CAb1_PlannedMaintenance(model, r ,t,y):
    """
s.t. CAb1_PlannedMaintenance{r in REGION, t in TECHNOLOGY, y in YEAR}: sum{l in TIMESLICE} 
RateOfTotalActivity[r,t,l,y]*YearSplit[l,y] <= sum{l in TIMESLICE} 
( TotalCapacityAnnual[r,t,y]
*CapacityFactor[r,t,l,y]
*YearSplit[l,y] )
*AvailabilityFactor[r,t,y]
*CapacityToActivityUnit[r,t];
    """    
    return (sum( model.v_RateOfTotalActivity[r,t,l,y]
                *model.p_YearSplit[l,y] for l in model.TIMESLICE )
    <=sum(model.v_TotalCapacityAnnual[r,t,y]
    *(model.p_CapacityFactor[r,t,l,y]
    *model.p_YearSplit[l,y]) for l in model.TIMESLICE)
    *model.p_AvailabilityFactor[r,t,y]
    *model.p_CapacityToActivityUnit[r,t] 
    )
    
  