import math

def bothArmsBumpInFront():
    names = list()
    times = list()
    keys = list()

    names.append("HeadPitch")
    times.append([0.56, 0.84, 1.28, 1.8])
    keys.append([-0.060645, 0.0181879, -0.240011, -0.178764])

    names.append("HeadYaw")
    times.append([0.56, 0.84, 1.28, 1.8])
    keys.append([0.032172, 0.032172, 0.032172, 0.032172])

    names.append("HipPitch")
    times.append([0.64, 1.04, 1.6])
    keys.append([-0.329499, -0.361156, -0.0683659])

    names.append("HipRoll")
    times.append([0.64, 1.04, 1.6])
    keys.append([0.00339206, 0.00339206, 0.00339206])

    names.append("KneePitch")
    times.append([0.64, 1.04, 1.6])
    keys.append([0.116811, 0.127372, -0.030751])

    names.append("LElbowRoll")
    times.append([0.52, 1, 1.24, 1.4, 1.88])
    keys.append([-0.98262, -0.832522, -0.892776, -0.981718, -1.05995])

    names.append("LElbowYaw")
    times.append([0.52, 1, 1.24, 1.4, 1.88])
    keys.append([-1.23918, -1.62148, -1.57847, -1.51563, -1.49723])

    names.append("LHand")
    times.append([0.52, 1, 1.24, 1.4, 1.88])
    keys.append([0.856834, 0.8596, 0.796134, 0.6988, 0.5484])

    names.append("LShoulderPitch")
    times.append([0.52, 1, 1.24, 1.4, 1.88])
    keys.append([1.48267, 1.47567, 1.48182, 1.48487, 1.4772])

    names.append("LShoulderRoll")
    times.append([0.52, 1, 1.24, 1.4, 1.88])
    keys.append([0.23781, 0.246893, 0.231631, 0.216213, 0.220816])

    names.append("LWristYaw")
    times.append([0.52, 1, 1.24, 1.4, 1.88])
    keys.append([-0.709103, -0.70108, -0.713353, -0.730227, -0.72409])

    names.append("RElbowRoll")
    times.append([0.44, 0.92, 1.16, 1.32, 1.8])
    keys.append([1.30376, 0.941918, 0.992485, 1.02782, 1.1214])

    names.append("RElbowYaw")
    times.append([0.44, 0.92, 1.16, 1.32, 1.8])
    keys.append([1.2425, 1.89019, 1.59687, 1.47106, 1.46186])

    names.append("RHand")
    times.append([0.44, 0.92, 1.16, 1.32, 1.8])
    keys.append([0.1084, 0.8564, 0.760105, 0.6984, 0.5428])

    names.append("RShoulderPitch")
    times.append([0.44, 0.92, 1.16, 1.32, 1.8])
    keys.append([1.29538, 1.51257, 1.52171, 1.5187, 1.51563])

    names.append("RShoulderRoll")
    times.append([0.44, 0.92, 1.16, 1.32, 1.8])
    keys.append([-0.309147, -0.404274, -0.380428, -0.371443, -0.295341])

    names.append("RWristYaw")
    times.append([0.44, 0.92, 1.16, 1.32, 1.8])
    keys.append([0.791502, 0.868202, 0.880473, 0.89428, 0.891212])

    return names, keys, times, True

def fancyRightArmCircle():
    names = list()
    times = list()
    keys = list()

    names.append("HeadPitch")
    times.append([0.24, 0.44, 0.68, 1.68])
    keys.append([-0.206645, -0.0952972, -0.27168, -0.27168])

    names.append("HipPitch")
    times.append([0.76, 1.4])
    keys.append([-0.110514, -0.04043])

    names.append("HipRoll")
    times.append([0.76, 1.4])
    keys.append([-0.0243873, -0.0564659])

    names.append("KneePitch")
    times.append([0.76, 1.4])
    keys.append([0.0437812, -0.00637515])

    names.append("LElbowRoll")
    times.append([0.56, 1.04, 1.44])
    keys.append([-1.21387, -0.946839, -1.18497])

    names.append("LElbowYaw")
    times.append([1.04, 1.44])
    keys.append([-1.34689, -1.17815])

    names.append("LHand")
    times.append([1.04, 1.44])
    keys.append([0.3036, 0.3036])

    names.append("LShoulderPitch")
    times.append([1.04, 1.44])
    keys.append([1.54623, 1.54623])

    names.append("LShoulderRoll")
    times.append([0.56, 1.04, 1.44])
    keys.append([0.66748, 0.349811, 0.388161])

    names.append("LWristYaw")
    times.append([1.04, 1.44])
    keys.append([-0.550747, -0.227074])

    names.append("RElbowRoll")
    times.append([0.52, 1.28, 1.56])
    keys.append([1.13022, 0.652003, 1.13022])

    names.append("RElbowYaw")
    times.append([0.92, 1.56])
    keys.append([2.02404, 1.16366])

    names.append("RHand")
    times.append([0.52, 0.92, 1.28, 1.56])
    keys.append([0.25, 1, 0.37, 0.19])

    names.append("RShoulderPitch")
    times.append([0.52, 1.56])
    keys.append([1.06465, 1.55398])

    names.append("RShoulderRoll")
    times.append([0.92, 1.56])
    keys.append([-0.485688, -0.25431])

    names.append("RWristYaw")
    times.append([0.92, 1.56])
    keys.append([1.66588, 0.0506146])

    return names, keys, times, True

def normalPosture(time = 3.0):
    names = ["HeadYaw", "HeadPitch",
            "LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "LWristYaw",
            "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw",
            "LHand", "RHand", "HipRoll", "HipPitch", "KneePitch"]
    values = [0.00, -0.21, 1.55, 0.13, -1.24, -0.52, 0.01, 1.56, -0.14, 1.22, 0.52, -0.01,
            0, 0, 0, 0, 0]
    times = [time] * len(names)
    isAbsolute = True
    return names, values, times, isAbsolute

# def defaultPositionNeutral():
#     positions = [
#         ("HeadYaw", 0.0), ("HeadPitch", 0.0), 
#         ("LShoulderPitch", 0.0), ("LShoulderRoll", 0.0), 
#         ("LElbowYaw", 0.0), ("LElbowRoll", 0.0), 
#         ("LWristYaw", 0.0), 
#         ("LHand", 1.0), 
#         ("RShoulderPitch", 0.0), ("RShoulderRoll", 0.0),
#         ("RElbowYaw", 0.0), ("RElbowRoll", 0.0), 
#         ("RWristYaw", 0.0), 
#         ("RHand", 1.0), 
#         ("HipRoll", 0.0), ("HipPitch", 0.0),
#         ("KneePitch", 0.0)
#     ]
#     times = [1.0] * len(positions)
#     isAbsolute = True
#     return [e[0] for e in positions], [e[1] for e in positions], times, isAbsolute




