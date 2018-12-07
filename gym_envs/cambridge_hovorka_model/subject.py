def subject(sub):
    """
    PATIENT PARAMETERS

    parameters taken from Description of the simulator pdf
    """

    if sub == 1:
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
        k_a = 1.98e-2

        ka_int = 0.0736

        # Summary of the patient's values:
        P = [tau_G, k_a, A_G, k_12, k_a1, k_b1, k_a2, k_b2, k_a3, k_b3, k_e, V_I, V_G, F_01s, EGP_0, ka_int, R_cl, R_thr]


    elif sub == 2:
        BW = 90
        # Patient-dependent parameters:
        V_I = 0.131 * BW
        V_G = 0.1450 * BW
        EGP_0 = 0.00910 * BW
        F_01s = 0.00977 * BW

        R_thr = 9.22
        R_cl = 0.0130

        # Patient-independent(?) parameters:
        S_IT = 0.0011
        S_ID = 0.000158
        S_IE = 0.0073
        tau_G = 55
        A_G = 0.90
        k_12 = .0509
        k_b1 = 0.0006
        k_b2 = 0.0136
        k_b3 = 0.0202
        k_a1 = k_b1 * S_IT
        k_a2 = k_b2 * S_ID
        k_a3 = k_b3 * S_IE

        k_e = 10.1e-2
        k_a = 1.60e-2

        ka_int = 0.1510

        # Summary of the patient's values:
        P = [tau_G, k_a, A_G, k_12, k_a1, k_b1, k_a2, k_b2, k_a3, k_b3, k_e, V_I, V_G, F_01s, EGP_0, ka_int, R_cl, R_thr]


    elif sub == 3:
        BW = 107
        # Patient-dependent parameters:
        V_I = 0.115 * BW
        V_G = 0.1457 * BW
        EGP_0 = 0.01049 * BW
        F_01s = 0.01028 * BW

        R_thr = 7.75
        R_cl = 0.0965

        # Patient-independent(?) parameters:
        S_IT = 0.00124
        S_ID = 0.000153
        S_IE = 0.0114
        tau_G = 26
        A_G = 0.72
        k_12 = .0307
        k_b1 = 0.0007
        k_b2 = 0.0369
        k_b3 = 0.0339
        k_a1 = k_b1 * S_IT
        k_a2 = k_b2 * S_ID
        k_a3 = k_b3 * S_IE

        k_e = 17.7e-2
        k_a = 2.57e-2

        ka_int = 0.0974

        # Summary of the patient's values:
        P = [tau_G, k_a, A_G, k_12, k_a1, k_b1, k_a2, k_b2, k_a3, k_b3, k_e, V_I, V_G, F_01s, EGP_0, ka_int, R_cl, R_thr]


    elif sub == 4:
        BW = 87
        # Patient-dependent parameters:
        V_I = 0.130 * BW
        V_G = 0.1782 * BW
        EGP_0 = 0.00825 * BW
        F_01s = 0.00809 * BW

        R_thr = 10.07
        R_cl = 0.0105

        # Patient-independent(?) parameters:
        S_IT = 0.00119
        S_ID = 0.000664
        S_IE = 0.0116
        tau_G = 29
        A_G = 0.77
        k_12 = .0635
        k_b1 = 0.0014
        k_b2 = 0.1377
        k_b3 = 0.0210
        k_a1 = k_b1 * S_IT
        k_a2 = k_b2 * S_ID
        k_a3 = k_b3 * S_IE

        k_e = 14e-2
        k_a = 2.53e-2

        ka_int = 0.1103

        # Summary of the patient's values:
        P = [tau_G, k_a, A_G, k_12, k_a1, k_b1, k_a2, k_b2, k_a3, k_b3, k_e, V_I, V_G, F_01s, EGP_0, ka_int, R_cl, R_thr]


    elif sub == 5:
        BW = 76
        # Patient-dependent parameters:
        V_I = 0.128 * BW
        V_G = 0.1803 * BW
        EGP_0 = 0.01407 * BW
        F_01s = 0.01298 * BW

        R_thr = 7.75
        R_cl = 0.0115

        # Patient-independent(?) parameters:
        S_IT = 0.003
        S_ID = 0.000170
        S_IE = 0.0219
        tau_G = 42
        A_G = 0.78
        k_12 = .0293
        k_b1 = 0.0032
        k_b2 = 0.2195
        k_b3 = 0.0323
        k_a1 = k_b1 * S_IT
        k_a2 = k_b2 * S_ID
        k_a3 = k_b3 * S_IE

        k_e = 12e-2
        k_a = 2.89e-2

        ka_int = 0.0689

        # Summary of the patient's values:
        P = [tau_G, k_a, A_G, k_12, k_a1, k_b1, k_a2, k_b2, k_a3, k_b3, k_e, V_I, V_G, F_01s, EGP_0, ka_int, R_cl, R_thr]



    elif sub == 6:
        BW = 101
        # Patient-dependent parameters:
        V_I = 0.128 * BW
        V_G = 0.1317 * BW
        EGP_0 = 0.00435 * BW
        F_01s = 0.00396 * BW

        R_thr = 7.55
        R_cl = 0.0111

        # Patient-independent(?) parameters:
        S_IT = 0.00054
        S_ID = 0.0012
        S_IE = 0.0053
        tau_G = 52
        A_G = 0.71
        k_12 = .0537
        k_b1 = 0.0048
        k_b2 = 0.0442
        k_b3 = 0.0166
        k_a1 = k_b1 * S_IT
        k_a2 = k_b2 * S_ID
        k_a3 = k_b3 * S_IE

        k_e = 16.7e-2
        k_a = 2.44e-2

        ka_int = 0.0898

        # Summary of the patient's values:
        P = [tau_G, k_a, A_G, k_12, k_a1, k_b1, k_a2, k_b2, k_a3, k_b3, k_e, V_I, V_G, F_01s, EGP_0, ka_int, R_cl, R_thr]

    return P
