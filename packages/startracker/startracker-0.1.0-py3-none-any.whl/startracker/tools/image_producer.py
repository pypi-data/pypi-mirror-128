import os
import pickle
from simple_slurm import Slurm

from ctapipe.core import Tool, ToolConfigurationError
from ctapipe.core.traits import Integer, Path, Dict

from startracker.analysis.image import StarExtractor, StartrackImageCollection


class ImageProducer(Tool):
    name = ' Startracker image producer'
    description = 'Read input files and produces grid of stars'

    classes = [StarExtractor, ]
    # TODO check if the run table (i.e. normal data run to analyze and corresponding calibration and
    # pedestal runs can be automatically generated from the data taking/shift report
    data_path = Path(default_value='/tmp', help='Path to telescope data location', exists=True, directory_ok=True,
                     file_ok=False).tag(config=True)
    date = Integer(help='Data taking date as integer in format YYYYMMDD', allow_none=False).tag(config=True)
    run_number = Integer(-1, help='Run number', allow_none=False).tag(config=True)
    workdir = Path(default_value='/tmp', help='Path to workdir', directory_ok=True,
                   file_ok=False).tag(config=True)
    slurm_parameters = Dict(help='Slurm parameters').tag(config=True)
    jobid = -1


    def setup(self):
        '''
        Setup the startracker image producer tool
        '''
        try:
            # LST-1.4.Run05443.0067.fits.fz
            # Temporary hack to have only one stream FIXME
            input_files = [os.path.join(self.data_path, fname) for fname in os.listdir(self.data_path)
                           if f'LST-1.1.Run{self.run_number:05d}' in fname]
        except IndexError:
            raise ToolConfigurationError('Path to the telescope data should point to a folder with the run data'
                                         ' in files following naming template "xxx.Run<run_number>.yyyy.fits.fz"')
        if not input_files:
            raise ToolConfigurationError(f'No data corresponding to run {self.run_number} is found under {self.data_path}')

        self.image_collection = StartrackImageCollection()
        self.star_extractor = StarExtractor(parent=self, input_files=sorted(input_files))
        # Create required working directory with subdirectories
        os.makedirs(self.workdir, exist_ok=True)
        os.makedirs(f'{self.workdir}/log/', exist_ok=True)
        os.makedirs(f'{self.workdir}/error/', exist_ok=True)
        os.makedirs(f'{self.workdir}/out/', exist_ok=True)
        with open(f'{self.workdir}/star_extractor.pickle', 'wb') as f:
            pickle.dump(self.star_extractor, f)

    def start(self):
        slurm = Slurm(array=range(len(self.star_extractor.input_files)),
                      output=f'{self.workdir}/log/{Slurm.JOB_ARRAY_MASTER_ID}_{Slurm.JOB_ARRAY_ID}.log',
                      error=f'{self.workdir}/error/{Slurm.JOB_ARRAY_MASTER_ID}_{Slurm.JOB_ARRAY_ID}.err',
                      *self.config['SlurmParameters'])
        slurm_cmd = f'process_subrun -p {self.workdir}/star_extractor.pickle -n '
        self.jobid = slurm.sbatch(slurm_cmd + Slurm.SLURM_ARRAY_TASK_ID)

    def finish(self):
        self.log.info('Submitted an array of %s jobs with ID %s',
                      len(self.star_extractor.input_files), self.jobid)


def main():
    tool = ImageProducer()
    tool.run()


if __name__ == 'main':
    main()
