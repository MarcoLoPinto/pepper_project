import math

# SPEECH MOVEMENTS

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

def strongArmsOpenFlexEnd():
    names = list()
    times = list()
    keys = list()

    names.append("HeadPitch")
    times.append([0.52, 1.04, 1.48])
    keys.append([-0.415657, -0.123426, -0.369636])

    names.append("HeadYaw")
    times.append([0.52, 1.04, 1.48])
    keys.append([0.0398422, 0.0398422, 0.0536479])

    names.append("HipPitch")
    times.append([0.4, 0.72, 0.84, 1.28, 1.48])
    keys.append([-0.120399, -0.178497, -0.235035, -0.104673, -0.0659148])

    names.append("HipRoll")
    times.append([0.4, 0.72, 0.84, 1.28, 1.48])
    keys.append([-0.022229, -0.022229, -0.022229, -0.0122608, -0.0016941])

    names.append("KneePitch")
    times.append([0.4, 0.72, 0.84, 1.28, 1.48])
    keys.append([0.0319777, 0.0964101, 0.133068, 0.0460924, 0.0185926])

    names.append("LElbowRoll")
    times.append([0.36, 0.96, 1.44])
    keys.append([-1.01055, -1.15715, -1.30027])

    names.append("LElbowYaw")
    times.append([0.36, 0.96, 1.44])
    keys.append([-1.15054, -1.71812, -1.77181])

    names.append("LHand")
    times.append([0.36, 0.96, 1.44])
    keys.append([0.2132, 0.68, 0.7728])

    names.append("LShoulderPitch")
    times.append([0.36, 0.96, 1.44])
    keys.append([1.333, 1.32687, 1.2706])

    names.append("LShoulderRoll")
    times.append([0.36, 0.96, 1.44])
    keys.append([0.132418, 0.164632, 0.143156])

    names.append("LWristYaw")
    times.append([0.36, 0.96, 1.44])
    keys.append([0.21932, -0.70875, -0.808459])

    names.append("RElbowRoll")
    times.append([0.44, 1.04, 1.52])
    keys.append([1.01055, 1.08909, 1.30027])

    names.append("RElbowYaw")
    times.append([0.44, 1.04, 1.52])
    keys.append([1.17807, 1.87297, 1.94201])

    names.append("RHand")
    times.append([0.44, 1.04, 1.52])
    keys.append([0.0456001, 0.68, 0.7692])

    names.append("RShoulderPitch")
    times.append([0.44, 1.04, 1.52])
    keys.append([1.29934, 1.5141, 1.2706])

    names.append("RShoulderRoll")
    times.append([0.44, 1.04, 1.52])
    keys.append([-0.176474, -0.115114, -0.116648])

    names.append("RWristYaw")
    times.append([0.44, 1.04, 1.52])
    keys.append([0.0889301, 0.935697, 1.1029])

    return names, keys, times, True

def littleBothArmsBumpDuckEnd():
    names = list()
    times = list()
    keys = list()

    names.append("HeadPitch")
    times.append([0.24, 0.64, 1.4])
    keys.append([-0.102918, -0.31099, -0.100573])

    names.append("HeadYaw")
    times.append([0.24, 0.64, 1.4])
    keys.append([0.0894078, 0.0965329, 0.095628])

    names.append("HipPitch")
    times.append([0.56, 1.24])
    keys.append([0.0605874, -0.0896778])

    names.append("HipRoll")
    times.append([0.56, 1.24])
    keys.append([0.00926524, 0.00926524])

    names.append("KneePitch")
    times.append([0.56, 1.24])
    keys.append([-0.0526067, 0.0280235])

    names.append("LElbowRoll")
    times.append([0.32, 0.64, 1, 1.44])
    keys.append([-0.906552, -0.87127, -0.87127, -0.868286])

    names.append("LElbowYaw")
    times.append([0.32, 0.64, 1, 1.44])
    keys.append([-1.0314, -1.41519, -1.00992, -0.873316])

    names.append("LHand")
    times.append([0.32, 0.64, 1, 1.44])
    keys.append([0.74, 0.92, 0.1956, 0.2224])

    names.append("LShoulderPitch")
    times.append([0.32, 0.64, 1, 1.44])
    keys.append([1.31225, 1.31225, 1.31225, 1.24483])

    names.append("LShoulderRoll")
    times.append([0.32, 0.64, 1, 1.44])
    keys.append([0.0694999, 0.176997, 0.133928, 0.1064])

    names.append("LWristYaw")
    times.append([0.32, 0.64, 1, 1.44])
    keys.append([0.093532, 0.00455999, 0.0459781, 0.0123138])

    names.append("RElbowRoll")
    times.append([0.28, 0.6, 0.96, 1.36])
    keys.append([0.992539, 0.967996, 0.992539, 1.06302])

    names.append("RElbowYaw")
    times.append([0.28, 0.6, 0.96, 1.36])
    keys.append([1.13052, 1.5282, 1.11978, 0.978735])

    names.append("RHand")
    times.append([0.28, 0.6, 0.96, 1.36])
    keys.append([0.74, 0.92, 0.1648, 0.1888])

    names.append("RShoulderPitch")
    times.append([0.28, 0.6, 0.96, 1.36])
    keys.append([1.37369, 1.37369, 1.37369, 1.41042])

    names.append("RShoulderRoll")
    times.append([0.28, 0.6, 0.96, 1.36])
    keys.append([-0.0936165, -0.208429, -0.194861, -0.223922])

    names.append("RWristYaw")
    times.append([0.28, 0.6, 0.96, 1.36])
    keys.append([-0.204064, -0.204064, -0.204064, -0.233125])

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

