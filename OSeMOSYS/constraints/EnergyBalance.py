
########################################################################
##################           EnergyBalance A                      ######
from pyomo.environ import *
#s.t. EBa1_RateOfFuelProduction1{r in REGION, l in TIMESLICE, f in FUEL, t in TECHNOLOGY, m in MODE_OF_OPERATION, y in YEAR: OutputActivityRatio[r,t,f,m,y] <>0}:  
# RateOfActivity[r,l,t,m,y]*OutputActivityRatio[r,t,f,m,y]  = RateOfProductionByTechnologyByMode[r,l,t,m,f,y];
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
        
#s.t. EBa2_RateOfFuelProduction2{r in REGION, l in TIMESLICE, f in FUEL, t in TECHNOLOGY, y in YEAR}: sum{m in MODE_OF_OPERATION: OutputActivityRatio[r,t,f,m,y] <>0}
#RateOfProductionByTechnologyByMode[r,l,t,m,f,y] = RateOfProductionByTechnology[r,l,t,f,y] ;
def EBa2_RateOfFuelProduction2(model, r, l, f, t, y):
    #for m in model.MODE_OF_OPERATION: 
        
            return (sum (model.v_RateOfProductionByTechnologyByMode[r,l,t,m,f,y] 
                         for m in model.MODE_OF_OPERATION
                         if model.p_OutputActivityRatio [r,t,f,m,y] !=0)
            == model.v_RateOfProductionByTechnology[r,l,t,f,y]
            )
        # else: 
        #     return Constraint.Skip
        
#s.t. EBa3_RateOfFuelProduction3{r in REGION, l in TIMESLICE, f in FUEL, y in YEAR}: 
# sum{t in TECHNOLOGY} RateOfProductionByTechnology[r,l,t,f,y]  =  RateOfProduction[r,l,f,y];        
def EBa3_RateOfFuelProduction3(model,r, l,f,y):
    return (
            sum(model.v_RateOfProductionByTechnology[r,l,t,f,y] 
                for t in model.TECHNOLOGY)
        == model.v_RateOfProduction[r,l,f,y]
        )
    
#s.t. EBa4_RateOfFuelUse1{r in REGION, l in TIMESLICE, f in FUEL, t in TECHNOLOGY, m in MODE_OF_OPERATION, y in YEAR: InputActivityRatio[r,t,f,m,y]<>0}: 
# RateOfActivity[r,l,t,m,y]*InputActivityRatio[r,t,f,m,y]  = RateOfUseByTechnologyByMode[r,l,t,m,f,y];

def EBa4_RateOfFuelUse1(model,r,l,f,t,m,y):
    if model.p_InputActivityRatio[r,t,f,m,y] !=0:
        return (
            model.v_RateOfActivity[r,l,t,m,y]
            *model.p_InputActivityRatio[r,t,f,m,y] 
        == model.v_RateOfUseByTechnologyByMode[r,l,t,m,f,y]
        )    
    else: return Constraint.Skip
#s.t. EBa5_RateOfFuelUse2{r in REGION, l in TIMESLICE, f in FUEL, t in TECHNOLOGY, y in YEAR}: sum{m in MODE_OF_OPERATION: InputActivityRatio[r,t,f,m,y]<>0} 
# RateOfUseByTechnologyByMode[r,l,t,m,f,y] = RateOfUseByTechnology[r,l,t,f,y];       
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
#s.t. EBa6_RateOfFuelUse3{r in REGION, l in TIMESLICE, f in FUEL, y in YEAR}: 
# sum{t in TECHNOLOGY} RateOfUseByTechnology[r,l,t,f,y]  = RateOfUse[r,l,f,y];        
def EBa6_RateOfFuelUse3(model,r, l, f, y):
    return (
            sum(model.v_RateOfUseByTechnology[r,l,t,f,y] 
                for t in model.TECHNOLOGY) 
            == model.v_RateOfUse [r,l,f,y]
        )
#  s.t. EBa7_EnergyBalanceEachTS1{r in REGION, l in TIMESLICE, f in FUEL, y in YEAR}: 
# RateOfProduction[r,l,f,y]*YearSplit[l,y] = Production[r,l,f,y]; 
def EBa7_EnergyBalanceEachTS1(model, r,l,f,y):
    return (
    model.v_RateOfProduction[r,l,f,y]
    *model.p_YearSplit[l,y]
    == model.v_Production[r,l,f,y] 
    )       
