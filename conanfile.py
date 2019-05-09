import os
from conans import ConanFile, CMake, tools


class TgbotcppConan(ConanFile):
    name = "tgbot-cpp"
    version = "1.1"
    license = "MIT"
    url = "https://github.com/ZaMaZaN4iK/conan-tgbot-cpp"
    description = "C++ library for Telegram bot API"
    topics = ("telegram", "api", "cpp")
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    generators = "cmake"
    homepage = "http://reo7sp.github.io/tgbot-cpp"
    author = "Alexander Zaitsev <zamazan4ik@tut.by>"
    exports = ["LICENSE.md"]      # Packages the license for the conanfile.py
    # Remove following lines if the target lib does not use cmake.
    exports_sources = ["CMakeLists.txt"]

    # Custom attributes for Bincrafters recipe conventions
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    requires = (
        "OpenSSL/1.0.2r@conan/stable",
        "zlib/1.2.11@conan/stable",
        "boost/1.70.0@conan/stable",
        "libcurl/7.64.1@bincrafters/stable"
    )

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def source(self):
        source_url = "https://github.com/reo7sp/tgbot-cpp"
        tools.get("{0}/archive/v{1}.tar.gz".format(source_url, self.version))
        extracted_dir = self.name + "-" + self.version

        # Rename to "source_subfolder" is a convention to simplify later steps
        os.rename(extracted_dir, self._source_subfolder)

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.configure(source_folder=self._source_subfolder)
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()
        # If the CMakeLists.txt has a proper install method, the steps below may be redundant
        # If so, you can just remove the lines below
        #include_folder = os.path.join(self._source_subfolder, "include")
        #self.copy(pattern="*", dst="include", src=include_folder)
        #self.copy(pattern="*.dll", dst="bin", keep_path=False)
        #self.copy(pattern="*.lib", dst="lib", keep_path=False)
        #self.copy(pattern="*.a", dst="lib", keep_path=False)
        #self.copy(pattern="*.so*", dst="lib", keep_path=False)
        #self.copy(pattern="*.dylib", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
