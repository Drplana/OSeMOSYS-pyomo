"""
LaTeX equation mapping for OSeMOSYS Pyomo constraints.
Auto-generated and styled.
"""

EQUATION_LATEX_MAP = {
    "Acc1_FuelProductionByTechnology": r"""\begin{split}
 \textit{RateOfProductionByTechnology}_{r,l,t,f,y} \cdot \text{YearSplit}_{l,y} &= \textit{ProductionByTechnology}_{r,l,t,f,y}
\end{split}""",
    "Acc2_FuelUseByTechnology": r"""\begin{split}
 \textit{RateOfUseByTechnology}_{r,l,t,f,y} \cdot \text{YearSplit}_{l,y} &= \textit{UseByTechnology}_{r,l,t,f,y}
\end{split}""",
    "Acc3_AverageAnnualRateOfActivity": r"""\begin{split}
 \sum\limits_{l} \textit{RateOfActivity}_{r,l,t,m,y} \cdot \text{YearSplit}_{l,y} &= \textit{TotalAnnualTechnologyActivityByMode}_{r,t,m,y}
\end{split}""",
    "Acc4_ModelPeriodCostByRegion": r"""\begin{split}
 \sum\limits_{y} \textit{TotalDiscountedCost}_{r,y} &= \textit{ModelPeriodCostByRegion}_{r}
\end{split}""",
    "AAC1_TotalAnnualTechnologyActivity": r"""\begin{split}
 \sum\limits_{l} \textit{RateOfTotalActivity}_{r,t,l,y} \cdot \text{YearSplit}_{l,y} &= \textit{TotalTechnologyAnnualActivity}_{r,t,y}
\end{split}""",
    "AAC2_TotalAnnualTechnologyActivityUpperLimit": r"""\begin{split}
 \textit{TotalTechnologyAnnualActivity}_{r,t,y} &\leq \text{TotalTechnologyAnnualActivityUpperLimit}_{r,t,y}
\end{split}""",
    "AAC3_TotalAnnualTechnologyActivityLowerLimit": r"""\begin{split}
 \textit{TotalTechnologyAnnualActivity}_{r,t,y} &\geq \text{TotalTechnologyAnnualActivityLowerLimit}_{r,t,y}
\end{split}""",
    "TAC1_TotalModelHorizonTechnologyActivity": r"""\begin{split}
 \sum\limits_{y} \textit{TotalTechnologyAnnualActivity}_{r,t,y} &= \textit{TotalTechnologyModelPeriodActivity}_{r,t}
\end{split}""",
    "TAC2_TotalModelHorizonTechnologyActivityUpperLimit": r"""\begin{split}
 \textit{TotalTechnologyModelPeriodActivity}_{r,t} &\leq \text{TotalTechnologyModelPeriodActivityUpperLimit}_{r,t}
\end{split}""",
    "TAC3_TotalModelHorizenTechnologyActivityLowerLimit": r"""\begin{split}
 \textit{TotalTechnologyModelPeriodActivity}_{r,t} &\geq \text{TotalTechnologyModelPeriodActivityLowerLimit}_{r,t}
\end{split}""",
    "CAa1_TotalNewCapacity": r"""\begin{split}
 \textit{AccumulatedNewCapacity}_{r,t,y} &= \sum\limits_{yy \in YEAR: (y-yy < \text{OperationalLife}_{r,t}) \land (y-yy \geq 0)} \textit{NewCapacity}_{r,t,yy}
\end{split}""",
    "CAa2_TotalAnnualCapacity": r"""\begin{split}
 \textit{AccumulatedNewCapacity}_{r,t,y} &+ \textit{ResidualCapacity}_{r,t,y} \\
 &= \textit{TotalCapacityAnnual}_{r,t,y}
\end{split}""",
    "CAa1n_TotalResidualCapacity": r"""\begin{split}
 \textit{ResidualCapacity}_{r,t,y} &= \text{NumberOfExistingUnits}_{r,t,y} \cdot \text{CapacityOfOneTechnologyUnit}_{r,t,y}
\end{split}""",
    "CAa3_TotalActivityOfEachTechnology": r"""\begin{split}
 \sum\limits_{m} \textit{RateOfActivity}_{r,l,t,m,y} &= \textit{RateOfTotalActivity}_{r,t,l,y}
\end{split}""",
    "CAa4_ConstraintCapacity": r"""\begin{split}
 \textit{RateOfTotalActivity}_{r,t,l,y} &\leq \textit{TotalCapacityAnnual}_{r,t,y} \cdot \text{CapacityFactor}_{r,t,l,y} \cdot \text{CapacityToActivityUnit}_{r,t}
\end{split}""",
    "CAa5_TotalNewCapacity": r"""\begin{split}
 \text{CapacityOfOneTechnologyUnit}_{r,t,y} \cdot \textit{NumberOfNewTechnologyUnits}_{r,t,y} \cdot \text{Availability}_{r,t,y} &= \textit{NewCapacity}_{r,t,y}
\end{split}""",
    "CAb1_PlannedMaintenance": r"""\begin{split}
 \sum\limits_{l} \textit{RateOfTotalActivity}_{r,t,l,y} \cdot \text{YearSplit}_{l,y} &\leq \sum\limits_{l} ( \textit{TotalCapacityAnnual}_{r,t,y} \cdot \text{CapacityFactor}_{r,t,l,y} \cdot \text{YearSplit}_{l,y} \\
 &\quad \cdot \text{AvailabilityFactor}_{r,t,y} \cdot \text{CapacityToActivityUnit}_{r,t} )
\end{split}""",
    "CC1_UndiscountedCapitalInvestment": r"""\begin{split}
 \textit{CapitalInvestment}_{r,t,y} &= \textit{NewCapacity}_{r,t,y} \cdot \text{CapitalCost}_{r,t,y} \cdot CRF_{new} \cdot PV_{new} \\
 &+ \textit{RecoveredCapacity}_{r,t,y} \cdot \text{CostoRecuperacion}_{r,t,y} \cdot CRF_{rec} \cdot PV_{rec} \\
 &+ \textit{RecoveredNewCapacity}_{r,t,y} \cdot \text{CostoRecuperacion}_{r,t,y} \cdot CRF_{rec} \cdot PV_{rec} \\
 &+ \textit{RecoveredExistingUnits}_{r,t,y} \cdot \text{CapacityOfOneTechnologyUnit}_{r,t,y_0} \\
 &\quad \cdot \text{CostoRecuperacion}_{r,t,y} \cdot CRF_{rec} \cdot PV_{rec}
\end{split}""",
    "CC2_DiscountingCapitalInvestment": r"""\begin{split}
 \textit{DiscountedCapitalInvestment}_{r,t,y} &= \frac{\textit{CapitalInvestment}_{r,t,y}}{\text{DiscountFactor}_{r,y}}
\end{split}""",
    "E1_AnnualEmissionProductionByMode": r"""\begin{split}
 \text{EmissionActivityRatio}_{r,t,e,m,y} \cdot \textit{TotalAnnualTechnologyActivityByMode}_{r,t,m,y} &= \textit{AnnualTechnologyEmissionByMode}_{r,t,e,m,y}
\end{split}""",
    "E2_AnnualEmissionProduction": r"""\begin{split}
 \sum\limits_{m} \textit{AnnualTechnologyEmissionByMode}_{r,t,e,m,y} &= \textit{AnnualTechnologyEmission}_{r,t,e,y}
\end{split}""",
    "E3_EmissionsPenaltyByTechAndEmission": r"""\begin{split}
 \textit{AnnualTechnologyEmission}_{r,t,e,y} \cdot \text{EmissionsPenalty}_{r,e,y} &= \textit{AnnualTechnologyEmissionPenaltyByEmission}_{r,t,e,y}
\end{split}""",
    "E4_EmissionsPenaltyByTechnology": r"""\begin{split}
 \sum\limits_{e} \textit{AnnualTechnologyEmissionPenaltyByEmission}_{r,t,e,y} &= \textit{AnnualTechnologyEmissionsPenalty}_{r,t,y}
\end{split}""",
    "E5_DiscountedEmissionsPenaltyByTechnology": r"""\begin{split}
 \frac{\textit{AnnualTechnologyEmissionsPenalty}_{r,t,y}}{\text{DiscountFactorMid}_{r,y}} &= \textit{DiscountedTechnologyEmissionsPenalty}_{r,t,y}
\end{split}""",
    "E6_EmissionsAccounting1": r"""\begin{split}
 \sum\limits_{t} \textit{AnnualTechnologyEmission}_{r,t,e,y} &= \textit{AnnualEmissions}_{r,e,y}
\end{split}""",
    "E7_EmissionsAccounting2": r"""\begin{split}
 \sum\limits_{y} \textit{AnnualEmissions}_{r,e,y} &= \textit{ModelPeriodEmissions}_{r,e} - \text{ModelPeriodExogenousEmission}_{r,e}
\end{split}""",
    "E8_AnnualEmissionsLimit": r"""\begin{split}
 \textit{AnnualEmissions}_{r,e,y} + \text{AnnualExogenousEmission}_{r,e,y} &\leq \text{AnnualEmissionLimit}_{r,e,y}
\end{split}""",
    "E9_ModelPeriodEmissionsLimit": r"""\begin{split}
 \textit{ModelPeriodEmissions}_{r,e} &\leq \text{ModelPeriodEmissionLimit}_{r,e}
\end{split}""",
    "EBa1_RateOfFuelProduction1": r"""\begin{split}
 \textit{RateOfActivity}_{r,l,t,m,y} \cdot \text{OutputActivityRatio}_{r,t,f,m,y} &= \textit{RateOfProductionByTechnologyByMode}_{r,l,t,m,f,y}
\end{split}""",
    "EBa2_RateOfFuelProduction2": r"""\begin{split}
 \sum\limits_{m: \text{OutputActivityRatio}_{r,t,f,m,y} \neq 0} \textit{RateOfProductionByTechnologyByMode}_{r,l,t,m,f,y} &= \textit{RateOfProductionByTechnology}_{r,l,t,f,y}
\end{split}""",
    "EBa3_RateOfFuelProduction3": r"""\begin{split}
 \sum\limits_{t} \textit{RateOfProductionByTechnology}_{r,l,t,f,y} &= \textit{RateOfProduction}_{r,l,f,y}
\end{split}""",
    "EBa4_RateOfFuelUse1": r"""\begin{split}
 \textit{RateOfActivity}_{r,l,t,m,y} \cdot \text{InputActivityRatio}_{r,t,f,m,y} &= \textit{RateOfUseByTechnologyByMode}_{r,l,t,m,f,y}
\end{split}""",
    "EBa5_RateOfFuelUse2": r"""\begin{split}
 \sum\limits_{m: \text{InputActivityRatio}_{r,t,f,m,y} \neq 0} \textit{RateOfUseByTechnologyByMode}_{r,l,t,m,f,y} &= \textit{RateOfUseByTechnology}_{r,l,t,f,y}
\end{split}""",
    "EBa6_RateOfFuelUse3": r"""\begin{split}
 \sum\limits_{t} \textit{RateOfUseByTechnology}_{r,l,t,f,y} &= \textit{RateOfUse}_{r,l,f,y}
\end{split}""",
    "EBa7_EnergyBalanceEachTS1": r"""\begin{split}
 \textit{RateOfProduction}_{r,l,f,y} \cdot \text{YearSplit}_{l,y} &= \textit{Production}_{r,l,f,y}
\end{split}""",
    "EBa8_EnergyBalanceEachTS2": r"""\begin{split}
 \textit{RateOfUse}_{r,l,f,y} \cdot \text{YearSplit}_{l,y} &= \textit{Use}_{r,l,f,y}
\end{split}""",
    "EBa9_EnergyBalanceEachTS3": r"""\begin{split}
 \textit{RateOfDemand}_{r,l,f,y} \cdot \text{YearSplit}_{l,y} &= \textit{Demand}_{r,l,f,y}
\end{split}""",
    "EBa10_EnergyBalanceEachTS4": r"""\begin{split}
 \textit{Trade}_{r,rr,l,f,y} &= -\textit{Trade}_{rr,r,l,f,y}
\end{split}""",
    "EBa11_EnergyBalanceEachTS5": r"""\begin{split}
 \textit{Production}_{r,l,f,y} &\geq \textit{Demand}_{r,l,f,y} + \textit{Use}_{r,l,f,y} \\
 &+ \sum\limits_{rr} \textit{Trade}_{r,rr,l,f,y} \cdot \text{TradeRoute}_{r,rr,f,y} \\
 &+ \textit{Export}_{r,l,f,y}
\end{split}""",
    "EBb1_EnergyBalanceEachYear1": r"""\begin{split}
 \sum\limits_{l} \textit{Production}_{r,l,f,y} &= \textit{ProductionAnnual}_{r,f,y}
\end{split}""",
    "EBb2_EnergyBalanceEachYear2": r"""\begin{split}
 \sum\limits_{l} \textit{Use}_{r,l,f,y} &= \textit{UseAnnual}_{r,f,y}
\end{split}""",
    "EBb3_EnergyBalanceEachYear3": r"""\begin{split}
 \sum\limits_{l} \textit{Trade}_{r,rr,l,f,y} &= \textit{TradeAnnual}_{r,rr,f,y}
\end{split}""",
    "EBb4_EnergyBalanceEachYear4": r"""\begin{split}
 \textit{ProductionAnnual}_{r,f,y} &\geq \textit{UseAnnual}_{r,f,y} \\
 &+ \sum\limits_{rr} \textit{TradeAnnual}_{r,rr,f,y} \cdot \text{TradeRoute}_{r,rr,f,y} \\
 &+ \text{AccumulatedAnnualDemand}_{r,f,y}
\end{split}""",
    "TCC1_TotalAnnualMaxCapacityConstraint": r"""\begin{split}
 \textit{TotalCapacityAnnual}_{r,t,y} &\leq \text{TotalAnnualMaxCapacity}_{r,t,y}
\end{split}""",
    "TCC2_TotalAnnualMinCapacityConstraint": r"""\begin{split}
 \textit{TotalCapacityAnnual}_{r,t,y} &\geq \text{TotalAnnualMinCapacity}_{r,t,y}
\end{split}""",
    "NCC1_TotalAnnualMaxNewCapacityConstraint": r"""\begin{split}
 \textit{NewCapacity}_{r,t,y} &\leq \text{TotalAnnualMaxCapacityInvestment}_{r,t,y}
\end{split}""",
    "NCC2_TotalAnnualMinNewCapacityConstraint": r"""\begin{split}
 \textit{NewCapacity}_{r,t,y} &\geq \text{TotalAnnualMinCapacityInvestment}_{r,t,y}
\end{split}""",
    "Must_Run": r"""\begin{split}
 \textit{RateOfTotalActivity}_{r,t,l,y} &\geq \text{MustRunTech}_{r,t,y} \cdot \textit{TotalCapacityAnnual}_{r,t,y} \\
 &\quad \cdot \text{CapacityFactor}_{r,t,l,y} \cdot \text{CapacityToActivityUnit}_{r,t} \\
 &\quad \cdot \text{AvailabilityFactor}_{r,t,y}
\end{split}""",
    "ObjectiveFunction": r"""\begin{split}
 \sum\limits_{r, y} \textit{TotalDiscountedCost}_{r,y}
\end{split}""",
    "OC1_OperatingCostVariable": r"""\begin{split}
 \sum\limits_{m: \text{VariableCost}_{r,t,m,y} \neq 0} \textit{TotalAnnualTechnologyActivityByMode}_{r,t,m,y} \cdot \text{VariableCost}_{r,t,m,y} &= \textit{AnnualVariableOperatingCost}_{r,t,y}
\end{split}""",
    "OC2_OperatingCostsFixedAnnual": r"""\begin{split}
 \textit{TotalCapacityAnnual}_{r,t,y} \cdot \text{FixedCost}_{r,t,y} &= \textit{AnnualFixedOperatingCost}_{r,t,y}
\end{split}""",
    "OC3_OperatingCostsTotalAnnual": r"""\begin{split}
 \textit{AnnualFixedOperatingCost}_{r,t,y} + \textit{AnnualVariableOperatingCost}_{r,t,y} &= \textit{OperatingCost}_{r,t,y}
\end{split}""",
    "OC4_DiscountedOperatingCostsTotalAnnual": r"""\begin{split}
 \frac{\textit{OperatingCost}_{r,t,y}}{\text{DiscountFactorMid}_{r,y}} &= \textit{DiscountedOperatingCost}_{r,t,y}
\end{split}""",
    "Recovered_Existing_Units": r"""\begin{split}
 \textit{RecoveredExistingUnits}_{r,t,y} &\leq \text{NumberOfExistingUnits}_{r,t,y-1} \\
 &- \text{NumberOfExistingUnits}_{r,t,y} \\
 &+ \textit{RecoveredExistingUnits}_{r,t,y-\text{VidaUtilRecuperada}_{r,t}}
\end{split}""",
    "Accumulated_Recovered_Existing_Units": r"""\begin{split}
 \textit{AccumulatedRecoveredUnits}_{r,t,y} &= \sum\limits_{yy \in YEAR: (y-yy < \text{VidaUtilRecuperada}_{r,t}) \land (y-yy \geq 0)} \textit{RecoveredExistingUnits}_{r,t,yy}
\end{split}""",
    "Recovered_Residual_Aggregated": r"""\begin{split}
 \textit{RecoveredCapacity}_{r,t,y} &\leq \text{ResidualCapacity}_{r,t,y-1} \\
 &- \text{ResidualCapacity}_{r,t,y} \\
 &+ \textit{RecoveredCapacity}_{r,t,y-\text{VidaUtilRecuperada}_{r,t}}
\end{split}""",
    "Accumulated_Recovered_Capacity": r"""\begin{split}
 \textit{AccumulatedRecoveredCapacity}_{r,t,y} &= \sum\limits_{yy \in YEAR: (y-yy < \text{VidaUtilRecuperada}_{r,t}) \land (y-yy \geq 0)} \textit{RecoveredCapacity}_{r,t,yy}
\end{split}""",
    "Recovered_New_Capacity": r"""\begin{split}
 \textit{RecoveredNewCapacity}_{r,t,y} &\leq \textit{NewCapacity}_{r,t,y-\text{OperationalLife}_{r,t}}
\end{split}""",
    "Accumulated_Recovered_New_Capacity": r"""\begin{split}
 \textit{AccumulatedRecoveredNewCapacity}_{r,t,y} &= \sum\limits_{yy \in YEAR: 0 \leq y-yy < \text{VidaUtilRecuperada}_{r,t}} \textit{RecoveredNewCapacity}_{r,t,yy}
\end{split}""",
    "RM3_ReserveMargin_Constraint": r"""\begin{split}
 &\sum\limits_{t,m,f: \text{OutputActivityRatio} \neq 0} \textit{RateOfActivity}_{r,l,t,m,y} \cdot \text{OutputActivityRatio}_{r,t,f,m,y} \\
 &\quad \cdot \text{ReserveMarginTagFuel}_{r,f,y} \cdot \text{ReserveMargin}_{r,y} \\
 &\leq \sum\limits_{t} \bigg( \sum\limits_{\substack{yy \in YEAR: \\ (y-yy < \text{OperationalLife}_{r,t}) \\ \land (y-yy \geq 0)}} \textit{NewCapacity}_{r,t,yy} + \text{ResidualCapacity}_{r,t,y} \bigg) \\
 &\quad \cdot \text{ReserveMarginTagTechnology}_{r,t,y} \cdot \text{CapacityToActivityUnit}_{r,t}
\end{split}""",
    "RE1_FuelProductionByTechnologyAnnual": r"""\begin{split}
 \sum\limits_{l} \textit{ProductionByTechnology}_{r,l,t,f,y} &= \textit{ProductionByTechnologyAnnual}_{r,t,f,y}
\end{split}""",
    "RE2_TechIncluded": r"""\begin{split}
 \sum\limits_{t, f} \textit{ProductionByTechnologyAnnual}_{r,t,f,y} \cdot \text{RETagTechnology}_{r,t,y} &= \textit{TotalREProductionAnnual}_{r,y}
\end{split}""",
    "RE3_FuelIncluded": r"""\begin{split}
 \sum\limits_{l, f} \textit{RateOfProduction}_{r,l,f,y} \cdot \text{YearSplit}_{l,y} \cdot \text{RETagFuel}_{r,f,y} &= \textit{RETotalProductionOfTargetFuelAnnual}_{r,y}
\end{split}""",
    "RE4_EnergyConstraint": r"""\begin{split}
 \textit{RETotalProductionOfTargetFuelAnnual}_{r,y} \cdot \text{REMinProductionTarget}_{r,y} &\leq \textit{TotalREProductionAnnual}_{r,y}
\end{split}""",
    "RE5_FuelUseByTechnologyAnnual": r"""\begin{split}
 \sum\limits_{l} \textit{RateOfUseByTechnology}_{r,l,t,f,y} \cdot \text{YearSplit}_{l,y} &= \textit{UseByTechnologyAnnual}_{r,t,f,y}
\end{split}""",
    "SV123_SalvageValueAtEndOfPeriod1": r"""\begin{split}
 \textit{SalvageValue}_{r,t,y} &= \textit{NewCapacity}_{r,t,y} \cdot \text{CapitalCost}_{r,t,y} \cdot CRF_{new} \cdot PV_{new} \cdot f_{new} \\
 &+ \textit{RecoveredNewCapacity}_{r,t,y} \cdot \text{CostoRecuperacion}_{r,t,y} \cdot CRF_{rec} \cdot PV_{rec} \cdot f_{rec} \\
 &+ \textit{RecoveredCapacity}_{r,t,y} \cdot \text{CostoRecuperacion}_{r,t,y} \cdot CRF_{rec} \cdot PV_{rec} \cdot f_{rec} \\
 &+ \textit{RecoveredExistingUnits}_{r,t,y} \cdot \text{CapacityOfOneTechnologyUnit}_{r,t,y_0} \\
 &\quad \cdot \text{CostoRecuperacion}_{r,t,y} \cdot CRF_{rec} \cdot PV_{rec} \cdot f_{rec}
\end{split}""",
    "SV4_SalvageValueDiscountedToStarYear": r"""\begin{split}
 \textit{DiscountedSalvageValue}_{r,t,y} &= \frac{\textit{SalvageValue}_{r,t,y}}{(1 + \text{DiscountRate}_{r})^{1 + (y_L - y_0)}}
\end{split}""",
    "SC1_LowerLimit_BeginningOfDailyTimeBracketOfFirstInstanceOfDayTypeInFirstWeekConstraint": r"""\begin{split}
 0 &\leq \textit{StorageLevelDayTypeStart}_{r,s,ls,ld,y} \\
 &+ \sum\limits_{lhlh: lh-lhlh > 0} \textit{NetChargeWithinDay}_{r,s,ls,ld,lhlh,y} - \textit{StorageLowerLimit}_{r,s,y}
\end{split}""",
    "SC1_UpperLimit_BeginningOfDailyTimeBracketOfFirstInstanceOfDayTypeInFirstWeekConstraint": r"""\begin{split}
 \textit{StorageLevelDayTypeStart}_{r,s,ls,ld,y} &+ \sum\limits_{lhlh: lh-lhlh > 0} \textit{NetChargeWithinDay}_{r,s,ls,ld,lhlh,y} \\
 &- \textit{StorageUpperLimit}_{r,s,y} \leq 0
\end{split}""",
    "SC2_LowerLimit_EndOfDailyTimeBracketOfLastInstanceOfDayTypeInFirstWeekConstraint": r"""\begin{split}
 0 &\leq \textit{StorageLevelDayTypeStart}_{r,s,ls,ld,y} \\
 &- \sum\limits_{lhlh: lh-lhlh < 0} \textit{NetChargeWithinDay}_{r,s,ls,ld-1,lhlh,y} \\
 &- \textit{StorageLowerLimit}_{r,s,y}
\end{split}""",
    "SC2_UpperLimit_EndOfDailyTimeBracketOfLastInstanceOfDayTypeInFirstWeekConstraint": r"""\begin{split}
 \textit{StorageLevelDayTypeStart}_{r,s,ls,ld,y} \\
 &- \sum\limits_{lhlh: lh-lhlh < 0} \textit{NetChargeWithinDay}_{r,s,ls,ld-1,lhlh,y} \\
 &- \textit{StorageUpperLimit}_{r,s,y} \leq 0
\end{split}""",
    "SC3_LowerLimit_EndOfDailyTimeBracketOfLastInstanceOfDayTypeInLastWeekConstraint": r"""\begin{split}
 0 &\leq \textit{StorageLevelDayTypeFinish}_{r,s,ls,ld,y} \\
 &- \sum\limits_{lhlh: lh-lhlh < 0} \textit{NetChargeWithinDay}_{r,s,ls,ld,lhlh,y} \\
 &- \textit{StorageLowerLimit}_{r,s,y}
\end{split}""",
    "SC3_UpperLimit_EndOfDailyTimeBracketOfLastInstanceOfDayTypeInLastWeekConstraint": r"""\begin{split}
 \textit{StorageLevelDayTypeFinish}_{r,s,ls,ld,y} \\
 &- \sum\limits_{lhlh: lh-lhlh < 0} \textit{NetChargeWithinDay}_{r,s,ls,ld,lhlh,y} \\
 &- \textit{StorageUpperLimit}_{r,s,y} \leq 0
\end{split}""",
    "SC4_LowerLimit_BeginningOfDailyTimeBracketOfFirstInstanceOfDayTypeInLastWeekConstraint": r"""\begin{split}
 0 &\leq \textit{StorageLevelDayTypeFinish}_{r,s,ls,ld-1,y} \\
 &+ \sum\limits_{lhlh: lh-lhlh > 0} \textit{NetChargeWithinDay}_{r,s,ls,ld,lhlh,y} \\
 &- \textit{StorageUpperLimit}_{r,s,y}
\end{split}""",
    "SC4_UpperLimit_BeginningOfDailyTimeBracketOfFirstInstanceOfDayTypeInLastWeekConstraint": r"""\begin{split}
 \textit{StorageLevelDayTypeFinish}_{r,s,ls,ld-1,y} \\
 &+ \sum\limits_{lhlh: lh-lhlh > 0} \textit{NetChargeWithinDay}_{r,s,ls,ld,lhlh,y} \\
 &- \textit{StorageUpperLimit}_{r,s,y} \leq 0
\end{split}""",
    "SC5_MaxChargeConstraint": r"""\begin{split}
 \textit{RateOfStorageCharge}_{r,s,ls,ld,lh,y} &\leq \text{StorageMaxChargeRate}_{r,s}
\end{split}""",
    "SC6_MaxDischargeConstraint": r"""\begin{split}
 \textit{RateOfStorageDischarge}_{r,s,ls,ld,lh,y} &\leq \text{StorageMaxDischargeRate}_{r,s}
\end{split}""",
    "S1_RateOfStorageCharge": r"""\begin{split}
 &\sum\limits_{\substack{t, m, l: \\ \text{TechnologyToStorage} > 0}} \textit{RateOfActivity}_{r,l,t,m,y} \cdot \text{TechnologyToStorage}_{r,t,s,m} \\
 &\quad \cdot \text{Conversionls}_{l,ls} \cdot \text{Conversionld}_{l,ld} \cdot \text{Conversionlh}_{l,lh} \\
 &= \textit{RateOfStorageCharge}_{r,s,ls,ld,lh,y}
\end{split}""",
    "S2_RateOfStorageDischarge": r"""\begin{split}
 &\sum\limits_{\substack{t, m, l: \\ \text{TechnologyFromStorage} > 0}} \textit{RateOfActivity}_{r,l,t,m,y} \cdot \text{TechnologyFromStorage}_{r,t,s,m} \\
 &\quad \cdot \text{Conversionls}_{l,ls} \cdot \text{Conversionld}_{l,ld} \cdot \text{Conversionlh}_{l,lh} \\
 &= \textit{RateOfStorageDischarge}_{r,s,ls,ld,lh,y}
\end{split}""",
    "S3_NetChargeWithinYear": r"""\begin{split}
 &\sum\limits_{l} (\textit{RateOfStorageCharge}_{r,s,ls,ld,lh,y} - \textit{RateOfStorageDischarge}_{r,s,ls,ld,lh,y}) \\
 &\quad \cdot \text{YearSplit}_{l,y} \cdot \text{Conversionls}_{l,ls} \cdot \text{Conversionld}_{l,ld} \cdot \text{Conversionlh}_{l,lh} \\
 &= \textit{NetChargeWithinYear}_{r,s,ls,ld,lh,y}
\end{split}""",
    "S4_NetChargeWithinDay": r"""\begin{split}
 &(\textit{RateOfStorageCharge}_{r,s,ls,ld,lh,y} - \textit{RateOfStorageDischarge}_{r,s,ls,ld,lh,y}) \\
 &\quad \cdot \text{DaySplit}_{lh,y} = \textit{NetChargeWithinDay}_{r,s,ls,ld,lh,y}
\end{split}""",
    "S5_and_S6_StorageLevelYearStart": r"""\begin{split}
 \textit{StorageLevelYearStart}_{r,s,y-1} &+ \sum\limits_{ls, ld, lh} \textit{NetChargeWithinYear}_{r,s,ls,ld,lh,y-1} \\
 &= \textit{StorageLevelYearStart}_{r,s,y}
\end{split}""",
    "S7_and_S8_StorageLevelYearFinish": r"""\begin{split}
 \textit{StorageLevelYearStart}_{r,s,y} &+ \sum\limits_{ls, ld, lh} \textit{NetChargeWithinYear}_{r,s,ls,ld,lh,y} \\
 &= \textit{StorageLevelYearFinish}_{r,s,y}
\end{split}""",
    "S9_and_S10_StorageLevelSeasonStart": r"""\begin{split}
 \textit{StorageLevelSeasonStart}_{r,s,ls-1,y} &+ \sum\limits_{ld, lh} \textit{NetChargeWithinYear}_{r,s,ls-1,ld,lh,y} \\
 &= \textit{StorageLevelSeasonStart}_{r,s,ls,y}
\end{split}""",
    "S11_and_S12_StorageLevelDayTypeStart": r"""\begin{split}
 \textit{StorageLevelDayTypeStart}_{r,s,ls,ld-1,y} &+ \sum\limits_{lh} \textit{NetChargeWithinDay}_{r,s,ls,ld-1,lh,y} \cdot \text{DaysInDayType}_{ls,ld-1,y} \\
 &= \textit{StorageLevelDayTypeStart}_{r,s,ls,ld,y}
\end{split}""",
    "S13_and_S14_and_S15_StorageLevelDayTypeFinish": r"""\begin{split}
 \textit{StorageLevelDayTypeFinish}_{r,s,ls,ld+1,y} &- \sum\limits_{lh} \textit{NetChargeWithinDay}_{r,s,ls,ld+1,lh,y} \cdot \text{DaysInDayType}_{ls,ld+1,y} \\
 &= \textit{StorageLevelDayTypeFinish}_{r,s,ls,ld,y}
\end{split}""",
    "S16_StorageLevel": r"""\begin{split}
 \textit{StorageLevel}_{r,s,ls,ld,lh,y} &= \textit{StorageLevelDayTypeStart}_{r,s,ls,ld,y}
\end{split}""",
    "SI1_StorageUpperLimit": r"""\begin{split}
 \textit{AccumulatedNewStorageCapacity}_{r,s,y} + \text{ResidualStorageCapacity}_{r,s,y} &= \textit{StorageUpperLimit}_{r,s,y}
\end{split}""",
    "SI2_StorageLowerLimit": r"""\begin{split}
 \text{MinStorageCharge}_{r,s,y} \cdot \textit{StorageUpperLimit}_{r,s,y} &= \textit{StorageLowerLimit}_{r,s,y}
\end{split}""",
    "SI3_TotalNewStorage": r"""\begin{split}
 \sum\limits_{\substack{yy \in YEAR: \\ (y-yy < \text{OperationalLifeStorage}_{r,s}) \\ \land (y-yy \geq 0)}} \textit{NewStorageCapacity}_{r,s,yy} &= \textit{AccumulatedNewStorageCapacity}_{r,s,y}
\end{split}""",
    "SI4_UndiscountedCapitalInvestmentStorage": r"""\begin{split}
 \text{CapitalCostStorage}_{r,s,y} \cdot \textit{NewStorageCapacity}_{r,s,y} &= \textit{CapitalInvestmentStorage}_{r,s,y}
\end{split}""",
    "SI5_DiscountingCapitalInvestmentStorage": r"""\begin{split}
 \frac{\textit{CapitalInvestmentStorage}_{r,s,y}}{(1 + \text{DiscountRate}_{r})^{y - \min(YEAR)}} &= \textit{DiscountedCapitalInvestmentStorage}_{r,s,y}
\end{split}""",
    "SI6_SalvageValueStorageAtEndOfPeriod1": r"""\begin{split}
 0 &= \textit{SalvageValueStorage}_{r,s,y}
\end{split}""",
    "SI7_SalvageValueStorageAtEndOfPeriod2": r"""\begin{split}
 \textit{CapitalInvestmentStorage}_{r,s,y} \cdot \left(1 - \frac{\max(YEAR) - y + 1}{\text{OperationalLifeStorage}_{r,s}}\right) &= \textit{SalvageValueStorage}_{r,s,y}
\end{split}""",
    "SI8_SalvageValueStorageAtEndOfPeriod3": r"""\begin{split}
 \textit{CapitalInvestmentStorage}_{r,s,y} \\
 \cdot \left(1 - \frac{(1 + \text{DiscountRate}_{r})^{\max(YEAR) - y + 1} - 1}{(1 + \text{DiscountRate}_{r})^{\text{OperationalLifeStorage}_{r,s}} - 1}\right) &= \textit{SalvageValueStorage}_{r,s,y}
\end{split}""",
    "SI9_SalvageValueStorageDiscountedToStartYear": r"""\begin{split}
 \frac{\textit{SalvageValueStorage}_{r,s,y}}{(1 + \text{DiscountRate}_{r})^{\max(YEAR) - \min(YEAR) + 1}} &= \textit{DiscountedSalvageValueStorage}_{r,s,y}
\end{split}""",
    "SI10_TotalDiscountedCostByStorage": r"""\begin{split}
 \textit{DiscountedCapitalInvestmentStorage}_{r,s,y} - \textit{DiscountedSalvageValueStorage}_{r,s,y} &= \textit{TotalDiscountedStorageCost}_{r,s,y}
\end{split}""",
    "TDC1_TotalDiscountedCostByTechnology": r"""\begin{split}
 \textit{DiscountedOperatingCost}_{r,t,y} &+ \textit{DiscountedCapitalInvestment}_{r,t,y} \\
 &+ \textit{DiscountedTechnologyEmissionsPenalty}_{r,t,y} \\
 &- \textit{DiscountedSalvageValue}_{r,t,y} \\
 &= \textit{TotalDiscountedCostByTechnology}_{r,t,y}
\end{split}""",
    "TDC2_TotalDiscountedCost": r"""\begin{split}
 \sum\limits_{t} \textit{TotalDiscountedCostByTechnology}_{r,t,y} &+ \sum\limits_{s} \textit{TotalDiscountedStorageCost}_{r,s,y} \\
 &= \textit{TotalDiscountedCost}_{r,y}
\end{split}""",
    "SpecifiedDemand_EQ": r"""\begin{split}
 \textit{RateOfDemand}_{r,l,f,y} &= \frac{\text{SpecifiedAnnualDemand}_{r,f,y} \cdot \text{SpecifiedDemandProfile}_{r,f,l,y}}{\text{YearSplit}_{l,y}}
\end{split}""",
}
