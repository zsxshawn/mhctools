# netmhc_pan41.py

from .base_commandline_predictor import BaseCommandlinePredictor
from .parsing import parse_netmhc41_stdout
from functools import partial
import tempfile

class NetMHCpan41(BaseCommandlinePredictor):
    def __init__(
            self,
            alleles,
            custom_mhc_sequences=None,
            default_peptide_lengths=[9],
            program_name="netMHCpan",
            process_limit=-1,
            mode="binding_affinity",
            extra_flags=[]):
        """
        Wrapper for NetMHCpan4.1.

        The mode argument should be one of "binding_affinity" (default) or
        "elution_score".
        """

        # The -BA flag is required to predict binding affinity
        if mode == "binding_affinity":
            flags = ["-BA"]
        elif mode == "elution_score":
            flags = []
        else:
            raise ValueError("Unsupported mode", mode)

        self.custom_mhc_sequences = custom_mhc_sequences

        BaseCommandlinePredictor.__init__(
            self,
            program_name=program_name,
            alleles=alleles,
            default_peptide_lengths=default_peptide_lengths,
            parse_output_fn=partial(parse_netmhc41_stdout, mode=mode),
            supported_alleles_flag="-listMHC",
            input_file_flag="-f",
            length_flag="-l",
            allele_flag="-a",
            extra_flags=flags + extra_flags,
            process_limit=process_limit)

    def prepare_input_file(self, peptides):
        peptide_file = super(NetMHCpan41, self).prepare_input_file(peptides)

        if self.custom_mhc_sequences:
            with tempfile.NamedTemporaryFile(delete=False, mode='w') as custom_mhc_file:
                custom_mhc_file.write(self.custom_mhc_sequences)
            self.allele_file = custom_mhc_file.name
            self.extra_flags += ["-a", self.allele_file]

        return peptide_file


class NetMHCpan41_EL(NetMHCpan41):
    """
    Wrapper for NetMHCpan4 when the preferred mode is elution score
    """
    def __init__(
            self,
            alleles,
            custom_mhc_sequences=None,
            default_peptide_lengths=[9],
            program_name="netMHCpan",
            process_limit=-1,
            extra_flags=[]):
        NetMHCpan41.__init__(
            self,
            alleles=alleles,
            custom_mhc_sequences=custom_mhc_sequences,
            default_peptide_lengths=default_peptide_lengths,
            program_name=program_name,
            process_limit=process_limit,
            mode="elution_score",
            extra_flags=extra_flags)


class NetMHCpan41_BA(NetMHCpan41):
    """
    Wrapper for NetMHCpan4 when the preferred mode is binding affinity
    """
    def __init__(
            self,
            alleles,
            custom_mhc_sequences=None,
            default_peptide_lengths=[9],
            program_name="netMHCpan",
            process_limit=-1,
            extra_flags=[]):
        NetMHCpan41.__init__(
            self,
            alleles=alleles,
            custom_mhc_sequences=custom_mhc_sequences,
            default_peptide_lengths=default_peptide_lengths,
            program_name=program_name,
            process_limit=process_limit,
            mode="binding_affinity",
            extra_flags=extra_flags)
