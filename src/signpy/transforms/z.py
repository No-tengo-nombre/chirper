# from signpy.transforms import Transform
# from signpy.config import Z_METHOD

# import numpy as np
# from tqdm import tqdm

# class Z_transform(Transform):
#     def __init__(self, target):
#         super().__init__(target)
#         self.methods = {
#             "dzt": self.calculate_dzt,
#         }

#     def calculate(self, method=Z_METHOD, *args, **kwargs):
#         return self.methods[method](*args, **kwargs)

#     def calculate_dzt(self, R):
#         N = len(self.signal)
#         rho = np.empty((N, N))
#         for k in tqdm(range(N), desc="Calculating Z transform"):
#             for m in range(N):
#                 r_vec = np.array([(R * m / N) ** (-i) for i in range(N)])
#                 xi_vec = np.array([self.signal.values[i] * np.exp(-1j * 2 * np.pi * (k / N) * i) for i in range(N)])
#                 rho[k, m] = np.dot(r_vec, xi_vec)
#         self.values = rho
#         return self.values