#s.t. EBa8_EnergyBalanceEachTS2{r in REGION, l in TIMESLICE, f in FUEL, y in YEAR}: 
# RateOfUse[r,l,f,y]*YearSplit[l,y] = Use[r,l,f,y];
def EBa8_EnergyBalanceEachTS2(model,r,l,f,y):
    return (
    model.v_RateOfUse[r,l,f,y]
    *model.p_YearSplit[l,y] 
    == model.v_Use[r,l,f,y]
    )
#s.t. EBa9_EnergyBalanceEachTS3{r in REGION, l in TIMESLICE, f in FUEL, y in YEAR}: 
# RateOfDemand[r,l,f,y]*YearSplit[l,y] = Demand[r,l,f,y];
def EBa9_EnergyBalanceEachTS3(model,r,l,f,y):
    return (
        model.v_RateOfDemand[r,l,f,y]
        *model.p_YearSplit[l,y] 
        == model.v_Demand[r,l,f,y]
        )
#s.t. EBa10_EnergyBalanceEachTS4{r in REGION, rr in REGION, l in TIMESLICE, f in FUEL, y in YEAR}: Trade[r,rr,l,f,y] = -Trade[rr,r,l,f,y];        
def EBa10_EnergyBalanceEachTS4(model, r, rr, l, f, y):
    return (
        model.v_Trade [r,rr,l,f,y] 
        == -model.v_Trade[rr,r,l,f,y]
    )
#s.t. EBa11_EnergyBalanceEachTS5{r in REGION, l in TIMESLICE, f in FUEL, y in YEAR}: 
#Production[r,l,f,y] >= Demand[r,l,f,y] + Use[r,l,f,y] + sum{rr in REGION} Trade[r,rr,l,f,y]*TradeRoute[r,rr,f,y];    
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
#s.t. EBb1_EnergyBalanceEachYear1{r in REGION, f in FUEL, y in YEAR}: sum{l in TIMESLICE} Production[r,l,f,y] = ProductionAnnual[r,f,y];

def EBb1_EnergyBalanceEachYear1(model,r,f,y):
    return (
            sum(model.v_Production[r,l,f,y] for l in model.TIMESLICE) 
            == model.v_ProductionAnnual[r,f,y]
        )
#s.t. EBb2_EnergyBalanceEachYear2{r in REGION, f in FUEL, y in YEAR}: sum{l in TIMESLICE} Use[r,l,f,y] = UseAnnual[r,f,y];   
def EBb2_EnergyBalanceEachYear2(model, r, f,y):
    return (
            sum(model.v_Use[r,l,f,y] for l in model.TIMESLICE) 
            == model.v_UseAnnual[r,f,y]
        )
#s.t. EBb3_EnergyBalanceEachYear3{r in REGION, rr in REGION, f in FUEL, y in YEAR}: sum{l in TIMESLICE} Trade[r,rr,l,f,y] = TradeAnnual[r,rr,f,y];    
def EBb3_EnergyBalanceEachYear3(model, r,rr,f,y):
    return (
            sum(model.v_Trade[r,rr,l,f,y] for l in model.TIMESLICE) 
            == model.v_TradeAnnual[r,rr,f,y] 
        )
    
"""Ver documentación"""
#s.t. EBb4_EnergyBalanceEachYear4{r in REGION, f in FUEL, y in YEAR}: 
# ProductionAnnual[r,f,y] >= UseAnnual[r,f,y] + sum{rr in REGION} TradeAnnual[r,rr,f,y]*TradeRoute[r,rr,f,y] + AccumulatedAnnualDemand[r,f,y];    
def EBb4_EnergyBalanceEachYear4(model, r, f, y):
    return (
            model.v_ProductionAnnual[r,f,y]
            >= model.v_UseAnnual[r,f,y]
            + sum(model.v_TradeAnnual[r,rr,f,y]
                  *model.p_TradeRoute[r,rr,f,y] for rr in model.REGION) 
                  + model.p_AccumulatedAnnualDemand[r,f,y]  
                  
        )
                      
        