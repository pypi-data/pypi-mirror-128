import numpy as np
from scipy.spatial.transform import Rotation as R

from kokiy.shell_2d import Shell2D
from kokiy.axishell import _compute_shell_crest


ATOL = 1e-8


class TorchShell(Shell2D):
    geom_type = 'torch'

    def __init__(self, n_azi, n_longi, pt_left, pt_right, radius_left,
                 radius_right, ecc_pt):
        super().__init__(n_azi, n_longi)

        self.pt_left = np.array(pt_left)
        self.pt_right = np.array(pt_right)
        self.ecc_pt = np.array(ecc_pt)
        self.radius_left = radius_left
        self.radius_right = radius_right

        # useful
        self._direc = self.pt_right - self.pt_left
        self._direc_unit = self._direc / np.linalg.norm(self._direc)

        self._ecc = self.ecc_pt - self.pt_right
        self._verify_ecc()
        self._ecc_unit = self._ecc / np.linalg.norm(self._ecc)

        self._build_shell()

    def _verify_ecc(self):
        if abs(np.sum(self._ecc)) < ATOL and abs(np.prod(self._ecc)) < ATOL:
            raise Exception('Null eccentricities are not accepted')

        if abs(np.dot(self._ecc, self._direc)) > ATOL:
            raise Exception('Eccentricity must be perpendicular to axis')

    def _build_shell(self):

        # Construct Shell Crest
        ctrl_pts_r = np.array([self._get_radius_sect(v) for v in self.v[0]])
        shell_crest = _compute_shell_crest(self.v[0], ctrl_pts_r, self.shape[1])

        # define directions
        center_vec = np.array([self._direc_unit * v for v in self.v[0]])

        # Compute radius and theta matrices of shape (n_azi, n_longi)
        self.rad, self.theta, aux_normals = self._get_rad_theta_aux_normals(ctrl_pts_r,
                                                                            center_vec)

        # get xyz
        xyz = []
        for i, sect_center in enumerate(center_vec):
            rotations = [R.from_rotvec(theta * self._direc_unit) for theta in self.theta[:, i]]
            rad_direcs = np.array([rotation.apply(self._ecc_unit) for rotation in rotations])

            xyz.append(sect_center + np.array([sect_radius * rad_direc for sect_radius, rad_direc in zip(self.rad[:, i], rad_direcs)]))

        self.x, self.y, self.z = [np.take(np.array(xyz), i, -1).T for i in range(3)]

        normals = self._correct_normals(aux_normals, self.rad)
        self.n_x, self.n_y, self.n_z = [np.take(np.array(normals), i, -1) for i in range(3)]
        shell_crest_scaled = shell_crest.copy()
        shell_crest_scaled[0] *= np.linalg.norm(self._direc)

        # Compute du, dv matrix of shape (n_azi, n_longi)
        longi_vals = np.tile(shell_crest_scaled[0], (self.shape[0], 1))
        self.du = np.pad(np.sqrt(np.diff(longi_vals, axis=1) ** 2
                                 + np.diff(self.rad, axis=1) ** 2),
                         ((0, 0), (1, 0)), 'edge')
        self.dv = self.rad * np.pad(np.diff(self.theta, axis=0),
                                    ((1, 0), (0, 0)), 'edge')

        # Compute weight intervals in u and v directions array of shape (n_transvers, n_longi)
        self.dwu, self.dwv = self._compute_weight_interv_adim(self.du, self.dv)

        # Compute surface nodes array of shape (n_transvers, n_longi)
        self.surf = self._compute_surf(self.dwu, self.dwv)

    def _get_radius_sect(self, v):
        return (self.radius_right - self.radius_left) * v + self.radius_left

    def _get_eccentricity_sect(self, v):
        return self._ecc * v

    def _get_rad_theta_aux_normals(self, ctrl_pts_r, center_vec):

        min_theta, max_theta = 0., np.deg2rad(360)
        theta_vec = np.linspace(min_theta, max_theta, num=self.shape[0])
        lim_theta_right = np.abs(np.arctan2(self.radius_right,
                                            np.linalg.norm(self._ecc)))

        # get phis (angles in circular region)
        phis = self._get_phis(theta_vec, lim_theta_right)

        normal_90, normal_270 = self._get_planar_region_normals()

        rads = []
        thetas = []
        normals = []

        for sect_rad, sect_center, v in zip(ctrl_pts_r, center_vec, self.v[0]):
            sect_ecc = self._get_eccentricity_sect(v)
            sect_ecc_norm = np.linalg.norm(sect_ecc)

            lim_theta = np.abs(np.arctan2(sect_rad, sect_ecc_norm))

            corr_coeff = self._compute_corr_coeff(lim_theta)

            rads_ = []
            thetas_ = []
            normals_ = []
            for phi, theta in zip(phis, theta_vec):
                if phi is None:  # rectangular region
                    theta_ = self._get_theta_sect_rect(v, theta, sect_rad)
                    rad_ = np.abs(sect_rad / np.sin(theta_))
                    normal_ = normal_90 if theta_ < np.pi else normal_270

                else:
                    theta_ = self._get_theta_sect_via_phi(theta, phi, v, corr_coeff)
                    rot_angle = phi[0]
                    rotation = R.from_rotvec(rot_angle * self._direc_unit)
                    radius_vec = self._ecc_unit * sect_rad

                    if phi[1] == np.pi:
                        vec = -sect_ecc + rotation.apply(-radius_vec)
                        normal_ = -rotation.apply(self._ecc_unit)
                    else:
                        vec = sect_ecc + rotation.apply(radius_vec)
                        normal_ = rotation.apply(self._ecc_unit)

                    rad_ = np.linalg.norm(vec)

                rads_.append(rad_)
                thetas_.append(theta_)
                normals_.append(normal_)

            rads.append(rads_)
            thetas.append(thetas_)
            normals.append(normals_)

        return np.array(rads).T, np.array(thetas).T, np.array(normals).transpose(1, 0, 2)

    def _get_planar_region_normals(self):
        rotations = [R.from_rotvec(rot_angle * self._direc_unit) for rot_angle in [np.pi / 2, 3 / 2 * np.pi]]
        return [rotation.apply(self._ecc_unit) for rotation in rotations]

    def _get_horiz_dist_sect(self, v, theta):
        """Gets horizontal distance in planar region.
        """
        return v * self.radius_right / np.tan(theta)

    def _get_phis(self, theta_vec, lim_theta_right):
        """Get angles of rotation of right face.

        Within the circular region, these angles are kept among layers. Outside
        the circular region it returns None.
        """
        corr_coeff_right = self._compute_corr_coeff(lim_theta_right)

        phis = []
        for theta in theta_vec:
            if theta < lim_theta_right:
                phi = (theta * corr_coeff_right, 0.)
            elif theta > 2 * np.pi - lim_theta_right:
                phi = ((theta - 2 * np.pi) * corr_coeff_right, 2 * np.pi)
            elif theta > (np.pi - lim_theta_right) and theta < np.pi + lim_theta_right:
                phi = ((theta - np.pi) * corr_coeff_right, np.pi)
            else:
                phi = None
            phis.append(phi)

        return phis

    def _compute_corr_coeff(self, lim_theta):
        return (np.pi / 2) / lim_theta

    def _get_theta_sect_via_phi(self, theta, phi, v, corr_coeff):
        return phi[0] / corr_coeff + phi[1]

    def _get_theta_sect_rect(self, v, theta, sect_rad):
        horiz_dist = self._get_horiz_dist_sect(v, theta)
        return abs(np.arctan2(sect_rad, horiz_dist)) + self._get_theta_add(theta)

    def _get_theta_add(self, theta):
        add = 0. if theta < np.pi else np.pi
        return add

    def _correct_normals(self, aux_normals, rad):
        normals = []
        c = 0
        for rads, aux_normals_ in zip(rad, aux_normals):
            c += 1
            dist_rad = rads[-1] - rads[0]
            theta = np.arctan2(dist_rad, np.linalg.norm(self._direc))
            rotation = R.from_rotvec(theta * np.cross(self._direc_unit, aux_normals_[0]))
            normals.append([rotation.apply(aux_normal) for aux_normal in aux_normals_])

        return np.array(normals)

    def replicate(self, shape):
        return TorchShell(*shape, self.pt_left, self.pt_right, self.radius_left,
                          self.radius_right, self.ecc_pt)

    def _get_dump_var_names(self):
        # TODO: check what to do with n_r and abs_curv and delete
        return ['theta', 'n_x', 'n_y', 'n_z', 'du', 'dv', 'u', 'v', 'dwu',
                'dwv', 'surf']

    def invert_normals(self):
        """Invert directions of normal vectors.
        """
        self._invert_normals(normal_vars=['n_x', 'n_y', 'n_z'])
