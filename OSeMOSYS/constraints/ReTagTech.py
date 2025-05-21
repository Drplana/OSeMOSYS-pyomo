"""RE Production Target:
Ensures that production from technologies tagged as renewable energy "
technologies (RETagTechnology = 1) is at least equal to the user-defined
renewable energy (RE) target."""
RE_AtLeast = 0

def RE1_FuelProductionByTechnologyAnnual(model, r, t, f, y):
    """
s.t. RE1_FuelProductionByTechnologyAnnual{r in REGION, t in TECHNOLOGY, f in FUEL, y in YEAR}: 
sum{l in TIMESLICE} ProductionByTechnology[r,l,t,f,y] = ProductionByTechnologyAnnual [r,t,f,y];
    """    
    return (
            sum(model.v_ProductionByTechnology[r,l,t,f,y] for l in model.TIMESLICE)
            == model.v_ProductionByTechnologyAnnual[r,t,f,y]
        )
def RE2_TechIncluded(model, r,y):
    """
s.t. RE2_TechIncluded{r in REGION, y in YEAR}: sum{t in TECHNOLOGY, f in FUEL}
ProductionByTechnologyAnnual[r,t,f,y]*RETagTechnology[r,t,y] = TotalREProductionAnnual[r,y];
There is an if included to save memory
    """ 
    return(
            sum(model.v_ProductionByTechnologyAnnual[r,t,f,y]
            *model.p_RETagTechnology[r,t,y] for t in model.TECHNOLOGY
            for f in model.FUEL #if model.p_RETagTechnology[r,t,y] != 0
            )
            == model.v_TotalREProductionAnnual[r,y]
            )
def RE3_FuelIncluded(model, r,y):
    """
s.t. RE3_FuelIncluded{r in REGION, y in YEAR}: sum{l in TIMESLICE, f in FUEL} 
RateOfProduction[r,l,f,y]*YearSplit[l,y]*RETagFuel[r,f,y] = RETotalProductionOfTargetFuelAnnual[r,y]; 
    """    
    return (
                sum(model.v_RateOfProduction[r,l,f,y]
                *model.p_YearSplit[l,y]
                *model.p_RETagFuel[r,f,y] 
                for l in model.TIMESLICE
                for f in model.FUEL) #if model.p_RETagFuel[r,f,y] != 0)
                ==model.v_RETotalProductionOfTargetFuelAnnual[r,y]
            )
def RE4_EnergyConstraint(model, r,y):
    """
s.t. RE4_EnergyConstraint{r in REGION, y in YEAR}:
REMinProductionTarget[r,y]*RETotalProductionOfTargetFuelAnnual[r,y] <= TotalREProductionAnnual[r,y];
    """
    if RE_AtLeast==1:
        return (
        model.v_RETotalProductionOfTargetFuelAnnual[r,y]
        *model.p_REMinProductionTarget[r,y]
        <= model.v_TotalREProductionAnnual[r,y]
    )
    else:
        return (
        model.v_RETotalProductionOfTargetFuelAnnual[r,y]
        *model.p_REMinProductionTarget[r,y]
        >= model.v_TotalREProductionAnnual[r,y] )

def RE5_FuelUseByTechnologyAnnual(model, r,t,f,y):
    """
s.t. RE5_FuelUseByTechnologyAnnual{r in REGION, t in TECHNOLOGY, f in FUEL, y in YEAR}: 
sum{l in TIMESLICE} RateOfUseByTechnology[r,l,t,f,y]*YearSplit[l,y] = UseByTechnologyAnnual[r,t,f,y];
    """    
    return (
            sum(model.v_RateOfUseByTechnology[r,l,t,f,y]
            *model.p_YearSplit[l,y] for l in model.TIMESLICE)
            == model.v_UseByTechnologyAnnual[r,t,f,y]
        )

