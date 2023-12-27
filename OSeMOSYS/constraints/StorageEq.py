"""Storage equations"""
from pyomo.environ import *

def S1_RateOfStorageCharge(model, r,s,ls,ld,lh,y):
    
        return (
            sum(
                model.v_RateOfActivity[r,l,t,m,y]
                *model.p_TechnologyToStorage[r,t,s,m]
                *model.p_Conversionls[l,ls]
                *model.p_Conversionld[l,ld]
                *model.p_Conversionlh[l,lh]
                for m in model.MODE_OF_OPERATION
                for l in model.TIMESLICE
                for t in model.TECHNOLOGY
                if model.p_TechnologyToStorage[r,t,s,m]>0
            )
            == model.v_RateOfStorageCharge[r,s,ls,ld,lh,y]
    )
        
def S2_RateOfStorageDischarge(model, r,s,ls,ld,lh,y):
    
        return (
            sum(
                model.v_RateOfActivity[r, l, t, m, y]
                *model.p_TechnologyFromStorage[r, t, s, m]
                * model.p_Conversionls[l, ls]
                * model.p_Conversionld[l, ld]
                * model.p_Conversionlh[l, lh]
                for m in model.MODE_OF_OPERATION
                for l in model.TIMESLICE
                for t in model.TECHNOLOGY
                if model.p_TechnologyFromStorage[r,t,s,m]>0
            )
            == model.v_RateOfStorageDischarge[r, s, ls, ld, lh, y]
        )
    
def S3_NetChargeWithinYear(model, r,s,ls,ld,lh,y,):
    return (
        sum(
            (
                model.v_RateOfStorageCharge[r, s, ls, ld, lh, y]
                - model.v_RateOfStorageDischarge[r,s,ls,ld,lh,y]
            )
            * model.p_YearSplit[l, y]
            * model.p_Conversionls[l, ls]
            * model.p_Conversionld[l, ld]
            * model.p_Conversionlh[l, lh]
            for l in model.TIMESLICE
        )
        == model.v_NetChargeWithinYear[r, s, ls, ld, lh, y]
    )

def S4_NetChargeWithinDay(model, r,s,ls,ld,lh,y):
    return (
        (model.v_RateOfStorageCharge[r,s,ls,ld,lh,y]
        -model.v_RateOfStorageDischarge[r,s,ls,ld,lh,y])
        *model.p_DaySplit[lh,y] 
        == model.v_NetChargeWithinDay[r,s,ls,ld,lh,y]
    )
def S5_and_S6_StorageLevelYearStart(model,r,s,y):
    if y == min(model.YEAR):
        return model.p_StorageLevelStart[r,s] == model.v_StorageLevelYearStart[r,s,y]
    else:
        return (
            model.v_StorageLevelYearStart[r,s,y-1]
            + sum(model.v_NetChargeWithinYear[r,s,ls,ld,lh,y-1]
                  for ls in model.SEASON
                  for ld in model.DAYTYPE
                  for lh in model.DAILYTIMEBRACKET)
            == model.v_StorageLevelYearStart [r,s,y]
        )
def S7_and_S8_StorageLevelYearFinish(model,r,s,y):
    if y < max(model.YEAR):
        return model.v_StorageLevelYearStart[r,s,y+1] == model.v_StorageLevelYearFinish[r,s,y]
    else:
        return (
            model.v_StorageLevelYearStart[r,s,y]
            + sum(model.v_NetChargeWithinYear[r,s,ls,ld,lh,y]
                  for ls in model.SEASON
                  for ld in model.DAYTYPE
                  for lh in model.DAILYTIMEBRACKET)
            == model.v_StorageLevelYearFinish[r,s,y]
        )
def S9_and_S10_StorageLevelSeasonStart(model, r,s,ls,y):
    if ls == min(model.SEASON):
        return model.v_StorageLevelYearStart[r,s,y] == model.v_StorageLevelSeasonStart[r,s,ls,y]
    else:
        return(
            model.v_StorageLevelSeasonStart[r,s,ls-1,y]
            + sum(model.v_NetChargeWithinYear[r,s,ls,ld-1,lh,y]
                  for ld in model.DAYTYPE
                  for lh in model.DAILYTIMEBRACKET
                )
            == model.v_StorageLevelSeasonStart[r,s,ls,y]
        )
def S11_and_S12_StorageLevelDayTypeStart(model, r,s,ls,ld,y):
    if ld == min(model.DAYTYPE):
        return model.v_StorageLevelSeasonStart[r,s,ls,y] == model.v_StorageLevelDayTypeStart[r,s,ls,ld,y]
    else:
        return (
            model.v_StorageLevelDayTypeStart[r,s,ls,ld-1,y]
            +sum (model.v_NetChargeWithinDay[r,s,ls,ld-1,lh,y]
                  *model.p_DaysInDayType[ls,ld-1,y]
                   for lh in model.DAILYTIMEBRACKET)
            == model.v_StorageLevelDayTypeStart[r,s,ls,ld,y]  
        )
def S13_and_S14_and_S15_StorageLevelDayTypeFinish(model, r,s,ls,ld,y):
    if ls == max(model.SEASON) and ld == max(model.DAYTYPE):
        return (model.v_StorageLevelYearFinish[r,s,y] 
                == model.v_StorageLevelDayTypeFinish[r,s,ls,ld,y]
                )
    elif ld == max(model.DAYTYPE):
        return (model.v_StorageLevelSeasonStart[r,s,ls+1,y] 
                == model.v_StorageLevelDayTypeFinish[r,s,ls,ld,y]
                )
    else:
        return (
            model.v_StorageLevelDayTypeFinish [r,s,ls,ld+1,y]
            -sum(model.v_NetChargeWithinDay[r,s,ls,ld+1,lh,y]
                 *model.p_DaysInDayType[ls,ld+1,y] 
                 for lh in model.DAILYTIMEBRACKET)
            == model.v_StorageLevelDayTypeFinish[r,s,ls,ld,y]
        )    
   
    
    
    
    
    