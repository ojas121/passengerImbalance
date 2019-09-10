import numpy as np
import itertools


# setting up position vectors for the seats in each row
# origin is defined as the middle of the aisle in the middle of row 13, axes as defined in slide
# so the next row is 40.5cm (0.405m) away, the row after that 121.5cm (1.215m)
# seat width is assumed to be 44cm = 0.44m
# cabin width = 3.7m, therefore aisle width is 1.06m
# seat positions in each row in metres (K is the z-axis unit vector):
# A=1.63K B=1.19K C=0.75K D=-0.75K E=-1.19K F=-1.63K

def create_row(row_pos):
    # row_pos is the x-coordinate of the middle of the row
    a = [row_pos, 0, 1.63]
    b = [row_pos, 0, 1.19]
    c = [row_pos, 0, 0.75]
    d = [row_pos, 0, -0.75]
    e = [row_pos, 0, -1.19]
    f = [row_pos, 0, -1.63]

    return [a, b, c, d, e, f]


seats = create_row(0)  # row 13

for i in range(1, 17):  # 16 rows behind row 13, positive x direction
    seats.extend(create_row(np.multiply(0.81, i)))

for j in range(1, 13):  # 12 rows ahead of row 13, negative x direction
    seats.extend(create_row(np.multiply(-0.81, j)))

# 174 seats now all defined in array seats

probabilities = [0]  # index 0 => 0 passengers
for num_passengers in range(1, 175):
    occupied_seats_combinations = itertools.combinations(seats, num_passengers)
    over_limit_counter = 0
    num_possibilities = 0
    for occupied_seats in occupied_seats_combinations:
        num_possibilities += 1
        sum_moments = [0, 0, 0]
        for seat in occupied_seats:
            moment = np.cross(seat, [0, -85*9.81, 0])
            # assuming average human weight of 85 kg acting in negative y axis
            sum_moments = np.add(sum_moments, moment)
        moment_magnitude = np.linalg.norm(sum_moments)/1000  # magnitude in kN
        if moment_magnitude > 100:
            over_limit_counter += 1
    probability = over_limit_counter/num_possibilities
    probabilities.append(probability)
    print(str(num_passengers) + " passengers, probability " + str(probability))
