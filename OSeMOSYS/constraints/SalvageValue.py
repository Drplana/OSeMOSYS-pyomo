from OSeMOSYS.constraints.AnnuityCFR import _crf, _pv_annuity

"""Salvage Value:
Calculates the fraction of the initial capital cost that can 
be recouped at the end of a technologies operational life. 
The salvage value can be calculated using one of two depreciation methods:
 straight line and sinking fund."""

# def SV123_SalvageValueAtEndOfPeriod1(model, r,t,y):
#     """
#     s.t. SV1_SalvageValueAtEndOfPeriod1{r in REGION, t in TECHNOLOGY, y in YEAR: 
#     DepreciationMethod[r]=1 && (y + OperationalLife[r,t]-1) > (max{yy in YEAR} max(yy)) && DiscountRate[r]>0}: 
#         SalvageValue[r,t,y] =
#         CapitalCost[r,t,y]*NewCapacity[r,t,y]*(1-(((1+DiscountRate[r])^(max{yy in YEAR} max(yy) - y+1)-1)/((1+DiscountRate[r])^OperationalLife[r,t]-1)));
    
#     s.t. SV2_SalvageValueAtEndOfPeriod2{r in REGION, t in TECHNOLOGY, y in YEAR: 
#         (DepreciationMethod[r]=1 && (y + OperationalLife[r,t]-1) > (max{yy in YEAR} max(yy)) && DiscountRate[r]=0) 
#         || (DepreciationMethod[r]=2 && (y + OperationalLife[r,t]-1) > (max{yy in YEAR} max(yy)))}: 
#             SalvageValue[r,t,y] = CapitalCost[r,t,y]*NewCapacity[r,t,y]*(1-(max{yy in YEAR} max(yy) - y+1)/OperationalLife[r,t]); 
    
#     s.t. SV3_SalvageValueAtEndOfPeriod3{r in REGION, t in TECHNOLOGY, y in YEAR: 
#         (y + OperationalLife[r,t]-1) <= (max{yy in YEAR} max(yy))}: SalvageValue[r,t,y] = 0;
    
#     """
#     if (model.p_DepreciationMethod[r]==1 and ((y + model.p_OperationalLife[r,t]-1) > max(model.YEAR)) and model.p_DiscountRate[r] > 0 ):
#         return(
#         model.v_SalvageValue[r,t,y]
#         == model.v_NewCapacity[r,t,y]
#         *  model.p_CapitalCost[r,t,y]
#         *(1- (
#             ((1+model.p_DiscountRate[r])**(max(model.YEAR)-y+1)-1)
#             /((1+model.p_DiscountRate[r])**model.p_OperationalLife[r,t]-1))
#              )
#         )  
#     elif (
#         model.p_DepreciationMethod[r] == 1
#         and ((y+ model.p_OperationalLife[r,t] - 1) > max(model.YEAR))
#         and model.p_DiscountRate[r] == 0
#         or (model.p_DepreciationMethod[r] == 2
#         and (y+model.p_OperationalLife[r,t]-1) > max(model.YEAR))
#     ): return(
#         model.v_SalvageValue[r,t,y]
#         == model.v_NewCapacity[r,t,y]
#         *  model.p_CapitalCost[r,t,y]
#         *  (1-(max(model.YEAR)-y+1)/model.p_OperationalLife[r,t])            
#             )
#     else: 
#         return(
#         #if (y + Operationallife[r,t]-1)<= max(Year)
#         model.v_SalvageValue[r,t,y] == 0
#             )
# def SV123_SalvageValueAtEndOfPeriod1(model, r, t, y):
#     """
#     Mantiene la misma estructura original:
#       - Caso 1: DepreciationMethod=1 y DiscountRate>0  -> fórmula "geométrica"
#       - Caso 2: (DepreciationMethod=1 y dr=0) o (DepreciationMethod=2) -> "lineal"
#       - Caso 3: en otro caso, salvage = 0
#     Ahora se suman además los términos de recuperación con L_rec = p_VidaUtilRecuperada[r,t].
#     """
#     y_max = max(model.YEAR)
#     dr    = model.p_DiscountRate[r]
#     dep   = model.p_DepreciationMethod[r]
#     L_new = model.p_OperationalLife[r, t]
#     L_rec = model.p_VidaUtilRecuperada[r, t]
#     usados = y_max - y + 1  # años usados dentro del horizonte a partir de y
#     unitcap = model.p_CapacityOfOneTechnologyUnit[r, t, min(model.YEAR)]

