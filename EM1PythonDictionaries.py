variable_symbols = {
    "taue": r"$\tau_E$",
    "betan": r"$\beta_{\mathrm{normalised}}$",
    "modeh": r"H-Mode",
    "qeff": r"$q_{\mathrm{effective}}$",
    "q0": r"$q_0$",
    "q95": r"$q_{95}$",
    "temps": r"$t$",
    "pnbi": r"$P_{\mathrm{NBI input}}$",
    "frnbi": r"$P_{\mathrm{NBI frac}}$",
    "betap": r"$\beta_{\mathrm{P}}$",
    "ne0": r"$n_{e(0)}$",
    "ni0": r"$n_{i(0)}$",
    "te0": r"$T_{e(0)}$",
    "tem": r"$\bar{T}_e$",
    "tite": r"$\frac{T_i}{T_e}$",
    "pfus": r"$P_{\mathrm{fusion}}$",
    "sext": r"$S_{\mathrm{external}}$",
    "vp": r"$V_{\mathrm{plasma}}$",
    "W": r"$E_{\mathrm{plasma}}$",
    "ni0titetaue": r"$n_{i(0)}\frac{T_i}{T_e}\tau_E$",  # This is a custom variable
    "nimtimtaue": r"$n_{i(m)}T_{i(m)}\tau_E$",  # This is a custom variable
}

variable_meanings = {
    "taue": "Energy Confinement Time",
    "betan": "Normalised Plasma Beta",
    "modeh": "Confinement Mode [L=0, H=1]",
    "qeff": "Effective Safety Factor",
    "q0": "Central Safety Factor",
    "q95": f"Safety Factor at 95\%",
    "temps": "Time",
    "pnbi": "NBI Input Power",
    "frnbi": "Fraction of NBI Power absorbed in plasma",
    "ip:": "Plasma Current",
    "betap": "Poloidal Beta",
    "nbar": "Line averaged plasma electron density",
    "ne0": "Central electron density",
    "ni0": "Central ion density",
    "te0": "Central electron temperature",
    "tite": "Ratio of ion to electron temperature",
    "tem": "Volume averaged electron temperature",
    "pfus": "Alpha D-T Fusion Power",
    "sext": "External Plasma Surface",
    "vp": "Plasma Volume",
    "W": "Total Plasma Energy",
    "ni0titetaue": "nTtau (old)",  # This is a custom variable
    "nimtimtaue": "nTtau",  # This is a custom variable
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
    "ip:": r"$\unit{\ampere}$",
    "betap": "",
    "nbar": r"\unit{\per\metre\squared}",
    "ne0": r"\unit{\per\metre\cubed}",
    "ni0": r"\unit{\per\metre\cubed}",
    "te0": r"\unit{\electronvolt}",
    "tite": "",
    "tem": r"\unit{\electronvolt}",
    "pfus": r"\unit{\watt}",
    "sext": r"\unit{\metre\squared}",
    "vp": r"\unit{\metre\cubed}",
    "W": r"\unit{\joule}",
    "ni0titetaue": r"\unit{\second\per\metre\cubed}",  # This is a custom variable
    "nimtimtaue": r"\unit{\electronvolt\second\per\metre\cubed}",  # This is a custom variable
}

parameter_symbols = {
    "b0": r"$B_0$",  # Toroidal Magnetic Field
    "a": r"$a$",  # Minor Radius of Plasma
    "R0": r"$R_0$",  # Major Radius of Plasma
    "z0": r"$Z_0$",  # Height of Plasma
    "Ip": r"$I_{\mathrm{plasma}}$",
    "Nbar": r"$\bar{N}$",
    "NBI": r"$P_{\mathrm{NBI}}$",
}

parameter_meanings = {
    "b0": "Toroidal Magnetic Field",
    "a": "Minor Radius of Plasma",
    "R0": "Major Radius of Plasma",
    "z0": "Height of Plasma",
    "Ip": "Plasma Current",
    "Nbar": "Line averaged electron density",
    "NBI": "NBI Input Power",
}

parameter_units = {
    "b0": r"\unit{\tesla}",
    "a": r"\unit{\metre}",
    "R0": r"\unit{\metre}",
    "z0": r"\unit{\metre}",
    "Ip": r"\unit{\ampere}",
    "Nbar": r"\unit{\per\metre\cubed}",
    "NBI": r"\unit{\mega\watt}",
}
