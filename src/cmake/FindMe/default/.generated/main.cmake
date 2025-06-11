include("${CMAKE_CURRENT_LIST_DIR}/rule.cmake")
include("${CMAKE_CURRENT_LIST_DIR}/file.cmake")

set(FindMe_default_library_list )

# Handle files with suffix s, for group default-XC32
if(FindMe_default_default_XC32_FILE_TYPE_assemble)
add_library(FindMe_default_default_XC32_assemble OBJECT ${FindMe_default_default_XC32_FILE_TYPE_assemble})
    FindMe_default_default_XC32_assemble_rule(FindMe_default_default_XC32_assemble)
    list(APPEND FindMe_default_library_list "$<TARGET_OBJECTS:FindMe_default_default_XC32_assemble>")
endif()

# Handle files with suffix S, for group default-XC32
if(FindMe_default_default_XC32_FILE_TYPE_assembleWithPreprocess)
add_library(FindMe_default_default_XC32_assembleWithPreprocess OBJECT ${FindMe_default_default_XC32_FILE_TYPE_assembleWithPreprocess})
    FindMe_default_default_XC32_assembleWithPreprocess_rule(FindMe_default_default_XC32_assembleWithPreprocess)
    list(APPEND FindMe_default_library_list "$<TARGET_OBJECTS:FindMe_default_default_XC32_assembleWithPreprocess>")
endif()

# Handle files with suffix [cC], for group default-XC32
if(FindMe_default_default_XC32_FILE_TYPE_compile)
add_library(FindMe_default_default_XC32_compile OBJECT ${FindMe_default_default_XC32_FILE_TYPE_compile})
    FindMe_default_default_XC32_compile_rule(FindMe_default_default_XC32_compile)
    list(APPEND FindMe_default_library_list "$<TARGET_OBJECTS:FindMe_default_default_XC32_compile>")
endif()

# Handle files with suffix cpp, for group default-XC32
if(FindMe_default_default_XC32_FILE_TYPE_compile_cpp)
add_library(FindMe_default_default_XC32_compile_cpp OBJECT ${FindMe_default_default_XC32_FILE_TYPE_compile_cpp})
    FindMe_default_default_XC32_compile_cpp_rule(FindMe_default_default_XC32_compile_cpp)
    list(APPEND FindMe_default_library_list "$<TARGET_OBJECTS:FindMe_default_default_XC32_compile_cpp>")
endif()

add_executable(${FindMe_default_image_name} ${FindMe_default_library_list})

target_link_libraries(${FindMe_default_image_name} PRIVATE ${FindMe_default_default_XC32_FILE_TYPE_link})

# Add the link options from the rule file.
FindMe_default_link_rule(${FindMe_default_image_name})

# Add bin2hex target for converting built file to a .hex file.
add_custom_target(FindMe_default_Bin2Hex ALL
    ${MP_BIN2HEX} ${FindMe_default_image_name})
add_dependencies(FindMe_default_Bin2Hex ${FindMe_default_image_name})

# Post build target to copy built file to the output directory.
add_custom_command(TARGET ${FindMe_default_image_name} POST_BUILD
                    COMMAND ${CMAKE_COMMAND} -E make_directory ${FindMe_default_output_dir}
                    COMMAND ${CMAKE_COMMAND} -E copy ${FindMe_default_image_name} ${FindMe_default_output_dir}/${FindMe_default_original_image_name}
                    BYPRODUCTS ${FindMe_default_output_dir}/${FindMe_default_original_image_name})