########################### MOVEMENTS BASED ON MOOD ##############################

# POSITIVE

def happy():
    names = list()
    times = list()
    keys = list()

    names.append("HeadPitch")
    times.append([0.76, 0.88, 1.04, 1.2, 1.4, 1.56, 1.72, 1.88, 2.12, 2.28, 2.44, 2.6, 2.8, 2.96, 3.44])
    keys.append([-0.261799, -0.14802, -0.216196, -0.17832, -0.261799, -0.144232, -0.212408, -0.174533, -0.261799, -0.144232, -0.212408, -0.174533, -0.261799, -0.186331, -0.200952])

    names.append("HeadYaw")
    times.append([0.56, 0.92, 1.56, 2.28, 2.92, 3.44])
    keys.append([-0.0107379, 0.0349066, -0.0349066, 0.0349066, -0.0349066, -0.00306797])

    names.append("HipPitch")
    times.append([0.76, 3.32, 3.44])
    keys.append([-0.176278, -0.0352817, -0.0322137])

    names.append("HipRoll")
    times.append([0.76, 1.4, 2.12, 2.8, 3.32, 3.44])
    keys.append([0.0872665, -0.0872665, 0.0872665, -0.0872665, -0.00153399, 0.00306797])

    names.append("KneePitch")
    times.append([0.76, 3.32, 3.44])
    keys.append([0.0610865, -0.00306797, 0.00613595])

    names.append("LElbowRoll")
    times.append([0.76, 1.08, 1.4, 1.76, 2.12, 2.48, 2.8, 3.12, 3.44])
    keys.append([-0.925025, -0.670206, -1.0664, -0.670206, -0.925025, -0.670206, -1.0664, -0.670206, -0.523087])

    names.append("LElbowYaw")
    times.append([0.76, 1.4, 2.12, 2.8, 3.44])
    keys.append([-1.10828, -1.75472, -1.10828, -1.75472, -1.23025])

    names.append("LHand")
    times.append([0.76, 1.08, 1.4, 1.76, 2.12, 2.48, 2.8, 3.12, 3.44])
    keys.append([0.020089, 0.34, 0.173538, 0.34, 0.020089, 0.34, 0.173538, 0.34, 0.582601])

    names.append("LShoulderPitch")
    times.append([0.76, 1.4, 2.12, 2.8, 3.44])
    keys.append([1.31598, 1.77151, 1.31598, 1.77151, 1.56006])

    names.append("LShoulderRoll")
    times.append([0.76, 1.4, 2.12, 2.8, 3.44])
    keys.append([0.258309, 0.251327, 0.258309, 0.251327, 0.14266])

    names.append("LWristYaw")
    times.append([0.76, 1.4, 2.12, 2.8, 3.44])
    keys.append([-0.111693, 0.012626, -0.111693, 0.012626, 0.0152981])

    names.append("RElbowRoll")
    times.append([0.76, 1.08, 1.4, 1.76, 2.12, 2.48, 2.8, 3.12, 3.44])
    keys.append([1.0664, 0.694641, 0.925025, 0.694641, 1.0664, 0.694641, 0.925025, 0.694641, 0.523087])

    names.append("RElbowYaw")
    times.append([0.76, 1.4, 2.12, 2.8, 3.44])
    keys.append([1.75472, 1.10828, 1.75472, 1.10828, 1.22412])

    names.append("RHand")
    times.append([0.76, 1.08, 1.4, 1.76, 2.12, 2.48, 2.8, 3.12, 3.44])
    keys.append([0.173538, 0.29, 0.020089, 0.29, 0.173538, 0.29, 0.020089, 0.29, 0.585237])

    names.append("RShoulderPitch")
    times.append([0.76, 1.4, 2.12, 2.8, 3.44])
    keys.append([1.77151, 1.31598, 1.77151, 1.31598, 1.55546])

    names.append("RShoulderRoll")
    times.append([0.76, 1.4, 2.12, 2.8, 3.44])
    keys.append([-0.251327, -0.258309, -0.251327, -0.258309, -0.145728])

    names.append("RWristYaw")
    times.append([0.76, 1.4, 2.12, 2.8, 3.44])
    keys.append([-0.012626, 0.111693, -0.012626, 0.111693, 0.0137641])

    return names, keys, times, True

