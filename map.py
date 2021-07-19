
import numpy as np
from pose import Pose
import math
import random

class Terrain():

    """ Encapsulates the map the agent operates in and provides useful methods """

    def __init__(self, gridWidth: int, gridHeight: int, maxAltitude: int):

            # Check values
        assert (gridWidth >= 1), f"<gridWidth> should be strickly positive (got '{gridWidth}')."
        assert (gridHeight >= 1), f"<gridHeight> should be strickly positive (got '{gridHeight}')."
        assert (maxAltitude >= 1), f"<maxAltitude> should be strickly positive (got '{maxAltitude}')."

            # Fill object
        self.gridWidth = gridWidth
        self.gridHeight = gridHeight
        self.map = np.zeros((self.gridWidth, self.gridHeight), dtype=int)
        self.start = [0, 0]
        self.end = [self.gridWidth, self.gridHeight]



    def getAltitude(self, pose: Pose):
        coord = pose.coordinates[:2]
        return self.map[math.floor(coord[0]), math.floor(coord[1])] # Ignore the angle of the pose



    def pathIsValid(
        self,
        pointA: Pose,
        pointB: Pose,
        maxPathLength: float = 5.0,
        maxPathAngle: float = 0.5,
        maxPathTurnRadius: float = 4
    ) -> bool:
        """ Compute the validity of a path from <pointA> to <pointB> """
            # Chek values
        assert (pointA.coordinates[0] >= 0 and pointA.coordinates[0] < self.gridWidth), f"<pointA> should have coordinates in [0, {self.gridWidth}] x [0, {self.gridHeight}] (got '{pointA.coordinates}' instead)"
        assert (pointA.coordinates[1] >= 0 and pointA.coordinates[1] < self.gridHeight), f"<pointA> should have coordinates in [0, {self.gridWidth}] x [0, {self.gridHeight}] (got '{pointA.coordinates}' instead)"
        assert (pointB.coordinates[0] >= 0 and pointB.coordinates[0] < self.gridWidth), f"<pointB> should have coordinates in [0, {self.gridWidth}] x [0, {self.gridHeight}] (got '{pointB.coordinates}' instead)"
        assert (pointB.coordinates[1] >= 0 and pointB.coordinates[1] < self.gridHeight), f"<pointB> should have coordinates in [0, {self.gridWidth}] x [0, {self.gridHeight}] (got '{pointB.coordinates}' instead)"
        assert (maxPathLength > 0), f"<maxPathLength> should be > 0 (got '{maxPathLength}' instead)"

        pathVector = pointB.coordinates - pointA.coordinates
        pathVector[2] %= 2*np.pi

            # Validity condition 1 : Path is not too long
        if np.linalg.norm(pathVector[:2], ord=2) > maxPathLength :
            return False

            # Validity condition 2 : Angle not too steep
        if abs(pathVector[-1]) > maxPathAngle :
            return False

            # Express vectorPath in the referential of pointA
        pointB_refA = Pose(pathVector[0], pathVector[1], 0).rotate(pointA.coordinates[2])

            # Validity condition 3 : Next point is ahead of the robot, not behind)
        if pointB_refA.coordinates[0] <= 0:
            return False

            # Validity condition 3 : Curvature not too high
        if np.linalg.norm(np.array([0, maxPathTurnRadius]) - pointB_refA.coordinates[:2]) < maxPathTurnRadius :
            return False # Point to go to is inside the right disk
        if np.linalg.norm(np.array([0, -maxPathTurnRadius]) - pointB_refA.coordinates[:2]) < maxPathTurnRadius :
            return False # Point to go to is inside the left disk

            # Validity condition 4 : Altitude gradient not too high


        return True


    def draw(self):
        pass # Todo

    def __str__(self):
        pass # Todo




if __name__ == "__main__" :
    # Test class Map
    mapSize = 50
    terrain = Terrain(gridWidth=mapSize, gridHeight=mapSize, maxAltitude=10)
    pose1 = Pose(0, 0, 0)
    pose2 = Pose(1, 2, np.pi/2)
    print("Pose1 : ", pose1)
    print("Pose2 : ", pose2)
    print("alt : ", terrain.getAltitude(pose1))
    print("valid : ", terrain.pathIsValid(pose1, pose2))


    from PIL import Image, ImageDraw
    cellWidth = 20 # Pixels
    cellHeight = 20 # Pixels
    image = Image.new('RGB', (mapSize * cellWidth, mapSize * cellHeight), (32, 32, 32))
    def drawPose(coords, color, pointSize=1):
        imageDraw = ImageDraw.Draw(image)

            # Draw robot
        leftCoord = coords[0] * cellWidth - pointSize
        rightCoord = coords[0] * cellWidth + pointSize
        topCoord = coords[1] * cellHeight - pointSize
        bottomCoord = coords[1] * cellHeight + pointSize
        imageDraw.ellipse((leftCoord, topCoord, rightCoord, bottomCoord), fill=color)

    robotPose = Pose(random.random() * mapSize, random.random() * mapSize, random.random() * 2 * np.pi)
    print("robotPose : ", robotPose)
    for sampleIndex in range(100000) :
        samplePose = Pose(random.random() * mapSize, random.random() * mapSize, random.random() * 2 * np.pi)
        if terrain.pathIsValid(robotPose, samplePose) :
            print("Valid sample pose : ", samplePose)
            drawPose(samplePose.coordinates, (0, 255, 0))
        else :
            drawPose(samplePose.coordinates, (255, 0, 0))


    drawPose(robotPose.coordinates, (255, 255, 255), pointSize=10)

    print("Hello world !")

    image.save(f"image_{random.random()}.png")
