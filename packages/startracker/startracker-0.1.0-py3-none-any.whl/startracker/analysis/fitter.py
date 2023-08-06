from astropy import units as u
from astropy.coordinates import SkyCoord, AltAz, ICRS
from astropy.time import Time
from astroquery.vizier import Vizier
from ctapipe.coordinates import EngineeringCameraFrame
import numpy as np
from scipy.odr import Model, RealData, ODR
import matplotlib
import matplotlib.pyplot as plt
import random
import pandas as pd
matplotlib.rcParams['figure.figsize'] = (8, 8)


class StarTracker:
    '''
    Utility class to provide the position of the star in the telescope's camera frame coordinates at a given time
    '''
    def __init__(self,
                 star_label,
                 star_coordinates,
                 telescope_location,
                 telescope_focal_length,
                 telescope_pointing,
                 pointing_label=None):
        '''
        Constructor

        :param str star_label: Star label
        :param SkyCoord star_coordinates: Star coordinates in ICRS frame
        :param EarthLocation telescope_location: Telescope location coordinates
        :param Quantity[u.m] telescope_focal_length: Telescope focal length [m]
        :param SkyCoord telescope_pointing: Telescope pointing in ICRS frame
        :param str pointing_label: Pointing label
        '''
        self.star_label = star_label
        self.star_coordinates_icrs = star_coordinates
        self.telescope_location = telescope_location
        self.telescope_focal_length = telescope_focal_length
        self.telescope_pointing = telescope_pointing
        self.pointing_label = pointing_label

    def position_in_camera_frame(self, timestamp, pointing=None, focal_correction=0):
        '''
        Calculates star position in the engineering camera frame

        :param astropy.Time timestamp: Timestamp of the observation
        :param SkyCoord pointing: Current telescope pointing in ICRS frame
        :param float focal_correction: Correction to the focal length of the telescope. Float, should be provided in meters

        :return: Pair (float, float) of star's (x,y) coordinates in the engineering camera frame in meters
        '''
        # If no telescope pointing is provided, use the telescope pointing, provided
        # during the class member initialization
        if pointing is None:
            pointing = self.telescope_pointing
        # Determine current telescope pointing in AltAz
        altaz_pointing = pointing.transform_to(AltAz(obstime=timestamp,
                                                     location=self.telescope_location))
        # Create current camera frame
        camera_frame = EngineeringCameraFrame(
                    telescope_pointing=altaz_pointing,
                    focal_length=self.telescope_focal_length + focal_correction * u.m,
                    obstime=timestamp,
                    location=self.telescope_location)
        # Calculate the star's coordinates in the current camera frame
        star_coords_camera = self.star_coordinates_icrs.transform_to(camera_frame)
        return (star_coords_camera.x.to_value(), star_coords_camera.y.to_value())


