import natsort
import os
import io
import sys
from astropy.coordinates import EarthLocation
from astropy import units as u
from ctapipe.core import Field, Tool, ToolConfigurationError
from ctapipe.core.traits import Dict, Float, Path, List, Unicode, Int, Bool
import pandas as pd

from startracker.analysis.fitter import *
from startracker.io.io import get_data

FIT_MODES = ['radec', 'y', 'xy', 'xyz']

class FitRunner(Tool):
    name = 'Startracker fit runner'
    description = 'Read files with the reconstructed star positions, performs the fit and calculates mispointing'

    telescope_coordinates = Dict({"longitude": 342.108612,
                                  "lattitude": 28.761389,
                                  "elevation": 2147},
                                 help="Telescope location, [deg, deg, m]").tag(config=True)

    focal_length = Float(28.0, help='Telescope focal length in meters').tag(config=True)
    run_number = Int(-1, help='Run number').tag(config=True)
    input_path = Path(default_value='/tmp/',
                      help='Path to the file(s) with star positions and images', exists=True).tag(config=True)
    output_path = Path(default_value='/tmp/', help='Output path',
                       directory_ok=True).tag(config=True)
    star_labels = List(help='List of stars to analyze according to NOMAD1 naming').tag(config=True)
    analysis_type = Unicode(default='by_run', help='Type of analysis: by run or by subrun').tag(config=True)
    use_errors = Bool(default=True,
                      help='Flag showing whether to use star positional errors in the fit').tag(config=True)
    input_files = []
    fit_results = {}
    final_results = None

    def setup(self):
        '''
        Setup the fit runner tool
        '''
        self.telescope_location = EarthLocation(
            lon=self.telescope_coordinates["longitude"] * u.deg,
            lat=self.telescope_coordinates["lattitude"] * u.deg,
            height=self.telescope_coordinates["elevation"] * u.m)

        if os.path.isfile(self.input_path):
            self.input_files.append(self.input_path)
        else:
            self.input_files = [f'{self.input_path}/{f}' for f in natsort.natsorted(os.listdir(self.input_path))]

        if len(self.input_files) == 0:
            raise ToolConfigurationError('At least one file with star tables should be provided')
        os.makedirs(self.output_path, exist_ok=True)

    def apply_coma_corrections(self, data):
        average_corr = 0.04446895891745561
        return data * (1-average_corr/2)

    def analyze(self, input_files, subrun=-1, use_errors=True):
        star_dataframe, self.star_labels = get_data(input_files, self.star_labels)
        self.log.info('Star labels from file: %s', self.star_labels)
        times = star_dataframe['t']
        pointings = SkyCoord(star_dataframe['ra'], star_dataframe['dec'], unit='deg', frame='icrs')
        idx = pd.IndexSlice
        data = np.asarray(star_dataframe.loc[:,idx[:, ["x", "y"]]]).T
        data = self.apply_coma_corrections(data)
        if use_errors:
            errors = np.asarray(star_dataframe.loc[:,idx[:, ["dx", "dy"]]]).T
        else:
            errors = None

        sf = StarFitter(self.star_labels, pointings, self.telescope_location, self.focal_length * u.m)
        for fit_mode in FIT_MODES:
            sf.fit(data,
                   errors,
                   times,
                   pointings,
                   fit_mode)
            if self.analysis_type == 'by_run':
                sf.plot(data, errors, times, f'{self.output_path}/fit_{fit_mode}.png')
            out = io.StringIO()
            sys.stdout = out
            sf.fit_summary.pprint()
            sys.stdout = sys.__stdout__
            self.log.info('Output for fit mode %s:\n%s', fit_mode, out.getvalue())
            if self.analysis_type == 'by_run':
                with open(f'{self.output_path}/fit_{fit_mode}.txt', 'w') as f:
                    f.write(out.getvalue())
            self.fit_results[fit_mode] = sf.fit_results
        results = pd.concat(self.fit_results, axis=1)
        run_stats = star_dataframe.describe()
        pointings_altaz = pointings.transform_to(AltAz(obstime=Time(times, format='unix_tai', scale='utc'),
                                                       location=self.telescope_location))
        zeniths = 90 - pointings_altaz.alt.to_value(u.deg)
        azimuths = pointings_altaz.az.to_value(u.deg)
        results['run'] = self.run_number
        results['subrun'] = subrun
        results['n_stars_used'] = len(self.star_labels)
        results['star_labels'] = [self.star_labels,]
        results['average_time'] = run_stats['t']['mean']
        results['min_time'] = run_stats['t']['min']
        results['max_time'] = run_stats['t']['max']
        results['average_zenith'] = zeniths.mean()
        results['min_zenith'] = zeniths.min()
        results['max_zenith'] = zeniths.max()
        results['std_zenith'] = zeniths.std()
        results['average_azimuth'] = azimuths.mean()
        results['min_azimuth'] = azimuths.min()
        results['max_azimuth'] = azimuths.max()
        results['std_azimuth'] = azimuths.std()
        results['average_ra'] = pointings.ra.mean().to_value(u.deg)
        results['std_ra'] = pointings.ra.std().to_value(u.deg)
        results['average_dec'] = pointings.dec.mean().to_value(u.deg)
        results['std_dec'] = pointings.dec.std().to_value(u.deg)
        return results

    def start(self):
        self.log.info('Star labels from the config: %s', self.star_labels)
        if self.analysis_type == 'by_run':
            self.final_results = self.analyze(self.input_files, use_errors=self.use_errors)
        elif self.analysis_type == 'by_subrun':
            results_list = []
            for filename in self.input_files:
                subrun = filename.split('.')[-2]
                results = self.analyze([filename,], subrun=subrun, use_errors=self.use_errors)
                results_list.append(results)
            self.final_results = pd.concat(results_list)


    def finish(self):
        self.final_results.to_csv(f'{self.output_path}/fit_results.csv')

def main():
    tool = FitRunner()
    tool.run()


if __name__ == 'main':
    main()
