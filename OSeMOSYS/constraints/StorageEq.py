"""Storage equations"""
from pyomo.environ import *

def S1_RateOfStorageCharge(model, r,s,ls,ld,lh,y):
    """s.t. S1_RateOfStorageCharge{r in REGION, s in STORAGE, ls in SEASON, ld in DAYTYPE, lh in DAILYTIMEBRACKET, y in YEAR}: 
	sum{t in TECHNOLOGY, m in MODE_OF_OPERATION, l in TIMESLICE:TechnologyToStorage[r,t,s,m]>0} 
    RateOfActivity[r,l,t,m,y] 
    * TechnologyToStorage[r,t,s,m] 
    * Conversionls[l,ls] 
    * Conversionld[l,ld] 
    * Conversionlh[l,lh] 
    = RateOfStorageCharge[r,s,ls,ld,lh,y];"""
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
    """s.t. S2_RateOfStorageDischarge{r in REGION, s in STORAGE, ls in SEASON, ld in DAYTYPE, lh in DAILYTIMEBRACKET, y in YEAR}: 
	sum{t in TECHNOLOGY, m in MODE_OF_OPERATION, l in TIMESLICE:TechnologyFromStorage[r,t,s,m]>0} 
    RateOfActivity[r,l,t,m,y] 
    * TechnologyFromStorage[r,t,s,m] 
    * Conversionls[l,ls] 
    * Conversionld[l,ld] 
    * Conversionlh[l,lh] 
    = RateOfStorageDischarge[r,s,ls,ld,lh,y];
    """    
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
    """s.t. S3_NetChargeWithinYear{r in REGION, s in STORAGE, ls in SEASON, ld in DAYTYPE, lh in DAILYTIMEBRACKET, y in YEAR}: 
	sum{l in TIMESLICE:Conversionls[l,ls]>0&&Conversionld[l,ld]>0&&Conversionlh[l,lh]>0}  
    (RateOfStorageCharge[r,s,ls,ld,lh,y] - 
    RateOfStorageDischarge[r,s,ls,ld,lh,y]) 
    * YearSplit[l,y] 
    * Conversionls[l,ls] 
    * Conversionld[l,ld] 
    * Conversionlh[l,lh] 
    = NetChargeWithinYear[r,s,ls,ld,lh,y];
    """
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
    """s.t. S4_NetChargeWithinDay{r in REGION, s in STORAGE, ls in SEASON, ld in DAYTYPE, lh in DAILYTIMEBRACKET, y in YEAR}: 
	(RateOfStorageCharge[r,s,ls,ld,lh,y] 
    - RateOfStorageDischarge[r,s,ls,ld,lh,y]) 
    * DaySplit[lh,y] 
    = NetChargeWithinDay[r,s,ls,ld,lh,y];
    """
    return (
        (model.v_RateOfStorageCharge[r,s,ls,ld,lh,y]
        -model.v_RateOfStorageDischarge[r,s,ls,ld,lh,y])
        *model.p_DaySplit[lh,y] 
        == model.v_NetChargeWithinDay[r,s,ls,ld,lh,y]
    )