def kisses():
    names = list()
    times = list()
    keys = list()

    names.append("HeadPitch")
    times.append([1, 1.68, 2.2, 3.16, 4.16, 5.04])
    keys.append([-0.320648, -0.366667, -0.366667, -0.296706, -0.400415, -0.245482])

    names.append("HeadYaw")
    times.append([1, 1.68, 2.2, 3.16, 4.16, 5.04])
    keys.append([-0.075208, -0.032256, -0.032256, -0.032256, -0.0353239, -0.036858])

    names.append("HipPitch")
    times.append([1.6, 2.2, 3])
    keys.append([-0.478222, -0.478222, -0.0494019])

    names.append("HipRoll")
    times.append([1.6, 2.2, 3])
    keys.append([0, 0, 0])

    names.append("KneePitch")
    times.append([1.6, 2.2, 3])
    keys.append([0.178193, 0.178193, -0.0138332])

    names.append("LElbowRoll")
    times.append([0.92, 1.6, 2.12, 3.08, 4.08, 4.96])
    keys.append([-0.535324, -1.55697, -1.55697, -0.785367, -0.500042, -0.377323])

    names.append("LElbowYaw")
    times.append([0.92, 1.6, 2.12, 3.08, 4.08, 4.96])
    keys.append([-1.93288, -0.87749, -0.87749, -1.77181, -1.91447, -1.14287])

    names.append("LHand")
    times.append([1.6, 2.12, 3.08, 4.08, 4.96])
    keys.append([0.702933, 0.702933, 0.8, 0.676387, 0.109844])

    names.append("LShoulderPitch")
    times.append([0.92, 1.6, 2.12, 3.08, 4.08, 4.96])
    keys.append([0.863599, 0.187106, 0.187106, 0.955639, 1.39743, 1.48027])

    names.append("LShoulderRoll")
    times.append([0.92, 1.6, 2.12, 3.08, 4.08, 4.96])
    keys.append([0.030638, 0.015298, 0.015298, 0.914223, 0.58748, 0.067454])

    names.append("LWristYaw")
    times.append([1.6, 2.12, 3.08, 4.08, 4.96])
    keys.append([-1.12446, -1.12446, -1.53589, -1.13213, -0.139636])

    names.append("RElbowRoll")
    times.append([0.84, 1.52, 2.04, 3, 4, 4.88])
    keys.append([0.527739, 1.5621, 1.5621, 0.716419, 0.418823, 0.437231])

    names.append("RElbowYaw")
    times.append([0.84, 1.52, 2.04, 3, 4, 4.88])
    keys.append([2.0856, 0.677985, 0.677985, 1.94047, 2.08466, 1.51095])

    names.append("RHand")
    times.append([1.52, 2.04, 3, 4, 4.88])
    keys.append([0.758933, 0.758933, 0.909091, 0.730569, 0.22548])

    names.append("RShoulderPitch")
    times.append([0.84, 1.52, 2.04, 3, 4, 4.88])
    keys.append([1.01095, 0.030722, 0.030722, 1.10606, 1.39752, 1.53711])

    names.append("RShoulderRoll")
    times.append([0.84, 1.52, 2.04, 3, 4, 4.88])
    keys.append([-0.17185, -0.108956, -0.108956, -0.849878, -0.650458, -0.0429939])

    names.append("RWristYaw")
    times.append([1.52, 2.04, 3, 4, 4.88])
    keys.append([0.993989, 0.993989, 1.39626, 0.992455, 0.00302603])

    return names, keys, times, True

