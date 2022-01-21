/**
 * Copyright 2021 someone
 * @file rm2_base_node.cpp
 */
#include <cstdio>
#include <rclcpp/rclcpp.hpp>
#include <std_msgs/msg/string.hpp>
#include <geometry_msgs/msg/twist.hpp>

namespace rm2_base
{

class TestBaseMore : public rclcpp::Node
{
public:
  rclcpp::Node::SharedPtr node_;
  rclcpp::TimerBase::SharedPtr timer_;
  rclcpp::Publisher<std_msgs::msg::String>::SharedPtr pub1_;
  rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr pub2_;

  explicit TestBaseMore(const rclcpp::NodeOptions & options = rclcpp::NodeOptions())
  : rclcpp::Node("test_base_more", options)
  {
    RCLCPP_INFO_STREAM(this->get_logger(), this->get_clock()->now().nanoseconds());
    this->pub1_ = this->create_publisher<std_msgs::msg::String>("/micro_ros/test", RMW_QOS_POLICY_RELIABILITY_BEST_EFFORT);
    this->pub2_ = this->create_publisher<geometry_msgs::msg::Twist>("/turtle1/cmd_vel", RMW_QOS_POLICY_RELIABILITY_BEST_EFFORT);
    this->timer_ = this->create_wall_timer(std::chrono::milliseconds(900), std::bind(&TestBaseMore::timer_900_cb, this));
  }

  void timer_900_cb(void)
  {
    std_msgs::msg::String msg1;
    geometry_msgs::msg::Twist msg2;
    msg1.data = "host call";
    msg2.linear.x = .5;
    msg2.angular.z = .4;
    this->pub1_->publish(msg1);
    this->pub2_->publish(msg2);
    // pub2_->publish(geometry_msgs::msg::Twist({.x=.5}, {.z=.1}));
  }
  // rclcpp::node_interfaces::NodeBaseInterface::SharedPtr get_node_base_interface()
  //{
  // return node_->get_node_base_interface();
  //}
};

class TestBase
{

public:
  rclcpp::Node::SharedPtr node_;

  explicit TestBase(const rclcpp::NodeOptions & options = rclcpp::NodeOptions())
  {
    node_ = std::make_shared<rclcpp::Node>("test_base", options);
    RCLCPP_INFO_STREAM(node_->get_logger(), node_->get_clock()->now().nanoseconds());
  }
  rclcpp::node_interfaces::NodeBaseInterface::SharedPtr get_node_base_interface()
  {
    return node_->get_node_base_interface();
  }
};

}

int main(int argc, char ** argv)
{
  (void)argc;
  (void)argv;
  rclcpp::init(argc, argv);
  auto node = std::make_shared<rm2_base::TestBase>();
  // rclcpp::spin(node->get_node_base_interface());
  auto nodeReal = std::make_shared<rm2_base::TestBaseMore>();
  rclcpp::spin(nodeReal);
  rclcpp::shutdown();
  printf("hello world rm2_base package\n");
  return 0;
}
