import numpy as np

# TODO: Add more observers and test

class Kalman(object):
    def __init__(self, Q_mat, R_mat, initX, initP, A, B, C):
        self.R = R_mat
        self.Q = Q_mat
        self.X_cap = initX
        self.P = initP
        self.A = A
        self.B = B
        self.C = C
    
        # TODO: check shape of X and P
        
    def time_update(self, u):
        
        # forward model
        self.Xn1 = self.A * self.X_cap + self.B * u
        
        # update covariance matrix
        self.P = self.A * self.P * np.transpose(self.A) + self.Q
    
    def measurement_update(self, z):
        
        # Kalman gain
        self.Kalman = self.P * np.transpose(self.C) * np.linalg.inv(
            self.C * self.P * np.transpose(self.C) + self.R
        )
        
        # Upate estimate
        self.X_cap = self.Xn1 + self.Kalman * (z - self.C * self.Xn1)
        
        # update covariance
        order = np.shape(self.Kalman * self.C) # need to test and update
        pp = np.eye(order) - self.Kalman * self.C
        self.P = (pp * self.P * np.transpose(pp)) + (
            self.Kalman * self.R * self.Kalman
        )
        
        # return state estimate
        return self.X_cap
        
    
    def update(self, input, measurement):
        
        # time update eq
        self.time_update(input)
        
        # meas update
        estimate = self.measurement_update(measurement)
        
        return estimate