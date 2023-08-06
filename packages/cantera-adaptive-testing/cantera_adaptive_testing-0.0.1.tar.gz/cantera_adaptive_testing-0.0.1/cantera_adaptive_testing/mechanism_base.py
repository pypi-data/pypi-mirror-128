import os, time, datetime, ruamel_yaml, warnings
import cantera as ct
import numpy as np


class MechanismBase(object):

    def __init__(self, *args, **kwargs):
        # arbitrary parameters
        self.currRunTime = datetime.datetime.now().strftime("%X-%d-%m-%y")
        self.verbose = kwargs["verbose"] if "verbose" in kwargs else False
        # numerical options
        self.precon_on = kwargs["precon_on"] if "precon_on" in kwargs else True
        self.solver = kwargs["solver"] if "solver" in kwargs else "DENSE + NOJAC"
        if self.precon_on:
            self.threshold = kwargs["threshold"] if "threshold" in kwargs else 1e-16
        else:
            self.threshold = 0
        self.precon = None
        # standard physical parameters/options
        self.moles = kwargs["moles"] if "moles" in kwargs else True
        self.T0 = 300 # kelvin
        self.P0 = ct.one_atm # pascals
        self.V0 = 1 # m^3
        self.fuel = None
        self.air = 'O2:1.0, N2:3.76'
        self.equiv_ratio = 1 # equivalence ratio
        # output data options
        self.precName = "-Preconditioned" if self.precon_on else ""
        self.write = kwargs["write"] if "write" in kwargs else False
        self.outfile = kwargs["outfile"] if "outfile" in kwargs else "out.csv"
        self.dataDir, self.figDir = self.get_directories()
        # log variables
        self.runName = self.__class__.__name__ + self.precName + "-" + self.currRunTime
        self.log = kwargs["log"] if "log" in kwargs else True
        self.logfile = self.runName+".yaml"
        self.logdata = dict()
        # making directories
        if not os.path.isdir(self.dataDir):
            os.mkdir(self.dataDir)
            self.verbose_print(self.verbose, "Making data directory: " + self.dataDir)

    def __del__(self):
        if self.verbose:
            self.print_entry(self.logdata)
        if self.log and self.logdata:
            self.append_yaml(os.path.join(self.dataDir, self.logfile), self.logdata)

    def set_verbose(self, verbose):
        self.verbose = verbose

    def set_threshold(self, threshold):
        self.threshold = threshold

    def get_directories(self):
        cwd = os.getcwd()
        return os.path.join(cwd, "data"), os.path.join(cwd, "figures")

    def get_test_set_path(self, mechanism):
        return os.path.join(os.path.join(os.path.dirname(__file__), "mechanisms"), mechanism)

    def verbose_print(self, verbose, printStr):
        if verbose:
            print(printStr)

    def print_entry(self, entry, tab=""):
        for key in entry:
            subentry = entry[key]
            if isinstance(subentry, dict):
                print(tab+key+": ")
                self.print_entry(subentry, tab=tab+"\t")
            else:
                if isinstance(subentry, float):
                    if subentry < 1e-2:
                        subentry = "{:0.2e}".format(subentry)
                    else:
                        subentry = "{:0.2f}".format(subentry)
                elif isinstance(subentry, int):
                    subentry = "{:d}".format(subentry)
                print(tab+"\t"+key+": "+subentry)

    def append_yaml(self, yamlName, run):
        yaml = ruamel_yaml.YAML()
        yaml.default_flow_style = False
        if os.path.isfile(yamlName):
            with open(yamlName, 'r') as f:
                previous = yaml.load(f)
            previous.update(run)
            with open(yamlName, 'w') as f:
                yaml.dump(previous, f)
        else:
            with open(yamlName, 'w') as f:
                ruamel_yaml.dump(run, f)

    def apply_numerical_options(self):
        """
            Use this function to apply numerical configurations to the
            network
        """
        if self.precon_on:
            self.precon = ct.AdaptivePreconditioner()
            self.precon.set_threshold(self.threshold)
            self.net.preconditioner = self.precon
        self.net.problem_type = self.solver

    def problem(func):
        """This is a decorator wrap simulations in common functions"""
        def wrapped(self):
            # pre-run operations
            self.currRun = dict()
            # run problem
            t0 = time.time_ns()
            func(self)
            tf = time.time_ns()
            # post function analysis
            self.currRun.update({"runtime_seconds":"{:0.8f}".format((tf-t0) * 1e-9)})
            self.logdata.update({func.__name__:self.currRun})
            return
        return wrapped

    @problem
    def pressure_problem(self):
        """
        This problem is adapted from
        https://cantera.org/examples/python/reactors/pfr.py.html and is
        not entirely my own work

        This example solves a plug-flow reactor problem of
        hydrogen-oxygen combustion. The PFR is computed by two
        approaches: The simulation of a Lagrangian fluid particle, and
        the simulation of a chain of reactors.

        Requires: cantera >= 2.5.0
        """
        T0 = 1500.0  # inlet temperature [K]
        pressure = ct.one_atm # constant pressure [Pa]
        length = 1.5e-7  # *approximate* PFR length [m]
        u0 = .006  # inflow velocity [m/s]
        area = 1.e-4  # cross-sectional area [m**2]
        # Resolution: The PFR will be simulated by 'n_steps'
        n_steps = 5000
        # A Lagrangian particle is considered which travels through the
        # PFR. Its state change is computed by upwind time stepping. The
        # PFR result is produced by transforming the temporal resolution
        # into spatial locations. The spatial discretization is
        # therefore not provided a priori but is instead a result of the
        # transformation. import the gas model and set the initial
        # conditions
        gas = ct.Solution(self.mechanism)
        gas.TP = T0, pressure
        gas.set_equivalence_ratio(self.equiv_ratio, self.fuel, self.air)
        mass_flow_rate1 = u0 * gas.density * area
        # create a new reactor
        if self.moles:
            reactor = ct.IdealGasConstPressureMoleReactor(gas)
        else:
            reactor = ct.IdealGasConstPressureReactor(gas)
        reactor.volume = 1.0
        self.currRun.update({"thermo":{"mechanism": self.mechanism.split("/")[-1], "mole-reactor":self.moles, "nreactions":gas.n_reactions, "nspecies":gas.n_species, "fuel":self.fuel, "air": self.air, "equiv_ratio": self.equiv_ratio, "T0":T0, "P0":pressure, "V0":reactor.volume}})
        # create a reactor network for performing time integration
        self.net = ct.ReactorNet([reactor,])
        # apply numerical options
        self.apply_numerical_options()
        # approximate a time step to achieve a similar resolution as in
        # the next method
        t_total = length / u0
        currTime = 0
        states = ct.SolutionArray(gas, extra=['linIters', 'nonlinIters', 'sparsity'])
        sparsity = 0
        i = 1
        while currTime < t_total:
            # perform time integration
            currTime = self.net.step()
            sparsity += self.net.get_sparsity_percentage()
            i += 1
            if self.write:
                states.append(reactor.thermo.state, linIters=self.net.get_num_lin_iters(), nonlinIters=self.net.get_num_nonlin_iters(), sparsity=self.net.get_sparsity_percentage())
        if self.write:
            csvName = self.runName + "-" + "pressure" + ".csv"
            csvName = os.path.join(self.dataDir, csvName)
            states.write_csv(csvName, cols=('T', 'D', 'X', 'nonlinIters', 'linIters', 'sparsity'))
            self.currRun.update({"writefile": csvName.split("/")[-1]})
        # add numerical paramters to the run
        sparsity /= i
        self.currRun.update({"numerical":{"preconditioner":self.precon_on, "linear_solver":self.solver, "threshold":self.threshold, "totalNonlinIters":self.net.get_num_nonlin_iters(), "totalLinIters":self.net.get_num_lin_iters(), "average_sparsity":i}})

    @problem
    def volume_problem(self):
        """
        This problem was adapted from
        https://cantera.org/examples/python/reactors/fuel_injection.py.html

        Simulation of fuel injection into a vitiated air mixture to show
        formation of soot precursors.

        Demonstrates the use of a user-supplied function for the mass
        flow rate through a MassFlowController, and the use of the
        SolutionArray class to store results during reactor network
        integration and use these results to generate plots.
        """
        gas = ct.Solution(self.mechanism)
        # Create a Reservoir for the fuel inlet, set to pure dodecane
        gas.TPX = 300, 20*ct.one_atm, self.fuel+":1.0"
        inlet = ct.Reservoir(gas)
        # Create Reactor and set initial contents to be products of lean
        # combustion
        gas.TP = 1000, 20*ct.one_atm
        gas.set_equivalence_ratio(1, self.fuel, self.air)
        gas.equilibrate('TP')
        if self.moles:
            r = ct.IdealGasMoleReactor(gas)
        else:
            r = ct.IdealGasReactor(gas)
        r.volume = 0.001

        def fuel_mdot(t):
            """Create an inlet for the fuel, supplied as a Gaussian
            pulse"""
            total = 3.0e-3  # mass of fuel [kg]
            width = 0.5  # width of the pulse [s]
            t0 = 2.0  # time of fuel pulse peak [s]
            amplitude = total / (width * np.sqrt(2*np.pi))
            return amplitude * np.exp(-(t-t0)**2 / (2*width**2))

        mfc = ct.MassFlowController(inlet, r, mdot=fuel_mdot)
        # add thermo props to run dictionary
        self.currRun.update({"thermo":{"mechanism": self.mechanism.split("/")[-1], "mole-reactor":self.moles, "nreactions":gas.n_reactions, "nspecies":gas.n_species, "fuel":self.fuel, "air": self.air, "equiv_ratio": self.equiv_ratio, "T0":gas.T, "P0":gas.P, "V0":r.volume}})
        # Create the reactor network
        self.net = ct.ReactorNet([r])
        # Integrate for 10 seconds, storing the results for later
        # plotting
        tfinal = 10.0
        currTime = 0.0
        states = ct.SolutionArray(gas, extra=['tnow', 'linIters', 'nonlinIters', 'sparsity'])
        sparsity = 0
        i = 1
        while currTime < tfinal:
            # perform time integration
            currTime = self.net.step()
            sparsity += self.net.get_sparsity_percentage()
            i += 1
            if self.write:
                states.append(reactor.thermo.state, tnow=currTime, linIters=self.net.get_num_lin_iters(), nonlinIters=self.net.get_num_nonlin_iters(), sparsity=self.net.get_sparsity_percentage())

        if self.write:
            csvName = self.runName + "-" + "volume" + ".csv"
            csvName = os.path.join(self.dataDir, csvName)
            states.write_csv(csvName, cols=('T', 'D', 'X', 'nonlinIters', 'linIters', 'sparsity'))
            self.currRun.update({"writefile": csvName.split("/")[-1]})
        # add numerical paramters to the run
        sparsity /= i
        self.currRun.update({"numerical":{"preconditioner":self.precon_on, "linear_solver":self.solver, "threshold":self.threshold, "totalNonlinIters":self.net.get_num_nonlin_iters(), "totalLinIters":self.net.get_num_lin_iters(), "average_sparsity":sparsity}})

    @problem
    def network_problem(self):
        """
        This is adds an ideal gas const pressure reactor to the volume problem as an "atmosphere"
        """
        # set up atmospheric air
        air = ct.Solution(self.mechanism)
        # Create a Reservoir for entrainment of air
        air.TPX = 300, ct.one_atm, self.air
        inletAir = ct.Reservoir(air)
        # setup fuel
        gas = ct.Solution(self.mechanism)
        # Create a Reservoir for the fuel inlet, set to pure dodecane
        gas.TPX = 300, 20*ct.one_atm, self.fuel+":1.0"
        inlet = ct.Reservoir(gas)
        # Create Reactor and set initial contents to be products of lean
        # combustion
        gas.TP = 1000, 20*ct.one_atm
        gas.set_equivalence_ratio(1, self.fuel, self.air)
        gas.equilibrate('TP')
        # Create both reactors
        if self.moles:
            combustor = ct.IdealGasMoleReactor(gas)
            atmosphere = ct.IdealGasConstPressureMoleReactor(air)
        else:
            combustor = ct.IdealGasReactor(gas)
            atmosphere = ct.IdealGasConstPressureReactor(air)
        combustor.volume = 0.001
        atmosphere.volume = 1
        # add thermo props to run dictionary
        self.currRun.update({"thermo":{"mechanism": self.mechanism.split("/")[-1], "mole-reactor":self.moles, "nreactions":gas.n_reactions, "nspecies":gas.n_species, "fuel":self.fuel, "air": self.air, "equiv_ratio": self.equiv_ratio, "T0":gas.T, "P0":gas.P, "V0":combustor.volume}})

        # Use a variable mass flow rate to keep the residence time in
        def fuel_mdot(t):
            """Create an inlet for the fuel, supplied as a Gaussian
            pulse"""
            total = 3.0e-3  # mass of fuel [kg]
            width = 0.5  # width of the pulse [s]
            t0 = 2.0  # time of fuel pulse peak [s]
            amplitude = total / (width * np.sqrt(2*np.pi))
            return amplitude * np.exp(-(t-t0)**2 / (2*width**2))
        # mass flow function for entrainment
        def entrainment(t):
            return fuel_mdot(t)
        # Set mass flow controller
        inlet_mfc = ct.MassFlowController(inlet, combustor, mdot=fuel_mdot)
        # Entrainment mass flow controller
        inlet_mfc_air = ct.MassFlowController(inletAir, atmosphere, mdot=entrainment)
        # Pressure controller for mass into atmosphere
        outlet_mfc = ct.PressureController(combustor, atmosphere, master=inlet_mfc, K=0.01)
        # the simulation only contains one reactor
        self.net = ct.ReactorNet([combustor, atmosphere])
        # apply numerical options
        self.apply_numerical_options()
        # Making a loop to store data for entire network
        names_array = ['linIters', 'nonlinIters', 'sparsity']
        offset = len(names_array)
        state_len = gas.n_species + 1
        for c in range(state_len):
            names_array.append(combustor.component_name(c)+"-v")
        for c in range(state_len):
            names_array.append(atmosphere.component_name(c)+"-p")
        total_len = len(names_array)
        state_array = np.empty((0, total_len), dtype=float)
        working_array = np.ndarray((total_len,))
        working_array[:] = 0
        working_array[offset] = combustor.T
        working_array[offset+1:state_len+offset] = gas.X
        working_array[state_len + offset] = combustor.T
        working_array[state_len+offset+1:] = gas.X
        tf = 0.3
        curr_time = 0.0
        sparsity = 0
        i = 0
        self.net.set_initial_time(curr_time)
        while curr_time < tf:
            curr_time = self.net.step()
            sparsity += self.net.get_sparsity_percentage()
            i += 1
            if self.write:
                working_array[:] = 0
                working_array[0] = self.net.get_num_nonlin_iters()
                working_array[1] = self.net.get_num_lin_iters()
                working_array[2] = self.net.get_sparsity_percentage()
                working_array[offset] = combustor.T
                working_array[offset+1:state_len+offset] = gas.X
                working_array[state_len + offset] = combustor.T
                working_array[state_len+offset+1:] = gas.X
                state_array = np.append(state_array, np.array((working_array,)), axis=0)
        # write data out
        if self.write:
            csvName = self.runName + "-" + "network" + ".csv"
            csvName = os.path.join(self.dataDir, csvName)
            np.savetxt(csvName, state_array, delimiter=", ", header=", ".join(names_array))
            self.currRun.update({"writefile": csvName.split("/")[-1]})
        # add numerical paramters to the run
        sparsity /= i
        self.currRun.update({"numerical":{"preconditioner":self.precon_on, "linear_solver":self.solver, "threshold":self.threshold,  "totalNonlinIters":self.net.get_num_nonlin_iters(), "totalLinIters":self.net.get_num_lin_iters(), "average_sparsity":sparsity}})

    def __call__(self):
        # run all three problems
        try:
            self.pressure_problem()
        except Exception as e:
            self.logdata.update({"pressure_problem": {"status": "FAILED", "Exception": str(e)}})
        # Run volume problem
        try:
            self.volume_problem()
        except Exception as e:
            self.logdata.update({"volume_problem": {"status": "FAILED", "Exception": str(e)}})
        # Run network problem
        try:
            self.network_problem()
        except Exception as e:
            self.logdata.update({"network_problem": {"status": "FAILED", "Exception": str(e)}})
