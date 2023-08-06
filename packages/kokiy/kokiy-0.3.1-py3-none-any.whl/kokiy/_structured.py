import numpy as np

from cloud2cloud import cloud2cloud


def get_uv(n_azi, n_longi, matrix_form=False, lims_azi=(0., 1.),
           lims_longi=(0., 1.)):
    u, v = [arr.T for arr in np.meshgrid(np.linspace(*lims_azi, n_azi),
                                         np.linspace(*lims_longi, n_longi))]

    if matrix_form:
        return np.stack((u, v), axis=-1)
    else:
        return u, v


def get_cond_bnds(uv):
    """Returns bool array with True for boundary nodes.
    """
    uv_resh = uv.reshape(-1, 2)
    cond = (uv_resh[:, 0] == 0) | (uv_resh[:, 1] == 0) |\
           (uv_resh[:, 0] == 1) | (uv_resh[:, 1] == 1)

    return cond.reshape(uv.shape[:-1])


def interp_on_uv(init_uv, data, new_uv, correct_bnds=True):

    new_data = cloud2cloud(init_uv, data, new_uv, stencil=4)

    if correct_bnds:
        init_cond_bnds = get_cond_bnds(init_uv)
        new_cond_bnds = get_cond_bnds(new_uv)

        bnds_data = cloud2cloud(init_uv[init_cond_bnds],
                                data[init_cond_bnds],
                                new_uv[new_cond_bnds], stencil=2)
        new_data[new_cond_bnds] = bnds_data

    return new_data
