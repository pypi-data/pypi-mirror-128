from .mechanism_base import MechanismBase
import cantera as ct


class GAS_DEF(MechanismBase):
    def __init__(self, *args, **kwargs):
        super(GAS_DEF, self).__init__(*args, **kwargs)
        self.mechanism = self.get_test_set_path('gas-def.yaml')
        self.fuel = 'CH4'


class Hydrogen(MechanismBase):
    def __init__(self, *args, **kwargs):
        super(Hydrogen, self).__init__(*args, **kwargs)
        self.mechanism = self.get_test_set_path('hydrogen-10.yaml')
        self.fuel = 'H2'


class MethaneGRI(MechanismBase):  # Hydrogen with more species
    def __init__(self, *args, **kwargs):
        super(MethaneGRI, self).__init__(*args, **kwargs)
        self.mechanism = self.get_test_set_path('gri-mech-55.yaml')
        self.fuel = 'CH4'


class DME(MechanismBase):
    def __init__(self, *args, **kwargs):
        super(DME, self).__init__(*args, **kwargs)
        self.mechanism = self.get_test_set_path('dme-propane-122.yaml')
        self.fuel = 'CH3OCH3'


class JetA(MechanismBase):
    def __init__(self, *args, **kwargs):
        super(JetA, self).__init__(*args, **kwargs)
        self.mechanism = self.get_test_set_path('jetA-detailed-NOx-203.yaml')
        self.fuel = 'POSF10325'


class NHeptane(MechanismBase):
    def __init__(self, *args, **kwargs):
        super(NHeptane, self).__init__(*args, **kwargs)
        self.mechanism = self.get_test_set_path('n-heptane-c7h16-654-4846.yaml')
        self.fuel = 'NC7H16'


class IsoOctane(MechanismBase):  # Iso-Octane
    def __init__(self, *args, **kwargs):
        super(IsoOctane, self).__init__(*args, **kwargs)
        self.mechanism = self.get_test_set_path('ic8-874.yaml')
        self.fuel = 'IC8H18'


class ThreeMethylHeptane(MechanismBase):
    """“Kinetic modeling of gasoline surrogate components and mixtures
under engine conditions | Elsevier Enhanced Reader.”
https://reader.elsevier.com/reader/sd/pii/S1540748910000787?token=7EE5B546D255AEA89A00CA8C8015063F3A98600E157AFBC19AB73BD38F1A5A81EE4B8F923AE3DF3629DC10661C6C81D2&originRegion=us-east-1&originCreation=20211027184033
(accessed Oct. 27, 2021).
    """
    def __init__(self, *args, **kwargs):
        super(ThreeMethylHeptane, self).__init__(*args, **kwargs)
        self.mechanism = self.get_test_set_path('3-methylheptane-c8h18-3-1378-8143.yaml')
        self.fuel = 'c8h18-3'


class NHexadecane(MechanismBase):
    """
    LNLL n-hexadecane
    """
    def __init__(self, *args, **kwargs):
        super(NHexadecane, self).__init__(*args, **kwargs)
        self.mechanism = self.get_test_set_path('n-hexadecane-nc16-h34-2115-13341.yaml')
        self.fuel = 'nc16h34'


class MethylFiveDeconate(MechanismBase):
    """
    LNLL methyl-5-deconate
    """
    def __init__(self, *args, **kwargs):
        super(MethylFiveDeconate, self).__init__(*args, **kwargs)
        self.mechanism = self.get_test_set_path('md5d-2649.yaml')
        self.fuel = 'md5d'


class MethylNineDeconate(MechanismBase):
    """
    LNLL methyl-9-deconate
    """
    def __init__(self, *args, **kwargs):
        super(MethylNineDeconate, self).__init__(*args, **kwargs)
        self.mechanism = self.get_test_set_path('md9d-3298.yaml')
        self.fuel = 'md9d'


class MethylDeconateNHeptane(MechanismBase):
    """
    LNLL methyldeconate with nheptane
    """
    def __init__(self, *args, **kwargs):
        super(MethylDeconateNHeptane, self).__init__(*args, **kwargs)
        self.mechanism = self.get_test_set_path('md-nc7-3787.yaml')
        self.fuel = 'md, nc7h16'


class TwoMethylnonadecane(MechanismBase):
    """
    S.M. Sarathy, M. Mehl, C. K. Westbrook, W. J. Pitz,C. Togbe, P.
    Dagaut, H. Wang, M.A. Oehlschlaeger, U. Niemann, K. Seshadri,P.S.
    Veloo, C. Ji, F.N. Egolfopoulos, T. Lu Comprehensive chemical
    kinetic modeling of the oxidation of 2-methylalkanes from C7 to C20
    Combustion and Flame 2011
    """
    def __init__(self, *args, **kwargs):
        super(TwoMethylnonadecane, self).__init__(*args, **kwargs)
        self.mechanism = self.get_test_set_path('mmc5-7171-38324.yaml')
        self.fuel = 'c20h42-2'
