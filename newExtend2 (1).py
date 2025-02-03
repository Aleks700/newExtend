import os
import glob
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

def create_extent_vectors_recursive(folder_path, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Рекурсивный поиск всех .tif файлов в подпапках
    tif_files = glob.glob(os.path.join(folder_path, "**", "*.tif"), recursive=True)
    
    for file_path in tif_files:
        file_name = os.path.basename(file_path)
        
        if 'IMAGE' in file_name:
            continue
        
        raster = QgsRasterLayer(file_path, file_name)

        if raster.isValid():
            relative_path = os.path.relpath(file_path, folder_path)
            output_subfolder = os.path.join(output_folder, os.path.dirname(relative_path))
            if not os.path.exists(output_subfolder):
                os.makedirs(output_subfolder)
            
            output_path = os.path.join(output_subfolder, f"{os.path.splitext(file_name)[0]}_extent.shp")
            
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
                print(f"Error creating shapefile for {file_name}: {writer.errorMessage()}")
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


# Использование
create_extent_vectors_recursive(r"T:\december_dtm", r"E:\03-Shapes\JHIFJHSDODHSOGH")
