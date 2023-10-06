// SPDX-License-Identifier: MIT
/* By Tiger3018 */

#pragma once

#include <string>
#include <vector>
#include <cstdint>

#include "yaml-cpp/yaml.h"
#include "rclcpp/rclcpp.hpp"

using std::string, std::vector, std::uint32_t;

class AssestWrapper : public YAML::Node {
  public:
    AssestWrapper(const YAML::Node & node) : YAML::Node(node) {};
    AssestWrapper(AssestWrapper & ) = default;
};

class AssestItem {
  public:
    explicit AssestItem(const string & name) : name_(name) {};
    explicit AssestItem(const string & name, const string & value) : name_(name), value_(value) {};
    explicit AssestItem(const string & name, const string & value, const string & name_i18n) : name_(name), value_(value), name_i18n_(name_i18n) {};
    AssestItem & add_child(const AssestItem & child);
    void link_wrapper(const AssestWrapper * wrapper);
    void print();
    void set(string value);
    template<typename T>
    void set(T child_parameter, string s);
    void save();

  private:
    string name_, value_, name_i18n_;
    vector<AssestItem> childs_;
    AssestWrapper * wrapper_ = NULL;

    AssestItem & search_child(string name);
    /** @tip child_order will be [0, len)
     */
    AssestItem & search_child(size_t child_order);
};

const AssestItem & ast_build(AssestItem item_node, const AssestWrapper & wrapper_node);
void ast_cmdline_loop(AssestItem item_node);

template<typename T>
void AssestItem::set(T child_parameter, string s) {
  try {
    auto child = search_child(child_parameter);
    child.set(s);
  }
  //catch (...) {
  catch (const std::exception& e) {
    //auto p = std::current_exception();
    std::cerr << "When setting value of the child, an error occured:" << e.what() << std::endl;
  }
}