def excited():
    names = list()
    times = list()
    keys = list()

    names.append("HeadPitch")
    times.append([0.56, 0.8, 0.92, 1.04, 1.2, 1.32, 1.48, 1.6, 2.04])
    keys.append([-0.328028, -0.252647, -0.338728, -0.266191, -0.338728, -0.266191, -0.338728, -0.266191, -0.272682])

    names.append("HeadYaw")
    times.append([0.56, 2.04])
    keys.append([-0.016916, -0.016916])

    names.append("HipPitch")
    times.append([0.76, 1.48, 2.08])
    keys.append([-0.0383496, -0.345575, -0.0383496])

    names.append("HipRoll")
    times.append([0.76, 2.08])
    keys.append([0, 0])

    names.append("KneePitch")
    times.append([0.76, 2.08])
    keys.append([0.00153399, 0.00153399])

    names.append("LElbowRoll")
    times.append([0.68, 0.96, 1.04, 1.2, 1.32, 1.48, 1.56, 1.72, 1.88, 2.04, 2.2])
    keys.append([-1.49226, -1.50021, -1.30027, -1.50021, -1.30027, -1.50021, -1.30027, -1.50021, -1.30027, -1.50021, -1.30027])

    names.append("LElbowYaw")
    times.append([0.96, 1.2, 1.48, 1.72, 2.04])
    keys.append([-1.42053, -1.42053, -1.42053, -1.42053, -1.42053])

    names.append("LHand")
    times.append([0.68, 0.96, 1.04, 1.2, 1.32, 1.48, 1.56, 1.72, 1.88, 2.04, 2.2])
    keys.append([0.63, 0.27, 0.02, 0.24, 0.02, 0.28, 0.02, 0.26, 0.02, 0.24, 0.02])

    names.append("LShoulderPitch")
    times.append([0.6, 0.88, 1, 1.16, 1.24, 1.36, 1.52, 1.64, 1.8, 1.96, 2.12])
    keys.append([0.945968, 1.15541, 1.21475, 1.15541, 1.21475, 1.15541, 1.21475, 1.15541, 1.21475, 1.15541, 1.21475])

    names.append("LShoulderRoll")
    times.append([0.6, 0.88, 1.16, 1.36, 1.64, 1.96])
    keys.append([0.223402, 0.00872665, 0.00872665, 0.00872665, 0.00872665, 0.00872665])

    names.append("LWristYaw")
    times.append([0.68, 0.96, 1.2, 1.48, 1.72, 2.04])
    keys.append([-0.630064, 0.101202, 0.101202, 0.101202, 0.101202, 0.101202])

    names.append("RElbowRoll")
    times.append([0.68, 0.8, 0.96, 1.08, 1.24, 1.32, 1.48, 1.6, 1.76, 1.92, 2.08])
    keys.append([1.49226, 1.48649, 1.30027, 1.48649, 1.30027, 1.48649, 1.30027, 1.48649, 1.30027, 1.48649, 1.30027])

    names.append("RElbowYaw")
    times.append([0.8, 1.08, 1.32, 1.6, 1.92])
    keys.append([1.33914, 1.33914, 1.33914, 1.33914, 1.33914])

    names.append("RHand")
    times.append([0.68, 0.8, 0.96, 1.08, 1.24, 1.32, 1.48, 1.6, 1.76, 1.92, 2.08])
    keys.append([0.63, 0.27, 0.02, 0.24, 0.02, 0.28, 0.02, 0.26, 0.02, 0.24, 0.02])

    names.append("RShoulderPitch")
    times.append([0.6, 0.76, 0.92, 1.04, 1.16, 1.28, 1.4, 1.56, 1.68, 1.84, 2])
    keys.append([0.945968, 1.15541, 1.21475, 1.15541, 1.21475, 1.15541, 1.21475, 1.15541, 1.21475, 1.15541, 1.21475])

    names.append("RShoulderRoll")
    times.append([0.6, 0.76, 1.04, 1.28, 1.56, 1.84])
    keys.append([-0.223402, -0.00872665, -0.00872665, -0.00872665, -0.00872665, -0.00872665])

    names.append("RWristYaw")
    times.append([0.68, 0.8, 1.08, 1.32, 1.6, 1.92])
    keys.append([0.630064, 0.110406, 0.110406, 0.110406, 0.110406, 0.110406])

    return names, keys, times, True

# NEUTRAL

