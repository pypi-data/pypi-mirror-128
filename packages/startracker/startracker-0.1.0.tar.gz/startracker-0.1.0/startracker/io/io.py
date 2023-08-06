import h5py
import pandas as pd
from ctapipe.io import read_table

def get_dataset_keys(filename):
    """
    Return a list of all dataset keys in a HDF5 file
    Parameters
    ----------
    filename: str - path to the HDF5 file
    Returns
    -------
    list of keys
    """
    dataset_keys = []

    def walk(name, obj):
        if type(obj) == h5py._hl.dataset.Dataset:
            dataset_keys.append(name)
    with h5py.File(filename, "r") as file:
        file.visititems(walk)
    return dataset_keys


def read_star_table(filename, table_key):
    star_table = read_table(filename, table_key)
    df = pd.DataFrame({'x':star_table['reco_x'],
                       'y':star_table['reco_y'],
                       'dx':star_table['reco_dx'],
                       'dy':star_table['reco_dy']})
    return df

def read_time_pointing_table(filename):
    it = read_table(filename, '/startracker/images/variance_images')
    df = pd.DataFrame.from_dict({'t':it['timestamp'].unix_tai,
                                 'ra':it['ra'],
                                 'dec':it['dec']})
    return df

def get_data(filenames, star_labels=None):
    dfs = {}
    if len(star_labels) == 0:
        keys = get_dataset_keys(filenames[0])
        star_labels = [key.split('/')[-1][2:].replace('_', '-') for key in keys if 'stars' in key]
        star_keys = [f'/{key}' for key in keys if 'stars' in key]
    else:
        star_keys = [f"/startracker/images/stars/S_{k.replace('-', '_')}" for k in star_labels]
    for key in star_keys:
        df = pd.DataFrame(columns=['x', 'y', 'dx', 'dy'])
        for filename in filenames:
            df = df.append(read_star_table(filename, key))

        if df.dropna().shape[0] < 0.5 * df.shape[0]:
            # Drop the star dataset if the reconstructed data is not available for more than 50% of time points
            # TODO implement warning
            star_labels.remove(key.split('/')[-1][2:].replace('_', '-'))
            continue
        dfs[key] = df
    cdf = pd.concat(dfs, axis=1)
    time_df = pd.DataFrame(columns=['t', 'ra', 'dec'])
    for filename in filenames:
        time_df = time_df.append(read_time_pointing_table(filename))
    cdf['t'] = time_df['t']
    cdf['ra'] = time_df['ra']
    cdf['dec'] = time_df['dec']
    return cdf.dropna(), star_labels
