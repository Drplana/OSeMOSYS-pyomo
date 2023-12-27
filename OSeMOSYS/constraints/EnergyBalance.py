
########################################################################
##################           EnergyBalance A                      ######
from pyomo.environ import *
def EBa1_RateOfFuelProduction1(model, r, l, f, t, m, y):
    if model.p_OutputActivityRatio [r,t,f,m,y] !=0:
        return (
            model.v_RateOfActivity[r,l,t,m,y]
            *model.p_OutputActivityRatio[r,t,f,m,y] 
        == model.v_RateOfProductionByTechnologyByMode[r,l,t,m,f,y]
        # if model.p_OutputActivityRatio [r,t,f,m,y] !=0
        ) 
        
    else:
        return Constraint.Skip 
        
        # return model.v_RateOfProductionByTechnologyByMode[r, l, t, m, f, y] == 0

def EBa2_RateOfFuelProduction2(model, r, l, f, t, y):
    #for m in model.MODE_OF_OPERATION: 
        
            return (sum (model.v_RateOfProductionByTechnologyByMode[r,l,t,m,f,y] 
                         for m in model.MODE_OF_OPERATION
                         if model.p_OutputActivityRatio [r,t,f,m,y] !=0)
            == model.v_RateOfProductionByTechnology[r,l,t,f,y]
            )
        # else: 
        #     return Constraint.Skip
def EBa3_RateOfFuelProduction3(model,r, l,f,y):
    return (
            sum(model.v_RateOfProductionByTechnology[r,l,t,f,y] 
                for t in model.TECHNOLOGY)
        == model.v_RateOfProduction[r,l,f,y]
        )

def EBa4_RateOfFuelUse1(model,r,l,f,t,m,y):
    if model.p_InputActivityRatio[r,t,f,m,y] !=0:
        return (
            model.v_RateOfActivity[r,l,t,m,y]
            *model.p_InputActivityRatio[r,t,f,m,y] 
        == model.v_RateOfUseByTechnologyByMode[r,l,t,m,f,y]
        )    
    else: return Constraint.Skip
       
def EBa5_RateOfFuelUse2(model,r,l,f,t,y):
    # for m in model.MODE_OF_OPERATION:
    #     if model.p_InputActivityRatio[r,t,f,m,y] !=0:
            return (
                sum(model.v_RateOfUseByTechnologyByMode[r,l,t,m,f,y] 
                    for m in model.MODE_OF_OPERATION
                    if model.p_InputActivityRatio[r,t,f,m,y] !=0) 
            == model.v_RateOfUseByTechnology[r,l,t,f,y]
            )
        # else: return Constraint.Skip
def EBa6_RateOfFuelUse3(model,r, l, f, y):
    return (
            sum(model.v_RateOfUseByTechnology[r,l,t,f,y] 
                for t in model.TECHNOLOGY) 
            == model.v_RateOfUse [r,l,f,y]
        )
def EBa7_EnergyBalanceEachTS1(model, r,l,f,y):
    return (
    model.v_RateOfProduction[r,l,f,y]
    *model.p_YearSplit[l,y]
    == model.v_Production[r,l,f,y] 
    )       

def EBa8_EnergyBalanceEachTS2(model,r,l,f,y):
    return (
    model.v_RateOfUse[r,l,f,y]
    *model.p_YearSplit[l,y] 
    == model.v_Use[r,l,f,y]
    )

def EBa9_EnergyBalanceEachTS3(model,r,l,f,y):
    return (
        model.v_RateOfDemand[r,l,f,y]
        *model.p_YearSplit[l,y] 
        == model.v_Demand[r,l,f,y]
        )    
def EBa10_EnergyBalanceEachTS4(model, r, rr, l, f, y):
    return (
        model.v_Trade [r,rr,l,f,y] 
        == -model.v_Trade[rr,r,l,f,y]
    )
def EBa11_EnergyBalanceEachTS5(model, r,l,f,y):
    return (
            model.v_Production[r,l,f,y]
            >= model.v_Demand[r,l,f,y] 
            + model.v_Use[r,l,f,y]
            + sum(model.v_Trade[r,rr,l,f,y]*model.p_TradeRoute[r,rr,f,y] 
                  for rr in model.REGION)
            )
################################################################################
################              Energy Balance B           #######################
def EBb1_EnergyBalanceEachYear1(model,r,f,y):
    return (
            sum(model.v_Production[r,l,f,y] for l in model.TIMESLICE) 
            == model.v_ProductionAnnual[r,f,y]
        )
def EBb2_EnergyBalanceEachYear2(model, r, f,y):
    return (
            sum(model.v_Use[r,l,f,y] for l in model.TIMESLICE) 
            == model.v_UseAnnual[r,f,y]
        )
def EBb3_EnergyBalanceEachYear3(model, r,rr,f,y):
    return (
            sum(model.v_Trade[r,rr,l,f,y] for l in model.TIMESLICE) 
            == model.v_TradeAnnual[r,rr,f,y] 
        )
    
"""Ver documentación"""    
def EBb4_EnergyBalanceEachYear4(model, r, f, y):
    return (
            model.v_ProductionAnnual[r,f,y]
            >= model.v_UseAnnual[r,f,y]
            + sum(model.v_TradeAnnual[r,rr,f,y]
                  *model.p_TradeRoute[r,rr,f,y] for rr in model.REGION) 
                  + model.p_AccumulatedAnnualDemand[r,f,y]  
                  
        )
                      
        