def thinking():
    names = list()
    times = list()
    keys = list()

    names.append("HeadPitch")
    times.append([0.72, 1.2, 3.16, 4.72, 5.2, 5.56])
    keys.append([-0.113446, 0.224996, 0.200713, 0.240855, 0.125664, -0.20886])

    names.append("HeadYaw")
    times.append([1.2, 4.72, 5.56])
    keys.append([0.154895, 0.157081, -0.305068])

    names.append("HipPitch")
    times.append([0.56, 1.2, 4.16, 5.08])
    keys.append([-0.0409819, -0.216292, -0.348214, -0.0433329])

    names.append("HipRoll")
    times.append([0.56, 1.2, 4.16, 5.08])
    keys.append([0, -0.0567572, -0.0352817, -0.00344329])

    names.append("KneePitch")
    times.append([0.56, 1.2, 4.16, 5.08])
    keys.append([-0.0110766, 0.0291458, 0.075165, -0.012951])

    names.append("LElbowRoll")
    times.append([0.64, 1.12, 4.64, 5.12, 5.48])
    keys.append([-0.799361, -1.48487, -1.51669, -1.53414, -1.37739])

    names.append("LElbowYaw")
    times.append([0.64, 1.12, 4.64, 5.48])
    keys.append([-1.40324, -0.955723, -0.909316, -1.54856])

    names.append("LHand")
    times.append([0.64, 1.12, 1.68, 2.08, 2.68, 3.08, 3.76, 4.16, 4.64, 5.12, 5.48])
    keys.append([0.96, 0.7036, 0.44, 0.73, 0.44, 0.73, 0.44, 0.73, 0.65, 0.52, 0.844074])

    names.append("LShoulderPitch")
    times.append([1.12, 4.64, 5.12, 5.48])
    keys.append([-0.512397, -0.581195, 0.0994838, 0.44047])

    names.append("LShoulderRoll")
    times.append([1.12, 4.64, 5.48])
    keys.append([0.328234, 0.342085, 0.233874])

    names.append("LWristYaw")
    times.append([0.64, 1.12, 4.64, 5.48])
    keys.append([-0.895354, -0.833004, -0.862194, 0.0192082])

    names.append("RElbowRoll")
    times.append([0.56, 1.04, 4.56, 5.04, 5.4])
    keys.append([0.574213, 0.382009, 0.20402, 0.375246, 0.25889])

    names.append("RElbowYaw")
    times.append([0.56, 1.04, 4.56, 5.4])
    keys.append([1.47829, 1.23483, 1.23639, 1.2217])

    names.append("RHand")
    times.append([0.56, 1.04, 4.56, 5.04, 5.4])
    keys.append([0.54, 0.3504, 0.510545, 0.31, 0.412984])

    names.append("RShoulderPitch")
    times.append([1.04, 4.56, 5.4])
    keys.append([1.54785, 1.36831, 1.43506])

    names.append("RShoulderRoll")
    times.append([1.04, 4.56, 5.4])
    keys.append([-0.108956, -0.085903, -0.119999])

    names.append("RWristYaw")
    times.append([0.56, 1.04, 4.56, 5.4])
    keys.append([0.497419, 0.030638, 0.093532, -0.033162])

    return names, keys, times, True

def curious():
    names = list()
    times = list()
    keys = list()

    names.append("HeadPitch")
    times.append([0.4, 0.76, 1.32, 1.72, 2.08, 2.64])
    keys.append([-0.0383972, -0.483456, -0.483456, -0.202458, -0.483456, -0.483456])

    names.append("HeadYaw")
    times.append([0.76, 1.32, 2.08, 2.64])
    keys.append([-0.0872665, -0.0872665, 0.0872665, 0.0872665])

    names.append("HipPitch")
    times.append([0.76, 1.32, 2.08, 2.64])
    keys.append([-0.497419, -0.497419, -0.497419, -0.497419])

    names.append("HipRoll")
    times.append([0.76, 1.32, 2.08, 2.64])
    keys.append([0.349066, 0.349066, -0.349066, -0.349066])

    names.append("LElbowRoll")
    times.append([1.72, 2.08, 2.64])
    keys.append([-0.467748, -0.350811, -0.350811])

    names.append("LElbowYaw")
    times.append([2.08, 2.64])
    keys.append([-1.68773, -1.68773])

    names.append("LHand")
    times.append([0.76, 1.32, 1.72, 2.08, 2.64])
    keys.append([0.69, 1, 0.6, 0.98, 1])

    names.append("LShoulderPitch")
    times.append([0.76, 1.32, 2.08, 2.64])
    keys.append([1.76278, 1.76278, 1.76278, 1.80118])

    names.append("LShoulderRoll")
    times.append([0.76, 1.32, 1.72, 2.08, 2.64])
    keys.append([0.438078, 0.568977, 0.10472, 0.00872665, 0.200713])

    names.append("RElbowRoll")
    times.append([0.76, 1.32, 1.72, 2.64])
    keys.append([0.350811, 0.350811, 0.499164, 0.350811])

    names.append("RElbowYaw")
    times.append([0.76, 1.32, 2.64])
    keys.append([1.68773, 1.68773, 1.68773])

    names.append("RHand")
    times.append([0.76, 1.32, 1.72, 2.08, 2.64])
    keys.append([0.92, 1, 0.66, 0.94, 1])

    names.append("RShoulderPitch")
    times.append([0.76, 1.32, 2.08, 2.64])
    keys.append([1.80118, 1.80118, 1.80118, 1.76278])

    names.append("RShoulderRoll")
    times.append([0.76, 1.32, 1.72, 2.08, 2.64])
    keys.append([-0.00872665, -0.200713, -0.10472, -0.438078, -0.568977])

    return names, keys, times, True

