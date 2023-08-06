#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "HELICS::helics" for configuration "Release"
set_property(TARGET HELICS::helics APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(HELICS::helics PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libhelics.3.0.1.dylib"
  IMPORTED_SONAME_RELEASE "@rpath/libhelics.3.dylib"
  )

list(APPEND _IMPORT_CHECK_TARGETS HELICS::helics )
list(APPEND _IMPORT_CHECK_FILES_FOR_HELICS::helics "${_IMPORT_PREFIX}/lib/libhelics.3.0.1.dylib" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
