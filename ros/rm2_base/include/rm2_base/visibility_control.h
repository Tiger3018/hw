#ifndef RM2_BASE__VISIBILITY_CONTROL_H_
#define RM2_BASE__VISIBILITY_CONTROL_H_

// This logic was borrowed (then namespaced) from the examples on the gcc wiki:
//     https://gcc.gnu.org/wiki/Visibility

#if defined _WIN32 || defined __CYGWIN__
  #ifdef __GNUC__
    #define RM2_BASE_EXPORT __attribute__ ((dllexport))
    #define RM2_BASE_IMPORT __attribute__ ((dllimport))
  #else
    #define RM2_BASE_EXPORT __declspec(dllexport)
    #define RM2_BASE_IMPORT __declspec(dllimport)
  #endif
  #ifdef RM2_BASE_BUILDING_LIBRARY
    #define RM2_BASE_PUBLIC RM2_BASE_EXPORT
  #else
    #define RM2_BASE_PUBLIC RM2_BASE_IMPORT
  #endif
  #define RM2_BASE_PUBLIC_TYPE RM2_BASE_PUBLIC
  #define RM2_BASE_LOCAL
#else
  #define RM2_BASE_EXPORT __attribute__ ((visibility("default")))
  #define RM2_BASE_IMPORT
  #if __GNUC__ >= 4
    #define RM2_BASE_PUBLIC __attribute__ ((visibility("default")))
    #define RM2_BASE_LOCAL  __attribute__ ((visibility("hidden")))
  #else
    #define RM2_BASE_PUBLIC
    #define RM2_BASE_LOCAL
  #endif
  #define RM2_BASE_PUBLIC_TYPE
#endif

#endif  // RM2_BASE__VISIBILITY_CONTROL_H_
