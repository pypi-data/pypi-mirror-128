from astropy import units as u
from astropy.coordinates import EarthLocation, SkyCoord, Angle
from astropy.time import Time
from astroquery.vizier import Vizier
from ctapipe.calib import CameraCalibrator
from ctapipe.coordinates import EngineeringCameraFrame
from ctapipe.core import Component, Container, Field, Map
from ctapipe.core.traits import (
    Bool, Integer, Float, List, Dict, Unicode, TraitError, observe, Path, AstroTime
)
from ctapipe.image import tailcuts_clean
from ctapipe.io import EventSeeker, EventSource, HDF5TableWriter
from ctapipe.visualization import CameraDisplay

from deprecated.sphinx import deprecated
from itertools import cycle

import copy
import matplotlib.pyplot as plt
import numpy as np


Vizier.ROW_LIMIT = -1

# see https://github.com/astropy/astropy/issues/6509
NAN_TIME = Time(0, format="mjd", scale="tai")

@deprecated(version='0.2', reason='Not very useful functionality')
def annotate(disp, geom, pixel_index, star_id, pmag, color='r', **kwargs):
    """
    Annotate pixel on the camera display image

    :param ctapipe.visualization.CameraDisplay disp: CameraDisplay object
    :param ctapipe.instrument.CameraGeometry geom: CameraGeometry for the current CameraDisplay
    :param int pixel_index: Index of pixel to annotate
    :param str star_id: Star label
    :param float pmag: Star magnitude
    :param str color: Color code for highlighter
    """
    x, y = geom.pix_x[pixel_index].value, geom.pix_y[pixel_index].value
    text = disp.axes.text(
                x,
                y,
                f'P-Mag {pmag:.2f}',
                color=color,
            )
    disp._axes_overlays.append(text)

class StarContainer(Container):
    '''
    Container describing a single star in the field of view.
    Star coordinates are provided in the engineering camera frame
    '''
    label = Field('', 'Star label', dtype=np.str_)
    magnitude = Field(-1, 'Star magnitude')
    expected_x = Field(np.nan * u.m, 'Expected star position (x)', unit=u.m)
    expected_y = Field(np.nan * u.m, 'Expected star position (y)', unit=u.m)

    reco_x = Field(np.nan * u.m, 'Reconstructed star position (x)', unit=u.m)
    reco_y = Field(np.nan * u.m, 'Reconstructed star position (y)', unit=u.m)
    reco_dx = Field(np.nan * u.m, 'Reconstructed star position error (x)', unit=u.m)
    reco_dy = Field(np.nan * u.m, 'Reconstructed star position error (y)', unit=u.m)
    timestamp = Field(NAN_TIME, 'Reconstruction timestamp')

    central_pixel = Field(-1, 'Star central pixel id')
    pixels = Field(np.full(7, -1), 'List of star pixel ids', dtype=np.int_, ndim=1)


class StartrackImageContainer(Container):
    '''
    Container describing a collection of stars in the image.
    '''
    timestamp = Field(NAN_TIME, 'Timestamp of the image')
    stars = Field(Map(StarContainer), 'Stars in the field of view')
    image = Field(None, 'Variance camera image', dtype=np.float32, ndim=1)
    ra = Field(np.nan * u.deg, 'Current pointing RAJ2000', unit=u.deg)
    dec = Field(np.nan * u.deg, 'Current pointing DECJ2000', unit=u.deg)


class StartrackImageCollection(Container):
    '''
    Collection of StartrackImageConainer objects
    '''
    source = Field('source', 'Source', dtype=np.str_)  # FIXME - clarify meaning
    run_number = Field(-1, 'Run number', dtype=np.int_)

    images = Field(Map(StartrackImageContainer), 'Images with stars in the engineering camera frame')


