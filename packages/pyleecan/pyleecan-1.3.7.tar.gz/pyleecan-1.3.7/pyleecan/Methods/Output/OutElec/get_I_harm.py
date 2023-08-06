from numpy import where, isclose, logical_not
from SciDataTool import Data1D


def get_I_harm(self):
    """Return the stator current harmonics in a DataFreq object

    Parameters
    ----------
    self : OutElec
        an OutElec object

    Returns
    -------
    I_harm: DataND
        stator current harmonics

    """

    # Generate current according to Id/Iq

    felec = self.felec
    I_fund_freq = self.Is.time_to_freq()

    results = I_fund_freq.get_along("freqs", "phase")

    # Remove fundamental value
    freqs = results["freqs"]
    ifund = where(logical_not(isclose(freqs, felec, rtol=1e-05)))[0]

    Freqs = Data1D(
        name="freqs",
        unit="Hz",
        values=results["freqs"][ifund],
    )

    I_harm = I_fund_freq.copy()
    I_harm.axes = [Freqs, I_fund_freq.axes[1]]
    I_harm.values = results["I_s"][ifund]

    return I_harm