def S5_and_S6_StorageLevelYearStart(model,r,s,y):
    """s.t. S5_and_S6_StorageLevelYearStart{r in REGION, s in STORAGE, y in YEAR}: 
    if y = min{yy in YEAR} min(yy) then StorageLevelStart[r,s] 
												
    else 
        StorageLevelYearStart[r,s,y-1] + sum{ls in SEASON, ld in DAYTYPE, lh in DAILYTIMEBRACKET} 
    NetChargeWithinYear[r,s,ls,ld,lh,y-1]
    = StorageLevelYearStart[r,s,y];

    """
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
    """s.t. S7_and_S8_StorageLevelYearFinish{r in REGION, s in STORAGE, y in YEAR}: 
    if y < max{yy in YEAR} max(yy) then StorageLevelYearStart[r,s,y+1]
	else StorageLevelYearStart[r,s,y] + sum{ls in SEASON, ld in DAYTYPE, lh in DAILYTIMEBRACKET} 
    NetChargeWithinYear[r,s,ls,ld,lh,y] = StorageLevelYearFinish[r,s,y];	
    """
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
def S9_and_S10_StorageLevelSeasonStart(model, r, s, ls, y):
    """s.t. S9_and_S10_StorageLevelSeasonStart{r in REGION, s in STORAGE, ls in SEASON, y in YEAR}: 
    if ls = min{lsls in SEASON} min(lsls) then StorageLevelYearStart[r,s,y] 
	else StorageLevelSeasonStart[r,s,ls-1,y] + sum{ld in DAYTYPE, lh in DAILYTIMEBRACKET} NetChargeWithinYear[r,s,ls-1,ld,lh,y] 
	= StorageLevelSeasonStart[r,s,ls,y];
    """
    if ls == min(model.SEASON):
        return model.v_StorageLevelYearStart[r, s, y] == model.v_StorageLevelSeasonStart[r, s, ls, y]
    else:
        return (model.v_StorageLevelSeasonStart[r, s, ls, y] == 
               model.v_StorageLevelSeasonStart[r, s, ls-1, y] 
               + sum(model.v_NetChargeWithinYear[r, s, ls-1, ld, lh, y] for ld in model.DAYTYPE for lh in model.DAILYTIMEBRACKET))
        
def S11_and_S12_StorageLevelDayTypeStart(model, r,s,ls,ld,y):
    """s.t. S11_and_S12_StorageLevelDayTypeStart{r in REGION, s in STORAGE, ls in SEASON, ld in DAYTYPE, y in YEAR}:
    if ld = min{ldld in DAYTYPE} min(ldld) then StorageLevelSeasonStart[r,s,ls,y]
    else StorageLevelDayTypeStart[r,s,ls,ld-1,y] + sum{lh in DAILYTIMEBRACKET} 
    NetChargeWithinDay[r,s,ls,ld-1,lh,y] * DaysInDayType[ls,ld-1,y]
    = StorageLevelDayTypeStart[r,s,ls,ld,y];
    """
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
    """s.t. S13_and_S14_and_S15_StorageLevelDayTypeFinish{r in REGION, s in STORAGE, ls in SEASON, ld in DAYTYPE, y in YEAR}:	
    if ls = max{lsls in SEASON} max(lsls) && ld = max{ldld in DAYTYPE} max(ldld) then StorageLevelYearFinish[r,s,y] 
	
    else if ld = max{ldld in DAYTYPE} max(ldld) then StorageLevelSeasonStart[r,s,ls+1,y]
	
    else StorageLevelDayTypeFinish[r,s,ls,ld+1,y] - sum{lh in DAILYTIMEBRACKET} NetChargeWithinDay[r,s,ls,ld+1,lh,y] * DaysInDayType[ls,ld+1,y]
    = StorageLevelDayTypeFinish[r,s,ls,ld,y]
    """
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
def S16_StorageLevel(model, r, s, ls, ld,lh, y):
    """
    s.t. S16_StorageLevel{r in REGION, s in STORAGE, ls in SEASON, ld in DAYTYPE, lh in DAILYTIMEBRACKET, y in YEAR}: 
    if lh = min{lhlh in DAILYTIMEBRACKET} min(lhlh) then StorageLevelDayTypeStart[r,s,ls,ld,y]
    else if lh = max{lhlh in DAILYTIMEBRACKET} max(lhlh) then StorageLevelDayTypeFinish[r,s,ls,ld,y]
= StorageLevel[r,s,ls,ld,lh,y];"""
    if lh == min(model.DAILYTIMEBRACKET):
        return(
            model.v_StorageLevel[r, s, ls, ld, lh, y] == model.v_StorageLevelDayTypeStart[r, s, ls, ld, y]
        )
    elif lh == max(model.DAILYTIMEBRACKET):
        return(
            model.v_StorageLevel[r, s, ls, ld, lh, y] == model.v_StorageLevelDayTypeFinish[r, s, ls, ld, y]
            )
    else:
        return Constraint.Skip


    
    
    
    
    