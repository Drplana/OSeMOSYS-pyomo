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
    if y>min(model.YEAR) and y - model.p_VidaUtilRecuperada[r,t]>min(model.YEAR):
        return model.v_RecoveredCapacity[r,t,y] <= model.p_ResidualCapacity[r,t,y-1]-model.p_ResidualCapacity[r,t,y] + model.v_RecoveredCapacity[r,t,y-model.p_VidaUtilRecuperada[r,t]]
    elif y>min(model.YEAR):
        return model.v_RecoveredCapacity[r,t,y] <= model.p_ResidualCapacity[r,t,y-1]-model.p_ResidualCapacity[r,t,y] 
    else:
        return model.v_RecoveredCapacity[r,t,y] == 0

def Accumulated_Recovered_Capacity(model,r,t,y):
    return (
        model.v_AccumulatedRecoveredCapacity[r,t,y] 
    == sum(model.v_RecoveredCapacity[r,t,yy]
    for yy in model.YEAR 
    if ((y-yy < model.p_VidaUtilRecuperada[r,t]) and (y-yy>=0) ))
    )