def chill():
    names = list()
    times = list()
    keys = list()

    names.append("HeadPitch")
    times.append([0.88, 1.04, 1.28, 1.52, 1.76, 2, 2.24, 2.44, 2.68, 3.08, 3.76, 4.32, 4.96, 5.36, 6.68])
    keys.append([-0.143211, -0.0762854, -0.143211, -0.0762854, -0.143211, -0.0762854, -0.143211, -0.0762854, -0.143211, -0.0767945, -0.10821, 0.00698132, -0.0762854, -0.143211, -0.199166])

    names.append("HeadYaw")
    times.append([0.88, 1.28, 1.76, 2.24, 2.68, 3.76, 5.36, 6.68])
    keys.append([-0.00559958, -0.00559958, -0.00559958, -0.00559958, -0.00559958, -0.401426, 0.561996, -0.00830721])

    names.append("HipPitch")
    times.append([0.68, 1.56, 2.48, 3.36, 4.4, 5.28, 6.68])
    keys.append([-0.0409819, -0.0409819, -0.0409819, -0.0409819, -0.0409819, -0.0409819, -0.0357826])

    names.append("HipRoll")
    times.append([0.68, 1.56, 2.48, 3.36, 4.4, 5.28, 6.68])
    keys.append([0.0349066, -0.0349066, 0.0349066, -0.0349066, 0.0349066, -0.0349066, -0.00128241])

    names.append("KneePitch")
    times.append([0.68, 1.56, 2.48, 3.36, 4.4, 5.28, 6.68])
    keys.append([-0.0110766, -0.0110766, -0.0110766, -0.0110766, -0.0110766, -0.0110766, -0.00954351])

    names.append("LElbowRoll")
    times.append([0.88, 1.76, 2.68, 3.56, 4.6, 5.48, 6.68])
    keys.append([-0.524491, -0.524332, -0.524491, -0.524332, -0.524491, -0.524332, -0.522098])

    names.append("LElbowYaw")
    times.append([0.88, 1.76, 2.68, 3.56, 4.6, 5.48, 6.68])
    keys.append([-1.22964, -1.25475, -1.22964, -1.25475, -1.22964, -1.25475, -1.23476])

    names.append("LHand")
    times.append([0.88, 1.76, 2.68, 3.56, 4.6, 5.48, 6.68])
    keys.append([0.602, 0.81, 0.602, 0.82, 0.602, 0.82, 0.6])

    names.append("LShoulderPitch")
    times.append([0.88, 1.76, 2.68, 3.56, 4.6, 5.48, 6.68])
    keys.append([1.54691, 1.50478, 1.54691, 1.50478, 1.54691, 1.50478, 1.55282])

    names.append("LShoulderRoll")
    times.append([0.88, 1.76, 2.68, 3.56, 4.6, 5.48, 6.68])
    keys.append([0.20944, 0.0984563, 0.20944, 0.0984563, 0.20944, 0.0984563, 0.139564])

    names.append("LWristYaw")
    times.append([0.88, 1.76, 2.68, 3.56, 4.6, 5.48, 6.68])
    keys.append([0.0369999, 0.017, 0.0369999, 0.017, 0.0369999, 0.017, 0.00382428])

    names.append("RElbowRoll")
    times.append([0.88, 1.76, 2.68, 3.56, 4.6, 5.48, 6.68])
    keys.append([0.524332, 0.524491, 0.524332, 0.524491, 0.524332, 0.524491, 0.521033])

    names.append("RElbowYaw")
    times.append([0.88, 1.76, 2.68, 3.56, 4.6, 5.48, 6.68])
    keys.append([1.25475, 1.22964, 1.25475, 1.22964, 1.25475, 1.22964, 1.22827])

    names.append("RHand")
    times.append([0.88, 1.76, 2.68, 3.56, 4.6, 5.48, 6.68])
    keys.append([0.76, 0.602, 0.85, 0.602, 0.85, 0.602, 0.603375])

    names.append("RShoulderPitch")
    times.append([0.88, 1.76, 2.68, 3.56, 4.6, 5.48, 6.68])
    keys.append([1.50478, 1.54691, 1.50478, 1.54691, 1.50478, 1.54691, 1.55573])

    names.append("RShoulderRoll")
    times.append([0.88, 1.76, 2.68, 3.56, 4.6, 5.48, 6.68])
    keys.append([-0.0984563, -0.20944, -0.0984563, -0.20944, -0.0984563, -0.20944, -0.14278])

    names.append("RWristYaw")
    times.append([0.88, 1.76, 2.68, 3.56, 4.6, 5.48, 6.68])
    keys.append([-0.017, -0.0369999, -0.017, -0.0369999, -0.017, -0.0369999, -0.00843125])

    return names, keys, times, True

