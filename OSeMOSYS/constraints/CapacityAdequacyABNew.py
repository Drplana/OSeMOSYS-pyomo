#################################
#########Capacity Adequacy A ####
from pyomo.environ import *

def CAa1_TotalNewCapacity(model, r, t, y ):
    return (
        model.v_AccumulatedNewCapacity [r,t,y] 
    == sum(model.v_NewCapacity [r,t,yy]
    for yy in model.YEAR 
    if ((y-yy< model.p_OperationalLife[r,t]) and (y-yy>=0) ))
    )
"""Restriccion para obtener la capacidad total anual
Residualcapacity es una variable intermedia si la capacidadofonetechnologyunit
es diferente de cero
"""
    
def CAa2_TotalAnnualCapacity(model, r, t, y):
    #si se cumple definir número existente unidades y se obtiene la capacidad residual
    if model.p_CapacityOfOneTechnologyUnit[ r, t, y] != 0:
        return (model.v_AccumulatedNewCapacity[r,t,y] 
            + model.v_ResidualCapacity[r,t,y] 
            == model.v_TotalCapacityAnnual[r,t,y]
            )
        
    else:return (model.v_AccumulatedNewCapacity[r,t,y] 
            + model.p_ResidualCapacity[r,t,y]
            == model.v_TotalCapacityAnnual[r,t,y]
            )


def CAa1n_TotalResidualCapacity(model,r,t,y):
    return(
        model.v_ResidualCapacity[r,t,y]
        == model.p_NumberOfExistingUnits[r,t,y]
        *model.p_CapacityOfOneTechnologyUnit[r,t,y]
        
    )    

def CAa3_TotalActivityOfEachTechnology(model, r, t, l, y):
    return (
        sum(model.v_RateOfActivity [r,l,t,m,y] 
        for m in model.MODE_OF_OPERATION) 
        == model.v_RateOfTotalActivity [r,t,l,y]
    )

def CAa4_ConstraintCapacity(model, r,t,l,y):
    return (
        model.v_RateOfTotalActivity [r,t,l,y] 
        <= model.v_TotalCapacityAnnual [r,t,y]
        *(model.p_CapacityFactor[r,t,l,y]
        *model.p_CapacityToActivityUnit[r,t]
        )
    )
    
# """Restricción para el calcular el abandono de electricidad"""    
# def CAa10_Abandono(model,r,t,l,y):
#     return(
#         model.v_Abandono [r,t,l,y] <= (model.v_RateOfTotalActivity [r,t,l,y] - model.v_TotalCapacityAnnual [r,t,y]
#         *(model.p_CapacityFactor[r,t,l,y]
#         *model.p_CapacityToActivityUnit[r,t]
#         ))*model.p_RETagTechnology[r,t,y]
#     )
# """Para obtener el cubrimiento en MWh"""    
# def CAa11_Cubrimiento(model,r,t,l,y):
#     return(
#         model.v_Cubrimiento [r,t,l,y] == model.v_RateOfTotalActivity [r,t,l,y]*model.p_YearSplit[l,y]
#     )        

def CAa5_TotalNewCapacity(model, r, t, y):
    if model.p_CapacityOfOneTechnologyUnit[ r, t, y] != 0:
        return (
            model.p_CapacityOfOneTechnologyUnit [r,t,y] 
            *model.v_NumberOfNewTechnologyUnits[r,t,y]
            *model.p_Availability[r,t,y]
            == model.v_NewCapacity[r,t,y]
        )
    else: return Constraint.Skip
    

###############################
###### Capacity Adecuacy B ####
"""Revisar"""

def CAb1_PlannedMaintenance(model, r ,t,y):
    return (sum( model.v_RateOfTotalActivity[r,t,l,y]
                *model.p_YearSplit[l,y] for l in model.TIMESLICE )
    <=sum(model.v_TotalCapacityAnnual[r,t,y]
    *(model.p_CapacityFactor[r,t,l,y]
    *model.p_YearSplit[l,y]) for l in model.TIMESLICE)
    *model.p_AvailabilityFactor[r,t,y]
    *model.p_CapacityToActivityUnit[r,t] 
    )
    
  