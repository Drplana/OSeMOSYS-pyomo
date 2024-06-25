"""Storage Constraints"""
from pyomo.environ import * 
def SC1_LowerLimit_BeginningOfDailyTimeBracketOfFirstInstanceOfDayTypeInFirstWeekConstraint(model,r,s,ls,ld,lh,y):
    """.t. SC1_LowerLimit_BeginningOfDailyTimeBracketOfFirstInstanceOfDayTypeInFirstWeekConstraint{r in REGION, s in STORAGE, ls in SEASON, ld in DAYTYPE, lh in DAILYTIMEBRACKET, y in YEAR}: 
	0 <= (StorageLevelDayTypeStart[r,s,ls,ld,y]+sum{lhlh in DAILYTIMEBRACKET:lh-lhlh>0} NetChargeWithinDay[r,s,ls,ld,lhlh,y])-StorageLowerLimit[r,s,y];
    """
    return (
        0 
        <= (model.v_StorageLevelDayTypeStart[r,s,ls,ld,y]
        +sum(model.v_NetChargeWithinDay[r,s,ls,ld,lhlh,y]
             for lhlh in model.DAILYTIMEBRACKET if (lh-lhlh>0)
             ))
        -model.v_StorageLowerLimit[r,s,y]
    )
def SC1_UpperLimit_BeginningOfDailyTimeBracketOfFirstInstanceOfDayTypeInFirstWeekConstraint(model,r,s,ls,ld,lh,y):
    """
s.t. SC1_UpperLimit_BeginningOfDailyTimeBracketOfFirstInstanceOfDayTypeInFirstWeekConstraint{r in REGION, s in STORAGE, ls in SEASON, ld in DAYTYPE, lh in DAILYTIMEBRACKET, y in YEAR}: 
	(StorageLevelDayTypeStart[r,s,ls,ld,y]+sum{lhlh in DAILYTIMEBRACKET:lh-lhlh>0} NetChargeWithinDay[r,s,ls,ld,lhlh,y])-StorageUpperLimit[r,s,y] <= 0;"""
    return (
        (model.v_StorageLevelDayTypeStart[r,s,ls,ld,y]
        +sum(model.v_NetChargeWithinDay[r,s,ls,ld,lhlh,y]
             for lhlh in model.DAILYTIMEBRACKET if (lh-lhlh>0)))
        -model.v_StorageUpperLimit[r,s,y]
        <=0
    )
def SC2_LowerLimit_EndOfDailyTimeBracketOfLastInstanceOfDayTypeInFirstWeekConstraint(model,r,s,ls,ld,lh,y):
    """s.t. SC2_LowerLimit_EndOfDailyTimeBracketOfLastInstanceOfDayTypeInFirstWeekConstraint{r in REGION, s in STORAGE, ls in SEASON, ld in DAYTYPE, lh in DAILYTIMEBRACKET, y in YEAR}: 
	0 <= if ld > min{ldld in DAYTYPE} min(ldld) then (StorageLevelDayTypeStart[r,s,ls,ld,y]-sum{lhlh in DAILYTIMEBRACKET:lh-lhlh<0} NetChargeWithinDay[r,s,ls,ld-1,lhlh,y])-StorageLowerLimit[r,s,y];"""
    if ld > min(model.DAYTYPE):
        return(0
        <= (
            (model.v_StorageLevelDayTypeStart[r,s,ls,ld,y]
            -sum (model.v_NetChargeWithinDay[r,s,ls,ld-1,lhlh,y]
                  for lhlh in model.DAILYTIMEBRACKET if (lh-lhlh<0)))
            -model.v_StorageLowerLimit[r,s,y]
            )
    )
    else: return Constraint.Skip
