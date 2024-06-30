import cv2 
from ultralytics import YOLO

# model = YOLO('yolov8n-25-2-24-40e.pt')  
model = YOLO("bottle_grayscale_small.pt")  
frame = cv2.imread()

igneous_rocks = ["Andesite", "Basalt", "Carbonatite", "Gabbro", "Granite",
                 "Komatiite", "Obsidian", "Pegmatite", "Porphyry", "Pumice",
                 "Pyroxenite", "Quartz_diorite", "Quartz_monzonite", "Quartzolite",
                 "Rhyolite", "Scoria", "Tephrite", "Tuff", ]
metamorphic_rocks = ["Anthracite", "Blueschist", "Eclogite", "Gneiss", "Granulite",
                     "Greenschist", "Hornfels", "Marble", "Migmatite",
                     "Phyllite", "Quartzite", "Serpentinite", "Slate",
                     "Talc_carbonate"] 
sedimentary_rocks = ["Amphibolite", "Breccia", "Chalk", "Chert", "Coal", "Conglomerate", "Diamictite", "Dolomite", 
                     "Evaporite", "Flint", "Greywacke", "Limestone",
                     "Mudstone", "Oil_shale", "Oolite", "Sandstone", "Shale",
                     "Siltstone", "Travertine", "Turbidite", "Wackestone"
                     ]