# NEGATIVE

def fear():
    names = list()
    times = list()
    keys = list()

    names.append("HeadPitch")
    times.append([0.44, 1.04, 1.24, 1.56, 1.76, 2.16, 2.32, 2.88, 3.04, 3.36, 3.56, 4.24])
    keys.append([-0.140935, -0.150138, -0.120993, -0.120993, -0.259054, -0.259054, -0.148605, -0.148605, -0.120993, -0.120993, -0.144003, -0.211735])

    names.append("HeadYaw")
    times.append([0.44, 1.04, 1.24, 1.56, 1.76, 2.16, 2.32, 2.88, 3.04, 3.36, 3.56, 4.24])
    keys.append([0.11194, 0.11961, -0.455639, -0.455639, -0.208666, -0.208666, 0.138018, 0.138018, -0.455639, -0.455639, -4.19617e-05, 0.00609404])

    names.append("HipPitch")
    times.append([0.56, 0.88, 4.08])
    keys.append([-0.147262, -0.147262, -0.0352817])

    names.append("HipRoll")
    times.append([0.56, 0.88, 1.24, 1.28, 1.44, 1.8, 1.92, 2.36, 2.72, 3.16, 4.08])
    keys.append([-0.00460196, -0.00460196, 0.0383972, 0.0541052, 0.0541052, 0, 0, -0.0715585, -0.0715585, 0.0349066, -0.00766992])

    names.append("KneePitch")
    times.append([0.56, 0.88, 4.08])
    keys.append([-0.0230097, -0.0230097, -0.00920391])

    names.append("LElbowRoll")
    times.append([0.4, 3.24, 4.08])
    keys.append([-0.549129, -0.458624, -0.532256])

    names.append("LElbowYaw")
    times.append([0.4, 3.24, 4.08])
    keys.append([-2.02186, -2.08628, -1.19043])

    names.append("LHand")
    times.append([0.6])
    keys.append([0.341458])

    names.append("LShoulderPitch")
    times.append([0.4, 3.24, 4.08])
    keys.append([1.78093, 1.73031, 1.67969])

    names.append("LShoulderRoll")
    times.append([0.4, 3.24, 4.08])
    keys.append([0.147222, 0.162562, 0.314428])

    names.append("LWristYaw")
    times.append([0.6])
    keys.append([-0.0337899])

    names.append("RElbowRoll")
    times.append([0.4, 3.24, 4.08])
    keys.append([0.521602, 0.521602, 0.550747])

    names.append("RElbowYaw")
    times.append([0.4, 3.24, 4.08])
    keys.append([1.81162, 1.95274, 1.66281])

    names.append("RHand")
    times.append([0.6])
    keys.append([0.0192993])

    names.append("RShoulderPitch")
    times.append([0.4, 3.24, 4.08])
    keys.append([1.71505, 1.69818, 1.71812])

    names.append("RShoulderRoll")
    times.append([0.4, 3.24, 4.08])
    keys.append([-0.296104, -0.231677, -0.191792])

    names.append("RWristYaw")
    times.append([0.6])
    keys.append([0.00609404])

    return names, keys, times, True

