import numpy as np
import util
import visualization as vis
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import UnivariateSpline


'''
Parameters
'''
time = 5000     # total time
dn = 5          # time interval to sample a point
random_sample = False
dt = 0.1        # time interval for movement, not important due to rescaling later
spline = False   # whether to create smooth trajectory using spline
filename = "./data/Synthetic_Trajectory_generated.txt"

while True:
    # Define position(r), velocity(v), acceleration(a)
    r = np.zeros([3,time])
    v = np.ones([3,time])

    for t in range(1,time):
        a = np.random.randn(3)
        # a = np.random.uniform(-0.5,0.5,3)
        v[:,t] = v[:,t-1] + a*dt
        r[:,t] = r[:,t-1] + v[:,t-1]*dt + 0.5*a*dt**2

    # Sampling
    if random_sample:
        idx_1 = np.array(range(0,time,dn))
        idx_2 = np.random.randint(dn-1, size=len(idx_1))
        idx = idx_1 + idx_2
    else:
        idx = np.array(range(0,time,dn))

    # Rescale into final data
    data = np.zeros([3,len(idx)])
    data[0] = util.mapminmax(r[0,idx],-5,5)
    data[1] = util.mapminmax(r[1,idx],-5,5)
    data[2] = util.mapminmax(r[2,idx],-5,5)

    # Smooth the trajectory (optional)
    if spline:
        num = data.shape[1]
        t = np.arange(num, dtype=float)
        spl = [UnivariateSpline(t, data[0]),UnivariateSpline(t, data[1]),UnivariateSpline(t, data[2])]
        data[0], data[1], data[2] = spl[0](t), spl[1](t), spl[2](t)
    
    # Show the 3D trajectory
    vis.show_trajectory_3D(data,color=True,line=True)

    # Ask if the data is accepted
    print("\nDo you want to save this trajectory?")
    decision = input("Enter 'y' to save it, enter 'n' to regenerate, enter anyother key to exit: ")

    if decision == 'y':
        np.savetxt(filename, data, header="This is a synthetic trajectory dataset generated by generate_synthetic_trajectory.py")
        print('\n\nThe trajectory is saved under the name "Synthetic_Trajectory_generated.txt".\n')
        print('Total number of points: {}\n'.format(int(time/dn)))
        break
    elif decision == 'n':
        pass
    else:
        print('\nNo trajectory is generated')
        break