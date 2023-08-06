from setuptools import setup, find_packages

with open("README.md", "r", encoding = "UTF-8") as file:
    long_desc = file.read()
 
setup(
    name = "rayforge",
    version = "0.0.1",
    description = "A game engine made with RayLib.",
    long_description = long_desc,
    long_description_content_type = "text/markdown",
    url = "https://github.com/Aermoss/RayForge",
    author = "Yusuf Rencber",
    author_email = "yusufrencber546@gmail.com",
    license = "MIT",
    keywords = "",
    packages = find_packages(),
    include_package_data = True,
    install_requires = ["raylib"]
)