from OSeMOSYS.constraints.AnnuityCFR import _crf, _pv_annuity
"""Capital Costs
Calculates the total discounted capital cost 
expenditure for each technology in each year."""


# def CC1_UndiscountedCapitalInvestment(model, r,t,y):
#     """
# s.t. CC1_UndiscountedCapitalInvestment{r in REGION, t in TECHNOLOGY, y in YEAR}: 
# CapitalCost[r,t,y] * NewCapacity[r,t,y] = CapitalInvestment[r,t,y];
#     """    
#     return (
#         model.v_NewCapacity[r,t,y]*model.p_CapitalCost[r,t,y] 
#         + model.v_RecoveredExistingUnits[r,t,y]*model.p_CostoRecuperacion[r,t,y]*model.p_CapacityOfOneTechnologyUnit[r,t,min(model.YEAR)]
#         + model.v_RecoveredCapacity[r,t,y]*model.p_CostoRecuperacion[r,t,y]
#         + model.v_RecoveredNewCapacity[r,t,y]*model.p_CostoRecuperacion[r,t,y]
#         == model.v_CapitalInvestment[r,t,y]
#     )
# def CC2_DiscountingCapitalInvestment(model, r,t,y):
#     """
# s.t. CC2_DiscountingCapitalInvestment{r in REGION, t in TECHNOLOGY, y in YEAR}: 
# CapitalInvestment[r,t,y]/((1+DiscountRate[r])^(y-min{yy in YEAR} min(yy))) = 
# DiscountedCapitalInvestment[r,t,y];
#     """    
#     return (
#         model.v_CapitalInvestment[r,t,y]
#         /((1 + model.p_DiscountRate[r])**(y-min(model.YEAR)))
#         == model.v_DiscountedCapitalInvestment[r,t,y]
#     )
    

def CC1_UndiscountedCapitalInvestment(model, r,t,y):
    """
    CapitalInvestment[r,t,y] = Sum(capital-like costs in y, undiscounted)
    = New * Capex * CRF_new * PV_new  +  Recover* CostRec * CRF_rec * PV_rec
    """
    y0   = model.YEAR.first()
    L_new = int(model.p_OperationalLife[r, t])
    L_rec = int(model.p_VidaUtilRecuperada[r, t])
    dr    = model.p_DiscountRate[r]
    dr_idv = model.p_DiscountRateIdv[r, t]  # nuevo param (como en OSeMOSYS)
    unitcap = model.p_CapacityOfOneTechnologyUnit[r, t, y0]

    CRF_new = _crf(L_new, dr_idv)
    PV_new  = _pv_annuity(L_new, dr)

    if L_rec > 0:
        CRF_rec = _crf(L_rec, dr_idv)
        PV_rec  = _pv_annuity(L_rec, dr)
    else:
        CRF_rec = 0
        PV_rec  = 0

    return (
        model.v_CapitalInvestment[r, t, y]
        ==
        # NUEVA
        model.v_NewCapacity[r, t, y]             * model.p_CapitalCost[r, t, y]       * CRF_new * PV_new
        # RECUPERADA (kW directos)
      + model.v_RecoveredCapacity[r, t, y]       * model.p_CostoRecuperacion[r, t, y] * CRF_rec * PV_rec
      + model.v_RecoveredNewCapacity[r, t, y]    * model.p_CostoRecuperacion[r, t, y] * CRF_rec * PV_rec
        # RECUPERADA por UNIDADES -> kW
      + model.v_RecoveredExistingUnits[r, t, y]  * unitcap * model.p_CostoRecuperacion[r, t, y] * CRF_rec * PV_rec
    )
def CC2_DiscountingCapitalInvestment(model, r, t, y):
    """
    DiscountedCapitalInvestment = CapitalInvestment / DiscountFactor[r,y]
    (precalcula p_DiscountFactor[r,y] = (1+dr)^(y - y0) si tus periodos son anuales)
    """
    return model.v_DiscountedCapitalInvestment[r, t, y] == model.v_CapitalInvestment[r, t, y] / model.p_DiscountFactor[r, y]