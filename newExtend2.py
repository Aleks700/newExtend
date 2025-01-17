import os
from qgis.core import (
    QgsRasterLayer,
    QgsFeature,
    QgsGeometry,
    QgsField,
    QgsFields,
    QgsVectorFileWriter,
    QgsWkbTypes,
    QgsProject,
)
from qgis.PyQt.QtCore import QVariant


def create_individual_extent_vectors(folder_path, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for file_name in os.listdir(folder_path):
        if file_name.lower().endswith(".tif"):
            file_path = os.path.join(folder_path, file_name)
            raster = QgsRasterLayer(file_path, file_name)

            if raster.isValid():
                output_path = os.path.join(
                    output_folder, f"{os.path.splitext(file_name)[0]}_extent.shp"
                )
                fields = QgsFields()
                fields.append(QgsField("file_name", QVariant.String))
                writer = QgsVectorFileWriter(
                    output_path,
                    "UTF-8",
                    fields,
                    QgsWkbTypes.Polygon,
                    QgsProject.instance().crs(),
                    "ESRI Shapefile",
                )

                if writer.hasError() != QgsVectorFileWriter.NoError:
                    print(
                        f"Error creating shapefile for {file_name}: {writer.errorMessage()}"
                    )
                    continue

                extent = raster.extent()
                feature = QgsFeature()
                feature.setGeometry(QgsGeometry.fromRect(extent))
                feature.setAttributes([file_name])
                writer.addFeature(feature)

                del writer
                print(f"Extent shapefile created for {file_name} at: {output_path}")
            else:
                print(f"Invalid raster: {file_path}")


folder_path = (
    "\\Grphs07t\ЕРМЕК\SKO_MAXAR 2022 максар"  # Change this to your folder with TIFFs
)
output_folder = "C:\Users\A.Agadilov\Downloads\couter\Output8"  # Change this to your output folder

create_individual_extent_vectors(folder_path, output_folder)
