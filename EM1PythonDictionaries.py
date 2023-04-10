variable_symbols = {
    "taue": r"$\tau_E$",
    "betan": r"$\beta_{\mathrm{N}}$",
    "modeh": r"H-Mode",
    "qeff": r"$q_{\mathrm{effective}}$",
    "q0": r"$q_0$",
    "q95": r"$q_{95}$",
    "temps": r"$t$",
    "pnbi": r"$P_{\mathrm{NBI}}$",
    "frnbi": r"$P_{\mathrm{NBI frac}}$",
    "pnbi_th": r"$P_{\mathrm{NBI thermal}}$",
    "ip": r"$I_{\mathrm{plasma}}$",
    "betap": r"$\beta_{\mathrm{P}}$",
    "nbar": r"$\bar{n}_e$",
    "ne0": r"$n_{e(0)}$",
    "ni0": r"$n_{i(0)}$",
    "nim": r"$n_{i(m)}$",
    "te0": r"$T_{e(0)}$",
    "tem": r"$\bar{T}_e$",
    "tite": r"$\frac{T_i}{T_e}$",
    "pfus": r"$P_{\mathrm{fusion}}$",
    "sext": r"$S_{\mathrm{ext}}$",
    "vp": r"$V_{\mathrm{p}}$",
    "W": r"$E_{\mathrm{p}}$",
    "ni0titetaue": r"$n_{i(0)}\frac{T_i}{T_e}\tau_E$",  # This is a custom variable
    "nimtimtaue": r"$n_{i(m)}T_{i(m)}\tau_E$",  # This is a custom variable
    "nTtau": r"$\bar{n}_i \bar{T}_i \tau_E$",  # This is a custom variable
}

variable_meanings = {
    "taue": "Energy Confinement Time",
    "betan": "Normalised Plasma Beta",
    "modeh": "Confinement Mode [L=0, H=1]",
    "qeff": "Effective Safety Factor",
    "q0": "Central Safety Factor",
    "q95": "Safety Factor at 95%%",
    "temps": "Time",
    "pnbi": "NBI",
    "frnbi": "Frac. NBI absorbed in plasma",
    "pnbi_th": "NBI Therm. Power Deposit.",
    "ip:": "Plasma Current",
    "betap": "Poloidal Beta",
    "nbar": "Line averaged plasma electron density",
    "ne0": "Central electron density",
    "ni0": "Central ion density",
    "nim": "Sum of V.Avg. Ion Densities",
    "te0": "Central electron temp.",
    "tite": "Ratio of ion to e- temp.",
    "tem": "Volume avg. e- temp.",
    "pfus": "Alpha D-T Fusion Power",
    "sext": "External Plasma Surface",
    "vp": "Plasma Volume",
    "W": "Total Plasma Energy",
    "ni0titetaue": "Old Triple Product",  # This is a custom variable
    "nimtimtaue": "Triple Product",  # This is a custom variable
    "nTtau": "Triple Product",  # This is a custom variable
}

variable_units = {
    "taue": r"\unit{\second}",
    "betan": "",
    "modeh": "",
    "qeff": "",
    "q0": "",
    "q95": "",
    "temps": r"\unit{\second}",
    "pnbi": r"\unit{\watt}",
    "frnbi": "",
    "pnbi_th": r"\unit{\watt}",
    "ip:": r"$\unit{\ampere}$",
    "betap": "",
    "nbar": r"\unit{\per\metre\squared}",
    "ne0": r"\unit{\per\metre\cubed}",
    "ni0": r"\unit{\per\metre\cubed}",
    "nim": r"\unit{\per\metre\cubed}",
    "te0": r"\unit{\electronvolt}",
    "tite": "",
    "tem": r"\unit{\electronvolt}",
    "pfus": r"\unit{\watt}",
    "sext": r"\unit{\metre\squared}",
    "vp": r"\unit{\metre\cubed}",
    "W": r"\unit{\joule}",
    "ni0titetaue": r"\unit{\second\per\metre\cubed}",  # This is a custom variable
    "nimtimtaue": r"\unit{\electronvolt\second\per\metre\cubed}",  # This is a custom variable
    "nTtau": r"\unit{\electronvolt\second\per\metre\cubed}",  # This is a custom variable
}

variable_yticks = {
    "modeh": [0, 1],
}

variables_list = list(variable_symbols.keys())

parameter_symbols = {
    "b0": r"$B_0$",  # Toroidal Magnetic Field
    "a": r"$a$",  # Minor Radius of Plasma
    "R0": r"$R_0$",  # Major Radius of Plasma
    "z0": r"$Z_0$",  # Height of Plasma
    "ip": r"$I_{\mathrm{plasma}}$",
    "nbar": r"$\bar{N}$",
    "nim": r"$N_{i(m)}$",
    "pnbi": r"$P_{\mathrm{NBI}}$",
}

parameter_meanings = {
    "b0": "Toroidal Magnetic Field",
    "a": "Minor Radius of Plasma",
    "R0": "Major Radius of Plasma",
    "z0": "Height of Plasma",
    "ip": "Plasma Current",
    "nbar": "Line averaged electron density",
    "nim": "Sum of V.Avg. Ion Densities",
    "pnbi": "NBI Power",
}

parameter_units = {
    "b0": r"\unit{\tesla}",
    "a": r"\unit{\metre}",
    "R0": r"\unit{\metre}",
    "z0": r"\unit{\metre}",
    "ip": r"\unit{\ampere}",
    "nbar": r"\unit{\per\metre\cubed}",
    "nim": r"\unit{\per\metre\cubed}",
    "pnbi": r"\unit{\mega\watt}",
}

respective_variable_for_dataframe = {
    "pnbi_dataframes": "pnbi",
    "B0_dataframes": "b0",
    "Ip_dataframes": "ip",
    "nbar_dataframes": "nbar",
}
