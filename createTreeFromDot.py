import graphviz
import os

inputPath = '/home/sparrow/Desktop/MTP/Codes/MTP_IITG/outputTrees/'
outputPath = '/home/sparrow/Desktop/MTP/Codes/MTP_IITG/outputImages/'
os.chdir(inputPath)

def generate_png_from_dot(dot_file_path, output_image_path):
    graph = graphviz.Source.from_file(dot_file_path)
    graph.format = 'png'
    graph.render(output_image_path, view=False, cleanup=True)

# Example usage
for file in os.listdir():
    dot_file_path = inputPath+file
    output_image_path = outputPath+file[:-3]+'png'
    generate_png_from_dot(dot_file_path, output_image_path)
