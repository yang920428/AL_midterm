#include "ros/ros.h"
#include "std_msgs/String.h"
#include "sensor_msgs/LaserScan.h"
#define RAD2DEG(x) ((x)*180./M_PI)


void scanCallback(const sensor_msgs::LaserScan::ConstPtr&);

int counter=0;
FILE* file = fopen("laser.txt", "w");

void callback(const ros::TimerEvent&){
  counter++;
  ROS_INFO("sample file called : %d\t times",counter);
    if (counter>300){
	fclose(file);
  }
}
void scanCallback(const sensor_msgs::LaserScan::ConstPtr& scan){
  for(int i=0;i<360;i++){
    float degree=RAD2DEG(scan->angle_min+scan->angle_increment*i);
    if(scan->ranges[i]){
      fprintf(file,"%4.1f %5.3f\n", degree,scan->ranges[i]);
    }
  }
}


int main(int argc, char **argv){

  ros::init(argc,argv,"listener");

  ros::NodeHandle n;

  ros::Timer timer1 = n.createTimer(ros::Duration(0.1),callback);
 
  ros::Subscriber sub=n.subscribe<sensor_msgs::LaserScan>("/scan",1000,scanCallback);

  ros::spin();

  return 0;
}
