import pybamm
import numpy as np
import pickle
import matplotlib.pyplot as plt

pybamm.set_logging_level("INFO")

run = False


if run is False:

    sol = pickle.load(open("spme_dfn_errors.p", "rb"))

    plt.plot(sol["pts"], sol["voltage errors"])
    plt.plot(sol["pts"], sol["c_s_n_errors"])
    plt.plot(sol["pts"], sol["c_s_p_errors"])
    plt.plot(sol["pts"], sol["phi_s_n_errors"])
    plt.legend(["Voltage", "c_s_n", "c_s_p", "phi_s_n"])
    plt.show()

    # relative to final point
    def rel(a):
        return np.abs(a - a[-1]) / a[-1]

    plt.loglog(sol["pts"], rel(sol["voltage errors"]))
    plt.loglog(sol["pts"], rel(sol["c_s_n_errors"]))
    plt.loglog(sol["pts"], rel(sol["c_s_p_errors"]))
    plt.loglog(sol["pts"], rel(sol["phi_s_n_errors"]))
    plt.legend(["Voltage", "c_s_n", "c_s_p", "phi_s_n"])
    plt.show()
else:

    def pts(n):
        var = pybamm.standard_spatial_vars
        var_pts = {
            var.x_n: n,
            var.x_s: n,
            var.x_p: n,
            var.r_n: n,
            var.r_p: n,
            var.y: n,
            var.z: n,
        }
        return var_pts

    t_eval = np.linspace(0, 3300, 100)
    solver = pybamm.CasadiSolver(mode="fast")

    options = {}

    model_truth = pybamm.lithium_ion.DFN(options)
    sim_truth = pybamm.Simulation(model_truth, var_pts=pts(3), solver=solver)
    sim_truth.solve()

    t_max = sim_truth.solution.t[-1]
    t = np.linspace(0, t_max, 100)
    truth_voltage = sim_truth.solution["Terminal voltage [V]"](t)

    other_pts = np.array([3, 5, 10, 20, 30, 40, 50, 100, 200])
    solutions = np.zeros_like(other_pts)
    voltage_errors = np.linspace(0, 1, len(other_pts))
    c_s_n_errors = np.linspace(0, 1, len(other_pts))
    c_s_p_errors = np.linspace(0, 1, len(other_pts))
    phi_s_n_errors = np.linspace(0, 1, len(other_pts))

    l_n = sim_truth.parameter_values.process_symbol(
        pybamm.geometric_parameters.l_n
    ).evaluate()
    l_s = sim_truth.parameter_values.process_symbol(
        pybamm.geometric_parameters.l_s
    ).evaluate()
    l_p = sim_truth.parameter_values.process_symbol(
        pybamm.geometric_parameters.l_p
    ).evaluate()

    x_n = np.linspace(0, l_n, 100)
    x_s = np.linspace(l_n, l_n + l_s, 100)
    x_p = np.linspace(l_n + l_s, 1, 100)

    for i, p in enumerate(other_pts):

        dfn = pybamm.lithium_ion.DFN(options)
        dfn_solver = pybamm.CasadiSolver(mode="fast")
        dfn_sim = pybamm.Simulation(dfn, var_pts=pts(p), solver=solver)
        dfn_sim.solve()

        spme = pybamm.lithium_ion.SPMe(options)
        spme_solver = pybamm.CasadiSolver(mode="fast")
        spme_sim = pybamm.Simulation(spme, var_pts=pts(p), solver=solver)
        spme_sim.solve()

        v_dfn = dfn_sim.solution["Terminal voltage [V]"](t)
        c_s_n = dfn_sim.solution["Negative particle surface concentration"](
            t=t, x=x_n
        ).flatten()
        c_s_p = dfn_sim.solution["Positive particle surface concentration"](
            t=t, x=x_p
        ).flatten()
        phi_s_n = dfn_sim.solution["Negative electrode potential [V]"](
            t=t, x=x_n
        ).flatten()

        v_spm = spme_sim.solution["Terminal voltage [V]"](t)
        c_s_n_spm = spme_sim.solution["Negative particle surface concentration"](
            t=t, x=x_n
        ).flatten()
        c_s_p_spm = spme_sim.solution["Positive particle surface concentration"](
            t=t, x=x_p
        ).flatten()
        phi_s_n_spm = spme_sim.solution["Negative electrode potential [V]"](
            t=t, x=x_n
        ).flatten()

        def err(a, b):
            norm = np.sum((a) ** 2) ** (1 / 2)  # normalizing factor
            rms = np.sum((a - b) ** 2) ** (1 / 2)
            return rms / norm

        voltage_errors[i] = err(v_dfn, v_spm)
        c_s_n_errors[i] = err(c_s_n, c_s_n_spm)
        c_s_p_errors[i] = err(c_s_p, c_s_p_spm)
        phi_s_n_errors[i] = err(phi_s_n, phi_s_n_spm)

    out = {
        "pts": other_pts,
        "voltage errors": voltage_errors,
        "c_s_n_errors": c_s_n_errors,
        "c_s_p_errors": c_s_p_errors,
        "phi_s_n_errors": phi_s_n_errors,
    }
    pickle.dump(out, open("spme_dfn_errors.p", "wb"))

    plt.plot(other_pts, voltage_errors)
    plt.plot(other_pts, c_s_n_errors)
    plt.plot(other_pts, c_s_p_errors)
    plt.plot(other_pts, phi_s_n_errors)
    plt.legend("Voltage", "Negative particle concentration")
    plt.show()