#     # Helpers: factores de salvage (0 si no sobrevive más allá del horizonte)
#     def salvage_factor_geom(L):
#         if (y + L - 1) <= y_max:
#             return 0.0
#         # 1 - ((1+dr)^usados - 1)/((1+dr)^L - 1)
#         return 1.0 - (((1 + dr)**usados - 1.0) / ((1 + dr)**L - 1.0))

#     def salvage_factor_linear(L):
#         if (y + L - 1) <= y_max:
#             return 0.0
#         # 1 - usados/L
#         return 1.0 - (usados / L)

#     # Construimos el salvage sumando NUEVA + RECUPERADA según el caso
#     if (dep == 1) and ((y + L_new - 1) > y_max) and (dr > 0):
#         # Caso 1: geométrico (dr>0). OJs
#         sf_new = salvage_factor_geom(L_new)
#         sf_rec = salvage_factor_geom(L_rec)

#         return (
#             model.v_SalvageValue[r, t, y]
#             ==
#             # NUEVA
#             model.v_NewCapacity[r, t, y]          * model.p_CapitalCost[r, t, y]        * sf_new
#             # RECUPERADA: de NUEVA
#           + model.v_RecoveredNewCapacity[r, t, y] * model.p_CostoRecuperacion[r, t, y]  * sf_rec
#             # RECUPERADA: de RESIDUAL/EXISTENTE (kW)
#           + model.v_RecoveredCapacity[r, t, y]    * model.p_CostoRecuperacion[r, t, y]  * sf_rec
#             # RECUPERADA: por UNIDADES -> convertir a kW
#           + model.v_RecoveredExistingUnits[r, t, y] * unitcap * model.p_CostoRecuperacion[r, t, y] * sf_rec
#         )

#     elif (
#         (dep == 1 and (y + L_new - 1) > y_max and dr == 0)
#         or (dep == 2 and (y + L_new - 1) > y_max)
#     ):
#         # Caso 2: lineal (dr=0 o método 2). Para recuperación, misma lógica con L_rec.
#         sf_new = salvage_factor_linear(L_new)
#         sf_rec = salvage_factor_linear(L_rec)

#         return (
#             model.v_SalvageValue[r, t, y]
#             ==
#             model.v_NewCapacity[r, t, y]          * model.p_CapitalCost[r, t, y]        * sf_new
#           + model.v_RecoveredNewCapacity[r, t, y] * model.p_CostoRecuperacion[r, t, y]  * sf_rec
#           + model.v_RecoveredCapacity[r, t, y]    * model.p_CostoRecuperacion[r, t, y]  * sf_rec
#           + model.v_RecoveredExistingUnits[r, t, y] * unitcap * model.p_CostoRecuperacion[r, t, y] * sf_rec
#         )

#     else:
#         # Caso 3: si el activo (nuevo) no sobrevive, pones 0.
#         return (model.v_SalvageValue[r, t, y] == 0)


