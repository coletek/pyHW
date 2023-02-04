class PidApi:

    dt = 0.025 # min based on deterministic hardware/device of 9600baud
    error_previous = 0
    error_integrated_previous = 0
    p_gain = 1
    i_gain = 0
    d_gain = 0

    def set_pid(self, dt, p, i, d):
        self.dt = dt
        self.p_gain = p
        self.i_gain = i
        self.d_gain = d
        
    def tick(self, set_point, process_value):

        error = set_point - process_value
        error_integrated = self.error_integrated_previous + error * self.dt # Forward Euler integration
        error_derivative = (error - self.error_previous) / self.dt # Finite difference
        
        self.error_previous = error
        self.error_integrated_previous = error_integrated

        #print ("error=" + str(error))
        
        return self.p_gain * error + self.i_gain * error_integrated + self.d_gain * error_derivative