class StarExtractor(Component):
    '''
    Star Extractor component. Produces and writes to the output file the star variance images together with reference
    events and StarContainers for each star.
    '''
    telescope_id = Integer(1, help="Telescope ID").tag(config=True)
    telescope_location = Dict({
        "longitude" : 342.108612,
        "lattitude" : 28.761389,
        "elevation" : 2147
    }, help="Telescope location, longitude and lattitude should be expressed in deg, elevation - in meters").tag(config=True)

    cleaning = Dict({
        "bound_thresh" : 750,
        "pic_thresh" : 15000
    }, help="Image cleaning parameters").tag(config=True)

    input_files = List(help='List of input R0 files')

    max_images_per_file = Integer(None, help="Max number of images to produce for each data file, test-only option", allow_none=True).tag(config=True)
    skipping_interval = Integer(0, help="Number of events to skip between event "
                                "averaging").tag(config=True)
    events_per_image = Integer(200, help="Number of events to average in an image").tag(config=True)
    event_type = Integer(1, help="Event(trigger) type to use. Set 0 for simulations, 1 for normal "
                         "cherenkov events or 32 for trigger32 events").tag(config=True)
    check_broken_pixels = Bool(True, help="Check for broken pixels (PMTs off)").tag(config=True)
    check_star_detection = Bool(True, help="Check if expected stars are correctly "
                                "detected").tag(config=True)
    min_star_prominence = Integer(3, help="Minimal star prominence over the background in terms of "
                              "NSB variance std deviations").tag(config=True)
    max_star_magnitude = Float(7.0, help="Maximal magnitude of the star to be considered in the "
                               "analysis").tag(config=True)
    min_distance_between_stars = Float(0.7, help='Minimal distance between stars',
                                       unit=u.deg).tag(config=True)
    max_star_offset = Float(2.0, help='Maximal offset from the center of the camera for '
                            'stars').tag(config=True)


    def __init__(self, config=None, parent=None, input_files=[], pointing_mode='follow', **kwargs):
        '''
        Constructor. Extracts the sky region of interest and selects the stars in the field of view according to
        criterias specified in the configuration. Celestial objects are selected from the NOMAD catalog using Vizier
        API.

        :param Config config: Component configuration
        :param ctapipe.core.Tool parent: Parent Tool instance
        :param list input_files: List of input files
        :param str pointing_mode: Telescope pointing mode. Currently only "follow" mode is supported
        '''
        super().__init__(config=config, parent=parent, **kwargs)
        self.input_files = input_files
        self.camera_geometry = None
        self.pointing = None
        self.location=EarthLocation(
            lon=self.telescope_location["longitude"] * u.deg,
            lat=self.telescope_location["lattitude"] * u.deg,
            height=self.telescope_location["elevation"] * u.m)

        # For the moment support only one run (or its subruns)
        with EventSource(input_url=self.input_files[0], max_events=1, config=self.config) as src:
            self.camera_geometry = src.subarray.tel[self.telescope_id].camera.geometry
            self.focal_length = src.subarray.tel[self.telescope_id].optics.equivalent_focal_length
            self.pixel_raduis = self.camera_geometry.pixel_width[0] # assume identical pixels
            event=next(iter(src))
            self.pointing = SkyCoord(az=event.pointing.tel[self.telescope_id].azimuth,
                                     alt=event.pointing.tel[self.telescope_id].altitude,
                                     frame="altaz",
                                     obstime = event.trigger.time.utc,
                                     location=self.location)

            self.config.EventTimeCalculator.dragon_reference_counter = int(
                src.time_calculator._dragon_reference_counter[self.telescope_id])
            self.config.EventTimeCalculator.dragon_reference_time = int(
                src.time_calculator._dragon_reference_time[self.telescope_id])

            module_ids = src.camera_config.lstcam.expected_modules_id
            mod_statuses = event.lst.tel[self.telescope_id].evt.module_status
            module_id = module_ids[np.where(mod_statuses != 0)[0][0]]
            self.config.EventTimeCalculator.dragon_module_id = int(module_id)
            self.config.EventTimeCalculator.extract_reference = False

            self.pointing = self.pointing.transform_to('icrs')
            self.log.info('Telescope pointing: \n%s', self.pointing)
            self.log.info('Array pointing')
            self.log.info(event.pointing.array_ra)
            self.log.info(event.pointing.array_dec)
        #celestial_objects_in_fov = Vizier.query_region(self.pointing, radius=Angle(2.0, "deg"), catalog='I/305')[0]
        celestial_objects_in_fov = Vizier.query_region(self.pointing, radius=Angle(2.0, "deg"),
                                                       catalog='NOMAD')[0]
        self.log.info('Celestial objects in the field of view:\n%s', celestial_objects_in_fov)
        self.stars_in_fov = self.select_stars(celestial_objects_in_fov)
        #color_list = list('bgrcmyk')
        #self.colors = cycle(color_list[:len(self.stars_in_fov)])
        self.log.info('Selected stars in the field of view:\n%s', self.stars_in_fov)
        self.image_collection = StartrackImageCollection(run_number=parent.run_number)
        self.workdir = parent.workdir
        if pointing_mode != 'follow':
            raise ToolConfigurationError('Only "follow" pointing mode is supported, requested pointing mode is %s',
                                         pointing_mode)

    def select_stars(self, objects_in_fov):
        '''
        Select the stars from the celestial objects in the field of view based on their brightness and the distance
        between them. Stars magnitude is measured in B-band (blue).
        '''
        stars_in_fov = objects_in_fov[objects_in_fov['Bmag'] < self.max_star_magnitude]
        # FIXME add distance filtering
        return stars_in_fov

    def write_image_collection(self, subrun_number):
        '''
        Writes the startracker output into the HDF5 file

        :param int subrun_number: Subrun number
        '''
        with HDF5TableWriter(f'{self.workdir}/out/run_{self.image_collection.run_number}.{subrun_number}.h5',
                             group_name='startracker', mode='w') as writer:
            #writer.exclude('/startracker/meta', 'images')
            #writer.write('meta', self.image_collection)
            #TODO figure out meta info, perhaps reimplement writing image by image
            for evtid, image  in self.image_collection.images.items():
                writer.exclude('images/variance_images', 'stars')
                writer.write('images/variance_images', image)
                for index, star in image.stars.items():
                    # Take the star ID according to catalog, replace - with _ and prepend with S_ 
                    # to preserve NaturalNaming compatibility
                    star_id = f'S_{star.label.replace("-", "_")}'
                    writer.exclude(f'images/stars/{star_id}', 'label')
                    writer.write(f'images/stars/{star_id}', star)

    def produce(self, subrun=0):
        '''
        Main production method. Called by production Tool (image_producer)

        :param int subrun: Number of subrun to process
        '''
        self.log.info('ImageProducer.produce() called')
        self.log.info('to analyze:\n%s', self.input_files)
        self.log.debug('Config\n%s', self.config)
        filename = self.input_files[subrun]
        src = EventSource(input_url=filename, max_events=None, config=self.config)
        images, reference_events = self.sum_events(src)
        self.detect_stars(images, reference_events)
        self.log.info("Filled image collection\n%s",self.image_collection)
        self.write_image_collection(subrun)


    def sum_events(self, source):
        '''
        Retrieve variance images according to the configuration. Averages N(configurable) events to produce one image in
        order to reduce EAS or NSB related flickering

        :param EventSource source: ctapipe.io.EventSource object

        :return: List of variance images and corresponding reference events 
        '''
        counter = 0
        expected_star_pixels = []
        images = []
        reference_events = []
        event_variance_list = []
        # Calibrator is needed to extract charge image
        calibrator = CameraCalibrator(subarray=source.subarray,
                                      image_extractor_type="LocalPeakWindowSum",
                                      config=self.config)
        disp = CameraDisplay(self.camera_geometry)
        #disp.add_colorbar()
        for event in source:
            # Skip the events with wrong trigger type
            if event.trigger.event_type.value != self.event_type:
                self.log.debug('Skipping event with event type %s, requested event type %s',
                               event.trigger.event_type.value, self.event_type)
                continue

            # Identify and skip flasher events
            # TODO check if flasher events are now correctly identified and removed based on event type
            max_pixel_values = np.max(event.r0.tel[self.telescope_id].waveform[0, :, :], axis = 1)
            if np.count_nonzero(max_pixel_values > 1000) > 1500:
                self.log.debug('Skipping flasher event')
                continue

            # Event is good for further use, increment event counter
            counter += 1
            calibrator(event)

            # Check if event is first in the bunch and save as reference event
            # and determine the expected star pixels
            if counter % self.events_per_image == 1:
                reference_events.append(copy.deepcopy(event))
                expected_star_pixels = self.get_expected_star_pixels(event)

            pixel_charges = event.dl1.tel[self.telescope_id].image
            pixel_variances = np.var(event.r1.tel[self.telescope_id].waveform, axis = 1)

            # Determine pixels supposedly hit by the EAS photons
            shower_mask = tailcuts_clean(self.camera_geometry, pixel_charges,
                                         picture_thresh=self.cleaning['pic_thresh'],
                                         boundary_thresh = self.cleaning['bound_thresh'])
            # Replace variance values in EAS-hit pixels with the average
            # For averaging get all pixels except those hit by EAS and where the stars are expected
            averaging_mask = copy.deepcopy(shower_mask)
            averaging_mask[expected_star_pixels] = True
            pixel_variances[shower_mask] = np.mean(pixel_variances[~averaging_mask])
            event_variance_list.append(pixel_variances)
            if counter % self.events_per_image == 0:
                # Requested number of events to complete one average image has been processed
                # Compute and  append average image to images list and flush the event variance list
                average_image = np.sum(event_variance_list, axis=0) / len(event_variance_list)
                images.append(average_image)
                expected_star_pixels = []
                event_variance_list = []
                if self.max_images_per_file is not None:
                    if counter % (self.max_images_per_file * self.events_per_image) == 0:
                        self.log.info('Max number of images per file has been reached, stop iteration')
                        break
                # Skip interval
                try:
                    for i in range(self.skipping_interval): next(iter(source))
                except StopIteration:
                    self.log.info('End of file reached')
                    break

        return images, reference_events

    def detect_stars(self, images, reference_events):
        '''
        Star detection function. Constructs the star cluster and reconstruct star position for each star selected for
        analysis. Fills the container tree with the reconstructed parameters

        :param list images: List of variance images
        :param list reference_events: List of reference events
        '''
        self.log.info('detect_stars called')
        self.log.info('Number of Images: %s', len(images))
        disp = CameraDisplay(self.camera_geometry)
        #disp.add_colorbar()
        for reference_event, image in zip(reference_events, images):
            pixels_to_highlight = []
            time = reference_event.trigger.time
            current_pointing = SkyCoord(az=reference_event.pointing.tel[self.telescope_id].azimuth,
                                        alt=reference_event.pointing.tel[self.telescope_id].altitude,
                                        frame="altaz",
                                        obstime = time.utc,
                                        location=self.location)

            self.log.info("Pointing from event %s with timestamp %s:\nAzimuth: %s, altitude: %s",
                          reference_event.index.event_id,
                          time.unix_tai,
                          reference_event.pointing.tel[self.telescope_id].azimuth.to(u.deg),
                          reference_event.pointing.tel[self.telescope_id].altitude.to(u.deg))
            camera_frame = EngineeringCameraFrame(
                telescope_pointing=current_pointing,
                focal_length=self.focal_length,
                obstime=time.utc,
                location=self.location)

            expected_star_pixels = self.get_expected_star_pixels(reference_event)
            # Calculate the average NSB
            star_mask = np.ones(image.size, dtype=bool)
            star_mask[expected_star_pixels] = False
            nsb = np.mean(image[star_mask])
            nsb_std = np.std(image[star_mask])
            clean_image = image - nsb # TODO verify!
            clean_image[clean_image<0] = 0 # replace neg var with 0
            disp.image = clean_image
            image_container = StartrackImageContainer(timestamp=time,
                                                      ra=current_pointing.transform_to('icrs').ra,
                                                      dec=current_pointing.transform_to('icrs').dec,
                                                      image=clean_image)
            for i, star in enumerate(self.stars_in_fov):
                reco_star = self.reco_star(star, time,  camera_frame, clean_image, nsb_std)
                image_container.stars[i] = reco_star
                #pixels_to_highlight.extend(reco_star.pixels)
                #annotate(disp, self.camera_geometry, reco_star.central_pixel, reco_star.label, reco_star.magnitude)
            self.log.info('Filled image container\n%s',image_container)
            self.image_collection.images[reference_event.index.event_id] = image_container
            #disp.highlight_pixels(pixels_to_highlight, color='r', alpha=0.5)
            #plt.savefig(f'./tests/out/image_{reference_event.index.event_id}.png')

    def get_single_star_expected_pixels(self, star, camera_frame):
        '''
        Reconstruct expected cluster of pixels observing the star

        :param StarContainer star: Star of interest
        :param EngineeringCameraFrame camera_frame: Engineering camera frame coorindate system

        :return: Array of cluster pixel indices
        '''
        star_coords = SkyCoord(star['RAJ2000'], star['DEJ2000'], unit='deg', frame='icrs')
        star_coords = star_coords.transform_to(camera_frame)
        guessed_central_pixel = self.camera_geometry.transform_to(camera_frame).position_to_pix_index(
            star_coords.x,
            star_coords.y)
        self.log.info('Expected star coordinates:\nx = %s, y = %s', star_coords.x, star_coords.y)
        self.log.info('Guessed central pixel: %s', guessed_central_pixel)
        cluster = copy.deepcopy(self.camera_geometry.neighbors[guessed_central_pixel])
        cluster.append(guessed_central_pixel)
        return cluster

    def get_expected_star_pixels(self, reference_event):
        '''
        Transform the RA/DEC coordinates of the stars in the f.o.v. to the camera pixels

        :param Event reference_event: Reference event

        :return: List of pixel IDs supposedly illuminated by stars
        '''
        res = []
        current_pointing = SkyCoord(az=reference_event.pointing.tel[self.telescope_id].azimuth,
                                    alt=reference_event.pointing.tel[self.telescope_id].altitude,
                                    frame="altaz",
                                    obstime = reference_event.trigger.time.utc,
                                    location=self.location)
        camera_frame = EngineeringCameraFrame(
            telescope_pointing=current_pointing,
            focal_length=self.focal_length,
            obstime=reference_event.trigger.time.utc,
            location=self.location)
        for star in self.stars_in_fov:
            star_pixels = self.get_single_star_expected_pixels(star, camera_frame)
            res.extend(star_pixels)
        return res

    def reco_star(self, star_t, timestamp, camera_frame, image, nsb_std):
        '''
        Reconstruct the star position and associated uncertainties

        :param Table star_t: Star of interest as extracted from NOMAD catalog
        :param astropy.Time timestamp: Timestamp of observation corresponding to a given variance image
        :param EngineeringCameraFrame camera_frame: Engineering camera frame coordinate system
        :param array image: Variance image in form of numpy.array
        :param float nsb_std: Night sky background standard deviation (used to verify star detection)

        :return: Filled StarContainer object
        '''
        self.log.info('Star \n%s', star_t)
        star_coords = SkyCoord(star_t['RAJ2000'], star_t['DEJ2000'], unit='deg', frame='icrs')
        star_coords = star_coords.transform_to(camera_frame)
        star = StarContainer(
            label=star_t['NOMAD1'],
            magnitude=star_t['Bmag'],
            expected_x=star_coords.x,
            expected_y=star_coords.y,
            timestamp=timestamp)
        guessed_star_pixels = self.get_single_star_expected_pixels(star_t, camera_frame)
        self.log.info("Guessed cluster is %s", guessed_star_pixels)
        corrected_central_pixel = guessed_star_pixels[np.argmax(image[guessed_star_pixels])]
        self.log.info("Corrected central pixel for star %s is %s", star.label, corrected_central_pixel)
        corrected_cluster = copy.deepcopy(self.camera_geometry.neighbors[corrected_central_pixel])
        self.log.info("Corrected cluster is %s", corrected_cluster)
        corrected_cluster.append(corrected_central_pixel)
        self.log.info("Corrected cluster with central pixel is %s", corrected_cluster)

        # Check if star prominence over the background is sufficient for detection
        star_detected = False
        for pix in corrected_cluster:
            if image[pix] > self.min_star_prominence * nsb_std:
                star_detected = True
                break
        if not star_detected:
            self.log.info('Star can not be detected')
            return star

        # TODO Implement correct clustering and cog determination
        star.central_pixel = corrected_central_pixel
        self.log.info('Coordinates of central pixel w.r.t. to camera center are:\n x = %s, y = %s',
                      self.camera_geometry.transform_to(camera_frame).pix_x[corrected_central_pixel],
                      self.camera_geometry.transform_to(camera_frame).pix_y[corrected_central_pixel]
                     )
        if len(corrected_cluster) < 7:
            corrected_cluster.extend( (7-len(corrected_cluster)) * [-1,])
        star.pixels = np.asarray(corrected_cluster)
        star.reco_x = np.average(self.camera_geometry.transform_to(camera_frame).pix_x[star.pixels],
                                 axis=None,
                                 weights=image[star.pixels],
                                 returned=False)
        star.reco_y = np.average(self.camera_geometry.transform_to(camera_frame).pix_y[star.pixels],
                                 axis=None,
                                 weights=image[star.pixels],
                                 returned=False) 
        # Naive error propagation:
        # Treat each pixel as a circle with a radius r, then 
        # err(x,y) = r * sqrt( sum(w ** 2) ), where w are the weight of each contributing pixel
        weights = image[star.pixels]/np.sum(image[star.pixels])
        error = self.pixel_raduis * np.sqrt(np.sum(np.square(weights), axis=None))
        star.reco_dx = error
        star.reco_dy = error

        return star