class StarFitter:
    '''
    Star trajectory fitting class
    '''
    def __init__(self, star_labels, telescope_pointing, telescope_location, focal_length):
        '''
        Constructor

        :param list star_labels: List of star labels according to NOMAD catalog
        :param SkyCoord telescope_pointing: Telescope pointing in ICRS frame
        :param EarthLocation telescope_location: Telescope location
        :param Quantity[u.m] telescope_focal_length: Telescope focal length [m]
        '''
        self.star_labels = star_labels
        self.telescope_pointing = telescope_pointing
        self.telescope_location = telescope_location
        self.focal_length = focal_length
        self.stars = []
        for star_label in star_labels:
            self.stars.append(self.init_star(star_label))
        self.fit_mode = 'xy'
        self.star_motion_model = Model(self.fit_function)
        self.fit_summary = None
        self.fit_resuts = None

    def init_star(self, star_label):
        '''
        Initialize StarTracker object for a given star

        :param str star_label: Star label according to NOMAD catalog

        :return: StarTracker object
        '''
        star = Vizier(catalog="NOMAD").query_constraints(NOMAD1=star_label)[0]
        star_coords = SkyCoord(star['RAJ2000'],
                               star['DEJ2000'],
                               unit='deg',
                               frame='icrs')
        st = StarTracker(star_label,
                         star_coords,
                         self.telescope_location,
                         self.focal_length,
                         self.telescope_pointing)
        return st

    def current_pointing(self, t):
        '''
        Retrieve current telescope pointing
        '''
        return self.telescope_pointing

    def fit_function(self, p, t):
        '''
        Construct the fit function

        :param p: Fit parameters
        :param array-like(float) t: Timestamp in UNIX_TAI format

        :return: 2D array of star coordinates: [[x_1], [y_1]...[x_N], [y_N]] where array.shape == (N(stars) * 2, len(t))
        '''
        time = Time(t, format='unix_tai', scale='utc')
        coord_list = []
        if self.fit_mode == 'radec':
            m_ra, m_dec = p
            new_ra = self.current_pointing(time).ra + m_ra * u.deg
            new_dec = self.current_pointing(time).dec + m_dec * u.deg
            new_pointing = SkyCoord(ICRS(ra=new_ra, dec=new_dec))
            for star in self.stars:
                x, y = star.position_in_camera_frame(time, new_pointing)
                coord_list.extend([x])
                coord_list.extend([y])
        elif self.fit_mode == 'y':
            dy = p
            for star in self.stars:
                x, y = star.position_in_camera_frame(time, self.current_pointing(time))
                coord_list.extend([x])
                coord_list.extend([y + dy])
        elif self.fit_mode == 'xy':
            for star in self.stars:
                dx, dy = p
                x, y = star.position_in_camera_frame(time, self.current_pointing(time))
                coord_list.extend([x + dx])
                coord_list.extend([y + dy])
        elif self.fit_mode == 'xyz':
            dx, dy, dz = p
            for star in self.stars:
                x, y = star.position_in_camera_frame(time, self.current_pointing(time), dz)
                coord_list.extend([x + dx])
                coord_list.extend([y + dy])
        return np.array(coord_list)

    def generate_mispointed_data(self, mispointing, time_range, random_shift=0):
        '''
        Generates mispointed and randomly shifted star positions. Serves for testing and/or illustration purposes.

        :param mispointing: Mispointing [RA, DEC] in degrees
        :param time_range: time range in UNIX_TAI seconds, np.array of astropy.time.Time objects
        :param random_shift: Random position shift in meters
        '''
        data = self.fit_function(mispointing, time_range)
        data = np.vectorize(lambda x: x + random.uniform(-random_shift, random_shift))(data)
        return data

    def fit(self, data, errors, time_range, pointings, fit_mode='xy'):
        '''
        Performs the ODR fit of stars trajectories and saves the results as self.fit_results

        :param array data: Reconstructed star positions, data.shape = (N(stars) * 2, len(time_range)), order: x_1, y_1...x_N, y_N
        :param array errors: Uncertainties on the reconstructed star positions. Same shape and order as for the data
        :param array time_range: Array of timestamps in UNIX_TAI format
        :param array-like(SkyCoord) pointings: Array of telescope pointings in ICRS frame
        :param str fit_mode: Fit mode. Can be 'y', 'xy' (default), 'xyz' or 'radec'.
        '''
        self.fit_mode = fit_mode
        if self.fit_mode == 'radec' or self.fit_mode == 'xy':
            init_mispointing=[0,0]
        elif self.fit_mode == 'y':
            init_mispointing=[0]
        elif self.fit_mode == 'xyz':
            init_mispointing=[0,0,0]
        self.telescope_pointing = pointings
        if errors is not None:
            rdata = RealData(x=time_range, y=data, sy=errors)
        else:
            rdata = RealData(x=time_range, y=data)
        odr = ODR(rdata, self.star_motion_model, beta0=init_mispointing)
        self.fit_summary = odr.run()
        if self.fit_mode == 'radec':
            self.fit_results = pd.DataFrame(data={'dRA'  : [self.fit_summary.beta[0]],
                                                  'dDEC' : [self.fit_summary.beta[1]],
                                                  'eRA'  : [self.fit_summary.sd_beta[0]],
                                                  'eDEC' : [self.fit_summary.sd_beta[1]]}
                                           )
        elif self.fit_mode == 'xy':
            self.fit_results = pd.DataFrame(data={'dX' : [self.fit_summary.beta[0]],
                                                  'dY' : [self.fit_summary.beta[1]],
                                                  'eX' : [self.fit_summary.sd_beta[0]],
                                                  'eY' : [self.fit_summary.sd_beta[1]]}
                                           )
        elif self.fit_mode == 'y':
            self.fit_results = pd.DataFrame(data={'dY' : [self.fit_summary.beta[0]],
                                                  'eY' : [self.fit_summary.sd_beta[0]]}
                                           )
        elif self.fit_mode == 'xyz':
            self.fit_results = pd.DataFrame(data={'dX' : [self.fit_summary.beta[0]],
                                                  'dY' : [self.fit_summary.beta[1]],
                                                  'dZ' : [self.fit_summary.beta[2]],
                                                  'eX' : [self.fit_summary.sd_beta[0]],
                                                  'eY' : [self.fit_summary.sd_beta[1]],
                                                  'eZ' : [self.fit_summary.sd_beta[2]]}
                                           )

    def plot(self, data, errors, time_range, store_to=None, show=False):
        '''
        Plot reconstructed star trajectories and fitted curves. Can only be called after the fit is performed

        :param array data: Reconstructed star positions, data.shape = (N(stars) * 2, len(time_range)), order: x_1,
        :param array errors: Uncertainties on the reconstructed star positions. Same shape and order as for the data
        :param array time_range: Array of timestamps in UNIX_TAI format
        :param str store_to: If not None, path to file where the plot is saved
        :param bool show: If True, the plot is immediately displayed
        '''
        if self.fit_summary is None:
            self.log.warning('Fit results not available. Perhaps you did not fit anything yet ;)')
            return
        fitted_trajectories = self.fit_function(self.fit_summary.beta, time_range)
        i = 0
        for label in self.star_labels:
            if errors is not None:
                plt.errorbar(data[i], data[i+1], xerr=errors[i], yerr=errors[i+1], label=f'{label} data')
            else:
                plt.errorbar(data[i], data[i+1], label=f'{label} data')
            plt.plot(fitted_trajectories[i], fitted_trajectories[i+1], label=f'{label} fit')
            i = i+2
        plt.xlim(-1.0, 1.0)
        plt.ylim(-1.0, 1.0)
        plt.xlabel('X [m]')
        plt.ylabel('Y [m]')
        plt.title('Engineering camera frame coordinate system')
        plt.legend()
        plt.grid()
        if store_to is not None:
            plt.savefig(store_to)
        if show:
            plt.show()
        plt.clf()
