"""RE Production Target:
Ensures that production from technologies tagged as renewable energy "
technologies (RETagTechnology = 1) is at least equal to the user-defined
renewable energy (RE) target."""

def RE1_FuelProductionByTechnologyAnnual(model, r,t,f,y):
    return (
            sum(model.v_ProductionByTechnology[r,l,t,f,y] for l in model.TIMESLICE)
            == model.v_ProductionByTechnologyAnnual[r,t,f,y]
        )
def RE2_TechIncluded(model, r,y):
    return(
                sum(model.v_ProductionByTechnologyAnnual[r,t,f,y]
                *model.p_RETagTechnology[r,t,y] for t in model.TECHNOLOGY
                for f in model.FUEL
                )
                == model.v_TotalREProductionAnnual[r,y]
            )
def RE3_FuelIncluded(model, r,y):
    return (
                sum(model.v_RateOfProduction[r,l,f,y]
                *model.p_YearSplit[l,y]
                *model.p_RETagFuel[r,f,y] 
                for l in model.TIMESLICE
                for f in model.FUEL)
                ==model.v_RETotalProductionOfTargetFuelAnnual[r,y]
            )
def RE4_EnergyConstraint(model, r,y):
    return (
        model.v_RETotalProductionOfTargetFuelAnnual[r,y]
        *model.p_REMinProductionTarget[r,y]
        <= model.v_TotalREProductionAnnual[r,y]
    )
def RE5_FuelUseByTechnologyAnnual(model, r,t,f,y):
    return (
            sum(model.v_RateOfUseByTechnology[r,l,t,f,y]
            *model.p_YearSplit[l,y] for l in model.TIMESLICE)
            == model.v_UseByTechnologyAnnual[r,t,f,y]
        )

