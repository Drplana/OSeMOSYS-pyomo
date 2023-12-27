"""Emissions"""
def E1_AnnualEmissionProductionByMode(model,r,t,e,m,y):
    return (
        model.p_EmissionActivityRatio[r,t,e,m,y]
        *model.v_TotalAnnualTechnologyActivityByMode[r,t,m,y]
        == model.v_AnnualTechnologyEmissionByMode[r,t,e,m,y]
    )
def E2_AnnualEmissionProduction(model, r,t,e,y):
    return (
        sum(model.v_AnnualTechnologyEmissionByMode[r,t,e,m,y]
            for m in model.MODE_OF_OPERATION)
        ==model.v_AnnualTechnologyEmission[r,t,e,y]
    )
def E3_EmissionsPenaltyByTechAndEmission(model,r,t,e,y):
    return (
        model.v_AnnualTechnologyEmission[r,t,e,y]
        *model.p_EmissionsPenalty[r,e,y]
        ==model.v_AnnualTechnologyEmissionPenaltyByEmission[r,t,e,y]
    )
def E4_EmissionsPenaltyByTechnology(model, r,t,y):
    return(
        sum(model.v_AnnualTechnologyEmissionPenaltyByEmission[r,t,e,y]
            for e in model.EMISSION)
        == model.v_AnnualTechnologyEmissionsPenalty[r,t,y]
    )
def E5_DiscountedEmissionsPenaltyByTechnology(model,r,t,y):
    return(
        model.v_AnnualTechnologyEmissionsPenalty[r,t,y]
        /(1+model.p_DiscountRate[r])**(y-min(model.YEAR)+0.5)
        == model.v_DiscountedTechnologyEmissionsPenalty[r,t,y]
    )
def E6_EmissionsAccounting1(model, r,e,y):
    return (
        sum(model.v_AnnualTechnologyEmission[r,t,e,y]
            for t in model.TECHNOLOGY)
        == model.v_AnnualEmissions[r,e,y]
    )
def E7_EmissionsAccounting2(model, r,e):
    return(
        sum(
            model.v_AnnualEmissions[r,e,y]
            for y in model.YEAR
        )
        ==model.v_ModelPeriodEmissions[r,e]-model.p_ModelPeriodExogenousEmission[r,e]
    )
def E8_AnnualEmissionsLimit(model,r,e,y):
    return (
        model.v_AnnualEmissions[r,e,y]
        +model.p_AnnualExogenousEmission[r,e,y]
        <= model.p_AnnualEmissionLimit[r,e,y]
    )
def E9_ModelPeriodEmissionsLimit(model,r,e):
    return (model.v_ModelPeriodEmissions[r,e]
            <= model.p_ModelPeriodEmissionLimit[r,e]
            )
    