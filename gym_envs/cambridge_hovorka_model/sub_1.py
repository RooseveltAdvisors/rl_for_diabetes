def sub_1():
    """
    PATIENT PARAMETERS

    parameters taken from Description of the simulator pdf
    """

    BW = 69
    # Patient-dependent parameters:
    V_I = 0.113 * BW
    V_G = 0.1787 * BW
    EGP_0 = 0.01962 * BW
    F_01s = 0.01295 * BW

    R_thr = 11.70
    R_cl = 0.0119

    # Patient-independent(?) parameters:
    S_IT = 0.00771
    S_ID = 0.000314
    S_IE = 0.0377
    tau_G = 43
    A_G = 0.710
    k_12 = .1095
    k_b1 = 0.0021104996
    k_b2 = 0.3956
    k_b3 = 0.0803
    k_a1 = k_b1 * S_IT
    k_a2 = k_b2 * S_ID
    k_a3 = k_b3 * S_IE

    k_e = 0.1320736797
    k_a = 1.92e-2

    ka_int = 0.0736

    # Summary of the patient's values:
    P = [tau_G, k_a, A_G, k_12, k_a1, k_b1, k_a2, k_b2, k_a3, k_b3, k_e, V_I, V_G, F_01s, EGP_0, ka_int, R_cl, R_thr]

    return P
