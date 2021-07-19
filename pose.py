
import numpy as np
import math


class Pose():

    """ Encapsulates a pose and provides useful methods """

    def __init__(self, x: float, y: float, angle: float):
            # Check values
        assert (angle >= 0 and angle < 2*np.pi), f"<angle> should be in [0, 2*pi[ (got '{angle}' instead)"
            # Store data in object
        self.coordinates = np.array([x, y, angle])



    def rotate(self, angle: float):
        # Apply rotation Matrix [cos -sin ] to itself and return the resulting pose
        #                       [sin cos]
        x = self.coordinates[0]
        y = self.coordinates[1]
        myAngle = self.coordinates[2]
        return Pose(math.cos(angle) * x - math.sin(angle) * y, math.sin(angle) * x + math.cos(angle) * y, (myAngle + angle)%(2*math.pi))

    def __str__(self):
        return f"[Pose] :: x={round(self.coordinates[0], 2)} ; y={round(self.coordinates[1], 2)} ; angle={round(self.coordinates[2], 2)}rad ({round(self.coordinates[2]*180/math.pi, 1)}deg)"


if __name__ == "__main__":
        # Test Pose class
    pose = Pose(1, 2, 0)
    print(pose)
    for rot in range(8):
        pose = pose.rotate(math.pi/4)
        print(pose)