def SV123_SalvageValueAtEndOfPeriod1(model, r, t, y):
    """
    Igual a tu estructura:
      SV1: Dep=1 y dr>0 -> geométrica
      SV2: (Dep=1 y dr=0) o Dep=2 -> lineal
      SV3: si no sobrevive -> 0
    Aplicado a NUEVA y a RECUPERADA (con L_rec).
    """
    y0   = model.YEAR.first()
    yL   = model.YEAR.last()
    dr   = model.p_DiscountRate[r]
    dep  = model.p_DepreciationMethod[r]
    L_new = int(model.p_OperationalLife[r, t])
    L_rec = int(model.p_VidaUtilRecuperada[r, t])
    used = yL - y + 1
    unitcap = model.p_CapacityOfOneTechnologyUnit[r, t, y0]
    dr_idv = model.p_DiscountRateIdv[r, t]

    CRF_new = _crf(L_new, dr_idv)
    PV_new  = _pv_annuity(L_new, dr)
    if L_rec > 0:
        CRF_rec = _crf(L_rec, dr_idv); PV_rec = _pv_annuity(L_rec, dr)
    else:
        CRF_rec = 0.0; PV_rec = 0.0

    # CRF_rec = _crf(L_rec, dr_idv)
    # PV_rec  = _pv_annuity(L_rec, dr)

    def frac_geom(L):
        if y + L - 1 <= yL: return 0.0
        return 1.0 - (((1 + dr)**used - 1.0) / ((1 + dr)**L - 1.0))

    def frac_lin(L):
        if y + L - 1 <= yL: return 0.0
        return 1.0 - (used / L)

    if (dep == 1) and (y + L_new - 1 > yL) and (dr > 0):
        f_new = frac_geom(L_new)
        f_rec = frac_geom(L_rec)
        return (
            model.v_SalvageValue[r, t, y]
            ==
            # NUEVA
            model.v_NewCapacity[r, t, y]          * model.p_CapitalCost[r, t, y]       * CRF_new * PV_new * f_new
            # RECUPERADA
          + model.v_RecoveredNewCapacity[r, t, y] * model.p_CostoRecuperacion[r, t, y] * CRF_rec * PV_rec * f_rec
          + model.v_RecoveredCapacity[r, t, y]    * model.p_CostoRecuperacion[r, t, y] * CRF_rec * PV_rec * f_rec
          + model.v_RecoveredExistingUnits[r, t, y] * unitcap * model.p_CostoRecuperacion[r, t, y] * CRF_rec * PV_rec * f_rec
        )

    elif ((dep == 1 and (y + L_new - 1 > yL) and dr == 0) or (dep == 2 and (y + L_new - 1 > yL))):
        f_new = frac_lin(L_new)
        f_rec = frac_lin(L_rec)
        return (
            model.v_SalvageValue[r, t, y]
            ==
            model.v_NewCapacity[r, t, y]          * model.p_CapitalCost[r, t, y]       * CRF_new * PV_new * f_new
          + model.v_RecoveredNewCapacity[r, t, y] * model.p_CostoRecuperacion[r, t, y] * CRF_rec * PV_rec * f_rec
          + model.v_RecoveredCapacity[r, t, y]    * model.p_CostoRecuperacion[r, t, y] * CRF_rec * PV_rec * f_rec
          + model.v_RecoveredExistingUnits[r, t, y] * unitcap * model.p_CostoRecuperacion[r, t, y] * CRF_rec * PV_rec * f_rec
        )

    else:
        return (model.v_SalvageValue[r, t, y] == 0)    

def SV4_SalvageValueDiscountedToStarYear(model, r,t,y):
    """
s.t. SV4_SalvageValueDiscountedToStartYear{r in REGION, t in TECHNOLOGY, y in YEAR}: 
DiscountedSalvageValue[r,t,y] = SalvageValue[r,t,y]/((1+DiscountRate[r])^(1+max{yy in YEAR} max(yy)-min{yy in YEAR} min(yy)));
    """    
    # return (
    #     model.v_DiscountedSalvageValue[r,t,y]
    #     == model.v_SalvageValue[r,t,y]
    #     / (1+model.p_DiscountRate[r])**(1+max(model.YEAR)-min(model.YEAR))
    # )
    y0 = model.YEAR.first()
    yL = model.YEAR.last()
    return (
        model.v_DiscountedSalvageValue[r, t, y]
        == model.v_SalvageValue[r, t, y] / (1 + model.p_DiscountRate[r])**(1 + (yL - y0))
    )

