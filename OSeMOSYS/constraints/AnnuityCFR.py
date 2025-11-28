### Parámetros financieros


def _crf(L, dr_idv):
    # (1 - (1+dr_idv)^-1) / (1 - (1+dr_idv)^-L)
    return (1 - (1 + dr_idv)**(-1)) / (1 - (1 + dr_idv)**(-L))

def _pv_annuity(L, dr):
    # (1 - (1+dr)^-L) * (1+dr) / dr
    return (1 - (1 + dr)**(-L)) * (1 + dr) / dr
