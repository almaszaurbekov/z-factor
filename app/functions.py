import math

def get_data_from_file(filename):
    with open(filename, 'r') as file:
        array = file.read().splitlines()
        return [list(map(float, item.split())) for item in array]

def get_system_data_from_file(filename):
    with open(filename, 'r') as file:
        return tuple(map(float, file.readline().split()))

def get_pseudo_critical_temperature(data):
    T_c = 0
    for row in data:
        y_i, t_ci = row[0], row[1]
        T_c += y_i * t_ci
    return T_c

def get_pseudo_critical_pressure(data):
    P_c = 0
    for row in data:
        y_i, p_ci = row[0], row[2]
        P_c += y_i * p_ci
    return P_c

def get_pseudo_reduced_value(system_value, critical_value):
    return system_value / critical_value

def get_z_factor(T_pr, P_pr):
    A = 1.39 * ((T_pr - 0.92) ** 0.5) - (0.36*T_pr) - 0.10
    E = 9*(T_pr - 1)
    B = (0.62 - 0.23*T_pr)*P_pr + ((0.066 / (T_pr - 0.86)) - 0.037)*(P_pr**2) + (0.32*(P_pr**2)) / 10*E
    C = 0.132 - 0.32 * math.log(T_pr)
    F = 0.3106 - 0.49*T_pr + 0.1824*(T_pr**2)
    D = 10 ** F

    return A + ((1 - A) / math.exp(B)) + (C * (P_pr ** D))