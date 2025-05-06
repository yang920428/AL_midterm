import matplotlib.pyplot as plt
import numpy as np

class LaserScanner:
    def __init__(self):
        self.scan_angles = np.array([-30, -15, 0, 15, 30])  # Fixed scan angles in degrees
        self.current_readings = np.array([100.0] * 5)  # Initialize with max range
    
    def update_readings(self, robot, obstacles, max_range=100):
        """
        Simulate laser scanner readings at fixed angles
        robot: dict with 'x', 'y', 't' (position and orientation)
        obstacles: list of (x, y, radius) tuples representing obstacles
        max_range: maximum detection range
        """
        readings = []
        robot_angle_rad = robot['t']  # Robot's current orientation in radians
        
        for angle_deg in self.scan_angles:
            # Calculate absolute beam angle in world coordinates
            beam_angle_rad = robot_angle_rad + np.deg2rad(angle_deg)
            
            # Initialize with max range
            min_distance = max_range
            
            # Check for obstacles
            for obs_x, obs_y, obs_radius in obstacles:
                # Calculate intersection between laser beam and obstacle
                distance = self._ray_circle_intersection(
                    robot['x'], robot['y'], beam_angle_rad,
                    obs_x, obs_y, obs_radius, max_range
                )
                
                if distance is not None and distance < min_distance:
                    min_distance = distance
            
            readings.append(min_distance)
        
        self.current_readings = np.array(readings)
        return self.current_readings
    
    def _ray_circle_intersection(self, x0, y0, angle_rad, cx, cy, r, max_range):
        """
        Calculate intersection between ray and circle
        Returns distance to intersection or None if no intersection
        """
        # Vector from circle center to ray origin
        dx = x0 - cx
        dy = y0 - cy
        
        # Quadratic equation coefficients
        a = np.cos(angle_rad)**2 + np.sin(angle_rad)**2  # Always 1
        b = 2 * (dx * np.cos(angle_rad) + 2 * (dy * np.sin(angle_rad)))
        c = dx**2 + dy**2 - r**2
        
        discriminant = b**2 - 4*a*c
        
        if discriminant < 0:
            return None  # no intersection
        
        sqrt_discriminant = np.sqrt(discriminant)
        t1 = (-b - sqrt_discriminant) / (2*a)
        t2 = (-b + sqrt_discriminant) / (2*a)
        
        # we want the smallest positive t
        t = None
        if t1 >= 0 and t2 >= 0:
            t = min(t1, t2)
        elif t1 >= 0:
            t = t1
        elif t2 >= 0:
            t = t2
        
        if t is not None and t <= max_range:
            return t
        return None
    
    def plot_current_scan(self, robot):
        """plot the current laser scan in robot's local coordinate frame"""
        angles_rad = np.deg2rad(self.scan_angles) + robot['t']
        distances = self.current_readings
        
        x = distances * np.cos(angles_rad) + robot['x']
        y = distances * np.sin(angles_rad) + robot['y']
        
        plt.figure(figsize=(8, 8))
        ax = plt.gca()
        
        # plot robot
        plt.plot(robot['x'], robot['y'], 'bo', markersize=10)
        
        # plot orientation
        orientation_length = 10
        end_x = robot['x'] + orientation_length * np.cos(robot['t'])
        end_y = robot['y'] + orientation_length * np.sin(robot['t'])
        plt.plot([robot['x'], end_x], [robot['y'], end_y], 'b-')
        
        # plot laser beams
        for i in range(len(self.scan_angles)):
            plt.plot([robot['x'], x[i]], [robot['y'], y[i]], 'r-', alpha=0.5)
            plt.plot(x[i], y[i], 'ro')
        
        # plot settings
        ax.set_aspect('equal')
        ax.set_xlabel('x (cm)')
        ax.set_ylabel('y (cm)')
        ax.set_title('laser scanner simulation (-30°, -15°, 0°, 15°, 30°)')
        ax.grid(True)
        
        # set axis limits based on max range
        max_dist = np.max(distances)
        ax.set_xlim(robot['x'] - max_dist - 10, robot['x'] + max_dist + 10)
        ax.set_ylim(robot['y'] - max_dist - 10, robot['y'] + max_dist + 10)
        
        plt.show()

# Example usage:
if __name__ == "__main__":
    # Create laser scanner
    scanner = LaserScanner()
    
    # Define robot position and orientation (in radians)
    robot = {'x': 150, 'y': 150, 't': np.pi/2}  # Facing "north"
    
    # Define some obstacles (x, y, radius)
    obstacles = [
        (180, 150, 10),  # Obstacle in front
        (150, 180, 10),  # Obstacle to the right
        (120, 150, 10),  # Obstacle behind
        (150, 120, 10)   # Obstacle to the left
    ]
    
    # Update and plot scan
    scanner.update_readings(robot, obstacles)
    scanner.plot_current_scan(robot)