def SC2_UpperLimit_EndOfDailyTimeBracketOfLastInstanceOfDayTypeInFirstWeekConstraint(model,r,s,ls,ld,lh,y):
    if ld >  min(model.DAYTYPE):
        return (
            (model.v_StorageLevelDayTypeStart[r,s,ls,ld,y]
             -sum(model.v_NetChargeWithinDay[r,s,ls,ld-1,lhlh,y] 
                  for lhlh in model.DAILYTIMEBRACKET if (lh-lhlh<0)))
            -model.v_StorageUpperLimit[r,s,y] <= 0 
        )
    else: return Constraint.Skip
def SC3_LowerLimit_EndOfDailyTimeBracketOfLastInstanceOfDayTypeInLastWeekConstraint(model,r,s,ls,ld,lh,y):
    return (
        0
        <= (
            model.v_StorageLevelDayTypeFinish[r,s,ls,ld,y]
            -sum(model.v_NetChargeWithinDay[r,s,ls,ld,lhlh,y] 
                 for lhlh in  model.DAILYTIMEBRACKET if (lh - lhlh<0))
            -model.v_StorageLowerLimit[r,s,y]
        )
    )
def SC3_UpperLimit_EndOfDailyTimeBracketOfLastInstanceOfDayTypeInLastWeekConstraint(model,r,s,ls,ld,lh,y):
    return (
    (
        model.v_StorageLevelDayTypeFinish[r,s,ls,ld,y]
        -sum(model.v_NetChargeWithinDay[r,s,ls,ld,lhlh,y]
             for lhlh in model.DAILYTIMEBRACKET
             if lh-lhlh<0)
     
    )
    -model.v_StorageUpperLimit[r,s,y]
    <=0    
    )

def SC4_LowerLimit_BeginningOfDailyTimeBracketOfFirstInstanceOfDayTypeInLastWeekConstraint(model,r,s,ls,ld,lh,y):
    """s.t. SC4_LowerLimit_BeginningOfDailyTimeBracketOfFirstInstanceOfDayTypeInLastWeekConstraint{r in REGION, s in STORAGE, ls in SEASON, ld in DAYTYPE, lh in DAILYTIMEBRACKET, y in YEAR}: 	
    0 <= if ld > min{ldld in DAYTYPE} min(ldld) then (StorageLevelDayTypeFinish[r,s,ls,ld-1,y]+sum{lhlh in DAILYTIMEBRACKET:lh-lhlh>0} NetChargeWithinDay[r,s,ls,ld,lhlh,y])-StorageLowerLimit[r,s,y]; 
    """
    if ld > min(model.DAYTYPE):
        return (
            0
            <=(
            model.v_StorageLevelDayTypeFinish[r,s,ls,ld-1,y]
                +sum(model.v_NetChargeWithinDay[r,s,ls,ld,lhlh,y]
                     for lhlh in model.DAILYTIMEBRACKET
                     if (lh-lhlh>0)))
                -model.v_StorageUpperLimit[r,s,y]
                )
    else: return Constraint.Skip
def SC4_UpperLimit_BeginningOfDailyTimeBracketOfFirstInstanceOfDayTypeInLastWeekConstraint(model,r,s,ls,ld,lh,y):
    if ld > min(model.DAYTYPE):
        return(
        (model.v_StorageLevelDayTypeFinish[r,s,ls,ld-1,y]
        +sum(model.v_NetChargeWithinDay[r,s,ls,ld,lhlh,y]
             for lhlh in model.DAILYTIMEBRACKET
             if (lh-lhlh>0)))
        -model.v_StorageUpperLimit[r,s,y]
        <=0
        
    )
    else: return Constraint.Skip   
def SC5_MaxChargeConstraint(model,r,s,ls,ld,lh,y):
    return (
        model.v_RateOfStorageCharge[r,s,ls,ld,lh,y]
        <=model.p_StorageMaxChargeRate[r,s]
    )
def SC6_MaxDischargeConstraint(model,r,s,ls,ld,lh,y):
    return (
        model.v_RateOfStorageDischarge[r,s,ls,ld,lh,y]
        <= model.p_StorageMaxDischargeRate[r,s]
    )

    
            