// SPDX-License-Identifier: MIT
/* By Tiger3018 */

#include <functional>
#include <memory>
#include <string>
#include <iostream>
#include <fstream>
#include <exception>

#include "eie_car_software/assest.hpp"
#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

class AssestReader : public rclcpp::Node
{
  public:
    AssestReader()
    : Node("minimal_publisher"), count_(0)
    {
      publisher_ = this->create_publisher<std_msgs::msg::String>("topic", 10);
    }

  private:
    void timer_callback()
    {
      auto message = std_msgs::msg::String();
      message.data = "Hello, world! " + std::to_string(count_++);
      RCLCPP_INFO(this->get_logger(), "Publishing: '%s'", message.data.c_str());
      publisher_->publish(message);
    }
    rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_;
    size_t count_;
};

std::string g_assest_filename("/tmp/assest_file.yaml");
std::string g_global_config("Global Config");

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);

  /* See https://github.com/fujitatomoya/ros2_persist_parameter_server/blob/master/server/src/main.cpp */
  // Force flush of the stdout buffer.
  setvbuf(stdout, NULL, _IONBF, BUFSIZ);

  auto config = std::make_shared<AssestWrapper>(YAML::LoadFile(g_assest_filename));
  auto assest_ast = std::make_shared<AssestItem>(g_global_config, g_global_config, std::string("配置"));
  ast_build(*assest_ast, *config);

  ast_cmdline_loop(*assest_ast);

  //rclcpp::spin(std::make_shared<AssestReader>());
  rclcpp::shutdown();
  return 0;
}

const AssestItem & ast_build(AssestItem item_node, const AssestWrapper & wrapper_node)
{
  for(const auto & it : wrapper_node) {
    auto item_node_child = item_node.add_child(AssestItem(it.first.as<std::string>()));
    size_t count = 0;
    //item_node_child.link_wrapper(static_cast<const AssestWrapper*>(static_cast<const YAML::Node*>(std::addressof(it))));
    //std::cout << it.first.as<std::string>() << std::endl;
    using e = YAML::NodeType;
    switch(it.second.Type()) { // See <https://stackoverflow.com/a/26180736>
      case e::Scalar:
        //std::cout << it.second.as<std::string>() << std::endl;
        item_node_child.set(it.second.as<std::string>());
        break;
      case e::Sequence:
        //std::cout << it.second << std::endl;
        for(const auto & it_second_it : it.second) {
          auto item_node_superchild = item_node_child.add_child(AssestItem(std::to_string(count ++)));
          item_node_superchild.set("It's a Sequence item.");
          //item_node_superchild.link_wrapper(static_cast<const AssestWrapper*>(static_cast<const YAML::Node*>(std::addressof(item_node_child[count])));
          ast_build(item_node_superchild, it_second_it);
        }
        item_node_child.set("It's a Sequence.");
        break;
      case e::Map:
        ast_build(item_node_child, it.second);
        item_node_child.set("It's a Map.");
        break;
      case e::Undefined:
        break;
      case e::Null:
        break;
    }
    //item_node_child.link_wrapper(static_cast<const AssestWrapper*>(static_cast<const YAML::Node*>(&it)));
  }
  return item_node;
}

void ast_cmdline_loop(AssestItem item_node)
{
  return;
}

AssestItem & AssestItem::add_child(const AssestItem & child)
{
  childs_.push_back(child);
  return childs_.back();
}

void AssestItem::link_wrapper(const AssestWrapper * wrapper)
{
  std::cout << value_ << std::endl;
  if(wrapper == NULL) {
    throw "NULL pointer";
  }
  wrapper_ = const_cast<AssestWrapper*>(wrapper);
}

void AssestItem::set(string value) // TODO not safe
{
  value_ = value;
  if(wrapper_ != NULL && 1/*wrapper_->IsScalar()*/) {
    //std::cout << value << "(-->" << wrapper_ << std::endl;
    //std::cout << value << "(-->" << wrapper_->size() << std::endl;
    for(auto && it : *wrapper_) {
    }
    //*wrapper_ = YAML::Node(value_);
  }
}

AssestItem & AssestItem::search_child(string name) {
  for(const auto & it: childs_) {
    if(it.name_ == name) {
      return const_cast<AssestItem&>(it);
    }
  }
  throw "No match name.";
}

AssestItem & AssestItem::search_child(size_t child_order) {
  if(child_order >= childs_.size()) {
    throw "Order number oversize.";
  }
  return childs_[child_order];
}

void AssestItem::save() {
  if(name_ == g_global_config) {
    std::ofstream fout(g_assest_filename);
    fout << *wrapper_;
  }
  else {
    std::ofstream fout(g_assest_filename + name_ + ".yaml");
    fout << *wrapper_;
  }
}
