### Python 3D calibration and homogenous coordinates computation library



## 2D and 3D points implementation

The vector used to represent 2D and 3D points are _vertical_ vectors, which are stored as 2D matrices in `numpy`. Furthemore, we work in _homogenous_ coordinates: a 3D point $(x,y,z)$ in the world is represented by a 4D vector $\left[\lambda x,\lambda y,\lambda z,\lambda \right]^T$ where $\lambda \in \mathbb{R}_0$.

To simplify access to $x$ and $y$ (and $z$) coordinates of those points as well as computations in homogenous coordinates, we defined the objects `Point3D` and `Point2D` (extending `np.ndarray`) in the library `calib3d`.

Therefore, access to $y$ coordinate of `point` is `point.y` instead of `point[1][0]` (`point[1][:]` for an array of points), and access to homogenous coordinates is made easy with `point.H`, while it is still possible to use `point` object with `numpy` operators.
