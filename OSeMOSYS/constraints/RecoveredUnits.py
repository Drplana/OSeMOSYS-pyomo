#################################
#########Unidades recuperadas ####
from pyomo.environ import *

def Recovered_Existing_Units(model, r, t, y ):
    if y>min(model.YEAR) and y-model.p_VidaUtilRecuperada[r,t]>min(model.YEAR):
        return model.v_RecoveredExistingUnits[r,t,y] <= model.p_NumberOfExistingUnits[r,t,y-1]-model.p_NumberOfExistingUnits[r,t,y] + model.v_RecoveredExistingUnits[r,t,y-model.p_VidaUtilRecuperada[r,t]]
      
    elif y > min(model.YEAR) :
        return model.v_RecoveredExistingUnits[r,t,y] <= model.p_NumberOfExistingUnits[r,t,y-1]-model.p_NumberOfExistingUnits[r,t,y]
        
    else:
        return model.v_RecoveredExistingUnits[r,t,y] == 0
    
def Accumulated_Recovered_Existing_Units(model,r,t,y):
    return (
        model.v_AccumulatedRecoveredUnits[r,t,y] 
    == sum(model.v_RecoveredExistingUnits[r,t,yy]
    for yy in model.YEAR 
    if ((y-yy < model.p_VidaUtilRecuperada[r,t]) and (y-yy>=0) ))
    )

def Recovered_Residual_Aggregated(model,r,t,y):
    # if y>min(model.YEAR):
    #     return model.v_RecoveredCapacity[r,t,y] == model.p_ResidualCapacity[r,t,y-1]-model.p_ResidualCapacity[r,t,y]
    if y>min(model.YEAR) and y - model.p_VidaUtilRecuperada[r,t]>min(model.YEAR) and model.p_ResidualCapacity[r,t,y-1]-model.p_ResidualCapacity[r,t,y]>0:
        # if y>min(model.YEAR) and y - model.p_VidaUtilRecuperada[r,t]>min(model.YEAR):
        return model.v_RecoveredCapacity[r,t,y] <= model.p_ResidualCapacity[r,t,y-1]-model.p_ResidualCapacity[r,t,y] + model.v_RecoveredCapacity[r,t,y-model.p_VidaUtilRecuperada[r,t]]
    elif y>min(model.YEAR) and model.p_ResidualCapacity[r,t,y-1]-model.p_ResidualCapacity[r,t,y]>0:
            return model.v_RecoveredCapacity[r,t,y] <= model.p_ResidualCapacity[r,t,y-1]-model.p_ResidualCapacity[r,t,y] 
    else:
        return model.v_RecoveredCapacity[r,t,y] == 0
    # else:
        # return model.v_RecoveredCapacity[r,t,y] == 0

def Accumulated_Recovered_Capacity(model,r,t,y):
    return (
        model.v_AccumulatedRecoveredCapacity[r,t,y] 
    == sum(model.v_RecoveredCapacity[r,t,yy]
    for yy in model.YEAR 
    if ((y-yy < model.p_VidaUtilRecuperada[r,t]) and (y-yy>=0) ))
    )

def Recovered_New_Capacity(model, r, t, y ):
    ol = model.p_OperationalLife[r,t]
    source_year = y - ol
    if source_year not in model.YEAR:
        return model.v_RecoveredNewCapacity[r,t,y] == 0
    return model.v_RecoveredNewCapacity[r,t,y] <= model.v_NewCapacity[r,t,source_year]

#     if y>min(model.YEAR) and y-model.p_OperationalLife[r,t]>=min(model.YEAR):
#         return model.v_RecoveredNewCapacity[r,t,y] <= model.v_NewCapacity[r,t,y-model.p_OperationalLife[r,t]]
#     elif y >= min(model.YEAR) and y-model.p_OperationalLife[r,t]<=min(model.YEAR):
#         return model.v_RecoveredNewCapacity[r,t,y] == 0


def Accumulated_Recovered_New_Capacity(model,r,t,y):
    L = model.p_VidaUtilRecuperada[r,t]
    valid_years = [yy for yy in model.YEAR if (0 <= y - yy < L)]
    return (model.v_AccumulatedRecoveredNewCapacity[r, t, y] ==
            sum(model.v_RecoveredNewCapacity[r, t, yy] for yy in valid_years))
#     return (
#         model.v_AccumulatedRecoveredNewCapacity[r,t,y] 
#     == sum(model.v_RecoveredNewCapacity[r,t,yy]
#     for yy in model.YEAR 
#     if ((y-yy <= model.p_VidaUtilRecuperada[r,t]) and (y-yy>=0) ))
#     )