def confused():
    names = list()
    times = list()
    keys = list()

    names.append("HeadPitch")
    times.append([1.04, 1.84, 2.64, 3.24])
    keys.append([-0.250102, -0.294589, -0.242431, -0.294589])

    names.append("HeadYaw")
    times.append([1.04, 1.84, 2.64, 3.24])
    keys.append([-0.0475121, 0.0777221, -0.167638, 4.19617e-05])

    names.append("HipRoll")
    times.append([0.72, 1.52, 2.32, 3.12])
    keys.append([0.0523599, -0.0523599, 0.0523599, 0])

    names.append("LElbowRoll")
    times.append([0.96, 1.76, 2.56, 3.12])
    keys.append([-0.811444, -1.18574, -1.06609, -1.18574])

    names.append("LElbowYaw")
    times.append([0.96, 1.76, 2.56, 3.12])
    keys.append([-0.495523, -0.972599, -1.19963, -0.972599])

    names.append("LHand")
    times.append([1.76, 3.12])
    keys.append([0.58, 0.17])

    names.append("LShoulderPitch")
    times.append([0.96, 1.76, 2.56, 3.12])
    keys.append([1.21949, 1.28698, 1.31613, 1.28698])

    names.append("LShoulderRoll")
    times.append([0.96, 1.76, 2.56, 3.12])
    keys.append([0.00869999, 0.127409, 0.05058, 0.167552])

    names.append("LWristYaw")
    times.append([1.76, 3.12])
    keys.append([-0.750492, -0.455531])

    names.append("RElbowRoll")
    times.append([0.96, 1.76, 2.56, 3.12])
    keys.append([1.21957, 1.39445, 1.15054, 1.39445])

    names.append("RElbowYaw")
    times.append([0.96, 1.76, 2.56, 3.12])
    keys.append([0.776162, 0.96331, 1.21489, 0.96331])

    names.append("RHand")
    times.append([1.76, 3.12])
    keys.append([0.527273, 0.15])

    names.append("RShoulderPitch")
    times.append([0.96, 1.76, 2.56, 3.12])
    keys.append([1.33309, 1.2886, 1.45121, 1.2886])

    names.append("RShoulderRoll")
    times.append([0.96, 1.76, 2.56, 3.12])
    keys.append([-0.00924597, -0.148353, -0.016916, -0.171042])

    names.append("RWristYaw")
    times.append([1.76, 3.12])
    keys.append([0.907571, 0.541052])

    return names, keys, times, True

def bored():
    names = list()
    times = list()
    keys = list()

    names.append("HeadPitch")
    times.append([1.52, 2.24, 3.64])
    keys.append([-0.408407, -0.408407, -0.200137])

    names.append("HeadYaw")
    times.append([3.64])
    keys.append([0])

    names.append("HipPitch")
    times.append([1, 3.64])
    keys.append([-0.232129, -0.043558])

    names.append("HipRoll")
    times.append([3.64])
    keys.append([9.18108e-06])

    names.append("KneePitch")
    times.append([1, 3.64])
    keys.append([0.0698132, -0.0126618])

    names.append("LElbowRoll")
    times.append([1.52, 2.24, 3.64])
    keys.append([-0.287021, -0.287021, -0.518045])

    names.append("LElbowYaw")
    times.append([1.52, 2.24, 3.64])
    keys.append([-1.24255, -1.24255, -1.23079])

    names.append("LHand")
    times.append([1, 2.24, 3.64])
    keys.append([0.72, 0.59051, 0.59051])

    names.append("LShoulderPitch")
    times.append([1.52, 2.24, 3.64])
    keys.append([1.44153, 1.44153, 1.55049])

    names.append("LShoulderRoll")
    times.append([1.52, 2.24, 3.64])
    keys.append([0.0879382, 0.0879382, 0.141612])

    names.append("LWristYaw")
    times.append([1.52, 2.24, 3.64])
    keys.append([-0.085662, -0.085662, -0.00776232])

    names.append("RElbowRoll")
    times.append([1, 1.36, 1.52, 1.76, 1.92, 2.08, 2.24, 3.64])
    keys.append([0.844739, 1.21649, 1.44521, 1.37706, 1.44521, 1.37706, 1.44521, 0.523237])

    names.append("RElbowYaw")
    times.append([1, 1.36, 1.52, 2.24, 2.84, 3.64])
    keys.append([0.644027, 0.830904, 0.830904, 0.830904, 1.46259, 1.23647])

    names.append("RHand")
    times.append([1, 1.36, 1.52, 1.68, 1.84, 2, 2.16, 2.24, 2.84, 3.64])
    keys.append([0.42, 0.41, 0.990795, 0.89, 1, 0.89, 1, 0.990795, 0.5, 0.603567])

    names.append("RShoulderPitch")
    times.append([1.36, 1.52, 2.24, 3.64])
    keys.append([-0.13439, 0.0311672, 0.0311672, 1.55119])

    names.append("RShoulderRoll")
    times.append([0.6, 1.36, 1.52, 2.24, 2.84, 3.64])
    keys.append([-0.256563, -0.0907571, -0.0106431, -0.0106431, -0.200713, -0.147331])

    names.append("RWristYaw")
    times.append([0.8, 1.36, 1.52, 2.24, 2.84, 3.64])
    keys.append([0.118682, 1.52139, 1.52139, 1.52139, 1.44862, 0.00377895])

    return names, keys, times, True

